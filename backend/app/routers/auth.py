import hashlib
import logging
import os
import re
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, Field, field_validator

from app.content_store import (
    find_user_by_email,
    save_email_otp_code,
    verify_and_consume_otp_code,
)
from app.password_reset_mail import send_passcode_email
from app.routers.accounts import _public_user, _start_user_session

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Email Passcode Verification"])


class SendCodeRequest(BaseModel):
    email: str = Field(min_length=3, max_length=254)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().casefold()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", normalized):
            raise ValueError("Please enter a valid email address.")
        return normalized


class VerifyCodeRequest(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    code: str = Field(min_length=4, max_length=12)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().casefold()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", normalized):
            raise ValueError("Please enter a valid email address.")
        return normalized

    @field_validator("code")
    @classmethod
    def validate_code(cls, value: str) -> str:
        cleaned = re.sub(r"\s+", "", value.strip())
        if not cleaned:
            raise ValueError("Please enter the verification code.")
        return cleaned


@router.post("/send-code")
def send_code(payload: SendCodeRequest):
    """
    Accept email, generate a secure random 6-digit numeric passcode,
    store in database with 10-minute expiry (overwriting any previous code),
    and send via the Resend SDK.
    """
    email = payload.email

    # Generate a cryptographically secure random 6-digit numeric passcode (100000 - 999999)
    passcode = f"{secrets.randbelow(900000) + 100000}"
    code_hash = hashlib.sha256(passcode.encode("utf-8")).hexdigest()

    # 10 minutes expiry timestamp
    now = datetime.now(timezone.utc)
    created_at = now.isoformat()
    expires_at = (now + timedelta(minutes=10)).isoformat()

    # Save to database (overwriting any existing code for that email)
    save_email_otp_code(
        email=email,
        code=passcode,
        code_hash=code_hash,
        expires_at=expires_at,
        created_at=created_at,
    )

    # Send email via Resend SDK
    try:
        send_passcode_email(email, passcode)
        logger.info("Verification passcode sent successfully to %s", email)
    except Exception as exc:
        logger.error("Failed to deliver passcode email to %s: %s", email, exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email. Please try again later.",
        ) from exc

    return {
        "status": "ok",
        "message": f"A 6-digit verification code has been sent to {email}.",
        "email": email,
        "expires_in_minutes": 10,
    }


@router.post("/verify-code")
def verify_code(payload: VerifyCodeRequest, request: Request):
    """
    Verify 6-digit passcode against the database:
    - Checks that code matches
    - Checks that it has not expired
    - Marks user as verified, deletes the used code from database
    - Starts session if user already exists
    """
    now = datetime.now(timezone.utc).isoformat()
    valid, message, user = verify_and_consume_otp_code(payload.email, payload.code, now)

    if not valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )

    # If the user exists in database, initialize their session
    response_data: dict[str, Any] = {
        "status": "ok",
        "verified": True,
        "message": message or "Email verified successfully.",
    }

    if user:
        _start_user_session(request, user)
        response_data["authenticated"] = True
        response_data["user"] = _public_user(user)

    return response_data
