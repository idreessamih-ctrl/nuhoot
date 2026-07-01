"""Nuhoot v4 — Bold Ad-Style Templates based on user's 9 design picks.

5 templates that look like REAL Saudi ads, not Canva templates:
1. Golden Hero — bold yellow, feature pills, ad layout
2. Purple Premium — purple gradient, price box, glass pills
3. Cinematic Dark — navy split, neon glow, big numbers
4. Clean Editorial — white bg, bold typography, minimal
5. Full-Bleed Story — photo-driven, warm overlay, cultural
"""

import base64

_AR = "٠١٢٣٤٥٦٧٨٩"
_to_arabic = lambda s: "".join(_AR[int(c)] if c.isdigit() else c for c in str(s))

def _photo_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ═══════════════════════════════════════════════════════
# NICHE → COLOR SYSTEM (bold, one dominant color per niche)
# ═══════════════════════════════════════════════════════
NICHE_COLORS = {
    "restaurants": {"bg": "#F5C518", "bg2": "#E5A800", "accent": "#1A1A1A", "text": "#1A1A1A", "pill_bg": "#1A1A1A", "pill_text": "#FFFFFF"},
    "cafes": {"bg": "#6F4E37", "bg2": "#5C3D2E", "accent": "#F5DEB3", "text": "#FFF8E7", "pill_bg": "#F5DEB3", "pill_text": "#3E2723"},
    "bakeries": {"bg": "#FF8C42", "bg2": "#E07B30", "accent": "#3E2723", "text": "#FFFFFF", "pill_bg": "#FFFFFF", "pill_text": "#3E2723"},
    "salons": {"bg": "#1A1A2E", "bg2": "#16213E", "accent": "#E94560", "text": "#FFFFFF", "pill_bg": "#E94560", "pill_text": "#FFFFFF"},
    "spas": {"bg": "#2D4A3E", "bg2": "#1E3328", "accent": "#A8D5BA", "text": "#E8F5E9", "pill_bg": "#A8D5BA", "pill_text": "#1E3328"},
    "barbershops": {"bg": "#0F0F0F", "bg2": "#1A1A1A", "accent": "#D4AF37", "text": "#FFFFFF", "pill_bg": "#D4AF37", "pill_text": "#0F0F0F"},
    "gyms": {"bg": "#0A0A0A", "bg2": "#1A1A1A", "accent": "#FF6B35", "text": "#FFFFFF", "pill_bg": "#FF6B35", "pill_text": "#0A0A0A"},
    "clinics": {"bg": "#E8F4F8", "bg2": "#D1ECF1", "accent": "#2DB8A8", "text": "#1E3A52", "pill_bg": "#2DB8A8", "pill_text": "#FFFFFF"},
    "dentists": {"bg": "#E8F4F8", "bg2": "#D1ECF1", "accent": "#00A8D5", "text": "#1E3A52", "pill_bg": "#00A8D5", "pill_text": "#FFFFFF"},
    "pharmacies": {"bg": "#E8F5E9", "bg2": "#C8E6C9", "accent": "#2E7D32", "text": "#1B5E20", "pill_bg": "#2E7D32", "pill_text": "#FFFFFF"},
    "dermatology": {"bg": "#FCE4EC", "bg2": "#F8BBD0", "accent": "#C2185B", "text": "#4A148C", "pill_bg": "#C2185B", "pill_text": "#FFFFFF"},
    "fashion": {"bg": "#1A1A2E", "bg2": "#16213E", "accent": "#E94560", "text": "#FFFFFF", "pill_bg": "#E94560", "pill_text": "#FFFFFF"},
    "perfumes": {"bg": "#1A1A1A", "bg2": "#2A2A2A", "accent": "#D4AF37", "text": "#FFFFFF", "pill_bg": "#D4AF37", "pill_text": "#1A1A1A"},
    "law_firms": {"bg": "#0E1428", "bg2": "#161E38", "accent": "#B8CCE0", "text": "#E8EDF5", "pill_bg": "#B8CCE0", "pill_text": "#0E1428"},
    "real_estate": {"bg": "#0E1428", "bg2": "#161E38", "accent": "#D4AF37", "text": "#E8EDF5", "pill_bg": "#D4AF37", "pill_text": "#0E1428"},
    "auto_shops": {"bg": "#1A1A1A", "bg2": "#2A2A2A", "accent": "#FF6B35", "text": "#FFFFFF", "pill_bg": "#FF6B35", "pill_text": "#1A1A1A"},
    "car_wash": {"bg": "#0A1929", "bg2": "#102A43", "accent": "#48CAE4", "text": "#FFFFFF", "pill_bg": "#48CAE4", "pill_text": "#0A1929"},
    "cleaning": {"bg": "#E8F5E9", "bg2": "#C8E6C9", "accent": "#4CAF50", "text": "#1B5E20", "pill_bg": "#4CAF50", "pill_text": "#FFFFFF"},
    "hvac_ac": {"bg": "#0A1929", "bg2": "#102A43", "accent": "#48CAE4", "text": "#FFFFFF", "pill_bg": "#48CAE4", "pill_text": "#0A1929"},
    "event_halls": {"bg": "#2D1B3D", "bg2": "#1A0F28", "accent": "#D4AF37", "text": "#FFFFFF", "pill_bg": "#D4AF37", "pill_text": "#2D1B3D"},
    "training_centers": {"bg": "#0E1428", "bg2": "#161E38", "accent": "#5C6BC0", "text": "#E8EDF5", "pill_bg": "#5C6BC0", "pill_text": "#FFFFFF"},
}

def _get_colors(niche):
    return NICHE_COLORS.get(niche, NICHE_COLORS["restaurants"])


def _build_css(c):
    return f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1080px; overflow:hidden; background:{c['bg']};
  font-family:'Noto Sans Arabic',sans-serif; -webkit-font-smoothing:antialiased; }}
.stage {{ position:relative; width:1080px; height:1080px; overflow:hidden; background:{c['bg']}; }}
.display {{ font-family:'Noto Kufi Arabic',serif; font-weight:900; line-height:1.2; direction:rtl; word-break:keep-all; }}
.body-ar {{ font-family:'Noto Sans Arabic',sans-serif; font-size:26px; line-height:1.6; direction:rtl; word-break:keep-all; }}
.label {{ font-family:'Lato',sans-serif; font-size:15px; font-weight:700; letter-spacing:0.2em; text-transform:uppercase; color:{c['accent']}; }}
.eyebrow {{ font-family:'Noto Kufi Arabic',serif; font-size:24px; font-weight:500; color:{c['accent']}; direction:rtl; }}
.pill {{ display:inline-block; background:{c['pill_bg']}; color:{c['pill_text']}; padding:10px 24px;
  border-radius:50px; font-size:18px; font-weight:600; font-family:'Noto Sans Arabic',sans-serif;
  white-space:nowrap; }}
.stars {{ color:{c['accent']}; }}
.footer-url {{ font-family:'Noto Mono',monospace; font-size:16px; color:{c['accent']}; opacity:0.6; }}
.footer-brand {{ font-family:'Noto Sans Arabic',sans-serif; font-size:18px; color:{c['accent']}; opacity:0.7; }}
"""


def _wrap(body, c):
    return f"""<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;700;900&family=Noto+Sans+Arabic:wght@400;600;700&display=swap" rel="stylesheet">
<style>{_build_css(c)}</style></head><body>{body}</body></html>"""


def _rating_block(data, c):
    rating = data.get("rating", "٤٫٧")
    reviews = _to_arabic(data["reviews"])
    return f"""<div style="display:flex;align-items:center;gap:12px;direction:rtl;" dir="rtl">
      <span class="stars" dir="ltr" style="font-size:22px;">★★★★<span style="opacity:0.3">★</span></span>
      <span style="font-size:28px;font-weight:800;color:{c['text']};white-space:nowrap;">{rating}</span>
      <span style="font-size:18px;color:{c['accent']};opacity:0.7;">{reviews} تقييم</span>
    </div>"""


def _footer(data, c):
    return f"""<div style="display:flex;justify-content:space-between;align-items:baseline;width:100%;gap:16px;padding-top:12px;
      border-top:1px solid {c['accent']}30;">
      <span class="footer-url" style="white-space:nowrap;">{data.get('domain','nuhoot.xyz')}</span>
      <span class="footer-brand" style="white-space:nowrap;">{data.get('brand_ar','نُهوت — التسويق الرقمي')}</span>
    </div>"""


# ═══════════════════════════════════════════════════════
# TEMPLATE 1: GOLDEN HERO — bold bg, headline top, photo center, pills bottom
# ═══════════════════════════════════════════════════════
def tpl_golden_hero(b64, data, obj_pos, c, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    trust = data.get("trust_badge", "")
    return _wrap(f"""<div class="stage">
  <!-- Top: kicker + headline -->
  <div style="position:absolute;top:0;left:0;right:0;padding:50px 50px 0;text-align:right;">
    <span class="label">{data.get('kicker','')}</span>
    <h1 class="display" style="font-size:56px;color:{c['text']};margin-top:10px;">{data['headline']}</h1>
    <span class="eyebrow" style="font-size:22px;">{data['business_name']}</span>
  </div>
  <!-- Center: photo in rounded frame -->
  <div style="position:absolute;top:280px;left:50%;transform:translateX(-50%);width:680px;height:480px;
    border-radius:24px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,0.25);">
    <img src="data:image/jpeg;base64,{b64}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};">
  </div>
  <!-- Bottom: pills + rating + footer -->
  <div style="position:absolute;bottom:0;left:0;right:0;padding:0 50px 40px;display:flex;flex-direction:column;gap:16px;align-items:flex-end;">
    <div style="display:flex;gap:10px;flex-wrap:wrap;justify-content:flex-end;">
      <span class="pill">{t1}</span>
      <span class="pill">{t2}</span>
      <span class="pill">{t3}</span>
    </div>
    {_rating_block(data, c)}
    {f'<div style="font-size:16px;color:{c['accent']};opacity:0.8;">✦ {trust}</div>' if trust else ''}
    {_footer(data, c)}
  </div>
</div>""", c)


# ═══════════════════════════════════════════════════════
# TEMPLATE 2: PREMIUM SPLIT — photo left, content right with pills
# ═══════════════════════════════════════════════════════
def tpl_premium_split(b64, data, obj_pos, c, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    trust = data.get("trust_badge", "")
    return _wrap(f"""<div class="stage" style="display:flex;">
  <!-- Left: photo -->
  <div style="width:52%;height:100%;overflow:hidden;position:relative;">
    <img src="data:image/jpeg;base64,{b64}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};">
    <div style="position:absolute;top:30px;left:30px;">
      <span class="label" style="color:#FFFFFF;text-shadow:0 2px 8px rgba(0,0,0,0.6);">{data.get('kicker','')}</span>
    </div>
  </div>
  <!-- Right: content -->
  <div style="width:48%;height:100%;background:{c['bg2']};display:flex;flex-direction:column;
    justify-content:center;gap:20px;padding:50px 40px;align-items:flex-end;text-align:right;">
    <span class="eyebrow">{data['business_name']}</span>
    <h1 class="display" style="font-size:50px;color:{c['text']};">{data['headline']}</h1>
    <div style="width:60px;height:3px;background:{c['accent']};border-radius:2px;"></div>
    <div style="display:flex;flex-direction:column;gap:10px;align-items:flex-end;">
      <span class="pill" style="font-size:16px;">{t1}</span>
      <span class="pill" style="font-size:16px;">{t2}</span>
      <span class="pill" style="font-size:16px;">{t3}</span>
    </div>
    {_rating_block(data, c)}
    {f'<div style="font-size:15px;color:{c['accent']};opacity:0.8;">✦ {trust}</div>' if trust else ''}
    {_footer(data, c)}
  </div>
</div>""", c)


# ═══════════════════════════════════════════════════════
# TEMPLATE 3: FULL-BLEED STORY — photo background, bottom card
# ═══════════════════════════════════════════════════════
def tpl_full_bleed(b64, data, obj_pos, c, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    trust = data.get("trust_badge", "")
    return _wrap(f"""<div class="stage">
  <img src="data:image/jpeg;base64,{b64}" style="position:absolute;inset:0;width:100%;height:100%;
    object-fit:cover;object-position:{obj_pos};filter:brightness(0.75);">
  <div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,0.8) 0%,rgba(0,0,0,0.3) 40%,transparent 70%);"></div>
  <!-- Top: kicker -->
  <div style="position:absolute;top:50px;right:50px;">
    <span class="label" style="color:#FFFFFF;text-shadow:0 2px 8px rgba(0,0,0,0.6);">{data.get('kicker','')}</span>
  </div>
  <!-- Bottom: glass card -->
  <div style="position:absolute;bottom:0;left:0;right:0;padding:40px 50px;
    background:linear-gradient(0deg,{c['bg']}95 0%,{c['bg']}80 60%,transparent 100%);
    display:flex;flex-direction:column;gap:14px;align-items:flex-end;">
    <span class="eyebrow" style="color:{c['accent']};">{data['business_name']}</span>
    <h1 class="display" style="font-size:52px;color:#FFFFFF;">{data['headline']}</h1>
    <div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end;">
      <span class="pill" style="font-size:15px;">{t1}</span>
      <span class="pill" style="font-size:15px;">{t2}</span>
    </div>
    {_rating_block(data, {**c, 'text':'#FFFFFF', 'accent':c['accent']})}
    {f'<div style="font-size:15px;color:{c['accent']};">✦ {trust}</div>' if trust else ''}
    {_footer(data, {**c, 'text':'#FFFFFF', 'accent':c['accent']})}
  </div>
</div>""", c)


# ═══════════════════════════════════════════════════════
# TEMPLATE 4: EDITORIAL GRID — photo top, bold content bottom
# ═══════════════════════════════════════════════════════
def tpl_editorial(b64, data, obj_pos, c, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    trust = data.get("trust_badge", "")
    return _wrap(f"""<div class="stage" style="display:flex;flex-direction:column;">
  <!-- Top: photo 55% -->
  <div style="height:55%;overflow:hidden;position:relative;">
    <img src="data:image/jpeg;base64,{b64}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};">
    <div style="position:absolute;top:30px;right:30px;">
      <span class="label" style="color:#FFFFFF;text-shadow:0 2px 8px rgba(0,0,0,0.7);">{data.get('kicker','')}</span>
    </div>
  </div>
  <!-- Bottom: content 45% -->
  <div style="flex:1;background:{c['bg2']};display:flex;flex-direction:column;
    justify-content:center;gap:14px;padding:35px 50px;align-items:flex-end;text-align:right;
    border-top:4px solid {c['accent']};">
    <div style="display:flex;justify-content:space-between;width:100%;align-items:baseline;">
      <span class="eyebrow">{data['business_name']}</span>
      {_rating_block(data, c)}
    </div>
    <h1 class="display" style="font-size:48px;color:{c['text']};">{data['headline']}</h1>
    <div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end;">
      <span class="pill" style="font-size:15px;">{t1}</span>
      <span class="pill" style="font-size:15px;">{t2}</span>
      <span class="pill" style="font-size:15px;">{t3}</span>
    </div>
    {f'<div style="font-size:15px;color:{c['accent']};opacity:0.8;">✦ {trust}</div>' if trust else ''}
    {_footer(data, c)}
  </div>
</div>""", c)


# ═══════════════════════════════════════════════════════
# TEMPLATE 5: CENTER CARD — photo bg, centered glass card
# ═══════════════════════════════════════════════════════
def tpl_center_card(b64, data, obj_pos, c, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    trust = data.get("trust_badge", "")
    return _wrap(f"""<div class="stage">
  <img src="data:image/jpeg;base64,{b64}" style="position:absolute;inset:0;width:100%;height:100%;
    object-fit:cover;object-position:{obj_pos};filter:brightness(0.7);">
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse at center,transparent 20%,rgba(0,0,0,0.4) 70%);"></div>
  <!-- Top: kicker -->
  <div style="position:absolute;top:50px;left:0;right:0;text-align:center;">
    <span class="label" style="color:#FFFFFF;text-shadow:0 2px 8px rgba(0,0,0,0.6);">{data.get('kicker','')}</span>
  </div>
  <!-- Center: card -->
  <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:760px;padding:44px 40px;
    background:rgba(255,255,255,0.08);backdrop-filter:blur(24px);border:1px solid rgba(255,255,255,0.15);
    border-radius:24px;box-shadow:0 20px 80px rgba(0,0,0,0.4);
    display:flex;flex-direction:column;gap:14px;align-items:center;text-align:center;">
    <span class="eyebrow" style="color:{c['accent']};">{data['business_name']}</span>
    <h1 class="display" style="font-size:52px;color:#FFFFFF;">{data['headline']}</h1>
    <div style="width:80px;height:3px;background:{c['accent']};border-radius:2px;"></div>
    <div class="body-ar" style="text-align:center;color:#FFFFFF;font-size:22px;">
      <div>{t1}</div><div>{t2}</div><div>{t3}</div>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center;">
      <span style="background:{c['accent']};color:{c['bg']};padding:8px 20px;border-radius:50px;font-size:16px;font-weight:600;">{data.get('rating','٤٫٧')} ★</span>
      <span style="background:rgba(255,255,255,0.15);color:#FFFFFF;padding:8px 20px;border-radius:50px;font-size:16px;">{_to_arabic(data['reviews'])} تقييم</span>
    </div>
    {f'<div style="font-size:15px;color:{c['accent']};">✦ {trust}</div>' if trust else ''}
    <div style="display:flex;justify-content:space-between;width:100%;padding-top:12px;
      border-top:1px solid rgba(255,255,255,0.1);">
      <span class="footer-url" style="color:rgba(255,255,255,0.5);">{data.get('domain','nuhoot.xyz')}</span>
      <span class="footer-brand" style="color:rgba(255,255,255,0.7);">{data.get('brand_ar','نُهوت — التسويق الرقمي')}</span>
    </div>
  </div>
</div>""", c)


# ═══════════════════════════════════════════════════════
# REGISTRY
# ═══════════════════════════════════════════════════════
TEMPLATES = {
    1: ("Golden Hero", tpl_golden_hero),
    2: ("Premium Split", tpl_premium_split),
    3: ("Full-Bleed Story", tpl_full_bleed),
    4: ("Editorial Grid", tpl_editorial),
    5: ("Center Card", tpl_center_card),
}


def generate_html(template_id, photo_path, data, obj_pos="50% 50%", niche="restaurants", photo_paths=None):
    c = _get_colors(niche)
    b64 = _photo_b64(photo_path)
    name, func = TEMPLATES[template_id]
    return func(b64, data, obj_pos, c)
