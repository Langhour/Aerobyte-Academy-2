import json
import os
import re
import unicodedata
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, File, Form, HTTPException, Request, Response, UploadFile, status, Query
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel

from app.content_store import (
    create_print_order,
    get_print_order,
    get_user_print_orders,
    list_all_print_orders,
    update_print_order_status,
    update_print_order_price,
    update_print_order_payment_status,
    delete_print_order,
    save_print_order_review,
    list_completed_print_reviews,
    save_uploaded_file,
    get_uploaded_file,
    find_user_by_id,
)

router = APIRouter(tags=["Print Orders"])

UPLOAD_DIRECTORY = Path(__file__).resolve().parents[2] / "data" / "uploads"
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
CAMBODIA_TZ = timezone(timedelta(hours=7))


def _require_admin(request: Request) -> None:
    if request.session.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin sign-in required")


def _sanitize_filename(name: str) -> str:
    cleaned = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    cleaned = re.sub(r"[^\w.\-]+", "_", cleaned).strip("._")
    return cleaned or "cad_model.stl"


def _format_size(num_bytes: int) -> str:
    if num_bytes < 1024:
        return f"{num_bytes} B"
    elif num_bytes < 1024 * 1024:
        return f"{num_bytes / 1024:.1f} KB"
    else:
        return f"{num_bytes / (1024 * 1024):.1f} MB"


class StatusUpdatePayload(BaseModel):
    status: str


class PriceUpdatePayload(BaseModel):
    price: float


class PaymentStatusUpdatePayload(BaseModel):
    payment_status: str


class ReviewPayload(BaseModel):
    rating: int = 5
    comment: Optional[str] = ""
    tags: Optional[list[str]] = []
    reviewer_name: Optional[str] = ""


# =========================================================================
# PUBLIC ENDPOINTS: Create Print Order & Download CAD Files
# =========================================================================

@router.post("/api/print-orders")
async def submit_print_order(
    request: Request,
    order_data: str = Form(...),
    files: list[UploadFile] = File(default=[]),
    qr_file: Optional[UploadFile] = File(default=None),
):
    """
    Submits a new 3D print quote inquiry with customer CAD files (.stl, .obj, .step, .3mf)
    and optional Telegram QR code screenshot.
    """
    try:
        parsed_data = json.loads(order_data) if isinstance(order_data, str) else order_data
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid order_data JSON: {str(exc)}"
        )

    client_files_meta = parsed_data.get("files", [])
    saved_files = []

    # 1. Process and store uploaded 3D CAD files
    for idx, f in enumerate(files):
        data = await f.read()
        clean_name = _sanitize_filename(f.filename or f"cad_part_{idx + 1}.stl")
        stored_filename = f"print_{uuid4().hex[:10]}_{clean_name}"
        target_path = UPLOAD_DIRECTORY / stored_filename

        try:
            target_path.write_bytes(data)
        except Exception:
            pass

        # Also persist to SQLite uploaded_files
        try:
            save_uploaded_file(stored_filename, f.content_type or "application/octet-stream", data)
        except Exception:
            pass

        meta = client_files_meta[idx] if idx < len(client_files_meta) else {}
        quantity = int(meta.get("quantity") or 1)
        dimensions = meta.get("dimensions") or {"x": 50, "y": 50, "z": 20}
        volume_cm3 = float(meta.get("volumeCm3") or meta.get("volume_cm3") or 15.0)

        saved_files.append({
            "id": f"file-{uuid4().hex[:8]}",
            "original_name": f.filename or clean_name,
            "stored_filename": stored_filename,
            "download_url": f"/api/print-orders/files/{stored_filename}?name={clean_name}",
            "size_str": _format_size(len(data)),
            "size_bytes": len(data),
            "quantity": quantity,
            "dimensions": dimensions,
            "volume_cm3": volume_cm3,
            "material": meta.get("material") or "PLA / Custom",
        })

    # If user used sample presets or simulated files without native File binary
    if not saved_files and client_files_meta:
        for idx, meta in enumerate(client_files_meta):
            clean_name = _sanitize_filename(meta.get("name") or f"model_{idx + 1}.stl")
            stored_filename = f"sample_{clean_name}"
            saved_files.append({
                "id": f"file-{uuid4().hex[:8]}",
                "original_name": meta.get("name") or clean_name,
                "stored_filename": stored_filename,
                "download_url": f"/api/print-orders/files/{stored_filename}?name={clean_name}",
                "size_str": meta.get("sizeStr") or "2.5 MB",
                "size_bytes": 2500000,
                "quantity": int(meta.get("quantity") or 1),
                "dimensions": meta.get("dimensions") or {"x": 45, "y": 45, "z": 12},
                "volume_cm3": float(meta.get("volumeCm3") or meta.get("volume_cm3") or 14.5),
                "material": meta.get("material") or "PLA / Custom",
            })

    # 2. Process Telegram QR code image if attached
    qr_file_url = ""
    if qr_file:
        qr_bytes = await qr_file.read()
        qr_clean = _sanitize_filename(qr_file.filename or "telegram_qr.png")
        qr_stored = f"qr_{uuid4().hex[:10]}_{qr_clean}"
        qr_path = UPLOAD_DIRECTORY / qr_stored
        try:
            qr_path.write_bytes(qr_bytes)
        except Exception:
            pass
        try:
            save_uploaded_file(qr_stored, qr_file.content_type or "image/png", qr_bytes)
        except Exception:
            pass
        qr_file_url = f"/uploads/{qr_stored}"

    total_parts = sum(f.get("quantity", 1) for f in saved_files) if saved_files else 1
    est_price = float(parsed_data.get("estimated_price") or 0.0)

    # Detect user account context from session or payload
    session_uid = request.session.get("user_id") if request.session.get("role") == "user" else None
    session_email = (request.session.get("email") or "").strip().lower() if request.session.get("role") == "user" else ""
    user_id = session_uid or parsed_data.get("user_id") or ""
    user_email = session_email or (parsed_data.get("user_email") or parsed_data.get("email") or "").strip().lower()
    if user_id and not user_email:
        user = find_user_by_id(user_id)
        if user:
            user_email = (user.get("email") or "").strip().lower()

    # 3. Create Order Record in Database
    created_order = create_print_order({
        "customer_name": parsed_data.get("name") or parsed_data.get("customer_name") or "",
        "phone": parsed_data.get("phone") or "",
        "telegram": parsed_data.get("telegram") or "",
        "notes": parsed_data.get("notes") or "",
        "qr_file_url": qr_file_url or parsed_data.get("qr_file_url") or "",
        "total_parts": total_parts,
        "estimated_price": est_price,
        "files_json": saved_files,
        "status": "Pending Review",
        "user_id": user_id,
        "user_email": user_email,
    })

    return {
        "success": True,
        "order": created_order,
        "message": "3D print order received successfully."
    }


@router.get("/api/print-orders/my-orders")
async def get_my_print_orders(
    request: Request,
    user_id: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    telegram: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
    order_ids: Optional[str] = Query(None),
):
    session_uid = request.session.get("user_id") if request.session.get("role") == "user" else None
    session_email = (request.session.get("email") or "").strip().lower() if request.session.get("role") == "user" else ""
    session_name = request.session.get("user_name") or ""
    uid = session_uid or user_id
    uemail = session_email or (email.strip().lower() if email else "")

    user = None
    if uid:
        user = find_user_by_id(uid)
    elif uemail:
        user = find_user_by_email(uemail)

    if user:
        if not uemail:
            uemail = (user.get("email") or "").strip().lower()
        if not session_name:
            session_name = user.get("full_name") or ""
        if not telegram and user.get("telegram"):
            telegram = user.get("telegram")

    customer_name = name or session_name or None
    ids_list = [x.strip() for x in order_ids.split(",") if x.strip()] if order_ids else None

    orders = get_user_print_orders(
        user_id=uid,
        email=uemail,
        customer_name=customer_name,
        telegram=telegram,
        order_ids=ids_list,
    )
    return {"orders": orders}


@router.get("/api/print-orders/{order_id}")
async def get_public_print_order(order_id: str):
    """
    Returns single print order details and live production status for customers.
    """
    clean_id = str(order_id).strip().lstrip("#")
    order = get_print_order(clean_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Print order not found")
    return {"order": order}


@router.post("/api/print-orders/{order_id}/review")
async def submit_print_order_review(
    order_id: str,
    payload: ReviewPayload,
    request: Request,
):
    """
    Allows a customer to submit or update a review on their completed 3D print order.
    """
    clean_id = order_id.strip()
    order = get_print_order(clean_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Print order not found")

    # Validate rating between 1 and 5
    rating = max(1, min(5, int(payload.rating)))

    # Session context if logged in
    session_user = request.session.get("user") or {}
    reviewer_name = payload.reviewer_name or session_user.get("full_name") or order.get("customer") or "Customer"

    review_dict = {
        "rating": rating,
        "comment": (payload.comment or "").strip(),
        "tags": [str(t).strip() for t in (payload.tags or []) if str(t).strip()],
        "reviewer_name": reviewer_name,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    updated_order = save_print_order_review(clean_id, review_dict)
    if not updated_order:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not save review")

    return {
        "success": True,
        "order": updated_order,
        "message": "Review submitted successfully"
    }


@router.get("/api/print-orders/reviews")
async def get_print_order_reviews(limit: int = Query(20, ge=1, le=100)):
    """
    Returns public verified customer reviews for 3D print orders.
    """
    reviews = list_completed_print_reviews(limit=limit)
    return {"reviews": reviews}


@router.get("/api/print-orders/files/{filename}")
async def download_print_file(filename: str, name: Optional[str] = Query(None)):
    """
    Direct download endpoint for user-dropped 3D CAD files (.stl, .obj, .step, .3mf).
    Forces attachment download with original user-friendly filename.
    """
    safe_stored = Path(filename).name
    file_path = UPLOAD_DIRECTORY / safe_stored
    download_filename = name or safe_stored

    if file_path.exists() and file_path.stat().st_size > 0:
        return FileResponse(
            path=str(file_path),
            filename=download_filename,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f'attachment; filename="{download_filename}"'},
        )

    # Check DB uploaded_files
    row = get_uploaded_file(safe_stored)
    if row and row.get("data"):
        data = row["data"]
        # Cache to disk for subsequent requests
        try:
            file_path.write_bytes(data)
        except Exception:
            pass
        return Response(
            content=data,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f'attachment; filename="{download_filename}"'},
        )

    # Fallback for seeded sample files: generate a valid minimal ASCII STL 3D mesh
    stl_ascii = (
        f"solid {download_filename}\n"
        "  facet normal 0 0 1\n"
        "    outer loop\n"
        "      vertex 0 0 0\n"
        "      vertex 10 0 0\n"
        "      vertex 0 10 0\n"
        "    endloop\n"
        "  endfacet\n"
        f"endsolid {download_filename}\n"
    ).encode("utf-8")

    return Response(
        content=stl_ascii,
        media_type="application/sla",
        headers={"Content-Disposition": f'attachment; filename="{download_filename}"'},
    )


# =========================================================================
# ADMIN ENDPOINTS: View Orders, Download Dropped Files & Update Status
# =========================================================================

@router.get("/api/admin/print-orders")
async def admin_list_print_orders(request: Request):
    """
    Returns all customer print inquiries and dropped files for the admin portal.
    """
    _require_admin(request)
    orders = list_all_print_orders(limit=200)
    return {"orders": orders}


@router.get("/api/admin/print-orders/{order_id}")
async def admin_get_print_order(order_id: str, request: Request):
    """
    Returns single print order details with CAD files metadata.
    """
    _require_admin(request)
    order = get_print_order(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Print order not found")
    return {"order": order}


@router.put("/api/admin/print-orders/{order_id}/status")
async def admin_update_print_order_status(
    order_id: str,
    payload: StatusUpdatePayload,
    request: Request
):
    """
    Updates the production status of a 3D print order.
    """
    _require_admin(request)
    clean_id = str(order_id).strip().lstrip("#")
    success = update_print_order_status(clean_id, payload.status)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return {"success": True, "order_id": clean_id, "status": payload.status}


@router.put("/api/admin/print-orders/{order_id}/price")
async def admin_update_print_order_price(
    order_id: str,
    payload: PriceUpdatePayload,
    request: Request,
):
    """
    Updates the quote price of a 3D print order.
    """
    _require_admin(request)
    clean_id = str(order_id).strip().lstrip("#")
    success = update_print_order_price(clean_id, payload.price)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return {"success": True, "order_id": clean_id, "price": payload.price}


@router.put("/api/admin/print-orders/{order_id}/payment-status")
async def admin_update_print_order_payment_status(
    order_id: str,
    payload: PaymentStatusUpdatePayload,
    request: Request,
):
    """
    Updates the payment status of a 3D print order ('Paid' or 'Not Paid').
    """
    _require_admin(request)
    clean_id = str(order_id).strip().lstrip("#")
    success = update_print_order_payment_status(clean_id, payload.payment_status)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return {"success": True, "order_id": clean_id, "payment_status": payload.payment_status}


@router.delete("/api/admin/print-orders/{order_id}")
async def admin_delete_print_order(order_id: str, request: Request):
    """
    Removes a print order inquiry.
    """
    _require_admin(request)
    success = delete_print_order(order_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return {"success": True, "deleted": order_id}
