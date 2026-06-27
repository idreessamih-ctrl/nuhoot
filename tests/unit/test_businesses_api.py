"""Tests for businesses API routes."""

import json
from unittest.mock import MagicMock, patch

import httpx

from nuhoot.models.business import Business
from nuhoot.services.finder import FinderService


def _sample_gosom_output() -> str:
    """Build sample gosom JSONL output for tests."""
    entry: dict[str, object] = {
        "title": "مطعم النخيل",
        "category": "Restaurant",
        "phone": "0501234567",
        "address": "123 King Fahd Rd, Riyadh",
        "website": "https://example.com",
        "review_count": 120,
        "review_rating": 4.5,
        "latitude": 24.7136,
        "longitude": 46.6753,
        "link": "https://maps.google.com/place/123",
    }
    return json.dumps(entry, ensure_ascii=False)


class TestListBusinesses:
    def test_list_returns_empty_when_no_data(self, client):
        """GET /businesses returns empty list when DB is empty."""
        response = client.get("/businesses")
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["data"]["items"] == []
        assert body["data"]["total"] == 0

    def test_list_returns_stored_businesses(self, client, db_session):
        """GET /businesses returns businesses stored in DB."""
        biz = Business(name="مطعم النخيل", category="restaurants")
        db_session.add(biz)
        db_session.commit()
        response = client.get("/businesses")
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert len(body["data"]["items"]) == 1
        assert body["data"]["items"][0]["name"] == "مطعم النخيل"

    def test_list_supports_pagination(self, client, db_session):
        """GET /businesses respects page and per_page params."""
        for i in range(5):
            db_session.add(Business(name=f"Business {i}", category="restaurants"))
        db_session.commit()
        response = client.get("/businesses?per_page=2&page=1")
        assert response.status_code == 200
        body = response.json()
        assert len(body["data"]["items"]) == 2
        assert body["data"]["total"] == 5
        assert body["data"]["page"] == 1
        assert body["data"]["per_page"] == 2


class TestSearchBusinesses:
    def test_search_creates_businesses(self, client):
        """POST /businesses/search scrapes and stores businesses."""
        with patch.object(FinderService, "_run_gosom", return_value=_sample_gosom_output()):
            response = client.post(
                "/businesses/search",
                json={"category": "restaurants", "city": "Riyadh"},
            )
        assert response.status_code == 201
        body = response.json()
        assert body["success"] is True
        assert body["data"]["count"] == 1
        assert body["data"]["businesses"][0]["name"] == "مطعم النخيل"
        assert body["data"]["businesses"][0]["phone"] == "+966 50 123 4567"

    def test_search_validates_required_fields(self, client):
        """POST /businesses/search rejects missing category."""
        response = client.post(
            "/businesses/search",
            json={"city": "Riyadh"},
        )
        assert response.status_code == 422

    def test_search_returns_count(self, client):
        """POST /businesses/search returns the number of businesses found."""
        entry1 = _sample_gosom_output()
        entry2_dict: dict[str, object] = {
            "title": "مطعم الورد",
            "category": "Restaurant",
            "phone": "0551234567",
            "address": "456 Olaya St, Riyadh",
            "website": None,
            "review_count": 85,
            "review_rating": 4.2,
            "latitude": 24.6877,
            "longitude": 46.6857,
            "link": "https://maps.google.com/place/456",
        }
        entry2 = json.dumps(entry2_dict, ensure_ascii=False)
        output = entry1 + "\n" + entry2
        with patch.object(FinderService, "_run_gosom", return_value=output):
            response = client.post(
                "/businesses/search",
                json={"category": "restaurants", "city": "Riyadh"},
            )
        assert response.status_code == 201
        body = response.json()
        assert body["data"]["count"] == 2


class TestGetBusinessById:
    def test_get_existing_business(self, client, db_session):
        """GET /businesses/{id} returns the business."""
        biz = Business(name="مطعم النخيل", category="restaurants", phone="+966 50 123 4567")
        db_session.add(biz)
        db_session.commit()
        biz_id = biz.id
        response = client.get(f"/businesses/{biz_id}")
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["data"]["name"] == "مطعم النخيل"

    def test_get_nonexistent_returns_404(self, client):
        """GET /businesses/{id} returns 404 for nonexistent ID."""
        response = client.get("/businesses/99999")
        assert response.status_code == 404
        body = response.json()
        assert body["success"] is False


_INVESTIGATE_HTML = """\
<!DOCTYPE html>
<html lang="ar">
<head>
    <title>مطعم النخيل</title>
    <meta name="description" content="مطعم النخيل">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:title" content="مطعم النخيل">
</head>
<body>
    <h1>مرحبا</h1>
    <a href="https://www.instagram.com/nakheel">Instagram</a>
</body>
</html>
"""


def _mock_httpx_response(html: str) -> MagicMock:
    """Build a mock httpx.Response."""
    response = MagicMock(spec=httpx.Response)
    response.text = html
    response.status_code = 200
    return response


class TestInvestigateBusiness:
    def test_investigate_returns_updated_business(self, client, db_session):
        """POST /businesses/{id}/investigate triggers investigation."""
        biz = Business(
            name="مطعم النخيل",
            category="restaurants",
            website="https://example.com",
            rating=4.5,
            review_count=120,
        )
        db_session.add(biz)
        db_session.commit()
        biz_id = biz.id
        with patch("nuhoot.services.investigator.httpx.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_client.get.return_value = _mock_httpx_response(_INVESTIGATE_HTML)
            mock_client_cls.return_value = mock_client
            response = client.post(f"/businesses/{biz_id}/investigate")
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["data"]["has_website"] is True
        assert body["data"]["has_instagram"] is True
        assert body["data"]["seo_score"] is not None
        assert body["data"]["social_score"] is not None
        assert body["data"]["status"] == "investigated"

    def test_investigate_returns_404_for_nonexistent(self, client):
        """POST /businesses/{id}/investigate returns 404 for unknown ID."""
        response = client.post("/businesses/99999/investigate")
        assert response.status_code == 404
        body = response.json()
        assert body["success"] is False

    def test_investigate_handles_no_website(self, client, db_session):
        """POST /businesses/{id}/investigate works for business without website."""
        biz = Business(
            name="متجر بلا موقع",
            category="electronics",
            website=None,
            rating=3.5,
            review_count=10,
        )
        db_session.add(biz)
        db_session.commit()
        biz_id = biz.id
        with patch("nuhoot.services.investigator.httpx.Client") as mock_client_cls:
            mock_client_cls.return_value = MagicMock()
            response = client.post(f"/businesses/{biz_id}/investigate")
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["data"]["has_website"] is False
        assert body["data"]["seo_score"] == 0
        assert body["data"]["status"] == "investigated"
