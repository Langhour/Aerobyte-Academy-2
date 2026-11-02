import os
import re
import secrets
import unicodedata
from datetime import datetime, timezone, timedelta
from pathlib import Path

CAMBODIA_TZ = timezone(timedelta(hours=7))
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, Request, Response, UploadFile, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlite3 import IntegrityError

from app.admin_security import admin_configuration_ready, verify_admin_credentials
from app.user_security import hash_user_password
from app.content_store import (
    get_traffic_summary, list_login_logs, list_visit_logs, log_login_event,
    create_course, delete_course, delete_coupon, find_coupon, find_course, find_enrollment,
    get_site_settings, increment_coupon_usage, list_admin_activity, list_coupons,
    list_courses, list_enrollments, log_admin_activity, reorder_courses, save_course,
    save_coupon, save_uploaded_file, save_enrollment, save_site_settings,
    list_users, find_user_by_id, find_user_by_email, admin_update_user,
    admin_set_user_password, admin_delete_user,
)
from app.models import BatchSchedule, Course, CourseModule, CourseReorderRequest, Coupon, HardwareSpec, PaymentStatusEvent, SiteSettings


router = APIRouter(prefix="/api/admin", tags=["Admin"])
UPLOAD_DIRECTORY = Path(__file__).resolve().parents[2] / "data" / "uploads"
MAX_IMAGE_BYTES = 5 * 1024 * 1024


class AdminLogin(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=256)


class CourseInput(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    slug: Optional[str] = Field(default=None, max_length=180)
    short_description: str = Field(default="", max_length=2000)
    category: str = Field(min_length=1, max_length=80)
    section_group: str = Field(default="Courses", max_length=80)
    level: Optional[str] = Field(default=None, max_length=80)
    price: float = Field(ge=0, le=1_000_000)
    original_price: Optional[float] = Field(default=None, ge=0, le=1_000_000)
    language: Optional[str] = Field(default="English", max_length=80)
    duration: Optional[str] = Field(default=None, max_length=120)
    image_url: str = Field(default="", max_length=2000)
    status: str = Field(default="published", pattern="^(published|draft|archived)$")
    badges: list[str] = Field(default_factory=list, max_length=20)
    batch_schedules: list[BatchSchedule] = Field(default_factory=list, max_length=100)
    modules: list[CourseModule] = Field(default_factory=list, max_length=100)
    hardware_specs: list[HardwareSpec] = Field(default_factory=list, max_length=100)
    title_kh: Optional[str] = Field(default=None, max_length=200)
    short_description_kh: Optional[str] = Field(default=None, max_length=3000)
    category_kh: Optional[str] = Field(default=None, max_length=100)
    level_kh: Optional[str] = Field(default=None, max_length=100)
    duration_kh: Optional[str] = Field(default=None, max_length=150)
    badges_kh: list[str] = Field(default_factory=list, max_length=20)

class StatusUpdate(BaseModel):
    status: str

class EnrollmentStatusUpdate(BaseModel):
    status: str = Field(pattern="^(pending|confirmed|cancelled)$")


class AdminUserUpdate(BaseModel):
    full_name: str = Field(min_length=1, max_length=120)
    email: str = Field(min_length=3, max_length=254)
    phone: Optional[str] = None
    telegram: Optional[str] = None
    date_of_birth: Optional[str] = None
    location: Optional[str] = None
    qualification: Optional[str] = None
    qualification_other: Optional[str] = None
    occupation: Optional[str] = None
    experience: Optional[str] = None
    is_verified: bool = True


class AdminUserPasswordChange(BaseModel):
    password: str = Field(min_length=8, max_length=256)


def _require_admin(request: Request) -> None:
    if request.session.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin sign-in required")


def _slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", normalized.casefold()).strip("-")
    return slug or f"course-{uuid4().hex[:8]}"


def _course_from_input(payload: CourseInput, course_id: Optional[str] = None) -> Course:
    slug = _slugify(payload.slug or payload.title)
    original_price = payload.original_price
    discount = 0
    if original_price and original_price > payload.price:
        discount = round((1 - payload.price / original_price) * 100)

    return Course(
        id=course_id or f"course-{uuid4()}",
        slug=slug,
        title=payload.title.strip(),
        short_description=payload.short_description.strip(),
        category=payload.category.strip(),
        section_group=payload.section_group.strip(),
        level=payload.level.strip() if payload.level else None,
        price=payload.price,
        original_price=original_price if original_price and original_price > payload.price else None,
        discount_badge=f"{discount}% OFF" if discount else None,
        language=payload.language.strip() if payload.language else None,
        duration=payload.duration.strip() if payload.duration else None,
        image_url=payload.image_url.strip(),
        status=payload.status,
        badges=payload.badges,
        batch_schedules=payload.batch_schedules,
        modules=payload.modules,
        hardware_specs=payload.hardware_specs,
        title_kh=(payload.title_kh or "").strip() or None,
        short_description_kh=(payload.short_description_kh or "").strip() or None,
        category_kh=(payload.category_kh or "").strip() or None,
        level_kh=(payload.level_kh or "").strip() or None,
        duration_kh=(payload.duration_kh or "").strip() or None,
        badges_kh=payload.badges_kh or [],
    )

def _log(action: str, details: str) -> None:
    log_admin_activity(action, details, datetime.now(CAMBODIA_TZ).strftime("%b %d, %Y %I:%M %p"))


@router.post("/login")
def login(payload: AdminLogin, request: Request):
    if not admin_configuration_ready():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admin sign-in is not configured on the server.",
        )
    if not verify_admin_credentials(payload.email, payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
    request.session.clear()
    request.session["role"] = "admin"
    request.session["csrf"] = secrets.token_urlsafe(24)
    try:
        forwarded = request.headers.get("x-forwarded-for")
        ip = forwarded.split(",")[0].strip() if forwarded else (request.client.host if request.client else "Unknown")
        ua = request.headers.get("user-agent", "Unknown")
        log_login_event(
            user_id="admin",
            user_email=payload.email,
            user_name="Administrator",
            role="Admin",
            login_method="Admin Portal",
            ip_address=ip,
            user_agent=ua,
            status="success",
        )
    except Exception:
        pass
    return {"authenticated": True, "csrf_token": request.session["csrf"]}


@router.get("/session")
def get_session(request: Request):
    _require_admin(request)
    return {"authenticated": True, "csrf_token": request.session.get("csrf", "")}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request):
    request.session.clear()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/courses", response_model=list[Course])
def admin_list_courses(request: Request):
    _require_admin(request)
    return list_courses()


@router.post("/courses", response_model=Course, status_code=status.HTTP_201_CREATED)
def admin_create_course(payload: CourseInput, request: Request):
    _require_admin(request)
    course = _course_from_input(payload)
    try:
        create_course(course)
    except IntegrityError as exc:
        raise HTTPException(status_code=409, detail="A course with that slug already exists.") from exc
    _log("Course created", course.title)
    return course


@router.put("/courses/reorder", response_model=list[Course])
def admin_reorder_courses(payload: CourseReorderRequest, request: Request):
    _require_admin(request)
    reorder_courses(payload.course_ids)
    _log("Courses reordered", f"{len(payload.course_ids)} courses rearranged")
    return list_courses()


@router.put("/courses/{course_id}", response_model=Course)
def admin_update_course(course_id: str, payload: CourseInput, request: Request):
    _require_admin(request)
    existing = find_course(course_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Course not found.")
    course = _course_from_input(payload, course_id=existing.id)
    try:
        save_course(course)
    except IntegrityError as exc:
        raise HTTPException(status_code=409, detail="A course with that slug already exists.") from exc
    _log("Course updated", course.title)
    return course


@router.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_course(course_id: str, request: Request):
    _require_admin(request)
    if not delete_course(course_id):
        raise HTTPException(status_code=404, detail="Course not found.")
    _log("Course deleted", course_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/images", status_code=status.HTTP_201_CREATED)
@router.post("/course-images", status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def upload_image(
    request: Request,
    image: UploadFile = File(...),
):
    _require_admin(request)
    contents = await image.read(MAX_IMAGE_BYTES + 1)
    if len(contents) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=413, detail="Image must be 5 MB or smaller.")
    if contents.startswith(b"\x89PNG\r\n\x1a\n"):
        extension = ".png"
        media_type = "image/png"
    elif contents.startswith(b"\xff\xd8\xff"):
        extension = ".jpg"
        media_type = "image/jpeg"
    else:
        raise HTTPException(status_code=415, detail="Only PNG and JPG/JPEG images are supported.")
    UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4().hex}{extension}"
    (UPLOAD_DIRECTORY / filename).write_bytes(contents)
    save_uploaded_file(filename, media_type, contents)
    _log("Admin image uploaded", filename)
    api_origin = os.getenv("BACKEND_API_ORIGIN", "").rstrip("/")
    image_url = f"{api_origin}/uploads/{filename}" if api_origin else f"/uploads/{filename}"
    return {"image_url": image_url, "content_type": media_type}


@router.get("/overview")
def admin_overview(request: Request):
    _require_admin(request)
    enrollments = list_enrollments()
    paid = [record for record in enrollments if record.status == "paid"]
    return {
        "total_revenue": round(sum(record.amount_due for record in paid), 2),
        "active_enrollments": sum(record.enrollment_status == "confirmed" for record in enrollments),
        "pending_qr_scans": sum(record.status == "pending" for record in enrollments),
        "published_courses": sum(course.status == "published" for course in list_courses()),
        "recent_enrollments": [record.model_dump() for record in enrollments[:10]],
        "top_courses": _top_courses(enrollments),
        "activity": list_admin_activity(),
    }


def _top_courses(enrollments):
    totals = {}
    for record in enrollments:
        totals[record.course_title] = totals.get(record.course_title, 0) + 1
    return [
        {"title": title, "enrollments": count}
        for title, count in sorted(totals.items(), key=lambda item: (-item[1], item[0]))[:5]
    ]


@router.get("/enrollments")
def admin_enrollments(request: Request):
    _require_admin(request)
    return [record.model_dump() for record in list_enrollments()]


@router.put("/enrollments/{enrollment_id}/status")
def admin_update_enrollment_status(
    enrollment_id: str, payload: EnrollmentStatusUpdate, request: Request
):
    _require_admin(request)
    record = find_enrollment(enrollment_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Enrollment not found.")
    record.enrollment_status = payload.status
    event_time = datetime.now(CAMBODIA_TZ).strftime("%b %d, %Y %I:%M %p")
    if payload.status == "confirmed":
        if record.status != "paid":
            record.status = "paid"
            record.payment_history.append(
                PaymentStatusEvent(
                    status="paid",
                    created_at=event_time,
                    note="Administrator confirmed enrollment and verified payment",
                )
            )
    elif payload.status == "cancelled":
        if record.status not in {"refunded", "expired"}:
            record.status = "expired"
            record.payment_history.append(
                PaymentStatusEvent(
                    status="expired",
                    created_at=event_time,
                    note="Administrator cancelled enrollment",
                )
            )
    elif payload.status == "pending":
        if record.status == "paid":
            record.status = "pending"
            record.payment_history.append(
                PaymentStatusEvent(
                    status="pending",
                    created_at=event_time,
                    note="Administrator reset enrollment to pending",
                )
            )
    save_enrollment(record)
    _log("Enrollment status changed", f"{enrollment_id}: {payload.status} (payment status: {record.status})")
    return record.model_dump()


@router.get("/enrollments/export")
def export_enrollments(request: Request, format: str = "excel"):
    _require_admin(request)
    records = list_enrollments()
    columns = [
        "enrollment_id", "student_name", "gender", "date_of_birth", "email",
        "phone_number", "phone_telegram", "course_title", "age_range",
        "highest_qualification", "current_occupation", "preferred_schedule",
        "preferred_start_date", "original_price", "discount_amount", "base_price",
        "administration_fee", "certification_fee", "card_fee", "amount_due",
        "enrollment_status", "status", "created_at",
    ]

    headers = [
        "Enrollment ID", "Student Name", "Gender", "Date of Birth", "Email",
        "Phone Number", "Telegram Username", "Course Title", "Age Range",
        "Highest Qualification", "Current Occupation / School", "Schedule",
        "Preferred Start Date", "Original Price ($)", "Discount ($)", "Base Price ($)",
        "Admin Fee ($)", "Cert Fee ($)", "Card Fee ($)", "Total Amount Due ($)",
        "Enrollment Status", "Payment Status", "Created At",
    ]

    if format == "csv":
        def rows():
            import csv
            import io

            def csv_value(value):
                text = "" if value is None else str(value)
                if text.lstrip().startswith(("=", "+", "-", "@")):
                    return f"'{text}"
                return text

            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(headers)
            yield output.getvalue()
            for record in records:
                output.seek(0)
                output.truncate(0)
                writer.writerow([csv_value(getattr(record, column)) for column in columns])
                yield output.getvalue()

        return StreamingResponse(
            rows(),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=aerobyte-enrollments.csv"},
        )

    # Export as Excel (.xlsx) using openpyxl
    import io
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Student Enrollments"

    ws.append(headers)

    header_fill = PatternFill(start_color="102A49", end_color="102A49", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    thin_border = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )

    ws.row_dimensions[1].height = 26
    for col_idx in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    for record in records:
        row_data = []
        for col in columns:
            val = getattr(record, col, "")
            if val is None:
                val = ""
            row_data.append(val)
        ws.append(row_data)

    for row_idx, row in enumerate(ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=len(headers)), start=2):
        fill_color = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
        row_fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")
        for cell in row:
            cell.fill = row_fill
            cell.border = thin_border
            cell.font = Font(name="Calibri", size=10)
            cell.alignment = Alignment(vertical="center")

    for col_idx, col_cells in enumerate(ws.columns, start=1):
        max_len = max(len(str(cell.value or '')) for cell in col_cells)
        col_letter = get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=aerobyte-enrollments.xlsx"},
    )


@router.get("/payments")
def admin_payments(request: Request):
    _require_admin(request)
    return [record.model_dump() for record in list_enrollments()]


@router.put("/payments/{enrollment_id}/status")
def admin_update_payment_status(
    enrollment_id: str, payload: StatusUpdate, request: Request
):
    _require_admin(request)
    if payload.status not in {"pending", "paid", "expired", "refunded"}:
        raise HTTPException(status_code=422, detail="Unsupported payment status.")
    record = find_enrollment(enrollment_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Payment not found.")
    if record.status != payload.status:
        record.payment_history.append(
            PaymentStatusEvent(
                status=payload.status,
                created_at=datetime.now(CAMBODIA_TZ).strftime("%b %d, %Y %I:%M %p"),
                note="Administrator verified payment status",
            )
        )
    record.status = payload.status
    if payload.status == "paid":
        record.enrollment_status = "confirmed"
    elif payload.status in {"expired", "refunded"}:
        record.enrollment_status = "cancelled"
    elif payload.status == "pending":
        record.enrollment_status = "pending"
    save_enrollment(record)
    _log("Payment status changed", f"{record.transaction_id}: {payload.status}")
    return record.model_dump()


@router.get("/coupons", response_model=list[Coupon])
def admin_coupons(request: Request):
    _require_admin(request)
    return list_coupons()


@router.post("/coupons", response_model=Coupon, status_code=status.HTTP_201_CREATED)
def admin_create_coupon(payload: Coupon, request: Request):
    _require_admin(request)
    coupon = payload.model_copy(update={"code": payload.code.strip().upper()})
    if find_coupon(coupon.code):
        raise HTTPException(status_code=409, detail="Coupon code already exists.")
    try:
        save_coupon(coupon)
    except IntegrityError as exc:
        raise HTTPException(status_code=409, detail="Coupon code already exists.") from exc
    _log("Coupon saved", coupon.code)
    return coupon


@router.put("/coupons/{code}", response_model=Coupon)
def admin_update_coupon(code: str, payload: Coupon, request: Request):
    _require_admin(request)
    existing = next((item for item in list_coupons() if item.code == code.upper()), None)
    if existing is None:
        raise HTTPException(status_code=404, detail="Coupon not found.")
    coupon = payload.model_copy(update={
        "code": code.upper(),
        "usage_count": existing.usage_count,
    })
    save_coupon(coupon)
    _log("Coupon updated", coupon.code)
    return coupon


@router.delete("/coupons/{code}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_coupon(code: str, request: Request):
    _require_admin(request)
    if not delete_coupon(code):
        raise HTTPException(status_code=404, detail="Coupon not found.")
    _log("Coupon deleted", code.upper())
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/settings", response_model=SiteSettings)
def admin_get_settings(request: Request):
    _require_admin(request)
    return get_site_settings()


@router.put("/settings", response_model=SiteSettings)
def admin_update_settings(payload: SiteSettings, request: Request):
    _require_admin(request)
    save_site_settings(payload)
    _log("Site settings updated", "Public site settings saved")
    return payload

@router.get("/logs/analytics")
def admin_logs_analytics(request: Request):
    _require_admin(request)
    return get_traffic_summary()


@router.get("/logs/logins")
def admin_login_logs(request: Request, role: Optional[str] = None, limit: int = 100):
    _require_admin(request)
    return list_login_logs(limit=limit, role=role)


@router.get("/logs/visits")
def admin_visit_logs(request: Request, limit: int = 100):
    _require_admin(request)
    return list_visit_logs(limit=limit)


@router.get("/users")
def admin_list_users(request: Request):
    _require_admin(request)
    return list_users()


@router.put("/users/{user_id}")
def admin_update_user_endpoint(user_id: str, payload: AdminUserUpdate, request: Request):
    _require_admin(request)
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    clean_email = payload.email.strip().casefold()
    if clean_email != user["email"].strip().casefold():
        existing = find_user_by_email(clean_email)
        if existing and existing["id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )

    profile_data = {
        "phone": (payload.phone or "").strip()[:50],
        "telegram": (payload.telegram or "").strip()[:80],
        "date_of_birth": (payload.date_of_birth or "").strip()[:30],
        "location": (payload.location or "").strip()[:100],
        "qualification": (payload.qualification or "").strip()[:100],
        "qualification_other": (payload.qualification_other or "").strip()[:100],
        "occupation": (payload.occupation or "").strip()[:100],
        "experience": (payload.experience or "").strip()[:100],
    }
    try:
        updated = admin_update_user(
            user_id=user_id,
            email=clean_email,
            full_name=payload.full_name.strip(),
            is_verified=1 if payload.is_verified else 0,
            profile_data=profile_data,
        )
        _log("Update user", f"Updated profile for user {clean_email} ({user_id})")
        return updated
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email is already in use."
        ) from exc


@router.put("/users/{user_id}/password")
def admin_change_user_password_endpoint(
    user_id: str, payload: AdminUserPasswordChange, request: Request
):
    _require_admin(request)
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    password_hash = hash_user_password(payload.password)
    success = admin_set_user_password(user_id, password_hash)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update password.",
        )

    _log("Reset user password", f"Updated password for user {user['email']} ({user_id})")
    return {"message": "User password updated successfully."}


@router.delete("/users/{user_id}")
def admin_delete_user_endpoint(user_id: str, request: Request):
    _require_admin(request)
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    success = admin_delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user.",
        )

    _log("Delete user", f"Deleted user account {user['email']} ({user_id})")
    return {"message": "User deleted successfully."}

