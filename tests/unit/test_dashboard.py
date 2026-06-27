"""Tests for bilingual dashboard — Arabic RTL + English LTR with language toggle.

Follows TDD: these tests were written BEFORE any dashboard implementation.
They drive the design of the routes, templates, translations, and stats service.
"""

from nuhoot.models.business import Business
from nuhoot.models.campaign import Campaign
from nuhoot.models.message import Message
from nuhoot.models.pitch import Pitch
from nuhoot.services.stats import get_dashboard_stats, get_quota_usage

# ------------------------------------------------------------------ #
# Dashboard HTML page tests
# ------------------------------------------------------------------ #


class TestDashboardPages:
    def test_root_redirects_to_dashboard_arabic(self, client):
        """GET / redirects to /dashboard?lang=ar."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code in (301, 302, 307)
        location = response.headers["location"]
        assert "/dashboard" in location
        assert "lang=ar" in location

    def test_dashboard_page_returns_200(self, client):
        """GET /dashboard returns HTTP 200."""
        response = client.get("/dashboard")
        assert response.status_code == 200

    def test_dashboard_default_language_is_arabic(self, client):
        """GET /dashboard without lang param defaults to Arabic content."""
        response = client.get("/dashboard")
        assert response.status_code == 200
        # Arabic title for "Dashboard"
        assert "لوحة التحكم" in response.text

    def test_dashboard_supports_english(self, client):
        """GET /dashboard?lang=en returns 200 with English content."""
        response = client.get("/dashboard?lang=en")
        assert response.status_code == 200
        assert "Dashboard" in response.text

    def test_dashboard_has_language_toggle(self, client):
        """Dashboard page contains language toggle with both AR and EN links."""
        response = client.get("/dashboard")
        assert "lang=ar" in response.text
        assert "lang=en" in response.text

    def test_arabic_layout_has_rtl(self, client):
        """Arabic layout sets dir=rtl on the html element."""
        response = client.get("/dashboard?lang=ar")
        assert 'dir="rtl"' in response.text

    def test_english_layout_has_ltr(self, client):
        """English layout sets dir=ltr on the html element."""
        response = client.get("/dashboard?lang=en")
        assert 'dir="ltr"' in response.text

    def test_businesses_page_returns_200(self, client):
        """GET /businesses-page returns 200."""
        response = client.get("/businesses-page")
        assert response.status_code == 200

    def test_campaigns_page_returns_200(self, client):
        """GET /campaigns-page returns 200."""
        response = client.get("/campaigns-page")
        assert response.status_code == 200

    def test_analytics_page_returns_200(self, client):
        """GET /analytics returns 200."""
        response = client.get("/analytics")
        assert response.status_code == 200

    def test_businesses_page_is_bilingual(self, client):
        """Businesses page renders Arabic by default and English on request."""
        ar_response = client.get("/businesses-page")
        assert "الشركات" in ar_response.text
        en_response = client.get("/businesses-page?lang=en")
        assert "Businesses" in en_response.text

    def test_campaigns_page_is_bilingual(self, client):
        """Campaigns page renders Arabic by default and English on request."""
        ar_response = client.get("/campaigns-page")
        assert "الحملات" in ar_response.text
        en_response = client.get("/campaigns-page?lang=en")
        assert "Campaigns" in en_response.text

    def test_analytics_page_is_bilingual(self, client):
        """Analytics page renders Arabic by default and English on request."""
        ar_response = client.get("/analytics")
        assert "التحليلات" in ar_response.text
        en_response = client.get("/analytics?lang=en")
        assert "Analytics" in en_response.text

    def test_dashboard_shows_stats(self, client, db_session):
        """Dashboard page renders stat values from the database."""
        for i in range(3):
            db_session.add(Business(name=f"Business {i}", category="restaurants"))
        db_session.commit()
        response = client.get("/dashboard")
        assert "3" in response.text

    def test_dashboard_sets_lang_cookie(self, client):
        """Dashboard sets a lang cookie for persistence."""
        response = client.get("/dashboard?lang=en")
        cookies = response.headers.get("set-cookie", "")
        assert "lang=en" in cookies


# ------------------------------------------------------------------ #
# Stats service tests
# ------------------------------------------------------------------ #


class TestStatsService:
    def test_stats_service_returns_correct_counts(self, db_session):
        """get_dashboard_stats returns accurate counts from DB."""
        for i in range(3):
            db_session.add(Business(name=f"Business {i}", category="restaurants"))
        campaign = Campaign(name="Summer", niche="restaurants")
        campaign.contacted = 10
        campaign.responded = 3
        db_session.add(campaign)
        db_session.commit()

        stats = get_dashboard_stats(db_session)
        assert stats["total_businesses"] == 3
        assert stats["total_campaigns"] == 1
        assert stats["messages_sent"] == 0
        assert stats["response_rate"] == 30.0

    def test_stats_service_empty_db_returns_zeros(self, db_session):
        """get_dashboard_stats returns zeros for an empty DB."""
        stats = get_dashboard_stats(db_session)
        assert stats["total_businesses"] == 0
        assert stats["total_campaigns"] == 0
        assert stats["messages_sent"] == 0
        assert stats["response_rate"] == 0.0

    def test_stats_service_counts_sent_messages(self, db_session):
        """messages_sent counts only sent/delivered/read (not pending)."""
        biz = Business(name="Test Biz", category="restaurants")
        db_session.add(biz)
        db_session.commit()
        pitch = Pitch(business_id=biz.id, pitch_text="test pitch")
        db_session.add(pitch)
        db_session.commit()

        db_session.add(
            Message(
                pitch_id=pitch.id,
                business_id=biz.id,
                phone_number="+966501234567",
                status="sent",
            )
        )
        db_session.add(
            Message(
                pitch_id=pitch.id,
                business_id=biz.id,
                phone_number="+966501234567",
                status="pending",
            )
        )
        db_session.commit()

        stats = get_dashboard_stats(db_session)
        assert stats["messages_sent"] == 1

    def test_quota_usage_returns_used_limit_remaining(self, db_session):
        """get_quota_usage returns used, limit (1000), and remaining."""
        biz = Business(name="Test Biz", category="restaurants")
        db_session.add(biz)
        db_session.commit()
        pitch = Pitch(business_id=biz.id, pitch_text="test pitch")
        db_session.add(pitch)
        db_session.commit()

        db_session.add(
            Message(
                pitch_id=pitch.id,
                business_id=biz.id,
                phone_number="+966501234567",
                status="delivered",
            )
        )
        db_session.commit()

        quota = get_quota_usage(db_session)
        assert quota["used"] == 1
        assert quota["limit"] == 1000
        assert quota["remaining"] == 999

    def test_quota_usage_empty_db(self, db_session):
        """get_quota_usage on empty DB returns full quota."""
        quota = get_quota_usage(db_session)
        assert quota["used"] == 0
        assert quota["limit"] == 1000
        assert quota["remaining"] == 1000
