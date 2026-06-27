"""Dashboard statistics service — aggregates metrics from the database."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from nuhoot.models.business import Business
from nuhoot.models.campaign import Campaign
from nuhoot.models.message import Message

# WhatsApp Cloud API free tier — 1,000 conversations / month.
WHATSAPP_MONTHLY_LIMIT: int = 1000

# Message statuses that count as "successfully sent" (consumed quota).
_SENT_STATUSES: tuple[str, ...] = ("sent", "delivered", "read")


def _count_sent_messages(db: Session) -> int:
    """Count messages whose status indicates successful delivery."""
    result = db.scalar(
        select(func.count()).select_from(Message).where(Message.status.in_(_SENT_STATUSES))
    )
    return int(result or 0)


def get_dashboard_stats(db: Session) -> dict[str, int | float]:
    """Return the four headline metrics shown on the dashboard overview.

    - total_businesses: count of all Business rows
    - total_campaigns: count of all Campaign rows
    - messages_sent: count of Messages with a sent/delivered/read status
    - response_rate: responded / contacted * 100 (aggregated from campaigns)
    """
    total_businesses = db.scalar(select(func.count()).select_from(Business)) or 0
    total_campaigns = db.scalar(select(func.count()).select_from(Campaign)) or 0
    messages_sent = _count_sent_messages(db)

    campaigns = list(db.scalars(select(Campaign)).all())
    total_contacted = sum(c.contacted for c in campaigns)
    total_responded = sum(c.responded for c in campaigns)
    response_rate: float = (
        round(total_responded / total_contacted * 100, 1) if total_contacted > 0 else 0.0
    )

    return {
        "total_businesses": int(total_businesses),
        "total_campaigns": int(total_campaigns),
        "messages_sent": messages_sent,
        "response_rate": response_rate,
    }


def get_quota_usage(db: Session) -> dict[str, int]:
    """Return WhatsApp monthly quota usage: used, limit, remaining."""
    used = _count_sent_messages(db)
    return {
        "used": used,
        "limit": WHATSAPP_MONTHLY_LIMIT,
        "remaining": WHATSAPP_MONTHLY_LIMIT - used,
    }


def get_recent_businesses(db: Session, limit: int = 10) -> list[Business]:
    """Return the most recently added businesses."""
    stmt = select(Business).order_by(Business.created_at.desc()).limit(limit)
    return list(db.scalars(stmt).all())


def get_active_campaigns(db: Session) -> list[Campaign]:
    """Return all campaigns whose status is 'active'."""
    stmt = select(Campaign).where(Campaign.status == "active")
    return list(db.scalars(stmt).all())


def get_top_categories(db: Session, limit: int = 5) -> list[dict[str, int | str]]:
    """Return the top business categories by lead count."""
    stmt = (
        select(Business.category, func.count().label("count"))
        .group_by(Business.category)
        .order_by(func.count().desc())
        .limit(limit)
    )
    rows = db.execute(stmt).all()
    return [{"category": row[0], "count": int(row[1])} for row in rows]


def get_seo_distribution(db: Session) -> dict[str, int]:
    """Bucket businesses by SEO score range."""
    ranges = {
        "seo_low": (0, 25),
        "seo_medium": (26, 50),
        "seo_good": (51, 75),
        "seo_excellent": (76, 100),
    }
    result: dict[str, int] = {}
    for label, (low, high) in ranges.items():
        count = db.scalar(
            select(func.count())
            .select_from(Business)
            .where(Business.seo_score.is_not(None))
            .where(Business.seo_score >= low)
            .where(Business.seo_score <= high)
        )
        result[label] = int(count or 0)
    return result
