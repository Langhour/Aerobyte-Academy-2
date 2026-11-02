from datetime import date

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional

class BatchSchedule(BaseModel):
    day_type: str = Field(min_length=1, max_length=80)
    time_slot: str = Field(min_length=1, max_length=80)
    start_time: str = Field(min_length=1, max_length=40)
    end_time: str = Field(min_length=1, max_length=40)
    max_seats: int = Field(default=20, ge=1, le=1000)
    active: bool = True

class CourseModule(BaseModel):
    module_number: str
    title: str
    description: str
    icon_type: str
    image_url: str = ""
    title_kh: Optional[str] = None
    description_kh: Optional[str] = None

class HardwareSpec(BaseModel):
    title: str
    items: List[str]
    title_kh: Optional[str] = None
    items_kh: Optional[List[str]] = Field(default_factory=list)

class Course(BaseModel):
    id: str
    slug: str
    title: str
    short_description: str
    category: str
    section_group: str
    level: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    discount_badge: Optional[str] = None
    language: Optional[str] = None
    duration: Optional[str] = None
    image_url: str = ""
    status: str = "published"
    order_index: Optional[int] = 0
    badges: List[str] = Field(default_factory=list)
    batch_schedules: List[BatchSchedule] = Field(default_factory=list)
    modules: List[CourseModule] = Field(default_factory=list)
    hardware_specs: List[HardwareSpec] = Field(default_factory=list)
    title_kh: Optional[str] = None
    short_description_kh: Optional[str] = None
    category_kh: Optional[str] = None
    level_kh: Optional[str] = None
    duration_kh: Optional[str] = None
    badges_kh: List[str] = Field(default_factory=list)

class CourseReorderRequest(BaseModel):
    course_ids: List[str]

class PaginatedCourseResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    courses: List[Course]

class EnrollmentCreate(BaseModel):
    course_id: str
    full_name: str
    date_of_birth: str
    gender: str
    phone_telegram: str
    phone_number: Optional[str] = None
    email: str
    parent_phone: Optional[str] = None
    address: str
    age_range: str
    highest_qualification: str
    current_occupation: str
    coding_experience: Optional[str] = None
    preferred_start_date: str
    preferred_schedule: str
    time_slot: str
    special_requirements: Optional[str] = None
    coupon_code: Optional[str] = None

class CouponValidateRequest(BaseModel):
    code: str
    course_price: float = Field(ge=0, le=1_000_000)

class CouponValidateResponse(BaseModel):
    valid: bool
    code: str
    discount_percent: int
    discount_amount: float
    final_price: float
    message: str

class PaymentStatusEvent(BaseModel):
    status: str
    created_at: str
    note: str = ""

class EnrollmentRecord(BaseModel):
    enrollment_id: str
    transaction_id: str
    course_id: str
    course_title: str
    course_slug: str
    course_image: str
    student_name: str
    email: str
    phone_telegram: str
    phone_number: Optional[str] = None
    preferred_schedule: str
    time_slot: str = ""
    preferred_start_date: str
    original_price: float
    discount_amount: float
    base_price: float = 0.0
    administration_fee: float = 7.50
    certification_fee: float = 5.00
    card_fee: float = 2.50
    amount_due: float
    status: str
    payment_history: List["PaymentStatusEvent"] = Field(default_factory=list)
    enrollment_status: str = "pending"
    created_at: str
    date_of_birth: str = ""
    gender: str = ""
    address: str = ""
    age_range: str = ""
    highest_qualification: str = ""
    current_occupation: str = ""
    coding_experience: Optional[str] = None
    special_requirements: Optional[str] = None
    coupon_code: Optional[str] = None

class PaymentSession(BaseModel):
    enrollment_id: str
    transaction_id: str
    course_id: str
    course_title: str
    course_slug: str
    course_image: str
    student_name: str = ""
    email: str = ""
    phone_telegram: str = ""
    phone_number: Optional[str] = None
    address: str = ""
    preferred_schedule: str = ""
    time_slot: str = ""
    preferred_start_date: str = ""
    date_of_birth: str = ""
    gender: str = ""
    age_range: str = ""
    highest_qualification: str = ""
    current_occupation: str = ""
    coding_experience: Optional[str] = None
    special_requirements: Optional[str] = None
    coupon_code: Optional[str] = None
    original_price: float
    discount_amount: float
    base_price: float = 0.0
    administration_fee: float = 7.50
    certification_fee: float = 5.00
    card_fee: float = 2.50
    amount_due: float
    status: str
    enrollment_status: str = "pending"
    created_at: str

class Coupon(BaseModel):
    code: str = Field(min_length=3, max_length=40)
    discount_type: str = Field(default="percent", pattern="^(percent|fixed)$")
    value: float = Field(gt=0, le=1_000_000)
    max_usage: Optional[int] = Field(default=None, ge=1)
    usage_count: int = Field(default=0, ge=0)
    expires_at: Optional[str] = None
    active: bool = True

    @field_validator("code")
    @classmethod
    def normalize_code(cls, value):
        normalized = value.strip().upper()
        if len(normalized) < 3:
            raise ValueError("Coupon code must contain at least three non-space characters.")
        return normalized

    @field_validator("expires_at")
    @classmethod
    def validate_expiry_date(cls, value):
        if value:
            try:
                date.fromisoformat(value)
            except ValueError as exc:
                raise ValueError("Expiry date must use YYYY-MM-DD format.") from exc
        return value or None

    @model_validator(mode="after")
    def validate_percent_discount(self):
        if self.discount_type == "percent" and self.value > 100:
            raise ValueError("Percentage discounts cannot exceed 100.")
        return self

class SiteSettings(BaseModel):
    about_courses: str = "15+"
    about_learning: str = "100%"
    about_mentors: str = "12+"
    about_projects: str = "500+"
    contact_email: str = ""
    contact_phone: str = ""
    footer_description: str = ""
    merchant_qr_url: str = "/aba-qr.png"
    merchant_bank_info: str = "ABA Bank: VIDHCHETRA KHEMARAK"
    payment_session_minutes: int = Field(default=15, ge=1, le=1440)
