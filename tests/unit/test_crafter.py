"""Tests for Crafter service — AI pitch generation via GLM 5.2.

TDD: these tests are written BEFORE the implementation.
Each test describes one behavior of CrafterService.

All AI API calls are mocked — no real network requests in unit tests.
"""

from __future__ import annotations

import json
import re
from unittest.mock import MagicMock, patch

import httpx
import pytest

from nuhoot.models.business import Business
from nuhoot.models.pitch import Pitch
from nuhoot.services.crafter import CrafterError, CrafterService

# Arabic Unicode range for validating pitch language.
_ARABIC_RANGE = "\u0600-\u06ff"

# ------------------------------------------------------------------ #
# Mock AI response data (what GLM 5.2 would return)
# ------------------------------------------------------------------ #

_AI_PITCH = (
    "مرحباً مطعم النخيل،\n\n"
    "نحن وكالة تسويق رقمي متخصصة في السوق السعودي. "
    "لاحظنا أن لديكم تقييماً ممتازاً وسمعة طيبة، "
    "ولكن هناك فرص كبيرة لتحسين حضوركم الرقمي.\n\n"
    "نقدم خدمات إدارة وسائل التواصل الاجتماعي وتحسين محركات البحث. "
    "هل يمكننا تحديد موعد لمكالمة لمناقشة كيف يمكننا مساعدتكم؟"
)

_AI_SAMPLE_POSTS = [
    "اطلب من مطعم النخيل اليوم! أشهى الأطباق السعودية بانتظارك 🍽️ "
    "#مطعم_النخيل #الرياض #طعام_سعودي",
    "جودة استثنائية وطعم لا يُنسى في مطعم النخيل ✨ " "#مطعم #الرياض #مطاعم_الرياض",
    "زورونا اليوم واستمتعوا بأفضل الأطباق في مطعم النخيل 🌟 " "#طعام #سعودية #مطعم_النخيل",
]

_AI_RESPONSE_CONTENT = json.dumps(
    {"pitch": _AI_PITCH, "sample_posts": _AI_SAMPLE_POSTS},
    ensure_ascii=False,
)


def _mock_ai_response(content: str = _AI_RESPONSE_CONTENT) -> MagicMock:
    """Build a mock httpx.Response simulating a GLM 5.2 chat completion."""
    response = MagicMock(spec=httpx.Response)
    response.status_code = 200
    response.raise_for_status = MagicMock()
    response.json.return_value = {
        "choices": [{"message": {"content": content}}],
    }
    return response


def _mock_error_response(status_code: int = 500) -> MagicMock:
    """Build a mock httpx.Response whose raise_for_status() raises."""
    request = httpx.Request("POST", "https://api.code.umans.ai/v1/chat/completions")
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
    rating: float | None = 4.5,
    review_count: int | None = 120,
    has_website: bool = True,
    has_instagram: bool = True,
    seo_score: int | None = 85,
    social_score: int | None = 75,
) -> Business:
    """Create a Business object for testing."""
    return Business(
        name=name,
        category=category,
        rating=rating,
        review_count=review_count,
        has_website=has_website,
        has_instagram=has_instagram,
        seo_score=seo_score,
        social_score=social_score,
        website="https://example.com" if has_website else None,
        instagram="https://instagram.com/nakheel" if has_instagram else None,
    )


def _patch_ai_client(response: MagicMock | None = None, *, side_effect=None):
    """Patch httpx.Client in the crafter module with a pre-configured mock.

    Returns the (patch_context, mock_client) pair.
    """
    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    if side_effect is not None:
        mock_client.post.side_effect = side_effect
    else:
        mock_client.post.return_value = response
    return patch("nuhoot.services.crafter.httpx.Client", return_value=mock_client), mock_client


# ------------------------------------------------------------------ #
# Tests
# ------------------------------------------------------------------ #


class TestCrafterServiceExists:
    def test_crafter_service_exists(self):
        """CrafterService is importable and has a craft_pitch method."""
        assert hasattr(CrafterService, "craft_pitch")
        assert hasattr(CrafterService, "__init__")


class TestCrafterGeneratesPitch:
    def test_crafter_generates_pitch_for_business(self, db_session):
        """craft_pitch() returns a Pitch object with non-empty pitch_text."""
        biz = _make_business()
        db_session.add(biz)
        db_session.commit()
        service = CrafterService(db_session)
        patch_ctx, _ = _patch_ai_client(_mock_ai_response())
        with patch_ctx:
            pitch = service.craft_pitch(biz)
        assert pitch is not None
        assert isinstance(pitch, Pitch)
        assert pitch.pitch_text
        assert len(pitch.pitch_text) > 0


class TestCrafterPitchContainsBusinessName:
    def test_crafter_pitch_contains_business_name(self, db_session):
        """The generated pitch contains the business name."""
        biz = _make_business(name="مطعم النخيل")
        db_session.add(biz)
        db_session.commit()
        service = CrafterService(db_session)
        patch_ctx, _ = _patch_ai_client(_mock_ai_response())
        with patch_ctx:
            pitch = service.craft_pitch(biz)
        assert "مطعم النخيل" in pitch.pitch_text


class TestCrafterPitchContainsPdplOptOut:
    def test_crafter_pitch_contains_pdpl_opt_out(self, db_session):
        """The pitch includes PDPL opt-out text (لإلغاء or إيقاف)."""
        biz = _make_business()
        db_session.add(biz)
        db_session.commit()
        service = CrafterService(db_session)
        patch_ctx, _ = _patch_ai_client(_mock_ai_response())
        with patch_ctx:
            pitch = service.craft_pitch(biz)
        assert "لإلغاء" in pitch.pitch_text or "إيقاف" in pitch.pitch_text


class TestCrafterGeneratesSamplePosts:
    def test_crafter_generates_sample_posts(self, db_session):
        """craft_pitch() generates exactly 3 sample Instagram post captions."""
        biz = _make_business()
        db_session.add(biz)
        db_session.commit()
        service = CrafterService(db_session)
        patch_ctx, _ = _patch_ai_client(_mock_ai_response())
        with patch_ctx:
            pitch = service.craft_pitch(biz)
        assert pitch.sample_posts is not None
        assert len(pitch.sample_posts) == 3


class TestCrafterHandlesApiError:
    def test_crafter_handles_api_error(self, db_session):
        """craft_pitch() raises CrafterError when the AI API returns 500."""
        biz = _make_business()
        db_session.add(biz)
        db_session.commit()
        service = CrafterService(db_session)
        patch_ctx, _ = _patch_ai_client(_mock_error_response(500))
        with patch_ctx, pytest.raises(CrafterError):
            service.craft_pitch(biz)


class TestCrafterHandlesTimeout:
    def test_crafter_handles_timeout(self, db_session):
        """craft_pitch() raises CrafterError on request timeout."""
        biz = _make_business()
        db_session.add(biz)
        db_session.commit()
        service = CrafterService(db_session)
        patch_ctx, _ = _patch_ai_client(
            side_effect=httpx.TimeoutException("timed out"),
        )
        with patch_ctx, pytest.raises(CrafterError):
            service.craft_pitch(biz)


class TestCrafterStoresPitchInDatabase:
    def test_crafter_stores_pitch_in_database(self, db_session):
        """craft_pitch() persists the Pitch record in the database."""
        biz = _make_business()
        db_session.add(biz)
        db_session.commit()
        biz_id = biz.id
        service = CrafterService(db_session)
        patch_ctx, _ = _patch_ai_client(_mock_ai_response())
        with patch_ctx:
            pitch = service.craft_pitch(biz)
        pitch_id = pitch.id
        # Expire the session cache to force a DB read.
        db_session.expire_all()
        fetched = db_session.get(Pitch, pitch_id)
        assert fetched is not None
        assert fetched.business_id == biz_id
        assert fetched.pitch_text
        assert len(fetched.sample_posts) == 3


class TestCrafterPitchIsInArabic:
    def test_crafter_pitch_is_in_arabic(self, db_session):
        """The generated pitch text contains Arabic characters."""
        biz = _make_business()
        db_session.add(biz)
        db_session.commit()
        service = CrafterService(db_session)
        patch_ctx, _ = _patch_ai_client(_mock_ai_response())
        with patch_ctx:
            pitch = service.craft_pitch(biz)
        assert re.search(f"[{_ARABIC_RANGE}]", pitch.pitch_text) is not None
