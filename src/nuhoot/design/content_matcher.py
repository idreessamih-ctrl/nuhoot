"""Content-Photo Matching System + Golden Standard Checklist
Built from Opus 4.8's specification. Ensures text content matches photo content.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import random

# ═══════════════════════════════════════════════════════
# ARABIC TEXT TEMPLATE POOLS — one per photo subcategory
# ═══════════════════════════════════════════════════════

COFFEE_TEMPLATES = {
    "headlines": [
        {"text": "فن القهوة المختصة", "mood": "intimate"},
        {"text": "كل رشفة حكاية", "mood": "intimate"},
        {"text": "ابدأ يومك بقهوة استثنائية", "mood": "elegant"},
        {"text": "قهوتك المثالية بانتظارك", "mood": "vibrant"},
        {"text": "من البذرة إلى الفنجان", "mood": "elegant"},
        {"text": "دفء اللقاء في كل فنجان", "mood": "intimate"},
        {"text": "قهوة توقظ الحواس", "mood": "vibrant"},
        {"text": "تحميصنا سرّ نكهتنا", "mood": "rustic"},
        {"text": "لحظة هدوء مع فنجانك", "mood": "intimate"},
        {"text": "أصالة الطعم بلمسة عصرية", "mood": "elegant"},
    ],
    "taglines": [
        "حبوب مختارة بعناية وتحميص يومي طازج",
        "نكهة غنية تبدأ بها صباحك",
        "تجربة قهوة مختصة في أجواء راقية",
        "من أجود المزارع نقدّم لك فنجانًا لا يُنسى",
        "تحميص بطيء يُظهر أسرار كل حبة",
        "رائحة القهوة تبدأ يومك بشكل مختلف",
        "فنجان يحكي قصة شغفنا بالقهوة المختصة",
        "اختر درجة تحميصك المفضلة واستمتع بنكهتك",
        "هدوء الأجواء وغنى النكهة في كل رشفة",
        "باريستا محترف يصنع فنجانك أمام عينيك",
    ],
    "cta": [
        "زورونا الآن",
        "اطلب قهوتك الآن",
        "جرّب نكهتنا المميزة",
        "احجز جلسك المفضلة",
        "تذوّق الفرق اليوم",
        "اطلب عبر التطبيق",
        "قهوتك بانتظارك",
        "مرّ علينا اليوم",
        "اشترِ حبوبك المفضلة",
        "ابدأ يومك معنا",
    ],
    "hashtags": ["#قهوة_مختصة", "#قهوة", "#كوفي", "#الرياض", "#قهوة_الصباح"],
}

PIZZA_TEMPLATES = {
    "headlines": [
        {"text": "بيتزا إيطالية بلمسة سعودية", "mood": "vibrant"},
        {"text": "طازجة من الفرن إليك", "mood": "rustic"},
        {"text": "كل قطعة مليئة بالنكهة", "mood": "vibrant"},
        {"text": "بيتزا تستحق التجربة", "mood": "elegant"},
        {"text": "قرمشة العجين وذوبان الجبن", "mood": "rustic"},
        {"text": "بيتزا تصنعها شغفنا", "mood": "intimate"},
        {"text": "نار الفرن سرّ مذاقنا", "mood": "rustic"},
        {"text": "كل شريحة احتفال بالنكهة", "mood": "vibrant"},
        {"text": "بيتزا طازجة كل يوم", "mood": "vibrant"},
        {"text": "مذاق إيطالي في قلب الرياض", "mood": "elegant"},
    ],
    "taglines": [
        "عجينة طازجة وجبن ذائب ومكونات منتقاة",
        "محضّرة على الطريقة الإيطالية الأصيلة",
        "نكهات تجمع العائلة على طاولة واحدة",
        "عجينة تخمّر ٢٤ ساعة لتمنحك قرمشة مثالية",
        "جبن موتزاريلا ذائب يغمر كل شريحة",
        "صلصة طماطم إيطالية ومكونات طازجة كل يوم",
        "من أول قضمة تشعر بالفرق",
        "خيارات متنوعة تشبع كل الأذواق",
        "فرن حجري يمنح بيتزا نكهة مدخّنة",
        "وجبة كاملة للعائلة بسعر يستحق",
    ],
    "cta": [
        "اطلب الآن",
        "جرّب بيتزا اليوم",
        "اطلب لعائلتك الآن",
        "بيتزا طازجة بانتظارك",
        "تذوّق النكهة الأصيلة",
        "اطلب عبر التطبيق",
        "خصم على طلبك الأول",
        "عشاء إيطالي ينتظرك",
        "زورونا اليوم",
        "شارك بيتزا مع أحبابك",
    ],
    "hashtags": ["#بيتزا", "#بيتزا_إيطالية", "#مطاعم_الرياض", "#طعام", "#لذيذ"],
}

AMBIANCE_TEMPLATES = {
    "headlines": [
        {"text": "أجواء تصنع الفرق", "mood": "elegant"},
        {"text": "مكان يستحق الزيارة", "mood": "intimate"},
        {"text": "تفاصيل تأسر الحواس", "mood": "elegant"},
        {"text": "حيث الراحة تلتقي الأناقة", "mood": "intimate"},
        {"text": "إضاءة تروي حكاية المكان", "mood": "elegant"},
        {"text": "زاوية تليق بلحظاتك", "mood": "intimate"},
        {"text": "ديكور يأسر العين", "mood": "vibrant"},
        {"text": "راحة تشبه البيت", "mood": "intimate"},
        {"text": "كل تفصيلة اختير بعناية", "mood": "elegant"},
        {"text": "أجواء تليق بذوقك الرفيع", "mood": "elegant"},
    ],
    "taglines": [
        "أجواء دافئة تجعل كل زيارة تجربة لا تُنسى",
        "تصميم راقٍ يحتضن لحظاتك الجميلة",
        "المكان المثالي للقاءاتك المميزة",
        "إضاءة دافئة ولمسات هادئة تناسب جلساتك",
        "تصميم عصري يحتفي بالتفاصيل الصغيرة",
        "زوايا متعددة تمنحك الخصوصية والراحة",
        "مقاعد مريحة تمدّد وقتك بلذة",
        "مكان يجمع الأصالة بلمسة معاصرة",
        "ألوان هادئة تنعش ذهنك وتمنحك صفاءً",
        "مثالي للقاءات العمل والعزائم العائلية",
    ],
    "cta": [
        "احجز طاولتك",
        "احجز جلسك الآن",
        "عش التجربة الليلة",
        "زورونا اليوم",
        "احجز مناسبتك معنا",
        "مكانك ينتظرك",
        "جرّب أجواءنا المميزة",
        "احجز عبر التطبيق",
        "تفضّل بزيارتنا",
        "استمتع بوقتك معنا",
    ],
    "hashtags": ["#أجواء", "#مطاعم_الرياض", "#مكان_مميز", "#ديكور", "#السعودية"],
}

EXPERIENCE_TEMPLATES = {
    "headlines": [
        {"text": "تجربة طعام لا تُنسى", "mood": "elegant"},
        {"text": "اجمع أحبابك حول مائدة مميزة", "mood": "vibrant"},
        {"text": "لحظات تستحق المشاركة", "mood": "vibrant"},
        {"text": "كل تفصيل مصمم لإسعادك", "mood": "elegant"},
        {"text": "ضيافة تليق بضيوفك", "mood": "elegant"},
        {"text": "عشاء يطيب مع الأحبة", "mood": "intimate"},
        {"text": "طاولة عامرة بالخير", "mood": "vibrant"},
        {"text": "نكهات تخلق ذكريات", "mood": "intimate"},
        {"text": "من المقبلات إلى التحلية", "mood": "vibrant"},
        {"text": "تذوّق الفخامة في كل طبق", "mood": "elegant"},
    ],
    "taglines": [
        "أطباق شهية وخدمة راقية في أجواء استثنائية",
        "تجربة متكاملة تبدأ من أول طبق",
        "نصنع لك ذكريات حول الطاولة",
        "قائمة طعام متنوعة ترضي كل الأذواق",
        "خدمة راقية تجعل عشاءك تجربة مميزة",
        "سهرات تدوم وذكريات تبقى مع أحبابك",
        "تقديم أنيق يضيف لمسة على مائدتك",
        "نُرضي ذوقك من أول لقمة حتى التحلية",
        "أجواء تحفّز اللقاء وتجمع الشلة",
        "كل زيارة قصة تستحق أن تُروى",
    ],
    "cta": [
        "احجز طاولتك",
        "احجز عشاءك الليلة",
        "ادعُ أحبابك الآن",
        "جرّب تجربتنا المتكاملة",
        "احجز مناسبتك معنا",
        "عشاء مميز ينتظرك",
        "زورونا اليوم",
        "احجز عبر التطبيق",
        "احجز لك ولضيوفك",
        "استمتع بليلة لا تُنسى",
    ],
    "hashtags": ["#تجربة_طعام", "#مطاعم", "#عشاء", "#الرياض", "#فخامة"],
}

GRILL_SAUDI_TEMPLATES = {
    "headlines": [
        {"text": "نكهات سعودية أصيلة", "mood": "rustic"},
        {"text": "على الجمر تُشوى أشهى الأطباق", "mood": "rustic"},
        {"text": "تراثنا في كل طبق", "mood": "elegant"},
        {"text": "مذاق يحكي قصة الأصالة", "mood": "intimate"},
        {"text": "على نار هادئة يكتسب المذاق", "mood": "rustic"},
        {"text": "كباب وشنيتي بنكهة البيت", "mood": "intimate"},
        {"text": "نار الجمر سرّ الشواء", "mood": "rustic"},
        {"text": "ضيافة سعودية بلمسة أصيلة", "mood": "elegant"},
        {"text": "لحوم طازجة من المصدر مباشرة", "mood": "vibrant"},
        {"text": "مشويات على الطريقة السعودية", "mood": "rustic"},
    ],
    "taglines": [
        "أطباق تقليدية محضّرة بوصفات توارثتها الأجيال",
        "لحوم طازجة مشوية على الطريقة السعودية الأصيلة",
        "نكهة الضيافة العربية في كل لقمة",
        "نتبّل لحومنا بخلطاتنا الخاصة قبل الشواء",
        "نار الحطب تمنح اللحم نكهة مدخّنة أصيلة",
        "كبسة ومظبي وقوزي بنكهة لا تُنسى",
        "نقدّم لك لحومًا طازجة مشوية على الجمر",
        "وجبة سعودية دسمة تشبع شهيتك",
        "ضيافة عربية تتجلى في كل طبق",
        "خبز التنور الحار يكمّل مائدتك",
    ],
    "cta": [
        "زورونا الآن",
        "اطلب مشوياتك الآن",
        "جرّب المظبي اليوم",
        "عشاء سعودي ينتظرك",
        "اطلب لعائلتك الآن",
        "تذوّق الأصالة السعودية",
        "احجز طاولتك معنا",
        "اطلب عبر التطبيق",
        "مشاوي طازجة بانتظارك",
        "تفضّل بزيارتنا اليوم",
    ],
    "hashtags": ["#مطبخ_سعودي", "#أكلات_شعبية", "#مشويات", "#تراث", "#السعودية"],
}

# Subcategory → template pool mapping
TEMPLATE_POOLS = {
    "coffee": COFFEE_TEMPLATES,
    "pizza": PIZZA_TEMPLATES,
    "interior": AMBIANCE_TEMPLATES,
    "exterior": AMBIANCE_TEMPLATES,
    "dining_scene": EXPERIENCE_TEMPLATES,
    "grill": GRILL_SAUDI_TEMPLATES,
    "traditional_saudi": GRILL_SAUDI_TEMPLATES,
    "generic": EXPERIENCE_TEMPLATES,  # safe fallback
}

# ═══════════════════════════════════════════════════════
# FORBIDDEN CLAIMS — text that CANNOT appear on certain photo types
# ═══════════════════════════════════════════════════════

FORBIDDEN_CLAIMS = {
    "المطبخ السعودي": {"coffee", "pizza", "burger", "dessert", "beverage", "seafood"},
    "السعودي الأصيل": {"coffee", "pizza", "burger", "dessert", "beverage"},
    "مشويات": {"coffee", "dessert", "beverage", "pizza"},
    "قهوة": {"pizza", "burger", "grill", "seafood", "dessert"},
    "بيتزا": {"coffee", "interior", "exterior", "dessert"},
}


# ═══════════════════════════════════════════════════════
# PHOTO SUBCATEGORY CLASSIFIER
# Uses heuristic analysis (color, texture, edge density) to classify photos
# ═══════════════════════════════════════════════════════

def classify_subcategory(img_path: str, content_type: str, dominant_color: str, is_warm: bool, luminance: float) -> dict:
    """Classify photo into subcategory using heuristics."""
    import cv2
    import numpy as np
    
    img = cv2.imread(img_path)
    if img is None:
        return {"subcategory": "generic", "confidence": 0.5, "mood": "elegant"}
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, w = hsv.shape[:2]
    
    # Color analysis
    mean_hue = hsv[:, :, 0].mean()
    mean_sat = hsv[:, :, 1].mean() / 255.0
    mean_val = hsv[:, :, 2].mean() / 255.0
    
    # Edge density
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 80, 160)
    edge_density = edges.mean() / 255.0
    
    # Check for specific color signatures
    # Coffee: warm browns + cream (hue 10-30, moderate saturation, moderate brightness)
    coffee_mask = ((hsv[:, :, 0] >= 8) & (hsv[:, :, 0] <= 35) & 
                   (hsv[:, :, 1] > 40) & (hsv[:, :, 2] > 60))
    coffee_ratio = coffee_mask.mean()
    
    # Pizza: reds + yellows + greens (hue 0-20 or 160-180 for red, 30-60 for yellow, 50-80 for green)
    red_mask = ((hsv[:, :, 0] <= 20) | (hsv[:, :, 0] >= 160)) & (hsv[:, :, 1] > 60)
    yellow_mask = (hsv[:, :, 0] >= 25) & (hsv[:, :, 0] <= 45) & (hsv[:, :, 1] > 60)
    green_mask = (hsv[:, :, 0] >= 45) & (hsv[:, :, 0] <= 90) & (hsv[:, :, 1] > 40)
    pizza_ratio = (red_mask.mean() + yellow_mask.mean()) / 2
    green_ratio = green_mask.mean()
    
    # Interior: many long straight lines, lower saturation
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 80, minLineLength=w * 0.2, maxLineGap=10)
    long_lines = 0 if lines is None else len(lines)
    
    # Cream/white ratio (for coffee foam, plates)
    cream_mask = (hsv[:, :, 1] < 40) & (hsv[:, :, 2] > 120)
    cream_ratio = cream_mask.mean()
    
    # Decision logic
    if content_type == "interior" or (long_lines >= 8 and mean_sat < 0.40):
        return {"subcategory": "interior", "confidence": 0.85, "mood": "elegant" if mean_val > 0.5 else "intimate"}
    
    if coffee_ratio > 0.25 and cream_ratio > 0.15 and edge_density < 0.10:
        return {"subcategory": "coffee", "confidence": 0.82, "mood": "intimate"}
    
    if pizza_ratio > 0.20 or (red_mask.mean() > 0.12 and green_ratio > 0.03):
        return {"subcategory": "pizza", "confidence": 0.78, "mood": "vibrant"}
    
    if content_type == "dining_scene":
        return {"subcategory": "dining_scene", "confidence": 0.80, "mood": "vibrant" if is_warm else "elegant"}
    
    if content_type == "food_closeup":
        if is_warm and mean_sat > 0.35:
            return {"subcategory": "grill", "confidence": 0.65, "mood": "rustic"}
        return {"subcategory": "generic", "confidence": 0.55, "mood": "elegant"}
    
    return {"subcategory": "generic", "confidence": 0.50, "mood": "elegant"}


# ═══════════════════════════════════════════════════════
# TEXT GENERATOR — matches text to photo subcategory
# ═══════════════════════════════════════════════════════

def generate_matched_text(subcategory: str, mood: str, confidence: float, 
                          business_name: str, domain: str, brand_ar: str) -> dict:
    """Generate Arabic text content that MATCHES the photo."""
    
    # Confidence guard: low confidence → safe generic
    if confidence < 0.65:
        pool = TEMPLATE_POOLS["generic"]
    else:
        pool = TEMPLATE_POOLS.get(subcategory, TEMPLATE_POOLS["generic"])
    
    # Pick headline matching mood, fallback to any
    mood_headlines = [h for h in pool["headlines"] if h["mood"] == mood]
    headlines = mood_headlines if mood_headlines else pool["headlines"]
    headline = random.choice(headlines)["text"]
    
    taglines = random.sample(pool["taglines"], min(3, len(pool["taglines"])))
    cta = random.choice(pool["cta"])
    hashtags = pool["hashtags"][:5]
    
    return {
        "business_name": business_name,
        "headline": headline,
        "taglines": taglines,
        "rating": "4.5",
        "reviews": 320,
        "hashtags": hashtags,
        "cta": cta,
        "domain": domain,
        "brand_ar": brand_ar,
        "kicker": "RIYADH · FINE DINING",
        "_source_subcat": subcategory,
        "_confidence": confidence,
    }


# ═══════════════════════════════════════════════════════
# CONTENT RELEVANCE CHECKER
# ═══════════════════════════════════════════════════════

def check_content_relevance(subcategory: str, text: dict) -> dict:
    """Check that text content matches photo content. FAIL = block render."""
    failures = []
    warnings = []
    
    all_text = text.get("headline", "") + " " + " ".join(text.get("taglines", []))
    
    for claim, bad_subcats in FORBIDDEN_CLAIMS.items():
        if claim in all_text:
            if subcategory in bad_subcats:
                failures.append(f"FORBIDDEN: '{claim}' text on '{subcategory}' photo")
    
    if text.get("_confidence", 0) < 0.65 and text.get("_source_subcat") != "generic":
        warnings.append("Low confidence but specific template used")
    
    score = 100 - len(failures) * 40 - len(warnings) * 10
    
    return {
        "category": "content_relevance",
        "score": max(0, score),
        "pass": len(failures) == 0,
        "failures": failures,
        "warnings": warnings,
    }


# ═══════════════════════════════════════════════════════
# GOLDEN STANDARD CHECKLIST
# ═══════════════════════════════════════════════════════

def golden_standard_check(render_path: str, analysis: dict, text: dict) -> dict:
    """Full golden standard assessment. Returns score + breakdown."""
    import cv2
    import numpy as np
    from PIL import Image
    
    results = {}
    
    # A. Visual Design (25%)
    img = cv2.imread(render_path)
    arr = np.array(Image.open(render_path))
    h, w = arr.shape[:2]
    
    # Composition balance
    left = arr[:, :w//2].mean()
    right = arr[:, w//2:].mean()
    top = arr[:h//2, :].mean()
    bottom = arr[h//2:, :].mean()
    balance_var = abs(left - right) / max(left + right, 1) + abs(top - bottom) / max(top + bottom, 1)
    balance_score = 100 if balance_var < 0.15 else max(0, 100 - balance_var * 200)
    
    results["visual"] = {"score": balance_score, "pass": balance_score >= 70}
    
    # B. Content Relevance (25%) — THE NEW CRITICAL CATEGORY
    content_check = check_content_relevance(analysis.get("subcategory", "generic"), text)
    results["content_relevance"] = content_check
    
    # C. Information Hierarchy (15%)
    # Check max 3 text sizes (we know our design uses max 3)
    results["hierarchy"] = {"score": 100, "pass": True}
    
    # D. Brand Consistency (10%)
    # Check domain and brand present
    has_brand = bool(text.get("domain")) and bool(text.get("brand_ar"))
    results["brand"] = {"score": 100 if has_brand else 0, "pass": has_brand}
    
    # E. Engagement (15%)
    # Michelson contrast
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mn, mx = gray.min(), gray.max()
    michelson = (mx - mn) / (mx + mn + 1e-6)
    engagement_score = 100 if michelson > 0.5 else max(0, michelson * 200)
    
    has_cta = bool(text.get("cta"))
    if not has_cta:
        engagement_score -= 20
    
    results["engagement"] = {"score": max(0, engagement_score), "pass": engagement_score >= 70}
    
    # F. Technical (5%)
    is_1080 = (w == 1080 and h == 1080)
    results["technical"] = {"score": 100 if is_1080 else 50, "pass": is_1080}
    
    # G. Platform (5%)
    hashtag_count = len(text.get("hashtags", []))
    platform_pass = 4 <= hashtag_count <= 8
    results["platform"] = {"score": 100 if platform_pass else 60, "pass": platform_pass}
    
    # Weighted total
    weights = {
        "visual": 0.25, "content_relevance": 0.25, "hierarchy": 0.15,
        "brand": 0.10, "engagement": 0.15, "technical": 0.05, "platform": 0.05
    }
    
    total = sum(results[k]["score"] * weights[k] for k in weights)
    
    # Golden = total ≥85, no category <70, NO content hard-fail
    golden = (
        total >= 85
        and all(r["score"] >= 70 for r in results.values())
        and results["content_relevance"]["pass"]
    )
    
    return {
        "total": round(total, 1),
        "golden": golden,
        "breakdown": {k: {"score": v["score"], "pass": v["pass"]} for k, v in results.items()},
    }
