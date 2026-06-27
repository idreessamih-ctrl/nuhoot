"""Tests for Sender service — WhatsApp Cloud API integration.

TDD: these tests are written BEFORE the implementation.
Each test describes one behavior of SenderService.

All WhatsApp API calls are mocked — no real messages are sent.
"""

from __future__ import annotations

import time
from unittest.mock import MagicMock, patch

import httpx
import pytest

from nuhoot.models.business import Business
from nuhoot.models.message import Message
from nuhoot.models.pitch import Pitch

# ------------------------------------------------------------------ #
# Mock WhatsApp API response data (what Meta Cloud API returns)
# ------------------------------------------------------------------ #

_WAMID = "wamid.HBgMOTE2NjUwMTIzNDU2Nw=="

_PITCH_TEXT = (
    "مرحباً مطعم النخيل،\n\n"
    "نحن وكالة تسويق رقمي متخصصة في السوق السعودي. "
    "هل يمكننا تحديد موعد لمكالمة؟\n\n"
    "لإلغاء الاشتراك، أرسل إيقاف"
)
_SAMPLE_POSTS = ["منشور أول #مطعم", "منشور ثانٍ #رياض", "منشور ثالث #سعودية"]


def _mock_whatsapp_success(message_id: str = _WAMID) -> MagicMock:
    """Build a mock httpx.Response simulating a successful WhatsApp send."""
    response = MagicMock(spec=httpx.Response)
    response.status_code = 200
    response.raise_for_status = MagicMock()
    response.json.return_value = {
        "messaging_product": "whatsapp",
        "contacts": [{"input": "966501234567", "wa_id": "966501234567"}],
        "messages": [{"id": message_id}],
    }
    return response


def _mock_error_response(status_code: int = 429) -> MagicMock:
    """Build a mock httpx.Response whose raise_for_status() raises."""
    request = httpx.Request("POST", "https://graph.facebook.com/v18.0/123456/messages")
    raw = httpx.Response(status_code=status_code, request=request)
    error = httpx.HTTPStatusError(
        f"Server returned {status_code}",
        request=request,
        response=raw,
    )
    response = MagicMock(spec=httpx.Response)
    response.status_code = status_code
    response.raise_for_status.side_effect = error
    return response


def _make_business(
    *,
    name: str = "مطعم النخيل",
    category: str = "restaurants",
    phone: str | None = "+966 50 123 4567",
    whatsapp: str | None = None,
) -> Business:
    """Create a Business object for testing."""
    return Business(
        name=name,
        category=category,
        phone=phone,
        whatsapp=whatsapp,
    )


def _make_pitch(business: Business, pitch_id: int | None = None) -> Pitch:
    """Create a Pitch object for testing."""
    pitch = Pitch(
        business_id=business.id,
        pitch_text=_PITCH_TEXT,
        sample_posts=list(_SAMPLE_POSTS),
        language="ar",
        status="approved",
    )
    if pitch_id is not None:
        pitch.id = pitch_id
    return pitch


def _patch_whatsapp_client(response: MagicMock | None = None, *, side_effect=None):
    """Patch httpx.Client in the sender module with a pre-configured mock.

    Returns the (patch_context, mock_client) pair.
    """
    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    if side_effect is not None:
        mock_client.post.side_effect = side_effect
    else:
        mock_client.post.return_value = response
    return (
        patch("nuhoot.services.sender.httpx.Client", return_value=mock_client),
        mock_client,
    )


def _setup_business_and_pitch(db_session) -> tuple[Business, Pitch]:
    """Persist a business + approved pitch and return them."""
    biz = _make_business()
    db_session.add(biz)
    db_session.commit()
    pitch = _make_pitch(biz)
    db_session.add(pitch)
    db_session.commit()
    return biz, pitch


# ------------------------------------------------------------------ #
# Tests
# ------------------------------------------------------------------ #


class TestSenderServiceExists:
    def test_sender_service_exists(self):
        """SenderService is importable and has a send_pitch method."""
        from nuhoot.services.sender import SenderService

        assert hasattr(SenderService, "send_pitch")
        assert hasattr(SenderService, "__init__")


class TestSenderSendsTextMessage:
    def test_sender_sends_text_message(self, db_session):
        """send_pitch() POSTs the correct WhatsApp text payload."""
        from nuhoot.services.sender import SenderService

        biz, pitch = _setup_business_and_pitch(db_session)
        service = SenderService(db_session)
        patch_ctx, mock_client = _patch_whatsapp_client(_mock_whatsapp_success())
        with patch_ctx:
            service.send_pitch(biz, pitch)

        mock_client.post.assert_called_once()
        call_kwargs = mock_client.post.call_args.kwargs
        body = call_kwargs["json"]
        assert body["messaging_product"] == "whatsapp"
        assert body["type"] == "text"
        assert body["text"]["body"] == _PITCH_TEXT


class TestSenderFormatsPhoneCorrectly:
    def test_sender_formats_phone_correctly(self, db_session):
        """Phone is stripped to pure digits (966501234567) in payload and DB."""
        from nuhoot.services.sender import SenderService

        biz, pitch = _setup_business_and_pitch(db_session)
        service = SenderService(db_session)
        patch_ctx, mock_client = _patch_whatsapp_client(_mock_whatsapp_success())
        with patch_ctx:
            message = service.send_pitch(biz, pitch)

        body = mock_client.post.call_args.kwargs["json"]
        assert body["to"] == "966501234567"
        assert message.phone_number == "966501234567"


class TestSenderHandlesApiSuccess:
    def test_sender_handles_api_success(self, db_session):
        """On success, send_pitch() returns a Message with the WhatsApp ID."""
        from nuhoot.services.sender import SenderService

        biz, pitch = _setup_business_and_pitch(db_session)
        service = SenderService(db_session)
        patch_ctx, _ = _patch_whatsapp_client(_mock_whatsapp_success())
        with patch_ctx:
            message = service.send_pitch(biz, pitch)

        assert isinstance(message, Message)
        assert message.whatsapp_message_id == _WAMID
        assert message.status == "sent"


class TestSenderHandlesApiError429:
    def test_sender_handles_api_error_429(self, db_session):
        """A 429 rate-limit response raises SenderError and marks failed."""
        from nuhoot.services.sender import SenderError, SenderService

        biz, pitch = _setup_business_and_pitch(db_session)
        service = SenderService(db_session)
        patch_ctx, _ = _patch_whatsapp_client(_mock_error_response(429))
        with patch_ctx, pytest.raises(SenderError):
            service.send_pitch(biz, pitch)

        stored = db_session.query(Message).filter_by(business_id=biz.id).first()
        assert stored is not None
        assert stored.status == "failed"


class TestSenderHandlesApiError401:
    def test_sender_handles_api_error_401(self, db_session):
        """A 401 bad-token response raises SenderError."""
        from nuhoot.services.sender import SenderError, SenderService

        biz, pitch = _setup_business_and_pitch(db_session)
        service = SenderService(db_session)
        patch_ctx, _ = _patch_whatsapp_client(_mock_error_response(401))
        with patch_ctx, pytest.raises(SenderError):
            service.send_pitch(biz, pitch)


class TestSenderHandlesTimeout:
    def test_sender_handles_timeout(self, db_session):
        """A request timeout raises SenderError."""
        from nuhoot.services.sender import SenderError, SenderService

        biz, pitch = _setup_business_and_pitch(db_session)
        service = SenderService(db_session)
        patch_ctx, _ = _patch_whatsapp_client(
            side_effect=httpx.TimeoutException("timed out"),
        )
        with patch_ctx, pytest.raises(SenderError):
            service.send_pitch(biz, pitch)


class TestSenderStoresMessageInDatabase:
    def test_sender_stores_message_in_database(self, db_session):
        """send_pitch() persists the Message record in the database."""
        from nuhoot.services.sender import SenderService

        biz, pitch = _setup_business_and_pitch(db_session)
        service = SenderService(db_session)
        patch_ctx, _ = _patch_whatsapp_client(_mock_whatsapp_success())
        with patch_ctx:
            message = service.send_pitch(biz, pitch)

        message_id = message.id
        db_session.expire_all()
        fetched = db_session.get(Message, message_id)
        assert fetched is not None
        assert fetched.business_id == biz.id
        assert fetched.pitch_id == pitch.id
        assert fetched.whatsapp_message_id == _WAMID
        assert fetched.status == "sent"


class TestSenderUpdatesPitchStatusAfterSend:
    def test_sender_updates_pitch_status_after_send(self, db_session):
        """After a successful send, the pitch status becomes 'sent'."""
        from nuhoot.services.sender import SenderService

        biz, pitch = _setup_business_and_pitch(db_session)
        service = SenderService(db_session)
        patch_ctx, _ = _patch_whatsapp_client(_mock_whatsapp_success())
        with patch_ctx:
            service.send_pitch(biz, pitch)

        db_session.refresh(pitch)
        assert pitch.status == "sent"


class TestSenderRateLimits:
    def test_sender_rate_limits(self, db_session):
        """When the message window is full, the sender waits before sending."""
        from nuhoot.services.sender import SenderService

        biz, pitch = _setup_business_and_pitch(db_session)
        # Use a tiny limit so we can fill the window easily.
        service = SenderService(db_session, max_per_minute=2)
        # Pre-fill the rate-limit window to capacity.
        now = time.monotonic()
        service._send_timestamps = [now, now]

        patch_ctx, mock_client = _patch_whatsapp_client(_mock_whatsapp_success())
        with patch_ctx, patch("nuhoot.services.sender.time.sleep") as mock_sleep:
            service.send_pitch(biz, pitch)

        mock_sleep.assert_called_once()
        sleep_seconds = mock_sleep.call_args.args[0]
        assert sleep_seconds > 0
        mock_client.post.assert_called_once()
