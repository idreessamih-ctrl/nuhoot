"""API routes for WhatsApp message sending (business-scoped).

Provides endpoints to send an AI-crafted pitch to a business via the
WhatsApp Cloud API and to list the delivery history for a business.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, ConfigDict
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from nuhoot.database import get_db
from nuhoot.models.business import Business
from nuhoot.models.message import Message
from nuhoot.models.pitch import Pitch
from nuhoot.services.sender import SenderError, SenderService

router = APIRouter(prefix="/businesses", tags=["messages"])

DbDep = Annotated[Session, Depends(get_db)]


# ------------------------------------------------------------------
# Schemas
# ------------------------------------------------------------------


class MessageResponse(BaseModel):
    """Serialized WhatsApp message delivery record."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    pitch_id: int
    business_id: int
    phone_number: str
    whatsapp_message_id: str | None = None
    status: str = "pending"
    error_message: str | None = None


# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------


@router.post("/{business_id}/send", response_model=None)
def send_business_pitch(
    business_id: int,
    request: Request,
    db: DbDep,
    lang: str = Form("ar"),
) -> dict[str, object] | JSONResponse | RedirectResponse:
    """Send the latest pitch to a business via WhatsApp.

    Returns JSON for API calls; redirects to businesses page for form posts.
    """
    biz = db.get(Business, business_id)
    if biz is None:
        return JSONResponse(
            status_code=404,
            content={"success": False, "data": None, "error": f"Business {business_id} not found"},
        )
    stmt = select(Pitch).where(Pitch.business_id == business_id).order_by(Pitch.created_at.desc())
    pitch = db.scalars(stmt).first()
    if pitch is None:
        return JSONResponse(
            status_code=404,
            content={"success": False, "data": None, "error": f"No pitch found for business {business_id}"},
        )
    service = SenderService(db)
    try:
        message = service.send_pitch(biz, pitch)
    except SenderError as exc:
        return JSONResponse(
            status_code=500,
            content={"success": False, "data": None, "error": str(exc)},
        )
    if request.headers.get("accept", "").startswith("text/html"):
        return RedirectResponse(url=f"/businesses-page?lang={lang}&msg=sent", status_code=303)
    return {"success": True, "data": MessageResponse.model_validate(message), "error": None}


@router.get("/{business_id}/messages", response_model=None)
def list_business_messages(
    business_id: int,
    db: DbDep,
    page: int = 1,
    per_page: int = 20,
) -> dict[str, object] | JSONResponse:
    """List all WhatsApp messages sent to a business."""
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
    page = max(page, 1)
    per_page = min(max(per_page, 1), 100)
    offset = (page - 1) * per_page
    stmt = (
        select(Message)
        .where(Message.business_id == business_id)
        .order_by(Message.created_at.desc())
        .offset(offset)
        .limit(per_page)
    )
    items = list(db.scalars(stmt).all())
    total = (
        db.scalar(
            select(func.count()).select_from(Message).where(Message.business_id == business_id)
        )
        or 0
    )
    return {
        "success": True,
        "data": {
            "items": [MessageResponse.model_validate(m) for m in items],
            "total": total,
            "page": page,
            "per_page": per_page,
        },
        "error": None,
    }
