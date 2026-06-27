"""API routes for businesses (leads found by the Finder)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from nuhoot.config import settings
from nuhoot.database import get_db
from nuhoot.models.business import Business
from nuhoot.models.pitch import Pitch
from nuhoot.services.crafter import CrafterError, CrafterService
from nuhoot.services.finder import FinderError, FinderService
from nuhoot.services.investigator import InvestigatorService

router = APIRouter(prefix="/businesses", tags=["businesses"])

DbDep = Annotated[Session, Depends(get_db)]


# ------------------------------------------------------------------
# Schemas
# ------------------------------------------------------------------


class SearchRequest(BaseModel):
    """Request body for POST /businesses/search."""

    category: str = Field(..., min_length=1, description="Business type to search")
    city: str = Field(..., min_length=1, description="Saudi city name")
    max_results: int = Field(default=200, ge=1, le=500)


class BusinessResponse(BaseModel):
    """Serialized business / lead."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    phone: str | None = None
    whatsapp: str | None = None
    address: str | None = None
    website: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    rating: float | None = None
    review_count: int | None = None
    instagram: str | None = None
    has_website: bool = False
    has_instagram: bool = False
    seo_score: int | None = None
    social_score: int | None = None
    status: str = "found"


class PitchResponse(BaseModel):
    """Serialized pitch — AI-generated WhatsApp message + sample posts."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    business_id: int
    pitch_text: str
    sample_posts: list[str]
    language: str = "ar"
    status: str = "draft"


# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------


@router.get("", response_model=None)
def list_businesses(
    db: DbDep,
    page: int = 1,
    per_page: int = 20,
) -> dict[str, object]:
    """List all stored businesses with pagination."""
    page = max(page, 1)
    per_page = min(max(per_page, 1), 100)
    offset = (page - 1) * per_page

    stmt = select(Business).offset(offset).limit(per_page)
    items = list(db.scalars(stmt).all())
    total = db.scalar(select(func.count()).select_from(Business)) or 0

    return {
        "success": True,
        "data": {
            "items": [BusinessResponse.model_validate(b) for b in items],
            "total": total,
            "page": page,
            "per_page": per_page,
        },
        "error": None,
    }


@router.post("/search", status_code=201, response_model=None)
def search_businesses(
    request: SearchRequest,
    db: DbDep,
) -> dict[str, object] | JSONResponse:
    """Trigger a Google Maps scrape for the given category and city."""
    service = FinderService(db, delay=float(settings.scraper_delay_seconds))
    try:
        businesses = service.search(
            category=request.category,
            city=request.city,
            max_results=request.max_results,
        )
    except FinderError as exc:
        return JSONResponse(
            status_code=502,
            content={
                "success": False,
                "data": None,
                "error": f"Scraper failed: {exc}",
            },
        )
    return {
        "success": True,
        "data": {
            "count": len(businesses),
            "businesses": [BusinessResponse.model_validate(b) for b in businesses],
        },
        "error": None,
    }


@router.get("/{business_id}", response_model=None)
def get_business(
    business_id: int,
    db: DbDep,
) -> dict[str, object] | JSONResponse:
    """Get a single business by ID."""
    biz = db.get(Business, business_id)
    if biz is None:
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "data": None,
                "error": f"Business {business_id} not found",
            },
        )
    return {
        "success": True,
        "data": BusinessResponse.model_validate(biz),
        "error": None,
    }


@router.post("/{business_id}/investigate", response_model=None)
def investigate_business(
    business_id: int,
    db: DbDep,
) -> dict[str, object] | JSONResponse:
    """Trigger digital presence investigation for a business."""
    biz = db.get(Business, business_id)
    if biz is None:
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "data": None,
                "error": f"Business {business_id} not found",
            },
        )
    service = InvestigatorService(db)
    service.investigate(biz)
    return {
        "success": True,
        "data": BusinessResponse.model_validate(biz),
        "error": None,
    }


@router.post("/{business_id}/craft", response_model=None)
def craft_business_pitch(
    business_id: int,
    db: DbDep,
) -> dict[str, object] | JSONResponse:
    """Generate an AI pitch for a business using GLM 5.2."""
    biz = db.get(Business, business_id)
    if biz is None:
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "data": None,
                "error": f"Business {business_id} not found",
            },
        )
    service = CrafterService(db)
    try:
        pitch = service.craft_pitch(biz)
    except CrafterError as exc:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "data": None,
                "error": str(exc),
            },
        )
    return {
        "success": True,
        "data": PitchResponse.model_validate(pitch),
        "error": None,
    }


@router.get("/{business_id}/pitch", response_model=None)
def get_business_pitch(
    business_id: int,
    db: DbDep,
) -> dict[str, object] | JSONResponse:
    """Get the most recent pitch for a business."""
    biz = db.get(Business, business_id)
    if biz is None:
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "data": None,
                "error": f"Business {business_id} not found",
            },
        )
    stmt = select(Pitch).where(Pitch.business_id == business_id).order_by(Pitch.created_at.desc())
    pitch = db.scalars(stmt).first()
    if pitch is None:
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "data": None,
                "error": f"No pitch found for business {business_id}",
            },
        )
    return {
        "success": True,
        "data": PitchResponse.model_validate(pitch),
        "error": None,
    }
