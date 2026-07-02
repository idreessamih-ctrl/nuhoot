#!/usr/bin/env python3
"""Parallel dramatic layout renderer — fires 3 Kimi calls at once, renders all 21 niches."""
import sys, json, os, time, subprocess, concurrent.futures, requests
sys.path.insert(0, '/opt/nuhoot/eagle-eye')
from niche_config import NICHE_COLORS, get_dramatic_layout, get_niche_config, GENDER_TEXTS

API_URL = 'https://api.code.umans.ai/v1/chat/completions'
API_KEY = 'sk-WxllgGhf4ZGSfEJ75mJYyDwjuVKP9SlrAP03m4_SUQs'
RENDER_DIR = '/tmp/nuhoot-dramatic-21'
os.makedirs(RENDER_DIR, exist_ok=True)

CAPTIONS_PATH = '/opt/nuhoot/remotion/captions.json'

NICHE_DATA = {
    "restaurants": {"name": "مطعم الذواقة", "rating": 4.7, "reviews": 324, "photo": "photos/restaurants.jpg"},
    "cafes": {"name": "قهوة الصباح", "rating": 4.8, "reviews": 215, "photo": "photos/cafes.jpg"},
    "bakeries": {"name": "مخبز الحلويات", "rating": 4.6, "reviews": 189, "photo": "photos/bakeries.jpg"},
    "salons": {"name": "صالون لمسة", "rating": 4.8, "reviews": 180, "photo": "photos/salons.jpg"},
    "spas": {"name": "سبا الاسترخاء", "rating": 4.9, "reviews": 142, "photo": "photos/spas.jpg"},
    "barbershops": {"name": "حلاقة الرجال", "rating": 4.7, "reviews": 267, "photo": "photos/barbershops.jpg"},
    "gyms": {"name": "جيم باور", "rating": 4.9, "reviews": 342, "photo": "photos/gyms.jpg"},
    "clinics": {"name": "عيادة الشفاء", "rating": 4.6, "reviews": 198, "photo": "photos/clinics.jpg"},
    "dentists": {"name": "مركز الابتسامة", "rating": 4.7, "reviews": 156, "photo": "photos/dentists.jpg"},
    "pharmacies": {"name": "صيدلية العناية", "rating": 4.5, "reviews": 312, "photo": "photos/pharmacies.jpg"},
    "dermatology": {"name": "مركز الجلدية", "rating": 4.8, "reviews": 134, "photo": "photos/dermatology.jpg"},
    "fashion": {"name": "أزياء الأناقة", "rating": 4.7, "reviews": 178, "photo": "photos/fashion.jpg"},
    "perfumes": {"name": "عطور الشرق", "rating": 4.8, "reviews": 145, "photo": "photos/perfumes.jpg"},
    "law_firms": {"name": "مكتب الحقوق", "rating": 4.9, "reviews": 89, "photo": "photos/law_firms.jpg"},
    "real_estate": {"name": "عقارات الرياض", "rating": 4.6, "reviews": 234, "photo": "photos/real_estate.jpg"},
    "auto_shops": {"name": "مركز السيارات", "rating": 4.5, "reviews": 167, "photo": "photos/auto_shops.jpg"},
    "car_wash": {"name": "غسيل السيارات", "rating": 4.6, "reviews": 198, "photo": "photos/car_wash.jpg"},
    "cleaning": {"name": "نظافة المنازل", "rating": 4.7, "reviews": 256, "photo": "photos/cleaning.jpg"},
    "hvac_ac": {"name": "تبريد المكيفات", "rating": 4.5, "reviews": 143, "photo": "photos/hvac_ac.jpg"},
    "event_halls": {"name": "قصر المناسبات", "rating": 4.8, "reviews": 112, "photo": "photos/event_halls.jpg"},
    "training_centers": {"name": "مركز التدريب", "rating": 4.7, "reviews": 178, "photo": "photos/training_centers.jpg"},
}

def kimi_generate_content(niche, data):
    """Generate Arabic content via Kimi API."""
    config = get_niche_config(niche)
    gender = config.get("gender", "plural")
    gender_word = GENDER_TEXTS.get(gender, GENDER_TEXTS["plural"]).get("you_want", "تبون")
    layout = get_dramatic_layout(niche)
    colors = NICHE_COLORS.get(niche, {"bg": "#1A1A2E", "bg2": "#16213E", "accent": "#E94560", "accent2": "#D4AF37"})
    gradient_angle = config.get("gradient_angle", 135)

    # Load existing captions
    with open(CAPTIONS_PATH) as f:
        captions = json.load(f)
    existing = captions.get(niche, {})

    prompt = f"""You are a Saudi social media copywriter. Create Arabic content for a {niche} ad.

BUSINESS: {data['name']}
NICHE: {niche}
CITY: Riyadh, Saudi Arabia
RATING: {data['rating']}/5 ({data['reviews']} reviews)
GENDER: {gender} — address them as "{gender_word}"
LAYOUT: {layout}

Write authentic Saudi Arabic content. Output ONLY this JSON:
{{
  "kicker": "English kicker (2-4 words, UPPERCASE)",
  "headline": "Arabic headline (bold, catchy, max 50 chars)",
  "businessName": "Arabic business name",
  "taglines": ["Arabic tagline 1", "Arabic tagline 2", "Arabic tagline 3"],
  "bodyText": "One sentence Arabic description (max 80 chars, or empty)",
  "ctaText": "Arabic CTA button (max 30 chars)",
  "trustBadge": "Arabic trust badge (3-5 words)",
  "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3"]
}}

RULES:
- Authentic Saudi dialect
- Headline: punchy, attention-grabbing
- Taglines: 3 short benefits (max 25 chars each)
- CTA: action verb (احجز/زورونا/اطلب/سجّلوا)
- Gender: use "{gender_word}" for "you want"

Existing text (improve it):
{json.dumps(existing, ensure_ascii=False, indent=2)}
"""

    try:
        r = requests.post(API_URL, json={
            "model": "umans-kimi-k2.7",
            "messages": [
                {"role": "system", "content": "You are a JSON-only content generator. Output ONLY a valid JSON object. No thinking, no explanation. Start with { and end with }."},
                {"role": "user", "content": "Create content for a cafe ad."},
                {"role": "assistant", "content": '{"kicker":"RIYADH · COFFEE","headline":"أفضل قهوة في الرياض","businessName":"قهوة الصباح","taglines":["حبوب مختارة بعناية","تحميص طازج يومياً","جلسة هادئة"],"bodyText":"مكانكم المفضل لقهوة الصباح","ctaText":"زورونا اليوم","trustBadge":"مختارة بعناية","hashtags":["#قهوة_الرياض","#صباح_الخير","#مقاهي"]}'},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000, "temperature": 0.4,
        }, headers={"Authorization": f"Bearer {API_KEY}"}, timeout=60)

        resp = r.json()
        text = resp["choices"][0]["message"]["content"].strip()

        # Extract JSON
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            content = json.loads(text[start:end])
        else:
            return None

    except Exception as e:
        print(f"  ❌ {niche}: API error: {e}")
        return None

    # Build dramatic blueprint
    blueprint = {
        "designPattern": f"dramatic-{layout.lower()}",
        "dramaticLayout": layout,
        "composition": [],
        "globalStyles": {
            "backgroundColor": colors["bg"],
            "background": f"linear-gradient({gradient_angle}deg, {colors['bg']}, {colors['bg2']})",
            "primaryColor": colors["accent"],
            "accentColor": colors["accent2"],
            "color": "#FFFFFF",
            "direction": "rtl",
            "gradientAngle": gradient_angle,
        },
        "dramaticContent": {
            "kicker": content.get("kicker", ""),
            "headline": content.get("headline", ""),
            "businessName": content.get("businessName", data["name"]),
            "taglines": content.get("taglines", [])[:3],
            "bodyText": content.get("bodyText", ""),
            "ctaText": content.get("ctaText", ""),
            "rating": data["rating"],
            "ratingCount": data["reviews"],
            "hashtags": content.get("hashtags", [])[:4],
            "trustBadge": content.get("trustBadge", ""),
            "photoPath": data["photo"],
        },
    }
    return blueprint


def render_blueprint(niche, blueprint):
    """Render blueprint with Remotion."""
    output = f"{RENDER_DIR}/{niche}_dramatic.png"
    props_json = json.dumps({"blueprint": blueprint}, ensure_ascii=False)

    cmd = [
        "npx", "remotion", "still", "src/index.ts", "dynamic",
        output, f"--props={props_json}",
        "--browser-executable=/snap/chromium/current/usr/lib/chromium-browser/chrome",
    ]

    try:
        subprocess.run(cmd, capture_output=True, text=True, cwd="/opt/nuhoot/remotion", timeout=120)
        if os.path.exists(output):
            return output
    except:
        pass
    return None


def process_niche(niche, data):
    """Generate content + render for one niche."""
    t0 = time.time()

    # Step 1: Generate content via Kimi
    bp = kimi_generate_content(niche, data)
    if not bp:
        return niche, None, None, "content failed"

    content = bp.get("dramaticContent", {})
    headline = content.get("headline", "?")[:40]

    # Step 2: Render with Remotion
    output = render_blueprint(niche, bp)
    elapsed = time.time() - t0

    if output and os.path.exists(output):
        size = os.path.getsize(output) // 1024
        return niche, bp, output, f"✅ {size}KB in {elapsed:.0f}s — {headline}"
    return niche, bp, None, f"❌ render failed in {elapsed:.0f}s"


def main():
    niches = list(NICHE_DATA.keys())
    print(f"🔥 PARALLEL DRAMATIC PIPELINE — 21 niches, batches of 3")
    print(f"   Layouts: {len(set(get_dramatic_layout(n) for n in niches))} unique\n")

    all_blueprints = {}
    all_outputs = {}
    t_start = time.time()

    # Process in batches of 3
    for i in range(0, len(niches), 3):
        batch = niches[i:i+3]
        batch_num = i // 3 + 1
        total_batches = (len(niches) + 2) // 3
        print(f"\n--- Batch {batch_num}/{total_batches}: {', '.join(batch)} ---")

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
            futures = {ex.submit(process_niche, n, NICHE_DATA[n]): n for n in batch}
            for f in concurrent.futures.as_completed(futures):
                niche = futures[f]
                try:
                    n, bp, output, msg = f.result()
                    layout = get_dramatic_layout(n)
                    print(f"  {n:20s} [{layout:20s}] {msg}")
                    if bp:
                        all_blueprints[n] = bp
                    if output:
                        all_outputs[n] = output
                except Exception as e:
                    print(f"  {niche:20s} ❌ ERROR: {e}")

    t_total = time.time() - t_start
    print(f"\n{'='*60}")
    print(f"PIPELINE COMPLETE — {len(all_outputs)}/21 rendered in {t_total:.0f}s")
    print(f"{'='*60}")

    # Save blueprints
    for n, bp in all_blueprints.items():
        with open(f"{RENDER_DIR}/{n}_bp.json", "w") as f:
            json.dump(bp, f, ensure_ascii=False)

    # Summary by layout type
    from collections import Counter
    layout_counts = Counter(get_dramatic_layout(n) for n in all_outputs)
    print("\nLayout distribution:")
    for layout, count in sorted(layout_counts.items()):
        print(f"  {layout:20s} → {count} niches")

    # List outputs
    print("\nRendered designs:")
    for n in niches:
        if n in all_outputs:
            size = os.path.getsize(all_outputs[n]) // 1024
            print(f"  ✅ {n:20s} {size}KB")
        else:
            print(f"  ❌ {n:20s} FAILED")


if __name__ == "__main__":
    main()
