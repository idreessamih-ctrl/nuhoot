"""Niche Configuration — All Saudi SME business niches supported by Nuhoot.

Each niche has:
- kicker: English label at top of design
- business_label_ar: Arabic noun for the business type
- accent: color theme key (maps to ACCENT_COLORS below)
- colors: actual CSS color values for this niche
- tone: emotional register for marketing copy
- maps_search_term: Google Maps category to search
- default_example: example business name in Arabic
"""

# ═══════════════════════════════════════════════════════
# ACCENT COLOR PALETTES — actual CSS values per accent type
# Each palette: light, core, deep, glint, grad, bg (panel background)
# ═══════════════════════════════════════════════════════
ACCENT_COLORS = {
    "gold": {
        "light": "#F2D9A0", "core": "#C9A25A", "deep": "#8C6A2E",
        "glint": "#FBEFC0",
        "grad": "linear-gradient(135deg,#8C6A2E,#C9A25A,#F2D9A0,#FBEFC0,#C9A25A,#8C6A2E)",
        "bg": "#1A140D", "bg2": "#2A2015",
    },
    "warm-gold": {
        "light": "#F5D0A0", "core": "#D49A45", "deep": "#9C6820",
        "glint": "#FFE8C0",
        "grad": "linear-gradient(135deg,#9C6820,#D49A45,#F5D0A0,#FFE8C0,#D49A45,#9C6820)",
        "bg": "#1F1608", "bg2": "#32230F",
    },
    "teal-gold": {
        "light": "#A0E8E0", "core": "#2DB8A8", "deep": "#156B5E",
        "glint": "#D0FFF5",
        "grad": "linear-gradient(135deg,#156B5E,#2DB8A8,#A0E8E0,#D0FFF5,#2DB8A8,#156B5E)",
        "bg": "#0A1A18", "bg2": "#0F2825",
    },
    "teal-rose": {
        "light": "#A0E8D8", "core": "#1DB8A0", "deep": "#0A5E52",
        "glint": "#D0FFF5",
        "grad": "linear-gradient(135deg,#0A5E52,#1DB8A0,#A0E8D8,#D0FFF5,#1DB8A0,#0A5E52)",
        "bg": "#0A1A16", "bg2": "#0F2820",
    },
    "rose-gold": {
        "light": "#F5C2C8", "core": "#D4737E", "deep": "#8C3A4A",
        "glint": "#FFE0E5",
        "grad": "linear-gradient(135deg,#8C3A4A,#D4737E,#F5C2C8,#FFE0E5,#D4737E,#8C3A4A)",
        "bg": "#1A0A0E", "bg2": "#2A1015",
    },
    "steel-gold": {
        "light": "#B8CCE0", "core": "#4A7090", "deep": "#1E3A52",
        "glint": "#D8E8F5",
        "grad": "linear-gradient(135deg,#1E3A52,#4A7090,#B8CCE0,#D8E8F5,#4A7090,#1E3A52)",
        "bg": "#0A0F15", "bg2": "#121A25",
    },
    "sage-gold": {
        "light": "#D2EDB8", "core": "#7BC868", "deep": "#3E7830",
        "glint": "#E8FFD8",
        "grad": "linear-gradient(135deg,#3E7830,#7BC868,#D2EDB8,#E8FFD8,#7BC868,#3E7830)",
        "bg": "#080F06", "bg2": "#0C1808",
    },
    "navy-gold": {
        "light": "#C8D8F0", "core": "#5A78B0", "deep": "#2A456E",
        "glint": "#E0ECF8",
        "grad": "linear-gradient(135deg,#2A456E,#5A78B0,#C8D8F0,#E0ECF8,#5A78B0,#2A456E)",
        "bg": "#0E1428", "bg2": "#161E38",
    },
    "energy-gold": {
        "light": "#A0FFE8", "core": "#10D8B8", "deep": "#008B7E",
        "glint": "#D0FFF5",
        "grad": "linear-gradient(135deg,#008B7E,#10D8B8,#A0FFE8,#D0FFF5,#10D8B8,#008B7E)",
        "bg": "#061814", "bg2": "#0A2820",
    },
    "fresh-gold": {
        "light": "#A8E8E0", "core": "#20B8A0", "deep": "#0A6858",
        "glint": "#C8FFF5",
        "grad": "linear-gradient(135deg,#0A6858,#20B8A0,#A8E8E0,#C8FFF5,#20B8A0,#0A6858)",
        "bg": "#08141A", "bg2": "#0F2028",
    },
    "royal-gold": {
        "light": "#D0B8F0", "core": "#7A4AC0", "deep": "#3A1A6E",
        "glint": "#E8D8FF",
        "grad": "linear-gradient(135deg,#3A1A6E,#7A4AC0,#D0B8F0,#E8D8FF,#7A4AC0,#3A1A6E)",
        "bg": "#0A0814", "bg2": "#120E25",
    },
    "amber-gold": {
        "light": "#F5D898", "core": "#C89838", "deep": "#8C6010",
        "glint": "#FFEFC0",
        "grad": "linear-gradient(135deg,#8C6010,#C89838,#F5D898,#FFEFC0,#C89838,#8C6010)",
        "bg": "#140E02", "bg2": "#221805",
    },
}


NICHES = {
    # ═══════════════════════════════════════════════════════
    # FOOD & BEVERAGE
    # ═══════════════════════════════════════════════════════
    "restaurants": {
        "kicker": "RIYADH · FINE DINING",
        "business_label_ar": "مطعم",
        "accent": "gold",
        "tone": "warm, inviting, appetizing, premium",
        "maps_search_term": "restaurants",
        "default_example": "مطعم النخيل الذهبي",
    },
    "cafes": {
        "kicker": "RIYADH · SPECIALTY COFFEE",
        "business_label_ar": "مقهى",
        "accent": "gold",
        "tone": "cozy, artisanal, modern, social",
        "maps_search_term": "cafes",
        "default_example": "مقهى البن المختص",
    },
    "bakeries": {
        "kicker": "RIYADH · FRESH BAKERY",
        "business_label_ar": "مخبز",
        "accent": "warm-gold",
        "tone": "fresh, wholesome, artisanal, homemade",
        "maps_search_term": "bakery",
        "default_example": "مخبز الحنان",
    },

    # ═══════════════════════════════════════════════════════
    # HEALTH & MEDICAL
    # ═══════════════════════════════════════════════════════
    "clinics": {
        "kicker": "RIYADH · EXPERT CARE",
        "business_label_ar": "عيادة",
        "accent": "teal-gold",
        "tone": "trustworthy, professional, clean, reassuring, expert",
        "maps_search_term": "clinics",
        "default_example": "عيادة الشفاء التخصصية",
    },
    "dentists": {
        "kicker": "RIYADH · DENTAL CARE",
        "business_label_ar": "عيادة أسنان",
        "accent": "teal-gold",
        "tone": "precise, gentle, modern, reassuring, confident",
        "maps_search_term": "dentist",
        "default_example": "عيادة الابتسامة الذهبية",
    },
    "pharmacies": {
        "kicker": "RIYADH · YOUR HEALTH",
        "business_label_ar": "صيدلية",
        "accent": "teal-gold",
        "tone": "trusted, accessible, caring, professional, available",
        "maps_search_term": "pharmacy",
        "default_example": "صيدلية الرعاية",
    },
    "dermatology": {
        "kicker": "RIYADH · SKIN EXPERTS",
        "business_label_ar": "مركز جلدية",
        "accent": "teal-rose",
        "tone": "modern, results-focused, confidence-building, expert",
        "maps_search_term": "dermatologist",
        "default_example": "مركز الجلدية والتجميل",
    },

    # ═══════════════════════════════════════════════════════
    # BEAUTY & PERSONAL CARE
    # ═══════════════════════════════════════════════════════
    "salons": {
        "kicker": "RIYADH · BEAUTY & STYLE",
        "business_label_ar": "صالون",
        "accent": "rose-gold",
        "tone": "glamorous, elegant, trendy, pampering, transformation",
        "maps_search_term": "beauty_salon",
        "default_example": "صالون لمسة جمال",
    },
    "barbershops": {
        "kicker": "RIYADH · GENTLEMEN'S GROOMING",
        "business_label_ar": "حلاقة رجالية",
        "accent": "steel-gold",
        "tone": "sharp, classic, confident, modern, precise",
        "maps_search_term": "barber_shop",
        "default_example": "حلاقة الذوق الرفيع",
    },
    "spas": {
        "kicker": "RIYADH · LUXURY SPA",
        "business_label_ar": "سبا",
        "accent": "sage-gold",
        "tone": "serene, luxurious, rejuvenating, calming, indulgent",
        "maps_search_term": "spa",
        "default_example": "سبا السكينة",
    },

    # ═══════════════════════════════════════════════════════
    # AUTOMOTIVE
    # ═══════════════════════════════════════════════════════
    "auto_shops": {
        "kicker": "RIYADH · TRUSTED SERVICE",
        "business_label_ar": "ورشة سيارات",
        "accent": "steel-gold",
        "tone": "trustworthy, precise, efficient, fair, expert",
        "maps_search_term": "auto_repair_shop",
        "default_example": "ورشة الدقة للسيارات",
    },
    "car_wash": {
        "kicker": "RIYADH · PRISTINE CARE",
        "business_label_ar": "غسيل سيارات",
        "accent": "steel-gold",
        "tone": "pristine, efficient, detail-oriented, premium, satisfying",
        "maps_search_term": "car_wash",
        "default_example": "غسيل وتلميع السيارات الفاخر",
    },

    # ═══════════════════════════════════════════════════════
    # REAL ESTATE
    # ═══════════════════════════════════════════════════════
    "real_estate": {
        "kicker": "RIYADH · PREMIUM LIVING",
        "business_label_ar": "عقارات",
        "accent": "navy-gold",
        "tone": "luxurious, aspirational, investment-savvy, lifestyle, location-focused",
        "maps_search_term": "real_estate_agency",
        "default_example": "دار العقارات",
    },

    # ═══════════════════════════════════════════════════════
    # FITNESS & SPORTS
    # ═══════════════════════════════════════════════════════
    "gyms": {
        "kicker": "RIYADH · STRENGTH & FITNESS",
        "business_label_ar": "جيم",
        "accent": "teal-gold",
        "tone": "motivating, energetic, results-driven, community, empowering",
        "maps_search_term": "gym",
        "default_example": "جيم القوة والعافية",
    },

    # ═══════════════════════════════════════════════════════
    # HOME SERVICES
    # ═══════════════════════════════════════════════════════
    "hvac_ac": {
        "kicker": "RIYADH · COOL COMFORT",
        "business_label_ar": "صيانة مكيفات",
        "accent": "steel-gold",
        "tone": "reliable, fast, expert, comfortable, honest",
        "maps_search_term": "hvac_contractor",
        "default_example": "مؤسسة الراحة للتكييف",
    },
    "cleaning": {
        "kicker": "RIYADH · SPOTLESS SPACES",
        "business_label_ar": "شركة تنظيف",
        "accent": "sage-gold",
        "tone": "thorough, professional, trustworthy, fresh, detail-oriented",
        "maps_search_term": "cleaning_service",
        "default_example": "شركة النقاء للتنظيف",
    },

    # ═══════════════════════════════════════════════════════
    # EDUCATION & TRAINING
    # ═══════════════════════════════════════════════════════
    "training_centers": {
        "kicker": "RIYADH · SKILL BUILDING",
        "business_label_ar": "مركز تدريب",
        "accent": "navy-gold",
        "tone": "empowering, professional, career-focused, credible, growth-oriented",
        "maps_search_term": "training_center",
        "default_example": "مركز التميز للتدريب",
    },

    # ═══════════════════════════════════════════════════════
    # EVENTS & HOSPITALITY
    # ═══════════════════════════════════════════════════════
    "event_halls": {
        "kicker": "RIYADH · CELEBRATION VENUES",
        "business_label_ar": "قاعة مناسبات",
        "accent": "amber-gold",
        "tone": "grand, elegant, celebratory, memorable, hospitable",
        "maps_search_term": "wedding_venue",
        "default_example": "قاعة اللؤلؤة للمناسبات",
    },

    # ═══════════════════════════════════════════════════════
    # RETAIL
    # ═══════════════════════════════════════════════════════
    "perfumes": {
        "kicker": "RIYADH · LUXURY FRAGRANCES",
        "business_label_ar": "عطور",
        "accent": "amber-gold",
        "tone": "luxurious, exotic, refined, distinctive, gift-worthy",
        "maps_search_term": "perfume_store",
        "default_example": "دار العطور الفاخرة",
    },
    "fashion": {
        "kicker": "RIYADH · STYLE & ELEGANCE",
        "business_label_ar": "أزياء",
        "accent": "rose-gold",
        "tone": "elegant, trendy, quality, distinctive, confident",
        "maps_search_term": "clothing_store",
        "default_example": "بوتيك الأناقة",
    },

    # ═══════════════════════════════════════════════════════
    # PROFESSIONAL SERVICES
    # ═══════════════════════════════════════════════════════
    "law_firms": {
        "kicker": "RIYADH · LEGAL EXCELLENCE",
        "business_label_ar": "مكتب محاماة",
        "accent": "navy-gold",
        "tone": "authoritative, trustworthy, expert, discreet, results-driven",
        "maps_search_term": "lawyer",
        "default_example": "مكتب العدالة القانوني",
    },
}


# ═══════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════
def get_niche_config(niche: str) -> dict:
    """Get configuration for a niche. Falls back to restaurants."""
    return NICHES.get(niche, NICHES["restaurants"])


def get_kicker(niche: str) -> str:
    return get_niche_config(niche)["kicker"]


def get_accent(niche: str) -> str:
    return get_niche_config(niche)["accent"]


def get_colors(niche: str) -> dict:
    """Get the actual CSS color values for a niche's accent."""
    accent_key = get_niche_config(niche)["accent"]
    return ACCENT_COLORS.get(accent_key, ACCENT_COLORS["gold"])


def get_maps_term(niche: str) -> str:
    return get_niche_config(niche)["maps_search_term"]


# ═══════════════════════════════════════════════════════
# TRUST BADGES — credibility text shown on each design
# Small text below rating that builds trust
# Written in authentic Saudi dialect (verified by Opus)
# ═══════════════════════════════════════════════════════
TRUST_BADGES = {
    "clinics": "معتمد من وزارة الصحة",
    "dentists": "معتمد من وزارة الصحة",
    "dermatology": "معتمد من وزارة الصحة",
    "pharmacies": "مرخصة من وزارة الصحة",
    "law_firms": "محامين معتمدين من وزارة العدل",
    "gyms": "نتايج مضمونة",
    "training_centers": "شهادات معتمدة",
    "restaurants": "تقييم 4.7 على خرائط جوجل",
    "cafes": "حبوب محمّصة كل يوم",
    "spas": "أيدي محترفة ومرخّصة",
    "barbershops": "أفضل حلاقين بالرياض",
    "perfumes": "عطور فاخرة معتمدة دولياً",
    "bakeries": "طازج كل صبح",
    "salons": "خبيرات معتمدات",
    "fashion": "أقمشة فاخرة مستوردة",
    "auto_shops": "ضمان على الصيانة",
    "car_wash": "تلميع احترافي مضمون",
    "real_estate": "عقارات موثقة ومسجلة",
    "hvac_ac": "صيانة معتمدة",
    "cleaning": "مواد آمنة ومصرّح بها",
    "event_halls": "خبرة بتنظيم المناسبات",
}


def get_trust_badge(niche: str) -> str:
    """Get the trust badge text for a niche."""
    return TRUST_BADGES.get(niche, "")


def get_default_example(niche: str) -> str:
    return get_niche_config(niche)["default_example"]


def list_all_niches() -> list:
    return list(NICHES.keys())


SECTOR_GROUPS = {
    "Food & Beverage": ["restaurants", "cafes", "bakeries"],
    "Health & Medical": ["clinics", "dentists", "pharmacies", "dermatology"],
    "Beauty & Personal Care": ["salons", "barbershops", "spas"],
    "Automotive": ["auto_shops", "car_wash"],
    "Real Estate": ["real_estate"],
    "Fitness & Sports": ["gyms"],
    "Home Services": ["hvac_ac", "cleaning"],
    "Education & Training": ["training_centers"],
    "Events & Hospitality": ["event_halls"],
    "Retail": ["perfumes", "fashion"],
    "Professional Services": ["law_firms"],
}
