"""Nuhoot v7 — CLEAN. Opus's brutal review applied.

THE 5 RULES (from Opus):
1. Images must be LARGE (300-400px min, centered or full-bleed)
2. Backgrounds must be SOLID colors (no gradient glow spots)
3. Remove everything that isn't essential (no floating panels, no dots, no bokeh)
4. Stats need LABELS (no floating numbers)
5. Match the reference EXACTLY — kicker, headline, big image, taglines, rating, domain

Formula per design:
  Top bar: kicker + brand name pill
  Headline: large, clear, breathing room
  Hero image: LARGE, centered or full-bleed
  Tagline pills: 3 max, horizontal row
  Rating bar: stars + number + review count + trust badge
  Domain: small, corner
  NOTHING ELSE.
"""

import base64

_AR = "٠١٢٣٤٥٦٧٨٩"
_to_ar = lambda s: "".join(_AR[int(c)] if c.isdigit() else c for c in str(s))


def _photo_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# ═══════════════════════════════════════════════════════
# SOLID COLORS ONLY — no gradients, no glow spots
# Each niche: solid_bg, accent, accent_text, pill_bg, pill_text, text
# ═══════════════════════════════════════════════════════
NICHE_COLORS = {
    "restaurants": {"bg": "#eab308", "accent": "#78350f", "accent_text": "#fef3c7", "pill_bg": "#78350f", "pill_text": "#fef3c7", "text": "#1c1917", "kicker_color": "#78350f"},
    "cafes": {"bg": "#3e2723", "accent": "#d7a86e", "accent_text": "#3e2723", "pill_bg": "#d7a86e", "pill_text": "#3e2723", "text": "#f5e6d3", "kicker_color": "#d7a86e"},
    "bakeries": {"bg": "#c66820", "accent": "#3e2723", "accent_text": "#fff", "pill_bg": "#fff", "pill_text": "#3e2723", "text": "#fff", "kicker_color": "#fff"},
    "salons": {"bg": "#1a1a2e", "accent": "#e11d48", "accent_text": "#fff", "pill_bg": "#e11d48", "pill_text": "#fff", "text": "#fff", "kicker_color": "#e11d48"},
    "spas": {"bg": "#1e3a32", "accent": "#a8d5ba", "accent_text": "#1e3a32", "pill_bg": "#a8d5ba", "pill_text": "#1e3a32", "text": "#e8f5e9", "kicker_color": "#a8d5ba"},
    "barbershops": {"bg": "#0f0f0f", "accent": "#d4af37", "accent_text": "#0f0f0f", "pill_bg": "#d4af37", "pill_text": "#0f0f0f", "text": "#fff", "kicker_color": "#d4af37"},
    "gyms": {"bg": "#0a0a0a", "accent": "#ea580c", "accent_text": "#0a0a0a", "pill_bg": "#ea580c", "pill_text": "#0a0a0a", "text": "#fff", "kicker_color": "#ea580c"},
    "clinics": {"bg": "#0d9488", "accent": "#fff", "accent_text": "#0d9488", "pill_bg": "#fff", "pill_text": "#0d9488", "text": "#fff", "kicker_color": "#fff"},
    "dentists": {"bg": "#0c4a6e", "accent": "#0ea5e9", "accent_text": "#0c4a6e", "pill_bg": "#0ea5e9", "pill_text": "#0c4a6e", "text": "#fff", "kicker_color": "#0ea5e9"},
    "pharmacies": {"bg": "#0d9488", "accent": "#fff", "accent_text": "#0d9488", "pill_bg": "#fff", "pill_text": "#0d9488", "text": "#fff", "kicker_color": "#fff"},
    "dermatology": {"bg": "#831843", "accent": "#f9a8d4", "accent_text": "#831843", "pill_bg": "#f9a8d4", "pill_text": "#831843", "text": "#fce7f3", "kicker_color": "#f9a8d4"},
    "fashion": {"bg": "#1a1a2e", "accent": "#e11d48", "accent_text": "#fff", "pill_bg": "#e11d48", "pill_text": "#fff", "text": "#fff", "kicker_color": "#e11d48"},
    "perfumes": {"bg": "#0f0f0f", "accent": "#d4af37", "accent_text": "#0f0f0f", "pill_bg": "#d4af37", "pill_text": "#0f0f0f", "text": "#fff", "kicker_color": "#d4af37"},
    "law_firms": {"bg": "#0f172a", "accent": "#c9a227", "accent_text": "#0f172a", "pill_bg": "#c9a227", "pill_text": "#0f172a", "text": "#e2e8f0", "kicker_color": "#c9a227"},
    "real_estate": {"bg": "#1c1917", "accent": "#d4a574", "accent_text": "#1c1917", "pill_bg": "#d4a574", "pill_text": "#1c1917", "text": "#f5f5f4", "kicker_color": "#d4a574"},
    "auto_shops": {"bg": "#171717", "accent": "#dc2626", "accent_text": "#171717", "pill_bg": "#dc2626", "pill_text": "#fff", "text": "#fff", "kicker_color": "#dc2626"},
    "car_wash": {"bg": "#0c1e2e", "accent": "#38bdf8", "accent_text": "#0c1e2e", "pill_bg": "#38bdf8", "pill_text": "#0c1e2e", "text": "#fff", "kicker_color": "#38bdf8"},
    "cleaning": {"bg": "#166534", "accent": "#fff", "accent_text": "#166534", "pill_bg": "#fff", "pill_text": "#166534", "text": "#fff", "kicker_color": "#fff"},
    "hvac_ac": {"bg": "#0c1e2e", "accent": "#38bdf8", "accent_text": "#0c1e2e", "pill_bg": "#38bdf8", "pill_text": "#0c1e2e", "text": "#fff", "kicker_color": "#38bdf8"},
    "event_halls": {"bg": "#1c1510", "accent": "#d4af37", "accent_text": "#1c1510", "pill_bg": "#d4af37", "pill_text": "#1c1510", "text": "#fff", "kicker_color": "#d4af37"},
    "training_centers": {"bg": "#1e1b4b", "accent": "#818cf8", "accent_text": "#1e1b4b", "pill_bg": "#818cf8", "pill_text": "#1e1b4b", "text": "#e0e7ff", "kicker_color": "#818cf8"},
}

def _get_colors(niche):
    return NICHE_COLORS.get(niche, NICHE_COLORS["restaurants"])


def _wrap(body, c):
    return f"""<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;500;700;800;900&family=Noto+Sans+Arabic:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:1080px;height:1080px;overflow:hidden;
  font-family:'Noto Sans Arabic',sans-serif;-webkit-font-smoothing:antialiased;}}
.stage{{width:1080px;height:1080px;background:{c['bg']};position:relative;
  display:flex;flex-direction:column;direction:rtl;}}
</style></head><body>{body}</body></html>"""


# ═══════════════════════════════════════════════════════
# TEMPLATE 1: CLEAN HERO — Opus's reference formula exactly
# Top bar → Headline → BIG image → Taglines → Rating bar
# ═══════════════════════════════════════════════════════
def tpl_clean_hero(b64, data, obj_pos, c, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    rating = data.get("rating", "٤٫٧")
    reviews = data.get("reviews_str", "٢٠٠")
    trust = data.get("trust_badge", "")
    return _wrap(f"""
  <!-- Top bar: kicker + brand name pill -->
  <div style="padding:32px 40px;display:flex;justify-content:space-between;align-items:center;">
    <span style="font-size:16px;color:{c['kicker_color']};font-weight:600;letter-spacing:0.1em;">{data.get('kicker','')}</span>
    <span style="background:{c['accent']};color:{c['accent_text']};padding:10px 24px;border-radius:10px;
      font-size:18px;font-weight:700;font-family:'Noto Kufi Arabic',serif;">{data['business_name']}</span>
  </div>
  <!-- Headline: large, breathing room -->
  <div style="padding:0 40px;margin-bottom:20px;">
    <h1 style="font-family:'Noto Kufi Arabic',serif;font-size:56px;font-weight:900;color:{c['text']};
      text-align:right;line-height:1.15;">{data['headline']}</h1>
  </div>
  <!-- Hero image: LARGE, centered, with drop shadow -->
  <div style="flex:1;display:flex;justify-content:center;align-items:center;padding:10px 40px;">
    <img src="data:image/jpeg;base64,{b64}" style="max-width:100%;max-height:100%;object-fit:cover;
      width:900px;height:480px;border-radius:16px;object-position:{obj_pos};
      filter:drop-shadow(0 20px 40px rgba(0,0,0,0.3));">
  </div>
  <!-- Bottom section: taglines + rating -->
  <div style="padding:20px 40px 28px;">
    <div style="display:flex;justify-content:center;gap:12px;margin-bottom:20px;flex-wrap:wrap;">
      <span style="background:{c['pill_bg']};color:{c['pill_text']};padding:12px 20px;border-radius:25px;
        font-size:15px;font-weight:600;">{t1}</span>
      <span style="background:{c['pill_bg']};color:{c['pill_text']};padding:12px 20px;border-radius:25px;
        font-size:15px;font-weight:600;">{t2}</span>
      <span style="background:{c['pill_bg']};color:{c['pill_text']};padding:12px 20px;border-radius:25px;
        font-size:15px;font-weight:600;">{t3}</span>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:center;
      padding-top:16px;border-top:1px solid {c['accent']}30;">
      <div style="display:flex;align-items:center;gap:6px;">
        <span style="color:{c['accent']};font-size:16px;">★★★★★</span>
        <span style="font-size:20px;font-weight:800;color:{c['text']};">{rating}</span>
        <span style="font-size:14px;color:{c['kicker_color']};opacity:0.8;">{reviews} تقييم</span>
      </div>
      <div style="display:flex;align-items:center;gap:12px;">
        {f'<span style="font-size:13px;color:{c["kicker_color"]};opacity:0.8;">✦ {trust}</span>' if trust else ''}
        <span style="font-size:13px;color:{c['kicker_color']};opacity:0.6;">{data.get('domain','nuhoot.xyz')}</span>
        <span style="font-size:13px;color:{c['kicker_color']};opacity:0.7;">{data.get('brand_ar','نُهوت')}</span>
      </div>
    </div>
  </div>
</div>""", c)


# ═══════════════════════════════════════════════════════
# TEMPLATE 2: FULL-BLEED — Photo is the background
# Dark overlay → text on top → bottom bar
# ═══════════════════════════════════════════════════════
def tpl_full_bleed(b64, data, obj_pos, c, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    rating = data.get("rating", "٤٫٧")
    reviews = data.get("reviews_str", "٢٠٠")
    trust = data.get("trust_badge", "")
    return f"""<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;500;700;800;900&family=Noto+Sans+Arabic:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:1080px;height:1080px;overflow:hidden;font-family:'Noto Sans Arabic',sans-serif;}}
.fb{{width:1080px;height:1080px;position:relative;overflow:hidden;direction:rtl;}}
.fb img.bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{obj_pos};z-index:1;}}
.fb::after{{content:'';position:absolute;inset:0;z-index:2;
  background:linear-gradient(180deg,rgba(0,0,0,0.55) 0%,rgba(0,0,0,0.15) 35%,rgba(0,0,0,0.75) 75%,rgba(0,0,0,0.95) 100%);}}
</style></head><body>
<div class="fb">
  <img class="bg" src="data:image/jpeg;base64,{b64}">
  <!-- Top: kicker + brand name -->
  <div style="position:absolute;top:32px;left:40px;right:40px;z-index:10;display:flex;justify-content:space-between;align-items:center;">
    <span style="font-size:16px;color:rgba(255,255,255,0.9);font-weight:600;letter-spacing:0.1em;">{data.get('kicker','')}</span>
    <span style="background:{c['accent']};color:{c['accent_text']};padding:10px 24px;border-radius:10px;
      font-size:18px;font-weight:700;font-family:'Noto Kufi Arabic',serif;">{data['business_name']}</span>
  </div>
  <!-- Bottom: headline + taglines + rating -->
  <div style="position:absolute;bottom:0;left:0;right:0;z-index:10;padding:30px 40px;">
    <h1 style="font-family:'Noto Kufi Arabic',serif;font-size:52px;font-weight:900;color:#fff;
      text-align:right;line-height:1.15;margin-bottom:20px;text-shadow:0 4px 20px rgba(0,0,0,0.8);">{data['headline']}</h1>
    <div style="display:flex;justify-content:flex-end;gap:12px;margin-bottom:20px;flex-wrap:wrap;">
      <span style="background:{c['accent']};color:{c['accent_text']};padding:12px 20px;border-radius:25px;font-size:15px;font-weight:600;">{t1}</span>
      <span style="background:{c['accent']};color:{c['accent_text']};padding:12px 20px;border-radius:25px;font-size:15px;font-weight:600;">{t2}</span>
      <span style="background:{c['accent']};color:{c['accent_text']};padding:12px 20px;border-radius:25px;font-size:15px;font-weight:600;">{t3}</span>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:center;padding-top:16px;border-top:1px solid rgba(255,255,255,0.15);">
      <div style="display:flex;align-items:center;gap:6px;">
        <span style="color:{c['accent']};font-size:16px;">★★★★★</span>
        <span style="font-size:20px;font-weight:800;color:#fff;">{rating}</span>
        <span style="font-size:14px;color:rgba(255,255,255,0.7);">{reviews} تقييم</span>
      </div>
      <div style="display:flex;align-items:center;gap:12px;">
        {f'<span style="font-size:13px;color:{c["accent"]};">✦ {trust}</span>' if trust else ''}
        <span style="font-size:13px;color:rgba(255,255,255,0.5);">{data.get('domain','nuhoot.xyz')}</span>
        <span style="font-size:13px;color:rgba(255,255,255,0.5);">{data.get('brand_ar','نُهوت')}</span>
      </div>
    </div>
  </div>
</div></body></html>"""


# ═══════════════════════════════════════════════════════
# TEMPLATE 3: SPLIT — Photo right, content left (Arabic RTL)
# Clean two-column, photo large, text minimal
# ═══════════════════════════════════════════════════════
def tpl_split(b64, data, obj_pos, c, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    rating = data.get("rating", "٤٫٧")
    reviews = data.get("reviews_str", "٢٠٠")
    trust = data.get("trust_badge", "")
    return _wrap(f"""
  <div style="display:flex;flex:1;overflow:hidden;">
    <!-- Right side (Arabic first): photo, LARGE -->
    <div style="width:55%;position:relative;overflow:hidden;">
      <img src="data:image/jpeg;base64,{b64}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};">
    </div>
    <!-- Left side: content -->
    <div style="width:45%;padding:40px 35px;display:flex;flex-direction:column;justify-content:center;gap:24px;">
      <div>
        <span style="font-size:14px;color:{c['kicker_color']};font-weight:600;letter-spacing:0.1em;">{data.get('kicker','')}</span>
        <span style="display:block;margin-top:8px;background:{c['accent']};color:{c['accent_text']};
          padding:8px 18px;border-radius:10px;font-size:16px;font-weight:700;
          font-family:'Noto Kufi Arabic',serif;width:fit-content;">{data['business_name']}</span>
      </div>
      <h1 style="font-family:'Noto Kufi Arabic',serif;font-size:42px;font-weight:900;color:{c['text']};
        line-height:1.15;">{data['headline']}</h1>
      <div style="width:50px;height:3px;background:{c['accent']};border-radius:2px;"></div>
      <div style="display:flex;flex-direction:column;gap:10px;">
        <span style="background:{c['pill_bg']};color:{c['pill_text']};padding:10px 18px;border-radius:25px;
          font-size:14px;font-weight:600;width:fit-content;">{t1}</span>
        <span style="background:{c['pill_bg']};color:{c['pill_text']};padding:10px 18px;border-radius:25px;
          font-size:14px;font-weight:600;width:fit-content;">{t2}</span>
        <span style="background:{c['pill_bg']};color:{c['pill_text']};padding:10px 18px;border-radius:25px;
          font-size:14px;font-weight:600;width:fit-content;">{t3}</span>
      </div>
      <div style="margin-top:10px;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
          <span style="color:{c['accent']};font-size:18px;">★★★★★</span>
          <span style="font-size:24px;font-weight:900;color:{c['text']};">{rating}</span>
          <span style="font-size:14px;color:{c['kicker_color']};opacity:0.8;">{reviews} تقييم</span>
        </div>
        {f'<div style="font-size:13px;color:{c["kicker_color"]};opacity:0.8;">✦ {trust}</div>' if trust else ''}
      </div>
    </div>
  </div>
  <!-- Footer strip -->
  <div style="padding:16px 35px;display:flex;justify-content:space-between;align-items:center;
    border-top:1px solid {c['accent']}20;">
    <span style="font-size:13px;color:{c['kicker_color']};opacity:0.6;">{data.get('domain','nuhoot.xyz')}</span>
    <span style="font-size:13px;color:{c['kicker_color']};opacity:0.7;">{data.get('brand_ar','نُهوت — التسويق الرقمي')}</span>
  </div>
</div>""", c)


# ═══════════════════════════════════════════════════════
# TEMPLATE 4: GALLERY — Multi-photo for niches with people
# Main photo large + 2 smaller photos below
# ═══════════════════════════════════════════════════════
def tpl_gallery(b64, data, obj_pos, c, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    rating = data.get("rating", "٤٫٧")
    reviews = data.get("reviews_str", "٢٠٠")
    trust = data.get("trust_badge", "")
    # Use extra photos if available
    extra = photos_b64 or []
    p2 = extra[0] if len(extra) > 0 else b64
    p3 = extra[1] if len(extra) > 1 else b64
    return _wrap(f"""
  <!-- Top bar -->
  <div style="padding:28px 40px;display:flex;justify-content:space-between;align-items:center;">
    <span style="font-size:16px;color:{c['kicker_color']};font-weight:600;letter-spacing:0.1em;">{data.get('kicker','')}</span>
    <span style="background:{c['accent']};color:{c['accent_text']};padding:10px 24px;border-radius:10px;
      font-size:18px;font-weight:700;font-family:'Noto Kufi Arabic',serif;">{data['business_name']}</span>
  </div>
  <!-- Headline -->
  <div style="padding:0 40px;margin-bottom:16px;">
    <h1 style="font-family:'Noto Kufi Arabic',serif;font-size:50px;font-weight:900;color:{c['text']};
      text-align:right;line-height:1.15;">{data['headline']}</h1>
  </div>
  <!-- Photo gallery: main large + 2 smaller -->
  <div style="flex:1;padding:0 40px;display:flex;flex-direction:column;gap:12px;">
    <div style="flex:2;overflow:hidden;border-radius:16px;box-shadow:0 15px 40px rgba(0,0,0,0.25);">
      <img src="data:image/jpeg;base64,{b64}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};">
    </div>
    <div style="flex:1;display:flex;gap:12px;">
      <div style="flex:1;overflow:hidden;border-radius:12px;box-shadow:0 10px 25px rgba(0,0,0,0.2);">
        <img src="data:image/jpeg;base64,{p2}" style="width:100%;height:100%;object-fit:cover;">
      </div>
      <div style="flex:1;overflow:hidden;border-radius:12px;box-shadow:0 10px 25px rgba(0,0,0,0.2);">
        <img src="data:image/jpeg;base64,{p3}" style="width:100%;height:100%;object-fit:cover;">
      </div>
    </div>
  </div>
  <!-- Bottom: taglines + rating -->
  <div style="padding:20px 40px 28px;">
    <div style="display:flex;justify-content:center;gap:12px;margin-bottom:16px;flex-wrap:wrap;">
      <span style="background:{c['pill_bg']};color:{c['pill_text']};padding:12px 20px;border-radius:25px;font-size:15px;font-weight:600;">{t1}</span>
      <span style="background:{c['pill_bg']};color:{c['pill_text']};padding:12px 20px;border-radius:25px;font-size:15px;font-weight:600;">{t2}</span>
      <span style="background:{c['pill_bg']};color:{c['pill_text']};padding:12px 20px;border-radius:25px;font-size:15px;font-weight:600;">{t3}</span>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:center;padding-top:14px;border-top:1px solid {c['accent']}30;">
      <div style="display:flex;align-items:center;gap:6px;">
        <span style="color:{c['accent']};font-size:16px;">★★★★★</span>
        <span style="font-size:20px;font-weight:800;color:{c['text']};">{rating}</span>
        <span style="font-size:14px;color:{c['kicker_color']};opacity:0.8;">{reviews} تقييم</span>
      </div>
      <div style="display:flex;align-items:center;gap:12px;">
        {f'<span style="font-size:13px;color:{c["kicker_color"]};opacity:0.8;">✦ {trust}</span>' if trust else ''}
        <span style="font-size:13px;color:{c['kicker_color']};opacity:0.6;">{data.get('domain','nuhoot.xyz')}</span>
        <span style="font-size:13px;color:{c['kicker_color']};opacity:0.7;">{data.get('brand_ar','نُهوت')}</span>
      </div>
    </div>
  </div>
</div>""", c)


# ═══════════════════════════════════════════════════════
# TEMPLATE 5: STATS — For professional services (law, clinic, training)
# Clean stats with LABELS + photo + taglines
# ═══════════════════════════════════════════════════════
def tpl_stats(b64, data, obj_pos, c, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    rating = data.get("rating", "٤٫٧")
    reviews = data.get("reviews_str", "٢٠٠")
    trust = data.get("trust_badge", "")
    return _wrap(f"""
  <!-- Top bar -->
  <div style="padding:28px 40px;display:flex;justify-content:space-between;align-items:center;">
    <span style="font-size:16px;color:{c['kicker_color']};font-weight:600;letter-spacing:0.1em;">{data.get('kicker','')}</span>
    <span style="background:{c['accent']};color:{c['accent_text']};padding:10px 24px;border-radius:10px;
      font-size:18px;font-weight:700;font-family:'Noto Kufi Arabic',serif;">{data['business_name']}</span>
  </div>
  <!-- Headline -->
  <div style="padding:0 40px;margin-bottom:20px;">
    <h1 style="font-family:'Noto Kufi Arabic',serif;font-size:48px;font-weight:900;color:{c['text']};
      text-align:right;line-height:1.15;">{data['headline']}</h1>
  </div>
  <!-- Main content: photo + stats side by side -->
  <div style="flex:1;padding:0 40px;display:flex;gap:24px;">
    <!-- Photo: LARGE -->
    <div style="flex:1.3;overflow:hidden;border-radius:16px;box-shadow:0 15px 40px rgba(0,0,0,0.25);">
      <img src="data:image/jpeg;base64,{b64}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};">
    </div>
    <!-- Stats: WITH LABELS -->
    <div style="flex:1;display:grid;grid-template-columns:1fr 1fr;gap:12px;align-content:center;">
      <div style="background:{c['accent']}15;border:1px solid {c['accent']}30;border-radius:14px;padding:20px;text-align:center;">
        <div style="font-size:32px;font-weight:900;color:{c['accent']};">+٥٠٠</div>
        <div style="font-size:13px;color:{c['text']};opacity:0.7;margin-top:4px;">عميل سعيد</div>
      </div>
      <div style="background:{c['accent']}15;border:1px solid {c['accent']}30;border-radius:14px;padding:20px;text-align:center;">
        <div style="font-size:32px;font-weight:900;color:{c['accent']};">+١٠</div>
        <div style="font-size:13px;color:{c['text']};opacity:0.7;margin-top:4px;">سنوات خبرة</div>
      </div>
      <div style="background:{c['accent']}15;border:1px solid {c['accent']}30;border-radius:14px;padding:20px;text-align:center;">
        <div style="font-size:32px;font-weight:900;color:{c['accent']};">٩٨٪</div>
        <div style="font-size:13px;color:{c['text']};opacity:0.7;margin-top:4px;">نسبة رضا</div>
      </div>
      <div style="background:{c['accent']}15;border:1px solid {c['accent']}30;border-radius:14px;padding:20px;text-align:center;">
        <div style="font-size:32px;font-weight:900;color:{c['accent']};">٢٤/٧</div>
        <div style="font-size:13px;color:{c['text']};opacity:0.7;margin-top:4px;">دعم متواصل</div>
      </div>
    </div>
  </div>
  <!-- Bottom: taglines + rating -->
  <div style="padding:20px 40px 28px;">
    <div style="display:flex;justify-content:center;gap:12px;margin-bottom:16px;flex-wrap:wrap;">
      <span style="background:{c['pill_bg']};color:{c['pill_text']};padding:12px 20px;border-radius:25px;font-size:15px;font-weight:600;">{t1}</span>
      <span style="background:{c['pill_bg']};color:{c['pill_text']};padding:12px 20px;border-radius:25px;font-size:15px;font-weight:600;">{t2}</span>
      <span style="background:{c['pill_bg']};color:{c['pill_text']};padding:12px 20px;border-radius:25px;font-size:15px;font-weight:600;">{t3}</span>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:center;padding-top:14px;border-top:1px solid {c['accent']}30;">
      <div style="display:flex;align-items:center;gap:6px;">
        <span style="color:{c['accent']};font-size:16px;">★★★★★</span>
        <span style="font-size:20px;font-weight:800;color:{c['text']};">{rating}</span>
        <span style="font-size:14px;color:{c['kicker_color']};opacity:0.8;">{reviews} تقييم</span>
      </div>
      <div style="display:flex;align-items:center;gap:12px;">
        {f'<span style="font-size:13px;color:{c["kicker_color"]};opacity:0.8;">✦ {trust}</span>' if trust else ''}
        <span style="font-size:13px;color:{c['kicker_color']};opacity:0.6;">{data.get('domain','nuhoot.xyz')}</span>
        <span style="font-size:13px;color:{c['kicker_color']};opacity:0.7;">{data.get('brand_ar','نُهوت')}</span>
      </div>
    </div>
  </div>
</div>""", c)


# ═══════════════════════════════════════════════════════
# REGISTRY
# ═══════════════════════════════════════════════════════
TEMPLATES = {
    1: ("Clean Hero", tpl_clean_hero),
    2: ("Full Bleed", tpl_full_bleed),
    3: ("Split", tpl_split),
    4: ("Gallery", tpl_gallery),
    5: ("Stats", tpl_stats),
}


def generate_html(template_id, photo_path, data, obj_pos="50% 50%", niche="restaurants", photo_paths=None):
    c = _get_colors(niche)
    b64 = _photo_b64(photo_path)
    photos_b64 = None
    if photo_paths:
        photos_b64 = [_photo_b64(p) for p in photo_paths[:2]]
    name, func = TEMPLATES[template_id]
    return func(b64, data, obj_pos, c, photos_b64)
