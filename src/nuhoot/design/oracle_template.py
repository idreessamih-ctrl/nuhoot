"""ORACLE Template Engine v3 — Opus alignment + jaw-dropping upgrades."""

import base64
from nuhoot.design.photo_analyzer import PhotoProfile

_AR = "٠١٢٣٤٥٦٧٨٩"
_to_arabic = lambda s: "".join(_AR[int(c)] if c.isdigit() else c for c in str(s))


def _photo_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


_GRAIN_SVG = '''<svg class="grain-svg" aria-hidden="true" style="position:absolute;inset:0;width:100%;height:100%;opacity:0.10;mix-blend-mode:overlay;pointer-events:none;z-index:9999">
  <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
  <rect width="100%" height="100%" filter="url(#grain)"/>
</svg>'''


def _shared_css() -> str:
    return """
:root {
  --obsidian: #0A0A0B; --obsidian-2: #121214; --ink-panel: #0E0E10;
  --gold-1: #F4D58D; --gold-2: #D4AF37; --gold-3: #A8842A;
  --white: #FFFFFF; --white-72: rgba(255,255,255,0.72); --white-50: rgba(255,255,255,0.50);
  --hairline: rgba(244,213,141,0.22);
  --type-hero: 56px; --type-tagline: 17px; --type-kicker: 12px; --type-foot: 13px;
}
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:1080px; height:1080px; overflow:hidden;
  background:var(--obsidian); font-family:'Lato',sans-serif;
  -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility; }
.canvas { position:relative; width:1080px; height:1080px; overflow:hidden; }
[dir="rtl"] { direction:rtl; unicode-bidi:isolate; }
.ar { font-family:'AlYamama','Noto Kufi Arabic','Noto Sans Arabic',sans-serif; }
.ar-body { font-family:'Noto Sans Arabic',sans-serif; }

/* === GOLD GRADIENT TITLE + DUAL DROP-SHADOW + ACCENT LINE + GLOW === */
.oracle-title {
  position: relative; padding-left: 22px;
  background: linear-gradient(135deg, #F6E3B4 0%, #C9A25A 45%, #9C7636 100%);
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent; color: transparent;
  filter: drop-shadow(0 1px 1px rgba(0,0,0,0.85)) drop-shadow(0 8px 24px rgba(201,162,90,0.28));
}
/* Gold vertical accent line beside title */
.oracle-title::before {
  content: ""; position: absolute; left: 0; top: 6px; bottom: 6px; width: 3px;
  background: linear-gradient(180deg, #E7CB8E 0%, #C9A86A 50%, rgba(201,168,106,0) 100%);
  border-radius: 2px;
}
/* Atmospheric gold glow behind title */
.oracle-title::after {
  content: ""; position: absolute; left: -10px; top: -20px;
  width: 220px; height: 160px;
  background: radial-gradient(ellipse, rgba(201,168,106,0.22) 0%, transparent 70%);
  filter: blur(28px); z-index: -1; pointer-events: none;
}

/* === KICKER CHIP === */
.kicker-chip {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 7px 14px; border-radius: 999px; align-self: flex-start;
  font-family: 'Lato'; font-size: var(--type-kicker); font-weight: 600;
  letter-spacing: 0.22em; text-transform: uppercase; color: #F0D9A8;
  background: rgba(201,162,90,0.12); border: 1px solid rgba(201,162,90,0.35);
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
}
.kicker-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--gold-2); box-shadow: 0 0 8px rgba(212,175,55,0.8); }

/* === PHOTO DUOTONE GRADE === */
.oracle-photo { position: relative; }
.oracle-photo::after {
  content: ""; position: absolute; inset: 0;
  background: linear-gradient(160deg, rgba(201,162,90,0.18) 0%, transparent 45%, rgba(40,20,50,0.30) 100%);
  mix-blend-mode: soft-light; pointer-events: none;
}

.rule { height:1px; width:100%; background:linear-gradient(90deg,transparent,rgba(201,168,106,0.28),transparent); }
.stars { color:var(--gold-1); text-shadow:0 0 12px rgba(212,175,55,0.4); }
"""


def _build_content(arch: str, data: dict) -> str:
    name = data["business_name"]
    t1, t2, t3 = data["taglines"]
    rating = data["rating"]
    reviews_ar = _to_arabic(data["reviews"])
    hashtags = data["hashtags"]
    brand = data.get("brand_ar", "نُهوت — التسويق الرقمي")
    domain = data.get("domain", "nuhoot.xyz")
    kicker = data.get("kicker", "RIYADH · FINE DINING")
    hash_str = "&nbsp;&nbsp;".join(h for h in hashtags)

    if arch == "A":
        return f"""
    <div class="hero-panel">
      <div class="kicker-chip"><span class="kicker-dot"></span>{kicker}</div>
      <h1 class="h1 ar oracle-title">{name}</h1>
      <div class="tagline ar-body"><div>{t1}</div><div>{t2}</div><div>{t3}</div></div>
      <div class="ratingrow" dir="rtl">
        <span class="stars" dir="ltr">★★★★<span style="color:rgba(244,213,141,0.4)">★</span></span>
        <span class="score" dir="ltr">{rating}</span>
        <span class="reviews ar-body">{reviews_ar} تقييم</span>
      </div>
      <div class="footer">
        <span class="footer-url">{domain}</span>
        <span class="footer-brand ar">{brand}</span>
      </div>
    </div>"""
    elif arch == "B":
        return f"""
    <div class="text-panel">
      <div class="panel-corner panel-corner-tr"></div>
      <div class="panel-corner panel-corner-bl"></div>
      <div class="zone-top">
        <div class="kicker-chip"><span class="kicker-dot"></span>{kicker}</div>
        <h1 class="h1 ar oracle-title">{name}</h1>
        <div class="tagline ar-body"><div>{t1}</div><div>{t2}</div><div>{t3}</div></div>
        <div class="ratingrow" dir="rtl">
          <span class="stars" dir="ltr">★★★★<span style="color:rgba(244,213,141,0.4)">★</span></span>
          <span class="score" dir="ltr">{rating}</span>
          <span class="reviews ar-body">{reviews_ar}</span>
        </div>
      </div>
      <div class="zone-bottom">
        <div class="hashtags ar-body">{hash_str}</div>
        <div class="footer">
          <span class="footer-url">{domain}</span>
          <span class="footer-brand ar">{brand}</span>
        </div>
      </div>
    </div>"""
    elif arch == "C":
        return f"""
      <div class="top">
        <div class="kicker-chip"><span class="kicker-dot"></span>{kicker}</div>
      </div>
      <div class="photo-card oracle-photo">
        <img src="data:image/jpeg;base64,{_photo_b64(data['photo_path'])}" alt="">
      </div>
      <div class="bottom">
        <h1 class="h1 ar oracle-title">{name}</h1>
        <div class="tagline ar-body"><div>{t1}</div><div>{t2}</div><div>{t3}</div></div>
        <div class="ratingrow" dir="rtl">
          <span class="stars" dir="ltr">★★★★<span style="color:rgba(244,213,141,0.4)">★</span></span>
          <span class="score" dir="ltr">{rating}</span>
          <span class="reviews ar-body">{reviews_ar} تقييم</span>
        </div>
        <div class="footer">
          <span class="footer-url">{domain}</span>
          <span class="footer-brand ar">{brand}</span>
        </div>
      </div>"""
    else:  # D
        return f"""
      <div class="header">
        <div class="kicker-chip"><span class="kicker-dot"></span>{kicker}</div>
        <h1 class="h1 ar oracle-title">{name}</h1>
        <div class="rule" style="margin-bottom:0"></div>
      </div>
      <div class="photo-frame oracle-photo">
        <img src="data:image/jpeg;base64,{_photo_b64(data['photo_path'])}" alt="">
      </div>
      <div class="meta" dir="rtl">
        <div class="tagline ar-body" style="flex:1">{t1}</div>
        <div class="ratingrow">
          <span class="stars" dir="ltr">★★★★<span style="color:rgba(244,213,141,0.4)">★</span></span>
          <span class="score" dir="ltr">{rating}</span>
          <span class="reviews ar-body">{reviews_ar}</span>
        </div>
      </div>
      <div class="footer">
        <span class="footer-url">{domain}</span>
        <span class="footer-brand ar">{brand}</span>
      </div>"""


def _arch_css(arch: str, profile: PhotoProfile) -> str:
    obj_pos = profile.object_position

    if arch == "A":
        return f"""
.A {{ position: relative; overflow: hidden; }}
.A .photo {{ position:absolute; inset:0; width:100%; height:100%;
  object-fit:cover; object-position:{obj_pos}; z-index:1; }}
.A::before {{ content:""; position:absolute; inset:0; z-index:2;
  background: linear-gradient(180deg, rgba(10,8,6,0.10) 0%, transparent 35%,
    rgba(10,8,6,0.55) 78%, rgba(8,6,4,0.88) 100%),
    radial-gradient(100% 70% at 50% 100%, rgba(201,162,90,0.12) 0%, transparent 65%);
  mix-blend-mode: multiply; pointer-events: none; }}
.A::after {{ content:""; position:absolute; inset:0; z-index:3;
  background: radial-gradient(130% 110% at 50% 42%, transparent 55%, rgba(0,0,0,0.55) 100%);
  pointer-events: none; }}
.A .hero-panel {{
  position: absolute; left: 48px; right: 48px; bottom: 48px; z-index: 10;
  padding: 44px 48px 40px; border-radius: 16px;
  background: linear-gradient(135deg, rgba(255,255,255,0.07) 0%, rgba(255,255,255,0.02) 100%);
  border: 1px solid rgba(255,255,255,0.12);
  backdrop-filter: blur(16px) saturate(1.3); -webkit-backdrop-filter: blur(16px) saturate(1.3);
  box-shadow: 0 20px 60px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.15);
  will-change: backdrop-filter; transform: translateZ(0);
  display: flex; flex-direction: column;
}}
.A .h1 {{ font-size: var(--type-hero); line-height: 1.1; font-weight: 700; margin-top: 22px; margin-bottom: 16px; }}
.A .tagline {{ font-size: var(--type-tagline); line-height: 1.5; color: var(--white-72); margin-top: 0;
  max-width: 42ch; text-shadow: 0 1px 8px rgba(0,0,0,0.6); }}
.A .ratingrow {{ display:flex; align-items:center; gap:14px; font-size:32px; margin-top: 28px; }}
.A .score {{ color: var(--white); font-weight: 700; }}
.A .reviews {{ font-size: var(--type-foot); color: var(--white-50); }}
.A .footer {{ margin-top: 32px; padding-top: 18px; border-top: 1px solid rgba(201,168,106,0.28);
  display: flex; justify-content: space-between; align-items: baseline; }}
.A .footer-url {{ font-family:'Lato'; font-size: var(--type-foot); color: #F0D9A8; letter-spacing: 0.14em; direction: ltr; }}
.A .footer-brand {{ font-size: 15px; color: #C9A86A; }}
"""
    elif arch == "B":
        return f"""
.B {{ display:flex; overflow:hidden; }}
.B .photo-panel {{ position:relative; width:670px; height:1080px; flex:0 0 670px; overflow:hidden; z-index:1; }}
.B .photo-panel img {{ width:100%; height:100%; object-fit:cover; object-position:{obj_pos}; }}
.B .photo-panel::after {{ content:''; position:absolute; top:0; right:0; bottom:0; width:120px;
  background:linear-gradient(to right, rgba(10,10,11,0) 0%, var(--obsidian) 100%); }}
/* TEXT PANEL — 3-zone flex layout, layered gradient, glass, grain, corner brackets */
.B .text-panel {{
  position: relative; width:410px; height:1080px; flex:0 0 410px; overflow:hidden;
  background: linear-gradient(135deg, rgba(28,22,16,0.92) 0%, rgba(14,12,10,0.96) 55%, rgba(8,7,6,0.98) 100%),
    radial-gradient(120% 90% at 80% 10%, rgba(201,162,90,0.14) 0%, transparent 60%);
  backdrop-filter: blur(18px) saturate(1.2); -webkit-backdrop-filter: blur(18px) saturate(1.2);
  box-shadow: inset 1px 0 0 rgba(201,162,90,0.25);
  -webkit-mask-image: linear-gradient(to right, transparent 0%, black 12%);
  mask-image: linear-gradient(to right, transparent 0%, black 12%);
  will-change: backdrop-filter; transform: translateZ(0);
  padding: 72px 48px 64px; display: flex; flex-direction: column; justify-content: space-between;
}}
/* Duotone glow bleed */
.B .text-panel::before {{
  content: ""; position: absolute; inset: 0;
  background: linear-gradient(135deg, rgba(201,162,90,0.10) 0%, rgba(120,60,90,0.06) 40%, transparent 75%);
  mix-blend-mode: screen; pointer-events: none;
}}
/* Corner bracket accents */
.panel-corner {{ position: absolute; width: 28px; height: 28px; border-color: rgba(201,168,106,0.55); border-style: solid; z-index: 3; }}
.panel-corner-tr {{ top: 28px; right: 28px; border-width: 1.5px 1.5px 0 0; }}
.panel-corner-bl {{ bottom: 28px; left: 28px; border-width: 0 0 1.5px 1.5px; }}
/* Zones */
.zone-top, .zone-bottom {{ position: relative; z-index: 2; }}
.zone-top {{ display: flex; flex-direction: column; }}
.zone-bottom {{ display: flex; flex-direction: column; }}
.B .h1 {{ font-size: var(--type-hero); line-height: 1.12; font-weight: 700; text-align: right; margin-top: 28px; }}
.B .tagline {{ font-size: var(--type-tagline); line-height: 1.5; color: var(--white-72); text-align: right;
  margin-top: 20px; max-width: 30ch; text-shadow: 0 1px 6px rgba(0,0,0,0.5); }}
.B .ratingrow {{ display:flex; align-items:center; gap:12px; font-size:28px; justify-content:flex-end; margin-top: 32px; }}
.B .score {{ color: var(--white); font-weight: 700; }}
.B .reviews {{ font-size: var(--type-foot); color: var(--white-50); }}
.B .hashtags {{ font-size: var(--type-foot); color: var(--white-50); text-align: right; line-height: 1.6;
  letter-spacing: 0.02em; opacity: 0.7; }}
.B .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(201,168,106,0.28);
  display: flex; flex-direction: column; gap: 6px; }}
.B .footer-url {{ font-family:'Lato'; font-size: var(--type-foot); color: rgba(255,255,255,0.85);
  letter-spacing: 0.14em; direction: ltr; text-align: left; }}
.B .footer-brand {{ font-size: 15px; color: #C9A86A; text-align: right; }}
"""
    elif arch == "C":
        return f"""
.C .canvas {{ display:flex; flex-direction:column; align-items:center;
  justify-content:space-between; padding:56px 72px; z-index:2; position:relative; }}
.C .top {{ text-align:center; }}
.C .photo-card {{ position:relative; width:{profile.card_w}; height:{profile.card_h};
  border-radius:8px; overflow:hidden;
  box-shadow:0 0 0 1px var(--gold-3), 0 0 0 6px rgba(212,175,55,0.10), 0 30px 80px rgba(0,0,0,0.65); }}
.C .photo-card img {{ width:100%; height:100%; object-fit:cover; object-position:{obj_pos}; }}
.C .bottom {{ text-align:center; width:100%; }}
.C .h1 {{ font-size: var(--type-hero); line-height: 1.08; font-weight: 700; margin: 24px 0 14px; }}
.C .tagline {{ font-size: var(--type-tagline); color: var(--white-72); line-height: 1.5; margin-bottom: 20px; }}
.C .ratingrow {{ display:flex; align-items:center; justify-content:center; gap:14px; font-size: 28px; margin-bottom: 24px; }}
.C .score {{ color: var(--white); font-weight: 700; }}
.C .reviews {{ font-size: var(--type-foot); color: var(--white-50); }}
.C .footer {{ display:flex; justify-content:space-between; align-items:baseline; width:100%; }}
.C .footer-url {{ font-family:'Lato'; font-size: var(--type-foot); color: #F0D9A8; letter-spacing: 0.14em; }}
.C .footer-brand {{ font-size: 15px; color: #C9A86A; }}
"""
    else:  # D
        return f"""
.D .canvas {{ position:relative; z-index:2; padding:56px 72px;
  display:flex; flex-direction:column; height:1080px; }}
.D .header {{ text-align:right; margin-bottom: 24px; }}
.D .h1 {{ font-size: var(--type-hero); line-height: 1.05; font-weight: 700; margin-bottom: 16px; }}
.D .photo-frame {{ position:relative; width:100%; height:440px;
  border-radius:8px; overflow:hidden;
  box-shadow:0 0 0 1px var(--hairline), 0 24px 60px rgba(0,0,0,0.55); margin: 8px 0 24px; }}
.D .photo-frame img {{ width:100%; height:100%; object-fit:cover; object-position:{obj_pos}; }}
.D .meta {{ display:flex; align-items:center; justify-content:space-between; margin-bottom: 20px; }}
.D .tagline {{ font-size: var(--type-tagline); color: var(--white-72); }}
.D .ratingrow {{ display:flex; align-items:center; gap:12px; font-size: 26px; }}
.D .score {{ color: var(--white); font-weight: 700; }}
.D .reviews {{ font-size: var(--type-foot); color: var(--white-50); }}
.D .footer {{ display:flex; justify-content:space-between; align-items:baseline; margin-top: auto;
  padding-top: 18px; border-top: 1px solid rgba(201,168,106,0.28); }}
.D .footer-url {{ font-family:'Lato'; font-size: var(--type-foot); color: #F0D9A8; letter-spacing: 0.14em; }}
.D .footer-brand {{ font-size: 15px; color: #C9A86A; }}
"""


def generate_html(profile: PhotoProfile, data: dict) -> str:
    arch = profile.archetype
    b64 = _photo_b64(data["photo_path"])

    if arch == "A":
        photo_html = f'<img class="photo" src="data:image/jpeg;base64,{b64}" alt="">'
        body = f'<div class="canvas A">{photo_html}{_build_content(arch, data)}{_GRAIN_SVG}</div>'
    elif arch == "B":
        photo_html = f'<div class="photo-panel oracle-photo"><img src="data:image/jpeg;base64,{b64}" alt=""></div>'
        body = f'<div class="canvas B">{photo_html}{_build_content(arch, data)}{_GRAIN_SVG}</div>'
    elif arch == "C":
        body = f'<div class="canvas C">{_build_content(arch, data)}{_GRAIN_SVG}</div>'
    else:
        body = f'<div class="canvas D">{_build_content(arch, data)}{_GRAIN_SVG}</div>'

    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<style>
{_shared_css()}
{_arch_css(arch, profile)}
</style>
</head>
<body>
{body}
</body>
</html>"""
