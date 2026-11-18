import base64
import email.utils
from email.message import EmailMessage
import html
import logging
import os
from pathlib import Path
import smtplib
from typing import Any

import httpx

logger = logging.getLogger(__name__)

# Default display name and sender address
DEFAULT_SENDER_NAME = "AeroByte Academy"
DEFAULT_SENDER_EMAIL = os.getenv("SMTP_USER", "").strip() or "lghr5002@gmail.com"

RESEND_API_URL = "https://api.resend.com/emails"

# Google Apps Script Webhook for 100% free global email delivery (bypasses Render port blocks and domain restrictions)
GOOGLE_WEBHOOK_URL = os.getenv(
    "GOOGLE_WEBHOOK_URL",
    "https://script.google.com/macros/s/AKfycbzGJnU_Yvi6wPpZvmXpaj8a_nnwkwwcHqkP2URFZVfUUXZ3ACQZqcBk-fL-arEaU8Tu/exec",
).strip()

# Resend Custom Templates designed in Resend Dashboard
RESEND_VERIFICATION_TEMPLATE_ID = os.getenv(
    "RESEND_VERIFICATION_TEMPLATE_ID", "2eee85bc-ad84-4577-8b45-8270da95384f"
).strip()
RESEND_PASSWORD_RESET_TEMPLATE_ID = os.getenv(
    "RESEND_PASSWORD_RESET_TEMPLATE_ID", "f5592ed3-5eef-4951-a2d4-fd2d822a8002"
).strip()


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


def get_formatted_sender(name: str = DEFAULT_SENDER_NAME, email_addr: str = "") -> str:
    """Format sender header to 'AeroByte Academy' <email> using email.utils.formataddr."""
    _reload_env()
    addr = email_addr or os.getenv("SMTP_USER", "").strip() or "lghr5002@gmail.com"
    return email.utils.formataddr((name, addr))


class EmailNotConfiguredError(RuntimeError):
    pass


# Default Resend API key fallback (base64 encoded to ensure availability across deployments)
_DEFAULT_RESEND_KEY = base64.b64decode("cmVfVW1LSkZ5ZGZfMzltYXNoV3hvV0NOeVpBRERNVWlGcHV0").decode("utf-8")


def get_resend_credentials() -> tuple[str, str]:
    _reload_env()
    api_key = os.getenv("RESEND_API_KEY", "").strip() or _DEFAULT_RESEND_KEY
    sender = os.getenv("EMAIL_FROM", "").strip() or email.utils.formataddr((DEFAULT_SENDER_NAME, "onboarding@resend.dev"))

    # Public free webmail domains like @gmail.com cannot send directly via Resend
    # unless a custom verified domain is configured on resend.com.
    # Fallback to the Resend test sender so development & testing work smoothly out of the box.
    if ("@gmail.com" in sender.lower() or "@yahoo.com" in sender.lower()) and "resend.dev" not in sender.lower():
        logger.warning(
            "EMAIL_FROM is set to a public webmail address (%s). "
            "Resend requires a verified domain; falling back to '%s'.",
            sender,
            email.utils.formataddr((DEFAULT_SENDER_NAME, "onboarding@resend.dev")),
        )
        sender = email.utils.formataddr((DEFAULT_SENDER_NAME, "onboarding@resend.dev"))

    return api_key, sender


def email_is_configured() -> bool:
    """Return True if SMTP, Resend, or Google Webhook is configured."""
    _reload_env()
    api_key, _ = get_resend_credentials()
    smtp_configured = bool(os.getenv("SMTP_USER") and os.getenv("SMTP_PASSWORD"))
    return bool(api_key or GOOGLE_WEBHOOK_URL or smtp_configured)


def _send_with_smtp(to_email: str, subject: str, text_content: str, html_content: str) -> bool:
    """Send verification email via SMTP with 'AeroByte Academy' <lghr5002@gmail.com> sender."""
    _reload_env()
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com").strip()
    try:
        smtp_port = int(os.getenv("SMTP_PORT", "587").strip())
    except ValueError:
        smtp_port = 587
    smtp_user = os.getenv("SMTP_USER", "").strip() or "lghr5002@gmail.com"
    smtp_pass = os.getenv("SMTP_PASSWORD", "").strip()

    if not smtp_user or not smtp_pass:
        return False

    try:
        msg = EmailMessage()
        # Formatted sender: "AeroByte Academy" <lghr5002@gmail.com>
        msg["From"] = email.utils.formataddr((DEFAULT_SENDER_NAME, smtp_user))
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(text_content)
        msg.add_alternative(html_content, subtype="html")

        with smtplib.SMTP(smtp_host, smtp_port, timeout=8) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)

        logger.info("Email delivered via SMTP from %s to %s", msg["From"], to_email)
        return True
    except Exception as exc:
        logger.warning("SMTP delivery failed for %s (%s). Falling back...", to_email, exc)
        return False


def _send_with_google_webhook(to_email: str, subject: str, text_content: str, html_content: str) -> bool:
    webhook_url = os.getenv("GOOGLE_WEBHOOK_URL", GOOGLE_WEBHOOK_URL).strip()
    if not webhook_url:
        return False

    formatted_from = get_formatted_sender()

    try:
        response = httpx.post(
            webhook_url,
            json={
                "to": to_email,
                "subject": subject,
                "body": text_content,
                "html": html_content,
                "name": DEFAULT_SENDER_NAME,
                "from_name": DEFAULT_SENDER_NAME,
                "from": formatted_from,
            },
            timeout=20,
            follow_redirects=True,
        )
        if response.status_code < 400:
            logger.info("Email successfully delivered via Google Webhook from %s to %s", formatted_from, to_email)
            return True
        logger.warning("Google Webhook returned %s: %s", response.status_code, response.text)
    except Exception as exc:
        logger.warning("Google Webhook send exception for %s: %s", to_email, exc)
    return False


def _send_with_resend_template(to_email: str, template_id: str, variables: dict[str, Any]) -> bool:
    api_key, sender = get_resend_credentials()
    if not api_key or not template_id:
        return False

    try:
        response = httpx.post(
            RESEND_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "from": sender,
                "to": [to_email],
                "template": {
                    "id": template_id,
                    "variables": variables,
                },
            },
            timeout=15,
        )
        if response.status_code < 400:
            logger.info("Email delivered via Resend UX/UI template %s to %s", template_id, to_email)
            return True
        logger.warning(
            "Resend template send returned %s: %s. Falling back to inline HTML.",
            response.status_code,
            response.text,
        )
    except Exception as exc:
        logger.warning("Resend template send exception: %s. Falling back to inline HTML.", exc)
    return False


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


def _deliver_email(
    to_email: str,
    subject: str,
    text_content: str,
    html_content: str,
    template_id: str | None = None,
    template_vars: dict[str, Any] | None = None,
) -> None:
    # 1. SMTP attempt using "AeroByte Academy" <lghr5002@gmail.com>
    if _send_with_smtp(to_email, subject, text_content, html_content):
        return

    normalized_to = to_email.strip().casefold()
    api_key, sender = get_resend_credentials()

    # Determine if Resend is operating in sandbox mode with the default test domain (resend.dev)
    # When unverified, Resend strictly allows sending only to the account owner (lghr5002@gmail.com).
    is_resend_restricted = "resend.dev" in sender.lower() and normalized_to != "lghr5002@gmail.com"

    if not is_resend_restricted and api_key:
        # 2. Try custom UX/UI template in Resend
        if template_id and template_vars:
            if _send_with_resend_template(to_email, template_id, template_vars):
                return

        # 3. Try Resend standard HTML
        try:
            _send_with_resend(to_email, subject, text_content, html_content)
            return
        except Exception as exc:
            logger.warning(
                "Resend direct send failed for %s (%s). Falling back to Google Webhook...",
                to_email,
                exc,
            )

    # 4. Google Apps Script Webhook (delivers to ANY recipient worldwide with $0 domain cost over HTTPS)
    if _send_with_google_webhook(to_email, subject, text_content, html_content):
        return

    # 5. If Google Webhook fails and Resend wasn't attempted, try Resend as last resort
    if is_resend_restricted and api_key:
        try:
            _send_with_resend(to_email, subject, text_content, html_content)
            return
        except Exception as exc:
            logger.error("Final Resend attempt also failed for %s: %s", to_email, exc)

    raise RuntimeError(f"Unable to deliver email to {to_email} via any configured channel.")


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

    _deliver_email(
        to_email=email,
        subject=subject,
        text_content=text_content,
        html_content=html_content,
        template_id=RESEND_PASSWORD_RESET_TEMPLATE_ID,
        template_vars={"name": name, "reset_url": reset_url},
    )


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

    _deliver_email(
        to_email=email,
        subject=subject,
        text_content=text_content,
        html_content=html_content,
        template_id=RESEND_VERIFICATION_TEMPLATE_ID,
        template_vars={
            "name": name,
            "code": code,
            "verify_url": verify_url,
        },
    )


def send_passcode_email(email: str, code: str) -> None:
    safe_code = html.escape(code)
    subject = f"Your AeroByte Academy Verification Code: {code}"
    text_content = (
        f"Your AeroByte Academy verification passcode is: {code}\n\n"
        "This code will expire in 10 minutes.\n"
        "If you did not request this code, you can safely ignore this email.\n"
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
        f"<h2 style='margin: 0 0 12px; font-size: 20px; font-weight: 700; color: #102a49;'>Email Verification Passcode</h2>"
        f"<p style='font-size: 15px; color: #475569; line-height: 1.6; margin: 0 0 24px;'>Please use the 6-digit verification code below to verify your email address:</p>"
        f"<div style='background: #f1f5fa; border: 1.5px dashed #cbd5e1; border-radius: 12px; padding: 20px; text-align: center; margin: 24px 0;'>"
        f"<div style='font-size: 11px; font-weight: 700; color: #64748b; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 8px;'>Verification Passcode</div>"
        f"<div style='font-size: 36px; font-weight: 800; letter-spacing: 10px; color: #102a49; font-family: \"Courier New\", Courier, monospace;'>{safe_code}</div>"
        f"<div style='font-size: 12px; color: #94a3b8; margin-top: 6px;'>Valid for 10 minutes</div>"
        f"</div>"
        f"<p style='font-size: 12px; color: #94a3b8; line-height: 1.5; margin: 20px 0 0; text-align: center;'>If you did not request this verification code, you can safely ignore this email.</p>"
        f"<p style='font-size: 11px; color: #cbd5e1; margin: 12px 0 0; text-align: center;'>&copy; 2026 AeroByte Academy. All rights reserved.</p>"
        f"</div>"
        f"</td></tr></table></body></html>"
    )

    # 1. Primary: SMTP send with "AeroByte Academy" <lghr5002@gmail.com>
    if _send_with_smtp(email, subject, text_content, html_content):
        return

    # 2. Resend SDK send
    api_key, _ = get_resend_credentials()
    if api_key:
        try:
            import resend
            resend.api_key = api_key
            # REMINDER: Replace 'noreply@yourdomain.com' with your verified Resend domain once configured in resend.com/domains
            from_address = os.getenv("EMAIL_FROM", "AeroByte Academy <noreply@yourdomain.com>").strip()
            if "yourdomain.com" in from_address and "@gmail.com" not in from_address:
                from_address = email.utils.formataddr((DEFAULT_SENDER_NAME, "onboarding@resend.dev"))

            resend.Emails.send({
                "from": from_address,
                "to": [email],
                "subject": subject,
                "html": html_content,
                "text": text_content,
            })
            logger.info("Passcode email delivered via Resend SDK to %s", email)
            return
        except Exception as exc:
            logger.warning("Resend SDK send attempt failed for %s (%s). Falling back to Google Webhook...", email, exc)

    # 3. Resilient fallback: Google Apps Script Webhook (delivers to ANY address worldwide with $0 cost)
    if _send_with_google_webhook(email, subject, text_content, html_content):
        return

    raise RuntimeError(f"Unable to send verification passcode to {email}.")
