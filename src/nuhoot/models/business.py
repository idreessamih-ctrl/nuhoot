"""Business/lead database model."""

from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from nuhoot.database import Base


class Business(Base):
    """A business found on Google Maps — a potential lead."""

    __tablename__ = "businesses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    category: Mapped[str] = mapped_column(String(200), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(50))
    whatsapp: Mapped[str | None] = mapped_column(String(50))
    address: Mapped[str | None] = mapped_column(Text)
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    website: Mapped[str | None] = mapped_column(Text)
    instagram: Mapped[str | None] = mapped_column(String(500))
    rating: Mapped[float | None] = mapped_column(Float)
    review_count: Mapped[int | None] = mapped_column(Integer, default=0)

    # Investigation results
    has_website: Mapped[bool] = mapped_column(default=False)
    has_instagram: Mapped[bool] = mapped_column(default=False)
    seo_score: Mapped[int | None] = mapped_column(Integer)
    social_score: Mapped[int | None] = mapped_column(Integer)

    # Status tracking
    status: Mapped[str] = mapped_column(String(50), default="found")
    # found → investigated → pitched → contacted → responded → converted

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
