"""Tests for the Arabic text template pools in content_matcher.

TDD guard: these tests were written BEFORE expanding the pools.
They lock in the contract that every niche pool offers a rich,
varied set of headlines / taglines / CTAs that fit design panels.
"""

from __future__ import annotations

import random

import pytest

from nuhoot.design.content_matcher import (
    AMBIANCE_TEMPLATES,
    COFFEE_TEMPLATES,
    EXPERIENCE_TEMPLATES,
    GRILL_SAUDI_TEMPLATES,
    PIZZA_TEMPLATES,
    TEMPLATE_POOLS,
    generate_matched_text,
)

ALL_POOLS = [
    ("coffee", COFFEE_TEMPLATES),
    ("pizza", PIZZA_TEMPLATES),
    ("ambiance", AMBIANCE_TEMPLATES),
    ("experience", EXPERIENCE_TEMPLATES),
    ("grill_saudi", GRILL_SAUDI_TEMPLATES),
]


def _word_count(text: str) -> int:
    return len(text.split())


@pytest.mark.parametrize("name,pool", ALL_POOLS)
def test_pool_has_ten_headlines(name: str, pool: dict) -> None:
    assert len(pool["headlines"]) == 10, f"{name}: expected 10 headlines"


@pytest.mark.parametrize("name,pool", ALL_POOLS)
def test_headlines_shape_and_length(name: str, pool: dict) -> None:
    for h in pool["headlines"]:
        assert set(h.keys()) == {"text", "mood"}, f"{name}: bad headline keys {h}"
        assert isinstance(h["text"], str) and h["text"].strip()
        assert h["mood"] in {"intimate", "vibrant", "elegant", "rustic"}
        assert _word_count(h["text"]) <= 6, f"{name}: headline too long: {h['text']!r}"


@pytest.mark.parametrize("name,pool", ALL_POOLS)
def test_headlines_have_varied_moods(name: str, pool: dict) -> None:
    moods = {h["mood"] for h in pool["headlines"]}
    assert len(moods) >= 3, f"{name}: moods not varied enough: {moods}"


@pytest.mark.parametrize("name,pool", ALL_POOLS)
def test_headlines_are_unique(name: str, pool: dict) -> None:
    texts = [h["text"] for h in pool["headlines"]]
    assert len(set(texts)) == len(texts), f"{name}: duplicate headlines"


@pytest.mark.parametrize("name,pool", ALL_POOLS)
def test_pool_has_ten_taglines(name: str, pool: dict) -> None:
    assert len(pool["taglines"]) == 10, f"{name}: expected 10 taglines"


@pytest.mark.parametrize("name,pool", ALL_POOLS)
def test_taglines_length_and_unique(name: str, pool: dict) -> None:
    for t in pool["taglines"]:
        assert isinstance(t, str) and t.strip()
        assert _word_count(t) <= 12, f"{name}: tagline too long: {t!r}"
    assert len(set(pool["taglines"])) == len(pool["taglines"]), f"{name}: duplicate taglines"


@pytest.mark.parametrize("name,pool", ALL_POOLS)
def test_pool_has_ten_ctas(name: str, pool: dict) -> None:
    assert isinstance(pool["cta"], list), f"{name}: cta must be a list"
    assert len(pool["cta"]) == 10, f"{name}: expected 10 CTAs, got {len(pool['cta'])}"
    assert len(set(pool["cta"])) == len(pool["cta"]), f"{name}: duplicate CTAs"
    for c in pool["cta"]:
        assert isinstance(c, str) and c.strip()
        assert _word_count(c) <= 6, f"{name}: CTA too long: {c!r}"


@pytest.mark.parametrize("name,pool", ALL_POOLS)
def test_hashtags_within_platform_range(name: str, pool: dict) -> None:
    assert 4 <= len(pool["hashtags"]) <= 8, f"{name}: hashtag count off"


def test_template_pools_mapping_covers_all_subcategories() -> None:
    expected = {"coffee", "pizza", "interior", "exterior", "dining_scene", "grill", "traditional_saudi", "generic"}
    assert expected.issubset(TEMPLATE_POOLS.keys())


def test_generate_matched_text_returns_string_cta_and_three_taglines() -> None:
    random.seed(42)
    text = generate_matched_text(
        subcategory="coffee",
        mood="intimate",
        confidence=0.9,
        business_name="مقهى الأصالة",
        domain="example.com",
        brand_ar="الأصالة",
    )
    assert isinstance(text["cta"], str) and text["cta"].strip()
    assert len(text["taglines"]) == 3
    assert text["headline"]
    assert len(text["hashtags"]) == 5
    assert text["domain"] == "example.com"
    assert text["brand_ar"] == "الأصالة"


def test_generate_matched_text_low_confidence_falls_back_to_generic() -> None:
    random.seed(7)
    text = generate_matched_text(
        subcategory="coffee",
        mood="elegant",
        confidence=0.5,
        business_name="ب",
        domain="d.com",
        brand_ar="ب",
    )
    # generic pool == EXPERIENCE_TEMPLATES
    assert text["cta"] in EXPERIENCE_TEMPLATES["cta"]
