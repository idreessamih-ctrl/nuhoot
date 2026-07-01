"""THE GOLDEN ENGINE — Luxury Social Design System v4
Follows Opus's complete design course. No judgment calls, just rules.
"""

import base64
from nuhoot.design.photo_analyzer import PhotoProfile

_AR = "٠١٢٣٤٥٦٧٨٩"
_to_arabic = lambda s: "".join(_AR[int(c)] if c.isdigit() else c for c in str(s))

def _photo_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# ═══════════════════════════════════════════════════════
# SHARED CSS — the design system tokens (from Opus course)
# ═══════════════════════════════════════════════════════
SHARED_CSS = """
:root {
  --ink: #0C0A08;
  --espresso: #1A140D;
  --coffee: #2A2015;
  --gold-light: #F2D9A0;
  --gold-core: #C9A25A;
  --gold-deep: #8C6A2E;
  --gold-glint: #FBEFC0;
  --text: #FBF6EC;
  --muted: #C9BFA8;
  --hairline: rgba(201,162,90,0.28);
}
* { margin:0; padding:0; box-sizing:border-box; }
html, body {
  width:1080px; height:1080px; overflow:hidden;
  background: var(--ink);
  font-family: 'Noto Sans Arabic', sans-serif;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}
.stage { position:relative; width:1080px; height:1080px; overflow:hidden; }

/* LAYER 0: Photo */
.photo { position:absolute; inset:0; width:100%; height:100%;
  object-fit:cover; filter:saturate(1.05) contrast(1.08) brightness(0.96); z-index:0; }

/* LAYER 1: Grade overlay */
.grade { position:absolute; inset:0; z-index:1; mix-blend-mode:multiply;
  background: linear-gradient(135deg, rgba(40,26,10,0.25), rgba(20,14,8,0.10) 50%, rgba(60,40,15,0.30)); }

/* LAYER 4: Grain */
.grain { position:absolute; inset:0; z-index:4; opacity:0.06;
  mix-blend-mode:overlay; pointer-events:none; }

/* Gold gradient text with specular glint */
.gold-text {
  background: linear-gradient(100deg,
    #8C6A2E 0%, #C9A25A 25%, #F2D9A0 48%, #FBEFC0 52%, #C9A25A 70%, #8C6A2E 100%);
  -webkit-background-clip:text; background-clip:text;
  -webkit-text-fill-color:transparent; color:transparent;
  filter: drop-shadow(0 1px 1px rgba(0,0,0,0.4));
}

/* Gold rule divider */
.gold-rule { height:2px;
  background: linear-gradient(90deg, transparent, var(--gold-core), transparent); }

/* Label (Latin, uppercase, wide tracking) */
.label { font-family:'Lato',sans-serif; font-size:16px; font-weight:600;
  letter-spacing:0.22em; text-transform:uppercase; color: var(--gold-light); }

/* Arabic display title */
.display { font-family:'AlYamama','Noto Kufi Arabic',serif; font-weight:700;
  line-height:1.1; direction:rtl; letter-spacing:0; }

/* Arabic body */
.body-ar { font-family:'Noto Sans Arabic',sans-serif; font-size:22px;
  font-weight:400; line-height:1.8; direction:rtl; letter-spacing:0; color: var(--muted); }

/* Stars */
.stars { color: var(--gold-light); letter-spacing:4px;
  text-shadow: 0 0 10px rgba(201,162,90,0.3); }

/* Glass panel */
.glass {
  background: linear-gradient(135deg, rgba(255,248,235,0.12) 0%, rgba(255,248,235,0.04) 100%);
  backdrop-filter: blur(24px) saturate(1.4);
  -webkit-backdrop-filter: blur(24px) saturate(1.4);
  border: 1px solid rgba(255,245,225,0.18);
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.45),
    inset 0 1px 0 rgba(255,255,255,0.25),
    inset 0 -1px 0 rgba(0,0,0,0.20);
}

[dir="rtl"] { direction:rtl; unicode-bidi:isolate; }
"""

GRAIN_SVG = '''<svg width="0" height="0"><filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter></svg>'''


# ═══════════════════════════════════════════════════════
# LAYOUT 1 — Full-bleed photo + bottom text (LANDSCAPE)
# Photo fills canvas. Text clusters bottom-right with scrim.
# ═══════════════════════════════════════════════════════
def layout_1(b64: str, data: dict, obj_pos: str) -> str:
    name = data["business_name"]
    t1, t2, t3 = data["taglines"]
    rating = data["rating"]
    reviews = _to_arabic(data["reviews"])
    kicker = data.get("kicker", "RIYADH · FINE DINING")
    domain = data.get("domain", "nuhoot.xyz")
    brand = data.get("brand_ar", "نُهوت — التسويق الرقمي")
    hashtags = data["hashtags"]
    hash_str = "  ".join(hashtags)

    return f"""<div class="stage">
  <img class="photo" src="data:image/jpeg;base64,{b64}" style="object-position:{obj_pos}">
  <div class="grade"></div>

  <!-- LAYER 2: stronger scrim (Opus tiered fix) -->
  <div style="position:absolute;inset:0;z-index:2;
    background:linear-gradient(to top,
      rgba(6,5,3,0.97) 0%, rgba(6,5,3,0.88) 18%,
      rgba(6,5,3,0.55) 38%, rgba(6,5,3,0.20) 55%,
      transparent 72%);"></div>

  <!-- top eyebrow (Y90, right-aligned) -->
  <div style="position:absolute;top:90px;right:90px;z-index:5;text-align:right;">
    <span class="label">{kicker}</span>
  </div>

  <!-- GLASS TEXT CLUSTER: radial plate + backdrop blur = text pops on busy photos -->
  <div style="position:absolute;right:56px;bottom:56px;left:56px;z-index:5;
       display:flex;flex-direction:column;align-items:flex-end;gap:24px;
       padding:34px 38px;border-radius:24px;max-width:62%;margin-left:auto;
       background:radial-gradient(120% 140% at 80% 80%,rgba(6,5,3,0.62) 0%,rgba(6,5,3,0.42) 55%,rgba(6,5,3,0) 100%);
       backdrop-filter:blur(4px) saturate(0.9);-webkit-backdrop-filter:blur(4px) saturate(0.9);
       border:1px solid rgba(255,255,255,0.10);
       box-shadow:0 12px 40px rgba(0,0,0,0.4),inset 0 1px 0 rgba(255,255,255,0.12);">
    <div class="gold-rule" style="width:90px;"></div>
    <h1 class="display gold-text" style="font-size:72px;line-height:1.45;text-align:right;
        filter:drop-shadow(0 2px 4px rgba(0,0,0,0.85)) drop-shadow(0 0 1px rgba(0,0,0,0.9));">{name}</h1>
    <div class="body-ar" style="text-align:right;max-width:580px;color:#FFFFFF;font-size:33px;line-height:1.6;
        text-shadow:0 2px 6px rgba(0,0,0,0.9),0 0 2px rgba(0,0,0,0.95);">
      <div>{t1}</div><div>{t2}</div><div>{t3}</div>
    </div>
    <div style="display:flex;align-items:center;gap:16px;direction:rtl;" dir="rtl">
      <span class="stars" dir="ltr" style="text-shadow:0 2px 5px rgba(0,0,0,0.9);">★★★★<span style="color:rgba(242,217,160,0.35)">★</span></span>
      <span style="font-family:Lato;font-size:36px;font-weight:700;color:#FFFFFF;direction:ltr;text-shadow:0 2px 6px rgba(0,0,0,0.9);">{rating}</span>
      <span style="font-size:26px;color:var(--muted);text-shadow:0 1px 4px rgba(0,0,0,0.8);">{reviews} تقييم</span>
    </div>
    <div class="gold-rule" style="width:100%;margin-top:8px;"></div>
    <div style="display:flex;justify-content:space-between;align-items:baseline;width:100%;">
      <span style="font-family:Lato;font-size:26px;color:var(--muted);letter-spacing:0.14em;direction:ltr;text-shadow:0 1px 4px rgba(0,0,0,0.8);">{domain}</span>
      <span style="font-size:26px;color:var(--gold-core);text-shadow:0 1px 4px rgba(0,0,0,0.8);">{brand}</span>
    </div>
  </div>

  {GRAIN_SVG}
  <div class="grain" style="filter:url(#grain)"></div>
</div>"""


# ═══════════════════════════════════════════════════════
# LAYOUT 2 — Split panel (PORTRAIT)
# Photo right 60%, glass text panel left 40%.
# ═══════════════════════════════════════════════════════
def layout_2(b64: str, data: dict, obj_pos: str) -> str:
    name = data["business_name"]
    t1, t2, t3 = data["taglines"]
    rating = data["rating"]
    reviews = _to_arabic(data["reviews"])
    kicker = data.get("kicker", "RIYADH · FINE DINING")
    domain = data.get("domain", "nuhoot.xyz")
    brand = data.get("brand_ar", "نُهوت — التسويق الرقمي")
    hashtags = data["hashtags"]
    hash_str = "  ".join(hashtags)

    return f"""<div class="stage">
  <!-- photo occupies right 57% (X620 to X1080) — panel widened 410→460 -->
  <img class="photo" src="data:image/jpeg;base64,{b64}"
       style="left:620px;width:460px;object-position:{obj_pos}">
  <div class="grade" style="left:620px;width:460px"></div>

  <!-- feather: photo fades into dark left field -->
  <div style="position:absolute;top:0;left:620px;width:180px;height:100%;z-index:2;
    background:linear-gradient(to right,var(--ink),transparent);"></div>

  <!-- solid dark left field -->
  <div style="position:absolute;top:0;left:0;width:620px;height:100%;z-index:1;
    background:var(--espresso);"></div>

  <!-- subtle radial warm glow behind glass -->
  <div style="position:absolute;top:0;left:0;width:620px;height:100%;z-index:1;
    background:radial-gradient(120% 80% at 70% 20%,rgba(60,40,15,0.6),transparent 60%);"></div>

  <!-- GLASS PANEL: text with bottom-right gravity — WIDENED 410→460, padding 48→40 -->
  <div class="glass" style="position:absolute;z-index:3;top:90px;left:90px;width:460px;height:900px;
    display:flex;flex-direction:column;justify-content:flex-end;align-items:flex-end;
    gap:24px;padding:40px;">
    <span class="label">{kicker}</span>
    <h1 class="display gold-text" style="font-size:56px;line-height:1.5;text-align:right;">{name}</h1>
    <div class="gold-rule" style="width:72px;"></div>
    <div class="body-ar" style="text-align:right;font-size:29px;line-height:1.6;color:var(--text);text-shadow:0 1px 6px rgba(0,0,0,0.35);">
      <div>{t1}</div><div>{t2}</div><div>{t3}</div>
    </div>
    <div style="display:flex;align-items:center;gap:12px;direction:rtl;" dir="rtl">
      <span class="stars" dir="ltr" style="font-size:24px;letter-spacing:3px;">★★★★<span style="color:rgba(242,217,160,0.35)">★</span></span>
      <span style="font-family:Lato;font-size:30px;font-weight:700;color:var(--text);direction:ltr;">{rating}</span>
      <span style="font-size:22px;color:var(--muted);">{reviews}</span>
    </div>
    <div class="gold-rule" style="width:100%;"></div>
    <div style="display:flex;flex-direction:column;align-items:flex-end;gap:8px;width:100%;">
      <span style="font-family:Lato;font-size:23px;color:var(--muted);letter-spacing:0.14em;direction:ltr;">{domain}</span>
      <span style="font-size:23px;color:var(--gold-core);">{brand}</span>
    </div>
  </div>

  {GRAIN_SVG}
  <div class="grain" style="filter:url(#grain)"></div>
</div>"""


# ═══════════════════════════════════════════════════════
# LAYOUT 3 — Centered framed photo (SQUARE / FOOD)
# Photo in centered frame, text below.
# ═══════════════════════════════════════════════════════
def layout_3(b64: str, data: dict, obj_pos: str) -> str:
    name = data["business_name"]
    t1 = data["taglines"][0]
    rating = data["rating"]
    reviews = _to_arabic(data["reviews"])
    kicker = data.get("kicker", "RIYADH · FINE DINING")
    domain = data.get("domain", "nuhoot.xyz")
    brand = data.get("brand_ar", "نُهوت — التسويق الرقمي")
    hashtags = data["hashtags"]
    hash_str = "  ".join(hashtags)

    return f"""<div class="stage" style="background:var(--espresso)">
  <!-- background radial gradient -->
  <div style="position:absolute;inset:0;z-index:0;
    background:radial-gradient(120% 80% at 50% 30%,#2A2015,#0C0A08);"></div>

  <!-- top eyebrow centered (Y90) -->
  <div style="position:absolute;top:90px;left:0;right:0;z-index:5;text-align:center;">
    <span class="label">{kicker}</span>
  </div>

  <!-- centered photo frame 540x540, X270 Y180 -->
  <div style="position:absolute;z-index:3;top:180px;left:270px;width:540px;height:540px;
    border-radius:20px;overflow:hidden;
    border:1px solid rgba(201,162,90,0.45);
    box-shadow:0 30px 70px rgba(0,0,0,0.55),inset 0 1px 0 rgba(255,255,255,0.15);">
    <img class="photo" src="data:image/jpeg;base64,{b64}" style="object-position:{obj_pos}">
    <div class="grade"></div>
    <div style="position:absolute;inset:0;
      background:linear-gradient(to top,rgba(8,6,4,0.5),transparent 40%);"></div>
  </div>

  <!-- title below photo (Y765, centered, gap:16px) -->
  <div style="position:absolute;z-index:5;top:765px;left:90px;right:90px;
       display:flex;flex-direction:column;align-items:center;gap:16px;">
    <h1 class="display gold-text" style="font-size:56px;text-align:center;">{name}</h1>
    <div class="gold-rule" style="width:90px;"></div>
    <div class="body-ar" style="text-align:center;font-size:20px;max-width:720px;color:var(--text);">{t1}</div>
    <div style="display:flex;align-items:center;gap:12px;direction:rtl;" dir="rtl">
      <span class="stars" dir="ltr" style="font-size:20px;letter-spacing:3px;">★★★★<span style="color:rgba(242,217,160,0.35)">★</span></span>
      <span style="font-family:Lato;font-size:24px;font-weight:700;color:var(--text);direction:ltr;">{rating}</span>
      <span style="font-size:16px;color:var(--muted);">{reviews} تقييم</span>
    </div>
    <div class="gold-rule" style="width:100%;margin-top:8px;"></div>
    <div style="display:flex;justify-content:space-between;align-items:baseline;width:100%;">
      <span style="font-family:Lato;font-size:14px;color:var(--muted);letter-spacing:0.14em;direction:ltr;">{domain}</span>
      <span style="font-size:14px;color:var(--gold-core);">{brand}</span>
    </div>
  </div>

  {GRAIN_SVG}
  <div class="grain" style="filter:url(#grain)"></div>
</div>"""


# ═══════════════════════════════════════════════════════
# GENERATE — entry point
# ═══════════════════════════════════════════════════════
def generate_html(profile: PhotoProfile, data: dict) -> str:
    b64 = _photo_b64(data["photo_path"])
    obj_pos = profile.object_position

    if profile.archetype == "A":
        body = layout_1(b64, data, obj_pos)
    elif profile.archetype == "B":
        body = layout_2(b64, data, obj_pos)
    else:  # C or D → centered frame
        body = layout_3(b64, data, obj_pos)

    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<style>
{SHARED_CSS}
</style>
</head>
<body>
{body}
</body>
</html>"""
