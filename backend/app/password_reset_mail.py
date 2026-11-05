import html
import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)

RESEND_API_URL = "https://api.resend.com/emails"
EMAILJS_API_URL = "https://api.emailjs.com/api/v1.0/email/send"


def _reload_env() -> None:
    # Check both backend/.env and project root .env
    for candidate in (
        Path(__file__).resolve().parents[1] / ".env",
        Path(__file__).resolve().parents[2] / ".env",
    ):
        if candidate.exists():
            for line in candidate.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    key = k.strip()
                    val = v.strip().strip("'\"")
                    if key and val and not os.environ.get(key):
                        os.environ[key] = val


class EmailNotConfiguredError(RuntimeError):
    pass


def get_resend_credentials() -> tuple[str, str]:
    _reload_env()
    api_key = os.getenv("RESEND_API_KEY", "").strip()
    sender = os.getenv("EMAIL_FROM", "").strip() or "AeroByte Academy <onboarding@resend.dev>"

    # Public free webmail domains like @gmail.com cannot send directly via Resend
    # unless a custom verified domain is configured on resend.com.
    # Fallback to the Resend test sender so development & testing work smoothly out of the box.
    if ("@gmail.com" in sender.lower() or "@yahoo.com" in sender.lower()) and "resend.dev" not in sender.lower():
        logger.warning(
            "EMAIL_FROM is set to a public webmail address (%s). "
            "Resend requires a verified domain; falling back to 'AeroByte Academy <onboarding@resend.dev>'.",
            sender,
        )
        sender = "AeroByte Academy <onboarding@resend.dev>"

    return api_key, sender


def get_emailjs_credentials() -> tuple[str, str, str, str]:
    _reload_env()
    service_id = os.getenv("EMAILJS_SERVICE_ID", "").strip()
    template_id = os.getenv("EMAILJS_TEMPLATE_ID", "").strip()
    public_key = os.getenv("EMAILJS_PUBLIC_KEY", "").strip()
    private_key = os.getenv("EMAILJS_PRIVATE_KEY", "").strip()
    return service_id, template_id, public_key, private_key


def get_emailjs_verification_template_id() -> str:
    _reload_env()
    return (
        os.getenv("EMAILJS_VERIFICATION_TEMPLATE_ID", "").strip()
        or os.getenv("EMAILJS_OTP_TEMPLATE_ID", "").strip()
    )


def has_remote_email_provider() -> bool:
    api_key, _ = get_resend_credentials()
    if api_key:
        return True

    service_id, template_id, public_key, private_key = get_emailjs_credentials()
    if all((service_id, template_id, public_key, private_key)):
        return True

    smtp_configured = bool(os.getenv("SMTP_USER", "").strip() and os.getenv("SMTP_PASSWORD", "").strip())
    if smtp_configured:
        return True

    return False


def email_is_configured() -> bool:
    """Return True ONLY if a real third-party email provider is configured to send outbound emails."""
    return has_remote_email_provider()


def _send_with_resend(to_email: str, subject: str, text_content: str, html_content: str) -> None:
    api_key, sender = get_resend_credentials()
    if not api_key:
        raise EmailNotConfiguredError("RESEND_API_KEY is not configured.")

    response = httpx.post(
        RESEND_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "from": sender,
            "to": [to_email],
            "subject": subject,
            "text": text_content,
            "html": html_content,
        },
        timeout=15,
    )
    if response.status_code >= 400:
        logger.error("Resend API error (%s): %s", response.status_code, response.text)
    response.raise_for_status()


def _send_with_emailjs(email: str, name: str, reset_url: str) -> None:
    service_id, template_id, public_key, private_key = get_emailjs_credentials()
    if not all((service_id, template_id, public_key, private_key)):
        raise EmailNotConfiguredError("EmailJS credentials incomplete.")

    response = httpx.post(
        EMAILJS_API_URL,
        json={
            "service_id": service_id,
            "template_id": template_id,
            "user_id": public_key,
            "accessToken": private_key,
            "template_params": {
                "to_email": email,
                "email": email,
                "user_email": email,
                "recipient": email,
                "to_name": name,
                "name": name,
                "reset_url": reset_url,
            },
        },
        timeout=15,
    )
    response.raise_for_status()


def _send_with_smtp(email: str, name: str, reset_url: str) -> None:
    smtp_user = os.environ["SMTP_USER"].strip()
    smtp_pass = os.environ["SMTP_PASSWORD"].strip()
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com").strip()
    smtp_port = int(os.getenv("SMTP_PORT", "587").strip())
    sender = os.getenv("EMAIL_FROM", smtp_user).strip()

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Reset your AeroByte Academy password"
    msg["From"] = sender
    msg["To"] = email

    safe_name = html.escape(name)
    safe_url = html.escape(reset_url, quote=True)

    text_content = (
        f"Hi {name},\n\n"
        "We received a request to reset your AeroByte Academy password. "
        "Use the link below within 30 minutes to choose a new password:\n\n"
        f"{reset_url}\n\n"
        "If you did not request this, you can ignore this email.\n"
    )
    html_content = (
        f"<p>Hi {safe_name},</p>"
        "<p>We received a request to reset your AeroByte Academy password. "
        "Use the link below within 30 minutes to choose a new password:</p>"
        f'<p><a href="{safe_url}">Reset your password</a></p>'
        "<p>If you did not request this, you can ignore this email.</p>"
    )
    msg.attach(MIMEText(text_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)


def send_password_reset_email(email: str, name: str, reset_url: str) -> None:
    safe_name = html.escape(name)
    safe_url = html.escape(reset_url, quote=True)

    subject = "Reset your AeroByte Academy password"
    text_content = (
        f"Hi {name},\n\n"
        "We received a request to reset your AeroByte Academy password. "
        "Use the link below within 30 minutes to choose a new password:\n\n"
        f"{reset_url}\n\n"
        "If you did not request this, you can ignore this email.\n"
    )
    html_content = (
        f"<!DOCTYPE html>"
        f"<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'></head>"
        f"<body style='margin: 0; padding: 32px 16px; background-color: #f4f6f9; font-family: -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, Helvetica, Arial, sans-serif;'>"
        f"<table role='presentation' width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td align='center'>"
        f"<div style='max-width: 560px; background: #ffffff; border-radius: 16px; border: 1px solid #e2e8f0; padding: 36px 32px; box-shadow: 0 4px 20px rgba(0,0,0,0.04); text-align: left;'>"
        f"<div style='text-align: center; margin-bottom: 20px;'>"
        f"<img src='https://raw.githubusercontent.com/Langhour/Aerobyte-Academy-2/main/frontend/public/aerobyte-logo-tight.png' alt='AeroByte Academy' width='96' height='65' style='display: block; margin: 0 auto 6px; width: 96px; height: auto; border: 0; outline: none;' />"
        f"<h1 style='margin: 0; font-size: 24px; font-weight: 800; color: #102a49; letter-spacing: -0.5px; line-height: 1.2;'>AeroByte Academy</h1>"
        f"<p style='margin: 4px 0 0; font-size: 11px; font-weight: 700; color: #64748b; letter-spacing: 0.12em; text-transform: uppercase;'>HANDS-ON ROBOTICS, IOT &amp; CODING</p>"
        f"</div>"
        f"<hr style='border: none; border-top: 1px solid #f1f5f9; margin: 18px 0 26px;' />"
        f"<h2 style='margin: 0 0 16px; font-size: 20px; font-weight: 700; color: #102a49;'>Reset Your Password</h2>"
        f"<p style='font-size: 16px; color: #1e293b; margin: 0 0 12px; line-height: 1.6;'>Hi <strong>{safe_name}</strong>,</p>"
        f"<p style='font-size: 15px; color: #475569; line-height: 1.6; margin: 0 0 24px;'>We received a request to reset your password for your <strong>AeroByte Academy</strong> account. Click the button below within 30 minutes to choose a new password:</p>"
        f"<div style='text-align: center; margin: 28px 0;'>"
        f"<a href='{safe_url}' target='_blank' style='display: inline-block; background-color: #102a49; color: #ffffff; font-size: 15px; font-weight: 700; text-decoration: none; padding: 14px 40px; border-radius: 10px; box-shadow: 0 4px 14px rgba(16, 42, 73, 0.25);'>Reset Password</a>"
        f"</div>"
        f"<p style='font-size: 12px; color: #64748b; line-height: 1.6; text-align: center; margin: 20px 0 0;'>If the button doesn\'t work, copy and paste this link into your browser:<br />"
        f"<a href='{safe_url}' style='color: #0284c7; word-break: break-all; text-decoration: underline;'>{safe_url}</a></p>"
        f"<hr style='border: none; border-top: 1px solid #f1f5f9; margin: 28px 0 20px;' />"
        f"<p style='font-size: 12px; color: #94a3b8; line-height: 1.5; margin: 0; text-align: center;'>This password reset link will expire in 30 minutes. If you did not request this, you can safely ignore this email — your account remains secure.</p>"
        f"<p style='font-size: 11px; color: #cbd5e1; margin: 12px 0 0; text-align: center;'>&copy; 2026 AeroByte Academy. All rights reserved.</p>"
        f"</div>"
        f"</td></tr></table></body></html>"
    )

    # 1. Primary: Resend
    api_key, _ = get_resend_credentials()
    if api_key:
        _send_with_resend(email, subject, text_content, html_content)
        return

    # 2. Secondary fallback: EmailJS
    service_id, template_id, public_key, private_key = get_emailjs_credentials()
    if all((service_id, template_id, public_key, private_key)):
        _send_with_emailjs(email, name, reset_url)
        return

    # 3. Tertiary fallback: SMTP
    if os.getenv("SMTP_USER", "").strip() and os.getenv("SMTP_PASSWORD", "").strip():
        _send_with_smtp(email, name, reset_url)
        return

    # 4. Dev Fallback
    dev_fallback = os.getenv("DEV_EMAIL_FALLBACK", "true").lower() in ("true", "1", "yes")
    if dev_fallback:
        logger.info("[DEV / FALLBACK PASSWORD RESET LINK] User: %s <%s> | Reset URL: %s", name, email, reset_url)
        print(f"\n{'='*70}\n[DEV PASSWORD RESET LINK]\nUser: {name} <{email}>\nReset URL: {reset_url}\n{'='*70}\n", flush=True)
        return

    raise EmailNotConfiguredError("Password reset email is not configured (set RESEND_API_KEY in environment).")


def send_verification_email(email: str, name: str, code: str, verify_url: str) -> None:
    safe_name = html.escape(name)
    safe_url = html.escape(verify_url, quote=True)
    safe_code = html.escape(code)

    subject = f"AeroByte Academy - Verification Code: {code}"
    text_content = (
        f"Hi {name},\n\n"
        "Welcome to AeroByte Academy! Please verify your email address to activate your account.\n\n"
        f"Your 6-digit verification code is: {code}\n\n"
        f"Or click the link below to verify directly:\n{verify_url}\n\n"
        "This code will expire in 15 minutes. If you did not sign up for an AeroByte Academy account, please ignore this email.\n"
    )
    html_content = (
        f"<!DOCTYPE html>"
        f"<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'></head>"
        f"<body style='margin: 0; padding: 32px 16px; background-color: #f4f6f9; font-family: -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, Helvetica, Arial, sans-serif;'>"
        f"<table role='presentation' width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td align='center'>"
        f"<div style='max-width: 560px; background: #ffffff; border-radius: 16px; border: 1px solid #e2e8f0; padding: 36px 32px; box-shadow: 0 4px 20px rgba(0,0,0,0.04); text-align: left;'>"
        f"<div style='text-align: center; margin-bottom: 24px;'>"
        f"<img src='https://raw.githubusercontent.com/Langhour/Aerobyte-Academy-2/main/frontend/public/aerobyte-logo-tight.png' alt='AeroByte Academy' width='96' height='65' style='display: block; margin: 0 auto 6px; width: 96px; height: auto; border: 0; outline: none;' />"
        f"<h1 style='margin: 0; font-size: 24px; font-weight: 800; color: #102a49; letter-spacing: -0.5px; line-height: 1.2;'>AeroByte Academy</h1>"
        f"<p style='margin: 4px 0 0; font-size: 11px; font-weight: 700; color: #64748b; letter-spacing: 0.12em; text-transform: uppercase;'>HANDS-ON ROBOTICS, IOT &amp; CODING</p>"
        f"</div>"
        f"<hr style='border: none; border-top: 1px solid #f1f5f9; margin: 20px 0 24px;' />"
        f"<p style='font-size: 16px; color: #1e293b; margin: 0 0 12px; line-height: 1.6;'>Hi <strong>{safe_name}</strong>,</p>"
        f"<p style='font-size: 15px; color: #475569; line-height: 1.6; margin: 0 0 24px;'>Thank you for joining <strong>AeroByte Academy</strong>! Please verify your email address to activate your account and start exploring our courses.</p>"
        f"<div style='background: #f1f5fa; border: 1.5px dashed #cbd5e1; border-radius: 12px; padding: 20px; text-align: center; margin: 24px 0;'>"
        f"<div style='font-size: 11px; font-weight: 700; color: #64748b; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 8px;'>Your Verification Code</div>"
        f"<div style='font-size: 36px; font-weight: 800; letter-spacing: 10px; color: #102a49; font-family: \"Courier New\", Courier, monospace;'>{safe_code}</div>"
        f"<div style='font-size: 12px; color: #94a3b8; margin-top: 6px;'>Valid for 15 minutes</div>"
        f"</div>"
        f"<p style='font-size: 14px; color: #475569; text-align: center; margin: 20px 0 12px;'>You can also click the button below to verify instantly:</p>"
        f"<div style='text-align: center; margin: 0 0 24px;'>"
        f"<a href='{safe_url}' target='_blank' style='display: inline-block; background-color: #102a49; color: #ffffff; font-size: 15px; font-weight: 700; text-decoration: none; padding: 14px 36px; border-radius: 10px; box-shadow: 0 4px 12px rgba(16, 42, 73, 0.25);'>Verify Email</a>"
        f"</div>"
        f"<p style='font-size: 12px; color: #64748b; line-height: 1.6; text-align: center; margin: 20px 0 0;'>If the button doesn\'t work, copy and paste this link into your browser:<br />"
        f"<a href='{safe_url}' style='color: #0284c7; word-break: break-all; text-decoration: underline;'>{safe_url}</a></p>"
        f"<hr style='border: none; border-top: 1px solid #f1f5f9; margin: 28px 0 20px;' />"
        f"<p style='font-size: 12px; color: #94a3b8; line-height: 1.5; margin: 0; text-align: center;'>If you did not sign up for an AeroByte Academy account, you can safely ignore this email.</p>"
        f"<p style='font-size: 11px; color: #cbd5e1; margin: 12px 0 0; text-align: center;'>&copy; 2026 AeroByte Academy. All rights reserved.</p>"
        f"</div>"
        f"</td></tr></table></body></html>"
    )

    # 1. Primary: Resend
    api_key, _ = get_resend_credentials()
    if api_key:
        try:
            _send_with_resend(email, subject, text_content, html_content)
            return
        except Exception:
            logger.exception("Failed to send verification email via Resend")
            raise

    # 2. Secondary fallback: EmailJS
    service_id, template_id, public_key, private_key = get_emailjs_credentials()
    otp_template_id = get_emailjs_verification_template_id() or template_id
    if all((service_id, otp_template_id, public_key, private_key)):
        try:
            response = httpx.post(
                EMAILJS_API_URL,
                json={
                    "service_id": service_id,
                    "template_id": otp_template_id,
                    "user_id": public_key,
                    "accessToken": private_key,
                    "template_params": {
                        "subject": subject,
                        "to_email": email,
                        "email": email,
                        "user_email": email,
                        "recipient": email,
                        "to_name": name,
                        "name": name,
                        "passcode": code,
                        "Passcode": code,
                        "PASSCODE": code,
                        "code": code,
                        "Code": code,
                        "CODE": code,
                        "otp": code,
                        "Otp": code,
                        "OTP": code,
                        "verification_code": code,
                        "verificationCode": code,
                        "VerificationCode": code,
                        "VERIFICATION_CODE": code,
                        "token": code,
                        "pin": code,
                        "time": "15 minutes",
                        "message": f"Your AeroByte Academy verification code is: {code}\n\nClick here to verify directly: {verify_url}",
                        "reset_url": verify_url,
                        "verify_url": verify_url,
                    },
                },
                timeout=15,
            )
            response.raise_for_status()
            return
        except Exception:
            logger.exception("Failed to send verification email via EmailJS")

    # 3. Tertiary fallback: SMTP
    if os.getenv("SMTP_USER", "").strip() and os.getenv("SMTP_PASSWORD", "").strip():
        try:
            smtp_user = os.environ["SMTP_USER"].strip()
            smtp_pass = os.environ["SMTP_PASSWORD"].strip()
            smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com").strip()
            smtp_port = int(os.getenv("SMTP_PORT", "587").strip())
            sender_addr = os.getenv("EMAIL_FROM", smtp_user).strip()

            msg = MIMEMultipart("alternative")
            msg["Subject"] = "Verify your AeroByte Academy account"
            msg["From"] = sender_addr
            msg["To"] = email
            msg.attach(MIMEText(text_content, "plain"))
            msg.attach(MIMEText(html_content, "html"))

            with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            return
        except Exception:
            logger.exception("Failed to send verification email via SMTP")

    # 4. Dev Fallback
    dev_fallback = os.getenv("DEV_EMAIL_FALLBACK", "true").lower() in ("true", "1", "yes")
    if dev_fallback:
        logger.info("[DEV / FALLBACK EMAIL VERIFICATION] User: %s <%s> | Code: %s | Verify URL: %s", name, email, code, verify_url)
        print(
            f"\n{'='*70}\n[DEV EMAIL VERIFICATION]\nUser: {name} <{email}>\nCode: {code}\nVerify URL: {verify_url}\n{'='*70}\n",
            flush=True,
        )
        return

    raise EmailNotConfiguredError("Verification email service is not configured (set RESEND_API_KEY in environment).")
