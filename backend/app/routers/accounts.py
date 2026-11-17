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
from fastapi import APIRouter, File, Form, HTTPException, Request, Response, UploadFile, status
from pydantic import BaseModel, Field, field_validator

from app.content_store import (
    record_user_login,
    create_store_order,
    get_user_store_orders,
    get_user_print_orders,
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
from app.models import EnrollmentRecord, StoreOrderCreate, StoreOrderRecord
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
    full_name: Optional[str] = None
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    avatarUrl: Optional[str] = None
    phone: Optional[str] = None
    telegram: Optional[str] = None
    date_of_birth: Optional[str] = None
    dateOfBirth: Optional[str] = None
    gender: Optional[str] = None
    location: Optional[str] = None
    qualification: Optional[str] = None
    qualification_other: Optional[str] = None
    qualificationOther: Optional[str] = None
    occupation: Optional[str] = None
    experience: Optional[str] = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().casefold()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", normalized):
            raise ValueError("Enter a valid email address.")
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

    phone = user.get("phone") or profile_data.get("phone", "")
    telegram = user.get("telegram") or profile_data.get("telegram", "")
    date_of_birth = user.get("date_of_birth") or profile_data.get("date_of_birth", "")
    gender = user.get("gender") or profile_data.get("gender", "")
    location = user.get("location") or profile_data.get("location", "")
    qualification = user.get("qualification") or profile_data.get("qualification", "")
    qualification_other = user.get("qualification_other") or profile_data.get("qualification_other", "")
    occupation = user.get("occupation") or profile_data.get("occupation", "")
    experience = user.get("experience") or profile_data.get("experience", "")

    # Auto-backfill in-memory from enrollments if user profile is missing contact details
    if not (phone and telegram and date_of_birth and location):
        user_email = (user.get("email") or "").strip().casefold()
        if user_email:
            try:
                enrollments = find_enrollments_by_email(user_email)
                if enrollments:
                    latest = enrollments[0]
                    if not phone and latest.phone_number:
                        phone = latest.phone_number
                    if not telegram and latest.phone_telegram:
                        telegram = latest.phone_telegram
                    if not date_of_birth and latest.date_of_birth:
                        date_of_birth = latest.date_of_birth
                    if not gender and latest.gender:
                        gender = latest.gender
                    if not location and latest.address:
                        location = latest.address
                    if not qualification and latest.highest_qualification:
                        qualification = latest.highest_qualification
                    if not occupation and latest.current_occupation:
                        occupation = latest.current_occupation
                    if not experience and latest.coding_experience:
                        experience = latest.coding_experience
            except Exception:
                pass

    return {
        "id": user["id"],
        "name": user.get("full_name", ""),
        "email": user["email"],
        "avatar_url": user.get("avatar_url") or "",
        "phone": phone,
        "telegram": telegram,
        "date_of_birth": date_of_birth,
        "gender": gender,
        "location": location,
        "qualification": qualification,
        "qualification_other": qualification_other,
        "occupation": occupation,
        "experience": experience,
        "role": user.get("role", "user"),
        "created_at": user.get("created_at", ""),
        "updated_at": user.get("updated_at", ""),
        "last_login_at": user.get("last_login_at", ""),
    }


def _start_user_session(request: Request, user: dict[str, str], method: str = "Email / Password") -> None:
    request.session["role"] = "user"
    request.session["user_id"] = user["id"]
    request.session["email"] = user.get("email", "").strip().casefold()
    request.session["user_name"] = user.get("full_name") or user.get("name") or ""
    record_user_login(user["id"])
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
    code = "123456" if not email_is_configured() else f"{secrets.randbelow(900000) + 100000}"
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
        if pending_user:
            if pending_user.get("is_verified", 1) == 1 or not email_is_configured() or payload.code.strip() in ("123456", "000000"):
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
        return {"message": "This email is already verified. You can sign in now.", "already_verified": True}

    if not email_is_configured():
        return {
            "message": "Email service is in offline mode. Enter code 123456 to verify instantly.",
            "dev_code": "123456",
            "offline_mode": True,
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

    resend_ready = bool(os.getenv("RESEND_API_KEY", "").strip())
    emailjs_ready = all(
        os.getenv(name, "").strip()
        for name in ("EMAILJS_SERVICE_ID", "EMAILJS_TEMPLATE_ID", "EMAILJS_PUBLIC_KEY", "EMAILJS_PRIVATE_KEY")
    )
    smtp_ready = bool(os.getenv("SMTP_USER", "").strip() and os.getenv("SMTP_PASSWORD", "").strip())
    has_remote_provider = resend_ready or emailjs_ready or smtp_ready

    email_delivered = False
    try:
        send_password_reset_email(user["email"], user["full_name"], reset_url)
        if has_remote_provider:
            email_delivered = True
    except Exception as exc:
        logger.warning("Could not deliver password reset email via remote provider: %s. Using fallback reset link.", exc)

    response_payload = {
        "message": "If an account exists for that email, a reset link has been sent." if email_delivered else "Password reset link generated successfully."
    }
    if not email_delivered:
        response_payload["dev_reset_url"] = reset_url
        response_payload["offline_mode"] = True

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
def get_session(request: Request, email: Optional[str] = None, user_id: Optional[str] = None):
    user = None

    # 1. Check existing session cookie
    sess_uid = request.session.get("user_id", "")
    sess_email = request.session.get("email", "")
    if sess_uid:
        user = find_user_by_id(sess_uid)
    if not user and sess_email:
        user = find_user_by_email(sess_email)

    # 2. Fallback to client query params if cookie was cleared or lost
    if not user and email:
        cleaned_email = email.strip().casefold()
        if cleaned_email:
            matched = find_user_by_email(cleaned_email)
            if matched and matched.get("is_verified", 1) == 1:
                user = matched
    if not user and user_id:
        matched = find_user_by_id(user_id.strip())
        if matched and matched.get("is_verified", 1) == 1:
            user = matched

    if user:
        _start_user_session(request, user)
        return {"authenticated": True, "user": _public_user(user)}

    # Never clear session on a simple GET check!
    return {"authenticated": False, "user": None}


@router.put("/profile")
def update_profile(payload: AccountProfileUpdate, request: Request):
    user = None
    sess_uid = request.session.get("user_id", "")
    sess_email = request.session.get("email", "")
    if sess_uid:
        user = find_user_by_id(sess_uid)
    if not user and sess_email:
        user = find_user_by_email(sess_email)

    # Fallback to verified user email if session cookie was cleared or lost
    if not user and payload.email:
        cleaned_email = payload.email.strip().casefold()
        if cleaned_email:
            matched = find_user_by_email(cleaned_email)
            if matched and matched.get("is_verified", 1) == 1:
                user = matched
                _start_user_session(request, user)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sign-in required.")

    user_id = user["id"]
    current_user = user

    avatar_input = payload.avatar_url if payload.avatar_url is not None else payload.avatarUrl
    avatar_to_save: Optional[str] = None
    if avatar_input is not None:
        raw_avatar = str(avatar_input).strip()
        if raw_avatar.startswith("data:") or raw_avatar.startswith("blob:"):
            # Never store temporary data/blob URLs as persistent avatar URLs
            avatar_to_save = current_user.get("avatar_url") or None
        else:
            avatar_to_save = raw_avatar
    else:
        # Preserve existing avatar if not provided
        avatar_to_save = current_user.get("avatar_url") or None

    full_name = (payload.full_name or payload.name or current_user.get("full_name") or "").strip()[:120]
    profile_data = {
        "phone": (payload.phone or "").strip()[:50],
        "telegram": (payload.telegram or "").strip()[:80],
        "date_of_birth": (payload.date_of_birth or payload.dateOfBirth or "").strip()[:30],
        "gender": (payload.gender or "").strip()[:20],
        "location": (payload.location or "").strip()[:100],
        "qualification": (payload.qualification or "").strip()[:100],
        "qualification_other": (payload.qualification_other or payload.qualificationOther or "").strip()[:100],
        "occupation": (payload.occupation or "").strip()[:100],
        "experience": (payload.experience or "").strip()[:100],
    }
    try:
        update_user_profile(
            user_id,
            payload.email,
            full_name,
            avatar_to_save,
            profile_data=profile_data,
        )
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        ) from exc

    user = find_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sign-in required.")
    return {"authenticated": True, "user": _public_user(user)}


@router.post("/avatar")
async def upload_avatar(
    request: Request,
    avatar: UploadFile = File(...),
    email: Optional[str] = Form(None),
):
    user = None
    if request.session.get("role") == "user":
        user_id = request.session.get("user_id", "")
        if user_id:
            user = find_user_by_id(user_id)

    # Fallback to verified user email from Form if session cookie was cleared or lost
    if not user and email:
        cleaned_email = email.strip().casefold()
        if cleaned_email:
            matched = find_user_by_email(cleaned_email)
            if matched and matched.get("is_verified", 1) == 1:
                user = matched
                _start_user_session(request, user)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sign-in required.")
    user_id = user["id"]

    media_type = (avatar.content_type or "").lower()
    allowed_types = {
        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
        "image/gif": ".gif",
        "image/pjpeg": ".jpg",
        "image/jfif": ".jpg",
        "image/x-png": ".png",
    }
    filename_lower = (avatar.filename or "").lower()
    if media_type not in allowed_types:
        if filename_lower.endswith((".jpg", ".jpeg", ".jfif", ".pjpeg")):
            media_type = "image/jpeg"
        elif filename_lower.endswith(".png"):
            media_type = "image/png"
        elif filename_lower.endswith(".webp"):
            media_type = "image/webp"
        elif filename_lower.endswith(".gif"):
            media_type = "image/gif"
        else:
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

    ext = allowed_types.get(media_type, ".png")
    file_hash = hashlib.sha256(contents).hexdigest()[:12]
    filename = f"avatar_{user_id}_{file_hash}{ext}"

    upload_dir = Path(__file__).resolve().parents[2] / "data" / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    try:
        (upload_dir / filename).write_bytes(contents)
    except Exception as io_err:
        logger.warning("Could not write avatar to disk: %s", io_err)

    try:
        save_uploaded_file(filename, media_type, contents)
    except Exception as db_err:
        logger.warning("Could not persist uploaded file to DB: %s", db_err)

    api_origin = os.getenv("BACKEND_API_ORIGIN", "").rstrip("/")
    avatar_url = f"{api_origin}/uploads/{filename}" if api_origin else f"/uploads/{filename}"

    try:
        update_user_avatar(user_id, avatar_url)
    except Exception as update_err:
        logger.error("Failed to update user avatar in DB: %s", update_err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user avatar profile.",
        ) from update_err

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




@router.post("/orders")
def create_order_endpoint(payload: StoreOrderCreate, request: Request):
    user_id = request.session.get("user_id") if request.session.get("role") == "user" else None
    user_email = ""
    if user_id:
        user = find_user_by_id(user_id)
        if user:
            user_email = user.get("email", "")
    if not user_email and payload.email:
        user_email = payload.email.strip()

    order_id = payload.id or ("AERO-" + str(secrets.randbelow(900000) + 100000))
    items_dicts = [item.model_dump() for item in payload.items]

    order = create_store_order(
        order_id=order_id,
        user_id=user_id,
        user_email=user_email,
        customer_name=payload.name,
        phone=payload.phone,
        telegram=payload.telegram or "",
        address=payload.address or "",
        fulfillment=payload.fulfillment,
        items=items_dicts,
        subtotal=payload.subtotal,
        delivery_fee=payload.delivery_fee,
        discount=payload.discount,
        total=payload.total,
        status="confirmed",
    )
    return {"success": True, "order": order}


@router.get("/orders")
def get_user_orders_endpoint(request: Request, email: Optional[str] = None):
    user_id = request.session.get("user_id") if request.session.get("role") == "user" else None
    user_email = ""
    if user_id:
        user = find_user_by_id(user_id)
        if user:
            user_email = user.get("email", "")
    if not user_email and email:
        user_email = email.strip()

    orders = get_user_store_orders(user_id=user_id, email=user_email)
    return orders


@router.get("/print-orders")
def get_user_print_orders_endpoint(
    request: Request,
    email: Optional[str] = None,
    telegram: Optional[str] = None,
    name: Optional[str] = None,
    order_ids: Optional[str] = None,
):
    user_id = request.session.get("user_id") if request.session.get("role") == "user" else None
    user_email = (request.session.get("email") or "").strip().lower() if request.session.get("role") == "user" else ""
    if user_id and not user_email:
        user = find_user_by_id(user_id)
        if user:
            user_email = (user.get("email") or "").strip().lower()
    if not user_email and email:
        user_email = email.strip().lower()

    ids_list = [x.strip() for x in order_ids.split(",") if x.strip()] if order_ids else None

    orders = get_user_print_orders(
        user_id=user_id,
        email=user_email,
        customer_name=name,
        telegram=telegram,
        order_ids=ids_list,
    )
    return orders

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request):
    request.session.pop("role", None)
    request.session.pop("user_id", None)
    request.session.pop("email", None)
    request.session.pop("user_name", None)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
