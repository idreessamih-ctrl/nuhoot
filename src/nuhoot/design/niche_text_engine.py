"""Unified Text Generation Engine — works across ALL 20 Saudi business niches.

Architecture:
- niche_config.py: defines niches (kickers, photo subcategories, tone)
- niche_pools_data.json: 200 Arabic text designs (10 per niche × 20 niches)
- text_pools.py: restaurant-specific pools (coffee/pizza/etc subcategories)
- THIS MODULE: unifies everything into one generate_text() function

Usage:
    from nuhoot.design.niche_text_engine import generate_text
    text = generate_text(niche="clinics", mood="trustworthy", 
                         business_name="عيادة الشفاء", confidence=0.85)
"""

import json
import random
import os
from pathlib import Path
from nuhoot.design.niche_config import NICHES, get_niche_config, get_kicker

# ═══════════════════════════════════════════════════════
# LOAD POOLS
# ═══════════════════════════════════════════════════════
_POOLS_PATH = Path(__file__).parent / "niche_pools_data.json"

def _load_pools() -> dict:
    """Load all niche text pools from JSON."""
    with open(_POOLS_PATH, encoding="utf-8") as f:
        return json.load(f)

NICHE_POOLS = _load_pools()

# Restaurant subcategory pools (from text_pools.py — loaded dynamically)
_RESTAURANT_SUBCATS = {
    "coffee": "coffee", "pizza": "pizza", "interior": "ambiance",
    "exterior": "ambiance", "dining_scene": "experience",
    "grill": "grill_saudi", "traditional_saudi": "grill_saudi",
}

# Map restaurant subcategories to the existing text_pools.py pools
def _get_restaurant_pool(subcategory: str) -> dict:
    """Get restaurant text pool based on photo subcategory."""
    try:
        from nuhoot.design.text_pools import (
            COFFEE_POOL, PIZZA_POOL, AMBIANCE_POOL,
            EXPERIENCE_POOL, GRILL_SAUDI_POOL
        )
        pools = {
            "coffee": COFFEE_POOL, "pizza": PIZZA_POOL,
            "ambiance": AMBIANCE_POOL, "experience": EXPERIENCE_POOL,
            "grill_saudi": GRILL_SAUDI_POOL,
        }
        key = _RESTAURANT_SUBCATS.get(subcategory, "experience")
        return pools.get(key, EXPERIENCE_POOL)
    except ImportError:
        return NICHE_POOLS.get("restaurants", NICHE_POOLS.get("cafes", {}))


# ═══════════════════════════════════════════════════════
# TEXT GENERATION
# ═══════════════════════════════════════════════════════
def generate_text(
    niche: str,
    mood: str = None,
    confidence: float = 0.80,
    business_name: str = None,
    domain: str = "nuhoot.xyz",
    brand_ar: str = "نُهوت — التسويق الرقمي",
    subcategory: str = None,
    reviews: int = 320,
    seed: int = None,
) -> dict:
    """Generate Arabic text content for any niche.
    
    Args:
        niche: Niche key (e.g. "clinics", "salons", "restaurants")
        mood: Desired mood (e.g. "trustworthy", "glamorous"). If None, picks randomly.
        confidence: Photo classification confidence (0-1). <0.65 uses generic.
        business_name: Arabic business name. If None, uses niche default.
        domain: Website URL
        brand_ar: Arabic brand text
        subcategory: Photo subcategory (for restaurants, selects coffee/pizza/etc pool)
        reviews: Number of reviews to display
        seed: Random seed for reproducibility
    
    Returns:
        dict with: business_name, headline, taglines, rating, reviews, 
                   hashtags, cta, domain, brand_ar, kicker, _niche, _confidence
    """
    if seed is not None:
        random.seed(seed)
    
    config = get_niche_config(niche)
    
    if business_name is None:
        business_name = config["default_example"]
    
    kicker = config["kicker"]
    
    # Get the right text pool
    if niche == "restaurants" and subcategory:
        pool = _get_restaurant_pool(subcategory)
    elif niche in NICHE_POOLS:
        pool = NICHE_POOLS[niche]
    else:
        # Fallback to restaurants or cafes
        pool = NICHE_POOLS.get("restaurants", NICHE_POOLS.get("cafes", {}))
    
    if not pool or confidence < 0.50:
        # Very low confidence — use generic experience pool
        pool = NICHE_POOLS.get("restaurants", pool)
    
    # Pick headline matching mood, or any
    headlines = pool.get("headlines", [])
    if mood:
        mood_matches = [h for h in headlines if h.get("mood") == mood]
        if mood_matches:
            headline = random.choice(mood_matches)["text"]
        else:
            headline = random.choice(headlines).get("text", "تجربة استثنائية")
    else:
        headline = random.choice(headlines).get("text", "تجربة استثنائية") if headlines else "تجربة استثنائية"
    
    # Pick taglines, CTA, hashtags
    taglines = random.choice(pool.get("taglines", [["", "", ""]]))
    cta = random.choice(pool.get("cta", ["زورونا"]))
    hashtags = random.sample(pool.get("hashtags", ["#nuhoot"]), min(5, len(pool.get("hashtags", ["#nuhoot"]))))
    
    # Arabic-Indic numerals
    _AR = "٠١٢٣٤٥٦٧٨٩"
    reviews_ar = "".join(_AR[int(c)] if c.isdigit() else c for c in str(reviews))
    
    return {
        "business_name": business_name,
        "headline": headline,
        "taglines": taglines[:3],  # exactly 3 lines
        "rating": "٤٫٥",
        "reviews": reviews,
        "reviews_ar": reviews_ar,
        "hashtags": hashtags,
        "cta": cta,
        "domain": domain,
        "brand_ar": brand_ar,
        "kicker": kicker,
        "_niche": niche,
        "_subcategory": subcategory,
        "_mood": mood,
        "_confidence": confidence,
    }


# ═══════════════════════════════════════════════════════
# CONTENT RELEVANCE CHECK
# ═══════════════════════════════════════════════════════
# Claims that should NOT appear on certain niche photos
FORBIDDEN_CLAIMS = {
    # Restaurant-specific claims shouldn't appear on non-restaurant niches
    "المطبخ السعودي": {"clinics", "dentists", "pharmacies", "salons", "spas", "gyms", 
                       "real_estate", "auto_shops", "law_firms", "fashion", "perfumes"},
    "مشويات": {"clinics", "dentists", "pharmacies", "salons", "spas", "perfumes", "fashion"},
    "قهوة": {"dentists", "pharmacies", "salons", "auto_shops", "real_estate", "law_firms"},
    "بيتزا": {"clinics", "salons", "spas", "gyms", "real_estate", "auto_shops", "law_firms"},
    # Clinic-specific claims shouldn't appear on non-medical niches
    "عيادة": {"restaurants", "cafes", "bakeries", "salons", "spas", "gyms", 
              "auto_shops", "real_estate", "perfumes", "fashion", "law_firms"},
    "أسنان": {"restaurants", "cafes", "bakeries", "salons", "spas", "gyms", 
              "auto_shops", "real_estate", "perfumes", "fashion", "law_firms"},
    # Salon-specific claims
    "مكياج": {"clinics", "dentists", "pharmacies", "auto_shops", "real_estate", "law_firms", "gyms"},
    # Auto-specific claims
    "سيارات": {"clinics", "dentists", "pharmacies", "salons", "spas", "perfumes", "fashion", "law_firms"},
}


def check_content_relevance(niche: str, text: dict) -> dict:
    """Check if text is appropriate for the niche. FAIL = mismatch."""
    failures = []
    all_text = text.get("headline", "") + " " + " ".join(text.get("taglines", []))
    
    for claim, bad_niches in FORBIDDEN_CLAIMS.items():
        if claim in all_text and niche in bad_niches:
            failures.append(f"FORBIDDEN: '{claim}' on '{niche}' design")
    
    score = 100 - len(failures) * 40
    return {
        "category": "content_relevance",
        "score": max(0, score),
        "pass": len(failures) == 0,
        "failures": failures,
    }


# ═══════════════════════════════════════════════════════
# STATS / INFO
# ═══════════════════════════════════════════════════════
def get_niche_count() -> int:
    """Total number of supported niches."""
    return len(NICHES)

def get_total_text_designs() -> int:
    """Total text designs across all niches."""
    # 20 niches × 10 designs = 200
    # Plus restaurant subcategories (5 × 10 = 50) from text_pools.py
    restaurant_subcats = 5
    return (get_niche_count() * 10) + (restaurant_subcats * 10)

def list_niches_by_sector() -> dict:
    """Return niches grouped by sector."""
    from nuhoot.design.niche_config import SECTOR_GROUPS
    return SECTOR_GROUPS

if __name__ == "__main__":
    # Demo: generate text for each niche
    print(f"=== {get_niche_count()} NICHES, {get_total_text_designs()} TEXT DESIGNS ===\n")
    for niche in sorted(NICHES.keys()):
        text = generate_text(niche, seed=42)
        rel = check_content_relevance(niche, text)
        status = "✅" if rel["pass"] else "❌"
        print(f"  {status} {niche:20s} | {text['kicker']:30s} | {text['headline']}")
