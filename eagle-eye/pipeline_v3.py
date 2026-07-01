#!/usr/bin/env python3
"""
Nuhoot Eagle-Eye Pipeline v3 — Dynamic Design Engine
====================================================
Kimi K2.7 generates COMPLETE design blueprints (component composition) →
DynamicComposer renders → OpenCV measures → Tesseract verifies → 
Kimi sees result → fixes → re-renders → repeat.

Key difference from v2:
- v2: Kimi changes text + colors on ONE hardcoded template
- v3: Kimi picks WHICH components to use and HOW to arrange them
      Each business gets a genuinely UNIQUE layout
"""

import json, time, base64, re, os, sys, subprocess, shutil
import requests
import cv2
import numpy as np
from PIL import Image, ImageDraw
from photo_db import (
    get_photo_catalog_text, resolve_photo_id, mark_used, record_composite,
)

# ─── Config ─────────────────────────────────────────────────
API_KEY = "sk-WxllgGhf4ZGSfEJ75mJYyDwjuVKP9SlrAP03m4_SUQs"
API_URL = "https://api.code.umans.ai/v1/chat/completions"
MODEL = "umans-kimi-k2.7"
RENDER_DIR = "/tmp/nuhoot-eagle-eye-v3"
REMOTION_DIR = "/opt/nuhoot/remotion"
CAPTIONS_PATH = "/opt/nuhoot/remotion/captions.json"
CHROMIUM = "/snap/chromium/current/usr/lib/chromium-browser/chrome"
MAX_ITERATIONS = 2
QUALITY_THRESHOLD = 0.75

MALE_NICHES = ['barbershops', 'gyms', 'auto_shops']
FEMALE_NICHES = ['salons', 'spas', 'dermatology', 'fashion']

BUSINESS_NAMES = {
    "restaurants": "مطعم النخيل الذهبي", "cafes": "قهوة الصباح",
    "bakeries": "مخبز الحلو", "salons": "صالون لمسة جمال",
    "spas": "سبا الورد", "barbershops": "حلاقة الذوق الرفيع",
    "gyms": "جيم القوة والعافية", "clinics": "عيادة الشفاء التخصصية",
    "dentists": "مركز الابتسامة", "pharmacies": "صيدلية الرعاية",
    "dermatology": "مركز الجلدية", "fashion": "دار الأناقة",
    "perfumes": "دار العطور الفاخرة", "law_firms": "مكتب العدالة",
    "real_estate": "عقارات الرياض", "auto_shops": "ورشة المحترف",
    "car_wash": "غسيل لمعان", "cleaning": "نظافة النخبة",
    "hvac_ac": "تبريد الرياض", "event_halls": "قاعة الأحلام",
    "training_centers": "مركز التميز",
}

# ─── Component Catalog (for Kimi's prompt) ─────────────────
COMPONENT_CATALOG = """
AVAILABLE COMPONENTS (76 total) — pick 5-8 to compose a UNIQUE design.
Each component has EXACT prop names — use them precisely.

HEADERS (pick 1):
- HeaderMinimal: kicker, headline, businessName
- HeaderGradient: kicker, headline, businessName (gradient background band)
- HeaderSplit: kicker, headline, businessName (headline left, name right)
- HeaderOverlay: kicker, headline, businessName, photoPath (photo background)
- HeaderMixed: kicker, headline, accentWord, businessName (multi-font, gold/gradient accent word)

PHOTOS (pick 1, fills middle of design):
- PhotoSingle: src (e.g. "photos/restaurants.jpg"), showOverlay (true/false)
- PhotoFrame: src, caption, showOverlay
- PhotoGrid: photos (array of 2-4 paths)
- PhotoMosaic: photos (array of exactly 3 paths)
- PhotoArch: src, width, height (arch-shaped mask — for salons/spas/real_estate)
- PhotoCircle: src, size (large circular photo — for salons/testimonials)
- PhotoDiagonal: src, direction ("left"/"right") (diagonal-cut — for gyms/auto)
- PhotoDuotone: src, shadowColor, highlightColor (two-color gradient overlay)
- PhotoDoubleFrame: src, outerColor, innerColor (double-framed — luxury)
- FramePolaroid: src, caption (polaroid-style frame)
- FrameStack: photos (array of 2-3 paths)
- FrameCircle: src, size (small circular framed photo)

CONTENT (pick 1-2):
- ContentStats: stats (array of {number, label, unit?}), glass (true/false), sizeGradient (true/false)
- ContentCards: items (array of {title, description}), glass (true/false)
- ContentList: items (array of strings), bulletStyle ("diamond"/"dot"/"arrow"/"check"/"star")
- ContentQuotes: quote, author, rating, glass (true/false)
- ContentFeatures: features (array of {icon, title, description} — icon is Lucide name like "star","heart","check","shield","clock","phone","scissors","sparkles","coffee","utensils","dumbbell","stethoscope","pill","smile","droplet","flame","crown","award","zap","home","key","wrench","car","wind","thermometer","graduation-cap","briefcase","scale","shirt","cookie","leaf")

CTAS (pick 1):
- CTAButton: text (e.g. "← احجز الآن"), useAccentShadow (true)
- CTABanner: text, subText
- CTAInline: text, underline ("solid"/"dashed"/"glow")
- CTAShimmer: text, iconName (premium shimmer — for restaurants/events)
- CTAGlow: text, iconName (glowing — for gyms/auto/tech)
- CTAOutline: text (outlined — for clinics/law)
- CTADual: text, subText, iconName (dual-line — for salons/fashion)

BADGES (pick 1-2):
- StatusBadge: text, iconName
- RatingBadge: rating, reviews
- TrustBadge: text, iconName
- DiscountBadge: percentage (number)
- SealBadge: text, subText (circular stamp/seal — for authenticity)
- OfferRibbon: text, position ("top-right"/"top-left") (diagonal ribbon)

PRICING (optional):
- PriceTag: price, currency, oldPrice
- PriceStrike: newPrice, oldPrice, currency, discountPercent
- PriceCard: title, price, oldPrice, description, discountPercent

DECORATIVE (pick 1-2 — MUST include at least 1):
- DecorShapes: (no props — auto-scatters circles/diamonds)
- DecorRings: (no props — concentric rings)
- DecorWatermark: text, fontSize (faint background text)
- DecorGradient: position ("top"/"bottom"/"full")
- Divider: centerChar (default "◆") (accent line with decorative center)
- EdgeLabel: text, side ("left"/"right") (rotated vertical text on edge)
- DecorVignette: intensity (0-1) (radial darkening at edges)
- DecorDiagonal: angle, lineWidth (diagonal accent line)
- ColorPanel: position, size, opacity (solid color section background)
- DecorCalligraphy: size, opacity (Arabic calligraphic stroke)

PATTERNS (pick 1 — MUST include at least 1):
- PatternGrid: cellSize, opacity (grid lines — for clinics/tech)
- PatternDots: spacing, opacity (dot matrix)
- PatternHex: size, opacity (hexagons — for gyms/industrial)
- PatternRays: count, opacity (radiating light rays — for events/restaurants)
- PatternBokeh: count, opacity (floating bokeh circles — for salons/spas/beauty)
- TextureGrain: intensity (noise/grain overlay — for paper texture)
- PatternIslamic: size, opacity (Islamic geometric 8-point star — for perfumes/law/events)
- TextureOverlay: type ("silk"/"metal"/"paper"/"carbon"/"marble") (niche texture)

FRAMES (optional):
- CornerBrackets: length, thickness, corners (L-shaped corner decorations)
- FrameKeyline: borderWidth, inset (thin border frame around canvas)

SOCIAL (optional):
- SocialBar: platforms (array like ["whatsapp","instagram","snapchat","tiktok"])
- ContactRow: phone, location, hours

PROGRESS (optional):
- BarProgress: value, label
- RingProgress: value, centerText
- GoalMeter: current, goal, label, unit

FOOTERS (pick 1, ALWAYS required):
- FooterComplete: rating, reviews, trustBadge, hashtags (array of strings)
- FooterRating: rating, reviews, trustBadge
- FooterHashtags: hashtags (array)
- FooterBranding: (no props)
"""
# ─── Kimi Design Generation ─────────────────────────────────
def kimi_chat(messages, max_tokens=4000, temperature=0.7):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": MODEL, "messages": messages, "max_tokens": max_tokens, "temperature": temperature}
    for attempt in range(3):
        try:
            r = requests.post(API_URL, headers=headers, json=payload, timeout=180)
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"].strip()
            elif r.status_code == 429:
                wait = 15 * (attempt + 1)  # 15s, 30s, 45s
                print(f"    ⏳ Rate limited, waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"    API error {r.status_code}: {r.text[:100]}")
                time.sleep(5)
        except Exception as e:
            print(f"    API exception: {e}")
            time.sleep(5)
    return None

def kimi_see(image_path, prompt, max_tokens=3000):
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    return kimi_chat([
        {"role": "system", "content": "You are a design critic. Respond with ONLY a JSON object. No explanation outside the JSON."},
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
                {"type": "text", "text": prompt}
            ]
        }
    ], max_tokens=max_tokens, temperature=0.4)

# ─── JSON Extraction ───────────────────────────────────────
def extract_json(text):
    if not text:
        return None
    # Strategy 1: Extract from ```json ... ``` code blocks
    match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except:
            pass
    # Strategy 2: Find JSON by looking for known keys
    # Kimi often generates reasoning before the JSON, so search for
    # the actual JSON object by looking for known root keys.
    for key in ['{"designPattern"', '{"composition"', '{"score"']:
        pos = text.rfind(key)  # Use rfind to get the LAST occurrence
        if pos != -1:
            # Match balanced braces from this position
            depth = 0
            in_string = False
            escape = False
            for i in range(pos, len(text)):
                ch = text[i]
                if escape:
                    escape = False
                    continue
                if ch == '\\':
                    escape = True
                    continue
                if ch == '"':
                    in_string = not in_string
                    continue
                if in_string:
                    continue
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0:
                        candidate = text[pos:i+1]
                        try:
                            return json.loads(candidate)
                        except:
                            cleaned = re.sub(r',\s*}', '}', candidate)
                            cleaned = re.sub(r',\s*]', ']', cleaned)
                            try:
                                return json.loads(cleaned)
                            except:
                                pass
                        break
    # Strategy 3: Try every { position as a last resort
    first = text.find('{')
    while first != -1:
        depth = 0
        in_string = False
        escape = False
        for i in range(first, len(text)):
            ch = text[i]
            if escape:
                escape = False
                continue
            if ch == '\\':
                escape = True
                continue
            if ch == '"':
                in_string = not in_string
                continue
            if in_string:
                continue
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    candidate = text[first:i+1]
                    try:
                        data = json.loads(candidate)
                        # Only accept if it has expected keys
                        if 'composition' in data or 'score' in data or 'designPattern' in data:
                            return data
                    except:
                        pass
                    break
        first = text.find('{', first + 1)
    return None

# ─── OpenCV + Tesseract (reused from v2) ──────────────────
def analyze_design(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return {"overall": 0.5}
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)
    contrast = np.std(gray)
    top_region = gray[40:200, :]
    mid_region = gray[600:880, :]
    bottom_region = gray[900:1050, :]
    scores = {
        "brightness": min(1.0, brightness / 128.0) if brightness > 20 else 0.3,
        "contrast": min(1.0, contrast / 60.0),
        "header_text": min(1.0, np.std(top_region) / 50.0),
        "body_text": min(1.0, np.std(mid_region) / 50.0),
        "footer_text": min(1.0, np.std(bottom_region) / 50.0),
    }
    zone_h, zone_w = h // 3, w // 3
    zones = [np.std(gray[r*zone_h:(r+1)*zone_h, c*zone_w:(c+1)*zone_w]) for r in range(3) for c in range(3)]
    scores["balance"] = max(0.0, 1.0 - (np.std(zones) / (np.mean(zones) + 1)))
    scores["overall"] = float(np.mean(list(scores.values())))
    scores["brightness_raw"] = float(brightness)
    scores["contrast_raw"] = float(contrast)
    return scores

def check_arabic_text(image_path):
    try:
        import pytesseract
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='ara')
        arabic_chars = re.findall(r'[\u0600-\u06FF]', text)
        return {
            "arabic_char_count": len(arabic_chars),
            "score": min(1.0, len(arabic_chars) / 80.0) if arabic_chars else 0.0
        }
    except:
        return {"score": 0.5, "arabic_char_count": 0}

# ─── Blueprint Normalization ──────────────────────────────
def normalize_blueprint(blueprint):
    """Fix common prop-name mismatches Kimi might produce."""
    if not blueprint or "composition" not in blueprint:
        return blueprint
    # All photo components that use "src" prop
    SRC_PHOTOS = {"PhotoSingle", "PhotoFrame", "PhotoArch", "PhotoCircle",
                  "PhotoDiagonal", "PhotoDuotone", "PhotoDoubleFrame",
                  "FramePolaroid", "FrameCircle", "HeaderOverlay"}
    # All photo components that use "photos" array prop
    ARRAY_PHOTOS = {"PhotoGrid", "PhotoMosaic", "FrameStack"}
    for block in blueprint["composition"]:
        comp = block.get("component", "")
        props = block.get("props", {})
        # Single-photo components: photoPath → src
        if comp in SRC_PHOTOS:
            if "photoPath" in props and "src" not in props:
                props["src"] = props.pop("photoPath")
        # Multi-photo components: collect photoPathN → photos array
        if comp in ARRAY_PHOTOS:
            if "photos" not in props:
                photos = []
                for key in sorted(props.keys()):
                    if key.startswith("photoPath"):
                        photos.append(props[key])
                if photos:
                    props["photos"] = photos
                    for key in list(props.keys()):
                        if key.startswith("photoPath"):
                            del props[key]
        # Resolve photo IDs → file paths
        niche = blueprint.get("_niche", "")
        if comp in SRC_PHOTOS:
            src_val = props.get("src", "")
            if src_val and not src_val.startswith("photos/") and not src_val.startswith("/"):
                resolved = resolve_photo_id(src_val, niche)
                props["src"] = resolved
                mark_used(src_val)
        if comp in ARRAY_PHOTOS:
            photo_list = props.get("photos", [])
            resolved_list = []
            for pid in photo_list:
                if pid and not pid.startswith("photos/") and not pid.startswith("/"):
                    resolved = resolve_photo_id(pid, niche)
                    resolved_list.append(resolved)
                    mark_used(pid)
                else:
                    resolved_list.append(pid)
            props["photos"] = resolved_list
        # FooterComplete: remove businessName (not a valid prop)
        if comp == "FooterComplete":
            props.pop("businessName", None)
        # Remove "colors" from props — system injects from globalStyles
        props.pop("colors", None)
    return blueprint

# ─── Render via DynamicComposer ────────────────────────────
def render_blueprint(blueprint, output_path):
    """Render a design blueprint using DynamicComposer."""
    blueprint = normalize_blueprint(blueprint)
    props = json.dumps({"blueprint": blueprint}, ensure_ascii=False)
    cmd = [
        "npx", "remotion", "still", "src/index.ts", "dynamic", output_path,
        f"--props={props}",
        f"--browser-executable={CHROMIUM}",
        "--log=error"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=REMOTION_DIR, timeout=60)
    if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
        return True
    if result.stderr:
        print(f"    Render error: {result.stderr[:200]}")
    return False

# ─── Kimi Design Generation ─────────────────────────────────
EXAMPLE_BLUEPRINT = """EXAMPLE BLUEPRINT format:
{
  "designPattern": "name",
  "composition": [
    {"id": "h1", "component": "HeaderGradient", "props": {"kicker": "RIYADH · COFFEE", "headline": "أفضل قهوة في الرياض", "businessName": "قهوة الصباح"}},
    {"id": "p1", "component": "PhotoSingle", "props": {"src": "photos/cafes.jpg"}},
    {"id": "c1", "component": "CTAButton", "props": {"text": "← زورونا اليوم"}},
    {"id": "f1", "component": "FooterComplete", "props": {"rating": 4.8, "reviews": 215, "trustBadge": "مختارة بعناية", "hashtags": ["#قهوة_الرياض","#صباح_الخير"]}}
  ],
  "globalStyles": {"backgroundColor": "#1A1A2E", "primaryColor": "#E94560", "accentColor": "#D4AF37", "color": "#FFFFFF", "direction": "rtl"}
}
"""


def generate_blueprint(niche, business_name, rating, reviews, photo_path, feedback=None):
    """Have Kimi generate a complete design blueprint for a business."""
    from niche_config import get_niche_config, get_gender_for_niche, NICHE_COLORS, GENDER_TEXTS
    
    config = get_niche_config(niche)
    gender = config.get("gender", "plural")
    gender_word = GENDER_TEXTS.get(gender, GENDER_TEXTS["plural"]).get("you_want", "تبون")
    
    # Get assigned components from niche config
    assigned_layout = config.get("layout_pattern", "LayoutStandard")
    assigned_font = config.get("font", "kufi")
    assigned_pattern = config.get("pattern", "PatternBokeh")
    assigned_cta = config.get("cta_variant", "CTAButton")
    assigned_photo = config.get("photo_component", "PhotoSingle")
    assigned_header = config.get("header_variant", "HeaderGradient")
    assigned_decorative = config.get("decorative", ["DecorShapes"])
    assigned_icons = config.get("default_icons", ["star"])
    assigned_texture = config.get("texture", "paper")
    assigned_radius = config.get("corner_radius", 16)
    gradient_angle = config.get("gradient_angle", 135)
    type_scale = config.get("type_scale", 1.333)
    
    # Get niche colors
    colors = NICHE_COLORS.get(niche, {"bg": "#1A1A2E", "bg2": "#16213E", "accent": "#E94560", "accent2": "#D4AF37"})
    
    # Load existing captions as reference
    with open(CAPTIONS_PATH) as f:
        captions = json.load(f)
    existing = captions.get(niche, {})
    
    # Build the recommended components list
    recommended_decorative = ", ".join(assigned_decorative[:2]) if assigned_decorative else "DecorShapes"
    recommended_icon_str = ", ".join(f'"{ic}"' for ic in assigned_icons[:3])
    
    base_prompt = f"""You are an expert Saudi social media designer. Create a COMPLETE design for a social media ad post.

BUSINESS CONTEXT:
- Name: {business_name}
- Niche: {niche}
- City: Riyadh, Saudi Arabia
- Rating: {rating}/5 ({reviews} reviews)
- Photo: {photo_path}
- Target audience: {gender} — use "{gender_word}" for addressing

{get_photo_catalog_text(niche)}

{COMPONENT_CATALOG}

MANDATORY DESIGN ASSIGNMENT (follow these exactly):
- LAYOUT: Use {assigned_layout} as your design structure
- HEADER: Use {assigned_header} component (font: {assigned_font})
- PHOTO: Use {assigned_photo} component. Set src to a photo ID from the AVAILABLE PHOTOS list above (e.g. "src": "restaurants_01"). For PhotoGrid/Mosaic/FrameStack, set "photos" to an array of 2-3 IDs.
- PATTERN: Include {assigned_pattern} as a decorative background
- CTA: Use {assigned_cta} component
- DECORATIVE: Include {recommended_decorative}
- For ContentFeatures, use Lucide icon names: {recommended_icon_str}
- If using ContentStats or ContentCards, set glass=true for premium look
- If using ContentList, set bulletStyle="diamond"

DESIGN RULES (CRITICAL — follow ALL):
1. Pick exactly 5-8 components total. Each design MUST include:
   - 1 header (use the assigned one above)
   - 1 photo (use the assigned one above)
   - 1 pattern component (use the assigned one above)
   - 1 decorative component (use the assigned one above)
   - 1 CTA (use the assigned one above)
   - 1 footer (FooterComplete recommended)
   - Optional: 1 content block, 1 badge
2. VARY the component sequence — NOT always Header→Photo→Content→CTA→Footer.
   Try: Pattern+Decorative first (as background), then Header, Photo, Content, CTA, Footer.
   Or: Header, Photo, Stats, CTA, Footer (skip content).
   Or: Photo first (full-bleed), then Header overlay, CTA, Footer.
3. Arabic text must be authentic Saudi dialect
4. Use RTL direction for all Arabic text
5. Colors: backgroundColor="{colors['bg']}", primaryColor="{colors['accent']}", accentColor="{colors['accent2']}", color="#FFFFFF"
   - Background MUST be dark (between #0A0A0A and #2A2A3A). Light backgrounds FAIL.
6. Headlines under 60 chars, CTAs under 35 chars
7. For photos use "src" prop with a photo ID from the AVAILABLE PHOTOS list (e.g. "src": "restaurants_01"). Do NOT use "photos/{niche}.jpg" directly — always pick an ID.
8. Set gradientAngle to {gradient_angle} in globalStyles

ARABIC GENDER RULES:
- Verbs get female ي suffix: يخليك → يخليكي (for female audience)
- Prepositions do NOT: لك stays لك (NOT لكي)
- Possessives do NOT: يومك stays يومك (NOT يومكي)
- نعطيك/تعطيك stay same for female
- Saudi: "ما تنسى" not "لا تنس"

CRITICAL: Output ONLY the JSON object. No explanation, no reasoning, no text before or after the JSON.
Start your response with {{ and end with }}.

{EXAMPLE_BLUEPRINT}IMPORTANT:
- Do NOT include "colors" in props — the system injects them from globalStyles
- PhotoSingle/PhotoArch/PhotoCircle/PhotoDiagonal/PhotoDuotone/PhotoDoubleFrame use "src" prop
- PhotoGrid/PhotoMosaic/FrameStack use "photos" array prop
- FooterComplete does NOT take businessName
- Every blueprint MUST have: 1 header, 1 photo, 1 pattern, 1 decorative, 1 CTA, 1 footer
- Use Arabic text for all content
- Pattern and decorative components should be placed FIRST in the composition (they render behind content)

Existing text for reference (you can improve it):
{json.dumps(existing, ensure_ascii=False, indent=2)}
"""

    if feedback:
        base_prompt += f"""

ISSUES FROM PREVIOUS ITERATION (fix these):
{feedback}

Output the FIXED blueprint as JSON only."""

    response = kimi_chat([
        {"role": "system", "content": "You are a JSON-only design generator. Output ONLY a valid JSON object. No thinking, no reasoning, no explanation, no markdown. Start your response with { and end with }."},
        {"role": "user", "content": "Create a design for a cafe in Riyadh. Use HeaderGradient, PhotoSingle, CTAButton, FooterComplete."},
        {"role": "assistant", "content": '{"designPattern":"warm-cafe","composition":[{"id":"h1","component":"HeaderGradient","props":{"kicker":"RIYADH · COFFEE","headline":"أفضل قهوة في الرياض","businessName":"قهوة الصباح"}},{"id":"p1","component":"PhotoSingle","props":{"src":"photos/cafes.jpg"}},{"id":"c1","component":"CTAButton","props":{"text":"← زورونا اليوم"}},{"id":"f1","component":"FooterComplete","props":{"rating":4.8,"reviews":215,"trustBadge":"مختارة بعناية","hashtags":["#قهوة_الرياض","#صباح_الخير"]}}],"globalStyles":{"backgroundColor":"#1A1A2E","primaryColor":"#E94560","accentColor":"#D4AF37","color":"#FFFFFF","direction":"rtl"}}'},
        {"role": "user", "content": base_prompt}
    ], max_tokens=6000, temperature=0.3)
    if not response:
        return None
    
    data = extract_json(response)
    if data and "composition" in data:
        return data
    
    print(f"    ⚠️ Blueprint extraction failed. Raw: {response[:200]}")
    return None

# ─── Kimi Vision Critique ──────────────────────────────────
def critique_design(image_path, niche, blueprint):
    prompt = f"""You are reviewing a {niche} social media ad design.

Rate the design quality 0.0-1.0 and list ALL issues:
1. Is Arabic text readable and correctly rendered?
2. Are components arranged well (no overlaps, good spacing)?
3. Is the color scheme appropriate for {niche}?
4. Is the layout balanced (no large empty areas)?
5. Is the CTA clear and visible?
6. Any visual issues?

Respond in JSON only:
{{"score": 0.0-1.0, "issues": ["issue 1", "issue 2"], "severity": "none|minor|major|critical", "fixes": ["what to fix 1", "what to fix 2"]}}"""

    # Use few-shot approach for better JSON output
    response = kimi_chat([
        {"role": "system", "content": "You are a design critic. Respond with ONLY a JSON object. No thinking, no reasoning. Start with { and end with }."},
        {"role": "user", "content": "Review this design. Rate it 0-1 and list issues."},
        {"role": "assistant", "content": '{"score": 0.75, "issues": ["header text slightly small", "photo could be larger"], "severity": "minor", "fixes": ["increase header font size", "expand photo area"]}'},
        {"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64.b64encode(open(image_path, 'rb').read()).decode()}"}},
            {"type": "text", "text": prompt}
        ]}
    ], max_tokens=2000, temperature=0.3)
    if not response:
        return {"score": 0.5, "issues": [], "fixes": []}    
    data = extract_json(response)
    if data:
        return data
    
    score_match = re.search(r'"score"\s*:\s*([\d.]+)', response)
    try:
        score = float(score_match.group(1)) if score_match else 0.5
    except (ValueError, AttributeError):
        score = 0.5
    return {"score": score, "issues": ["Could not parse critique"], "fixes": []}

# ─── Before/After Comparison ───────────────────────────────
def create_comparison(niche, before_path, after_path, output_path):
    before = Image.open(before_path)
    after = Image.open(after_path)
    w, h = before.size
    if w > 540:
        scale = 540 / w
        before = before.resize((540, int(h * scale)))
        after = after.resize((540, int(h * scale)))
        w, h = before.size
    gap = 20
    canvas = Image.new('RGB', (w * 2 + gap * 3, h + 40), '#222222')
    draw = ImageDraw.Draw(canvas)
    draw.text((gap + w//2 - 30, 8), "BEFORE", fill='#FF6B6B')
    draw.text((gap * 2 + w + w//2 - 30, 8), "AFTER", fill='#4ECDC4')
    canvas.paste(before, (gap, 40))
    canvas.paste(after, (gap * 2 + w, 40))
    canvas.save(output_path)

# ─── Main Pipeline ─────────────────────────────────────────
def run_pipeline(niches=None):
    os.makedirs(RENDER_DIR, exist_ok=True)
    
    with open(CAPTIONS_PATH) as f:
        all_captions = json.load(f)
    
    if niches is None:
        niches = ["restaurants", "barbershops", "salons"]
    
    results = {}
    
    for niche in niches:
        print(f"\n{'='*60}")
        print(f"  NICHE: {niche}")
        print(f"{'='*60}")
        
        business_name = BUSINESS_NAMES.get(niche, niche)
        rating = 4.7
        reviews = 150
        photo_path = f"photos/{niche}.jpg"
        
        # BEFORE: Render old template version
        print("  [0] Rendering BEFORE (old template)...")
        before_path = f"{RENDER_DIR}/{niche}_before.png"
        comp_id = niche.replace('_', '-')
        old_props = json.dumps({
            "niche": niche,
            "headline": all_captions.get(niche, {}).get("headline", ""),
            "name": business_name,
            "taglines": all_captions.get(niche, {}).get("taglines", []),
            "hashtags": all_captions.get(niche, {}).get("hashtags", []),
            "cta": all_captions.get(niche, {}).get("cta", "زورونا"),
            "photoPath": photo_path
        }, ensure_ascii=False)
        old_cmd = [
            "npx", "remotion", "still", "src/index.ts", comp_id, before_path,
            f"--props={old_props}",
            f"--browser-executable={CHROMIUM}",
            "--log=error"
        ]
        subprocess.run(old_cmd, capture_output=True, text=True, cwd=REMOTION_DIR, timeout=60)
        if os.path.exists(before_path):
            print(f"  ✓ Before: {os.path.getsize(before_path)//1024}KB")
        else:
            print("  ⚠️ Before render failed")
            before_path = None
        
        best_score = 0
        best_blueprint = None
        best_render = None
        feedback = None
        
        for iteration in range(1, MAX_ITERATIONS + 1):
            print(f"\n  --- Iteration {iteration}/{MAX_ITERATIONS} ---")
            
            # Step 1: Generate blueprint
            print("  [1] Kimi generating design blueprint...")
            blueprint = generate_blueprint(niche, business_name, rating, reviews, photo_path, feedback)
            
            if not blueprint:
                print("  ⚠️ Blueprint generation failed")
                if best_blueprint:
                    blueprint = best_blueprint
                else:
                    break
            
            blueprint["_niche"] = niche  # for photo ID resolution
            blueprint = normalize_blueprint(blueprint)  # resolve photo IDs → file paths BEFORE compositing
            comp_count = len(blueprint.get("composition", []))
            pattern = blueprint.get("designPattern", "unknown")
            print(f"  ✓ Pattern: {pattern}, Components: {comp_count}")
            for block in blueprint.get("composition", []):
                print(f"    • {block.get('component', '?')}: {block.get('id', '?')}")
            
            best_blueprint = blueprint
            time.sleep(2)
            
            # Step 1.5: Photo compositing + enhancement (NEW)
            print("  [1.5] Processing photos...")
            from photo_compositor import composite_photos
            from photo_enhancer import enhance_photo
            ad_id = f"{niche}_iter{iteration}"

            for block in blueprint.get("composition", []):
                comp = block.get("component", "")
                props = block.get("props", {})

                # Multi-photo components → composite into single image
                if comp in ("PhotoGrid", "PhotoMosaic", "FrameStack"):
                    photo_ids = props.get("photos", [])
                    if len(photo_ids) >= 2:
                        comp_path = composite_photos(photo_ids, niche, ad_id)
                        if comp_path:
                            block["component"] = "PhotoSingle"
                            block["props"] = {"src": comp_path, "showOverlay": True}
                            record_composite(ad_id, niche, comp_path,
                                            photo_ids, comp, ad_id)
                            abs_comp = os.path.join("/opt/nuhoot/remotion/public", comp_path)
                            enhance_photo(abs_comp, do_upscale=False, do_face=True)

                # Single-photo components → enhance
                elif comp in ("PhotoSingle", "PhotoFrame", "PhotoArch", "PhotoCircle",
                              "PhotoDiagonal", "PhotoDuotone", "PhotoDoubleFrame",
                              "FramePolaroid", "FrameCircle", "HeaderOverlay"):
                    src = props.get("src", "")
                    if src and src.startswith("photos/"):
                        abs_src = os.path.join("/opt/nuhoot/remotion/public", src)
                        if os.path.exists(abs_src):
                            enhance_photo(abs_src, do_upscale=False, do_face=True)

            # Step 2: Render with DynamicComposer
            print("  [2] Rendering with DynamicComposer...")
            render_path = f"{RENDER_DIR}/{niche}_iter{iteration}.png"
            success = render_blueprint(blueprint, render_path)
            
            if not success:
                print("  ⚠️ Render failed")
                continue
            
            size_kb = os.path.getsize(render_path) // 1024
            print(f"  ✓ Rendered: {size_kb}KB")
            best_render = render_path
            
            # Step 3: OpenCV analysis
            print("  [3] OpenCV analysis...")
            cv_scores = analyze_design(render_path)
            cv_score = cv_scores.get("overall", 0)
            print(f"  ✓ CV Score: {cv_score:.2f} (brightness={cv_scores.get('brightness_raw',0):.0f}, contrast={cv_scores.get('contrast_raw',0):.0f})")
            
            # Step 4: Tesseract
            print("  [4] Tesseract Arabic check...")
            tess = check_arabic_text(render_path)
            tess_score = tess.get("score", 0.5)
            print(f"  ✓ Arabic chars: {tess.get('arabic_char_count', 0)}, score: {tess_score:.2f}")
            
            # Step 5: Kimi vision critique
            print("  [5] Kimi vision critique...")
            critique = critique_design(render_path, niche, blueprint)
            kimi_score = critique.get("score", 0.5)
            issues = critique.get("issues", [])
            fixes = critique.get("fixes", [])
            print(f"  ✓ Kimi Score: {kimi_score:.2f}")
            if issues:
                for iss in issues[:3]:
                    print(f"    • {iss}")
            
            # Combined score
            combined = cv_score * 0.3 + tess_score * 0.2 + kimi_score * 0.5
            print(f"\n  📊 Combined: {combined:.2f} (threshold: {QUALITY_THRESHOLD})")
            
            if combined > best_score:
                best_score = combined
                final_path = f"{RENDER_DIR}/{niche}_best.png"
                shutil.copy(render_path, final_path)
            
            if combined >= QUALITY_THRESHOLD:
                print("  ✅ PASSED!")
                break
            
            # Build feedback for next iteration
            if iteration < MAX_ITERATIONS:
                parts = []
                if issues:
                    parts.append("Issues:\n" + "\n".join(f"- {i}" for i in issues))
                if fixes:
                    parts.append("Fixes needed:\n" + "\n".join(f"- {f}" for f in fixes))
                if cv_scores.get("brightness_raw", 128) < 30:
                    parts.append("Design is too dark — use lighter colors")
                if cv_scores.get("contrast_raw", 50) < 20:
                    parts.append("Low contrast — increase text/background difference")
                feedback = "\n\n".join(parts) if parts else "Improve the design quality"
                print("  🔄 Will fix and re-render...")
            
            time.sleep(5)
        
        # Save AFTER
        after_path = f"{RENDER_DIR}/{niche}_after.png"
        if best_render:
            shutil.copy(best_render, after_path)
        
        # Comparison
        if before_path and os.path.exists(after_path):
            comp_path = f"{RENDER_DIR}/{niche}_comparison.png"
            create_comparison(niche, before_path, after_path, comp_path)
            print(f"\n  📸 Comparison: {comp_path}")
        
        results[niche] = {
            "score": best_score,
            "iterations": iteration,
            "passed": best_score >= QUALITY_THRESHOLD,
            "pattern": best_blueprint.get("designPattern", "?") if best_blueprint else "?",
            "components": [b.get("component", "?") for b in best_blueprint.get("composition", [])] if best_blueprint else [],
            "blueprint": best_blueprint
        }
        print(f"  Final: score={best_score:.2f}, pattern={results[niche]['pattern']}")
        
        # Delay between niches to avoid rate limiting
        if niche != niches[-1]:
            print(f"  ⏸️  Waiting 15s before next niche...")
            time.sleep(15)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"  PIPELINE v3 SUMMARY")
    print(f"{'='*60}")
    for niche, r in sorted(results.items()):
        status = "✅" if r["passed"] else "⚠️"
        comps = ", ".join(r["components"][:4])
        print(f"  {status} {niche:20s} score={r['score']:.2f} pattern={r['pattern']}")
        print(f"     Components: {comps}")
    
    with open(f"{RENDER_DIR}/pipeline_v3_results.json", "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    return results

if __name__ == "__main__":
    niches = sys.argv[1:] if len(sys.argv) > 1 else ["restaurants", "barbershops", "salons"]
    run_pipeline(niches)
