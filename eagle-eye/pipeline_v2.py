#!/usr/bin/env python3
"""
Nuhoot Eagle-Eye Pipeline v2
============================
Kimi K2.7 has FULL CONTROL over both text AND design.

Flow: Kimi sees current render → outputs text fixes + design overrides → 
Remotion re-renders → OpenCV measures → Kimi critiques again → repeat.

Key upgrade over v1:
- Kimi can change colors, opacity, arrow direction, badge rotation, shapes
- Better JSON extraction (handles reasoning text before JSON)
- Before/after comparison images
- 5 iterations instead of 3
- Design overrides passed as Remotion props
"""

import json, time, base64, re, os, sys, subprocess, shutil
import requests
import cv2
import numpy as np
from PIL import Image, ImageDraw

# ─── Configuration ──────────────────────────────────────────
API_KEY = "sk-WxllgGhf4ZGSfEJ75mJYyDwjuVKP9SlrAP03m4_SUQs"
API_URL = "https://api.code.umans.ai/v1/chat/completions"
MODEL = "umans-kimi-k2.7"
RENDER_DIR = "/tmp/nuhoot-eagle-eye-v2"
BEFORE_DIR = "/tmp/nuhoot-eagle-eye-v2/before"
AFTER_DIR = "/tmp/nuhoot-eagle-eye-v2/after"
REMOTION_DIR = "/opt/nuhoot/remotion"
CAPTIONS_PATH = "/opt/nuhoot/remotion/captions.json"
CHROMIUM = "/snap/chromium/current/usr/lib/chromium-browser/chrome"
MAX_ITERATIONS = 5
QUALITY_THRESHOLD = 0.80

MALE_NICHES = ['barbershops', 'gyms', 'auto_shops']
FEMALE_NICHES = ['salons', 'spas', 'dermatology', 'fashion']

# ─── Kimi API ──────────────────────────────────────────────
def kimi_chat(messages, max_tokens=3000, temperature=0.6):
    """Call Kimi with arbitrary message format (text or vision)."""
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    for attempt in range(3):
        try:
            r = requests.post(API_URL, headers=headers, json=payload, timeout=180)
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"].strip()
            elif r.status_code == 429:
                print("    ⏳ Rate limited, waiting 10s...")
                time.sleep(10)
            else:
                print(f"    API error {r.status_code}: {r.text[:100]}")
                time.sleep(5)
        except Exception as e:
            print(f"    API exception: {e}")
            time.sleep(5)
    return None

def kimi_see(image_path, prompt, max_tokens=3000):
    """Call Kimi with image + text (vision mode)."""
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    return kimi_chat([{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
            {"type": "text", "text": prompt}
        ]
    }], max_tokens=max_tokens, temperature=0.4)

# ─── JSON Extraction (robust) ──────────────────────────────
def extract_json(text):
    """Extract JSON from Kimi response — handles reasoning, markdown, partial."""
    if not text:
        return None
    # 1. Try ```json ... ``` block
    match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except:
            pass
    # 2. Try first { to last } (outermost object)
    first = text.find('{')
    last = text.rfind('}')
    if first != -1 and last != -1 and last > first:
        candidate = text[first:last+1]
        try:
            return json.loads(candidate)
        except:
            # Try fixing trailing commas
            cleaned = re.sub(r',\s*}', '}', candidate)
            cleaned = re.sub(r',\s*]', ']', cleaned)
            try:
                return json.loads(cleaned)
            except:
                pass
    # 3. Try line-by-line accumulation
    lines = text.split('\n')
    buf = ""
    for line in lines:
        buf += line + "\n"
        stripped = buf.strip()
        if stripped.startswith('{') and stripped.endswith('}'):
            try:
                return json.loads(stripped)
            except:
                pass
    return None

# ─── OpenCV Design Analyzer ────────────────────────────────
def analyze_design(image_path):
    """Analyze rendered PNG with OpenCV for objective quality metrics."""
    img = cv2.imread(image_path)
    if img is None:
        return {"error": "Cannot read image", "overall": 0.5}
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)
    contrast = np.std(gray)
    top_region = gray[40:200, :]
    mid_region = gray[600:880, :]
    bottom_region = gray[900:1050, :]
    header_text_score = min(1.0, np.std(top_region) / 50.0)
    body_text_score = min(1.0, np.std(mid_region) / 50.0)
    footer_text_score = min(1.0, np.std(bottom_region) / 50.0)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue_std = np.std(hsv[:,:,0][hsv[:,:,2] > 30])
    saturation_mean = np.mean(hsv[:,:,1])
    zone_height = h // 3
    zone_width = w // 3
    zones = []
    for ry in range(3):
        for rx in range(3):
            zone = gray[ry*zone_height:(ry+1)*zone_height, rx*zone_width:(rx+1)*zone_width]
            zones.append(np.std(zone))
    balance = max(0.0, 1.0 - (np.std(zones) / (np.mean(zones) + 1)))
    photo_region = gray[200:580, 230:850]
    photo_score = min(1.0, np.std(photo_region) / 50.0)
    scores = {
        "brightness": min(1.0, brightness / 128.0) if brightness > 20 else 0.3,
        "contrast": min(1.0, contrast / 60.0),
        "header_text": header_text_score,
        "body_text": body_text_score,
        "footer_text": footer_text_score,
        "color_harmony": min(1.0, 1.0 - (hue_std / 90.0)),
        "balance": balance,
        "photo_content": photo_score,
    }
    overall = float(np.mean(list(scores.values())))
    scores["overall"] = overall
    scores["brightness_raw"] = float(brightness)
    scores["contrast_raw"] = float(contrast)
    return scores

# ─── Tesseract Arabic Text Check ───────────────────────────
def check_arabic_text(image_path):
    """Use Tesseract to detect and verify Arabic text in the render."""
    try:
        import pytesseract
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='ara')
        arabic_chars = re.findall(r'[\u0600-\u06FF]', text)
        words = text.strip().split()
        return {
            "text_detected": len(arabic_chars) > 10,
            "arabic_char_count": len(arabic_chars),
            "word_count": len(words),
            "raw_text": text.strip()[:500],
            "score": min(1.0, len(arabic_chars) / 100.0) if arabic_chars else 0.0
        }
    except Exception as e:
        return {"error": str(e), "score": 0.5}

# ─── Remotion Renderer with Design Overrides ───────────────
def render_niche(niche, caption_data, design_overrides=None):
    """Render a niche with Remotion, passing design overrides as props."""
    comp_id = niche.replace('_', '-')
    photo = f"photos/{niche}.jpg"
    props_dict = {
        "niche": niche,
        "headline": caption_data.get("headline", ""),
        "name": caption_data.get("name", ""),
        "taglines": caption_data.get("taglines", []),
        "hashtags": caption_data.get("hashtags", []),
        "cta": caption_data.get("cta", "زورونا"),
        "photoPath": photo
    }
    if design_overrides:
        # Only pass non-None values
        clean = {k: v for k, v in design_overrides.items() if v is not None}
        if clean:
            props_dict["designOverrides"] = clean
    props = json.dumps(props_dict, ensure_ascii=False)
    output = f"{RENDER_DIR}/{niche}_iter{iteration_counter.get(niche, 0)}.png"
    cmd = [
        "npx", "remotion", "still", "src/index.ts", comp_id, output,
        f"--props={props}",
        f"--browser-executable={CHROMIUM}",
        "--log=error"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=REMOTION_DIR, timeout=60)
    if os.path.exists(output) and os.path.getsize(output) > 1000:
        return output
    print(f"    Render stderr: {result.stderr[:200] if result.stderr else 'none'}")
    return None

# Global iteration counter for unique filenames
iteration_counter = {}

# ─── Kimi Full Control Prompt ──────────────────────────────
def build_critique_and_fix_prompt(niche, current_text, current_design, cv_scores, iteration):
    """Build the prompt that gives Kimi full control to fix text AND design."""
    gender = "male" if niche in MALE_NICHES else "female" if niche in FEMALE_NICHES else "plural"
    gender_word = {"male": "تبي (male)", "female": "تبين (female)", "plural": "تبون (plural)"}[gender]
    
    prompt = f"""You are a professional Saudi graphic designer and copywriter. You have FULL CONTROL to fix both the Arabic text AND the visual design of this social media ad post.

**Niche**: {niche} — "{current_text.get('name', '')}" in Riyadh
**Target audience**: {gender} — use "{gender_word}" for addressing
**Iteration**: {iteration} (you can fix up to {MAX_ITERATIONS} times)

## Current Text
- Headline: {current_text.get('headline', '')}
- Taglines: {json.dumps(current_text.get('taglines', []), ensure_ascii=False)}
- CTA: {current_text.get('cta', '')}
- Hashtags: {json.dumps(current_text.get('hashtags', []), ensure_ascii=False)}

## Current Design Parameters
{json.dumps(current_design, ensure_ascii=False, indent=2)}

## OpenCV Objective Metrics
- Overall: {cv_scores.get('overall', 0):.2f}
- Brightness: {cv_scores.get('brightness_raw', 0):.0f}/255
- Contrast: {cv_scores.get('contrast_raw', 0):.0f}/60
- Balance: {cv_scores.get('balance', 0):.2f}
- Body text score: {cv_scores.get('body_text', 0):.2f}
- Footer text score: {cv_scores.get('footer_text', 0):.2f}

## What You Can Fix

### Text (fix Arabic grammar, Saudi dialect, gender forms):
- `headline`: Catchy Saudi-dialect headline (< 60 chars)
- `taglines`: Array of 3 marketing sentences in Saudi dialect
- `hashtags`: Array of 5 relevant hashtags
- `cta`: Short call-to-action (< 35 chars)

### Design (fix visual issues you see):
- `bg`: Main background color (#RRGGBB)
- `bg2`: Secondary background color (#RRGGBB)  
- `accent`: Primary accent color (#RRGGBB)
- `accent2`: Secondary accent color (#RRGGBB)
- `text`: Main text color (#RRGGBB)
- `bodyOpacity`: Body text opacity (0.5-1.0, higher = more visible)
- `hashtagOpacity`: Hashtag opacity (0.5-1.0)
- `hashtagColor`: Hashtag text color (#RRGGBB)
- `ctaArrow`: Arrow before CTA text ("←" or "→" or "" for none)
- `badgeRotation`: Badge rotation in degrees (-20 to 0)
- `shapeOpacityMult`: Decorative shapes opacity multiplier (0.3-1.0)
- `gridAlpha`: Grid line opacity (0.0-0.1, lower = less visible)

## Arabic Gender Rules (CRITICAL)
- Verbs get female ي suffix: يخليك → يخليكي (for female audience)
- Prepositions do NOT: لك stays لك (NOT لكي)
- Possessives do NOT: يومك stays يومك (NOT يومكي)
- نعطيك/تعطيك stay same for female
- Saudi dialect: "ما تنسى" not "لا تنس", "وانتي" not "وأنتي"

## Instructions
1. Look at the rendered image carefully
2. Identify ALL issues (text, color, contrast, layout, spacing)
3. Fix everything you can — you have full control
4. Output ONLY the JSON below, no explanation:

```json
{{
  "headline": "...",
  "taglines": ["...", "...", "..."],
  "hashtags": ["#...", "#...", "#...", "#...", "#..."],
  "cta": "...",
  "designOverrides": {{
    "bg": "#XXXXXX",
    "bg2": "#XXXXXX",
    "accent": "#XXXXXX",
    "accent2": "#XXXXXX",
    "bodyOpacity": 0.95,
    "hashtagOpacity": 0.9,
    "hashtagColor": "#XXXXXX",
    "ctaArrow": "→",
    "badgeRotation": -8,
    "shapeOpacityMult": 0.6,
    "gridAlpha": 0.02
  }},
  "score": 0.0-1.0,
  "issues_fixed": ["what you fixed 1", "what you fixed 2"]
}}
```

Only include designOverrides fields you want to change. Omit fields you want to keep as-is."""

    return prompt

def build_initial_prompt(niche):
    """Build the initial generation prompt for Kimi."""
    gender = "male" if niche in MALE_NICHES else "female" if niche in FEMALE_NICHES else "plural"
    gender_word = {"male": "تبي", "female": "تبين", "plural": "تبون"}[gender]
    
    names = {
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
    name = names.get(niche, niche)
    
    prompt = f"""You are a Saudi marketing copywriter. Write ad content for "{name}" in Riyadh.
Audience: {gender}. Use "{gender_word}" for addressing.

Rules:
- headline: Catchy Saudi-dialect headline (< 60 chars)
- 3 taglines: Complete marketing sentences in Saudi dialect
- 5 hashtags: Related to the niche
- cta: Very short call-to-action (< 35 chars)

Output ONLY JSON, no explanation:
```json
{{
  "headline": "...",
  "taglines": ["...", "...", "..."],
  "hashtags": ["#...", "#...", "#...", "#...", "#..."],
  "cta": "..."
}}```"""
    
    response = kimi_chat([{"role": "user", "content": prompt}], max_tokens=1500, temperature=0.7)
    if not response:
        return None
    data = extract_json(response)
    if data and "headline" in data:
        data["name"] = name
        return data
    print(f"    ⚠️ Initial JSON extraction failed. Raw: {response[:200]}")
    return None

# ─── Get Current Design Parameters ─────────────────────────
def get_current_design(niche):
    """Get the current design parameters from NuhootPost.tsx NICHE_DATA."""
    # Read the TSX file to extract niche colors
    tsx_path = f"{REMOTION_DIR}/src/NuhootPost.tsx"
    with open(tsx_path) as f:
        content = f.read()
    # Parse the NICHE_DATA line for this niche
    match = re.search(rf"{niche}:\s*\{{([^}}]+)\}}", content)
    if not match:
        return {}
    data_str = match.group(1)
    design = {}
    for pair in re.finditer(r"(\w+):'#?([\w\d]+)'", data_str):
        key, val = pair.group(1), pair.group(2)
        if key in ('bg', 'bg2', 'accent', 'accent2', 'text', 'badgeBg', 'badgeText'):
            design[key] = f"#{val}" if not val.startswith('#') else val
    # Add current override defaults
    design['bodyOpacity'] = 0.92
    design['hashtagOpacity'] = 0.75
    design['hashtagColor'] = design.get('accent2', '#FFFFFF')
    design['ctaArrow'] = '←'
    design['badgeRotation'] = -12
    design['shapeOpacityMult'] = 1.0
    design['gridAlpha'] = 0.06 if design.get('bg', '').lower() in ['#0f0f0f', '#1a1a2e', '#121212', '#2d4a3e', '#0e1428', '#0a1929', '#2d1b3d', '#1a1a1a'] else 0.05
    return design

# ─── Before/After Comparison ────────────────────────────────
def create_comparison(niche, before_path, after_path, output_path):
    """Create a side-by-side before/after comparison image."""
    before = Image.open(before_path)
    after = Image.open(after_path)
    w, h = before.size
    # Scale down if too large
    if w > 540:
        scale = 540 / w
        before = before.resize((540, int(h * scale)))
        after = after.resize((540, int(h * scale)))
        w, h = before.size
    gap = 20
    label_h = 40
    total_w = w * 2 + gap * 3
    total_h = h + label_h + gap
    canvas = Image.new('RGB', (total_w, total_h), '#222222')
    draw = ImageDraw.Draw(canvas)
    # Labels
    draw.text((gap + w//2 - 30, 8), "BEFORE", fill='#FF6B6B')
    draw.text((gap * 2 + w + w//2 - 30, 8), "AFTER", fill='#4ECDC4')
    canvas.paste(before, (gap, label_h))
    canvas.paste(after, (gap * 2 + w, label_h))
    canvas.save(output_path)
    return output_path

# ─── Main Pipeline ─────────────────────────────────────────
def run_pipeline(niches=None):
    """Run the full eagle-eye pipeline v2 with design control."""
    os.makedirs(RENDER_DIR, exist_ok=True)
    os.makedirs(BEFORE_DIR, exist_ok=True)
    os.makedirs(AFTER_DIR, exist_ok=True)
    
    # Load existing captions as starting point
    with open(CAPTIONS_PATH) as f:
        all_captions = json.load(f)
    
    if niches is None:
        niches = sorted(all_captions.keys())[:3]  # Default: first 3 for testing
    
    results = {}
    
    for niche in niches:
        print(f"\n{'='*60}")
        print(f"  NICHE: {niche}")
        print(f"{'='*60}")
        
        global iteration_counter
        iteration_counter[niche] = 0
        
        # Get current design params
        current_design = get_current_design(niche)
        print(f"  Current design: bg={current_design.get('bg', '?')}, accent={current_design.get('accent', '?')}")
        
        # ── BEFORE: Render with current captions (no overrides) ──
        print("  [0] Rendering BEFORE (baseline)...")
        before_path = f"{BEFORE_DIR}/{niche}_before.png"
        iteration_counter[niche] = 0
        rendered = render_niche(niche, all_captions.get(niche, {}), None)
        if rendered:
            shutil.copy(rendered, before_path)
            print(f"  ✓ Before saved: {os.path.getsize(before_path)//1024}KB")
        else:
            print("  ⚠️ Before render failed")
            continue
        
        best_score = 0
        best_captions = all_captions.get(niche, {})
        best_design = None
        best_render_path = before_path
        feedback_text = None
        
        for iteration in range(1, MAX_ITERATIONS + 1):
            iteration_counter[niche] = iteration
            print(f"\n  --- Iteration {iteration}/{MAX_ITERATIONS} ---")
            
            # Step 1: Generate or fix text + design
            if iteration == 1:
                print("  [1] Kimi generating initial copy...")
                captions = build_initial_prompt(niche)
                if not captions:
                    captions = best_captions
                design_overrides = None  # Start with no overrides
                kimi_score = 0.5  # First iteration has no Kimi score yet
            else:
                print("  [1] Kimi seeing render + fixing text + design...")
                prompt = build_critique_and_fix_prompt(
                    niche, best_captions, current_design, cv_scores, iteration
                )
                response = kimi_see(best_render_path, prompt, max_tokens=3000)
                if response:
                    data = extract_json(response)
                    if data:
                        # Extract text fixes
                        if "headline" in data:
                            captions = {**best_captions, **{k: data[k] for k in 
                                ["headline", "taglines", "hashtags", "cta"] if k in data}}
                            if "name" not in captions:
                                captions["name"] = best_captions.get("name", niche)
                        else:
                            captions = best_captions
                        
                        # Extract design overrides
                        design_overrides = data.get("designOverrides", {})
                        if design_overrides:
                            print(f"  ✓ Design overrides: {json.dumps(design_overrides, ensure_ascii=False)[:200]}")
                            # Update current_design for next iteration's context
                            current_design.update({k: v for k, v in design_overrides.items() if v is not None})
                        
                        kimi_score = data.get("score", 0.7)
                        fixes = data.get("issues_fixed", [])
                        if fixes:
                            print(f"  ✓ Issues fixed: {', '.join(fixes[:3])}")
                    else:
                        print(f"  ⚠️ JSON extraction failed. Raw: {response[:200]}")
                        captions = best_captions
                        design_overrides = best_design
                        kimi_score = 0.5
                else:
                    print("  ⚠️ No response from Kimi")
                    captions = best_captions
                    design_overrides = best_design
                    kimi_score = 0.5
            
            if captions and "headline" in captions:
                best_captions = captions
                all_captions[niche] = captions
                print(f"  ✓ Headline: {captions.get('headline', '')[:50]}")
                print(f"  ✓ CTA: {captions.get('cta', '')[:40]}")
            
            if design_overrides:
                best_design = design_overrides
            else:
                best_design = best_design  # Keep previous
            
            time.sleep(2)
            
            # Step 2: Render with Remotion (with design overrides if any)
            print("  [2] Rendering with Remotion...")
            png_path = render_niche(niche, best_captions, best_design)
            if not png_path:
                print("  ⚠️ Render failed, skipping")
                continue
            best_render_path = png_path
            size_kb = os.path.getsize(png_path) // 1024
            print(f"  ✓ Rendered: {size_kb}KB")
            
            # Step 3: OpenCV analysis
            print("  [3] OpenCV design analysis...")
            cv_scores = analyze_design(png_path)
            cv_score = cv_scores.get("overall", 0)
            print(f"  ✓ CV Score: {cv_score:.2f}")
            print(f"    brightness={cv_scores.get('brightness_raw',0):.0f} "
                  f"contrast={cv_scores.get('contrast_raw',0):.0f} "
                  f"balance={cv_scores.get('balance',0):.2f}")
            
            # Step 4: Tesseract Arabic check
            print("  [4] Tesseract Arabic text check...")
            tess_result = check_arabic_text(png_path)
            tess_score = tess_result.get("score", 0.5)
            arabic_chars = tess_result.get("arabic_char_count", 0)
            print(f"  ✓ Arabic chars: {arabic_chars}, score: {tess_score:.2f}")
            
            # Step 5: Kimi vision critique (only if not already done in fix step)
            if iteration > 1 and kimi_score == 0.5:
                print("  [5] Kimi vision critique...")
                critique_prompt = f"""You are reviewing a {niche} social media ad. 
Rate the design quality 0.0-1.0 and list any remaining issues.
Respond in JSON only:
{{"score": 0.0-1.0, "issues": ["..."], "severity": "none|minor|major|critical"}}"""
                critique_response = kimi_see(png_path, critique_prompt, max_tokens=1000)
                if critique_response:
                    critique_data = extract_json(critique_response)
                    if critique_data:
                        kimi_score = critique_data.get("score", 0.5)
                        remaining = critique_data.get("issues", [])
                        if remaining:
                            print(f"  Remaining issues: {', '.join(remaining[:3])}")
                    else:
                        score_match = re.search(r'"score"\s*:\s*([\d.]+)', critique_response)
                        kimi_score = float(score_match.group(1)) if score_match else 0.5
                print(f"  ✓ Kimi Score: {kimi_score:.2f}")
            elif iteration == 1:
                # First iteration: do a separate critique
                print("  [5] Kimi vision critique (first look)...")
                critique_prompt = f"""You are reviewing a {niche} social media ad for the first time.
Rate the design quality 0.0-1.0 and list ALL issues you see.
Respond in JSON only:
{{"score": 0.0-1.0, "issues": ["..."], "severity": "none|minor|major|critical"}}"""
                critique_response = kimi_see(png_path, critique_prompt, max_tokens=1500)
                if critique_response:
                    critique_data = extract_json(critique_response)
                    if critique_data:
                        kimi_score = critique_data.get("score", 0.5)
                        issues = critique_data.get("issues", [])
                        if issues:
                            print(f"  Issues found:")
                            for iss in issues[:5]:
                                print(f"    • {iss}")
                        feedback_text = "\n".join(f"- {i}" for i in issues) if issues else ""
                    else:
                        kimi_score = 0.5
                print(f"  ✓ Kimi Score: {kimi_score:.2f}")
            
            # Step 6: Combined score
            combined_score = (cv_score * 0.3 + tess_score * 0.2 + kimi_score * 0.5)
            print(f"\n  📊 Combined Score: {combined_score:.2f} (threshold: {QUALITY_THRESHOLD})")
            
            if combined_score > best_score:
                best_score = combined_score
                # Save this as the best version
                final_path = f"{AFTER_DIR}/{niche}_best.png"
                shutil.copy(png_path, final_path)
            
            if combined_score >= QUALITY_THRESHOLD:
                print(f"  ✅ PASSED!")
                break
            
            if iteration < MAX_ITERATIONS:
                print(f"  🔄 Will fix and re-render...")
            
            time.sleep(3)
        
        # ── AFTER: Save best version ──
        final_after = f"{AFTER_DIR}/{niche}_after.png"
        if best_render_path and os.path.exists(best_render_path):
            shutil.copy(best_render_path, final_after)
        else:
            shutil.copy(before_path, final_after)
        
        # Create comparison
        comparison_path = f"{RENDER_DIR}/{niche}_comparison.png"
        create_comparison(niche, before_path, final_after, comparison_path)
        print(f"\n  📸 Comparison saved: {comparison_path}")
        
        results[niche] = {
            "score": best_score,
            "iterations": iteration,
            "passed": best_score >= QUALITY_THRESHOLD,
            "before": before_path,
            "after": final_after,
            "comparison": comparison_path,
            "captions": best_captions,
            "design_overrides": best_design
        }
        print(f"  Final: score={best_score:.2f}, passed={'YES' if best_score >= QUALITY_THRESHOLD else 'NO'}")
    
    # ── Summary ──
    print(f"\n{'='*60}")
    print(f"  PIPELINE v2 SUMMARY")
    print(f"{'='*60}")
    for niche, result in sorted(results.items()):
        status = "✅" if result["passed"] else "⚠️"
        print(f"  {status} {niche}: score={result['score']:.2f}, iters={result['iterations']}")
        if result.get("design_overrides"):
            print(f"     Design changes: {list(result['design_overrides'].keys())}")
    
    # Save results
    with open(f"{RENDER_DIR}/pipeline_v2_results.json", 'w') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    return results

# ─── Entry Point ───────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) > 1:
        niches = sys.argv[1:]
    else:
        niches = ["restaurants", "barbershops", "salons"]
    
    results = run_pipeline(niches)
