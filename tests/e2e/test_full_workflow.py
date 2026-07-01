"""End-to-end workflow test: finder → investigator → crafter → render → sender.

Mocks external APIs (GLM 5.2, WhatsApp Cloud, gosom scraper, HTTP) but
runs the REAL Satori renderer (node render.mjs) to produce actual PNG images.

This verifies the full pipeline works end-to-end, including image generation.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from nuhoot.models.business import Business
from nuhoot.models.pitch import Pitch
from nuhoot.services.crafter import CrafterService
from nuhoot.services.investigator import InvestigatorService
from nuhoot.services.renderer import RendererService
from nuhoot.services.sender import SenderService


# ── Mock data ─────────────────────────────────────────────────────────────────

_MOCK_AI_RESPONSE = json.dumps({
    "pitch": (
        "مرحباً مطعم النخيل الذهبي،\n\n"
        "نحن وكالة تسويق رقمي متخصصة في السوق السعودي. "
        "لاحظنا أن لديكم تقييماً ممتازاً وسمعة طيبة، "
        "ولكن هناك فرص كبيرة لتحسين حضوركم الرقمي.\n\n"
        "هل يمكننا تحديد موعد لمكالمة لمناقشة كيف يمكننا مساعدتكم؟"
    ),
    "sample_posts": [
        "اكتشف نكهات المطبخ السعودي الأصيل مع أطباق شهية لا تُنسى #مطعم_النخيل #الرياض #طعام_سعودي",
        "تجربة طعام فاخرة في قلب المدينة مع أجود المكونات الطازجة #مطعم #ذواقة #تجربة_فريدة",
        "احجز طاولتك الآن واستمتع بأشهى الأطباق السعودية التقليدية #حجز #مطعم_النخيل #أكل",
    ],
}, ensure_ascii=False)

_MOCK_INVESTIGATE_HTML = """
<html>
<head><title>مطعم النخيل الذهبي - الرياض</title></head>
<body>
<h1>مطعم النخيل الذهبي</h1>
<p>أفضل مطعم سعودي في الرياض</p>
<a href="https://instagram.com/nakheel">Instagram</a>
</body>
</html>
"""

_MOCK_WHATSAPP_RESPONSE = {
    "messaging_product": "whatsapp",
    "contacts": [{"input": "966501234567", "wa_id": "966501234567"}],
    "messages": [{"id": "wamid.test123"}],
}


# ── E2E Test ──────────────────────────────────────────────────────────────────


class TestFullWorkflow:
    """Full pipeline: find → investigate → craft → render → send.

    External APIs mocked. Satori renderer runs for real.
    """

    def test_full_pipeline_produces_pitch_with_images_and_sends(
        self, db_session
    ):
        """The complete Nuhoot pipeline from business discovery to WhatsApp send.

        Steps:
        1. Create a business (simulating finder output)
        2. Investigate digital presence (mocked HTTP)
        3. Craft AI pitch (mocked GLM 5.2)
        4. Render branded images (REAL Satori)
        5. Send via WhatsApp (mocked Cloud API)
        """
        # ── Step 1: Finder output — business discovered ───────────────────
        business = Business(
            name="مطعم النخيل الذهبي",
            category="restaurants",
            phone="+966501234567",
            whatsapp="966501234567",
            address="الرياض، حي العليا",
            rating=4.5,
            review_count=320,
            website="https://example.com",
            status="found",
        )
        db_session.add(business)
        db_session.commit()
        assert business.id is not None
        assert business.status == "found"

        # ── Step 2: Investigator — analyze digital presence ────────────────
        with patch("nuhoot.services.investigator.httpx.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_response = MagicMock()
            mock_response.text = _MOCK_INVESTIGATE_HTML
            mock_response.status_code = 200
            mock_response.raise_for_status = MagicMock()
            mock_client.get.return_value = mock_response
            mock_client_cls.return_value = mock_client

            investigator = InvestigatorService(db_session)
            investigator.investigate(business)
            db_session.commit()

        assert business.status == "investigated"
        assert business.has_website is True
        assert business.seo_score is not None
        assert business.social_score is not None

        # ── Step 3: Crafter — generate AI pitch ───────────────────────────
        with patch.object(CrafterService, "_call_ai", return_value=_MOCK_AI_RESPONSE):
            crafter = CrafterService(db_session)
            pitch = crafter.craft_pitch(business)

        assert pitch.id is not None
        assert pitch.pitch_text is not None
        assert len(pitch.sample_posts) == 3
        assert "مرحباً" in pitch.pitch_text or "مرحبا" in pitch.pitch_text

        # ── Step 4: Renderer — generate branded images (REAL Satori) ──────
        # Uses a real business photo from /tmp/nuhoot-pro/
        photo = "/tmp/nuhoot-pro/enhanced_photo_3.jpg"
        renderer = RendererService()
        image_posts = renderer.render_posts(pitch, business, photo_path=photo)

        assert len(image_posts) == 3
        from PIL import Image as PILImage
        for i, img_post in enumerate(image_posts):
            assert "caption" in img_post
            assert "image_path" in img_post
            assert Path(img_post["image_path"]).exists()
            assert Path(img_post["image_path"]).stat().st_size > 10000  # real PNG

            # Verify the image has real visual content (not a blank rectangle)
            img = PILImage.open(img_post["image_path"])
            # Sample pixels in different regions — they should differ
            tl = img.getpixel((100, 100))
            br = img.getpixel((980, 980))
            assert tl != br, f"Post {i}: top-left and bottom-right are identical — no photo content"

        # ── Step 5: Sender — send pitch via WhatsApp ───────────────────────
        with patch.object(SenderService, "_call_whatsapp_api", return_value="wamid.test123"):
            sender = SenderService(db_session)
            message = sender.send_pitch(business, pitch)

        assert message.id is not None
        assert message.status == "sent"
        assert message.whatsapp_message_id == "wamid.test123"

        # ── Verify final state ────────────────────────────────────────────
        db_session.refresh(pitch)
        assert pitch.status == "sent"  # pitch marked as sent
        assert message.status == "sent"
        # Note: business.status stays "investigated" — sender doesn't update it yet
