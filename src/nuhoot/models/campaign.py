"""Campaign database model."""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from nuhoot.database import Base


class Campaign(Base):
    """A lead generation campaign targeting a specific niche and area."""

    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    niche: Mapped[str] = mapped_column(String(200), nullable=False)
    # e.g., "restaurants", "clinics", "salons", "real_estate"
    city: Mapped[str] = mapped_column(String(100), default="Riyadh")
    language: Mapped[str] = mapped_column(String(10), default="ar")

    # Pitch template
    pitch_template: Mapped[str | None] = mapped_column(Text)

    # Stats
    total_leads: Mapped[int] = mapped_column(Integer, insert_default=0)
    contacted: Mapped[int] = mapped_column(Integer, insert_default=0)
    responded: Mapped[int] = mapped_column(Integer, insert_default=0)
    converted: Mapped[int] = mapped_column(Integer, insert_default=0)

    status: Mapped[str] = mapped_column(String(50), insert_default="draft")
    # draft → active → paused → completed

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    def __init__(self, **kwargs):
        kwargs.setdefault("total_leads", 0)
        kwargs.setdefault("contacted", 0)
        kwargs.setdefault("responded", 0)
        kwargs.setdefault("converted", 0)
        kwargs.setdefault("status", "draft")
        kwargs.setdefault("language", "ar")
        kwargs.setdefault("city", "Riyadh")
        super().__init__(**kwargs)
