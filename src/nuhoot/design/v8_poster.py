"""Nuhoot v8 — POSTER STYLE. Not websites. Social media ADS.

Opus's fix applied:
- ABSOLUTE positioning (poster/ad style, NOT flexbox column = website)
- SOLID colors edge-to-edge (NO white backgrounds)
- Images FLOAT on color (NO cards, NO rounded borders, NO frames)
- HUGE typography (72px+ headlines, not 56px)
- NO navigation-looking elements
- Two variants: LIGHT (solid color + floating photo) and DARK (photo bg + gradient)
"""

import base64

_AR = "٠١٢٣٤٥٦٧٨٩"
_to_ar = lambda s: "".join(_AR[int(c)] if c.isdigit() else c for c in str(s))

def _photo_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# SOLID colors only — each niche gets ONE color
NICHE_COLORS = {
    "restaurants": {"bg": "#F5C518", "pill_bg": "#1a1a1a", "pill_text": "#FFD700", "text": "#1a1a1a", "kicker": "rgba(0,0,0,0.5)", "stars": "#1a1a1a", "is_dark": False},
    "cafes": {"bg": "#3e2723", "pill_bg": "#d7a86e", "pill_text": "#3e2723", "text": "#f5e6d3", "kicker": "#d7a86e", "stars": "#d7a86e", "is_dark": True},
    "bakeries": {"bg": "#FF8C42", "pill_bg": "#fff", "pill_text": "#3e2723", "text": "#fff", "kicker": "rgba(255,255,255,0.7)", "stars": "#fff", "is_dark": False},
    "salons": {"bg": "#1a1a2e", "pill_bg": "#e11d48", "pill_text": "#fff", "text": "#fff", "kicker": "#e11d48", "stars": "#e11d48", "is_dark": True},
    "spas": {"bg": "#1e3a32", "pill_bg": "#a8d5ba", "pill_text": "#1e3a32", "text": "#e8f5e9", "kicker": "#a8d5ba", "stars": "#a8d5ba", "is_dark": True},
    "barbershops": {"bg": "#0f0f0f", "pill_bg": "#d4af37", "pill_text": "#0f0f0f", "text": "#fff", "kicker": "#d4af37", "stars": "#d4af37", "is_dark": True},
    "gyms": {"bg": "#0D0D0D", "pill_bg": "#E85A25", "pill_text": "#fff", "text": "#fff", "kicker": "rgba(255,255,255,0.5)", "stars": "#E85A25", "is_dark": True},
    "clinics": {"bg": "#0d9488", "pill_bg": "#fff", "pill_text": "#0d9488", "text": "#fff", "kicker": "rgba(255,255,255,0.7)", "stars": "#fff", "is_dark": False},
    "dentists": {"bg": "#0c4a6e", "pill_bg": "#0ea5e9", "pill_text": "#0c4a6e", "text": "#fff", "kicker": "#0ea5e9", "stars": "#0ea5e9", "is_dark": True},
    "pharmacies": {"bg": "#0d9488", "pill_bg": "#fff", "pill_text": "#0d9488", "text": "#fff", "kicker": "rgba(255,255,255,0.7)", "stars": "#fff", "is_dark": False},
    "dermatology": {"bg": "#831843", "pill_bg": "#f9a8d4", "pill_text": "#831843", "text": "#fce7f3", "kicker": "#f9a8d4", "stars": "#f9a8d4", "is_dark": True},
    "fashion": {"bg": "#1a1a2e", "pill_bg": "#e11d48", "pill_text": "#fff", "text": "#fff", "kicker": "#e11d48", "stars": "#e11d48", "is_dark": True},
    "perfumes": {"bg": "#0f0f0f", "pill_bg": "#d4af37", "pill_text": "#0f0f0f", "text": "#fff", "kicker": "#d4af37", "stars": "#d4af37", "is_dark": True},
    "law_firms": {"bg": "#0f172a", "pill_bg": "#c9a227", "pill_text": "#0f172a", "text": "#e2e8f0", "kicker": "#c9a227", "stars": "#c9a227", "is_dark": True},
    "real_estate": {"bg": "#1c1917", "pill_bg": "#d4a574", "pill_text": "#1c1917", "text": "#f5f5f4", "kicker": "#d4a574", "stars": "#d4a574", "is_dark": True},
    "auto_shops": {"bg": "#171717", "pill_bg": "#dc2626", "pill_text": "#fff", "text": "#fff", "kicker": "#dc2626", "stars": "#dc2626", "is_dark": True},
    "car_wash": {"bg": "#0c1e2e", "pill_bg": "#38bdf8", "pill_text": "#0c1e2e", "text": "#fff", "kicker": "#38bdf8", "stars": "#38bdf8", "is_dark": True},
    "cleaning": {"bg": "#166534", "pill_bg": "#fff", "pill_text": "#166534", "text": "#fff", "kicker": "rgba(255,255,255,0.7)", "stars": "#fff", "is_dark": True},
    "hvac_ac": {"bg": "#0c1e2e", "pill_bg": "#38bdf8", "pill_text": "#0c1e2e", "text": "#fff", "kicker": "#38bdf8", "stars": "#38bdf8", "is_dark": True},
    "event_halls": {"bg": "#1c1510", "pill_bg": "#d4af37", "pill_text": "#1c1510", "text": "#fff", "kicker": "#d4af37", "stars": "#d4af37", "is_dark": True},
    "training_centers": {"bg": "#1e1b4b", "pill_bg": "#818cf8", "pill_text": "#1e1b4b", "text": "#e0e7ff", "kicker": "#818cf8", "stars": "#818cf8", "is_dark": True},
}

def _get_colors(niche):
    return NICHE_COLORS.get(niche, NICHE_COLORS["restaurants"])


# ═══════════════════════════════════════════════════════
# TEMPLATE 1: LIGHT POSTER — Solid color + floating photo
# Exactly Opus's restaurant reference: solid bg, floating image, pills, rating
# ═══════════════════════════════════════════════════════
def tpl_light_poster(b64, data, obj_pos, c, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    rating = data.get("rating", "٤٫٧")
    reviews = data.get("reviews_str", "٢٠٠")
    trust = data.get("trust_badge", "")
    kicker = data.get("kicker", "")
    headline = data["headline"]
    biz = data["business_name"]
    domain = data.get("domain", "nuhoot.xyz")
    brand = data.get("brand_ar", "نُهوت — التسويق الرقمي")
    
    # Text colors based on dark/light
    if c["is_dark"]:
        text_color = "#FFFFFF"
        kicker_color = c["kicker"]
    else:
        text_color = c["text"]
        kicker_color = c["kicker"]
    
    return f'''<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap" rel="stylesheet">
<style>*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:1080px;height:1080px;overflow:hidden;font-family:'Tajawal',sans-serif;}}
.ad{{width:1080px;height:1080px;background:{c['bg']};position:relative;overflow:hidden;direction:rtl;}}
.cat-label{{position:absolute;top:48px;left:48px;font-size:22px;font-weight:500;color:{kicker_color};letter-spacing:2px;}}
.headline{{position:absolute;top:90px;right:48px;font-size:68px;font-weight:900;color:{text_color};line-height:1.2;text-align:right;max-width:900px;}}
.biz-pill{{position:absolute;top:195px;right:48px;background:{c['pill_bg']};color:{c['pill_text']};padding:12px 32px;border-radius:50px;font-size:26px;font-weight:700;}}
.product-img{{position:absolute;top:280px;left:50%;transform:translateX(-50%);width:800px;height:450px;object-fit:cover;object-position:{obj_pos};filter:drop-shadow(0 20px 40px rgba(0,0,0,0.25));border-radius:12px;}}
.pills-row{{position:absolute;bottom:200px;right:48px;left:48px;display:flex;justify-content:flex-end;gap:14px;flex-wrap:wrap;}}
.feat-pill{{background:{c['pill_bg']};color:{c['pill_text']};padding:14px 26px;border-radius:50px;font-size:20px;font-weight:600;white-space:nowrap;}}
.rating-sec{{position:absolute;bottom:115px;right:48px;display:flex;align-items:center;gap:12px;}}
.rating-stars{{color:{c['stars']};font-size:26px;letter-spacing:2px;}}
.rating-num{{font-size:44px;font-weight:900;color:{text_color};}}
.rating-count{{font-size:22px;color:{kicker_color};margin-right:8px;}}
.google-text{{position:absolute;bottom:75px;right:48px;font-size:16px;color:{kicker_color};}}
.branding{{position:absolute;bottom:48px;left:48px;font-size:15px;color:{kicker_color};}}
.domain{{position:absolute;bottom:48px;right:48px;font-size:20px;font-weight:500;color:{kicker_color};font-family:monospace;}}
.trust-badge{{position:absolute;bottom:155px;left:48px;font-size:16px;color:{c['pill_bg']};font-weight:600;}}
</style></head><body>
<div class="ad">
  <div class="cat-label">{kicker}</div>
  <h1 class="headline">{headline}</h1>
  <div class="biz-pill">{biz}</div>
  <img class="product-img" src="data:image/jpeg;base64,{b64}">
  <div class="pills-row">
    <span class="feat-pill">{t1}</span>
    <span class="feat-pill">{t2}</span>
    <span class="feat-pill">{t3}</span>
  </div>
  <div class="rating-sec">
    <span class="rating-count">{reviews} تقييم</span>
    <span class="rating-stars">★★★★★</span>
    <span class="rating-num">{rating}</span>
  </div>
  <div class="google-text">↗ تقييم {rating} على خرائط جوجل</div>
  {f'<div class="trust-badge">✦ {trust}</div>' if trust else ''}
  <div class="branding">{brand}</div>
  <div class="domain">{domain}</div>
</div>
</body></html>'''


# ═══════════════════════════════════════════════════════
# TEMPLATE 2: DARK POSTER — Photo as bg + gradient overlay
# Exactly Opus's gym reference: dark bg image, gradient, text on top
# ═══════════════════════════════════════════════════════
def tpl_dark_poster(b64, data, obj_pos, c, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    rating = data.get("rating", "٤٫٧")
    reviews = data.get("reviews_str", "٢٠٠")
    trust = data.get("trust_badge", "")
    kicker = data.get("kicker", "")
    headline = data["headline"]
    biz = data["business_name"]
    domain = data.get("domain", "nuhoot.xyz")
    brand = data.get("brand_ar", "نُهوت — التسويق الرقمي")
    
    return f'''<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap" rel="stylesheet">
<style>*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:1080px;height:1080px;overflow:hidden;font-family:'Tajawal',sans-serif;}}
.ad{{width:1080px;height:1080px;background:{c['bg']};position:relative;overflow:hidden;direction:rtl;}}
.bg-img{{position:absolute;top:0;left:0;width:100%;height:65%;object-fit:cover;object-position:{obj_pos};opacity:0.5;}}
.gradient{{position:absolute;top:0;left:0;width:100%;height:100%;
  background:linear-gradient(to bottom,rgba(0,0,0,0.3) 0%,{c['bg']}dd 40%,{c['bg']} 60%);}}
.cat-label{{position:absolute;top:48px;left:48px;font-size:22px;font-weight:500;color:rgba(255,255,255,0.6);letter-spacing:2px;z-index:10;}}
.headline{{position:absolute;top:90px;right:48px;font-size:72px;font-weight:900;color:#fff;line-height:1.2;text-align:right;max-width:900px;z-index:10;text-shadow:0 4px 20px rgba(0,0,0,0.5);}}
.biz-pill{{position:absolute;top:210px;right:48px;background:{c['pill_bg']};color:{c['pill_text']};padding:14px 36px;border-radius:50px;font-size:26px;font-weight:700;z-index:10;}}
.pills-row{{position:absolute;bottom:210px;right:48px;left:48px;display:flex;justify-content:flex-end;gap:14px;flex-wrap:wrap;z-index:10;}}
.feat-pill{{background:{c['pill_bg']};color:{c['pill_text']};padding:16px 28px;border-radius:50px;font-size:20px;font-weight:600;white-space:nowrap;}}
.feat-pill.outline{{background:transparent;border:2px solid {c['pill_bg']};color:{c['pill_bg']};}}
.rating-sec{{position:absolute;bottom:125px;right:48px;display:flex;align-items:center;gap:12px;z-index:10;}}
.rating-stars{{color:{c['stars']};font-size:26px;letter-spacing:2px;}}
.rating-num{{font-size:44px;font-weight:900;color:#fff;}}
.rating-count{{font-size:22px;color:rgba(255,255,255,0.5);margin-right:8px;}}
.extra-info{{position:absolute;bottom:82px;right:48px;font-size:17px;color:{c['pill_bg']};z-index:10;}}
.branding{{position:absolute;bottom:48px;left:48px;font-size:15px;color:rgba(255,255,255,0.3);z-index:10;}}
.domain{{position:absolute;bottom:48px;right:48px;font-size:20px;font-weight:500;color:rgba(255,255,255,0.4);font-family:monospace;z-index:10;}}
</style></head><body>
<div class="ad">
  <img class="bg-img" src="data:image/jpeg;base64,{b64}">
  <div class="gradient"></div>
  <div class="cat-label">{kicker}</div>
  <h1 class="headline">{headline}</h1>
  <div class="biz-pill">{biz}</div>
  <div class="pills-row">
    <span class="feat-pill outline">{t1}</span>
    <span class="feat-pill">{t2}</span>
    <span class="feat-pill">{t3}</span>
  </div>
  <div class="rating-sec">
    <span class="rating-count">{reviews} تقييم</span>
    <span class="rating-stars">★★★★★</span>
    <span class="rating-num">{rating}</span>
  </div>
  {f'<div class="extra-info">✦ {trust}</div>' if trust else ''}
  <div class="branding">{brand}</div>
  <div class="domain">{domain}</div>
</div>
</body></html>'''


# ═══════════════════════════════════════════════════════
# TEMPLATE 3: SPLIT POSTER — Photo right half, color left half
# ═══════════════════════════════════════════════════════
def tpl_split_poster(b64, data, obj_pos, c, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    rating = data.get("rating", "٤٫٧")
    reviews = data.get("reviews_str", "٢٠٠")
    trust = data.get("trust_badge", "")
    kicker = data.get("kicker", "")
    headline = data["headline"]
    biz = data["business_name"]
    domain = data.get("domain", "nuhoot.xyz")
    brand = data.get("brand_ar", "نُهوت — التسويق الرقمي")
    
    text_color = "#FFFFFF" if c["is_dark"] else c["text"]
    
    return f'''<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap" rel="stylesheet">
<style>*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:1080px;height:1080px;overflow:hidden;font-family:'Tajawal',sans-serif;}}
.ad{{width:1080px;height:1080px;position:relative;overflow:hidden;direction:rtl;display:flex;}}
.left{{width:48%;height:100%;background:{c['bg']};display:flex;flex-direction:column;justify-content:center;padding:50px 40px;gap:24px;}}
.right{{width:52%;height:100%;overflow:hidden;}}
.right img{{width:100%;height:100%;object-fit:cover;object-position:{obj_pos};}}
.cat-label{{font-size:18px;font-weight:500;color:{c['kicker']};letter-spacing:2px;}}
.headline{{font-size:52px;font-weight:900;color:{text_color};line-height:1.2;text-align:right;}}
.biz-pill{{background:{c['pill_bg']};color:{c['pill_text']};padding:10px 28px;border-radius:50px;font-size:22px;font-weight:700;width:fit-content;}}
.divider{{width:60px;height:3px;background:{c['pill_bg']};border-radius:2px;}}
.pills-col{{display:flex;flex-direction:column;gap:10px;align-items:flex-end;}}
.feat-pill{{background:{c['pill_bg']};color:{c['pill_text']};padding:12px 24px;border-radius:50px;font-size:18px;font-weight:600;white-space:nowrap;}}
.rating{{display:flex;align-items:center;gap:10px;margin-top:8px;}}
.rating-stars{{color:{c['stars']};font-size:24px;}}
.rating-num{{font-size:36px;font-weight:900;color:{text_color};}}
.rating-count{{font-size:18px;color:{c['kicker']};}}
.footer{{position:absolute;bottom:30px;left:40px;right:40px;display:flex;justify-content:space-between;align-items:center;z-index:10;}}
.footer span{{font-size:14px;color:{c['kicker']};opacity:0.6;}}
</style></head><body>
<div class="ad">
  <div class="left">
    <span class="cat-label">{kicker}</span>
    <h1 class="headline">{headline}</h1>
    <div class="biz-pill">{biz}</div>
    <div class="divider"></div>
    <div class="pills-col">
      <span class="feat-pill">{t1}</span>
      <span class="feat-pill">{t2}</span>
      <span class="feat-pill">{t3}</span>
    </div>
    <div class="rating">
      <span class="rating-count">{reviews} تقييم</span>
      <span class="rating-stars">★★★★★</span>
      <span class="rating-num">{rating}</span>
    </div>
    {f'<div style="font-size:15px;color:{c["pill_bg"]};margin-top:4px;">✦ {trust}</div>' if trust else ''}
  </div>
  <div class="right">
    <img src="data:image/jpeg;base64,{b64}">
  </div>
  <div class="footer">
    <span>{brand}</span>
    <span>{domain}</span>
  </div>
</div>
</body></html>'''


# ═══════════════════════════════════════════════════════
# REGISTRY
# ═══════════════════════════════════════════════════════
TEMPLATES = {
    1: ("Light Poster", tpl_light_poster),
    2: ("Dark Poster", tpl_dark_poster),
    3: ("Split Poster", tpl_split_poster),
}

def generate_html(template_id, photo_path, data, obj_pos="50% 50%", niche="restaurants", photo_paths=None):
    c = _get_colors(niche)
    b64 = _photo_b64(photo_path)
    name, func = TEMPLATES[template_id]
    return func(b64, data, obj_pos, c)
