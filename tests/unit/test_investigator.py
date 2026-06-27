"""Tests for Investigator service — website + social media analysis.

TDD: these tests are written BEFORE the implementation.
Each test describes one behavior of InvestigatorService.
"""

from unittest.mock import MagicMock, patch

import httpx

from nuhoot.models.business import Business
from nuhoot.services.investigator import InvestigatorService

# ------------------------------------------------------------------ #
# HTML fixtures
# ------------------------------------------------------------------ #

FULL_SEO_HTML = """\
<!DOCTYPE html>
<html lang="ar">
<head>
    <title>مطعم النخيل — أفضل مطعم في الرياض</title>
    <meta name="description" content="مطعم النخيل يقدم أشهى الأطباق السعودية">
    <meta name="keywords" content="مطعم, الرياض, طعام سعودي">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:title" content="مطعم النخيل">
    <meta property="og:description" content="أفضل مطعم في الرياض">
    <meta property="og:image" content="https://example.com/logo.png">
</head>
<body>
    <h1>مرحبا بكم في مطعم النخيل</h1>
    <p>تواصل معنا على <a href="https://www.instagram.com/nakheel_restaurant">Instagram</a></p>
</body>
</html>
"""

HTML_WITHOUT_INSTAGRAM = """\
<!DOCTYPE html>
<html lang="ar">
<head>
    <title>متجر الإلكترونيات</title>
    <meta name="description" content="إلكترونيات حديثة">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <h1>متجر الإلكترونيات</h1>
    <p>لا يوجد انستغرام</p>
</body>
</html>
"""

MINIMAL_HTML = """\
<!DOCTYPE html>
<html><head></head><body><p>Hello</p></body></html>
"""


def _mock_httpx_response(html: str, status_code: int = 200) -> MagicMock:
    """Build a mock httpx.Response with the given HTML body."""
    response = MagicMock(spec=httpx.Response)
    response.text = html
    response.status_code = status_code
    return response


def _make_business(
    *,
    name: str = "مطعم النخيل",
    category: str = "restaurants",
    website: str | None = "https://example.com",
    rating: float | None = 4.5,
    review_count: int | None = 120,
) -> Business:
    """Create a Business object for testing."""
    return Business(
        name=name,
        category=category,
        website=website,
        rating=rating,
        review_count=review_count,
    )


# ------------------------------------------------------------------ #
# Tests
# ------------------------------------------------------------------ #


class TestInvestigatorServiceExists:
    def test_investigator_service_exists(self):
        """InvestigatorService is importable and has an investigate method."""
        assert hasattr(InvestigatorService, "investigate")
        assert hasattr(InvestigatorService, "__init__")


class TestInvestigatorAnalyzesWebsite:
    def test_investigator_analyzes_website(self, db_session):
        """investigate() fetches website HTML and sets has_website=True."""
        biz = _make_business(website="https://example.com")
        db_session.add(biz)
        db_session.commit()
        service = InvestigatorService(db_session)
        with patch("nuhoot.services.investigator.httpx.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_client.get.return_value = _mock_httpx_response(FULL_SEO_HTML)
            mock_client_cls.return_value = mock_client
            service.investigate(biz)
        assert biz.has_website is True
        assert biz.seo_score is not None
        assert biz.seo_score > 0


class TestInvestigatorDetectsInstagramLink:
    def test_investigator_detects_instagram_link(self, db_session):
        """investigate() detects Instagram links in the HTML and sets has_instagram."""
        biz = _make_business(website="https://example.com")
        db_session.add(biz)
        db_session.commit()
        service = InvestigatorService(db_session)
        with patch("nuhoot.services.investigator.httpx.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_client.get.return_value = _mock_httpx_response(FULL_SEO_HTML)
            mock_client_cls.return_value = mock_client
            service.investigate(biz)
        assert biz.has_instagram is True
        assert biz.instagram is not None
        assert "instagram.com" in biz.instagram

    def test_investigator_no_instagram_when_absent(self, db_session):
        """investigate() sets has_instagram=False when no Instagram link is found."""
        biz = _make_business(website="https://example.com")
        db_session.add(biz)
        db_session.commit()
        service = InvestigatorService(db_session)
        with patch("nuhoot.services.investigator.httpx.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_client.get.return_value = _mock_httpx_response(HTML_WITHOUT_INSTAGRAM)
            mock_client_cls.return_value = mock_client
            service.investigate(biz)
        assert biz.has_instagram is False
        assert biz.instagram is None


class TestInvestigatorScoresSeoCorrectly:
    def test_investigator_scores_seo_full_100(self, db_session):
        """SEO score is 100 when all SEO elements are present (HTTPS URL)."""
        biz = _make_business(website="https://example.com")
        service = InvestigatorService(db_session)
        with patch("nuhoot.services.investigator.httpx.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_client.get.return_value = _mock_httpx_response(FULL_SEO_HTML)
            mock_client_cls.return_value = mock_client
            service.investigate(biz)
        assert biz.seo_score == 100

    def test_investigator_scores_seo_partial_when_missing_elements(self, db_session):
        """SEO score is lower when some SEO elements are missing."""
        biz = _make_business(website="http://example.com")
        service = InvestigatorService(db_session)
        with patch("nuhoot.services.investigator.httpx.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_client.get.return_value = _mock_httpx_response(MINIMAL_HTML)
            mock_client_cls.return_value = mock_client
            service.investigate(biz)
        # MINIMAL_HTML has no title, no meta description, no keywords,
        # no viewport, no h1, no og tags, and HTTP (not HTTPS) → 0 points
        assert biz.seo_score == 0

    def test_investigator_scores_seo_https_gives_20(self, db_session):
        """HTTPS URL alone (no other SEO elements) gives 20 points."""
        biz = _make_business(website="https://secure.example.com")
        service = InvestigatorService(db_session)
        with patch("nuhoot.services.investigator.httpx.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_client.get.return_value = _mock_httpx_response(MINIMAL_HTML)
            mock_client_cls.return_value = mock_client
            service.investigate(biz)
        assert biz.seo_score == 20


class TestInvestigatorScoresSocialPresence:
    def test_investigator_scores_social_full_100(self, db_session):
        """Social score is 100 when Instagram + high rating + reviews + website."""
        biz = _make_business(
            website="https://example.com",
            rating=4.8,
            review_count=200,
        )
        db_session.add(biz)
        db_session.commit()
        service = InvestigatorService(db_session)
        with patch("nuhoot.services.investigator.httpx.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_client.get.return_value = _mock_httpx_response(FULL_SEO_HTML)
            mock_client_cls.return_value = mock_client
            service.investigate(biz)
        # Instagram (30) + rating>=4 (25) + review_count>=50 (25) + has_website (20) = 100
        assert biz.social_score == 100

    def test_investigator_scores_social_partial_without_instagram(self, db_session):
        """Social score is 70 when no Instagram but has website, rating, reviews."""
        biz = _make_business(
            website="https://example.com",
            rating=4.5,
            review_count=120,
        )
        service = InvestigatorService(db_session)
        with patch("nuhoot.services.investigator.httpx.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_client.get.return_value = _mock_httpx_response(HTML_WITHOUT_INSTAGRAM)
            mock_client_cls.return_value = mock_client
            service.investigate(biz)
        # rating>=4 (25) + review_count>=50 (25) + has_website (20) = 70
        assert biz.social_score == 70

    def test_investigator_scores_social_low_rating(self, db_session):
        """Social score excludes rating points when rating < 4.0."""
        biz = _make_business(
            website="https://example.com",
            rating=3.2,
            review_count=120,
        )
        service = InvestigatorService(db_session)
        with patch("nuhoot.services.investigator.httpx.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_client.get.return_value = _mock_httpx_response(HTML_WITHOUT_INSTAGRAM)
            mock_client_cls.return_value = mock_client
            service.investigate(biz)
        # review_count>=50 (25) + has_website (20) = 45
        assert biz.social_score == 45


class TestInvestigatorHandlesWebsiteTimeout:
    def test_investigator_handles_website_timeout(self, db_session):
        """investigate() handles httpx timeout gracefully without crashing."""
        biz = _make_business(website="https://example.com")
        service = InvestigatorService(db_session)
        with patch("nuhoot.services.investigator.httpx.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_client.get.side_effect = httpx.TimeoutException("timed out")
            mock_client_cls.return_value = mock_client
            service.investigate(biz)
        # Timeout → no HTML fetched, SEO score is 0, business still has_website=True
        assert biz.seo_score == 0
        assert biz.has_website is True
        assert biz.has_instagram is False


class TestInvestigatorHandlesNoWebsite:
    def test_investigator_handles_no_website(self, db_session):
        """investigate() handles a business with no website gracefully."""
        biz = _make_business(website=None, rating=4.5, review_count=120)
        db_session.add(biz)
        db_session.commit()
        service = InvestigatorService(db_session)
        with patch("nuhoot.services.investigator.httpx.Client") as mock_client_cls:
            mock_client_cls.return_value = MagicMock()
            service.investigate(biz)
        assert biz.has_website is False
        assert biz.seo_score == 0
        # No httpx call should have been made
        mock_client_cls.assert_not_called()

    def test_investigator_no_website_still_scores_social(self, db_session):
        """Social score is still computed for businesses without a website."""
        biz = _make_business(website=None, rating=4.5, review_count=120)
        service = InvestigatorService(db_session)
        with patch("nuhoot.services.investigator.httpx.Client") as mock_client_cls:
            mock_client_cls.return_value = MagicMock()
            service.investigate(biz)
        # No Instagram (0) + rating>=4 (25) + review_count>=50 (25) + no website (0) = 50
        assert biz.social_score == 50


class TestInvestigatorUpdatesBusinessModel:
    def test_investigator_updates_business_model(self, db_session):
        """investigate() updates the Business model with all results."""
        biz = _make_business(
            website="https://example.com",
            rating=4.5,
            review_count=120,
        )
        db_session.add(biz)
        db_session.commit()
        biz_id = biz.id
        service = InvestigatorService(db_session)
        with patch("nuhoot.services.investigator.httpx.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client.__enter__ = MagicMock(return_value=mock_client)
            mock_client.__exit__ = MagicMock(return_value=False)
            mock_client.get.return_value = _mock_httpx_response(FULL_SEO_HTML)
            mock_client_cls.return_value = mock_client
            service.investigate(biz)
        # Verify all investigation fields are updated
        assert biz.has_website is True
        assert biz.has_instagram is True
        assert biz.instagram is not None
        assert biz.seo_score == 100
        assert biz.social_score == 100
        assert biz.status == "investigated"

        # Verify changes are persisted to the database
        db_session.expire_all()
        fetched = db_session.get(Business, biz_id)
        assert fetched is not None
        assert fetched.has_website is True
        assert fetched.has_instagram is True
        assert fetched.seo_score == 100
        assert fetched.social_score == 100
        assert fetched.status == "investigated"
