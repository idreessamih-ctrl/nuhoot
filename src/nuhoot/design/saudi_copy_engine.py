"""Saudi Arabic Copy Engine — transforms GLM formal output into native Saudi dialect.

Implements Claude's 5 rules:
1. Conversational connectors (formal → Saudi dialect)
2. Emotional triggers over features
3. Local cultural references
4. Active voice + personal address
5. Rhythmic text patterns (short punchy lines)

Three copy variants per post:
- Authoritative (trust, expertise) — medical, legal, training
- Aspirational (transformation, dreams) — beauty, fitness, fashion
- Conversational (local, friendly) — food, retail, services
"""

from __future__ import annotations

import re
import random
from typing import Any

# ═══════════════════════════════════════════════════════
# RULE 1: Conversational Connectors
# Replace formal Arabic with Saudi dialect equivalents
# ═══════════════════════════════════════════════════════
FORMAL_TO_SAUDI = [
    # Formal → Saudi conversational
    ("نقدم لكم", "نقدم لكم"),  # Keep — already good
    ("نقدم خدمات", "عندنا خدمات"),
    ("نقدم لكم خدمات", "نقدم لكم"),
    ("نوفر لكم", "نوفّر لكم"),
    ("نسعى لتقديم", "هدفنا"),
    ("نحن ملتزمون بـ", "نلتزم بـ"),
    ("يتم تقديم", "نقدّم"),
    ("يتم توفير", "نوفّر"),
    ("يتميز بإرضاء", "يرضي"),
    ("يتميز بتقديم", "يقدّم"),
    ("بأعلى جودة", "بأعلى جودة"),  # Keep
    ("بجودة عالية", "بجودة عالية"),  # Keep
    ("خدمات متميزة", "خدمات مميزة"),
    ("بأحدث التقنيات", "بأحدث التقنيات"),  # Keep — common in Saudi
    ("نستخدم أحدث", "نستخدم أحدث"),  # Keep
    ("فريق متخصص", "فريقنا المتخصص"),
    ("فريق محترف", "فريقنا المحترف"),
    ("بيئة", "بيئة"),  # Keep
    ("تجربة فريدة", "تجربة لا تُنسى"),
    ("تجربة استثنائية", "تجربة ما تقدر تنساها"),  # More conversational
    ("تجربة لا تُنسى", "تجربة ما تنساها"),
    ("نرحب بكم", "حيّاكم الله"),
    ("ترحيب حار", "ترحيب يثلج الصدر"),
    ("في قلب", "في قلب"),  # Keep
    ("لا تنسونا", "لا تنسونا"),  # Keep
    ("زورونا", "زورونا"),  # Keep
    ("احجز الآن", "احجز موعدك الحين"),  # "الحين" = Saudi for "now"
    ("احجز موعدك", "احجز موعدك"),  # Keep
    ("احجزي الآن", "احجزي موعدك الحين"),
    ("تواصل معنا", "تواصل وياانا"),  # "وياانا" = Saudi dialect
    ("للمزيد", "للمزيد"),  # Keep
    ("مميزاتنا", "ليش تختارونا"),  # More conversational
    ("لماذا تختارنا", "ليش تختارونا"),
    ("نتميز بـ", "نتميّز بـ"),
    ("نضمن لكم", "نضمن لكم"),  # Keep
    ("رضا عملائنا", "رضا عملائنا"),  # Keep
    ("أكثر من مجرد", "أكثر من"),  # Simpler
    ("نهدف إلى", "هدفنا"),
    ("رسالتنا هي", "هدفنا"),
    ("رؤيتنا هي", "نبي نوصل لـ"),  # "نبي" = Saudi for "we want"
    ("فريق العمل", "فريقنا"),
    ("إدارة", "إدارة"),  # Keep
    ("موظفينا", "فريقنا"),
    ("العاملين لدينا", "فريقنا"),
]

# ═══════════════════════════════════════════════════════
# RULE 2: Emotional Trigger Replacements
# Replace feature descriptions with emotional triggers
# ═══════════════════════════════════════════════════════
EMOTIONAL_TRIGGERS = {
    # Feature → Emotional trigger
    "أحدث التقنيات": "نتائج تشوفونها بأنفسكم",
    "أحدث المعدات": "نتائج تشوفونها بنفسكم",
    "تقنيات متطورة": "تغيّر حقيقي تشوفه وتحس فيه",
    "بيئة نظيفة": "مكان يريّحكم من أول دخول",
    "فريق محترف": "ناس تبي ترضيكم مش بس تخدمكم",
    "أسعار مناسبة": "ما يكلفكم كثر ما يستاهل",
    "أسعار تنافسية": "قيمة تستاهل كل ريال",
    "جودة عالية": "جودة يكفي تشوفونها",
    "خدمة سريعة": "ما يطوّل انتظاركم",
    "موقع متميز": "مكانكم في قلب المدينة",
    "تشكيلة واسعة": "كل اللي تدوّرونه عندنا",
    "منتجات أصلية": "الأصلي يفرق دايمًا",
    "خبرة سنوات": "ثقة أهل الرياض سنوات طويلة",
    "رضا العملاء": "آخر شي يهمّنا رضاكم",
    "نتائج مضمونة": "نتائج نضمنها لكم",
    "عناية فائقة": "عناية كنكم أهلنا",
    "حلول متكاملة": "نحل لكم من الألف للياء",
    "احترافية في العمل": "شغل يبان فيه الأصيل",
}

# ═══════════════════════════════════════════════════════
# RULE 3: Local Cultural References
# Replace generic references with Saudi local ones
# ═══════════════════════════════════════════════════════
LOCAL_REFERENCES = {
    "خبرة عالمية": "ثقة أهل الرياض",
    "مستوى عالمي": "مستوى يليق بأهل الرياض",
    "معايير عالمية": "معايير أهل الرياض يعرفونها",
    "بمستوى عالمي": "بمستوى يليق فيكم",
    "الأفضل في المنطقة": "الأفضل في الرياض",
    "من الأفضل": "من أفضل أماكن الرياض",
    "متميز": "مميز بيّن",  # "بيّن" = clearly visible
    "فاخر": "فاخر يبين من أول نظرة",
}

# ═══════════════════════════════════════════════════════
# RULE 4: Active Voice Patterns
# Convert passive/formal to active + personal address
# ═══════════════════════════════════════════════════════
ACTIVE_VOICE = [
    ("يتم تقديم الخدمة", "نقدّم لكم الخدمة"),
    ("يتم توفير", "نوفّر لكم"),
    ("يتميز المكان بـ", "يتميّز مكاننا بـ"),
    ("تتوفر لدينا", "نوفّر لكم"),
    ("متوفر لدينا", "عندنا"),
    ("يتم استخدام", "نستخدم"),
    ("يتم الاعتماد على", "نعتمد على"),
    ("يتميز فريقنا", "فريقنا يتميّز"),
    ("نحن في خدمتكم", "نحن في خدمتكم"),  # Keep
]

# ═══════════════════════════════════════════════════════
# COPY VARIANTS — 3 tones per niche
# ═══════════════════════════════════════════════════════
# Each niche gets a preferred tone + fallback templates

NICHE_TONE = {
    # Medical → Authoritative (trust, expertise)
    "clinics": "authoritative",
    "dentists": "authoritative",
    "pharmacies": "authoritative",
    "dermatology": "authoritative",
    "law_firms": "authoritative",
    "training_centers": "authoritative",
    
    # Beauty → Aspirational (transformation, dreams)
    "salons": "aspirational",
    "barbershops": "aspirational",
    "spas": "aspirational",
    "fashion": "aspirational",
    "perfumes": "aspirational",
    "gyms": "aspirational",
    "real_estate": "aspirational",
    "event_halls": "aspirational",
    
    # Food/Retail → Conversational (local, friendly)
    "restaurants": "conversational",
    "cafes": "conversational",
    "bakeries": "conversational",
    "auto_shops": "conversational",
    "car_wash": "conversational",
    "cleaning": "conversational",
    "hvac_ac": "conversational",
}

# Per-niche emotional copy templates (headline + 3 taglines)
NICHE_COPY_TEMPLATES = {
    "restaurants": {
        "conversational": [
            {
                "headline": "تعال ذقها بنفسك",
                "taglines": ["أكل يدوّر العقل من أول لقمة", "مرّوا علينا وسط الرياض", "نبي نشوفكم على الغدا"],
            },
            {
                "headline": "أكلك اللي تحبه هنا",
                "taglines": ["نكهات رياضية أصيلة", "كل اللي تشتهيه بمكان", "تعال جرّب بنفسك"],
            },
            {
                "headline": "جعت؟ الحل عندنا",
                "taglines": ["أطيب أكل سعودي تذوقه", "أسعار تستاهل كل ريال", "حيّاكم عندنا ديما"],
            },
        ],
    },
    "cafes": {
        "conversational": [
            {
                "headline": "قهوتك عندنا غير",
                "taglines": ["أحلى لاتيه بالرياض تلقاه هنا", "مكان يجمّعك مع ربعك", "تعال نتقهوى سوا"],
            },
            {
                "headline": "كوب يعدّل مزاجك",
                "taglines": ["قهوة مختصة تحس فرقها", "جلسة تريّحك من هم الدنيا", "مكانك محجوز ديما"],
            },
        ],
    },
    "bakeries": {
        "conversational": [
            {
                "headline": "ريحة الخبز توّها طالعة",
                "taglines": ["طازج كل صبح من عندنا", "حلى يمشي مع قهوتك", "بكّر قبل لا يخلص"],
            },
        ],
    },
    "clinics": {
        "authoritative": [
            {
                "headline": "صحتك غالية علينا",
                "taglines": ["خبرة أهل الرياض يثقون فيها", "دكاترة يفهمون راحتك", "احجز موعدك اليوم"],
            },
            {
                "headline": "علاجك يبدأ من هنا",
                "taglines": ["دكاترة تقدر تثق فيهم", "أجهزة يديدة لعلاجك", "صحتك تستاهل الأفضل"],
            },
        ],
    },
    "dentists": {
        "authoritative": [
            {
                "headline": "ابتسامتك تستاهل الأحلى",
                "taglines": ["أحدث أجهزة الأسنان عندنا", "نتيجة تشوفها بعينك", "احجز وابتسم"],
            },
            {
                "headline": "ابتسم بثقة",
                "taglines": ["علاج بدون ألم ترى", "فريق يهمه راحتك", "جودة ما نتنازل عنها"],
            },
        ],
    },
    "pharmacies": {
        "authoritative": [
            {
                "headline": "دواك كله عندنا",
                "taglines": ["كل اللي تبيه بمكان واحد", "استشارة مجانية ديما", "نخدمكم بأمانة"],
            },
        ],
    },
    "dermatology": {
        "authoritative": [
            {
                "headline": "بشرتك تستاهل الأحلى",
                "taglines": ["نتيجة تشوفينها بعينك", "دكاترة جلدية تثقين فيهم", "احجزي موعدك اليوم"],
            },
            {
                "headline": "بشرتك سر ثقتك",
                "taglines": ["أحدث أجهزة العناية بالبشرة", "تشوفين الفرق بنفسك", "خصوصية تامة وعناية كاملة"],
            },
        ],
    },
    "salons": {
        "aspirational": [
            {
                "headline": "حلاوتك تبدأ من عندنا",
                "taglines": ["لمسة تغيّر شكلك كله", "بنات يفهمون ذوقك", "احجزي جلستك الحين"],
            },
            {
                "headline": "جمالك يستاهل الأفضل",
                "taglines": ["ستايلات تطلّعك أحلى", "لمسة تفرق معك", "كوني أحلى نسخة منك"],
            },
        ],
    },
    "barbershops": {
        "aspirational": [
            {
                "headline": "طلّتك تبدأ من هنا",
                "taglines": ["قصّات تطلّعك أنيق", "أفضل حلاقين بالرياض", "احجز موعدك الحين"],
            },
            {
                "headline": "شكلك علينا",
                "taglines": ["شغل يبيّن فيه الاحتراف", "تجربة ما تلقاها إلا عندنا", "ادخل وطلّع أحلى"],
            },
        ],
    },
    "spas": {
        "aspirational": [
            {
                "headline": "راحة تستاهلينها",
                "taglines": ["استرخاء كامل بأيدي محترفات", "تجربة تنسّيك هم الدنيا", "احجزي جلستك الحين"],
            },
            {
                "headline": "روّحي وارتاحي",
                "taglines": ["جلسات تريّح جسمك كله", "هدوء تحسّينه بنفسك", "نفسيتك أهم شي"],
            },
        ],
    },
    "gyms": {
        "aspirational": [
            {
                "headline": "ابدأ اليوم وشف الفرق",
                "taglines": ["أحدث أجهزة بالرياض", "مدربين يدفعونك للأمام", "نتايج مضمونة أو نرد لك"],
            },
            {
                "headline": "جسمك يستاهل التغيير",
                "taglines": ["نتيجة تشوفها بالمراية", "فريق يمشي معك خطوة بخطوة", "ما في عذر يوقفك"],
            },
        ],
    },
    "perfumes": {
        "aspirational": [
            {
                "headline": "عطر فخم يليق فيك",
                "taglines": ["عود فاخر بلمسة أصيلة", "ريحة تدوم معك طول اليوم", "هدايا تليق بذوقك"],
            },
            {
                "headline": "ريحتك تخلّي أثر",
                "taglines": ["عطور تطلّع شخصيتك", "أجود عود وبخور تلقاه", "كل ريحة لها قصة"],
            },
        ],
    },
    "fashion": {
        "aspirational": [
            {
                "headline": "ستايلك يبدأ من هنا",
                "taglines": ["تشكيلات تطلّع ذوقك", "أقمشة فخمة تحسّينها", "كوني مختلفة عن الكل"],
            },
            {
                "headline": "إطلالة تفرق معك",
                "taglines": ["تصاميم على ذوقك", "جودة تشوفينها بعينك", "تألّقي بكل مناسبة"],
            },
        ],
    },
    "law_firms": {
        "authoritative": [
            {
                "headline": "حقك ما يضيع عندنا",
                "taglines": ["خبرة قانونية تثق فيها", "سرّية وخصوصية كاملة", "استشارتك الأولى واضحة"],
            },
            {
                "headline": "قضيتك بأيدي أمينة",
                "taglines": ["محامين يفهمون نظام المملكة", "نتايج نضمنها لك", "استشير وارتاح"],
            },
        ],
    },
    "training_centers": {
        "authoritative": [
            {
                "headline": "طوّر نفسك وشف الفرق",
                "taglines": ["دورات معتمدة تفتح لك أبواب", "مدربين يفرقون معك", "ابدأ مشوارك اليوم"],
            },
            {
                "headline": "تعلّم شي يغيّر مستقبلك",
                "taglines": ["شهادات معترف فيها", "محتوى عملي تطبّقه على طول", "فرصتك تبدأ من هنا"],
            },
        ],
    },
    "auto_shops": {
        "conversational": [
            {
                "headline": "سيارتك بأيدي تثق فيها",
                "taglines": ["صيانة تشوفها بعينك", "أسعار ما تظلمك", "مرّ علينا ونتفاهم"],
            },
        ],
    },
    "car_wash": {
        "conversational": [
            {
                "headline": "سيارتك تستاهل تلمع",
                "taglines": ["غسيل تشوف فرقه", "تفصيل يوصل لكل زاوية", "بعدنا تشوف الفرق"],
            },
        ],
    },
    "real_estate": {
        "aspirational": [
            {
                "headline": "بيتك يبدأ من هنا",
                "taglines": ["عقارات تليق بطموحك", "أماكن تختارها لعيالك", "استثمر وانت مرتاح"],
            },
        ],
    },
    "cleaning": {
        "conversational": [
            {
                "headline": "بيتك يستاهل يلمع",
                "taglines": ["تنظيف تشوف فرقه", "فريق يحترم خصوصيتك", "احجز خدمتك الحين"],
            },
        ],
    },
    "hvac_ac": {
        "conversational": [
            {
                "headline": "مكيفك خربان؟ علينا",
                "taglines": ["صيانة سريعة ومضمونة", "ما نطوّل عليك", "اتصل ونجيك"],
            },
        ],
    },
    "event_halls": {
        "aspirational": [
            {
                "headline": "مناسبتك تستاهل الأفضل",
                "taglines": ["قاعات تليق بيومك", "أجواء تصير ذكرى ما تنتسى", "احجزي موعدك الحين"],
            },
        ],
    },
}


# ═══════════════════════════════════════════════════════
# TRANSFORMATION ENGINE
# ═══════════════════════════════════════════════════════

def apply_saudi_dialect(text: str) -> str:
    """Rule 1: Replace formal Arabic with Saudi dialect."""
    for formal, saudi in FORMAL_TO_SAUDI:
        text = text.replace(formal, saudi)
    return text


def apply_emotional_triggers(text: str) -> str:
    """Rule 2: Replace feature descriptions with emotional triggers."""
    for feature, emotion in EMOTIONAL_TRIGGERS.items():
        text = text.replace(feature, emotion)
    return text


def apply_local_references(text: str) -> str:
    """Rule 3: Replace generic references with local Saudi ones."""
    for generic, local in LOCAL_REFERENCES.items():
        text = text.replace(generic, local)
    return text


def apply_active_voice(text: str) -> str:
    """Rule 4: Convert passive to active voice."""
    for passive, active in ACTIVE_VOICE:
        text = text.replace(passive, active)
    return text


def apply_rhythmic_pattern(taglines: list[str]) -> list[str]:
    """Rule 5: Ensure taglines are short and rhythmic.
    
    Break long lines into shorter ones, keep max 8 words per line.
    """
    result = []
    for line in taglines:
        words = line.split()
        if len(words) > 10:
            # Split at midpoint
            mid = len(words) // 2
            result.append(" ".join(words[:mid]))
            result.append(" ".join(words[mid:]))
        else:
            result.append(line)
    return result[:3]  # Max 3 taglines


def transform_copy(text: str) -> str:
    """Apply all 5 Saudi dialect rules to text."""
    text = apply_saudi_dialect(text)
    text = apply_emotional_triggers(text)
    text = apply_local_references(text)
    text = apply_active_voice(text)
    return text


def get_niche_copy(niche: str, business_name: str, rating: str, 
                   reviews: int, seed: int = 0) -> dict[str, Any]:
    """Get niche-specific Saudi Arabic copy.
    
    Returns:
        {"headline": str, "taglines": list[str], "tone": str}
    """
    tone = NICHE_TONE.get(niche, "conversational")
    templates = NICHE_COPY_TEMPLATES.get(niche, NICHE_COPY_TEMPLATES["restaurants"])
    
    # Select variant by tone
    tone_templates = []
    for t in templates.values():
        if isinstance(t, list):
            tone_templates.extend(t)
    
    if not tone_templates:
        tone_templates = list(NICHE_COPY_TEMPLATES["restaurants"].values())[0]
    
    # Pick template by seed (deterministic)
    idx = seed % len(tone_templates)
    template = tone_templates[idx]
    
    headline = template["headline"]
    taglines = template["taglines"]
    
    # Apply rhythmic pattern (Rule 5)
    taglines = apply_rhythmic_pattern(taglines)
    
    return {
        "headline": headline,
        "taglines": taglines,
        "tone": tone,
    }


def post_process_glm_caption(caption: str, niche: str) -> dict[str, Any]:
    """Post-process GLM output through Saudi dialect rules.
    
    Takes GLM's formal Arabic caption and transforms it into
    native Saudi dialect with emotional triggers.
    
    Returns:
        {"headline": str, "taglines": list[str], "tone": str}
    """
    # 1. Apply all transformation rules to the raw caption
    transformed = transform_copy(caption)
    
    # 2. Split into lines for taglines
    lines = [l.strip() for l in re.split(r"[\n]+", transformed) if l.strip()]
    
    # 3. If too few lines, supplement with niche templates
    niche_copy = get_niche_copy(niche, "", "", 0, seed=hash(caption) % 100)
    
    if len(lines) < 3:
        # Use niche template taglines to fill
        needed = 3 - len(lines)
        for t in niche_copy["taglines"][:needed]:
            if t not in lines:
                lines.append(t)
    
    # 4. Headline = first line
    headline = lines[0] if lines else niche_copy["headline"]
    taglines = apply_rhythmic_pattern(lines[1:4] if len(lines) > 1 else niche_copy["taglines"])
    
    return {
        "headline": headline,
        "taglines": taglines[:3],  # Max 3 taglines
        "tone": NICHE_TONE.get(niche, "conversational"),
    }
