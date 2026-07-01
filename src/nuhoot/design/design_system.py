"""
Design System — Fixed archetypes with proven composition rules.
Based on Claude's architecture: design system → composition engine → render → quality gate.

Each archetype defines:
- composition: layout rule (how elements are arranged)
- hierarchy: visual element ordering (what the eye sees first)
- color_mood: color palette for the Saudi luxury market
- photo_treatment: how the business photo is processed
- positions: golden-ratio-based element positions
- spacing: 8px-based spacing system
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import hashlib


@dataclass
class ColorPalette:
    """Color palette for a design archetype."""
    bg_primary: str
    bg_secondary: str
    accent_gold: str
    accent_gold_light: str
    accent_gold_dark: str
    text_primary: str
    text_secondary: str
    text_muted: str
    photo_overlay: str


@dataclass
class Archetype:
    """A proven design template with fixed composition rules."""
    name: str
    composition: str  # layout rule
    hierarchy: List[str]  # visual element ordering
    color_mood: str
    photo_treatment: str  # how to process the business photo
    photo_position: str  # where the photo goes
    photo_size: Tuple[float, float]  # (width_pct, height_pct) of canvas
    text_position: str  # where the text block goes
    text_align: str  # text alignment
    spacing_system: int  # base unit (8px)
    golden_ratio: float  # 1.618 for positioning
    palette: ColorPalette
    bg_style: str  # background generation style for Cairo
    bg_colors: List[Tuple[float, float, float]]  # RGB 0-1 for Cairo


# ═══ COLOR PALETTES (Saudi Luxury Market) ═══

WARM_GOLD = ColorPalette(
    bg_primary="#0a0503",
    bg_secondary="#1a0f05",
    accent_gold="#D4AF37",
    accent_gold_light="#FFF5E1",
    accent_gold_dark="#B8860B",
    text_primary="#FFFFFF",
    text_secondary="rgba(245,240,232,0.85)",
    text_muted="rgba(155,147,136,0.6)",
    photo_overlay="rgba(10,5,3,0.5)",
)

COOL_PLATINUM = ColorPalette(
    bg_primary="#080a12",
    bg_secondary="#121828",
    accent_gold="#E8E8E8",
    accent_gold_light="#FFFFFF",
    accent_gold_dark="#A0A0B0",
    text_primary="#F8F8FF",
    text_secondary="rgba(230,230,240,0.85)",
    text_muted="rgba(150,150,170,0.6)",
    photo_overlay="rgba(8,10,18,0.5)",
)

MONOCHROME_GOLD = ColorPalette(
    bg_primary="#050505",
    bg_secondary="#0a0a0a",
    accent_gold="#D4AF37",
    accent_gold_light="#FFE8A3",
    accent_gold_dark="#8B6914",
    text_primary="#FFFFFF",
    text_secondary="rgba(240,240,240,0.8)",
    text_muted="rgba(120,120,120,0.5)",
    photo_overlay="rgba(5,5,5,0.5)",
)


# ═══ ARCHETYPES ═══

ARCHETYPES: Dict[str, Archetype] = {
    "hero_statement": Archetype(
        name="Hero Statement",
        composition="center_dominant",
        hierarchy=["hero_text", "business_photo", "accent_text", "cta"],
        color_mood="warm_gold_luxury",
        photo_treatment="cinematic_crop",
        photo_position="center_top",
        photo_size=(0.85, 0.35),  # 85% width, 35% height
        text_position="center_bottom",
        text_align="center",
        spacing_system=8,
        golden_ratio=1.618,
        palette=WARM_GOLD,
        bg_style="warm_gold_luxury",
        bg_colors=[
            (0.02, 0.01, 0.0),    # Deep black-brown
            (0.1, 0.06, 0.02),    # Dark warm brown
            (0.05, 0.03, 0.01),   # Mid dark
            (0.0, 0.0, 0.0),      # Pure black
        ],
    ),
    "split_luxury": Archetype(
        name="Split Luxury",
        composition="horizontal_split",
        hierarchy=["business_photo", "hero_text", "supporting_text"],
        color_mood="cool_platinum",
        photo_treatment="architectural_frame",
        photo_position="top_half",
        photo_size=(1.0, 0.50),  # Full width, 50% height
        text_position="bottom_half",
        text_align="right",
        spacing_system=8,
        golden_ratio=1.618,
        palette=COOL_PLATINUM,
        bg_style="cool_platinum",
        bg_colors=[
            (0.03, 0.04, 0.07),   # Dark blue-black
            (0.07, 0.09, 0.15),   # Dark navy
            (0.04, 0.05, 0.08),   # Mid dark blue
            (0.01, 0.01, 0.02),   # Near black
        ],
    ),
    "minimal_power": Archetype(
        name="Minimal Power",
        composition="asymmetric_grid",
        hierarchy=["hero_text", "minimal_photo", "accent_line"],
        color_mood="monochrome_gold_accent",
        photo_treatment="geometric_mask",
        photo_position="circle_center",
        photo_size=(0.26, 0.26),  # 26% width/height (circular)
        text_position="below_photo",
        text_align="center",
        spacing_system=8,
        golden_ratio=1.618,
        palette=MONOCHROME_GOLD,
        bg_style="monochrome_gold",
        bg_colors=[
            (0.01, 0.01, 0.01),   # Near pure black
            (0.03, 0.03, 0.03),   # Very dark gray
            (0.02, 0.02, 0.02),   # Mid dark
            (0.0, 0.0, 0.0),      # Pure black
        ],
    ),
}


def select_archetype(business_type: str = "restaurant") -> str:
    """Select the best archetype for a business type."""
    mapping = {
        "restaurant": "split_luxury",
        "cafe": "hero_statement",
        "salon": "hero_statement",
        "gym": "minimal_power",
        "retail": "split_luxury",
        "default": "split_luxury",
    }
    return mapping.get(business_type, mapping["default"])


def get_seed(business_name: str, content: str) -> int:
    """Generate a deterministic seed from business data."""
    combined = f"{business_name}:{content}"
    return int(hashlib.md5(combined.encode()).hexdigest()[:8], 16)


def golden_ratio_position(canvas_size: int, index: int = 0) -> int:
    """Calculate position using golden ratio (0.618 = 1/1.618)."""
    return int(canvas_size * (0.618 ** (index + 1)))
