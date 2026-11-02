from pydantic import BaseModel
from typing import Optional
import os
import secrets
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Response, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from app.content_store import find_user_by_id, get_uploaded_file, initialize_content_store, log_visit_event
from app.routers import accounts, admin, courses, enrollment, google_auth, public


def _load_local_environment() -> None:
    environment_file = Path(__file__).resolve().parents[1] / ".env"
    if not environment_file.exists():
        return
    for line in environment_file.read_text(encoding="utf-8").splitlines():
        key, separator, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if separator and key and not key.startswith("#") and key not in os.environ:
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
                value = value[1:-1]
            os.environ[key] = value


_load_local_environment()

app = FastAPI(
    title="AeroByte Academy API",
    description="Backend API for AeroByte Academy E-Learning & Robotics Platform",
    version="1.0.0"
)

def _resolve_allowed_origins() -> list[str]:
    origins = {
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "http://localhost:8010",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:8010",
    }
    raw = os.getenv("FRONTEND_ORIGINS", "")
    for item in raw.split(","):
        trimmed = item.strip().rstrip("/")
        if trimmed:
            origins.add(trimmed)

    for env_var in ("FRONTEND_URL", "RENDER_EXTERNAL_URL", "RAILWAY_PUBLIC_DOMAIN", "RAILWAY_STATIC_URL"):
        val = os.getenv(env_var, "").strip().rstrip("/")
        if val:
            if not val.startswith("http://") and not val.startswith("https://"):
                val = f"https://{val}"
            origins.add(val)

    return list(origins)


app.add_middleware(
    CORSMiddleware,
    allow_origins=_resolve_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

cookie_samesite = os.getenv("SESSION_COOKIE_SAMESITE", "lax").lower()
if cookie_samesite not in ("lax", "strict", "none"):
    cookie_samesite = "lax"

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("ADMIN_SESSION_SECRET") or secrets.token_urlsafe(32),
    session_cookie="aerobyte_admin",
    max_age=8 * 60 * 60,
    same_site=cookie_samesite,
    https_only=os.getenv("ADMIN_COOKIE_SECURE", "false").casefold() == "true",
)

app.include_router(courses.router)
app.include_router(enrollment.router)
app.include_router(admin.router)
app.include_router(public.router)
app.include_router(accounts.router)
app.include_router(google_auth.router)

upload_directory = Path(__file__).resolve().parents[1] / "data" / "uploads"
upload_directory.mkdir(parents=True, exist_ok=True)


def _optimize_image_webp(source_bytes: bytes, target_path: Path, max_width: Optional[int] = None, quality: int = 82) -> bool:
    try:
        from PIL import Image, ImageOps
        import io

        with Image.open(io.BytesIO(source_bytes)) as img:
            img = ImageOps.exif_transpose(img)
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGBA" if "A" in img.mode else "RGB")

            orig_w, orig_h = img.size
            if max_width and orig_w > max_width:
                new_h = max(1, int(orig_h * (max_width / orig_w)))
                img = img.resize((max_width, new_h), Image.Resampling.LANCZOS)

            target_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(target_path, format="WEBP", quality=quality, method=4)
            return True
    except Exception:
        return False


@app.get("/uploads/{filename}")
def serve_uploaded_file(
    filename: str,
    w: Optional[int] = Query(None, ge=50, le=2560),
    q: int = Query(82, ge=20, le=95),
    raw: bool = Query(False),
):
    clean_name = Path(filename).name
    if not clean_name or clean_name != filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    disk_path = upload_directory / clean_name
    is_image = clean_name.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".bmp"))

    # Raw or non-image request
    if raw or not is_image:
        if disk_path.is_file():
            return FileResponse(
                disk_path,
                headers={"Cache-Control": "public, max-age=31536000, immutable"},
            )
        file_record = get_uploaded_file(clean_name)
        if file_record and file_record.get("data"):
            data = file_record["data"]
            if isinstance(data, memoryview):
                data = bytes(data)
            elif not isinstance(data, bytes):
                data = bytes(data)
            try:
                disk_path.write_bytes(data)
            except Exception:
                pass
            return Response(
                content=data,
                media_type=file_record.get("content_type", "application/octet-stream"),
                headers={"Cache-Control": "public, max-age=31536000, immutable"},
            )
        raise HTTPException(status_code=404, detail="File not found")

    # Image request: check cache
    target_w = min(max(w, 50), 2560) if w else None
    cache_tag = f"opt_w{target_w}_q{q}_{clean_name}.webp" if target_w else f"opt_orig_q{q}_{clean_name}.webp"
    cached_path = upload_directory / cache_tag

    if cached_path.is_file():
        return FileResponse(
            cached_path,
            media_type="image/webp",
            headers={"Cache-Control": "public, max-age=31536000, immutable"},
        )

    # Need source bytes
    source_bytes = None
    if disk_path.is_file():
        source_bytes = disk_path.read_bytes()
    else:
        file_record = get_uploaded_file(clean_name)
        if file_record and file_record.get("data"):
            data = file_record["data"]
            if isinstance(data, memoryview):
                source_bytes = bytes(data)
            elif not isinstance(data, bytes):
                source_bytes = bytes(data)
            else:
                source_bytes = data
            try:
                disk_path.write_bytes(source_bytes)
            except Exception:
                pass

    if not source_bytes:
        raise HTTPException(status_code=404, detail="File not found")

    # Optimize and save
    if _optimize_image_webp(source_bytes, cached_path, max_width=target_w, quality=q):
        return FileResponse(
            cached_path,
            media_type="image/webp",
            headers={"Cache-Control": "public, max-age=31536000, immutable"},
        )

    # Fallback to original
    return Response(
        content=source_bytes,
        media_type="image/png" if clean_name.lower().endswith(".png") else "image/jpeg",
        headers={"Cache-Control": "public, max-age=31536000, immutable"},
    )

frontend_directory = Path(__file__).resolve().parents[1] / "static"



class VisitTrackPayload(BaseModel):
    path: str = "/"
    visitor_id: Optional[str] = None
    referrer: Optional[str] = None
    user_email: Optional[str] = None
    user_name: Optional[str] = None


@app.post("/api/track-visit")
def track_visit(payload: VisitTrackPayload, request: Request):
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        ip = forwarded.split(",")[0].strip()
    else:
        ip = request.client.host if request.client else "Unknown"
    ua = request.headers.get("user-agent", "Unknown")

    user_email = ""
    user_name = ""
    try:
        user_id = request.session.get("user_id") if hasattr(request, "session") else None
        if user_id:
            user = find_user_by_id(user_id)
            if user:
                user_email = user.get("email", "") or ""
                user_name = user.get("name", "") or ""
    except Exception:
        pass

    if not user_email and payload.user_email:
        user_email = payload.user_email
    if not user_name and payload.user_name:
        user_name = payload.user_name

    # Extract email from URL parameters (e.g. during verification links)
    if not user_email and "email=" in (payload.path or ""):
        try:
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(payload.path)
            qs = parse_qs(parsed.query)
            if "email" in qs and qs["email"]:
                user_email = qs["email"][0].strip()
        except Exception:
            pass

    log_visit_event(
        path=payload.path[:250],
        visitor_id=(payload.visitor_id or ip)[:100],
        ip_address=ip[:60],
        user_agent=ua[:400],
        referrer=(payload.referrer or "")[:400],
        user_email=user_email[:120],
        user_name=user_name[:120],
    )
    return {"status": "ok"}

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "AeroByte Academy API"}


@app.get("/{path:path}", include_in_schema=False)
def serve_frontend(path: str):
    requested_file = (frontend_directory / path).resolve()
    if requested_file.is_relative_to(frontend_directory.resolve()) and requested_file.is_file():
        if path:
            headers = {}
            if path.startswith("assets/") or path.endswith((".js", ".css", ".woff2", ".png", ".jpg", ".svg", ".ico", ".webp", ".txt", ".xml")):
                headers["Cache-Control"] = "public, max-age=31536000, immutable"
            return FileResponse(requested_file, headers=headers)
    if path == "api" or path.startswith("api/") or path == "uploads" or path.startswith("uploads/"):
        raise HTTPException(status_code=404, detail="Not Found")
    return FileResponse(
        frontend_directory / "index.html",
        headers={"Cache-Control": "no-cache, must-revalidate"}
    )


@app.on_event("startup")
def startup():
    initialize_content_store()
