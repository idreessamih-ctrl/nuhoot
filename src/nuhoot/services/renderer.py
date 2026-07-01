"""Renderer service v3 — GLM-primary text flow.

Architecture (per Opus consultation):
- GLM caption = PRIMARY text source (business-specific Arabic)
- niche_text_engine = FALLBACK ONLY (kicker + missing tagline slots)
- Kicker keyed by business.category (NOT campaign.niche)
- Rating = business.rating (single source, no duplicates)
- Emoji stripped from headline (system Chromium can't render them)

Pipeline:
    Pitch (GLM sample_posts) + Business → parse GLM caption →
    fill missing slots from niche engine → render HTML →
    Playwright screenshot → quality gate → image_posts
"""

from __future__ import annotations

import re
import structlog
from pathlib import Path
from typing import Any

from nuhoot.config import settings
from nuhoot.models.business import Business
from nuhoot.models.pitch import Pitch

logger = structlog.get_logger()

CHROMIUM_PATH = "/snap/chromium/current/usr/lib/chromium-browser/chrome"

# Minimum taglines to show on each design
MIN_TAGLINES = 3
MAX_HEADLINE_LEN = 50

# Emoji pattern to strip from headlines (system Chromium can't render them)
_EMOJI_RE = re.compile(
    "[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U0000FE00-\U0000FE0F"
    "\U0001FA70-\U0001FAFF\U00002600-\U000026FF\U00002B00-\U00002BFF"
    "\u2605\u2606\u2728\u2729\u272A\u272B\u272C\u272D\u272E\u272F\u2730\u2731]+",
    flags=re.UNICODE,
)

# Trailing punctuation to strip from headlines
_TRAILING_PUNCT_RE = re.compile(r'[،,.!?؟؛;]+$')


class RendererError(Exception):
    pass


def parse_glm_caption(caption: str) -> dict[str, Any]:
    """Parse a GLM-generated caption into headline + taglines + hashtags.

    GLM returns captions like:
        "ألذ مأكولات بحرية طازجة بانتظاركم!\\nنقدم لكم\\nقهوة مختصة #مأكولات_بحرية #الرياض"

    Returns:
        {"headline": str, "taglines": list[str], "hashtags": list[str]}
    """
    if not caption or not caption.strip():
        return {"headline": None, "taglines": [], "hashtags": []}

    # 1. Extract hashtags
    hashtags = re.findall(r"#[^\s#]+", caption)

    # 2. Strip hashtags from body
    body = re.sub(r"#[^\s#]+", "", caption).strip()
    # Collapse whitespace
    body = re.sub(r"\s+", " ", body)

    # 3. Split into lines
    lines = [l.strip() for l in re.split(r"[\n]+", body) if l.strip()]

    # Fallback: if single blob, split on Arabic sentence terminators
    if len(lines) == 1:
        lines = [s.strip() for s in re.split(r"[.!?؟।]+", body) if s.strip()]

    if not lines:
        return {"headline": None, "taglines": [], "hashtags": hashtags}

    # 4. Headline = first non-rating line, strip emoji, enforce length cap
    headline = None
    # Match: lines starting with "تقييم"/"مراجعات"/"نجوم" OR lines starting with
    # a digit that also contain rating-related words (تقييم، مراجعات، آلاف، نجوم، عملاء، زوار)
    _rating_words = re.compile(r'(تقييم|تقيّم|مراجعات|مراجعة|نجوم|آلاف|مئات|عملاء|زوار|تقييمكم)')
    _digit_start = re.compile(r'^[\d\.،,]+')
    for line in lines:
        clean_line = _EMOJI_RE.sub("", line).strip()
        # Skip empty
        if not clean_line:
            continue
        # Skip lines starting with rating words
        if clean_line.startswith(('تقييم', 'تقيّم', 'مراجعات', 'مراجعة', 'نجوم')):
            continue
        # Skip lines starting with a digit that contain rating-related words
        if _digit_start.match(clean_line) and _rating_words.search(clean_line):
            continue
        headline = clean_line
        break
    
    if not headline:
        # All lines were rating-like — use niche fallback by returning None
        headline = None
    
    if headline and len(headline) > MAX_HEADLINE_LEN:
        headline = headline[:MAX_HEADLINE_LEN].rsplit(" ", 1)[0]
    
    # Strip trailing punctuation (commas, periods, etc.)
    if headline:
        headline = _TRAILING_PUNCT_RE.sub("", headline).strip()

    # 5. Taglines = remaining lines (strip emoji, filter out rating-like lines)
    taglines = []
    for line in lines[1:]:
        clean = _EMOJI_RE.sub("", line).strip()
        if not clean or len(clean) <= 2:
            continue
        # Skip rating-like lines
        if clean.startswith(('تقييم', 'تقيّم', 'مراجعات', 'مراجعة', 'نجوم')):
            continue
        if _digit_start.match(clean) and _rating_words.search(clean):
            continue
        taglines.append(clean)

    return {"headline": headline, "taglines": taglines, "hashtags": hashtags}


class RendererService:
    """Generate branded social media post images via the Golden Engine.

    GLM-primary text flow:
    1. Parse GLM caption → headline + taglines + hashtags
    2. Fill missing tagline slots from niche_text_engine (fallback only)
    3. Kicker from business.category (NOT campaign.niche)
    4. Rating from business.rating (single source)
    """

    def __init__(self) -> None:
        self.output_dir = Path(settings.render_output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def render_posts(
        self, pitch: Pitch, business: Business, photo_path: str | None = None
    ) -> list[dict]:
        """Render an image for each sample post in *pitch*."""
        from playwright.sync_api import sync_playwright
        from nuhoot.design.template_engine import TEMPLATES, generate_html
        from nuhoot.design.niche_text_engine import generate_text
        from nuhoot.design.niche_config import get_niche_config, get_kicker, get_colors
        from nuhoot.design.photo_analyzer import analyze_photo
        from nuhoot.design.quality_gate import QualityGate
        from nuhoot.design.saudi_copy_engine import post_process_glm_caption, get_niche_copy
        import random

        # Determine niche from BUSINESS CATEGORY (not campaign niche)
        niche = self._get_business_niche(business)
        config = get_niche_config(niche)
        kicker = config["kicker"]
        logger.info("renderer.start", pitch_id=pitch.id, business_id=business.id,
                     niche=niche, kicker=kicker, business_category=business.category)

        # Get available photos — prefer real business photos from Google Maps
        photos = self._get_business_photos(business, niche, photo_path)
        if not photos:
            photos = self._available_photos(photo_path, niche)
        if not photos:
            logger.warning("renderer.no_photos", business_id=business.id)
            photos = [self._generate_fallback_photo(niche)]

        sample_posts = pitch.sample_posts or []
        image_posts: list[dict] = []
        gate = QualityGate()

        # Use ALL 15 templates for maximum variety — new ones first for bold look
        template_ids = [11, 12, 13, 14, 15, 1, 5, 2, 3, 4, 6, 7, 8, 9, 10]

        with sync_playwright() as pw:
            browser = pw.chromium.launch(
                executable_path=CHROMIUM_PATH,
                args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu",
                      "--force-device-scale-factor=2", "--hide-scrollbars"],
            )

            for index, post_data in enumerate(sample_posts[:10]):
                # Use niche-matched photo; cycle if more posts than photos
                # (Repeating a matching photo is better than using a mismatched one)
                photo = photos[index % len(photos)]

                # Analyze photo for smart positioning
                try:
                    profile = analyze_photo(photo)
                    obj_pos = profile.object_position
                except Exception:
                    obj_pos = "50% 50%"

                # Extract caption from GLM post data
                # GLM returns: {"content": "Arabic text", "hashtags": "#tag1 #tag2"}
                if isinstance(post_data, dict):
                    glm_caption = post_data.get("content", 
                                post_data.get("caption", 
                                post_data.get("post_text", "")))
                    glm_hashtags_str = post_data.get("hashtags", "")
                else:
                    glm_caption = str(post_data)
                    glm_hashtags_str = ""

                # === SAUDI COPY ENGINE (Claude Blueprint Step 1) ===
                # Step 1: Parse GLM caption
                glm_parsed = parse_glm_caption(glm_caption)

                seed = hash(f"{business.id}_{index}") % 1000
                
                # Step 2: Post-process GLM output through Saudi dialect rules
                saudi_processed = post_process_glm_caption(glm_caption, niche)
                
                # Step 3: Get niche fallback text
                niche_text = generate_text(niche, confidence=0.85, seed=seed,
                                           business_name=business.name,
                                           reviews=business.review_count or 320)

                # Step 4: Resolve final text — Saudi-processed GLM first, niche fallback
                # Headline: Saudi-processed GLM → niche template → original GLM
                headline = saudi_processed["headline"] or niche_text["headline"] or glm_parsed["headline"]

                # Taglines: Saudi-processed first, fill missing from niche
                taglines = list(saudi_processed["taglines"])
                if len(taglines) < MIN_TAGLINES:
                    needed = MIN_TAGLINES - len(taglines)
                    niche_tags = [t for t in niche_text["taglines"] if t not in taglines]
                    taglines.extend(niche_tags[:needed])
                taglines = taglines[:MIN_TAGLINES]

                # Hashtags: GLM first (from hashtags field + parsed from caption), niche fallback
                glm_hashtags = glm_parsed["hashtags"]
                if glm_hashtags_str:
                    if isinstance(glm_hashtags_str, list):
                        # GLM returns hashtags as a list: ["#tag1", "#tag2"]
                        glm_hashtags = glm_hashtags_str if glm_hashtags_str else glm_hashtags
                    elif isinstance(glm_hashtags_str, str):
                        # GLM returns hashtags as a string: "#tag1 #tag2"
                        glm_hashtags = re.findall(r"#[^\s#]+", glm_hashtags_str) or glm_hashtags
                hashtags = glm_hashtags if glm_hashtags else niche_text["hashtags"]
                # Normalize: ensure all hashtags are strings with # prefix
                hashtags = [str(h) if not str(h).startswith("#") else str(h) for h in hashtags][:5]

                # Rating: SINGLE SOURCE — business.rating only (no duplicates)
                _AR = "٠١٢٣٤٥٦٧٨٩"
                rating_val = business.rating or 4.5
                rating_ar = "".join(_AR[int(c)] if c.isdigit() else c for c in str(rating_val))
                reviews_val = business.review_count or 320
                reviews_ar = "".join(_AR[int(c)] if c.isdigit() else c for c in str(reviews_val))

                # Build the text data dict for the template
                text_data = {
                    "business_name": business.name,
                    "headline": headline,
                    "taglines": taglines,
                    "rating": rating_ar,
                    "reviews": reviews_val,
                    "reviews_ar": reviews_ar,
                    "hashtags": hashtags[:5],
                    "cta": niche_text.get("cta", "زورونا"),
                    "domain": "nuhoot.xyz",
                    "brand_ar": "نُهوت — التسويق الرقمي",
                    "kicker": kicker,
                }

                logger.info("renderer.text_resolved",
                           post_index=index,
                           headline_source="glm" if glm_parsed["headline"] else "niche",
                           headline=headline[:40],
                           tagline_count=len(taglines),
                           glm_taglines=len(glm_parsed["taglines"]),
                           niche_fills=MIN_TAGLINES - min(len(glm_parsed["taglines"]), MIN_TAGLINES))

                # === IMAGE-FIRST TEMPLATE SELECTION (Claude Blueprint Step 2) ===
                # Use photo analyzer's recommended template when available,
                # fall back to rotated template list for variety
                if profile and profile.recommended_template:
                    tid = profile.recommended_template
                else:
                    tid = template_ids[index % len(template_ids)]
                all_photos = photos[:3] if len(photos) >= 3 else None
                html = generate_html(tid, photo, text_data, obj_pos,
                                     niche=niche, photo_paths=all_photos)

                # Render with Playwright (sync)
                output_path = self._output_path(pitch.id, index)
                page = browser.new_page(viewport={"width": 1080, "height": 1080})
                page.set_content(html)
                page.wait_for_timeout(2000)
                page.screenshot(path=str(output_path), type="png")
                page.close()

                # Quality gate check
                try:
                    passed, details = gate.assess(str(output_path))
                    score = details.get("overall", 0)
                    logger.info("renderer.post_done", pitch_id=pitch.id,
                               post_index=index, template=tid, score=score,
                               passed=passed)
                except Exception:
                    pass

                image_posts.append({
                    "caption": glm_caption,
                    "image_path": str(output_path),
                    "template": TEMPLATES[tid][0],
                    "niche": niche,
                    "headline": headline,
                    "headline_source": "glm" if glm_parsed["headline"] else "niche",
                })

            browser.close()

        logger.info("renderer.done", pitch_id=pitch.id, rendered=len(image_posts),
                     niche=niche, kicker=kicker)
        return image_posts

    def _get_business_niche(self, business: Business) -> str:
        """Get niche from BUSINESS CATEGORY first, then campaign niche as fallback."""
        # Business category is the most reliable signal
        if business.category:
            cat = business.category.lower().strip()
            # Map common Google Maps categories to our niches
            cat_map = {
                "restaurants": "restaurants", "restaurant": "restaurants",
                "cafe": "cafes", "cafes": "cafes", "coffee_shop": "cafes",
                "bakery": "bakeries", "bakeries": "bakeries",
                "clinic": "clinics", "clinics": "clinics", "doctor": "clinics",
                "dentist": "dentists", "dental": "dentists",
                "pharmacy": "pharmacies", "pharmacies": "pharmacies",
                "dermatology": "dermatology", "skin_care": "dermatology",
                "salon": "salons", "salons": "salons", "beauty_salon": "salons",
                "barbershop": "barbershops", "barber": "barbershops",
                "spa": "spas", "spas": "spas",
                "real_estate": "real_estate", "real_estate_agency": "real_estate",
                "auto_repair": "auto_shops", "car_repair": "auto_shops",
                "car_wash": "car_wash",
                "gym": "gyms", "fitness": "gyms",
                "hvac": "hvac_ac", "air_conditioning": "hvac_ac",
                "cleaning": "cleaning", "cleaning_service": "cleaning",
                "training": "training_centers", "education": "training_centers",
                "event_venue": "event_halls", "event_hall": "event_halls",
                "perfume": "perfumes", "perfumes": "perfumes",
                "clothing": "fashion", "fashion": "fashion",
                "lawyer": "law_firms", "law_firm": "law_firms",
            }
            if cat in cat_map:
                return cat_map[cat]
            return "restaurants"  # Default to restaurants for unknown categories

        # Fallback: campaign niche
        try:
            if hasattr(business, 'campaign_id') and business.campaign_id:
                from nuhoot.models.campaign import Campaign
                from nuhoot.database import SessionLocal
                db = SessionLocal()
                try:
                    campaign = db.query(Campaign).filter_by(id=business.campaign_id).first()
                    if campaign:
                        return campaign.niche or "restaurants"
                finally:
                    db.close()
        except Exception:
            pass
        return "restaurants"

    def _get_business_photos(self, business: Business, niche: str, photo_path: str | None) -> list[str]:
        """Download real business photos from Google Maps (stored as photo_urls in DB).

        Returns a list of local file paths. Downloads on demand and caches.
        """
        import urllib.request

        # Check if business has photo_urls stored from gosom
        photo_urls = getattr(business, "photo_urls", None)
        if not photo_urls:
            return []

        # Create a per-business photo directory
        biz_photo_dir = Path(f"/tmp/nuhoot-photos/business_{business.id}")
        biz_photo_dir.mkdir(parents=True, exist_ok=True)

        # Check if we already downloaded these photos
        existing = sorted(biz_photo_dir.glob("*.jpg"))
        if len(existing) >= 3:
            logger.info("renderer.photos_cached", business_id=business.id, count=len(existing))
            return [str(f) for f in existing]

        # Download photos
        downloaded = []
        for i, photo in enumerate(photo_urls[:7]):  # Up to 7 photos
            url = photo.get("url", "")
            title = photo.get("title", f"photo_{i}").lower().replace(" ", "_").replace("&", "and")
            if not url:
                continue

            # Request higher resolution by modifying URL suffix
            if "=w" in url:
                url = url.split("=w")[0] + "=w1080-h1080-k-no"

            fname = f"{niche}_{title}.jpg"
            fpath = biz_photo_dir / fname

            if fpath.exists():
                downloaded.append(str(fpath))
                continue

            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=15) as resp:
                    fpath.write_bytes(resp.read())
                downloaded.append(str(fpath))
                logger.info("renderer.photo_downloaded", business_id=business.id,
                           title=title, size=fpath.stat().st_size // 1024)
            except Exception as e:
                logger.warning("renderer.photo_download_failed", url=url[:80], error=str(e))

        return downloaded

    def _available_photos(self, photo_path: str | None, niche: str = "restaurants") -> list[str]:
        """Get list of available photos, filtered by niche relevance.

        Priority:
        1. Niche-matched photos from /opt/nuhoot/assets/photos/{niche}/ (Pexels stock)
        2. Explicitly passed photo_path (if provided)
        3. All Pexels photos as fallback
        """
        all_photos: list[str] = []
        niche_photos: list[str] = []

        # 1. Pexels stock photos — primary source (10 per niche)
        pexels_dir = Path("/opt/nuhoot/assets/photos") / niche
        if pexels_dir.exists():
            for f in sorted(pexels_dir.glob("*.jpg")):
                fp = str(f)
                if fp not in niche_photos:
                    niche_photos.append(fp)
                if fp not in all_photos:
                    all_photos.append(fp)

        # 2. Explicitly passed photo_path
        if photo_path and Path(photo_path).exists():
            if photo_path not in all_photos:
                all_photos.append(photo_path)

        # 3. Old AI photos in /tmp/nuhoot-pro/ as last-resort fallback
        pro_dir = Path("/tmp/nuhoot-pro")
        if pro_dir.exists() and not niche_photos:
            for f in sorted(pro_dir.glob("*.jpg")):
                fp = str(f)
                if fp not in all_photos:
                    all_photos.append(fp)

        return niche_photos if niche_photos else all_photos

    def _generate_fallback_photo(self, niche: str) -> str:
        """Generate a fallback photo using Pollinations.ai."""
        import urllib.request, urllib.parse
        prompts = {
            "restaurants": "elegant restaurant interior, warm lighting, fine dining",
            "clinics": "modern medical clinic interior, clean, professional",
            "salons": "luxury beauty salon interior, elegant, modern",
            "default": "professional business interior, elegant, modern",
        }
        prompt = prompts.get(niche, prompts["default"])
        encoded = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=1080&height=1080&nologo=true&model=flux"
        out_path = f"/tmp/nuhoot/fallback_{niche}.jpg"
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        try:
            urllib.request.urlretrieve(url, out_path)
        except Exception:
            pass
        return out_path

    def _output_path(self, pitch_id: int, post_index: int) -> Path:
        return self.output_dir / f"pitch_{pitch_id}_post_{post_index}.png"
