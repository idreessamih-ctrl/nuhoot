"""
Nuhoot Niche Configuration — Per-niche design settings.

Each niche gets a unique combination of:
  - layout_pattern: which Layout component to use
  - font: 'kufi' (modern) or 'naskh' (traditional)
  - corner_radius: border radius for cards/buttons (niche identity)
  - shape_set: 'organic' | 'angular' | 'curved' | 'grid' | 'industrial'
  - default_icons: Lucide icon names for ContentFeatures
  - texture: niche-specific texture overlay type
  - gradient_angle: preferred gradient direction
  - type_scale: modular type ratio
  - pattern: which Pattern component to use
  - cta_variant: which CTA component variant
  - photo_component: preferred photo component
  - header_variant: preferred header component

This ensures every niche looks visually distinct.
"""

NICHE_CONFIG = {
    "restaurants": {
        "layout_pattern": "LayoutSplit",
        "font": "kufi",
        "corner_radius": 24,
        "shape_set": "organic",
        "default_icons": ["utensils", "flame", "clock"],
        "texture": "paper",
        "gradient_angle": 135,
        "type_scale": 1.333,
        "pattern": "PatternBokeh",
        "cta_variant": "CTAShimmer",
        "photo_component": "PhotoMosaic",
        "header_variant": "HeaderGradient",
        "decorative": ["DecorShapes", "ColorPanel"],
        "gender": "plural",
    },
    "cafes": {
        "layout_pattern": "LayoutStandard",
        "font": "kufi",
        "corner_radius": 20,
        "shape_set": "organic",
        "default_icons": ["coffee", "clock", "heart"],
        "texture": "paper",
        "gradient_angle": 160,
        "type_scale": 1.25,
        "pattern": "PatternBokeh",
        "cta_variant": "CTAButton",
        "photo_component": "PhotoSingle",
        "header_variant": "HeaderMinimal",
        "decorative": ["DecorShapes"],
        "gender": "plural",
    },
    "bakeries": {
        "layout_pattern": "LayoutMagazine",
        "font": "kufi",
        "corner_radius": 20,
        "shape_set": "organic",
        "default_icons": ["cookie", "flame", "star"],
        "texture": "paper",
        "gradient_angle": 120,
        "type_scale": 1.25,
        "pattern": "PatternDots",
        "cta_variant": "CTAButton",
        "photo_component": "PhotoGrid",
        "header_variant": "HeaderGradient",
        "decorative": ["DecorShapes", "Divider"],
        "gender": "plural",
    },
    "salons": {
        "layout_pattern": "LayoutMagazine",
        "font": "kufi",
        "corner_radius": 50,  # soft/rounded
        "shape_set": "curved",
        "default_icons": ["scissors", "sparkles", "heart"],
        "texture": "silk",
        "gradient_angle": 145,
        "type_scale": 1.25,
        "pattern": "PatternBokeh",
        "cta_variant": "CTADual",
        "photo_component": "PhotoCircle",
        "header_variant": "HeaderMixed",
        "decorative": ["DecorRings", "DecorCalligraphy"],
        "gender": "female",
    },
    "spas": {
        "layout_pattern": "LayoutPhotoFull",
        "font": "kufi",
        "corner_radius": 50,
        "shape_set": "curved",
        "default_icons": ["leaf", "droplet", "heart"],
        "texture": "silk",
        "gradient_angle": 150,
        "type_scale": 1.2,
        "pattern": "PatternBokeh",
        "cta_variant": "CTAGlow",
        "photo_component": "PhotoArch",
        "header_variant": "HeaderOverlay",
        "decorative": ["DecorRings", "DecorCalligraphy"],
        "gender": "female",
    },
    "barbershops": {
        "layout_pattern": "LayoutAsymmetric",
        "font": "kufi",
        "corner_radius": 8,
        "shape_set": "angular",
        "default_icons": ["scissors", "crown", "star"],
        "texture": "metal",
        "gradient_angle": 135,
        "type_scale": 1.414,
        "pattern": "PatternGrid",
        "cta_variant": "CTAGlow",
        "photo_component": "PhotoSingle",
        "header_variant": "HeaderSplit",
        "decorative": ["CornerBrackets", "EdgeLabel"],
        "gender": "male",
    },
    "gyms": {
        "layout_pattern": "LayoutAsymmetric",
        "font": "kufi",
        "corner_radius": 4,  # sharp/angular
        "shape_set": "angular",
        "default_icons": ["dumbbell", "zap", "award"],
        "texture": "carbon",
        "gradient_angle": 180,
        "type_scale": 1.5,
        "pattern": "PatternHex",
        "cta_variant": "CTAGlow",
        "photo_component": "PhotoDiagonal",
        "header_variant": "HeaderSplit",
        "decorative": ["DecorDiagonal", "CornerBrackets"],
        "gender": "male",
    },
    "clinics": {
        "layout_pattern": "LayoutStandard",
        "font": "kufi",
        "corner_radius": 8,  # clean
        "shape_set": "grid",
        "default_icons": ["stethoscope", "shield", "heart"],
        "texture": "paper",
        "gradient_angle": 135,
        "type_scale": 1.25,
        "pattern": "PatternGrid",
        "cta_variant": "CTAOutline",
        "photo_component": "PhotoGrid",
        "header_variant": "HeaderMinimal",
        "decorative": ["Divider", "FrameKeyline"],
        "gender": "plural",
    },
    "dentists": {
        "layout_pattern": "LayoutStandard",
        "font": "kufi",
        "corner_radius": 12,
        "shape_set": "grid",
        "default_icons": ["smile", "shield", "star"],
        "texture": "paper",
        "gradient_angle": 140,
        "type_scale": 1.25,
        "pattern": "PatternDots",
        "cta_variant": "CTAOutline",
        "photo_component": "PhotoSingle",
        "header_variant": "HeaderGradient",
        "decorative": ["Divider", "FrameKeyline"],
        "gender": "plural",
    },
    "pharmacies": {
        "layout_pattern": "LayoutSplit",
        "font": "kufi",
        "corner_radius": 12,
        "shape_set": "grid",
        "default_icons": ["pill", "shield", "clock"],
        "texture": "paper",
        "gradient_angle": 135,
        "type_scale": 1.25,
        "pattern": "PatternGrid",
        "cta_variant": "CTAOutline",
        "photo_component": "PhotoGrid",
        "header_variant": "HeaderSplit",
        "decorative": ["FrameKeyline", "Divider"],
        "gender": "plural",
    },
    "dermatology": {
        "layout_pattern": "LayoutMagazine",
        "font": "kufi",
        "corner_radius": 24,
        "shape_set": "curved",
        "default_icons": ["sparkles", "shield", "heart"],
        "texture": "silk",
        "gradient_angle": 145,
        "type_scale": 1.25,
        "pattern": "PatternBokeh",
        "cta_variant": "CTADual",
        "photo_component": "PhotoCircle",
        "header_variant": "HeaderMixed",
        "decorative": ["DecorRings", "DecorCalligraphy"],
        "gender": "female",
    },
    "fashion": {
        "layout_pattern": "LayoutMagazine",
        "font": "kufi",
        "corner_radius": 0,  # sharp/editorial
        "shape_set": "angular",
        "default_icons": ["shirt", "star", "crown"],
        "texture": "silk",
        "gradient_angle": 180,
        "type_scale": 1.618,  # golden ratio
        "pattern": "PatternIslamic",
        "cta_variant": "CTADual",
        "photo_component": "PhotoArch",
        "header_variant": "HeaderMixed",
        "decorative": ["DecorCalligraphy", "FrameKeyline"],
        "gender": "female",
    },
    "perfumes": {
        "layout_pattern": "LayoutPhotoFull",
        "font": "naskh",  # traditional
        "corner_radius": 50,
        "shape_set": "curved",
        "default_icons": ["droplet", "sparkles", "star"],
        "texture": "silk",
        "gradient_angle": 160,
        "type_scale": 1.25,
        "pattern": "PatternIslamic",
        "cta_variant": "CTAGlow",
        "photo_component": "PhotoArch",
        "header_variant": "HeaderMixed",
        "decorative": ["PatternIslamic", "DecorCalligraphy"],
        "gender": "female",
    },
    "law_firms": {
        "layout_pattern": "LayoutStandard",
        "font": "naskh",  # traditional
        "corner_radius": 4,  # sharp/classical
        "shape_set": "angular",
        "default_icons": ["scale", "shield", "briefcase"],
        "texture": "marble",
        "gradient_angle": 135,
        "type_scale": 1.333,
        "pattern": "PatternIslamic",
        "cta_variant": "CTAOutline",
        "photo_component": "PhotoSingle",
        "header_variant": "HeaderMixed",
        "decorative": ["FrameKeyline", "PatternIslamic"],
        "gender": "plural",
    },
    "real_estate": {
        "layout_pattern": "LayoutSplit",
        "font": "kufi",
        "corner_radius": 12,
        "shape_set": "grid",
        "default_icons": ["home", "key", "star"],
        "texture": "marble",
        "gradient_angle": 135,
        "type_scale": 1.333,
        "pattern": "PatternGrid",
        "cta_variant": "CTAShimmer",
        "photo_component": "PhotoArch",
        "header_variant": "HeaderGradient",
        "decorative": ["FrameKeyline", "Divider"],
        "gender": "plural",
    },
    "auto_shops": {
        "layout_pattern": "LayoutAsymmetric",
        "font": "kufi",
        "corner_radius": 4,
        "shape_set": "industrial",
        "default_icons": ["wrench", "car", "shield"],
        "texture": "carbon",
        "gradient_angle": 135,
        "type_scale": 1.414,
        "pattern": "PatternHex",
        "cta_variant": "CTAGlow",
        "photo_component": "PhotoDiagonal",
        "header_variant": "HeaderSplit",
        "decorative": ["DecorDiagonal", "CornerBrackets"],
        "gender": "male",
    },
    "car_wash": {
        "layout_pattern": "LayoutAsymmetric",
        "font": "kufi",
        "corner_radius": 16,
        "shape_set": "curved",
        "default_icons": ["droplet", "car", "sparkles"],
        "texture": "metal",
        "gradient_angle": 145,
        "type_scale": 1.333,
        "pattern": "PatternRays",
        "cta_variant": "CTAShimmer",
        "photo_component": "PhotoDiagonal",
        "header_variant": "HeaderGradient",
        "decorative": ["DecorDiagonal", "DecorShapes"],
        "gender": "male",
    },
    "cleaning": {
        "layout_pattern": "LayoutStandard",
        "font": "kufi",
        "corner_radius": 16,
        "shape_set": "organic",
        "default_icons": ["sparkles", "droplet", "shield"],
        "texture": "paper",
        "gradient_angle": 135,
        "type_scale": 1.25,
        "pattern": "PatternDots",
        "cta_variant": "CTAButton",
        "photo_component": "PhotoGrid",
        "header_variant": "HeaderMinimal",
        "decorative": ["DecorShapes", "Divider"],
        "gender": "plural",
    },
    "hvac_ac": {
        "layout_pattern": "LayoutSplit",
        "font": "kufi",
        "corner_radius": 8,
        "shape_set": "grid",
        "default_icons": ["wind", "thermometer", "shield"],
        "texture": "metal",
        "gradient_angle": 135,
        "type_scale": 1.333,
        "pattern": "PatternGrid",
        "cta_variant": "CTAOutline",
        "photo_component": "PhotoSingle",
        "header_variant": "HeaderSplit",
        "decorative": ["FrameKeyline", "EdgeLabel"],
        "gender": "plural",
    },
    "event_halls": {
        "layout_pattern": "LayoutPhotoFull",
        "font": "naskh",  # traditional
        "corner_radius": 24,
        "shape_set": "curved",
        "default_icons": ["sparkles", "star", "crown"],
        "texture": "silk",
        "gradient_angle": 145,
        "type_scale": 1.333,
        "pattern": "PatternRays",
        "cta_variant": "CTAShimmer",
        "photo_component": "PhotoArch",
        "header_variant": "HeaderOverlay",
        "decorative": ["PatternIslamic", "DecorCalligraphy"],
        "gender": "plural",
    },
    "training_centers": {
        "layout_pattern": "LayoutSplit",
        "font": "kufi",
        "corner_radius": 8,
        "shape_set": "grid",
        "default_icons": ["graduation-cap", "award", "star"],
        "texture": "paper",
        "gradient_angle": 135,
        "type_scale": 1.333,
        "pattern": "PatternHex",
        "cta_variant": "CTAOutline",
        "photo_component": "PhotoGrid",
        "header_variant": "HeaderSplit",
        "decorative": ["CornerBrackets", "Divider"],
        "gender": "plural",
    },
}


def get_niche_config(niche: str) -> dict:
    """Get design configuration for a specific niche."""
    return NICHE_CONFIG.get(niche, NICHE_CONFIG["restaurants"])


def get_layout_for_niche(niche: str) -> str:
    """Get the assigned layout pattern for a niche."""
    return NICHE_CONFIG.get(niche, {}).get("layout_pattern", "LayoutStandard")


def get_gender_for_niche(niche: str) -> str:
    """Get the Arabic gender form for a niche (male/female/plural)."""
    return NICHE_CONFIG.get(niche, {}).get("gender", "plural")


def get_font_for_niche(niche: str) -> str:
    """Get the font family for a niche ('kufi' or 'naskh')."""
    return NICHE_CONFIG.get(niche, {}).get("font", "kufi")


# Gender-specific Arabic text forms
GENDER_TEXTS = {
    "male": {
        "you_want": "تبي",
        "your_day": "يومك",
        "for_you": "لك",
        "dont_forget": "ما تنسى",
        "and_you": "وأنت",
    },
    "female": {
        "you_want": "تبين",
        "your_day": "يومك",  # NOT يومكي
        "for_you": "لك",  # NOT لكي
        "dont_forget": "ما تنسى",
        "and_you": "وانتي",
    },
    "plural": {
        "you_want": "تبون",
        "your_day": "يومكم",
        "for_you": "لكم",
        "dont_forget": "ما تنسون",
        "and_you": "وأنتوا",
    },
}


def get_gendered_text(niche: str, text_key: str) -> str:
    """Get gender-appropriate Arabic text for a niche."""
    gender = get_gender_for_niche(niche)
    return GENDER_TEXTS.get(gender, GENDER_TEXTS["plural"]).get(text_key, "")


# Niche color palettes (dark backgrounds, bold colors)
NICHE_COLORS = {
    "restaurants": {"bg": "#1A0F0A", "bg2": "#2D1810", "accent": "#FF6B35", "accent2": "#FFD700"},
    "cafes": {"bg": "#1A1410", "bg2": "#2D231C", "accent": "#C8A97E", "accent2": "#8B5E3C"},
    "bakeries": {"bg": "#1F1208", "bg2": "#2D1A0E", "accent": "#E8A87C", "accent2": "#C38D5C"},
    "salons": {"bg": "#1A0A1A", "bg2": "#2D102D", "accent": "#E056A0", "accent2": "#D4AF37"},
    "spas": {"bg": "#0A1A18", "bg2": "#102D2A", "accent": "#5CB8A8", "accent2": "#A8D5BA"},
    "barbershops": {"bg": "#0F0F0F", "bg2": "#1A1A1A", "accent": "#C9A25A", "accent2": "#FFFFFF"},
    "gyms": {"bg": "#0A0A0F", "bg2": "#15151F", "accent": "#FF4444", "accent2": "#FFD700"},
    "clinics": {"bg": "#0A1518", "bg2": "#102028", "accent": "#2E86AB", "accent2": "#A8D5BA"},
    "dentists": {"bg": "#0A1518", "bg2": "#102028", "accent": "#2E86AB", "accent2": "#5BC0DE"},
    "pharmacies": {"bg": "#0A1218", "bg2": "#101E28", "accent": "#2E86AB", "accent2": "#5BC0DE"},
    "dermatology": {"bg": "#1A0A14", "bg2": "#2D101E", "accent": "#E056A0", "accent2": "#FFC0CB"},
    "fashion": {"bg": "#0F0A0F", "bg2": "#1A0F1A", "accent": "#D4AF37", "accent2": "#E8C5C5"},
    "perfumes": {"bg": "#100A14", "bg2": "#1A1024", "accent": "#D4AF37", "accent2": "#9B59B6"},
    "law_firms": {"bg": "#0A0F1A", "bg2": "#10182D", "accent": "#C9A25A", "accent2": "#2E4057"},
    "real_estate": {"bg": "#0A1210", "bg2": "#101E1A", "accent": "#2ECC71", "accent2": "#C9A25A"},
    "auto_shops": {"bg": "#0F0F0A", "bg2": "#1A1A10", "accent": "#FF8C00", "accent2": "#888888"},
    "car_wash": {"bg": "#0A1015", "bg2": "#101820", "accent": "#00BFFF", "accent2": "#5BC0DE"},
    "cleaning": {"bg": "#0A1510", "bg2": "#101E18", "accent": "#2ECC71", "accent2": "#A8D5BA"},
    "hvac_ac": {"bg": "#0A1015", "bg2": "#101820", "accent": "#00BFFF", "accent2": "#2E86AB"},
    "event_halls": {"bg": "#100A14", "bg2": "#1A1024", "accent": "#D4AF37", "accent2": "#E056A0"},
    "training_centers": {"bg": "#0A0F15", "bg2": "#10182A", "accent": "#2E86AB", "accent2": "#FFD700"},
}
