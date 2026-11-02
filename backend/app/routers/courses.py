from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import math
from app.models import Course, PaginatedCourseResponse
from app.content_store import find_course, list_published_courses

router = APIRouter(prefix="/api/courses", tags=["Courses"])

@router.get("", response_model=PaginatedCourseResponse)
def get_courses(
    search: Optional[str] = Query(None),
    categories: Optional[List[str]] = Query(None),
    levels: Optional[List[str]] = Query(None),
    price_range: Optional[str] = Query("all"),
    languages: Optional[List[str]] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(9, ge=1, le=50)
):
    filtered = list_published_courses()
    if search:
        q = search.lower().strip()
        filtered = [c for c in filtered if q in c.title.lower() or q in c.short_description.lower() or q in c.category.lower()]
    if categories:
        cat_set = {c.lower() for c in categories}
        filtered = [c for c in filtered if c.category.lower() in cat_set]
    if levels:
        lvl_set = {l.lower() for l in levels}
        filtered = [c for c in filtered if c.level and c.level.lower() in lvl_set]
    if price_range and price_range != "all":
        if price_range == "under_100":
            filtered = [c for c in filtered if c.price < 100]
        elif price_range == "100_200":
            filtered = [c for c in filtered if 100 <= c.price <= 200]
        elif price_range == "over_200":
            filtered = [c for c in filtered if c.price > 200]
    if languages:
        lang_set = {lang.lower() for lang in languages}
        filtered = [c for c in filtered if c.language and c.language.lower() in lang_set]

    total = len(filtered)
    total_pages = max(1, math.ceil(total / limit))
    start = (page - 1) * limit
    return PaginatedCourseResponse(
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages,
        courses=filtered[start:start + limit]
    )

@router.get("/{course_id}", response_model=Course)
def get_course_detail(course_id: str):
    course = find_course(course_id)
    if course and course.status == "published":
        return course
    raise HTTPException(status_code=404, detail="Course not found")
