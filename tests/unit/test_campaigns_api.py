"""Tests for campaigns API routes — batch WhatsApp sending."""

from unittest.mock import patch

from nuhoot.models.business import Business
from nuhoot.models.campaign import Campaign
from nuhoot.models.message import Message
from nuhoot.models.pitch import Pitch
from nuhoot.services.sender import SenderService

_PITCH_TEXT = "مرحباً مطعم النخيل، هل يمكننا مكالمة؟ لإلغاء الاشتراك، أرسل إيقاف"


def _make_campaign(db_session, name: str = "Riyadh Restaurants") -> Campaign:
    campaign = Campaign(name=name, niche="restaurants", city="Riyadh")
    db_session.add(campaign)
    db_session.commit()
    return campaign


def _make_business_with_pitch(db_session, campaign: Campaign, name: str = "مطعم") -> Business:
    biz = Business(
        name=name,
        category="restaurants",
        phone="+966 50 123 4567",
        campaign_id=campaign.id,
    )
    db_session.add(biz)
    db_session.commit()
    pitch = Pitch(
        business_id=biz.id,
        pitch_text=_PITCH_TEXT,
        sample_posts=["منشور 1", "منشور 2", "منشور 3"],
        language="ar",
        status="approved",
    )
    db_session.add(pitch)
    db_session.commit()
    return biz


def _make_sent_message(business: Business, pitch: Pitch) -> Message:
    message = Message(
        pitch_id=pitch.id,
        business_id=business.id,
        phone_number="966501234567",
        whatsapp_message_id="wamid.BATCH",
        status="sent",
    )
    message.id = 1
    return message


class TestSendCampaignPitches:
    def test_send_campaign_sends_to_all_businesses(self, client, db_session):
        """POST /campaigns/{id}/send sends to every business in the campaign."""
        campaign = _make_campaign(db_session)
        biz1 = _make_business_with_pitch(db_session, campaign, "مطعم النخيل")
        _make_business_with_pitch(db_session, campaign, "مطعم الورد")

        mock_message = _make_sent_message(biz1, db_session.get(Pitch, 1))  # noqa
        with patch.object(SenderService, "send_pitch", return_value=mock_message) as mock_send:
            response = client.post(f"/campaigns/{campaign.id}/send")

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["data"]["sent"] == 2
        assert body["data"]["failed"] == 0
        assert body["data"]["total"] == 2
        assert mock_send.call_count == 2

    def test_send_campaign_returns_404_for_nonexistent(self, client):
        """POST /campaigns/{id}/send returns 404 for unknown campaign."""
        response = client.post("/campaigns/99999/send")
        assert response.status_code == 404
        body = response.json()
        assert body["success"] is False

    def test_send_campaign_counts_failed_sends(self, client, db_session):
        """POST /campaigns/{id}/send counts businesses without pitches as failed."""
        campaign = _make_campaign(db_session)
        _make_business_with_pitch(db_session, campaign, "مطعم النخيل")
        # Second business with no pitch → should be counted as failed.
        biz_no_pitch = Business(
            name="متجر بلا عرض",
            category="restaurants",
            phone="+966 55 555 5555",
            campaign_id=campaign.id,
        )
        db_session.add(biz_no_pitch)
        db_session.commit()

        mock_message = _make_sent_message(biz_no_pitch, db_session.get(Pitch, 1))  # noqa
        with patch.object(SenderService, "send_pitch", return_value=mock_message):
            response = client.post(f"/campaigns/{campaign.id}/send")

        assert response.status_code == 200
        body = response.json()
        assert body["data"]["sent"] == 1
        assert body["data"]["failed"] == 1
        assert body["data"]["total"] == 2
