"""Nuhoot v5 — ALIVE Templates with depth, gradients, 3D text, particles.

Based on Opus design consultation: 5 techniques that add LIFE:
1. Rich multi-stop gradient backgrounds (not flat colors)
2. 3D extruded typography (stacked text-shadows)
3. Organic image masks (non-rectangular photos)
4. Floating particle systems (sparkles, dots, shapes)
5. Layered depth (foreground/midground/background z-index)
"""

import base64, random

_AR = "٠١٢٣٤٥٦٧٨٩"
_to_arabic = lambda s: "".join(_AR[int(c)] if c.isdigit() else c for c in str(s))

def _photo_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# ═══════════════════════════════════════════════════════
# NICHE COLORS with GRADIENT definitions
# ═══════════════════════════════════════════════════════
NICHE_COLORS = {
    "restaurants": {
        "bg_grad": "radial-gradient(ellipse at 30% 20%,rgba(255,255,255,0.15) 0%,transparent 50%),radial-gradient(ellipse at center,#FFD93D 0%,#F5C800 40%,#E5A800 70%,#D4A700 100%)",
        "accent": "#1A1A1A", "accent_light": "#3A2A1A", "text": "#1A1A1A",
        "pill_bg": "#1A1A1A", "pill_text": "#FFFFFF",
        "particle_color": "rgba(0,0,0,0.15)", "particle_count": 12,
        "text_3d_shadows": "1px 1px 0 #B8960C,2px 2px 0 #9C7A0A,3px 3px 0 #806108,4px 4px 0 #644806,5px 5px 0 #483004,6px 6px 15px rgba(0,0,0,0.3)",
    },
    "cafes": {
        "bg_grad": "radial-gradient(ellipse at 20% 30%,rgba(245,222,179,0.2) 0%,transparent 50%),radial-gradient(ellipse at center,#6F4E37 0%,#5C3D2E 60%,#3E2723 100%)",
        "accent": "#F5DEB3", "accent_light": "#FFF8E7", "text": "#FFF8E7",
        "pill_bg": "#F5DEB3", "pill_text": "#3E2723",
        "particle_color": "rgba(245,222,179,0.3)", "particle_count": 10,
        "text_3d_shadows": "1px 1px 0 #3E2723,2px 2px 0 #2A1B14,3px 3px 0 #1A0F08,4px 4px 12px rgba(0,0,0,0.4)",
    },
    "bakeries": {
        "bg_grad": "radial-gradient(ellipse at 30% 20%,rgba(255,255,255,0.2) 0%,transparent 50%),radial-gradient(ellipse at center,#FF8C42 0%,#E07B30 50%,#C66820 100%)",
        "accent": "#3E2723", "accent_light": "#5D4037", "text": "#FFFFFF",
        "pill_bg": "#FFFFFF", "pill_text": "#3E2723",
        "particle_color": "rgba(255,255,255,0.3)", "particle_count": 12,
        "text_3d_shadows": "1px 1px 0 #C66820,2px 2px 0 #A05518,3px 3px 0 #804012,4px 4px 15px rgba(0,0,0,0.3)",
    },
    "salons": {
        "bg_grad": "radial-gradient(ellipse at 70% 30%,rgba(233,69,96,0.2) 0%,transparent 50%),radial-gradient(ellipse at center,#1A1A2E 0%,#16213E 50%,#0F0F1E 100%)",
        "accent": "#E94560", "accent_light": "#FF6B7A", "text": "#FFFFFF",
        "pill_bg": "#E94560", "pill_text": "#FFFFFF",
        "particle_color": "rgba(233,69,96,0.4)", "particle_count": 15,
        "text_3d_shadows": "1px 1px 0 #B03050,2px 2px 0 #8C2040,3px 3px 0 #681030,4px 4px 15px rgba(0,0,0,0.5)",
    },
    "spas": {
        "bg_grad": "radial-gradient(ellipse at 50% 80%,rgba(168,213,186,0.2) 0%,transparent 50%),radial-gradient(ellipse at center,#2D4A3E 0%,#1E3328 60%,#0F1E18 100%)",
        "accent": "#A8D5BA", "accent_light": "#C8E6D0", "text": "#E8F5E9",
        "pill_bg": "#A8D5BA", "pill_text": "#1E3328",
        "particle_color": "rgba(168,213,186,0.3)", "particle_count": 12,
        "text_3d_shadows": "1px 1px 0 #1E3328,2px 2px 0 #0F1E18,3px 3px 0 #08120C,4px 4px 12px rgba(0,0,0,0.4)",
    },
    "barbershops": {
        "bg_grad": "radial-gradient(ellipse at 50% 20%,rgba(212,175,55,0.15) 0%,transparent 40%),radial-gradient(ellipse at center,#1A1A1A 0%,#0F0F0F 70%,#000000 100%)",
        "accent": "#D4AF37", "accent_light": "#F0D050", "text": "#FFFFFF",
        "pill_bg": "#D4AF37", "pill_text": "#0F0F0F",
        "particle_color": "rgba(212,175,55,0.3)", "particle_count": 15,
        "text_3d_shadows": "1px 1px 0 #B8960C,2px 2px 0 #9C7A0A,3px 3px 0 #806108,4px 4px 0 #644806,5px 5px 0 #483004,6px 6px 15px rgba(0,0,0,0.5)",
    },
    "gyms": {
        "bg_grad": "radial-gradient(ellipse at 50% 100%,rgba(255,107,53,0.2) 0%,transparent 50%),radial-gradient(ellipse at center,#1A1A1A 0%,#0A0A0A 70%,#000000 100%)",
        "accent": "#FF6B35", "accent_light": "#FF9555", "text": "#FFFFFF",
        "pill_bg": "#FF6B35", "pill_text": "#0A0A0A",
        "particle_color": "rgba(255,107,53,0.4)", "particle_count": 18,
        "text_3d_shadows": "1px 1px 0 #CC4515,2px 2px 0 #A03510,3px 3px 0 #802508,4px 4px 15px rgba(0,0,0,0.5)",
    },
    "clinics": {
        "bg_grad": "radial-gradient(ellipse at 30% 20%,rgba(255,255,255,0.4) 0%,transparent 50%),radial-gradient(ellipse at center,#E8F4F8 0%,#D1ECF1 50%,#B8DDE8 100%)",
        "accent": "#2DB8A8", "accent_light": "#5DD8C8", "text": "#1E3A52",
        "pill_bg": "#2DB8A8", "pill_text": "#FFFFFF",
        "particle_color": "rgba(45,184,168,0.2)", "particle_count": 10,
        "text_3d_shadows": "1px 1px 0 #156B5E,2px 2px 0 #0A5E52,3px 3px 0 #004035,4px 4px 12px rgba(0,0,0,0.2)",
    },
    "dentists": {
        "bg_grad": "radial-gradient(ellipse at 30% 20%,rgba(255,255,255,0.4) 0%,transparent 50%),radial-gradient(ellipse at center,#E8F4F8 0%,#D1ECF1 50%,#B8DDE8 100%)",
        "accent": "#00A8D5", "accent_light": "#33C0E5", "text": "#1E3A52",
        "pill_bg": "#00A8D5", "pill_text": "#FFFFFF",
        "particle_color": "rgba(0,168,213,0.2)", "particle_count": 10,
        "text_3d_shadows": "1px 1px 0 #007A9C,2px 2px 0 #006080,3px 3px 0 #004060,4px 4px 12px rgba(0,0,0,0.2)",
    },
    "pharmacies": {
        "bg_grad": "radial-gradient(ellipse at 30% 20%,rgba(255,255,255,0.4) 0%,transparent 50%),radial-gradient(ellipse at center,#E8F5E9 0%,#C8E6C9 50%,#A5D6A7 100%)",
        "accent": "#2E7D32", "accent_light": "#4CAF50", "text": "#1B5E20",
        "pill_bg": "#2E7D32", "pill_text": "#FFFFFF",
        "particle_color": "rgba(46,125,50,0.2)", "particle_count": 10,
        "text_3d_shadows": "1px 1px 0 #1B5E20,2px 2px 0 #0D3D10,3px 3px 0 #062008,4px 4px 12px rgba(0,0,0,0.2)",
    },
    "dermatology": {
        "bg_grad": "radial-gradient(ellipse at 50% 80%,rgba(194,24,91,0.15) 0%,transparent 50%),radial-gradient(ellipse at center,#FCE4EC 0%,#F8BBD0 50%,#F48FB1 100%)",
        "accent": "#C2185B", "accent_light": "#E91E63", "text": "#4A148C",
        "pill_bg": "#C2185B", "pill_text": "#FFFFFF",
        "particle_color": "rgba(194,24,91,0.2)", "particle_count": 12,
        "text_3d_shadows": "1px 1px 0 #880E4F,2px 2px 0 #66003A,3px 3px 0 #440025,4px 4px 12px rgba(0,0,0,0.2)",
    },
    "fashion": {
        "bg_grad": "radial-gradient(ellipse at 70% 30%,rgba(233,69,96,0.15) 0%,transparent 50%),radial-gradient(ellipse at center,#1A1A2E 0%,#16213E 50%,#0F0F1E 100%)",
        "accent": "#E94560", "accent_light": "#FF6B7A", "text": "#FFFFFF",
        "pill_bg": "#E94560", "pill_text": "#FFFFFF",
        "particle_color": "rgba(233,69,96,0.3)", "particle_count": 15,
        "text_3d_shadows": "1px 1px 0 #B03050,2px 2px 0 #8C2040,3px 3px 0 #681030,4px 4px 15px rgba(0,0,0,0.5)",
    },
    "perfumes": {
        "bg_grad": "radial-gradient(ellipse at 50% 30%,rgba(212,175,55,0.15) 0%,transparent 40%),radial-gradient(ellipse at center,#1A1A1A 0%,#0F0F0F 70%,#000000 100%)",
        "accent": "#D4AF37", "accent_light": "#F0D050", "text": "#FFFFFF",
        "pill_bg": "#D4AF37", "pill_text": "#1A1A1A",
        "particle_color": "rgba(212,175,55,0.4)", "particle_count": 18,
        "text_3d_shadows": "1px 1px 0 #B8960C,2px 2px 0 #9C7A0A,3px 3px 0 #806108,4px 4px 0 #644806,5px 5px 0 #483004,6px 6px 15px rgba(0,0,0,0.5)",
    },
    "law_firms": {
        "bg_grad": "radial-gradient(ellipse at 50% 20%,rgba(184,204,224,0.15) 0%,transparent 40%),radial-gradient(ellipse at center,#0E1428 0%,#0A0F1E 70%,#060912 100%)",
        "accent": "#B8CCE0", "accent_light": "#D8E8F5", "text": "#E8EDF5",
        "pill_bg": "#B8CCE0", "pill_text": "#0E1428",
        "particle_color": "rgba(184,204,224,0.2)", "particle_count": 12,
        "text_3d_shadows": "1px 1px 0 #4A7090,2px 2px 0 #2A456E,3px 3px 0 #1A3550,4px 4px 15px rgba(0,0,0,0.5)",
    },
    "real_estate": {
        "bg_grad": "radial-gradient(ellipse at 50% 30%,rgba(212,175,55,0.15) 0%,transparent 40%),radial-gradient(ellipse at center,#0E1428 0%,#0A0F1E 70%,#060912 100%)",
        "accent": "#D4AF37", "accent_light": "#F0D050", "text": "#E8EDF5",
        "pill_bg": "#D4AF37", "pill_text": "#0E1428",
        "particle_color": "rgba(212,175,55,0.25)", "particle_count": 12,
        "text_3d_shadows": "1px 1px 0 #4A7090,2px 2px 0 #2A456E,3px 3px 0 #1A3550,4px 4px 15px rgba(0,0,0,0.5)",
    },
    "auto_shops": {
        "bg_grad": "radial-gradient(ellipse at 50% 100%,rgba(255,107,53,0.15) 0%,transparent 50%),radial-gradient(ellipse at center,#1A1A1A 0%,#0F0F0F 70%,#000000 100%)",
        "accent": "#FF6B35", "accent_light": "#FF9555", "text": "#FFFFFF",
        "pill_bg": "#FF6B35", "pill_text": "#1A1A1A",
        "particle_color": "rgba(255,107,53,0.3)", "particle_count": 15,
        "text_3d_shadows": "1px 1px 0 #CC4515,2px 2px 0 #A03510,3px 3px 0 #802508,4px 4px 15px rgba(0,0,0,0.5)",
    },
    "car_wash": {
        "bg_grad": "radial-gradient(ellipse at 50% 30%,rgba(72,202,228,0.15) 0%,transparent 40%),radial-gradient(ellipse at center,#0A1929 0%,#07121E 70%,#030810 100%)",
        "accent": "#48CAE4", "accent_light": "#72DCEF", "text": "#FFFFFF",
        "pill_bg": "#48CAE4", "pill_text": "#0A1929",
        "particle_color": "rgba(72,202,228,0.4)", "particle_count": 18,
        "text_3d_shadows": "1px 1px 0 #0090B0,2px 2px 0 #006080,3px 3px 0 #004060,4px 4px 15px rgba(0,0,0,0.5)",
    },
    "cleaning": {
        "bg_grad": "radial-gradient(ellipse at 30% 20%,rgba(255,255,255,0.4) 0%,transparent 50%),radial-gradient(ellipse at center,#E8F5E9 0%,#C8E6C9 50%,#A5D6A7 100%)",
        "accent": "#4CAF50", "accent_light": "#66BB6A", "text": "#1B5E20",
        "pill_bg": "#4CAF50", "pill_text": "#FFFFFF",
        "particle_color": "rgba(76,175,80,0.2)", "particle_count": 10,
        "text_3d_shadows": "1px 1px 0 #2E7D32,2px 2px 0 #1B5E20,3px 3px 0 #0D3D10,4px 4px 12px rgba(0,0,0,0.2)",
    },
    "hvac_ac": {
        "bg_grad": "radial-gradient(ellipse at 50% 30%,rgba(72,202,228,0.15) 0%,transparent 40%),radial-gradient(ellipse at center,#0A1929 0%,#07121E 70%,#030810 100%)",
        "accent": "#48CAE4", "accent_light": "#72DCEF", "text": "#FFFFFF",
        "pill_bg": "#48CAE4", "pill_text": "#0A1929",
        "particle_color": "rgba(72,202,228,0.4)", "particle_count": 18,
        "text_3d_shadows": "1px 1px 0 #0090B0,2px 2px 0 #006080,3px 3px 0 #004060,4px 4px 15px rgba(0,0,0,0.5)",
    },
    "event_halls": {
        "bg_grad": "radial-gradient(ellipse at 50% 30%,rgba(212,175,55,0.15) 0%,transparent 40%),radial-gradient(ellipse at center,#2D1B3D 0%,#1A0F28 60%,#0F0818 100%)",
        "accent": "#D4AF37", "accent_light": "#F0D050", "text": "#FFFFFF",
        "pill_bg": "#D4AF37", "pill_text": "#2D1B3D",
        "particle_color": "rgba(212,175,55,0.35)", "particle_count": 20,
        "text_3d_shadows": "1px 1px 0 #8C6A2E,2px 2px 0 #6C5020,3px 3px 0 #4C3815,4px 4px 15px rgba(0,0,0,0.5)",
    },
    "training_centers": {
        "bg_grad": "radial-gradient(ellipse at 50% 20%,rgba(92,107,192,0.15) 0%,transparent 40%),radial-gradient(ellipse at center,#0E1428 0%,#0A0F1E 70%,#060912 100%)",
        "accent": "#5C6BC0", "accent_light": "#7E8EE0", "text": "#E8EDF5",
        "pill_bg": "#5C6BC0", "pill_text": "#FFFFFF",
        "particle_color": "rgba(92,107,192,0.25)", "particle_count": 12,
        "text_3d_shadows": "1px 1px 0 #3949AB,2px 2px 0 #2A3890,3px 3px 0 #1A286E,4px 4px 15px rgba(0,0,0,0.5)",
    },
}

def _get_colors(niche):
    return NICHE_COLORS.get(niche, NICHE_COLORS["restaurants"])


def _particles(c, seed=0):
    """Generate floating particle HTML elements."""
    random.seed(seed)
    html = ""
    for i in range(c.get("particle_count", 12)):
        x = random.randint(2, 98)
        y = random.randint(2, 95)
        size = random.randint(3, 8)
        opacity = random.uniform(0.2, 0.6)
        shape = random.choice(["circle", "circle", "square", "diamond"])
        if shape == "circle":
            html += f'<div style="position:absolute;width:{size}px;height:{size}px;background:{c["particle_color"]};border-radius:50%;top:{y}%;left:{x}%;opacity:{opacity:.1f};z-index:2;"></div>'
        elif shape == "square":
            html += f'<div style="position:absolute;width:{size}px;height:{size}px;background:{c["particle_color"]};border-radius:2px;top:{y}%;left:{x}%;opacity:{opacity:.1f};z-index:2;transform:rotate(45deg);"></div>'
        else:
            html += f'<div style="position:absolute;width:{size}px;height:{size}px;background:{c["particle_color"]};top:{y}%;left:{x}%;opacity:{opacity:.1f};z-index:2;transform:rotate(45deg);"></div>'
    return html


def _wrap(body, c):
    css = f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1080px; overflow:hidden;
  font-family:'Noto Sans Arabic',sans-serif; -webkit-font-smoothing:antialiased; }}
.stage {{ position:relative; width:1080px; height:1080px; overflow:hidden;
  background:{c['bg_grad']}; }}
.stage::after {{ content:''; position:absolute; inset:0;
  background-image:linear-gradient(rgba(0,0,0,0.03) 1px,transparent 1px),
    linear-gradient(90deg,rgba(0,0,0,0.03) 1px,transparent 1px);
  background-size:40px 40px; pointer-events:none; z-index:1; }}
.display {{ font-family:'Noto Kufi Arabic',serif; font-weight:900; line-height:1.2;
  direction:rtl; word-break:keep-all; }}
.body-ar {{ font-family:'Noto Sans Arabic',sans-serif; font-size:24px; line-height:1.6;
  direction:rtl; word-break:keep-all; }}
.label {{ font-family:'Lato',sans-serif; font-size:15px; font-weight:700;
  letter-spacing:0.2em; text-transform:uppercase; color:{c['accent']}; }}
.pill {{ display:inline-block; background:{c['pill_bg']}; color:{c['pill_text']};
  padding:10px 24px; border-radius:50px; font-size:17px; font-weight:600;
  font-family:'Noto Sans Arabic',sans-serif; white-space:nowrap;
  box-shadow:0 4px 15px rgba(0,0,0,0.15); }}
"""
    return f"""<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;700;900&family=Noto+Sans+Arabic:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>{css}</style></head><body>{body}</body></html>"""


def _footer(data, c):
    return f"""<div style="display:flex;justify-content:space-between;align-items:baseline;width:100%;gap:16px;padding-top:10px;
  border-top:1px solid {c['accent']}30;">
  <span style="font-family:'Noto Mono',monospace;font-size:16px;color:{c['accent']};opacity:0.6;">{data.get('domain','nuhoot.xyz')}</span>
  <span style="font-size:18px;color:{c['accent']};opacity:0.7;">{data.get('brand_ar','نُهوت — التسويق الرقمي')}</span>
</div>"""


# ═══════════════════════════════════════════════════════
# TEMPLATE 1: HERO CUTOUT — 3D headline + floating photo + particles
# ═══════════════════════════════════════════════════════
def tpl_hero_alive(b64, data, obj_pos, c, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    trust = data.get("trust_badge", "")
    rating = data.get("rating", "٤٫٧")
    reviews = _to_arabic(data["reviews"])
    return _wrap(f"""<div class="stage">
  {_particles(c, seed=42)}
  <!-- Top: kicker + 3D headline -->
  <div style="position:absolute;top:50px;left:0;right:0;padding:0 50px;text-align:right;z-index:10;">
    <span class="label">{data.get('kicker','')}</span>
    <h1 class="display" style="font-size:58px;color:{c['text']};margin-top:8px;
      text-shadow:{c['text_3d_shadows']};">{data['headline']}</h1>
  </div>
  <!-- Business name badge -->
  <div style="position:absolute;top:185px;right:50px;z-index:10;">
    <span style="background:{c['accent']};color:{c['pill_text']};padding:6px 20px;
      border-radius:50px;font-size:20px;font-weight:700;font-family:'Noto Kufi Arabic',serif;
      box-shadow:0 4px 15px rgba(0,0,0,0.2);">{data['business_name']}</span>
  </div>
  <!-- Center: photo in soft-edged frame with depth shadow -->
  <div style="position:absolute;top:250px;left:50%;transform:translateX(-50%);width:680px;height:460px;
    border-radius:24px;overflow:hidden;z-index:5;
    box-shadow:0 30px 80px rgba(0,0,0,0.3),0 10px 30px rgba(0,0,0,0.2);
    mask-image:radial-gradient(ellipse 95% 95% at center,black 70%,transparent 100%);
    -webkit-mask-image:radial-gradient(ellipse 95% 95% at center,black 70%,transparent 100%);">
    <img src="data:image/jpeg;base64,{b64}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};">
  </div>
  <!-- Bottom: pills + rating + footer -->
  <div style="position:absolute;bottom:0;left:0;right:0;padding:0 50px 35px;
    display:flex;flex-direction:column;gap:14px;align-items:flex-end;z-index:10;">
    <div style="display:flex;gap:10px;flex-wrap:wrap;justify-content:flex-end;">
      <span class="pill">{t1}</span>
      <span class="pill">{t2}</span>
      <span class="pill">{t3}</span>
    </div>
    <div style="display:flex;align-items:center;gap:12px;direction:rtl;" dir="rtl">
      <span style="color:{c['accent']};font-size:22px;">★★★★<span style="opacity:0.3">★</span></span>
      <span style="font-size:28px;font-weight:800;color:{c['text']};">{rating}</span>
      <span style="font-size:18px;color:{c['accent']};opacity:0.7;">{reviews} تقييم</span>
    </div>
    {f'<div style="font-size:16px;color:{c["accent"]};opacity:0.8;">✦ {trust}</div>' if trust else ''}
    {_footer(data, c)}
  </div>
</div>""", c)


# ═══════════════════════════════════════════════════════
# TEMPLATE 2: SPLIT DEPTH — photo with soft edge + 3D text panel
# ═══════════════════════════════════════════════════════
def tpl_split_alive(b64, data, obj_pos, c, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    trust = data.get("trust_badge", "")
    rating = data.get("rating", "٤٫٧")
    reviews = _to_arabic(data["reviews"])
    return _wrap(f"""<div class="stage" style="display:flex;">
  {_particles(c, seed=99)}
  <!-- Left: photo with diagonal soft edge -->
  <div style="width:52%;height:100%;position:relative;overflow:hidden;z-index:5;
    clip-path:polygon(0 0,100% 0,85% 100%,0 100%);
    box-shadow:15px 0 60px rgba(0,0,0,0.3);">
    <img src="data:image/jpeg;base64,{b64}" style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};">
    <div style="position:absolute;top:30px;right:30px;">
      <span class="label" style="color:#FFFFFF;text-shadow:0 2px 10px rgba(0,0,0,0.6);">{data.get('kicker','')}</span>
    </div>
  </div>
  <!-- Right: content panel -->
  <div style="width:48%;height:100%;display:flex;flex-direction:column;
    justify-content:center;gap:18px;padding:50px 40px;align-items:flex-end;text-align:right;z-index:10;">
    <span style="font-family:'Noto Kufi Arabic',serif;font-size:22px;font-weight:500;color:{c['accent']};">{data['business_name']}</span>
    <h1 class="display" style="font-size:48px;color:{c['text']};
      text-shadow:{c['text_3d_shadows']};">{data['headline']}</h1>
    <div style="width:60px;height:3px;background:{c['accent']};border-radius:2px;"></div>
    <div style="display:flex;flex-direction:column;gap:8px;align-items:flex-end;">
      <span class="pill" style="font-size:15px;">{t1}</span>
      <span class="pill" style="font-size:15px;">{t2}</span>
      <span class="pill" style="font-size:15px;">{t3}</span>
    </div>
    <div style="display:flex;align-items:center;gap:12px;direction:rtl;" dir="rtl">
      <span style="color:{c['accent']};font-size:22px;">★★★★<span style="opacity:0.3">★</span></span>
      <span style="font-size:26px;font-weight:800;color:{c['text']};">{rating}</span>
      <span style="font-size:17px;color:{c['accent']};opacity:0.7;">{reviews} تقييم</span>
    </div>
    {f'<div style="font-size:15px;color:{c["accent"]};opacity:0.8;">✦ {trust}</div>' if trust else ''}
    {_footer(data, c)}
  </div>
</div>""", c)


# ═══════════════════════════════════════════════════════
# TEMPLATE 3: FULL-BLEED STORY — photo bg + glass card + particles
# ═══════════════════════════════════════════════════════
def tpl_story_alive(b64, data, obj_pos, c, photos_b64=None):
    t1, t2, t3 = data["taglines"]
    trust = data.get("trust_badge", "")
    rating = data.get("rating", "٤٫٧")
    reviews = _to_arabic(data["reviews"])
    return _wrap(f"""<div class="stage">
  <img src="data:image/jpeg;base64,{b64}" style="position:absolute;inset:0;width:100%;height:100%;
    object-fit:cover;object-position:{obj_pos};filter:brightness(0.65);z-index:1;">
  <div style="position:absolute;inset:0;z-index:2;
    background:linear-gradient(0deg,{c['bg_grad'].split(',')[0]} 0%,rgba(0,0,0,0.3) 40%,transparent 70%);"></div>
  {_particles(c, seed=77)}
  <!-- Top kicker -->
  <div style="position:absolute;top:50px;right:50px;z-index:10;">
    <span class="label" style="color:#FFFFFF;text-shadow:0 2px 10px rgba(0,0,0,0.6);">{data.get('kicker','')}</span>
  </div>
  <!-- Bottom: glass card with content -->
  <div style="position:absolute;bottom:0;left:0;right:0;padding:40px 50px 35px;z-index:10;
    background:linear-gradient(0deg,rgba(0,0,0,0.85) 0%,rgba(0,0,0,0.5) 60%,transparent 100%);
    display:flex;flex-direction:column;gap:14px;align-items:flex-end;">
    <span style="font-family:'Noto Kufi Arabic',serif;font-size:24px;font-weight:500;color:{c['accent_light']};">{data['business_name']}</span>
    <h1 class="display" style="font-size:52px;color:#FFFFFF;
      text-shadow:0 4px 20px rgba(0,0,0,0.8),{c['text_3d_shadows']};">{data['headline']}</h1>
    <div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end;">
      <span class="pill" style="font-size:15px;">{t1}</span>
      <span class="pill" style="font-size:15px;">{t2}</span>
    </div>
    <div style="display:flex;align-items:center;gap:12px;direction:rtl;" dir="rtl">
      <span style="color:{c['accent_light']};font-size:22px;">★★★★<span style="opacity:0.3">★</span></span>
      <span style="font-size:28px;font-weight:800;color:#FFFFFF;">{rating}</span>
      <span style="font-size:18px;color:rgba(255,255,255,0.7);">{reviews} تقييم</span>
    </div>
    {f'<div style="font-size:15px;color:{c["accent_light"]};">✦ {trust}</div>' if trust else ''}
    {_footer(data, {**c, 'accent': c['accent_light']})}
  </div>
</div>""", c)


# ═══════════════════════════════════════════════════════
# REGISTRY
# ═══════════════════════════════════════════════════════
TEMPLATES = {
    1: ("Hero Alive", tpl_hero_alive),
    2: ("Split Depth", tpl_split_alive),
    3: ("Story Alive", tpl_story_alive),
}


def generate_html(template_id, photo_path, data, obj_pos="50% 50%", niche="restaurants", photo_paths=None):
    c = _get_colors(niche)
    b64 = _photo_b64(photo_path)
    name, func = TEMPLATES[template_id]
    return func(b64, data, obj_pos, c)
