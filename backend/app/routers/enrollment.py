from datetime import date, datetime, timezone, timedelta
import uuid

CAMBODIA_TZ = timezone(timedelta(hours=7))

from fastapi import APIRouter, HTTPException, Request
from typing import Optional

from app.content_store import (
    find_coupon,
    find_enrollment,
    find_course,
    increment_coupon_usage,
    list_enrollments,
    log_admin_activity,
    save_enrollment,
)
from app.models import (
    CouponValidateRequest,
    CouponValidateResponse,
    EnrollmentCreate,
    EnrollmentRecord,
    PaymentSession,
    PaymentStatusEvent,
)

router = APIRouter(prefix="/api/enrollments", tags=["Enrollments & Payments"])

ADMINISTRATION_FEE = 7.50
CERTIFICATION_FEE = 5.00
CARD_FEE = 2.50
TOTAL_FEES = ADMINISTRATION_FEE + CERTIFICATION_FEE + CARD_FEE


@router.get("/fees")
def get_enrollment_fees():
    return {
        "administration_fee": ADMINISTRATION_FEE,
        "certification_fee": CERTIFICATION_FEE,
        "card_fee": CARD_FEE,
        "total_fees": TOTAL_FEES,
        "breakdown": [
            {"label": "Administration fee", "amount": ADMINISTRATION_FEE},
            {"label": "Certification fee", "amount": CERTIFICATION_FEE},
            {"label": "Card fee", "amount": CARD_FEE},
        ],
    }


def _coupon_error(code: str) -> str | None:
    coupon = find_coupon(code)
    if coupon is None or not coupon.active:
        return "Invalid or expired coupon code."
    if coupon.expires_at:
        try:
            expires = date.fromisoformat(coupon.expires_at)
        except ValueError:
            return "This coupon has an invalid expiry date."
        if expires < datetime.now(timezone.utc).date():
            return "Invalid or expired coupon code."
    if coupon.max_usage is not None and coupon.usage_count >= coupon.max_usage:
        return "This coupon has reached its usage limit."
    return None


def _discount(code: str, price: float) -> tuple[float, float, int]:
    coupon = find_coupon(code)
    if coupon is None:
        return 0, price, 0
    if coupon.code == "TEST1CENT":
        discount = round(max(0.0, price - 0.01), 2)
        return discount, 0.01, 99
    if coupon.discount_type == "fixed":
        discount = min(price, coupon.value)
        percent = round(discount / price * 100) if price else 0
    else:
        percent = round(coupon.value)
        discount = round(price * percent / 100, 2)
    return discount, round(max(0.0, price - discount), 2), percent


@router.post("/validate-coupon", response_model=CouponValidateResponse)
def validate_coupon(payload: CouponValidateRequest):
    code = payload.code.strip().upper()
    error = _coupon_error(code)
    if error:
        return CouponValidateResponse(
            valid=False,
            code=code,
            discount_percent=0,
            discount_amount=0.0,
            final_price=round(payload.course_price + TOTAL_FEES, 2),
            message=error,
        )

    discount_amount, discounted_course_price, percentage = _discount(code, payload.course_price)
    final_price = round(discounted_course_price + TOTAL_FEES, 2)
    message = (
        "Test mode coupon applied ($0.01 course price before fees)!"
        if code == "TEST1CENT"
        else f"Coupon applied! You saved ${discount_amount:.2f} ({percentage}% OFF)."
    )
    return CouponValidateResponse(
        valid=True,
        code=code,
        discount_percent=percentage,
        discount_amount=discount_amount,
        final_price=final_price,
        message=message,
    )


@router.post("", response_model=PaymentSession)
def create_enrollment(payload: EnrollmentCreate):
    course = find_course(payload.course_id)
    if not course or course.status != "published":
        raise HTTPException(status_code=404, detail="Selected course not found")

    if not payload.gender or not payload.gender.strip():
        raise HTTPException(status_code=422, detail="Gender is required to process enrollment.")
    if not payload.age_range or not payload.age_range.strip():
        raise HTTPException(status_code=422, detail="Age range is required to process enrollment.")
    if not payload.highest_qualification or not payload.highest_qualification.strip():
        raise HTTPException(status_code=422, detail="Highest qualification is required to process enrollment.")

    schedule_display = payload.time_slot
    if course.batch_schedules:
        selected_batch = next(
            (
                batch for batch in course.batch_schedules
                if batch.active
                and batch.day_type == payload.preferred_schedule
                and batch.time_slot == payload.time_slot
            ),
            None,
        )
        if selected_batch is None:
            raise HTTPException(status_code=400, detail="Selected course schedule is unavailable.")
        schedule_display = f"{selected_batch.time_slot} · {selected_batch.start_time} - {selected_batch.end_time}"
        reserved = sum(
            record.course_id == course.id
            and record.preferred_schedule == selected_batch.day_type
            and record.time_slot == schedule_display
            and record.enrollment_status != "cancelled"
            and record.status != "expired"
            for record in list_enrollments()
        )
        if reserved >= selected_batch.max_seats:
            raise HTTPException(status_code=409, detail="This course batch is full.")

    code = payload.coupon_code.strip().upper() if payload.coupon_code else ""
    if code:
        error = _coupon_error(code)
        if error:
            raise HTTPException(status_code=400, detail=error)
        discount_amount, discounted_course_price, _ = _discount(code, course.price)
    else:
        discount_amount, discounted_course_price = 0.0, course.price
    amount_due = round(discounted_course_price + TOTAL_FEES, 2)

    enrollment_id = f"ENR-{uuid.uuid4().hex[:8].upper()}"
    transaction_id = f"TXN-{uuid.uuid4().hex[:10].upper()}"
    created_at = datetime.now(CAMBODIA_TZ).strftime("%b %d, %Y %I:%M %p")
    record = EnrollmentRecord(
        enrollment_id=enrollment_id,
        transaction_id=transaction_id,
        course_id=course.id,
        course_title=course.title,
        course_slug=course.slug,
        course_image=course.image_url,
        student_name=payload.full_name,
        email=payload.email,
        phone_telegram=payload.phone_telegram,
        phone_number=payload.phone_number,
        preferred_schedule=payload.preferred_schedule,
        time_slot=schedule_display,
        preferred_start_date=payload.preferred_start_date,
        original_price=course.original_price or course.price,
        discount_amount=round(max(0.0, (course.original_price or course.price) - course.price) + discount_amount, 2),
        base_price=discounted_course_price,
        administration_fee=ADMINISTRATION_FEE,
        certification_fee=CERTIFICATION_FEE,
        card_fee=CARD_FEE,
        amount_due=amount_due,
        status="pending",
        enrollment_status="pending",
        created_at=created_at,
        payment_history=[PaymentStatusEvent(status="pending", created_at=created_at, note="QR checkout created")],
        date_of_birth=payload.date_of_birth,
        gender=payload.gender,
        address=payload.address,
        age_range=payload.age_range,
        highest_qualification=payload.highest_qualification,
        current_occupation=payload.current_occupation,
        coding_experience=payload.coding_experience,
        special_requirements=payload.special_requirements,
        coupon_code=code or None,
    )
    save_enrollment(record)
    if code:
        increment_coupon_usage(code)
    log_admin_activity(
        "New enrollment",
        f"{record.student_name} enrolled in {record.course_title}",
        datetime.now(CAMBODIA_TZ).strftime("%b %d, %Y %I:%M %p"),
    )
    return PaymentSession.model_validate(record.model_dump())


@router.get("/my-history", response_model=list[EnrollmentRecord])
def get_my_enrollment_history(
    request: Request,
    email: Optional[str] = None,
    ids: Optional[str] = None,
):
    from app.routers.accounts import get_account_enrollments
    return get_account_enrollments(request=request, email=email, ids=ids)


@router.get("/{enrollment_id}", response_model=EnrollmentRecord)
def get_enrollment(enrollment_id: str):
    record = find_enrollment(enrollment_id)
    if not record:
        raise HTTPException(status_code=404, detail="Enrollment session not found")
    return record


@router.post("/{enrollment_id}/status", response_model=PaymentSession)
def update_payment_status(enrollment_id: str, status: str):
    if status not in {"expired", "pending"}:
        raise HTTPException(status_code=400, detail="Invalid payment status")

    record = find_enrollment(enrollment_id)
    if not record:
        raise HTTPException(status_code=404, detail="Enrollment session not found")
    if status == "pending" and record.status != "expired":
        raise HTTPException(status_code=400, detail="Only an expired session can be restarted.")
    record.status = status
    event_time = datetime.now(CAMBODIA_TZ).strftime("%b %d, %Y %I:%M %p")
    record.payment_history.append(
        PaymentStatusEvent(status=status, created_at=event_time, note="Customer payment session update")
    )
    save_enrollment(record)
    return PaymentSession.model_validate(record.model_dump())
