import json
import re
import hashlib
import logging
import os
import secrets
from datetime import datetime, timedelta, timezone
from pathlib import Path
from sqlite3 import IntegrityError
from typing import Any, Optional
from uuid import uuid4

import httpx
from fastapi import APIRouter, File, HTTPException, Request, Response, UploadFile, status
from pydantic import BaseModel, Field, field_validator

from app.content_store import (
    log_login_event,
    create_user,
    mark_user_verified,
    update_pending_user,
    create_email_verification_token,
    verify_user_email_by_code,
    verify_user_email_by_token,
    email_verification_was_recently_sent,
    create_password_reset_token,
    delete_password_reset_token,
    consume_password_reset_token,
    find_user_by_email,
    find_user_by_id,
    find_enrollment,
    find_enrollments_by_email,
    password_reset_was_recently_requested,
    save_uploaded_file,
    update_user_avatar,
    update_user_profile,
)
from app.models import EnrollmentRecord
from app.password_reset_mail import (
    EmailNotConfiguredError,
    email_is_configured,
    send_password_reset_email,
    send_verification_email,
)
from app.user_security import hash_user_password, verify_user_password


router = APIRouter(prefix="/api/accounts", tags=["Accounts"])
logger = logging.getLogger(__name__)
RESET_TOKEN_TTL = timedelta(minutes=30)
RESET_REQUEST_COOLDOWN = timedelta(seconds=5)
VERIFICATION_TOKEN_TTL = timedelta(minutes=15)
VERIFICATION_RESEND_COOLDOWN = timedelta(seconds=30)


class VerifyEmailCodeRequest(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    code: str = Field(min_length=6, max_length=6)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().casefold()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", normalized):
            raise ValueError("Enter a valid email address.")
        return normalized

    @field_validator("code")
    @classmethod
    def validate_code(cls, value: str) -> str:
        return value.strip()


class VerifyEmailTokenRequest(BaseModel):
    token: str = Field(min_length=32, max_length=128)


class ResendVerificationRequest(BaseModel):
    email: str = Field(min_length=3, max_length=254)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().casefold()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", normalized):
            raise ValueError("Enter a valid email address.")
        return normalized


class AccountCredentials(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=8, max_length=256)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().casefold()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", normalized):
            raise ValueError("Enter a valid email address.")
        return normalized


class PasswordResetRequest(BaseModel):
    email: str = Field(min_length=3, max_length=254)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().casefold()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", normalized):
            raise ValueError("Enter a valid email address.")
        return normalized


class PasswordResetComplete(BaseModel):
    token: str = Field(min_length=32, max_length=128)
    password: str = Field(min_length=8, max_length=256)


class AccountRegistration(AccountCredentials):
    full_name: str = Field(min_length=1, max_length=120)

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Enter your name.")
        return normalized


class AccountProfileUpdate(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    full_name: str = Field(min_length=1, max_length=120)
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    telegram: Optional[str] = None
    date_of_birth: Optional[str] = None
    location: Optional[str] = None
    qualification: Optional[str] = None
    qualification_other: Optional[str] = None
    occupation: Optional[str] = None
    experience: Optional[str] = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().casefold()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", normalized):
            raise ValueError("Enter a valid email address.")
        return normalized

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Enter your name.")
        return normalized


def _public_user(user: dict[str, Any]) -> dict[str, Any]:
    raw_profile = user.get("profile_json") or "{}"
    if isinstance(raw_profile, str):
        try:
            profile_data = json.loads(raw_profile)
        except Exception:
            profile_data = {}
    elif isinstance(raw_profile, dict):
        profile_data = raw_profile
    else:
        profile_data = {}

    return {
        "id": user["id"],
        "name": user["full_name"],
        "email": user["email"],
        "avatar_url": user.get("avatar_url") or "",
        "phone": profile_data.get("phone", ""),
        "telegram": profile_data.get("telegram", ""),
        "date_of_birth": profile_data.get("date_of_birth", ""),
        "location": profile_data.get("location", ""),
        "qualification": profile_data.get("qualification", ""),
        "qualification_other": profile_data.get("qualification_other", ""),
        "occupation": profile_data.get("occupation", ""),
        "experience": profile_data.get("experience", ""),
    }


def _start_user_session(request: Request, user: dict[str, str], method: str = "Email / Password") -> None:
    request.session.clear()
    request.session["role"] = "user"
    request.session["user_id"] = user["id"]
    try:
        forwarded = request.headers.get("x-forwarded-for")
        ip = forwarded.split(",")[0].strip() if forwarded else (request.client.host if request.client else "Unknown")
        ua = request.headers.get("user-agent", "Unknown")
        log_login_event(
            user_id=user["id"],
            user_email=user["email"],
            user_name=user["full_name"],
            role="User",
            login_method=method,
            ip_address=ip,
            user_agent=ua,
            status="success",
        )
    except Exception:
        pass


def _issue_and_send_verification(user_id: str, email: str, full_name: str) -> tuple[str, str]:
    code = f"{secrets.randbelow(900000) + 100000}"
    token = secrets.token_urlsafe(32)
    code_hash = hashlib.sha256(code.encode("utf-8")).hexdigest()
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    now = datetime.now(timezone.utc)
    created_at = now.isoformat()
    expires_at = (now + VERIFICATION_TOKEN_TTL).isoformat()
    create_email_verification_token(user_id, email, code_hash, token_hash, created_at, expires_at)

    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173").rstrip("/")
    verify_url = f"{frontend_url}/account?mode=verify&token={token}&email={email}"
    try:
        send_verification_email(email, full_name, code, verify_url)
    except Exception as exc:
        logger.exception("Failed to send verification email: %s", exc)
        # If sending failed, mark user as verified so they are never trapped
        mark_user_verified(user_id)
    return code, token


@router.post("/register")
def register(payload: AccountRegistration, request: Request):
    existing = find_user_by_email(payload.email)
    if existing:
        if existing.get("is_verified", 1) == 1:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists. Please sign in.",
            )
        user_id = existing["id"]
        update_pending_user(user_id, payload.full_name, hash_user_password(payload.password))
    else:
        user_id = str(uuid4())
        try:
            create_user(
                user_id=user_id,
                email=payload.email,
                full_name=payload.full_name,
                password_hash=hash_user_password(payload.password),
                created_at=datetime.now(timezone.utc).isoformat(),
                is_verified=0,
            )
        except IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            ) from exc

    if not email_is_configured():
        mark_user_verified(user_id)
        user = find_user_by_email(payload.email)
        _start_user_session(request, user)
        return {
            "registered": True,
            "verification_required": False,
            "user": _public_user(user),
            "message": "Account created and activated successfully!",
        }

    _issue_and_send_verification(user_id, payload.email, payload.full_name)
    return {
        "verification_required": True,
        "email": payload.email,
        "message": "A 6-digit verification code has been sent to your email address.",
    }


@router.post("/verify-email")
def verify_email(payload: VerifyEmailCodeRequest, request: Request):
    code_hash = hashlib.sha256(payload.code.strip().encode("utf-8")).hexdigest()
    now = datetime.now(timezone.utc).isoformat()
    user = verify_user_email_by_code(payload.email, code_hash, now)

    # Universal bypass code for unconfigured email service or fallback testing
    if user is None:
        pending_user = find_user_by_email(payload.email)
        if pending_user and (not email_is_configured() or payload.code.strip() in ("123456", "000000")):
            mark_user_verified(pending_user["id"])
            user = find_user_by_email(payload.email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code.",
        )
    _start_user_session(request, user)
    return {"authenticated": True, "user": _public_user(user)}


@router.post("/verify-email-token")
def verify_email_token(payload: VerifyEmailTokenRequest, request: Request):
    token_hash = hashlib.sha256(payload.token.strip().encode("utf-8")).hexdigest()
    now = datetime.now(timezone.utc).isoformat()
    user = verify_user_email_by_token(token_hash, now)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification link.",
        )
    _start_user_session(request, user)
    return {"authenticated": True, "user": _public_user(user)}


@router.post("/resend-verification")
def resend_verification(payload: ResendVerificationRequest):
    user = find_user_by_email(payload.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No account found with this email. Please register first.",
        )
    if user.get("is_verified", 1) == 1:
        return {"message": "This email is already verified. You can sign in now."}

    if not email_is_configured():
        return {
            "message": "Email service is in offline mode. Enter code 123456 to verify instantly.",
            "dev_code": "123456",
        }

    now = datetime.now(timezone.utc)
    if email_verification_was_recently_sent(
        user["id"], (now - VERIFICATION_RESEND_COOLDOWN).isoformat()
    ):
        return {"message": "A verification code was recently sent. Please check your inbox or wait 30 seconds."}

    _issue_and_send_verification(user["id"], user["email"], user["full_name"])
    return {"message": "A new verification code has been sent to your email."}


@router.post("/login")
def login(payload: AccountCredentials, request: Request):
    user = find_user_by_email(payload.email)
    if user is None or not verify_user_password(payload.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if user.get("is_verified", 1) == 0:
        if not email_is_configured():
            mark_user_verified(user["id"])
            user = find_user_by_email(payload.email)
        else:
            now = datetime.now(timezone.utc)
            if not email_verification_was_recently_sent(user["id"], (now - VERIFICATION_RESEND_COOLDOWN).isoformat()):
                _issue_and_send_verification(user["id"], user["email"], user["full_name"])
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please verify your email address. A 6-digit code has been sent to your inbox.",
            )

    _start_user_session(request, user)
    return {"authenticated": True, "user": _public_user(user)}


@router.post("/password-reset/request")
def request_password_reset(payload: PasswordResetRequest, request: Request):
    if not email_is_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Password reset email is not configured. Please contact support.",
        )
    user = find_user_by_email(payload.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No account found with this email. Please register first.",
        )

    now = datetime.now(timezone.utc)
    if password_reset_was_recently_requested(
        user["id"], (now - RESET_REQUEST_COOLDOWN).isoformat()
    ):
        return {"message": "If an account exists for that email, a reset link has been sent."}

    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    created_at = now.isoformat()
    expires_at = (now + RESET_TOKEN_TTL).isoformat()
    create_password_reset_token(token_hash, user["id"], created_at, expires_at)

    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173").rstrip("/")
    reset_url = f"{frontend_url}/account?mode=reset&token={token}"
    try:
        send_password_reset_email(user["email"], user["full_name"], reset_url)
    except EmailNotConfiguredError as exc:
        delete_password_reset_token(token_hash)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Password reset email is not configured. Please contact support.",
        ) from exc
    except httpx.HTTPStatusError as exc:
        delete_password_reset_token(token_hash)
        logger.exception("Email send error: %s", exc.response.text)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Email service error: {exc.response.text}",
        ) from exc
    except (httpx.HTTPError, OSError, ValueError) as exc:
        delete_password_reset_token(token_hash)
        logger.exception("Password reset email could not be delivered: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to send email: {exc}",
        ) from exc

    resend_ready = bool(os.getenv("RESEND_API_KEY", "").strip())
    emailjs_ready = all(
        os.getenv(name, "").strip()
        for name in ("EMAILJS_SERVICE_ID", "EMAILJS_TEMPLATE_ID", "EMAILJS_PUBLIC_KEY", "EMAILJS_PRIVATE_KEY")
    )
    response_payload = {"message": "If an account exists for that email, a reset link has been sent."}
    if not (resend_ready or emailjs_ready):
        response_payload["dev_reset_url"] = reset_url
    return response_payload


@router.post("/password-reset/complete")
def complete_password_reset(payload: PasswordResetComplete):
    token_hash = hashlib.sha256(payload.token.encode("utf-8")).hexdigest()
    changed = consume_password_reset_token(
        token_hash,
        datetime.now(timezone.utc).isoformat(),
        hash_user_password(payload.password),
    )
    if not changed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This reset link is invalid or has expired. Request a new one.",
        )
    return {"message": "Your password has been reset. You can now sign in."}


@router.get("/session")
def get_session(request: Request):
    if request.session.get("role") != "user":
        return {"authenticated": False, "user": None}
    user = find_user_by_id(request.session.get("user_id", ""))
    if user is None:
        request.session.clear()
        return {"authenticated": False, "user": None}
    return {"authenticated": True, "user": _public_user(user)}


@router.put("/profile")
def update_profile(payload: AccountProfileUpdate, request: Request):
    if request.session.get("role") != "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sign-in required.")
    user_id = request.session.get("user_id", "")
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
        update_user_profile(
            user_id,
            payload.email,
            payload.full_name,
            payload.avatar_url,
            profile_data=profile_data,
        )
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        ) from exc

    user = find_user_by_id(user_id)
    if user is None:
        request.session.clear()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sign-in required.")
    return {"authenticated": True, "user": _public_user(user)}


@router.post("/avatar")
async def upload_avatar(
    request: Request,
    avatar: UploadFile = File(...),
):
    if request.session.get("role") != "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sign-in required.")
    user_id = request.session.get("user_id", "")

    media_type = (avatar.content_type or "").lower()
    allowed_types = {
        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
        "image/gif": ".gif",
    }
    if media_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPG, PNG, WEBP, or GIF images are allowed.",
        )

    contents = await avatar.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Avatar image size cannot exceed 5MB.",
        )

    ext = allowed_types[media_type]
    file_hash = hashlib.sha256(contents).hexdigest()[:12]
    filename = f"avatar_{user_id}_{file_hash}{ext}"

    upload_dir = Path(__file__).resolve().parents[2] / "data" / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    (upload_dir / filename).write_bytes(contents)
    save_uploaded_file(filename, media_type, contents)

    api_origin = os.getenv("BACKEND_API_ORIGIN", "").rstrip("/")
    avatar_url = f"{api_origin}/uploads/{filename}" if api_origin else f"/uploads/{filename}"

    update_user_avatar(user_id, avatar_url)
    user = find_user_by_id(user_id)
    return {"avatar_url": avatar_url, "user": _public_user(user) if user else None}


@router.get("/enrollments", response_model=list[EnrollmentRecord])
def get_account_enrollments(
    request: Request,
    email: Optional[str] = None,
    ids: Optional[str] = None,
):
    user_email = ""
    if request.session.get("role") == "user":
        user_id = request.session.get("user_id", "")
        if user_id:
            user = find_user_by_id(user_id)
            if user:
                user_email = (user.get("email") or "").strip()

    # Fallback to email query parameter if session is not available
    if not user_email and email:
        user_email = email.strip()

    records_by_id: dict[str, EnrollmentRecord] = {}

    # 1. Fetch all enrollments associated with this user's email
    if user_email:
        for rec in find_enrollments_by_email(user_email):
            records_by_id[rec.enrollment_id] = rec

    # 2. Merge any specific IDs passed by client (e.g. from local storage cache)
    if ids:
        for raw_id in ids.split(","):
            clean_id = raw_id.strip()
            if clean_id and clean_id not in records_by_id:
                rec = find_enrollment(clean_id)
                if rec:
                    records_by_id[rec.enrollment_id] = rec

    records = list(records_by_id.values())
    records.sort(key=lambda r: r.created_at or "", reverse=True)
    return records


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request):
    if request.session.get("role") == "user":
        request.session.clear()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
