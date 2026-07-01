"""
HTML Template System — generates HTML from archetype + business data.

Takes:
- Cairo-generated background image
- Business photo
- Business data (name, rating, reviews, post text, hashtags)
- Archetype (determines layout, colors, positioning)

Renders via Playwright → PNG.
"""

import base64
import os
from typing import Dict, List


def _encode_image(path: str) -> str:
    """Encode an image file as a base64 data URI."""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    ext = os.path.splitext(path)[1].lower()
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png"}.get(ext.lstrip("."), "image/jpeg")
    return f"data:{mime};base64,{data}"


def generate_html(
    bg_image_path: str,
    photo_path: str,
    business_name: str,
    rating: float,
    reviews: int,
    reviews_label: str,
    post_lines: List[str],
    hashtags: List[str],
    location: str,
    archetype_name: str = "split_luxury",
) -> str:
    """Generate complete HTML for a social media post.

    Args:
        bg_image_path: Path to Cairo-generated background
        photo_path: Path to business photo
        business_name: Arabic business name
        rating: Star rating (e.g., 4.5)
        reviews: Number of reviews
        reviews_label: Arabic word for "reviews" (تقييم)
        post_lines: List of Arabic text lines
        hashtags: List of hashtag strings (without #)
        location: Arabic location string
        archetype_name: Which archetype to use

    Returns:
        Complete HTML string
    """

    bg_uri = _encode_image(bg_image_path)
    photo_uri = _encode_image(photo_path)

    # Build hashtag HTML
    hashtag_html = "\n".join(
        f'        <span>#{tag}</span>' for tag in hashtags
    )

    # Build post text HTML
    post_html = "\n".join(
        f'        <p>{line}</p>' for line in post_lines
    )

    # Layout based on archetype
    if archetype_name == "hero_statement":
        layout_css = _hero_statement_css()
        photo_html = _hero_statement_photo(photo_uri, business_name, rating, reviews, reviews_label)
    elif archetype_name == "minimal_power":
        layout_css = _minimal_power_css()
        photo_html = _minimal_power_photo(photo_uri, business_name, rating, reviews, reviews_label)
    else:  # split_luxury (default — user's favorite "Black Velvet")
        layout_css = _split_luxury_css()
        photo_html = _split_luxury_photo(photo_uri, business_name, rating, reviews, reviews_label)

    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;700&family=Noto+Naskh+Arabic:wght@400;500;700&family=Noto+Sans+Arabic:wght@400;500;700&family=Lato:wght@300;400;700;900&display=swap');
@font-face {{
  font-family: 'Alyamama';
  src: url('file:///usr/share/fonts/truetype/noto/Alyamama-Bold.woff2') format('woff2');
  font-weight: 700;
}}
@font-face {{
  font-family: 'Alyamama';
  src: url('file:///usr/share/fonts/truetype/noto/Alyamama-ExtraBold.woff2') format('woff2');
  font-weight: 800;
}}
* {{
  margin: 0; padding: 0; box-sizing: border-box;
  -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility; -webkit-text-size-adjust: 100%;
}}
body {{
  width: 1080px; height: 1080px; overflow: hidden;
  background: #0a0a0a; position: relative;
  font-family: 'Noto Sans Arabic', sans-serif;
}}
.bg {{
  position: absolute; inset: 0; z-index: 0;
  background-image: url('{bg_uri}');
  background-size: cover; background-position: center;
}}
{layout_css}
</style>
</head>
<body>
  <div class="bg"></div>
  {photo_html}
  <div class="ptext">
{post_html}
  </div>
  <div class="tags">
{hashtag_html}
  </div>
  <div class="footer">
    <div class="fl">
      <div class="fline"></div>
      <div class="fdom">nuhoot.xyz</div>
      <div class="far">نُهوت — التسويق الرقمي</div>
    </div>
  </div>
</body>
</html>"""


def _gold_text_css() -> str:
    """Shared metallic gold text CSS."""
    return """
.gold-text {
  font-family: 'Alyamama', serif;
  font-weight: 800;
  background-image: linear-gradient(135deg,
    #462523 0%, #cb9b51 22%, #f6e27a 45%,
    #ffffff 50%, #f6e27a 55%, #cb9b51 78%, #462523 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 2px; line-height: 1.15;
  filter:
    drop-shadow(0px 1px 0px #8a6c3c)
    drop-shadow(0px 2px 0px #70562d)
    drop-shadow(0px 3px 0px #523e1e)
    drop-shadow(0px 12px 20px rgba(0,0,0,0.7));
}"""


def _common_elements_css() -> str:
    """Shared CSS for rating, text, tags, footer."""
    return """
.header { position: absolute; top: 32px; left: 56px; right: 56px;
  display: flex; justify-content: space-between; align-items: center; z-index: 10; }
.logo { display: flex; align-items: center; gap: 12px; }
.logo-c { width: 48px; height: 48px; border-radius: 50%;
  background: linear-gradient(135deg, #FF6B35, #FF8C42);
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 24px rgba(255,107,53,0.4), inset 0 1px 0 rgba(255,255,255,0.25); }
.logo-c span { font-family: 'Lato'; font-size: 26px; font-weight: 900; color: #fff; }
.logo-t { font-family: 'Lato'; font-size: 28px; font-weight: 700;
  color: rgba(245,240,232,0.95); letter-spacing: 1px;
  text-shadow: 0 2px 12px rgba(0,0,0,0.6); }
.loc { font-family: 'Noto Sans Arabic'; font-size: 16px;
  color: rgba(245,240,232,0.6); padding: 8px 20px;
  background: rgba(255,255,255,0.04); backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.06); border-radius: 999px; }
.rating { display: flex; align-items: center; gap: 12px; justify-content: flex-end; }
.star-b { width: 38px; height: 38px; border-radius: 50%;
  background: rgba(212,175,55,0.12); border: 1px solid rgba(212,175,55,0.35);
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 0 16px rgba(212,175,55,0.08); }
.star-b span { font-size: 19px; color: #D4AF37; }
.rnum { font-family: 'Lato'; font-size: 30px; font-weight: 700; color: #D4AF37; }
.dot { width: 5px; height: 5px; border-radius: 50%; background: rgba(212,175,55,0.35); }
.revs { font-family: 'Noto Sans Arabic'; font-size: 19px; color: rgba(245,240,232,0.75); }
.ptext { position: absolute; z-index: 10; }
.ptext p { font-family: 'Noto Naskh Arabic'; font-size: 34px; font-weight: 500;
  line-height: 1.6; letter-spacing: 0.5px; margin-bottom: 14px;
  text-shadow: 0 2px 24px rgba(0,0,0,0.8); }
.ptext p:nth-child(1) { color: #FFFFFF; }
.ptext p:nth-child(2) { color: rgba(245,240,232,0.92); }
.ptext p:nth-child(3) { color: rgba(245,240,232,0.85); }
.tags { position: absolute; z-index: 10; display: flex; gap: 16px; }
.tags span { font-family: 'Noto Sans Arabic'; font-size: 17px;
  color: rgba(212,175,55,0.6); letter-spacing: 0.3px; }
.footer { position: absolute; bottom: 32px; left: 56px; right: 56px;
  display: flex; justify-content: space-between; align-items: center; z-index: 10; }
.fl { display: flex; align-items: center; gap: 16px; }
.fline { width: 56px; height: 1.5px; background: linear-gradient(90deg, #D4AF37, rgba(212,175,55,0.2)); }
.fdom { font-family: 'Lato'; font-size: 17px; color: rgba(155,147,136,0.8); letter-spacing: 0.5px; }
.far { font-family: 'Noto Sans Arabic'; font-size: 14px; color: rgba(155,147,136,0.5); }
"""


def _split_luxury_css() -> str:
    """CSS for split_luxury archetype — photo top 50%, text bottom 50%."""
    return f"""
{_common_elements_css()}
{_gold_text_css()}
.photo-frame {{
  position: absolute; top: 80px; left: 56px; right: 56px; height: 460px;
  border-radius: 24px; overflow: hidden;
  border: 2px solid rgba(212,175,55,0.15);
  box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 80px rgba(212,175,55,0.05);
  z-index: 5;
}}
.photo-frame img {{ width: 100%; height: 100%; object-fit: cover;
  filter: brightness(0.95) contrast(1.1) saturate(1.15); }}
.photo-frame::after {{ content: ''; position: absolute; inset: 0;
  background: linear-gradient(180deg, transparent 50%, rgba(5,5,8,0.75)); }}
.name-overlay {{ position: absolute; bottom: 24px; right: 28px; left: 28px; z-index: 6; text-align: right; }}
.gold-text {{ font-size: 52px; margin-bottom: 14px; }}
.ptext {{ bottom: 140px; right: 56px; left: 56px; text-align: right; }}
.tags {{ bottom: 80px; right: 56px; }}
"""


def _hero_statement_css() -> str:
    """CSS for hero_statement archetype — center dominant."""
    return f"""
{_common_elements_css()}
{_gold_text_css()}
.photo-frame {{
  position: absolute; top: 180px; left: 50%; transform: translateX(-50%);
  width: 880px; height: 320px; border-radius: 24px; overflow: hidden;
  border: 2px solid rgba(212,175,55,0.15);
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
  z-index: 5;
}}
.photo-frame img {{ width: 100%; height: 100%; object-fit: cover;
  filter: brightness(0.95) contrast(1.1) saturate(1.15); }}
.photo-frame::after {{ content: ''; position: absolute; inset: 0;
  background: linear-gradient(180deg, transparent 60%, rgba(5,5,8,0.6)); }}
.name-overlay {{ position: absolute; top: 80px; left: 0; right: 0; text-align: center; z-index: 6; }}
.gold-text {{ font-size: 56px; margin-bottom: 12px; }}
.rating {{ justify-content: center; }}
.ptext {{ bottom: 130px; left: 50%; transform: translateX(-50%); width: 880px; text-align: center; }}
.tags {{ bottom: 80px; left: 50%; transform: translateX(-50%); }}
"""


def _minimal_power_css() -> str:
    """CSS for minimal_power archetype — typography hero, photo as circle."""
    return f"""
{_common_elements_css()}
{_gold_text_css()}
.photo-circle {{
  position: absolute; top: 130px; left: 50%; transform: translateX(-50%);
  width: 280px; height: 280px; border-radius: 50%; overflow: hidden;
  border: 3px solid rgba(212,175,55,0.2);
  box-shadow: 0 12px 40px rgba(0,0,0,0.4), 0 0 60px rgba(212,175,55,0.06);
  z-index: 5;
}}
.photo-circle img {{ width: 100%; height: 100%; object-fit: cover;
  filter: brightness(0.95) contrast(1.1) saturate(1.15); }}
.name-overlay {{ position: absolute; top: 450px; left: 0; right: 0; text-align: center; z-index: 6; }}
.gold-text {{ font-size: 64px; margin-bottom: 16px; }}
.rating {{ justify-content: center; }}
.ptext {{ bottom: 130px; left: 50%; transform: translateX(-50%); width: 880px; text-align: center; }}
.tags {{ bottom: 80px; left: 50%; transform: translateX(-50%); }}
"""


def _split_luxury_photo(photo_uri, name, rating, reviews, reviews_label) -> str:
    return f"""
  <div class="header">
    <div class="logo">
      <div class="logo-c"><span>N</span></div>
      <div class="logo-t">Nuhoot</div>
    </div>
    <div class="loc">الرياض</div>
  </div>
  <div class="photo-frame">
    <img src="{photo_uri}">
    <div class="name-overlay">
      <div class="gold-text">{name}</div>
      <div class="rating">
        <div class="star-b"><span>★</span></div>
        <div class="rnum">{rating}</div>
        <div class="dot"></div>
        <div class="revs">{reviews} {reviews_label}</div>
      </div>
    </div>
  </div>
  """


def _hero_statement_photo(photo_uri, name, rating, reviews, reviews_label) -> str:
    return f"""
  <div class="header">
    <div class="logo">
      <div class="logo-c"><span>N</span></div>
      <div class="logo-t">Nuhoot</div>
    </div>
    <div class="loc">الرياض</div>
  </div>
  <div class="name-overlay">
    <div class="gold-text">{name}</div>
    <div class="rating">
      <div class="star-b"><span>★</span></div>
      <div class="rnum">{rating}</div>
      <div class="dot"></div>
      <div class="revs">{reviews} {reviews_label}</div>
    </div>
  </div>
  <div class="photo-frame">
    <img src="{photo_uri}">
  </div>
  """


def _minimal_power_photo(photo_uri, name, rating, reviews, reviews_label) -> str:
    return f"""
  <div class="header">
    <div class="logo">
      <div class="logo-c"><span>N</span></div>
      <div class="logo-t">Nuhoot</div>
    </div>
    <div class="loc">الرياض</div>
  </div>
  <div class="photo-circle">
    <img src="{photo_uri}">
  </div>
  <div class="name-overlay">
    <div class="gold-text">{name}</div>
    <div class="rating">
      <div class="star-b"><span>★</span></div>
      <div class="rnum">{rating}</div>
      <div class="dot"></div>
      <div class="revs">{reviews} {reviews_label}</div>
    </div>
  </div>
  """
