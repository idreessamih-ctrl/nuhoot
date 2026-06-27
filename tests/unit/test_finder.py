"""Tests for Finder service — Google Maps scraper wrapper (gosom).

TDD: these tests are written BEFORE the implementation.
Each test describes one behavior of FinderService.
"""

import json
from unittest.mock import patch

import pytest

from nuhoot.models.business import Business
from nuhoot.services.finder import FinderError, FinderService


def _make_gosom_entry(
    title: str = "مطعم النخيل",
    phone: str = "0501234567",
    address: str = "123 King Fahd Rd, Riyadh",
    website: str | None = "https://example.com",
    review_count: int = 120,
    review_rating: float = 4.5,
    latitude: float = 24.7136,
    longitude: float = 46.6753,
    link: str = "https://maps.google.com/place/123",
) -> str:
    """Build a single gosom JSON line (JSONL format)."""
    entry: dict[str, object] = {
        "title": title,
        "category": "Restaurant",
        "phone": phone,
        "address": address,
        "website": website,
        "review_count": review_count,
        "review_rating": review_rating,
        "latitude": latitude,
        "longitude": longitude,
        "link": link,
    }
    return json.dumps(entry, ensure_ascii=False)


SINGLE_ENTRY = _make_gosom_entry()


class TestFinderServiceExists:
    def test_finder_service_exists(self):
        """FinderService is importable and has a search method."""
        assert hasattr(FinderService, "search")
        assert hasattr(FinderService, "__init__")


class TestFinderAcceptsCategoryAndCity:
    def test_finder_accepts_category_and_city(self, db_session):
        """search() accepts category and city without raising."""
        service = FinderService(db_session, delay=0.0)
        with patch.object(service, "_run_gosom", return_value=SINGLE_ENTRY):
            results = service.search("restaurants", "Riyadh")
        assert isinstance(results, list)


class TestFinderReturnsBusinessList:
    def test_finder_returns_business_list(self, db_session):
        """search() returns a list of Business objects."""
        service = FinderService(db_session, delay=0.0)
        with patch.object(service, "_run_gosom", return_value=SINGLE_ENTRY):
            results = service.search("restaurants", "Riyadh")
        assert len(results) == 1
        assert isinstance(results[0], Business)
        assert results[0].name == "مطعم النخيل"
        assert results[0].category == "restaurants"

    def test_finder_maps_gosom_fields_to_business(self, db_session):
        """gosom fields are correctly mapped to Business model attributes."""
        service = FinderService(db_session, delay=0.0)
        with patch.object(service, "_run_gosom", return_value=SINGLE_ENTRY):
            results = service.search("restaurants", "Riyadh")
        biz = results[0]
        assert biz.address == "123 King Fahd Rd, Riyadh"
        assert biz.website == "https://example.com"
        assert biz.rating == 4.5
        assert biz.review_count == 120
        assert biz.latitude == 24.7136
        assert biz.longitude == 46.6753

    def test_finder_stores_results_in_database(self, db_session):
        """search() persists Business records to the database."""
        service = FinderService(db_session, delay=0.0)
        with patch.object(service, "_run_gosom", return_value=SINGLE_ENTRY):
            results = service.search("restaurants", "Riyadh")
        assert len(results) == 1
        stored_id = results[0].id
        assert stored_id is not None
        from nuhoot.models.business import Business as Biz

        fetched = db_session.get(Biz, stored_id)
        assert fetched is not None
        assert fetched.name == "مطعم النخيل"


class TestFinderDeduplicatesResults:
    def test_finder_deduplicates_by_phone(self, db_session):
        """Two entries with the same phone number are deduplicated to one."""
        entry_a = _make_gosom_entry(title="مطعم النخيل", phone="0501234567")
        entry_b = _make_gosom_entry(title="مطعم النخيل - فرع 2", phone="0501234567")
        output = entry_a + "\n" + entry_b
        service = FinderService(db_session, delay=0.0)
        with patch.object(service, "_run_gosom", return_value=output):
            results = service.search("restaurants", "Riyadh")
        assert len(results) == 1

    def test_finder_deduplicates_by_name_when_no_phone(self, db_session):
        """Two entries with the same name (no phone) are deduplicated."""
        entry_a = _make_gosom_entry(title="مطعم الشرق", phone="")
        entry_b = _make_gosom_entry(title="مطعم الشرق", phone="")
        output = entry_a + "\n" + entry_b
        service = FinderService(db_session, delay=0.0)
        with patch.object(service, "_run_gosom", return_value=output):
            results = service.search("restaurants", "Riyadh")
        assert len(results) == 1

    def test_finder_keeps_different_businesses(self, db_session):
        """Entries with different phones and names are all kept."""
        entry_a = _make_gosom_entry(title="مطعم النخيل", phone="0501234567")
        entry_b = _make_gosom_entry(title="مطعم الورد", phone="0551234567", address="456 Olaya St")
        output = entry_a + "\n" + entry_b
        service = FinderService(db_session, delay=0.0)
        with patch.object(service, "_run_gosom", return_value=output):
            results = service.search("restaurants", "Riyadh")
        assert len(results) == 2


class TestFinderNormalizesPhoneNumbers:
    def test_finder_normalizes_phone_numbers(self, db_session):
        """Phone numbers are normalized to +966 5X XXX XXXX format."""
        entry = _make_gosom_entry(phone="0501234567")
        service = FinderService(db_session, delay=0.0)
        with patch.object(service, "_run_gosom", return_value=entry):
            results = service.search("restaurants", "Riyadh")
        assert results[0].phone == "+966 50 123 4567"

    def test_finder_normalizes_plus_prefix(self, db_session):
        """Phone with +966 prefix is normalized correctly."""
        entry = _make_gosom_entry(phone="+966501234567")
        service = FinderService(db_session, delay=0.0)
        with patch.object(service, "_run_gosom", return_value=entry):
            results = service.search("restaurants", "Riyadh")
        assert results[0].phone == "+966 50 123 4567"

    def test_finder_skips_invalid_phone(self, db_session):
        """Non-Saudi phone numbers are set to None, not stored."""
        entry = _make_gosom_entry(phone="447911123456")
        service = FinderService(db_session, delay=0.0)
        with patch.object(service, "_run_gosom", return_value=entry):
            results = service.search("restaurants", "Riyadh")
        assert results[0].phone is None


class TestFinderHandlesEmptyResults:
    def test_finder_handles_empty_results(self, db_session):
        """Empty gosom output returns an empty list."""
        service = FinderService(db_session, delay=0.0)
        with patch.object(service, "_run_gosom", return_value=""):
            results = service.search("restaurants", "Riyadh")
        assert results == []

    def test_finder_handles_whitespace_only_output(self, db_session):
        """Whitespace-only output returns an empty list."""
        service = FinderService(db_session, delay=0.0)
        with patch.object(service, "_run_gosom", return_value="  \n  \n"):
            results = service.search("restaurants", "Riyadh")
        assert results == []

    def test_finder_handles_gosom_error(self, db_session):
        """FinderError is raised when gosom fails."""
        service = FinderService(db_session, delay=0.0)
        with (
            patch.object(
                service,
                "_run_gosom",
                side_effect=FinderError("gosom failed"),
            ),
            pytest.raises(FinderError),
        ):
            service.search("restaurants", "Riyadh")


class TestFinderGosomCommand:
    def test_finder_builds_correct_query(self, db_session):
        """The search query sent to gosom is 'category in city'."""
        service = FinderService(db_session, delay=0.0)
        with patch.object(service, "_run_gosom", return_value=SINGLE_ENTRY) as mock_run:
            service.search("restaurants", "Riyadh")
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        query = call_args.kwargs.get("query") or call_args.args[0]
        assert "restaurants" in query
        assert "Riyadh" in query
