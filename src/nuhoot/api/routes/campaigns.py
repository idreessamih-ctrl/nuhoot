"""API routes for campaigns — batch WhatsApp sending."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from nuhoot.database import get_db
from nuhoot.models.business import Business
from nuhoot.models.campaign import Campaign
from nuhoot.models.pitch import Pitch
from nuhoot.services.sender import SenderError, SenderService

router = APIRouter(prefix="/campaigns", tags=["campaigns"])

DbDep = Annotated[Session, Depends(get_db)]


class BatchSendResult(BaseModel):
    """Summary of a campaign batch send operation."""

    sent: int = 0
    failed: int = 0
    total: int = 0


@router.post("", response_model=None)
def create_campaign(
    db: DbDep,
    name: str = Form(...),
    niche: str = Form(...),
    city: str = Form(...),
    lang: str = Form("ar"),
) -> RedirectResponse:
    """Create a new campaign, then redirect back to the campaigns page."""
    campaign = Campaign(name=name, niche=niche, city=city, language=lang)
    db.add(campaign)
    db.commit()
    return RedirectResponse(url=f"/campaigns-page?lang={lang}", status_code=303)


@router.post("/{campaign_id}/send", response_model=None)
def send_campaign_pitches(
    campaign_id: int,
    request: Request,
    db: DbDep,
    lang: str = Form("ar"),
) -> dict[str, object] | JSONResponse | RedirectResponse:
    """Send pitches to all businesses in a campaign (batch).

    Iterates over every business linked to the campaign, finds its latest
    pitch, and sends it via WhatsApp. Businesses without a pitch are counted
    as failed. Rate limiting is handled inside SenderService.

    Returns JSON for API calls; redirects to campaigns page for form posts.
    """
    campaign = db.get(Campaign, campaign_id)
    if campaign is None:
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "data": None,
                "error": f"Campaign {campaign_id} not found",
            },
        )

    stmt = select(Business).where(Business.campaign_id == campaign_id)
    businesses = list(db.scalars(stmt).all())

    service = SenderService(db)
    sent = 0
    failed = 0
    for biz in businesses:
        pitch_stmt = (
            select(Pitch).where(Pitch.business_id == biz.id).order_by(Pitch.created_at.desc())
        )
        pitch = db.scalars(pitch_stmt).first()
        if pitch is None:
            failed += 1
            continue
        try:
            service.send_pitch(biz, pitch)
            sent += 1
        except SenderError:
            failed += 1

    result = BatchSendResult(sent=sent, failed=failed, total=len(businesses))
    if request.headers.get("accept", "").startswith("text/html"):
        return RedirectResponse(
            url=f"/campaigns-page?lang={lang}&msg=sent-{sent}-{failed}-{len(businesses)}",
            status_code=303,
        )
    return {"success": True, "data": result, "error": None}
