"""Tests for application config."""

from nuhoot.config import Settings


class TestSettings:
    def test_default_database_url(self):
        s = Settings()
        assert "postgresql" in s.database_url

    def test_default_timezone_is_riyadh(self):
        s = Settings()
        assert s.app_timezone == "Asia/Riyadh"

    def test_default_language_is_arabic(self):
        s = Settings()
        assert s.app_language == "ar"

    def test_default_ai_model_is_glm(self):
        s = Settings()
        assert s.ai_model == "umans-glm-5.2"
