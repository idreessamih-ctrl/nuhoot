"""Tests for Saudi phone number formatting."""

import pytest

from nuhoot.utils.phone import (
    format_phone_for_whatsapp,
    is_whatsapp_capable,
    normalize_saudi_phone,
)


class TestNormalizeSaudiPhone:
    def test_strips_leading_zero(self):
        result = normalize_saudi_phone("0501234567")
        assert result == "+966 50 123 4567"

    def test_strips_country_code(self):
        result = normalize_saudi_phone("966501234567")
        assert result == "+966 50 123 4567"

    def test_strips_plus_and_country_code(self):
        result = normalize_saudi_phone("+966501234567")
        assert result == "+966 50 123 4567"

    def test_handles_bare_number(self):
        result = normalize_saudi_phone("501234567")
        assert result == "+966 50 123 4567"

    def test_raises_on_invalid_number(self):
        with pytest.raises(ValueError):
            normalize_saudi_phone("12345")

    def test_raises_on_non_saudi_number(self):
        with pytest.raises(ValueError):
            normalize_saudi_phone("447911123456")


class TestIsWhatsappCapable:
    def test_valid_saudi_number(self):
        assert is_whatsapp_capable("0501234567") is True

    def test_invalid_number(self):
        assert is_whatsapp_capable("12345") is False


class TestFormatPhoneForWhatsapp:
    def test_strips_plus_and_spaces(self):
        assert format_phone_for_whatsapp("+966 50 123 4567") == "966501234567"

    def test_strips_dashes(self):
        assert format_phone_for_whatsapp("+966-50-123-4567") == "966501234567"

    def test_strips_parentheses(self):
        assert format_phone_for_whatsapp("(966) 501234567") == "966501234567"

    def test_already_digits_unchanged(self):
        assert format_phone_for_whatsapp("966501234567") == "966501234567"
