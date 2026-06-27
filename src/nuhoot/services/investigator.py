"""Investigator service — analyzes a business's digital presence.

Fetches the business website HTML, checks for Instagram/social media links,
scores SEO (0-100) and social media presence (0-100), then updates the
Business model with the results.

SEO scoring (100 pts total):
    title (10), meta description (15), meta keywords (5), SSL/HTTPS (20),
    responsive viewport (20), h1 tag (10), og tags (20).

Social scoring (100 pts total):
    has Instagram (30), rating >= 4.0 (25), review_count >= 50 (25),
    has website (20).
"""

from __future__ import annotations

import re

import httpx
import structlog
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from nuhoot.models.business import Business

logger = structlog.get_logger()

# Default request timeout in seconds.
_DEFAULT_TIMEOUT = 10.0

# SEO point values — sum to 100.
_SEO_TITLE = 10
_SEO_DESCRIPTION = 15
_SEO_KEYWORDS = 5
_SEO_HTTPS = 20
_SEO_VIEWPORT = 20
_SEO_H1 = 10
_SEO_OG = 20

# Social point values — sum to 100.
_SOCIAL_INSTAGRAM = 30
_SOCIAL_HIGH_RATING = 25
_SOCIAL_MANY_REVIEWS = 25
_SOCIAL_HAS_WEBSITE = 20

# Thresholds.
_RATING_THRESHOLD = 4.0
_REVIEW_THRESHOLD = 50

# Regex to find an Instagram profile URL in raw HTML.
_INSTAGRAM_RE = re.compile(
    r"https?://(?:www\.)?instagram\.com/[A-Za-z0-9_.]+/?",
    re.IGNORECASE,
)


class InvestigatorError(Exception):
    """Raised when the Investigator service encounters an unrecoverable error."""


def _detect_instagram(html: str) -> str | None:
    """Return the first Instagram profile URL found in *html*, or None."""
    match = _INSTAGRAM_RE.search(html)
    if match:
        return match.group(0)
    return None


def _score_seo(html: str, url: str) -> int:
    """Score SEO quality of *html* (0-100) based on meta tags and structure."""
    soup = BeautifulSoup(html, "html.parser")
    score = 0

    # <title> tag with text content.
    if soup.title and soup.title.get_text(strip=True):
        score += _SEO_TITLE

    # Meta description.
    if soup.find("meta", attrs={"name": "description"}):
        score += _SEO_DESCRIPTION

    # Meta keywords.
    if soup.find("meta", attrs={"name": "keywords"}):
        score += _SEO_KEYWORDS

    # SSL / HTTPS.
    if url.startswith("https://"):
        score += _SEO_HTTPS

    # Responsive viewport meta tag.
    viewport = soup.find("meta", attrs={"name": "viewport"})
    if viewport:
        content = viewport.get("content", "")
        if content and "width=device-width" in content:
            score += _SEO_VIEWPORT

    # At least one <h1> tag.
    if soup.find("h1"):
        score += _SEO_H1

    # Open Graph tags (og:title or og:description).
    if soup.find("meta", property="og:title") or soup.find("meta", property="og:description"):
        score += _SEO_OG

    return score


def _score_social(
    *,
    has_instagram: bool,
    rating: float | None,
    review_count: int | None,
    has_website: bool,
) -> int:
    """Score social media presence (0-100) based on engagement signals."""
    score = 0
    if has_instagram:
        score += _SOCIAL_INSTAGRAM
    if rating is not None and rating >= _RATING_THRESHOLD:
        score += _SOCIAL_HIGH_RATING
    if review_count is not None and review_count >= _REVIEW_THRESHOLD:
        score += _SOCIAL_MANY_REVIEWS
    if has_website:
        score += _SOCIAL_HAS_WEBSITE
    return score


class InvestigatorService:
    """Investigate a business's digital presence.

    Usage::

        service = InvestigatorService(db_session)
        service.investigate(business)
    """

    def __init__(self, db: Session, *, timeout: float = _DEFAULT_TIMEOUT) -> None:
        self.db = db
        self.timeout = timeout

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def investigate(self, business: Business) -> Business:
        """Analyze *business*'s website and update its investigation fields.

        Fetches the website HTML (if the business has one), detects Instagram
        links, scores SEO and social presence, and persists the results.

        Args:
            business: The :class:`Business` to investigate.

        Returns:
            The updated *business* object.
        """
        logger.info(
            "investigator.start",
            business_id=business.id,
            name=business.name,
        )

        if not business.website:
            self._analyze_without_website(business)
        else:
            self._analyze_with_website(business)

        business.social_score = _score_social(
            has_instagram=business.has_instagram,
            rating=business.rating,
            review_count=business.review_count,
            has_website=business.has_website,
        )
        business.status = "investigated"
        self.db.commit()

        logger.info(
            "investigator.done",
            business_id=business.id,
            seo_score=business.seo_score,
            social_score=business.social_score,
        )
        return business

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _analyze_without_website(self, business: Business) -> None:
        """Set investigation fields for a business with no website."""
        business.has_website = False
        business.has_instagram = False
        business.instagram = None
        business.seo_score = 0

    def _analyze_with_website(self, business: Business) -> None:
        """Fetch and analyze the business website HTML."""
        website = business.website
        if not website:
            self._analyze_without_website(business)
            return

        business.has_website = True
        html = self._fetch_html(website)

        if html is None:
            # Fetch failed (timeout or HTTP error) — no HTML to analyze.
            business.has_instagram = False
            business.instagram = None
            business.seo_score = 0
            return

        instagram_url = _detect_instagram(html)
        business.has_instagram = instagram_url is not None
        business.instagram = instagram_url
        business.seo_score = _score_seo(html, website)

    def _fetch_html(self, url: str) -> str | None:
        """Fetch the HTML content at *url* using httpx.

        Returns ``None`` on timeout or HTTP error.
        """
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url)
                response.raise_for_status()
                return response.text
        except httpx.TimeoutException:
            logger.warning("investigator.fetch.timeout", url=url)
            return None
        except httpx.HTTPError as exc:
            logger.warning(
                "investigator.fetch.error",
                url=url,
                error=str(exc),
            )
            return None
