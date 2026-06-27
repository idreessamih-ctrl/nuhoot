"""Message database model — WhatsApp message delivery tracking."""

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from nuhoot.database import Base


class Message(Base):
    """A WhatsApp message sent to a business via the Meta Cloud API.

    Tracks the delivery lifecycle:
    pending → sent → delivered → read → failed

    Each message links a pitch to a business and records the WhatsApp
    message ID returned by Meta for webhook-based status updates.
    """

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pitch_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("pitches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    business_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    phone_number: Mapped[str] = mapped_column(String(50), nullable=False)
    whatsapp_message_id: Mapped[str | None] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(50), insert_default="pending")
    # pending → sent → delivered → read → failed
    error_message: Mapped[str | None] = mapped_column(Text)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime)
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("status", "pending")
        super().__init__(**kwargs)
