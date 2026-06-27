"""Tests for Business model."""

from nuhoot.models.business import Business


class TestBusinessModel:
    def test_create_business_with_required_fields(self):
        b = Business(name="مطعم الشرق", category="restaurants")
        assert b.name == "مطعم الشرق"
        assert b.category == "restaurants"

    def test_default_status_is_found(self):
        b = Business(name="Test", category="restaurants")
        assert b.status == "found"

    def test_default_has_website_is_false(self):
        b = Business(name="Test", category="restaurants")
        assert b.has_website is False

    def test_default_has_instagram_is_false(self):
        b = Business(name="Test", category="restaurants")
        assert b.has_instagram is False
