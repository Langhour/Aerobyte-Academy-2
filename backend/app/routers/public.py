from fastapi import APIRouter

from app.content_store import get_site_settings

router = APIRouter(prefix="/api/site-settings", tags=["Site settings"])


@router.get("")
def public_site_settings():
    settings = get_site_settings()
    return {
        "about_courses": settings.about_courses,
        "about_learning": settings.about_learning,
        "about_mentors": settings.about_mentors,
        "about_projects": settings.about_projects,
        "contact_email": settings.contact_email,
        "contact_phone": settings.contact_phone,
        "footer_description": settings.footer_description,
        "merchant_qr_url": settings.merchant_qr_url,
        "merchant_bank_info": settings.merchant_bank_info,
        "payment_session_minutes": settings.payment_session_minutes,
    }
