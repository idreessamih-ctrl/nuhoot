"""Settings model — stores encrypted API credentials."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from nuhoot.database import Base


class AppSetting(Base):
    """Key-value store for app settings and encrypted API credentials."""

    __tablename__ = "app_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    value: Mapped[str] = mapped_column(Text, nullable=False, default="")
    is_secret: Mapped[bool] = mapped_column(Integer, default=0)  # 0=no, 1=yes
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # Known setting keys
    KEYS = {
        "umans_api_key": {"label": "umans.ai API Key", "secret": True},
        "google_maps_api_key": {"label": "Google Maps API Key", "secret": True},
        "meta_app_id": {"label": "Meta App ID", "secret": False},
        "meta_app_secret": {"label": "Meta App Secret", "secret": True},
        "whatsapp_phone_number_id": {"label": "WhatsApp Phone Number ID", "secret": False},
        "whatsapp_access_token": {"label": "WhatsApp Access Token", "secret": True},
        "whatsapp_business_id": {"label": "WhatsApp Business ID", "secret": False},
    }

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
