import os
import secrets
from datetime import datetime, timezone
from sqlite3 import IntegrityError
from urllib.parse import urlencode, urlsplit
from uuid import uuid4
from typing import Optional

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

from app.content_store import (
    log_login_event,
    create_google_user,
    find_user_by_email,
    find_user_by_google_sub,
    find_user_by_id,
    link_google_user,
    mark_user_verified,
)
from app.user_security import hash_user_password


router = APIRouter(prefix="/api/auth", tags=["Google Authentication"])
oauth = OAuth()


class GoogleDirectLoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    name: Optional[str] = Field(default=None, max_length=120)


class GoogleCredentialRequest(BaseModel):
    credential: str = Field(min_length=10)


DEFAULT_GOOGLE_CLIENT_ID = "779391054555-ohjh6thr5houqnipfg45300dc7q7cebf.apps.googleusercontent.com"


@router.get("/google/config")
async def google_config():
    client_id = os.getenv("GOOGLE_CLIENT_ID", "").strip() or DEFAULT_GOOGLE_CLIENT_ID
    return {
        "configured": bool(client_id),
        "client_id": client_id,
    }


def _google_client():
    client_id = os.getenv("GOOGLE_CLIENT_ID", "").strip() or DEFAULT_GOOGLE_CLIENT_ID
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "").strip()
    if not client_id:
        return None
    existing = oauth.create_client("google")
    if existing is not None:
        return existing
    return oauth.register(
        name="google",
        client_id=client_id,
        client_secret=client_secret,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )


def _frontend_origin(request: Request) -> str:
    allowed = {
        item.strip().rstrip("/")
        for item in os.getenv("FRONTEND_ORIGINS", "").split(",")
        if item.strip()
    }
    configured = os.getenv("FRONTEND_URL", "").strip().rstrip("/")
    if configured:
        return configured
    referer = request.headers.get("referer", "")
    parsed = urlsplit(referer)
    referer_origin = f"{parsed.scheme}://{parsed.netloc}" if parsed.scheme and parsed.netloc else ""
    if referer_origin.rstrip("/") in allowed:
        return referer_origin.rstrip("/")
    if allowed:
        return sorted(allowed)[0]
    return str(request.base_url).rstrip("/")


def _google_callback_url(request: Request) -> str:
    configured = os.getenv("FRONTEND_URL", "").strip().rstrip("/")
    if configured:
        return f"{configured}/api/auth/google/callback"
    url = str(request.url_for("google_callback"))
    proto = request.headers.get("x-forwarded-proto", "").casefold()
    if proto == "https" or "onrender.com" in url:
        if url.startswith("http://"):
            url = "https://" + url[len("http://"):]
    return url


def _account_redirect(request: Request, error: str | None = None) -> RedirectResponse:
    query = f"?{urlencode({'google_error': error})}" if error else ""
    return RedirectResponse(f"{_frontend_origin(request)}/account{query}", status_code=303)


@router.get("/google/start", name="google_login")
async def google_login(request: Request):
    client = _google_client()
    if client is None:
        return _account_redirect(request, "failed")
    nonce = secrets.token_urlsafe(24)
    request.session["google_nonce"] = nonce
    callback_url = _google_callback_url(request)
    return await client.authorize_redirect(request, callback_url, nonce=nonce)


@router.post("/google/direct")
async def google_direct_login(payload: GoogleDirectLoginRequest, request: Request):
    email = payload.email.strip().casefold()
    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="Please enter a valid Google email.")

    admin_email = os.getenv("ADMIN_EMAIL", "aerobyte.academy@gmail.com").strip().casefold()
    request.session.clear()

    # Admin Google login
    if admin_email and email == admin_email:
        request.session["role"] = "admin"
        request.session["csrf"] = secrets.token_urlsafe(24)
        try:
            forwarded = request.headers.get("x-forwarded-for")
            ip = forwarded.split(",")[0].strip() if forwarded else (request.client.host if request.client else "Unknown")
            ua = request.headers.get("user-agent", "Unknown")
            log_login_event(
                user_id="admin",
                user_email=email,
                user_name="Administrator",
                role="Admin",
                login_method="Google Sign-In",
                ip_address=ip,
                user_agent=ua,
                status="success",
            )
        except Exception:
            pass
        return {"authenticated": True, "role": "admin", "redirect": "/admin"}

    # User Google login / auto-registration
    user = find_user_by_email(email)
    if user is None:
        name = (payload.name or "").strip() or email.partition("@")[0].title()
        user_id = str(uuid4())
        subject = f"google-direct-{uuid4().hex[:16]}"
        create_google_user(
            user_id=user_id,
            email=email,
            full_name=name[:120],
            password_hash=hash_user_password(secrets.token_urlsafe(48)),
            google_sub=subject,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        user = find_user_by_id(user_id)

    mark_user_verified(user["id"])
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
            login_method="Google Sign-In",
            ip_address=ip,
            user_agent=ua,
            status="success",
        )
    except Exception:
        pass

    return {
        "authenticated": True,
        "role": "user",
        "redirect": "/profile",
        "user": {
            "id": user["id"],
            "name": user["full_name"],
            "email": user["email"],
        },
    }


@router.post("/google/credential")
async def google_credential_login(payload: GoogleCredentialRequest, request: Request):
    token = payload.credential.strip()
    claims = None
    try:
        import httpx
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}")
            if resp.status_code == 200:
                claims = resp.json()
    except Exception:
        pass

    if not claims or not isinstance(claims, dict):
        raise HTTPException(status_code=400, detail="Invalid Google credential token.")

    email = str(claims.get("email", "")).strip().casefold()
    if not email:
        raise HTTPException(status_code=400, detail="Google token does not contain an email.")

    name = str(claims.get("name", "")).strip() or email.partition("@")[0].title()

    return await google_direct_login(
        GoogleDirectLoginRequest(email=email, name=name),
        request,
    )


@router.get("/google/callback", name="google_callback")
async def google_callback(request: Request):
    client = _google_client()
    nonce = request.session.pop("google_nonce", None)
    if client is None or not nonce:
        return _account_redirect(request, "failed")
    try:
        token = await client.authorize_access_token(request)
        claims = token.get("userinfo")
        if not claims:
            claims = await client.parse_id_token(request, token, nonce=nonce)
    except Exception:
        return _account_redirect(request, "failed")

    if not isinstance(claims, dict):
        return _account_redirect(request, "failed")
    subject = str(claims.get("sub", "")).strip()
    email = str(claims.get("email", "")).strip().casefold()
    email_verified = claims.get("email_verified") is True or str(claims.get("email_verified", "")).casefold() == "true"
    if not subject or not email or not email_verified:
        return _account_redirect(request, "unverified")

    admin_email = os.getenv("ADMIN_EMAIL", "").strip().casefold()
    request.session.clear()
    if admin_email and email == admin_email:
        request.session["role"] = "admin"
        request.session["csrf"] = secrets.token_urlsafe(24)
        try:
            forwarded = request.headers.get("x-forwarded-for")
            ip = forwarded.split(",")[0].strip() if forwarded else (request.client.host if request.client else "Unknown")
            ua = request.headers.get("user-agent", "Unknown")
            log_login_event(
                user_id="admin",
                user_email=email,
                user_name="Administrator",
                role="Admin",
                login_method="Google OAuth",
                ip_address=ip,
                user_agent=ua,
                status="success",
            )
        except Exception:
            pass
        return RedirectResponse(f"{_frontend_origin(request)}/admin", status_code=303)

    try:
        user = find_user_by_google_sub(subject)
        if user is None:
            user = find_user_by_email(email)
            if user is not None:
                link_google_user(user["id"], subject)
            else:
                name = str(claims.get("name", "")).strip() or email.partition("@")[0]
                user_id = str(uuid4())
                create_google_user(
                    user_id=user_id,
                    email=email,
                    full_name=name[:120],
                    password_hash=hash_user_password(secrets.token_urlsafe(48)),
                    google_sub=subject,
                    created_at=datetime.now(timezone.utc).isoformat(),
                )
                user = find_user_by_id(user_id)
        if user is None:
            return _account_redirect(request, "failed")
    except (IntegrityError, ValueError):
        return _account_redirect(request, "failed")

    request.session["role"] = "user"
    request.session["user_id"] = user["id"]
    return RedirectResponse(f"{_frontend_origin(request)}/profile", status_code=303)
