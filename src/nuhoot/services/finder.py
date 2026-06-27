"""Finder service — wraps gosom CLI to scrape Google Maps businesses.

Finds local businesses for a given category and city, normalizes Saudi phone
numbers, deduplicates results, and stores them in the database.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import time
from pathlib import Path

import structlog
from sqlalchemy import select
from sqlalchemy.orm import Session

from nuhoot.config import settings
from nuhoot.models.business import Business
from nuhoot.utils.phone import normalize_saudi_phone

logger = structlog.get_logger()

# gosom depth of 10 yields ~120 results; each level ~12 results.
_RESULTS_PER_DEPTH = 12
_GOSOM_TIMEOUT = 600  # 10 minutes
_EXIT_ON_INACTIVITY = "5m"
_GOSOM_DOCKER_IMAGE = "nuhoot-gosom:latest"


class FinderError(Exception):
    """Raised when the Finder service encounters an unrecoverable error."""


def _safe_float(value: object) -> float | None:
    """Convert a JSON value to float, returning None on failure."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def _safe_int(value: object) -> int | None:
    """Convert a JSON value to int, returning None on failure."""
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return None
    return None


class FinderService:
    """Scrape Google Maps businesses via the gosom CLI.

    Usage::

        service = FinderService(db_session)
        results = service.search("restaurants", "Riyadh")
    """

    def __init__(
        self,
        db: Session,
        *,
        delay: float | None = None,
        gosom_path: str | None = None,
    ) -> None:
        self.db = db
        self.gosom_path: str = gosom_path or settings.gosom_binary_path
        self.delay: float = delay if delay is not None else float(settings.scraper_delay_seconds)
        self.default_max: int = settings.scraper_max_results

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def search(
        self,
        category: str,
        city: str,
        max_results: int = 200,
    ) -> list[Business]:
        """Find businesses for *category* in *city*.

        Args:
            category: Business type to search (e.g. ``"restaurants"``).
            city: Saudi city name (e.g. ``"Riyadh"``).
            max_results: Maximum number of businesses to return.

        Returns:
            List of deduplicated, stored :class:`Business` objects.

        Raises:
            FinderError: If the gosom scraper fails.
        """
        query = f"{category} in {city}"
        logger.info(
            "finder.search.start",
            category=category,
            city=city,
            max_results=max_results,
        )

        raw_output = self._run_gosom(query, max_results)
        entries = self._parse_output(raw_output)

        businesses = [self._to_business(e, category) for e in entries]
        businesses = self._deduplicate(businesses)
        businesses = businesses[:max_results]
        businesses = self._store(businesses)

        logger.info("finder.search.done", found=len(entries), stored=len(businesses))
        return businesses

    # ------------------------------------------------------------------
    # gosom subprocess
    # ------------------------------------------------------------------

    def _run_gosom(self, query: str, max_results: int) -> str:
        """Execute the gosom CLI via Docker and return its stdout (JSONL).

        Uses a Docker container (Ubuntu 22.04) because gosom's Playwright
        dependency doesn't support the host OS (Ubuntu 26.04).

        Includes a delay after the scrape to avoid IP bans.
        """
        depth = max(10, max_results // _RESULTS_PER_DEPTH)

        fd, tmp_path = tempfile.mkstemp(suffix=".txt", prefix="nuhoot_query_")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(query + "\n")

            cmd = [
                "docker",
                "run",
                "--rm",
                "-v",
                f"{tmp_path}:/data/query.txt",
                "-v",
                "gosom-browser-cache:/root/.cache/ms-playwright-go",
                _GOSOM_DOCKER_IMAGE,
                "-input",
                "/data/query.txt",
                "-json",
                "-depth",
                str(depth),
                "-c",
                "1",
                "-exit-on-inactivity",
                _EXIT_ON_INACTIVITY,
            ]
            logger.debug("finder.gosom.run", cmd=cmd)
            try:
                result = subprocess.run(  # noqa: S603 — trusted command
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=_GOSOM_TIMEOUT,
                    check=False,
                )
            except FileNotFoundError as exc:
                raise FinderError("docker not found — is Docker installed?") from exc
            except subprocess.TimeoutExpired as exc:
                raise FinderError(f"gosom timed out after {_GOSOM_TIMEOUT}s") from exc

            if result.returncode != 0:
                stderr = result.stderr.strip() if result.stderr else ""
                raise FinderError(f"gosom exited with code {result.returncode}: {stderr}")
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        # Rate-limit: wait between scrapes to avoid IP bans.
        if self.delay > 0:
            time.sleep(self.delay)

        return result.stdout

    # ------------------------------------------------------------------
    # Parsing
    # ------------------------------------------------------------------

    def _parse_output(self, output: str) -> list[dict[str, object]]:
        """Parse gosom JSONL (or JSON array) output into a list of dicts."""
        stripped = output.strip()
        if not stripped:
            return []

        # Try JSON array first (some gosom versions may emit this).
        try:
            data = json.loads(stripped)
            if isinstance(data, list):
                return [e for e in data if isinstance(e, dict)]
            if isinstance(data, dict):
                return [data]
        except json.JSONDecodeError:
            pass

        # Fall back to JSONL (one JSON object per line).
        entries: list[dict[str, object]] = []
        for line in stripped.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(entry, dict):
                entries.append(entry)
        return entries

    # ------------------------------------------------------------------
    # Mapping
    # ------------------------------------------------------------------

    def _to_business(self, entry: dict[str, object], category: str) -> Business:
        """Convert a gosom JSON entry to a :class:`Business` model."""
        title = str(entry.get("title", "")).strip()
        if not title:
            title = "Unknown"

        raw_phone = entry.get("phone")
        phone = self._normalize_phone(raw_phone)

        website_raw = entry.get("website")
        website = str(website_raw).strip() if website_raw else None
        has_website = bool(website)

        return Business(
            name=title,
            category=category,
            phone=phone,
            address=str(entry.get("address", "")).strip() or None,
            website=website,
            has_website=has_website,
            rating=_safe_float(entry.get("review_rating")),
            review_count=_safe_int(entry.get("review_count")) or 0,
            latitude=_safe_float(entry.get("latitude")),
            longitude=_safe_float(entry.get("longitude")),
        )

    def _normalize_phone(self, phone: object | None) -> str | None:
        """Normalize a phone number to +966 5X XXX XXXX.

        Returns ``None`` for empty or non-Saudi numbers.
        """
        if phone is None:
            return None
        phone_str = str(phone).strip()
        if not phone_str:
            return None
        try:
            return normalize_saudi_phone(phone_str)
        except ValueError:
            logger.debug("finder.phone.invalid", phone=phone_str)
            return None

    # ------------------------------------------------------------------
    # Deduplication
    # ------------------------------------------------------------------

    def _deduplicate(self, businesses: list[Business]) -> list[Business]:
        """Remove duplicates by phone (when available) or name."""
        seen: set[str] = set()
        unique: list[Business] = []
        for biz in businesses:
            key = biz.phone if biz.phone else biz.name.strip().lower()
            if key in seen:
                continue
            seen.add(key)
            unique.append(biz)
        return unique

    # ------------------------------------------------------------------
    # Database storage
    # ------------------------------------------------------------------

    def _store(self, businesses: list[Business]) -> list[Business]:
        """Persist businesses, skipping duplicates already in the DB."""
        result: list[Business] = []
        for biz in businesses:
            existing = self._find_existing(biz)
            if existing is not None:
                result.append(existing)
            else:
                self.db.add(biz)
                result.append(biz)
        self.db.commit()
        return result

    def _find_existing(self, biz: Business) -> Business | None:
        """Check if a business with the same phone/name already exists."""
        if biz.phone:
            stmt = select(Business).where(Business.phone == biz.phone)
            found = self.db.scalars(stmt).first()
            if found is not None:
                return found
        stmt = select(Business).where(
            Business.name == biz.name,
            Business.category == biz.category,
        )
        return self.db.scalars(stmt).first()
