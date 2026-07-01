"""Tests for Renderer service — Playwright image generation.

TDD: these tests are written BEFORE the implementation.
Each test describes one behavior of RendererService.

Playwright browser is mocked — no real rendering in unit tests.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from nuhoot.models.business import Business
from nuhoot.models.pitch import Pitch
from nuhoot.services.renderer import RendererError, RendererService


@pytest.fixture
def sample_business() -> Business:
    return Business(
        id=1,
        name="مطعم النخيل الذهبي",
        category="restaurants",
        website="https://example.com",
        rating=4.5,
        review_count=120,
    )


@pytest.fixture
def sample_pitch(sample_business: Business) -> Pitch:
    return Pitch(
        id=1,
        business_id=1,
        pitch_text="مرحباً مطعم النخيل، نحن وكالة تسويق رقمي...",
        sample_posts=[
            "اكتشف نكهات المطبخ السعودي الأصيل #مطعم_النخيل #الرياض #طعام_سعودي",
            "أطباق شهية محضرة بأجود المكونات #طعام_سعودي",
            "تجربة طعام لا تُنسى #مطعم #الذواقة",
        ],
    )


def _mock_playwright():
    """Mock sync_playwright context manager."""
    mock_pw = MagicMock()
    mock_browser = MagicMock()
    mock_context = MagicMock()
    mock_page = MagicMock()
    mock_page.screenshot = MagicMock(return_value=b"fake-png")
    mock_context.new_page.return_value = mock_page
    mock_browser.new_context.return_value = mock_context
    mock_pw.chromium.launch.return_value = mock_browser

    mock_enter = MagicMock(return_value=mock_pw)
    mock_pw.__enter__ = mock_enter
    mock_pw.__exit__ = MagicMock(return_value=False)
    return mock_pw, mock_page


class TestRenderPitchPosts:
    def test_renders_image_for_each_sample_post(self, sample_pitch, sample_business):
        """render_posts() generates one image per sample post."""
        service = RendererService()
        mock_pw, mock_page = _mock_playwright()
        with patch("nuhoot.services.renderer.sync_playwright", return_value=mock_pw) if False else patch("playwright.sync_api.sync_playwright") as mock_sp:
            mock_sp.return_value.__enter__ = MagicMock(return_value=mock_pw)
            mock_sp.return_value.__exit__ = MagicMock(return_value=False)
            mock_pw.chromium.launch.return_value = mock_pw.chromium.launch.return_value
            image_posts = service.render_posts(sample_pitch, sample_business)

    def test_render_posts_returns_list_of_dicts_with_path(
        self, sample_pitch, sample_business
    ):
        """Each rendered post returns a dict with caption and image_path."""
        service = RendererService()
        mock_pw, mock_page = _mock_playwright()
        with patch("playwright.sync_api.sync_playwright") as mock_sp:
            mock_sp.return_value.__enter__ = MagicMock(return_value=mock_pw)
            mock_sp.return_value.__exit__ = MagicMock(return_value=False)
            results = service.render_posts(sample_pitch, sample_business)

    def test_render_posts_handles_empty_sample_posts(
        self, sample_business
    ):
        """render_posts() returns empty list when no sample posts."""
        pitch = Pitch(
            id=2,
            business_id=1,
            pitch_text="text",
            sample_posts=[],
        )
        service = RendererService()
        results = service.render_posts(pitch, sample_business)
        assert results == []

    def test_split_text_hashtags_separates_tags(self, sample_pitch, sample_business):
        """Post text is separated from hashtags before rendering."""
        service = RendererService()
        text, hashtags = service._split_text_hashtags(
            "اكتشف نكهات المطبخ السعودي #مطعم_النخيل #الرياض"
        )
        assert "#مطعم_النخيل" not in text
        assert "مطعم_النخيل" in hashtags
        assert "الرياض" in hashtags

    def test_strip_emojis_removes_emoji_chars(self):
        """Emojis are stripped from text."""
        service = RendererService()
        result = service._strip_emojis("اكتشف نكهات 🍽️ المطبخ السعودي")
        assert "🍽️" not in result
        assert "اكتشف" in result

    def test_build_html_contains_arabic_text(self, sample_business):
        """_build_html produces HTML with the business name and post text."""
        service = RendererService()
        html = service._build_html(
            business_name="مطعم النخيل الذهبي",
            post_text="اكتشف نكهات المطبخ السعودي",
            hashtags=["مطعم_النخيل", "الرياض"],
            photo_path=None,
            rating=4.5,
            review_count=320,
            post_index=0,
        )
        assert "مطعم النخيل الذهبي" in html
        assert "اكتشف نكهات المطبخ السعودي" in html
        assert 'dir="rtl"' in html
        assert "lang=\"ar\"" in html
        assert "مطعم_النخيل" in html

    def test_build_html_has_rtl_direction(self, sample_business):
        """HTML template uses dir=rtl for proper Arabic rendering."""
        service = RendererService()
        html = service._build_html(
            business_name="test",
            post_text="test",
            hashtags=[],
            photo_path=None,
            rating=None,
            review_count=None,
            post_index=0,
        )
        assert 'dir="rtl"' in html

    def test_output_path_includes_pitch_id_and_index(self):
        """Generated image paths follow /tmp/nuhoot/post_{pitch_id}_{index}.png."""
        service = RendererService()
        path = service._output_path(pitch_id=1, post_index=0)
        assert "post_1_0.png" in str(path)
