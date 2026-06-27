"""Dashboard HTML routes — bilingual web UI (Arabic RTL + English LTR).

All routes accept ``?lang=ar`` or ``?lang=en`` (default ``ar``) and store the
preference in a cookie for persistence across sessions.
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from nuhoot.database import get_db
from nuhoot.models.business import Business
from nuhoot.models.campaign import Campaign
from nuhoot.services.stats import (
    get_active_campaigns,
    get_dashboard_stats,
    get_quota_usage,
    get_recent_businesses,
    get_seo_distribution,
    get_top_categories,
)
from nuhoot.translations import DEFAULT_LANG, SUPPORTED_LANGS, t

router = APIRouter(tags=["dashboard"])

DbDep = Annotated[Session, Depends(get_db)]

_TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates"
templates = Jinja2Templates(directory=str(_TEMPLATES_DIR))
templates.env.globals["t"] = t  # make t() callable inside Jinja2 templates

_COOKIE_MAX_AGE = 2592000  # 30 days


def _valid_lang(lang: str) -> str:
    """Return ``lang`` if supported, else the default (Arabic)."""
    return lang if lang in SUPPORTED_LANGS else DEFAULT_LANG


def _render(request: Request, template: str, lang: str, context: dict[str, object]) -> Response:
    """Render a template and set the lang cookie for persistence."""
    result = templates.TemplateResponse(request, template, context)
    result.set_cookie("lang", lang, max_age=_COOKIE_MAX_AGE)
    return result


# ------------------------------------------------------------------ #
# Routes
# ------------------------------------------------------------------ #


@router.get("/", response_model=None)
def root() -> RedirectResponse:
    """Redirect to the Arabic dashboard."""
    return RedirectResponse(url="/dashboard?lang=ar", status_code=302)


@router.get("/dashboard", response_model=None)
def dashboard_page(request: Request, db: DbDep, lang: str = "ar") -> Response:
    """Stats overview page — bilingual."""
    lang = _valid_lang(lang)
    stats = get_dashboard_stats(db)
    recent = get_recent_businesses(db)
    active = get_active_campaigns(db)
    return _render(
        request,
        "dashboard.html",
        lang,
        {
            "lang": lang,
            "active": "dashboard",
            "stats": stats,
            "recent_businesses": recent,
            "active_campaigns": active,
        },
    )


@router.get("/businesses-page", response_model=None)
def businesses_page(
    request: Request,
    db: DbDep,
    lang: str = "ar",
    page: int = 1,
) -> Response:
    """Businesses management page — table, filters, pagination."""
    lang = _valid_lang(lang)
    page = max(page, 1)
    per_page = 20
    offset = (page - 1) * per_page

    businesses = list(db.scalars(select(Business).offset(offset).limit(per_page)).all())
    total = db.scalar(select(func.count()).select_from(Business)) or 0
    total_pages = max(int(total + per_page - 1) // per_page, 1)
    categories = list(db.scalars(select(Business.category).distinct()).all())

    return _render(
        request,
        "businesses.html",
        lang,
        {
            "lang": lang,
            "active": "businesses",
            "businesses": businesses,
            "categories": categories,
            "page": page,
            "total_pages": total_pages,
        },
    )


@router.get("/campaigns-page", response_model=None)
def campaigns_page(request: Request, db: DbDep, lang: str = "ar") -> Response:
    """Campaigns page — cards with stats and create form."""
    lang = _valid_lang(lang)
    campaigns = list(db.scalars(select(Campaign)).all())
    return _render(
        request,
        "campaigns.html",
        lang,
        {
            "lang": lang,
            "active": "campaigns",
            "campaigns": campaigns,
        },
    )


@router.get("/analytics", response_model=None)
def analytics_page(request: Request, db: DbDep, lang: str = "ar") -> Response:
    """Analytics page — quota, response rate, top categories, SEO distribution."""
    lang = _valid_lang(lang)
    stats = get_dashboard_stats(db)
    quota = get_quota_usage(db)
    quota_pct = round(quota["used"] / quota["limit"] * 100, 1) if quota["limit"] > 0 else 0.0

    top_raw = get_top_categories(db)
    max_cat = max((int(c["count"]) for c in top_raw), default=1) or 1
    top_categories = [
        {
            "category": c["category"],
            "count": int(c["count"]),
            "pct": round(int(c["count"]) / max_cat * 100, 1),
        }
        for c in top_raw
    ]

    seo_dist = get_seo_distribution(db)
    max_seo = max(seo_dist.values(), default=1) or 1
    seo_pct = {k: round(v / max_seo * 100, 1) for k, v in seo_dist.items()}

    return _render(
        request,
        "analytics.html",
        lang,
        {
            "lang": lang,
            "active": "analytics",
            "stats": stats,
            "quota": quota,
            "quota_pct": quota_pct,
            "top_categories": top_categories,
            "seo_dist": seo_dist,
            "seo_pct": seo_pct,
            "contacted_pct": min(float(stats["response_rate"]) * 2, 100.0),
            "responded_pct": float(stats["response_rate"]),
        },
    )
