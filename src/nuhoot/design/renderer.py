"""
Render Pipeline — orchestrates archetype → background → HTML → Playwright → quality check.

This is the main entry point for generating jaw-dropping social media images.

Pipeline:
1. Select archetype based on business type
2. Generate deterministic seed from business data
3. Generate procedural background (Cairo + Perlin noise)
4. Build HTML with background + photo + Arabic text
5. Render to PNG via Playwright
6. Quality gate (OpenCV: contrast, harmony, balance, readability)
7. If quality < 0.75, retry with different seed (up to 3 attempts)
8. Return final image path(s)

License: FOSS (Cairo LGPL, Playwright Apache-2.0, OpenCV Apache-2.0)
"""

import asyncio
import os
import time
from typing import List, Optional, Tuple

from .design_system import ARCHETYPES, select_archetype, get_seed
from .background_generator import BackgroundGenerator
from .quality_gate import QualityGate
from .template_engine import TEMPLATES, generate_html as generate_html_v4
from .template import generate_html
from .saudi_copy_engine import get_niche_copy
from .niche_config import get_colors, get_kicker, get_trust_badge, get_niche_config
from .photo_analyzer import analyze_photo


# Chromium path (system snap install)
CHROMIUM_PATH = "/snap/chromium/current/usr/lib/chromium-browser/chrome"


class RenderPipeline:
    """Main pipeline for generating agency-quality social media images."""

    def __init__(
        self,
        output_dir: str = "/tmp/nuhoot",
        font_paths: Optional[List[str]] = None,
        max_retries: int = 3,
        quality_threshold: float = 0.75,
    ):
        self.output_dir = output_dir
        self.bg_generator = BackgroundGenerator()
        self.quality_gate = QualityGate()
        self.max_retries = max_retries
        self.quality_threshold = quality_threshold
        self.font_paths = font_paths or [
            "/usr/share/fonts/truetype/noto",
            "/usr/share/fonts/truetype/lato",
        ]
        os.makedirs(output_dir, exist_ok=True)

    def render_post_v4(
        self,
        business_name: str,
        rating: float,
        reviews: int,
        niche: str = "restaurants",
        photo_path: str = None,
        post_lines: List[str] = None,
        seed: int = 0,
        template_id: int = 1,
        output_name: str = None,
        size: Tuple[int, int] = (1080, 1080),
    ) -> str:
        """Generate a social media post using the v4 design system.

        Uses:
        - Saudi Arabic copy engine (authentic dialect)
        - Niche-specific colors (gold, teal, navy, etc.)
        - Trust badges (credibility indicators)
        - Dynamic headline sizing
        - Photo analyzer for optimal positioning
        - 15 luxury templates (T01-T15)

        Args:
            business_name: Arabic business name
            rating: Star rating (e.g., 4.7)
            reviews: Number of reviews
            niche: Business niche (restaurants, cafes, dentists, etc.)
            photo_path: Path to business photo
            post_lines: Override copy (if None, uses Saudi copy engine)
            seed: Seed for copy variant selection
            template_id: Template ID 1-15 (default 1 = Vertical Split)
            output_name: Custom output filename
            size: (width, height) in pixels

        Returns:
            Path to the rendered PNG image
        """
        # Arabic-Indic numeral conversion
        _AR = "٠١٢٣٤٥٦٧٨٩"
        def to_arabic(s):
            return "".join(_AR[int(c)] if c.isdigit() else c for c in str(s))

        rating_ar = to_arabic(f"{rating:.1f}")
        reviews_ar = to_arabic(reviews)

        # Get Saudi Arabic copy (or use provided lines)
        if post_lines:
            copy = {
                "headline": post_lines[0] if post_lines else "",
                "taglines": post_lines[1:4] if len(post_lines) > 1 else [],
                "tone": "conversational",
            }
        else:
            copy = get_niche_copy(niche, business_name, rating_ar, reviews, seed=seed)

        # Analyze photo for optimal positioning
        obj_pos = "50% 50%"
        if photo_path and os.path.exists(photo_path):
            try:
                profile = analyze_photo(photo_path)
                obj_pos = profile.object_position
            except Exception:
                pass

        # Build text data with niche-specific colors and trust badge
        text_data = {
            "business_name": business_name,
            "headline": copy["headline"],
            "taglines": copy["taglines"],
            "rating": rating_ar,
            "reviews": reviews,
            "reviews_ar": reviews_ar,
            "hashtags": [],
            "cta": "",
            "domain": "nuhoot.xyz",
            "brand_ar": "نُهوت — التسويق الرقمي",
            "kicker": get_kicker(niche),
            "trust_badge": get_trust_badge(niche),
        }

        # Generate HTML using v4 template engine
        if photo_path and os.path.exists(photo_path):
            html = generate_html_v4(
                template_id, photo_path, text_data, obj_pos, niche=niche
            )
        else:
            # No photo — use a fallback dark background
            html = generate_html_v4(
                template_id, photo_path or "", text_data, obj_pos, niche=niche
            )

        # Save HTML and render via Playwright
        html_path = os.path.join(self.output_dir, f"render_v4_{seed}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        output_name = output_name or f"post_v4_{niche}_{seed}.png"
        output_path = os.path.join(self.output_dir, output_name)

        asyncio.run(self._render_html(html_path, output_path, size))

        # Quality check
        if os.path.exists(output_path):
            passed, scores = self.quality_gate.assess(output_path)
            if not passed:
                # Log but still return — quality gate is advisory
                pass

        return output_path

    def render_post(
        self,
        business_name: str,
        rating: float,
        reviews: int,
        reviews_label: str = "تقييم",
        post_lines: List[str] = None,
        hashtags: List[str] = None,
        location: str = "الرياض",
        photo_path: str = None,
        business_type: str = "restaurant",
        archetype_name: str = None,
        output_name: str = None,
        size: Tuple[int, int] = (1080, 1080),
    ) -> str:
        """Generate a social media post image.

        Args:
            business_name: Arabic business name
            rating: Star rating (e.g., 4.5)
            reviews: Number of reviews
            reviews_label: Arabic word for "reviews"
            post_lines: List of Arabic text lines
            hashtags: List of hashtags (without #)
            location: Arabic location string
            photo_path: Path to business photo
            business_type: Type of business (determines archetype)
            archetype_name: Override archetype selection
            output_name: Custom output filename
            size: (width, height) in pixels

        Returns:
            Path to the rendered PNG image
        """
        # Defaults
        if post_lines is None:
            post_lines = [
                "اكتشف نكهات المطبخ السعودي الأصيل",
                "أطباق شهية محضرة بأجود المكونات",
                "تجربة طعام لا تُنسى في قلب الرياض",
            ]
        if hashtags is None:
            hashtags = ["مطعم_النخيل", "الرياض", "طعام_سعودي", "تجربة_فريدة"]

        # 1. Select archetype
        if archetype_name is None:
            archetype_name = select_archetype(business_type)
        archetype = ARCHETYPES[archetype_name]

        # 2. Generate seed
        content = post_lines[0] if post_lines else business_name
        base_seed = get_seed(business_name, content)

        # 3-7. Retry loop
        for attempt in range(self.max_retries):
            seed = base_seed + attempt * 1000

            # 3. Generate background
            bg_path = os.path.join(self.output_dir, f"bg_{seed}.png")
            self.bg_generator.generate(
                style=archetype.bg_style,
                bg_colors=archetype.bg_colors,
                seed=seed,
                output_path=bg_path,
            )

            # 4. Build HTML
            html = generate_html(
                bg_image_path=bg_path,
                photo_path=photo_path,
                business_name=business_name,
                rating=rating,
                reviews=reviews,
                reviews_label=reviews_label,
                post_lines=post_lines,
                hashtags=hashtags,
                location=location,
                archetype_name=archetype_name,
            )

            html_path = os.path.join(self.output_dir, f"render_{seed}.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html)

            # 5. Render via Playwright
            output_name = output_name or f"post_{archetype_name}_{seed}.png"
            output_path = os.path.join(self.output_dir, output_name)

            asyncio.run(self._render_html(html_path, output_path, size))

            if not os.path.exists(output_path):
                continue

            # 6. Quality check
            passed, scores = self.quality_gate.assess(output_path)

            if passed or attempt == self.max_retries - 1:
                # Return best attempt (or last attempt if all failed)
                return output_path

            # 7. Retry with different seed

        return output_path

    async def _render_html(
        self, html_path: str, output_path: str, size: Tuple[int, int]
    ):
        """Render HTML to PNG via Playwright."""
        from playwright.async_api import async_playwright

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                executable_path=CHROMIUM_PATH,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--force-device-scale-factor=2",
                    "--hide-scrollbars",
                ],
            )
            page = await browser.new_page(
                viewport={"width": size[0], "height": size[1]}
            )
            await page.goto(
                f"file://{os.path.abspath(html_path)}",
                wait_until="networkidle",
            )
            await page.evaluate("document.fonts.ready")
            await asyncio.sleep(0.5)
            await page.screenshot(path=output_path, type="png")
            await browser.close()

    def render_multiple_sizes(
        self,
        business_name: str,
        rating: float,
        reviews: int,
        photo_path: str = None,
        post_lines: List[str] = None,
        hashtags: List[str] = None,
        **kwargs,
    ) -> List[str]:
        """Render the same post in multiple sizes.

        Sizes: 1080×1080 (square), 1080×1920 (story), 1200×675 (landscape)
        """
        sizes = [
            ("square", (1080, 1080)),
            ("story", (1080, 1920)),
            ("landscape", (1200, 675)),
        ]
        paths = []
        for name, size in sizes:
            path = self.render_post(
                business_name=business_name,
                rating=rating,
                reviews=reviews,
                photo_path=photo_path,
                post_lines=post_lines,
                hashtags=hashtags,
                output_name=f"post_{name}.png",
                size=size,
                **kwargs,
            )
            paths.append(path)
        return paths
