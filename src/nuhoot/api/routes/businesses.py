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
from nuhoot.services.finder import FinderService

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
    has_website: bool = False
    has_instagram: bool = False
    status: str = "found"


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
) -> dict[str, object]:
    """Trigger a Google Maps scrape for the given category and city."""
    service = FinderService(db, delay=float(settings.scraper_delay_seconds))
    businesses = service.search(
        category=request.category,
        city=request.city,
        max_results=request.max_results,
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
