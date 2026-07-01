"""Industry-Specific Design Systems for Nuhoot.

6 completely different visual languages — one per industry group.
Each system has its own colors, backgrounds, typography, and layouts.
NO MORE dark+gold everywhere.

Systems:
1. WARM — restaurants, cafes, bakeries (cream bg, terracotta accent)
2. CLINICAL — clinics, dentists, pharmacies, dermatology (white bg, teal accent)
3. LUXURY — salons, spas, barbershops, fashion, perfumes (charcoal bg, rose gold)
4. CORPORATE — law_firms, real_estate, training_centers (navy bg, silver)
5. BOLD — gyms, auto_shops, car_wash, hvac_ac (black bg, electric lime/orange)
6. FRESH — cleaning, event_halls (light green bg, fresh green)
"""

import base64

_AR = "٠١٢٣٤٥٦٧٨٩"
_to_arabic = lambda s: "".join(_AR[int(c)] if c.isdigit() else c for c in str(s))

def _photo_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# ═══════════════════════════════════════════════════════
# DESIGN SYSTEM DEFINITIONS
# ═══════════════════════════════════════════════════════
SYSTEMS = {
    "warm": {
        "niches": ["restaurants", "cafes", "bakeries"],
        "bg": "#F5F0E8",
        "bg2": "#EBE0D0",
        "accent": "#B85C3C",
        "accent_light": "#D4805C",
        "accent_deep": "#8C3A1A",
        "text": "#3A2A1A",
        "text_light": "#6B5544",
        "white": "#FFFFFF",
        "font_head": "'AlYamama','Noto Kufi Arabic',serif",
        "font_body": "'Noto Sans Arabic',sans-serif",
        "card_bg": "rgba(255,255,255,0.85)",
    },
    "clinical": {
        "niches": ["clinics", "dentists", "pharmacies", "dermatology"],
        "bg": "#FAFCFE",
        "bg2": "#E8F4F8",
        "accent": "#2DB8A8",
        "accent_light": "#5DD8C8",
        "accent_deep": "#156B5E",
        "text": "#1E3A52",
        "text_light": "#5A7090",
        "white": "#FFFFFF",
        "font_head": "'AlYamama','Noto Kufi Arabic',serif",
        "font_body": "'Noto Sans Arabic',sans-serif",
        "card_bg": "rgba(255,255,255,0.9)",
    },
    "luxury": {
        "niches": ["salons", "spas", "barbershops", "fashion", "perfumes"],
        "bg": "#1A1A1E",
        "bg2": "#252528",
        "accent": "#D4737E",
        "accent_light": "#F5C2C8",
        "accent_deep": "#8C3A4A",
        "text": "#F5F0EC",
        "text_light": "#C9BFB8",
        "white": "#FFFFFF",
        "font_head": "'AlYamama','Noto Kufi Arabic',serif",
        "font_body": "'Noto Sans Arabic',sans-serif",
        "card_bg": "rgba(255,255,255,0.08)",
    },
    "corporate": {
        "niches": ["law_firms", "real_estate", "training_centers"],
        "bg": "#0E1428",
        "bg2": "#161E38",
        "accent": "#B8CCE0",
        "accent_light": "#D8E8F5",
        "accent_deep": "#4A7090",
        "text": "#E8EDF5",
        "text_light": "#8A9AB5",
        "white": "#FFFFFF",
        "font_head": "'AlYamama','Noto Kufi Arabic',serif",
        "font_body": "'Noto Sans Arabic',sans-serif",
        "card_bg": "rgba(255,255,255,0.06)",
    },
    "bold": {
        "niches": ["gyms", "auto_shops", "car_wash", "hvac_ac"],
        "bg": "#0A0A0A",
        "bg2": "#141414",
        "accent": "#FF6B35",
        "accent_light": "#FF9555",
        "accent_deep": "#CC4515",
        "text": "#FFFFFF",
        "text_light": "#AAAAAA",
        "white": "#FFFFFF",
        "font_head": "'AlYamama','Noto Kufi Arabic',serif",
        "font_body": "'Noto Sans Arabic',sans-serif",
        "card_bg": "rgba(0,0,0,0.7)",
    },
    "fresh": {
        "niches": ["cleaning", "event_halls"],
        "bg": "#F0F7F0",
        "bg2": "#E0EFE0",
        "accent": "#4CAF50",
        "accent_light": "#80C882",
        "accent_deep": "#2E7D32",
        "text": "#1B5E20",
        "text_light": "#4A6B4D",
        "white": "#FFFFFF",
        "font_head": "'AlYamama','Noto Kufi Arabic',serif",
        "font_body": "'Noto Sans Arabic',sans-serif",
        "card_bg": "rgba(255,255,255,0.85)",
    },
}


def get_system_for_niche(niche: str) -> str:
    """Return the system key for a given niche."""
    for sys_key, sys_data in SYSTEMS.items():
        if niche in sys_data["niches"]:
            return sys_key
    return "warm"  # fallback


def _build_css(s: dict) -> str:
    """Build CSS for a design system."""
    is_dark = s["bg"].startswith("#0") or s["bg"].startswith("#1A")
    text_on_photo = "#FFFFFF" if is_dark else s["text"]
    return f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1080px; overflow:hidden; background:{s['bg']};
  font-family:{s['font_body']}; -webkit-font-smoothing:antialiased; }}
.stage {{ position:relative; width:1080px; height:1080px; overflow:hidden; background:{s['bg']}; }}
.display {{ font-family:{s['font_head']}; font-weight:900; line-height:1.25; direction:rtl;
  word-break:keep-all; }}
.body-ar {{ font-family:{s['font_body']}; font-size:26px; line-height:1.7; direction:rtl;
  color:{text_on_photo}; word-break:keep-all; }}
.label {{ font-family:'Lato',sans-serif; font-size:16px; font-weight:600;
  letter-spacing:0.22em; text-transform:uppercase; color:{s['accent']}; }}
.eyebrow {{ font-family:{s['font_head']}; font-size:24px; font-weight:500;
  color:{s['accent_light']}; direction:rtl; }}
.accent-text {{ color:{s['accent']}; }}
.stars {{ color:{s['accent']}; }}
.gold-rule {{ height:2px; background:linear-gradient(90deg,transparent,{s['accent']},transparent); }}
.footer-url {{ font-family:'JetBrains Mono','Courier New',monospace; font-size:18px; color:{s['text_light']}; }}
.footer-brand {{ font-family:{s['font_body']}; font-size:20px; color:{s['accent_light']}; opacity:0.8; }}
"""


def _text_block_v2(data: dict, s: dict, align: str = "right") -> str:
    """Generate text block with system-specific colors."""
    t1, t2, t3 = data["taglines"]
    rating = data.get("rating", "٤٫٥")
    reviews = _to_arabic(data["reviews"])
    trust = data.get("trust_badge", "")
    trust_html = ""
    if trust:
        trust_html = f'<div style="font-size:17px;color:{s["accent_light"]};font-weight:600;direction:rtl;opacity:0.85;">✦ {trust}</div>'
    
    is_dark = s["bg"].startswith("#0") or s["bg"].startswith("#1A")
    headline_color = f"color:{s['accent']};" if not is_dark else f"color:{s['accent_light']};"
    
    return f"""
    <span class="eyebrow" style="white-space:nowrap;">{data['business_name']}</span>
    <h1 class="display" style="font-size:54px;text-align:{align};{headline_color}">{data['headline']}</h1>
    <div class="gold-rule" style="width:80px;"></div>
    <div class="body-ar" style="text-align:{align};">
      <div>{t1}</div><div>{t2}</div><div>{t3}</div>
    </div>
    <div style="display:flex;align-items:center;gap:12px;direction:rtl;" dir="rtl">
      <span class="stars" dir="ltr" style="font-size:24px;">★★★★<span style="color:rgba(255,255,255,0.2)">★</span></span>
      <span style="font-size:30px;font-weight:800;color:{s['white']};white-space:nowrap;">{rating}</span>
      <span style="font-size:20px;color:{s['text_light']};">{reviews} تقييم</span>
    </div>
    {trust_html}
    <div class="gold-rule" style="width:100%;opacity:0.4;"></div>
    <div style="display:flex;justify-content:space-between;align-items:baseline;width:100%;gap:16px;">
      <span class="footer-url" style="white-space:nowrap;">{data.get('domain','nuhoot.xyz')}</span>
      <span class="footer-brand" style="white-space:nowrap;">{data.get('brand_ar','نُهوت — التسويق الرقمي')}</span>
    </div>"""


def _wrap(body: str, s: dict) -> str:
    return f"""<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8">
<style>{_build_css(s)}</style></head><body>{body}</body></html>"""


# ═══════════════════════════════════════════════════════
# TEMPLATE 1: HERO SPLIT — photo left, text right
# ═══════════════════════════════════════════════════════
def tpl_hero_split(b64, data, obj_pos, s: dict, photos_b64=None):
    return _wrap(f"""<div class="stage" style="display:flex;flex-direction:row-reverse;">
  <div style="width:52%;height:100%;position:relative;overflow:hidden;">
    <img src="data:image/jpeg;base64,{b64}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};">
  </div>
  <div style="width:48%;height:100%;background:{s['bg2']};display:flex;flex-direction:column;
    justify-content:center;align-items:flex-end;gap:18px;padding:60px 50px;
    border-right:4px solid {s['accent']};">
    <span class="label">{data.get('kicker','')}</span>
    {_text_block_v2(data, s, 'right')}
  </div>
</div>""", s)


# ═══════════════════════════════════════════════════════
# TEMPLATE 2: FULL-BLEED — photo background, text bottom
# ═══════════════════════════════════════════════════════
def tpl_full_bleed(b64, data, obj_pos, s: dict, photos_b64=None):
    is_dark = s["bg"].startswith("#0") or s["bg"].startswith("#1A")
    overlay = "rgba(0,0,0,0.8)" if is_dark else f"rgba({int(s['bg'][1:3],16)},{int(s['bg'][3:5],16)},{int(s['bg'][5:7],16)},0.9)"
    return _wrap(f"""<div class="stage">
  <img src="data:image/jpeg;base64,{b64}" style="position:absolute;inset:0;width:100%;height:100%;
    object-fit:cover;object-position:{obj_pos};filter:brightness(0.7);">
  <div style="position:absolute;inset:0;background:linear-gradient(0deg,{overlay} 0%,rgba(0,0,0,0.5) 40%,transparent 70%);"></div>
  <div style="position:absolute;top:50px;right:50px;">
    <span class="label" style="text-shadow:0 2px 8px rgba(0,0,0,0.6);">{data.get('kicker','')}</span>
  </div>
  <div style="position:absolute;bottom:0;left:0;right:0;padding:50px 60px 45px;
    display:flex;flex-direction:column;gap:16px;align-items:flex-end;">
    {_text_block_v2(data, s, 'right')}
  </div>
</div>""", s)


# ═══════════════════════════════════════════════════════
# TEMPLATE 3: CARD FLOAT — photo bg, floating text card
# ═══════════════════════════════════════════════════════
def tpl_card_float(b64, data, obj_pos, s: dict, photos_b64=None):
    return _wrap(f"""<div class="stage">
  <img src="data:image/jpeg;base64,{b64}" style="position:absolute;inset:0;width:100%;height:100%;
    object-fit:cover;object-position:{obj_pos};filter:brightness(0.75);">
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse at center,transparent 30%,rgba(0,0,0,0.4) 80%);"></div>
  <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:760px;
    padding:48px 44px;background:{s['card_bg']};backdrop-filter:blur(20px);
    border:1px solid {s['accent']};border-radius:20px;
    box-shadow:0 20px 80px rgba(0,0,0,0.4);
    display:flex;flex-direction:column;gap:16px;align-items:center;text-align:center;">
    <span class="label">{data.get('kicker','')}</span>
    {_text_block_v2(data, s, 'center')}
  </div>
</div>""", s)


# ═══════════════════════════════════════════════════════
# TEMPLATE 4: MAGAZINE GRID — photo top, text bottom
# ═══════════════════════════════════════════════════════
def tpl_magazine(b64, data, obj_pos, s: dict, photos_b64=None):
    return _wrap(f"""<div class="stage" style="display:flex;flex-direction:column;">
  <div style="height:55%;overflow:hidden;position:relative;">
    <img src="data:image/jpeg;base64,{b64}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};">
    <div style="position:absolute;top:30px;right:30px;">
      <span class="label" style="text-shadow:0 2px 8px rgba(0,0,0,0.7);">{data.get('kicker','')}</span>
    </div>
  </div>
  <div style="flex:1;background:{s['bg2']};display:flex;flex-direction:column;
    justify-content:center;align-items:flex-end;gap:14px;padding:40px 50px;
    border-top:4px solid {s['accent']};">
    {_text_block_v2(data, s, 'right')}
  </div>
</div>""", s)


# ═══════════════════════════════════════════════════════
# TEMPLATE 5: SIDE PANEL — photo right, text left
# ═══════════════════════════════════════════════════════
def tpl_side_panel(b64, data, obj_pos, s: dict, photos_b64=None):
    return _wrap(f"""<div class="stage" style="display:flex;">
  <div style="width:45%;height:100%;background:{s['bg2']};display:flex;flex-direction:column;
    justify-content:center;align-items:flex-end;gap:18px;padding:60px 45px;
    border-left:4px solid {s['accent']};">
    <span class="label">{data.get('kicker','')}</span>
    {_text_block_v2(data, s, 'right')}
  </div>
  <div style="width:55%;height:100%;overflow:hidden;">
    <img src="data:image/jpeg;base64,{b64}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};">
  </div>
</div>""", s)


# ═══════════════════════════════════════════════════════
# TEMPLATE REGISTRY
# ═══════════════════════════════════════════════════════
TEMPLATES = {
    1: ("Hero Split", tpl_hero_split),
    2: ("Full Bleed", tpl_full_bleed),
    3: ("Card Float", tpl_card_float),
    4: ("Magazine", tpl_magazine),
    5: ("Side Panel", tpl_side_panel),
}


def generate_html(template_id: int, photo_path: str, data: dict,
                  obj_pos: str = "50% 50%", niche: str = "restaurants",
                  photo_paths: list = None) -> str:
    """Generate HTML using the industry-appropriate design system."""
    sys_key = get_system_for_niche(niche)
    s = SYSTEMS[sys_key]
    b64 = _photo_b64(photo_path)
    name, func = TEMPLATES[template_id]
    return func(b64, data, obj_pos, s)


# Registry compatible with old engine
DESIGN_SYSTEMS = {
    sys_key: {
        "name": sys_key.title(),
        "niches": data["niches"],
        "templates": TEMPLATES,
    }
    for sys_key, data in SYSTEMS.items()
}
