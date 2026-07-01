"""15-Template Engine v3 — Luxury Social Design System v4

Niche-aware: each design uses the accent colors of its niche.
T01-T10: Classic templates (fixed, niche-colored)
T11-T15: NEW bold jaw-dropping templates
T07: Fixed — uses 3 different photos instead of same 3x
"""

import base64

_AR = "٠١٢٣٤٥٦٧٨٩"
_to_arabic = lambda s: "".join(_AR[int(c)] if c.isdigit() else c for c in str(s))


def _photo_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _niche_css(colors: dict) -> str:
    """Generate CSS custom properties for niche-specific accent colors."""
    return f"""
:root {{
  --ink: #0C0A08; --espresso: {colors['bg']}; --coffee: {colors['bg2']};
  --accent-light: {colors['light']}; --accent-core: {colors['core']}; --accent-deep: {colors['deep']};
  --accent-glint: {colors['glint']}; --text: #FBF6EC; --muted: #C9BFA8;
  --accent-grad: {colors['grad']};
  --gold-light: {colors['light']}; --gold-core: {colors['core']}; --gold-deep: {colors['deep']};
  --gold-glint: {colors['glint']}; --gold-grad: {colors['grad']};
}}"""


_BASE_CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:1080px; height:1080px; overflow:hidden; background:var(--ink);
  font-family:'Noto Sans Arabic',sans-serif; -webkit-font-smoothing:antialiased; }
.stage { position:relative; width:1080px; height:1080px; overflow:hidden; }
.gold-text { background:var(--accent-grad); -webkit-background-clip:text; background-clip:text;
  -webkit-text-fill-color:transparent; filter:drop-shadow(0 3px 6px rgba(0,0,0,0.9)); }
.gold-rule { height:2px; background:linear-gradient(90deg,transparent,var(--accent-core),transparent); }
.label { font-family:'Lato'; font-size:16px; font-weight:600; letter-spacing:0.22em;
  text-transform:uppercase; color:var(--accent-light); }
.display { font-family:'AlYamama','Noto Kufi Arabic',serif; font-weight:900; line-height:1.2;
  direction:rtl; letter-spacing:0; }
.body-ar { font-family:'Noto Sans Arabic',sans-serif; font-size:27px; line-height:1.7;
  direction:rtl; letter-spacing:0; color:#FFFFFF; text-shadow:0 2px 8px rgba(0,0,0,0.7);
  word-spacing:-0.02em; }
.stars { color:var(--accent-light); text-shadow:0 0 10px rgba(201,162,90,0.3); }
.body-ar, .display { word-break:keep-all; overflow-wrap:normal; white-space:normal; hyphens:none; }
.body-ar { text-shadow:0 2px 6px rgba(0,0,0,0.8),0 4px 12px rgba(0,0,0,0.4); }
.footer-url { font-family:'JetBrains Mono','Courier New',monospace; font-size:18px; color:var(--muted); }
.footer-brand { font-family:'Noto Sans Arabic',sans-serif; font-size:20px; color:var(--accent-light); opacity:0.8; }
.eyebrow { font-family:'AlYamama','Noto Kufi Arabic',serif; font-size:24px; font-weight:500;
  color:var(--accent-light); direction:rtl; opacity:0.9; text-shadow:0 1px 4px rgba(0,0,0,0.6); }
.footer-url { font-family:'Lato'; font-size:23px; color:#C9BFA8; letter-spacing:0.14em; direction:ltr; }
.footer-brand { font-size:23px; color:var(--accent-light); }
.grain { position:absolute; inset:0; opacity:0.06; mix-blend-mode:overlay; pointer-events:none; z-index:9999; }
[dir="rtl"] { direction:rtl; unicode-bidi:isolate; }
"""

GRAIN_SVG = '<svg width="0" height="0"><filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter></svg>'


def _dynamic_headline_size(headline: str) -> int:
    """Claude Blueprint Rule 1: Golden ratio text sizing.
    Dynamically size headline based on length.
    """
    length = len(headline)
    if length <= 15:
        return 72  # Short = big impact
    if length <= 25:
        return 62  # Medium
    if length <= 35:
        return 54  # Long
    return 46  # Very long = smaller


def _dynamic_padding(taglines: list) -> tuple:
    """Claude Blueprint Rule 2: Luxury spacing based on content amount.
    Returns (container_padding, gap_between_elements)
    """
    total_chars = sum(len(t) for t in taglines)
    if total_chars < 80:
        return 80, 28  # Short content = more padding, more gap
    if total_chars < 150:
        return 70, 24  # Medium
    return 60, 20  # Long content = tighter spacing


def _text_block(data: dict, align: str = "right") -> str:
    t1, t2, t3 = data["taglines"]
    rating = data.get("rating", "٤٫٥")
    reviews = _to_arabic(data["reviews"])
    domain = data.get("domain", "nuhoot.xyz")
    brand = data.get("brand_ar", "نُهوت — التسويق الرقمي")
    trust = data.get("trust_badge", "")
    
    # Claude Blueprint: Dynamic headline sizing
    h_size = _dynamic_headline_size(data['headline'])
    # Claude Blueprint: Dynamic padding
    _pad, gap = _dynamic_padding(data["taglines"])

    # Trust badge element (small text below rating)
    trust_html = ""
    if trust:
        trust_html = f'<div style="font-size:18px;color:var(--accent-light);font-weight:600;direction:rtl;opacity:0.85;letter-spacing:0.02em;">✦ {trust}</div>'

    return f"""
    <span class="eyebrow" style="white-space:nowrap;unicode-bidi:isolate;">{data['business_name']}</span>
    <h1 class="display gold-text" style="font-size:{h_size}px;text-align:{align};">{data['headline']}</h1>
    <div class="gold-rule" style="width:72px;"></div>
    <div class="body-ar" style="text-align:{align};">
      <div>{t1}</div><div>{t2}</div><div>{t3}</div>
    </div>
    <div style="display:flex;align-items:center;gap:12px;direction:rtl;" dir="rtl">
      <span class="stars" dir="ltr" style="font-size:24px;">★★★★<span style="color:rgba(242,217,160,0.3)">★</span></span>
      <span style="font-size:30px;font-weight:700;color:#FFFFFF;direction:rtl;white-space:nowrap;text-shadow:0 2px 8px rgba(0,0,0,0.8);">{rating}</span>
      <span style="font-size:22px;color:#C9BFA8;">{reviews} تقييم</span>
    </div>
    {trust_html}
    <div class="gold-rule" style="width:100%;"></div>
    <div style="display:flex;justify-content:space-between;align-items:baseline;width:100%;gap:16px;flex-wrap:nowrap;">
      <span class="footer-url" style="white-space:nowrap;">{domain}</span>
      <span class="footer-brand" style="white-space:nowrap;font-size:20px;">{brand}</span>
    </div>"""


def _wrap(body: str, colors: dict) -> str:
    return f"""<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8">
<style>{_niche_css(colors)}{_BASE_CSS}</style></head><body>{body}</body></html>"""


# ═══════════════════════════════════════════════════════
# T01 — Vertical Split
# ═══════════════════════════════════════════════════════
def t01(b64, data, obj_pos, colors, photos_b64=None):
    return _wrap(f"""<div class="stage" style="display:flex;flex-direction:row-reverse;">
  <div style="width:50%;height:100%;position:relative;overflow:hidden;">
    <img src="data:image/jpeg;base64,{b64}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};">
  </div>
  <div style="width:50%;height:100%;background:var(--espresso);display:flex;flex-direction:column;
    justify-content:flex-end;align-items:flex-end;gap:20px;padding:70px 60px;border-left:3px solid var(--accent-core);">
    <span class="label">{data.get('kicker','RIYADH · FINE DINING')}</span>
    {_text_block(data, 'right')}
  </div>
  {GRAIN_SVG}<div class="grain" style="filter:url(#grain)"></div>
</div>""", colors)


# ═══════════════════════════════════════════════════════
# T02 — Gold Frame
# ═══════════════════════════════════════════════════════
def t02(b64, data, obj_pos, colors, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    rating = data.get("rating", "٤٫٥")
    reviews = _to_arabic(data["reviews"])
    trust = data.get("trust_badge", "")
    trust_html = ""
    if trust:
        trust_html = f'<div style="font-size:17px;color:var(--accent-light);font-weight:600;direction:rtl;opacity:0.85;">✦ {trust}</div>'
    h_size = _dynamic_headline_size(data['headline'])
    return _wrap(f"""<div class="stage" style="background:var(--espresso);">
  <!-- Large photo: 65% of canvas, full-width with gold frame -->
  <div style="position:absolute;top:0;left:0;right:0;height:650px;overflow:hidden;">
    <img src="data:image/jpeg;base64,{b64}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};">
    <!-- Gold border frame overlay -->
    <div style="position:absolute;inset:24px;border:3px solid var(--accent-core);border-radius:8px;
      pointer-events:none;box-shadow:0 0 30px rgba(201,162,90,0.15),inset 0 0 30px rgba(0,0,0,0.3);"></div>
    <!-- Gradient fade to text area -->
    <div style="position:absolute;bottom:0;left:0;right:0;height:180px;
      background:linear-gradient(0deg,var(--espresso) 0%,rgba(20,16,10,0.8) 50%,transparent 100%);"></div>
    <!-- Kicker on photo -->
    <div style="position:absolute;top:40px;right:40px;">
      <span class="label" style="text-shadow:0 2px 8px rgba(0,0,0,0.8);">{data.get('kicker','RIYADH · FINE DINING')}</span>
    </div>
  </div>
  <!-- Text panel bottom -->
  <div style="position:absolute;bottom:0;left:0;right:0;padding:0 50px 45px;display:flex;flex-direction:column;
    gap:14px;align-items:flex-end;">
    <span class="eyebrow" style="font-size:26px;">{data['business_name']}</span>
    <h1 class="display gold-text" style="font-size:{h_size}px;text-align:right;line-height:1.2;">{data['headline']}</h1>
    <div class="gold-rule" style="width:100px;"></div>
    <div class="body-ar" style="text-align:right;font-size:24px;">
      <div>{t1}</div><div>{t2}</div><div>{t3}</div>
    </div>
    <div style="display:flex;align-items:center;gap:14px;direction:rtl;" dir="rtl">
      <span class="stars" dir="ltr" style="font-size:24px;">★★★★<span style="color:rgba(242,217,160,0.3)">★</span></span>
      <span style="font-size:32px;font-weight:800;color:#FFF;white-space:nowrap;text-shadow:0 2px 8px rgba(0,0,0,0.8);">{rating}</span>
      <span style="font-size:20px;color:#C9BFA8;">{reviews} تقييم</span>
    </div>
    {trust_html}
    <div class="gold-rule" style="width:100%;opacity:0.5;"></div>
    <div style="display:flex;justify-content:space-between;width:100%;gap:16px;">
      <span class="footer-url" style="white-space:nowrap;">{data.get('domain','nuhoot.xyz')}</span>
      <span class="footer-brand" style="white-space:nowrap;font-size:20px;">{data.get('brand_ar','نُهوت — التسويق الرقمي')}</span>
    </div>
  </div>
  {GRAIN_SVG}<div class="grain" style="filter:url(#grain)"></div>
</div>""", colors)


# ═══════════════════════════════════════════════════════
# T03 — Gold Ring (formerly Circle Frame — redesigned: no circle crop)
# Full-bleed photo with elegant gold ring accent, text in bottom panel
# ═══════════════════════════════════════════════════════
def t03(b64, data, obj_pos, colors, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    rating = data.get("rating", "٤٫٥")
    reviews = _to_arabic(data["reviews"])
    trust = data.get("trust_badge", "")
    trust_html = ""
    if trust:
        trust_html = f'<div style="font-size:17px;color:var(--accent-light);font-weight:600;direction:rtl;opacity:0.85;">✦ {trust}</div>'
    h_size = _dynamic_headline_size(data['headline'])
    return _wrap(f"""<div class="stage" style="background:var(--ink);">
  <!-- Full-bleed photo -->
  <img src="data:image/jpeg;base64,{b64}" style="position:absolute;inset:0;width:100%;height:100%;
    object-fit:cover;object-position:{obj_pos};filter:brightness(0.72) contrast(1.08);">
  <!-- Vignette -->
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 40%,transparent 30%,rgba(0,0,0,0.4) 70%,rgba(0,0,0,0.7) 100%);"></div>
  <!-- Gold ring accent (decorative, not cropping) -->
  <div style="position:absolute;top:100px;left:50%;transform:translateX(-50%);
    width:280px;height:280px;border-radius:50%;border:2px solid var(--accent-core);
    opacity:0.35;box-shadow:0 0 40px rgba(201,162,90,0.15),inset 0 0 40px rgba(201,162,90,0.1);
    pointer-events:none;"></div>
  <!-- Inner ring -->
  <div style="position:absolute;top:130px;left:50%;transform:translateX(-50%);
    width:220px;height:220px;border-radius:50%;border:1px solid var(--accent-light);
    opacity:0.2;pointer-events:none;"></div>
  <!-- Kicker top -->
  <div style="position:absolute;top:60px;left:0;right:0;text-align:center;">
    <span class="label" style="text-shadow:0 2px 8px rgba(0,0,0,0.8);">{data.get('kicker','RIYADH · FINE DINING')}</span>
  </div>
  <!-- Business name inside ring -->
  <div style="position:absolute;top:195px;left:0;right:0;text-align:center;">
    <span class="eyebrow" style="font-size:24px;text-shadow:0 2px 8px rgba(0,0,0,0.9);">{data['business_name']}</span>
  </div>
  <!-- Bottom text panel -->
  <div style="position:absolute;bottom:0;left:0;right:0;padding:50px 60px 45px;
    background:linear-gradient(0deg,var(--ink) 0%,var(--ink) 50%,rgba(12,10,8,0.9) 75%,transparent 100%);
    display:flex;flex-direction:column;gap:16px;align-items:center;text-align:center;">
    <h1 class="display gold-text" style="font-size:{h_size}px;text-align:center;line-height:1.25;">{data['headline']}</h1>
    <div class="gold-rule" style="width:120px;"></div>
    <div class="body-ar" style="text-align:center;font-size:24px;">
      <div>{t1}</div><div>{t2}</div><div>{t3}</div>
    </div>
    <div style="display:flex;align-items:center;gap:14px;direction:rtl;" dir="rtl">
      <span class="stars" dir="ltr" style="font-size:24px;">★★★★<span style="color:rgba(242,217,160,0.3)">★</span></span>
      <span style="font-size:32px;font-weight:800;color:#FFF;white-space:nowrap;text-shadow:0 2px 8px rgba(0,0,0,0.8);">{rating}</span>
      <span style="font-size:20px;color:#C9BFA8;">{reviews} تقييم</span>
    </div>
    {trust_html}
    <div class="gold-rule" style="width:100%;opacity:0.5;"></div>
    <div style="display:flex;justify-content:space-between;width:100%;gap:16px;">
      <span class="footer-url" style="white-space:nowrap;">{data.get('domain','nuhoot.xyz')}</span>
      <span class="footer-brand" style="white-space:nowrap;font-size:20px;">{data.get('brand_ar','نُهوت — التسويق الرقمي')}</span>
    </div>
  </div>
  {GRAIN_SVG}<div class="grain" style="filter:url(#grain)"></div>
</div>""", colors)


# ═══════════════════════════════════════════════════════
# T04 — Bottom Band
# ═══════════════════════════════════════════════════════
def t04(b64, data, obj_pos, colors, photos_b64=None):
    return _wrap(f"""<div class="stage">
  <div style="position:absolute;inset:0;overflow:hidden;">
    <img src="data:image/jpeg;base64,{b64}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};">
  </div>
  <div style="position:absolute;bottom:0;left:0;right:0;height:560px;
    background:linear-gradient(0deg,
      var(--ink) 0%, var(--ink) 50%,
      rgba(12,10,8,0.92) 65%, rgba(12,10,8,0.45) 82%,
      rgba(12,10,8,0.15) 93%, transparent 100%);
    backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);
    display:flex;flex-direction:column;justify-content:flex-end;align-items:flex-end;gap:16px;
    padding:40px 60px 40px;">
    <span class="label" style="align-self:flex-end;">{data.get('kicker','RIYADH · FINE DINING')}</span>
    {_text_block(data, 'right')}
  </div>
  {GRAIN_SVG}<div class="grain" style="filter:url(#grain)"></div>
</div>""", colors)


# ═══════════════════════════════════════════════════════
# T05 — Arch Window
# ═══════════════════════════════════════════════════════
def t05(b64, data, obj_pos, colors, photos_b64=None):
    return _wrap(f"""<div class="stage" style="display:flex;flex-direction:row-reverse;align-items:center;">
  <div style="width:48%;height:88%;margin:0 50px;border-radius:240px 240px 20px 20px;overflow:hidden;
    border:5px solid var(--accent-core);box-shadow:0 20px 60px rgba(0,0,0,0.5);">
    <img src="data:image/jpeg;base64,{b64}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};">
  </div>
  <div style="width:44%;height:100%;display:flex;flex-direction:column;justify-content:center;
    align-items:flex-end;gap:24px;padding:0 50px;">
    <span class="label">{data.get('kicker','RIYADH · FINE DINING')}</span>
    {_text_block(data, 'right')}
  </div>
  {GRAIN_SVG}<div class="grain" style="filter:url(#grain)"></div>
</div>""", colors)


# ═══════════════════════════════════════════════════════
# T06 — Magazine Sidebar
# ═══════════════════════════════════════════════════════
def t06(b64, data, obj_pos, colors, photos_b64=None):
    return _wrap(f"""<div class="stage" style="display:flex;flex-direction:row-reverse;">
  <div style="width:35%;height:100%;overflow:hidden;border-left:3px solid var(--accent-core);">
    <img src="data:image/jpeg;base64,{b64}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};">
  </div>
  <div style="width:65%;height:100%;background:var(--espresso);display:flex;flex-direction:column;
    justify-content:center;align-items:flex-end;gap:20px;padding:70px 60px;">
    <span class="label">{data.get('kicker','RIYADH · FINE DINING')}</span>
    {_text_block(data, 'right')}
  </div>
  {GRAIN_SVG}<div class="grain" style="filter:url(#grain)"></div>
</div>""", colors)


# ═══════════════════════════════════════════════════════
# T07 — Triple Strip (FIXED: uses 3 different photos)
# ═══════════════════════════════════════════════════════
def t07(b64, data, obj_pos, colors, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    rating = data.get("rating", "٤٫٥")
    reviews = _to_arabic(data["reviews"])
    trust = data.get("trust_badge", "")
    trust_html = ""
    if trust:
        trust_html = f'<div style="font-size:17px;color:var(--accent-light);font-weight:600;direction:rtl;opacity:0.85;">✦ {trust}</div>'
    h_size = _dynamic_headline_size(data['headline'])
    p1 = photos_b64[0] if photos_b64 and len(photos_b64) > 0 else b64
    p2 = photos_b64[1] if photos_b64 and len(photos_b64) > 1 else b64
    p3 = photos_b64[2] if photos_b64 and len(photos_b64) > 2 else b64
    return _wrap(f"""<div class="stage" style="background:var(--espresso);">
  <!-- Top: 3 photos as horizontal strip -->
  <div style="position:absolute;top:0;left:0;right:0;height:520px;display:flex;overflow:hidden;">
    <div style="flex:1;overflow:hidden;border-right:2px solid var(--accent-core);">
      <img src="data:image/jpeg;base64,{p1}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};">
    </div>
    <div style="flex:1;overflow:hidden;border-right:2px solid var(--accent-core);">
      <img src="data:image/jpeg;base64,{p2}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};filter:brightness(0.85);">
    </div>
    <div style="flex:1;overflow:hidden;">
      <img src="data:image/jpeg;base64,{p3}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};filter:brightness(0.92);">
    </div>
  </div>
  <!-- Gradient transition -->
  <div style="position:absolute;top:440px;left:0;right:0;height:120px;
    background:linear-gradient(0deg,var(--espresso) 0%,rgba(20,16,10,0.6) 50%,transparent 100%);"></div>
  <!-- Bottom: text panel -->
  <div style="position:absolute;bottom:0;left:0;right:0;padding:30px 60px 40px;
    display:flex;flex-direction:column;gap:14px;align-items:flex-end;text-align:right;">
    <div style="display:flex;justify-content:space-between;width:100%;align-items:center;">
      <span class="label">{data.get('kicker','RIYADH · FINE DINING')}</span>
      <span class="eyebrow" style="font-size:24px;">{data['business_name']}</span>
    </div>
    <h1 class="display gold-text" style="font-size:{h_size}px;text-align:right;line-height:1.2;">{data['headline']}</h1>
    <div class="gold-rule" style="width:100px;"></div>
    <div class="body-ar" style="text-align:right;font-size:24px;">
      <div>{t1}</div><div>{t2}</div><div>{t3}</div>
    </div>
    <div style="display:flex;align-items:center;gap:14px;direction:rtl;" dir="rtl">
      <span class="stars" dir="ltr" style="font-size:24px;">★★★★<span style="color:rgba(242,217,160,0.3)">★</span></span>
      <span style="font-size:30px;font-weight:800;color:#FFF;white-space:nowrap;text-shadow:0 2px 8px rgba(0,0,0,0.8);">{rating}</span>
      <span style="font-size:20px;color:#C9BFA8;">{reviews} تقييم</span>
    </div>
    {trust_html}
    <div class="gold-rule" style="width:100%;opacity:0.5;"></div>
    <div style="display:flex;justify-content:space-between;width:100%;gap:16px;">
      <span class="footer-url" style="white-space:nowrap;">{data.get('domain','nuhoot.xyz')}</span>
      <span class="footer-brand" style="white-space:nowrap;font-size:20px;">{data.get('brand_ar','نُهوت — التسويق الرقمي')}</span>
    </div>
  </div>
  {GRAIN_SVG}<div class="grain" style="filter:url(#grain)"></div>
</div>""", colors)


def t08(b64, data, obj_pos, colors, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    rating = data.get("rating", "٤٫٥")
    reviews = _to_arabic(data["reviews"])
    trust = data.get("trust_badge", "")
    trust_html = ""
    if trust:
        trust_html = f'<div style="font-size:17px;color:var(--accent-light);font-weight:600;direction:rtl;opacity:0.85;">✦ {trust}</div>'
    h_size = _dynamic_headline_size(data['headline'])
    return _wrap(f"""<div class="stage" style="background:var(--espresso);">
  <!-- Left: Photo in arch frame -->
  <div style="position:absolute;top:80px;left:50px;width:480px;height:920px;
    border-radius:240px 240px 12px 12px;overflow:hidden;
    border:2px solid var(--accent-core);box-shadow:0 20px 60px rgba(0,0,0,0.5);">
    <img src="data:image/jpeg;base64,{b64}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};">
    <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0.2) 0%,transparent 30%,transparent 70%,rgba(0,0,0,0.3) 100%);"></div>
  </div>
  <!-- Right: Text panel -->
  <div style="position:absolute;top:0;right:0;width:520px;height:100%;
    display:flex;flex-direction:column;justify-content:center;gap:18px;
    align-items:flex-end;padding:60px 50px;text-align:right;">
    <span class="label">{data.get('kicker','RIYADH · FINE DINING')}</span>
    <span class="eyebrow" style="font-size:26px;">{data['business_name']}</span>
    <h1 class="display gold-text" style="font-size:{h_size}px;text-align:right;line-height:1.25;">{data['headline']}</h1>
    <div class="gold-rule" style="width:100px;"></div>
    <div class="body-ar" style="text-align:right;font-size:24px;">
      <div>{t1}</div><div>{t2}</div><div>{t3}</div>
    </div>
    <div style="display:flex;align-items:center;gap:14px;direction:rtl;" dir="rtl">
      <span class="stars" dir="ltr" style="font-size:24px;">★★★★<span style="color:rgba(242,217,160,0.3)">★</span></span>
      <span style="font-size:32px;font-weight:800;color:#FFF;white-space:nowrap;text-shadow:0 2px 8px rgba(0,0,0,0.8);">{rating}</span>
      <span style="font-size:20px;color:#C9BFA8;">{reviews} تقييم</span>
    </div>
    {trust_html}
    <div class="gold-rule" style="width:100%;opacity:0.4;"></div>
    <div style="display:flex;justify-content:space-between;width:100%;gap:16px;">
      <span class="footer-url" style="white-space:nowrap;">{data.get('domain','nuhoot.xyz')}</span>
      <span class="footer-brand" style="white-space:nowrap;font-size:18px;">{data.get('brand_ar','نُهوت — التسويق الرقمي')}</span>
    </div>
  </div>
  {GRAIN_SVG}<div class="grain" style="filter:url(#grain)"></div>
</div>""", colors)


# ═══════════════════════════════════════════════════════
# T09 — Duotone Split
# ═══════════════════════════════════════════════════════
def t09(b64, data, obj_pos, colors, photos_b64=None):
    return _wrap(f"""<div class="stage" style="display:flex;flex-direction:row-reverse;">
  <div style="width:55%;height:100%;position:relative;overflow:hidden;">
    <img src="data:image/jpeg;base64,{b64}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};
      filter:sepia(0.3) saturate(1.2) brightness(0.9);">
    <div style="position:absolute;inset:0;background:linear-gradient(135deg,rgba(140,106,46,0.25),rgba(12,10,8,0.15));
      mix-blend-mode:overlay;"></div>
  </div>
  <div style="width:45%;height:100%;background:var(--espresso);display:flex;flex-direction:column;
    justify-content:flex-end;align-items:flex-end;gap:20px;padding:70px 50px;border-left:3px solid var(--accent-core);">
    <span class="label">{data.get('kicker','RIYADH · FINE DINING')}</span>
    {_text_block(data, 'right')}
  </div>
  {GRAIN_SVG}<div class="grain" style="filter:url(#grain)"></div>
</div>""", colors)


# ═══════════════════════════════════════════════════════
# T10 — Framed Float
# ═══════════════════════════════════════════════════════
def t10(b64, data, obj_pos, colors, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    rating = data.get("rating", "٤٫٥")
    reviews = _to_arabic(data["reviews"])
    trust = data.get("trust_badge", "")
    trust_html = ""
    if trust:
        trust_html = f'<div style="font-size:17px;color:var(--accent-light);font-weight:600;direction:rtl;opacity:0.85;">✦ {trust}</div>'
    h_size = _dynamic_headline_size(data['headline'])
    return _wrap(f"""<div class="stage">
  <img src="data:image/jpeg;base64,{b64}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{obj_pos};filter:brightness(0.72);">
  <div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,0.85) 0%,rgba(0,0,0,0.3) 50%,transparent 70%);"></div>
  <!-- Top: kicker -->
  <div style="position:absolute;top:50px;left:0;right:0;text-align:center;">
    <span class="label" style="text-shadow:0 2px 8px rgba(0,0,0,0.9);">{data.get('kicker','RIYADH · FINE DINING')}</span>
  </div>
  <!-- Bottom: large floating card -->
  <div style="position:absolute;bottom:0;left:0;right:0;width:100%;padding:50px 60px 45px;
    background:linear-gradient(0deg,var(--ink) 0%,rgba(12,10,8,0.95) 60%,rgba(12,10,8,0.7) 85%,transparent 100%);
    display:flex;flex-direction:column;gap:16px;align-items:flex-end;text-align:right;">
    <span class="eyebrow" style="font-size:26px;">{data['business_name']}</span>
    <h1 class="display gold-text" style="font-size:{h_size}px;text-align:right;line-height:1.2;">{data['headline']}</h1>
    <div class="gold-rule" style="width:120px;"></div>
    <div class="body-ar" style="text-align:right;font-size:24px;">
      <div>{t1}</div><div>{t2}</div><div>{t3}</div>
    </div>
    <div style="display:flex;align-items:center;gap:14px;direction:rtl;" dir="rtl">
      <span class="stars" dir="ltr" style="font-size:24px;">★★★★<span style="color:rgba(242,217,160,0.3)">★</span></span>
      <span style="font-size:30px;font-weight:800;color:#FFF;white-space:nowrap;text-shadow:0 2px 8px rgba(0,0,0,0.8);">{rating}</span>
      <span style="font-size:20px;color:#C9BFA8;">{reviews} تقييم</span>
    </div>
    {trust_html}
    <div class="gold-rule" style="width:100%;opacity:0.5;"></div>
    <div style="display:flex;justify-content:space-between;width:100%;gap:16px;">
      <span class="footer-url" style="white-space:nowrap;">{data.get('domain','nuhoot.xyz')}</span>
      <span class="footer-brand" style="white-space:nowrap;font-size:20px;">{data.get('brand_ar','نُهوت — التسويق الرقمي')}</span>
    </div>
  </div>
  {GRAIN_SVG}<div class="grain" style="filter:url(#grain)"></div>
</div>""", colors)


def t11(b64, data, obj_pos, colors, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    rating = data.get("rating", "٤٫٥")
    reviews = _to_arabic(data["reviews"])
    trust = data.get("trust_badge", "")
    trust_html = ""
    if trust:
        trust_html = f'<div style="font-size:18px;color:var(--accent-light);font-weight:600;direction:rtl;opacity:0.85;letter-spacing:0.02em;">✦ {trust}</div>'
    h_size = _dynamic_headline_size(data['headline'])
    return _wrap(f"""<div class="stage">
  <img src="data:image/jpeg;base64,{b64}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{obj_pos};filter:brightness(0.62) contrast(1.12) saturate(1.05);">
  <!-- Vignette + gradient bottom -->
  <div style="position:absolute;inset:0;background:
    radial-gradient(ellipse at center,transparent 25%,rgba(0,0,0,0.5) 75%,rgba(0,0,0,0.85) 100%);"></div>
  <!-- Solid dark panel behind text for contrast -->
  <div style="position:absolute;bottom:0;left:0;right:0;height:600px;
    background:linear-gradient(0deg,var(--ink) 0%,var(--ink) 45%,rgba(12,10,8,0.95) 70%,rgba(12,10,8,0.6) 88%,transparent 100%);"></div>
  <!-- Content bottom-right -->
  <div style="position:absolute;bottom:0;left:0;right:0;padding:60px 70px 50px;display:flex;flex-direction:column;gap:22px;align-items:flex-end;">
    <span class="label" style="text-shadow:0 2px 10px rgba(0,0,0,0.9);">{data.get('kicker','RIYADH · FINE DINING')}</span>
    <span class="eyebrow" style="font-size:28px;">{data['business_name']}</span>
    <h1 class="display gold-text" style="font-size:{h_size}px;text-align:right;line-height:1.25;">{data['headline']}</h1>
    <div class="gold-rule" style="width:120px;"></div>
    <div class="body-ar" style="text-align:right;font-size:26px;">
      <div>{t1}</div><div>{t2}</div><div>{t3}</div>
    </div>
    <div style="display:flex;align-items:center;gap:16px;direction:rtl;" dir="rtl">
      <span class="stars" dir="ltr" style="font-size:28px;">★★★★<span style="color:rgba(255,255,255,0.25)">★</span></span>
      <span style="font-size:36px;font-weight:800;color:#FFF;white-space:nowrap;text-shadow:0 2px 10px rgba(0,0,0,0.9);">{rating}</span>
      <span style="font-size:22px;color:rgba(255,255,255,0.75);">{reviews} تقييم</span>
    </div>
    {trust_html}
    <div class="gold-rule" style="width:100%;opacity:0.5;"></div>
    <div style="display:flex;justify-content:space-between;width:100%;gap:16px;">
      <span class="footer-url" style="white-space:nowrap;">{data.get('domain','nuhoot.xyz')}</span>
      <span class="footer-brand" style="white-space:nowrap;font-size:20px;">{data.get('brand_ar','نُهوت — التسويق الرقمي')}</span>
    </div>
  </div>
  {GRAIN_SVG}<div class="grain" style="filter:url(#grain)"></div>
</div>""", colors)


# ═══════════════════════════════════════════════════════
# T12 — GLASS MORPHISM (NEW — modern frosted glass)
# Photo with large frosted glass panel, accent glow
# ═══════════════════════════════════════════════════════
def t12(b64, data, obj_pos, colors, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    rating = data.get("rating", "٤٫٥")
    reviews = _to_arabic(data["reviews"])
    trust = data.get("trust_badge", "")
    trust_html = ""
    if trust:
        trust_html = f'<div style="font-size:18px;color:var(--accent-light);font-weight:600;direction:rtl;opacity:0.85;letter-spacing:0.02em;">✦ {trust}</div>'
    return _wrap(f"""<div class="stage">
  <img src="data:image/jpeg;base64,{b64}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{obj_pos};filter:brightness(0.6);">
  <!-- Accent glow halo -->
  <div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 45%,{colors['core']}15 0%,transparent 50%);"></div>
  <!-- Glass panel — dark for contrast -->
  <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:760px;padding:52px 44px;
    background:rgba(0,0,0,0.55);backdrop-filter:blur(20px) saturate(1.3);-webkit-backdrop-filter:blur(20px) saturate(1.3);
    border:1px solid var(--accent-core);border-radius:24px;box-shadow:0 20px 80px rgba(0,0,0,0.6),0 0 40px rgba(201,162,90,0.1),inset 0 1px 0 rgba(255,255,255,0.08);
    display:flex;flex-direction:column;gap:20px;align-items:center;text-align:center;">
    <span class="label">{data.get('kicker','RIYADH · FINE DINING')}</span>
    <span class="eyebrow">{data['business_name']}</span>
    <h1 class="display gold-text" style="font-size:56px;text-align:center;line-height:1.25;">{data['headline']}</h1>
    <div class="gold-rule" style="width:100px;"></div>
    <div class="body-ar" style="text-align:center;font-size:24px;">
      <div>{t1}</div><div>{t2}</div><div>{t3}</div>
    </div>
    <div style="display:flex;align-items:center;gap:14px;direction:rtl;" dir="rtl">
      <span class="stars" dir="ltr" style="font-size:22px;">★★★★<span style="color:rgba(255,255,255,0.2)">★</span></span>
      <span style="font-size:28px;font-weight:700;color:#FFF;white-space:nowrap;">{rating}</span>
      <span style="font-size:20px;color:rgba(255,255,255,0.6);">{reviews} تقييم</span>
    </div>
    {trust_html}
    <div class="gold-rule" style="width:100%;opacity:0.3;"></div>
    <div style="display:flex;justify-content:space-between;width:100%;gap:16px;">
      <span class="footer-url" style="white-space:nowrap;">{data.get('domain','nuhoot.xyz')}</span>
      <span class="footer-brand" style="white-space:nowrap;font-size:18px;">{data.get('brand_ar','نُهوت — التسويق الرقمي')}</span>
    </div>
  </div>
  {GRAIN_SVG}<div class="grain" style="filter:url(#grain)"></div>
</div>""", colors)


# ═══════════════════════════════════════════════════════
# T13 — DIAGONAL SPLIT (NEW — bold asymmetric)
# Photo clipped diagonally, text on colored panel
# ═══════════════════════════════════════════════════════
def t13(b64, data, obj_pos, colors, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    rating = data.get("rating", "٤٫٥")
    reviews = _to_arabic(data["reviews"])
    trust = data.get("trust_badge", "")
    trust_html = ""
    if trust:
        trust_html = f'<div style="font-size:18px;color:var(--accent-light);font-weight:600;direction:rtl;opacity:0.85;letter-spacing:0.02em;">✦ {trust}</div>'
    h_size = _dynamic_headline_size(data['headline'])
    return _wrap(f"""<div class="stage" style="background:var(--espresso);">
  <!-- Diagonal photo clip -->
  <div style="position:absolute;inset:0;overflow:hidden;clip-path:polygon(0 0,100% 0,100% 75%,0 100%);">
    <img src="data:image/jpeg;base64,{b64}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};filter:brightness(0.85) contrast(1.05);">
  </div>
  <!-- Accent line at split -->
  <div style="position:absolute;top:75%;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--accent-core),transparent);opacity:0.6;"></div>
  <!-- Text panel bottom -->
  <div style="position:absolute;bottom:0;left:0;right:0;padding:50px 70px 45px;display:flex;flex-direction:column;gap:18px;align-items:flex-end;
    background:linear-gradient(0deg,var(--ink) 60%,rgba(12,10,8,0.85) 85%,transparent 100%);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);">
    <span class="label">{data.get('kicker','RIYADH · FINE DINING')}</span>
    <span class="eyebrow">{data['business_name']}</span>
    <h1 class="display gold-text" style="font-size:{h_size}px;text-align:right;line-height:1.25;">{data['headline']}</h1>
    <div class="gold-rule" style="width:80px;"></div>
    <div class="body-ar" style="text-align:right;font-size:25px;">
      <div>{t1}</div><div>{t2}</div><div>{t3}</div>
    </div>
    <div style="display:flex;align-items:center;gap:12px;direction:rtl;" dir="rtl">
      <span class="stars" dir="ltr" style="font-size:22px;">★★★★<span style="color:rgba(255,255,255,0.25)">★</span></span>
      <span style="font-size:28px;font-weight:700;color:#FFF;white-space:nowrap;">{rating}</span>
      <span style="font-size:20px;color:#C9BFA8;">{reviews} تقييم</span>
    </div>
    {trust_html}
    <div class="gold-rule" style="width:100%;"></div>
    <div style="display:flex;justify-content:space-between;width:100%;gap:16px;">
      <span class="footer-url" style="white-space:nowrap;">{data.get('domain','nuhoot.xyz')}</span>
      <span class="footer-brand" style="white-space:nowrap;font-size:20px;">{data.get('brand_ar','نُهوت — التسويق الرقمي')}</span>
    </div>
  </div>
  {GRAIN_SVG}<div class="grain" style="filter:url(#grain)"></div>
</div>""", colors)


# ═══════════════════════════════════════════════════════
# T14 — MAGAZINE COVER (NEW — editorial bold typography)
# Huge headline dominating, small photo inset
# ═══════════════════════════════════════════════════════
def t14(b64, data, obj_pos, colors, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    rating = data.get("rating", "٤٫٥")
    reviews = _to_arabic(data["reviews"])
    trust = data.get("trust_badge", "")
    trust_html = ""
    if trust:
        trust_html = f'<div style="font-size:17px;color:var(--accent-light);font-weight:600;direction:rtl;opacity:0.85;">✦ {trust}</div>'
    h_size = _dynamic_headline_size(data['headline'])
    return _wrap(f"""<div class="stage" style="background:var(--espresso);display:flex;flex-direction:column;
    padding:45px 50px 35px;">
  <!-- Top row: kicker left, business name right -->
  <div style="display:flex;justify-content:space-between;align-items:center;">
    <span class="label">{data.get('kicker','RIYADH · FINE DINING')}</span>
    <span class="eyebrow" style="font-size:22px;">{data['business_name']}</span>
  </div>
  <!-- Massive headline full width -->
  <h1 class="display gold-text" style="font-size:{h_size}px;text-align:right;line-height:1.2;margin-top:20px;">{data['headline']}</h1>
  <div class="gold-rule" style="width:140px;margin-top:10px;"></div>
  <!-- Middle: photo left (55%), text right (45%) -->
  <div style="display:flex;gap:24px;margin-top:24px;flex:1;">
    <!-- Photo -->
    <div style="width:55%;border-radius:12px;overflow:hidden;border:2px solid var(--accent-core);
      box-shadow:0 15px 50px rgba(0,0,0,0.4);">
      <img src="data:image/jpeg;base64,{b64}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};">
    </div>
    <!-- Text -->
    <div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:16px;text-align:right;">
      <div class="body-ar" style="text-align:right;font-size:24px;line-height:1.7;">
        <div>{t1}</div><div style="margin-top:6px;">{t2}</div><div style="margin-top:6px;">{t3}</div>
      </div>
      <div style="display:flex;align-items:center;gap:12px;direction:rtl;" dir="rtl">
        <span class="stars" dir="ltr" style="font-size:22px;">★★★★<span style="color:rgba(242,217,160,0.25)">★</span></span>
        <span style="font-size:28px;font-weight:700;color:#FFF;white-space:nowrap;">{rating}</span>
        <span style="font-size:19px;color:var(--muted);">{reviews} تقييم</span>
      </div>
      {trust_html}
    </div>
  </div>
  <!-- Footer -->
  <div class="gold-rule" style="width:100%;margin-top:18px;"></div>
  <div style="display:flex;justify-content:space-between;margin-top:10px;gap:16px;">
    <span class="footer-url" style="white-space:nowrap;">{data.get('domain','nuhoot.xyz')}</span>
    <span class="footer-brand" style="white-space:nowrap;font-size:20px;">{data.get('brand_ar','نُهوت — التسويق الرقمي')}</span>
  </div>
  {GRAIN_SVG}<div class="grain" style="filter:url(#grain)"></div>
</div>""", colors)


# ═══════════════════════════════════════════════════════
# T15 — NEON EDGE (NEW — dark dramatic with glowing accent)
# Dark photo with neon accent glow, ultra-modern
# ═══════════════════════════════════════════════════════
def t15(b64, data, obj_pos, colors, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    rating = data.get("rating", "٤٫٥")
    reviews = _to_arabic(data["reviews"])
    trust = data.get("trust_badge", "")
    trust_html = ""
    if trust:
        trust_html = f'<div style="font-size:17px;color:var(--accent-light);font-weight:600;direction:rtl;opacity:0.85;">✦ {trust}</div>'
    glow = colors['core']
    glow_light = colors['light']
    h_size = _dynamic_headline_size(data['headline'])
    return _wrap(f"""<div class="stage" style="background:#060403;">
  <!-- Photo: right 55%, with neon edge -->
  <div style="position:absolute;top:0;right:0;width:55%;height:100%;overflow:hidden;">
    <img src="data:image/jpeg;base64,{b64}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};
      filter:brightness(0.65) contrast(1.15) saturate(1.1);">
    <!-- Neon edge glow on left side of photo -->
    <div style="position:absolute;top:0;left:0;bottom:0;width:4px;
      background:{glow};box-shadow:0 0 20px {glow},0 0 40px {glow}80,0 0 60px {glow}40;"></div>
  </div>
  <!-- Left panel: dark with neon text -->
  <div style="position:absolute;top:0;left:0;width:45%;height:100%;
    background:linear-gradient(135deg,#060403 0%,#0C0806 100%);
    display:flex;flex-direction:column;justify-content:center;gap:18px;
    align-items:flex-end;padding:50px 35px 45px;text-align:right;">
    <!-- Neon kicker -->
    <span class="label" style="color:{glow_light};text-shadow:0 0 8px {glow}80,0 0 16px {glow}40;">
      {data.get('kicker','RIYADH · FINE DINING')}
    </span>
    <span class="eyebrow" style="font-size:24px;">{data['business_name']}</span>
    <!-- Neon headline -->
    <h1 class="display" style="font-size:{h_size}px;text-align:right;line-height:1.25;
      color:#FFF;text-shadow:0 0 6px {glow}90,0 0 12px {glow}60,0 0 24px {glow}30,0 2px 4px rgba(0,0,0,0.8);">
      {data['headline']}
    </h1>
    <!-- Neon divider -->
    <div style="height:2px;width:100px;background:{glow};
      box-shadow:0 0 8px {glow},0 0 16px {glow}80;"></div>
    <div class="body-ar" style="text-align:right;font-size:23px;">
      <div>{t1}</div><div>{t2}</div><div>{t3}</div>
    </div>
    <!-- Rating with neon glow -->
    <div style="display:flex;align-items:center;gap:12px;direction:rtl;" dir="rtl">
      <span class="stars" dir="ltr" style="font-size:22px;text-shadow:0 0 8px {glow}60;">★★★★<span style="color:rgba(255,255,255,0.2)">★</span></span>
      <span style="font-size:30px;font-weight:800;color:#FFF;white-space:nowrap;
        text-shadow:0 0 6px {glow}80,0 0 12px {glow}40;">{rating}</span>
      <span style="font-size:19px;color:rgba(255,255,255,0.55);">{reviews} تقييم</span>
    </div>
    {trust_html}
    <!-- Neon footer line -->
    <div style="height:1px;width:100%;background:{glow};opacity:0.4;
      box-shadow:0 0 6px {glow}60;"></div>
    <div style="display:flex;justify-content:space-between;width:100%;gap:12px;">
      <span class="footer-url" style="white-space:nowrap;color:rgba(255,255,255,0.5);">{data.get('domain','nuhoot.xyz')}</span>
      <span class="footer-brand" style="white-space:nowrap;font-size:18px;color:rgba(255,255,255,0.7);">{data.get('brand_ar','نُهوت — التسويق الرقمي')}</span>
    </div>
  </div>
  {GRAIN_SVG}<div class="grain" style="filter:url(#grain)"></div>
</div>""", colors)


# ═══════════════════════════════════════════════════════
# Template registry
# ═══════════════════════════════════════════════════════
TEMPLATES = {
    1: ("Vertical Split", t01, "Any photo — clean 50/50 divide"),
    2: ("Gold Frame", t02, "Hero dish — large framed showcase"),
    3: ("Gold Ring", t03, "Full-bleed photo — gold ring accent"),
    4: ("Bottom Band", t04, "Wide table spread — full-bleed"),
    5: ("Arch Window", t05, "Vertical/tall subject — elegant"),
    6: ("Magazine Sidebar", t06, "Any photo — editorial sidebar"),
    7: ("Triple Strip", t07, "Course sequence — triptych (3 photos)"),
    8: ("Arch Accent", t08, "Bold single subject — arch frame"),
    9: ("Duotone Split", t09, "Any photo — warm editorial"),
    10: ("Framed Float", t10, "Atmospheric/moody — glass card hero"),
    11: ("Cinematic", t11, "Full-bleed dramatic — massive headline"),
    12: ("Glass Morphism", t12, "Frosted glass — modern luxury"),
    13: ("Diagonal Split", t13, "Asymmetric bold — diagonal photo"),
    14: ("Magazine Cover", t14, "Editorial grid — huge typography"),
    15: ("Neon Edge", t15, "Dark dramatic — real neon glow split"),
}


def generate_html(template_id: int, photo_path: str, data: dict,
                  obj_pos: str = "50% 50%", niche: str = "restaurants",
                  photo_paths: list = None) -> str:
    """Generate HTML for a template with niche-specific colors."""
    from nuhoot.design.niche_config import get_colors
    colors = get_colors(niche)
    b64 = _photo_b64(photo_path)

    # For T07 Triple Strip: pass multiple photo base64 strings
    photos_b64 = None
    if photo_paths and len(photo_paths) >= 3:
        photos_b64 = [_photo_b64(p) for p in photo_paths[:3]]

    name, func, best_for = TEMPLATES[template_id]
    return func(b64, data, obj_pos, colors, photos_b64)
