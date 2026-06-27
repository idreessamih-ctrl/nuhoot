"""Tests for WhatsApp sender API routes (business-scoped)."""

from unittest.mock import patch

from nuhoot.models.business import Business
from nuhoot.models.message import Message
from nuhoot.models.pitch import Pitch
from nuhoot.services.sender import SenderError, SenderService

_PITCH_TEXT = "مرحباً مطعم النخيل، هل يمكننا مكالمة؟ لإلغاء الاشتراك، أرسل إيقاف"


def _make_business(db_session, *, phone: str = "+966 50 123 4567") -> Business:
    biz = Business(name="مطعم النخيل", category="restaurants", phone=phone)
    db_session.add(biz)
    db_session.commit()
    return biz


def _make_pitch(db_session, business: Business) -> Pitch:
    pitch = Pitch(
        business_id=business.id,
        pitch_text=_PITCH_TEXT,
        sample_posts=["منشور 1", "منشور 2", "منشور 3"],
        language="ar",
        status="approved",
    )
    db_session.add(pitch)
    db_session.commit()
    return pitch


def _make_message(business: Business, pitch: Pitch, message_id: int = 1) -> Message:
    """Create a Message object for testing (with a synthetic id)."""
    message = Message(
        pitch_id=pitch.id,
        business_id=business.id,
        phone_number="966501234567",
        whatsapp_message_id="wamid.TEST123",
        status="sent",
        error_message=None,
    )
    message.id = message_id
    return message


class TestSendBusinessPitch:
    def test_send_returns_message(self, client, db_session):
        """POST /businesses/{id}/send sends the pitch and returns the message."""
        biz = _make_business(db_session)
        pitch = _make_pitch(db_session, biz)
        mock_message = _make_message(biz, pitch)
        with patch.object(SenderService, "send_pitch", return_value=mock_message):
            response = client.post(f"/businesses/{biz.id}/send")
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["data"]["phone_number"] == "966501234567"
        assert body["data"]["whatsapp_message_id"] == "wamid.TEST123"
        assert body["data"]["status"] == "sent"

    def test_send_returns_404_for_nonexistent_business(self, client):
        """POST /businesses/{id}/send returns 404 for unknown ID."""
        response = client.post("/businesses/99999/send")
        assert response.status_code == 404
        body = response.json()
        assert body["success"] is False

    def test_send_returns_404_when_no_pitch(self, client, db_session):
        """POST /businesses/{id}/send returns 404 when no pitch exists."""
        biz = _make_business(db_session)
        response = client.post(f"/businesses/{biz.id}/send")
        assert response.status_code == 404
        body = response.json()
        assert body["success"] is False
        assert "No pitch" in body["error"]

    def test_send_returns_500_on_sender_error(self, client, db_session):
        """POST /businesses/{id}/send returns 500 when WhatsApp fails."""
        biz = _make_business(db_session)
        _make_pitch(db_session, biz)
        with patch.object(
            SenderService,
            "send_pitch",
            side_effect=SenderError("WhatsApp API returned HTTP 429"),
        ):
            response = client.post(f"/businesses/{biz.id}/send")
        assert response.status_code == 500
        body = response.json()
        assert body["success"] is False


class TestListBusinessMessages:
    def test_list_returns_messages(self, client, db_session):
        """GET /businesses/{id}/messages returns sent messages."""
        biz = _make_business(db_session)
        pitch = _make_pitch(db_session, biz)
        msg = Message(
            pitch_id=pitch.id,
            business_id=biz.id,
            phone_number="966501234567",
            whatsapp_message_id="wamid.ABC",
            status="sent",
        )
        db_session.add(msg)
        db_session.commit()
        response = client.get(f"/businesses/{biz.id}/messages")
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["data"]["total"] == 1
        assert body["data"]["items"][0]["whatsapp_message_id"] == "wamid.ABC"

    def test_list_returns_empty_when_no_messages(self, client, db_session):
        """GET /businesses/{id}/messages returns empty list when none sent."""
        biz = _make_business(db_session)
        response = client.get(f"/businesses/{biz.id}/messages")
        assert response.status_code == 200
        body = response.json()
        assert body["data"]["items"] == []
        assert body["data"]["total"] == 0

    def test_list_returns_404_for_nonexistent_business(self, client):
        """GET /businesses/{id}/messages returns 404 for unknown ID."""
        response = client.get("/businesses/99999/messages")
        assert response.status_code == 404
        body = response.json()
        assert body["success"] is False
