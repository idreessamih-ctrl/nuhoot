"""Sender service — WhatsApp Cloud API integration.

Sends AI-generated pitches to businesses via the Meta WhatsApp Cloud API.
Tracks delivery status (pending → sent → delivered → read → failed), stores
a Message record for every send attempt, and updates the pitch status to
'sent' after a successful delivery.

Rate limiting: max 20 messages per 60-second window (conservative — WhatsApp
allows 80/sec, but this prevents flooding contacts and stays PDPL-friendly).
"""

from __future__ import annotations

import time
from datetime import datetime
from typing import Any

import httpx
import structlog
from sqlalchemy.orm import Session

from nuhoot.config import settings
from nuhoot.models.business import Business
from nuhoot.models.message import Message
from nuhoot.models.pitch import Pitch
from nuhoot.utils.phone import format_phone_for_whatsapp

logger = structlog.get_logger()

_DEFAULT_TIMEOUT = 30.0
_MAX_MESSAGES_PER_MINUTE = 20
_RATE_WINDOW_SECONDS = 60
_WHATSAPP_API_VERSION = "v18.0"


class SenderError(Exception):
    """Raised when the Sender service encounters an unrecoverable error."""


class SenderService:
    """Send AI-crafted pitches to businesses via WhatsApp Cloud API.

    Usage::

        service = SenderService(db_session)
        message = service.send_pitch(business, pitch)
    """

    def __init__(
        self,
        db: Session,
        *,
        timeout: float = _DEFAULT_TIMEOUT,
        max_per_minute: int = _MAX_MESSAGES_PER_MINUTE,
    ) -> None:
        self.db = db
        self.timeout = timeout
        self.max_per_minute = max_per_minute
        self._send_timestamps: list[float] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def send_pitch(self, business: Business, pitch: Pitch) -> Message:
        """Send *pitch* to *business* via WhatsApp and record the delivery.

        Args:
            business: The recipient business (must have a phone/whatsapp).
            pitch: The AI-generated pitch to send.

        Returns:
            The stored :class:`Message` with delivery status.

        Raises:
            SenderError: If the business has no phone, or the WhatsApp API
                call fails (timeout, HTTP error, rate-limit response).
        """
        logger.info(
            "sender.send.start",
            business_id=business.id,
            pitch_id=pitch.id,
            name=business.name,
        )

        self._wait_if_rate_limited()

        phone = self._resolve_phone(business)

        message = Message(
            pitch_id=pitch.id,
            business_id=business.id,
            phone_number=phone,
            status="pending",
        )
        self.db.add(message)
        self.db.flush()

        try:
            wamid = self._call_whatsapp_api(phone, pitch.pitch_text)
        except SenderError as exc:
            message.status = "failed"
            message.error_message = str(exc)
            self.db.commit()
            logger.warning(
                "sender.send.failed",
                business_id=business.id,
                error=str(exc),
            )
            raise

        message.whatsapp_message_id = wamid
        message.status = "sent"
        message.sent_at = datetime.now()
        pitch.status = "sent"
        self._send_timestamps.append(time.monotonic())
        self.db.commit()

        logger.info(
            "sender.send.done",
            message_id=message.id,
            business_id=business.id,
            wamid=wamid,
        )
        return message

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _resolve_phone(self, business: Business) -> str:
        """Pick the best phone number and format it for WhatsApp.

        Prefers the dedicated whatsapp field, falls back to the general
        phone field, then strips non-digits.

        Raises:
            SenderError: If the business has no phone number at all.
        """
        raw = business.whatsapp or business.phone
        if not raw:
            raise SenderError(
                f"Business {business.id} has no phone number to send to",
            )
        return format_phone_for_whatsapp(raw)

    def _call_whatsapp_api(self, phone: str, text: str) -> str:
        """POST a text message to the WhatsApp Cloud API and return the wamid.

        Raises:
            SenderError: On timeout, HTTP error, or unexpected response.
        """
        url = (
            f"https://graph.facebook.com/{_WHATSAPP_API_VERSION}/"
            f"{settings.whatsapp_phone_number_id}/messages"
        )
        headers = {
            "Authorization": f"Bearer {settings.whatsapp_access_token}",
            "Content-Type": "application/json",
        }
        body: dict[str, Any] = {
            "messaging_product": "whatsapp",
            "to": phone,
            "type": "text",
            "text": {"body": text},
        }

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=body, headers=headers)
                response.raise_for_status()
                data: Any = response.json()
        except httpx.TimeoutException as exc:
            raise SenderError(
                f"WhatsApp request timed out after {self.timeout}s",
            ) from exc
        except httpx.HTTPStatusError as exc:
            raise SenderError(
                f"WhatsApp API returned HTTP {exc.response.status_code}",
            ) from exc
        except httpx.HTTPError as exc:
            raise SenderError(f"WhatsApp request failed: {exc}") from exc

        try:
            return str(data["messages"][0]["id"])
        except (KeyError, IndexError, TypeError) as exc:
            raise SenderError(
                "WhatsApp response missing message id",
            ) from exc

    def _wait_if_rate_limited(self) -> None:
        """Sleep if the send window is at capacity.

        Tracks recent send timestamps and, when ``max_per_minute`` messages
        have been sent in the last ``_RATE_WINDOW_SECONDS``, sleeps until the
        oldest one leaves the window.
        """
        now = time.monotonic()
        self._send_timestamps = [t for t in self._send_timestamps if now - t < _RATE_WINDOW_SECONDS]
        if len(self._send_timestamps) >= self.max_per_minute:
            oldest = self._send_timestamps[0]
            sleep_seconds = _RATE_WINDOW_SECONDS - (now - oldest)
            if sleep_seconds > 0:
                logger.info(
                    "sender.rate_limited",
                    sleep_seconds=round(sleep_seconds, 2),
                    window_size=len(self._send_timestamps),
                )
                time.sleep(sleep_seconds)
