#!/usr/bin/env python3
"""
Nuhoot Reels Generator — Phase 4
================================
Converts static PNG designs into animated Instagram Reels (1080×1920) using FFmpeg.

Features:
- Ken Burns zoom effect (slow zoom in on the design)
- Blurred background from the design itself
- Text overlays (business name, CTA)
- Nuhoot branding
- 8-second duration, 25fps, H.264
- Arabic text support via libfreetype + libfribidi

Usage:
  python3 reels_generator.py                    # Generate all 21 reels
  python3 reels_generator.py restaurants salons # Specific niches
"""

import json, os, sys, subprocess

# ─── Config ───────────────────────────────────────────────
RENDER_DIR = "/tmp/nuhoot-eagle-eye-v3"
OUTPUT_DIR = "/tmp/nuhoot-reels"
FONTS_DIR = "/opt/nuhoot/remotion/public/fonts"
DURATION = 8  # seconds
FPS = 25
WIDTH = 1080
HEIGHT = 1920
DESIGN_SIZE = 1080

# Font paths (Arabic-capable)
FONT_KUFI = f"{FONTS_DIR}/NotoKufiArabic-Bold.ttf"
FONT_SANS = f"{FONTS_DIR}/NotoSansArabic-Bold.ttf"
FONT_LATO = f"{FONTS_DIR}/Lato-Bold.ttf"

# Business names (same as pipeline)
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

# CTAs per niche
NICHE_CTAS = {
    "restaurants": "احجزوا طاولتكم الآن",
    "cafes": "زورونا اليوم",
    "bakeries": "اطلبوا الحلويات",
    "salons": "احجزي موعدك الآن",
    "spas": "احجزي جلسة استرخاء",
    "barbershops": "احجز موعدك الآن",
    "gyms": "اشترك اليوم",
    "clinics": "احجز موعدك الطبي",
    "dentists": "احجز موعدك الآن",
    "pharmacies": "زرنا اليوم",
    "dermatology": "احجزي استشارتك",
    "fashion": "تسوقي الآن",
    "perfumes": "اكتشف مجموعتنا",
    "law_firms": "استشرنا اليوم",
    "real_estate": "تصفح العقارات",
    "auto_shops": "احجز موعد صيانة",
    "car_wash": "اغسل سيارتك اليوم",
    "cleaning": "احجز خدمة التنظيف",
    "hvac_ac": "اطلب الصيانة الآن",
    "event_halls": "احجز قاعتك",
    "training_centers": "سجل الآن",
}


def escape_text(text):
    """Escape text for FFmpeg drawtext filter."""
    return text.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")


def generate_reel(niche):
    """Generate an Instagram Reel from a niche's PNG design."""
    input_png = f"{RENDER_DIR}/{niche}_best.png"
    if not os.path.exists(input_png):
        print(f"  ❌ Design not found: {input_png}")
        return False

    output_mp4 = f"{OUTPUT_DIR}/{niche}_reel.mp4"
    business_name = BUSINESS_NAMES.get(niche, niche)
    cta = NICHE_CTAS.get(niche, "زورونا")

    # Check font files
    font_kufi = FONT_KUFI if os.path.exists(FONT_KUFI) else None
    font_sans = FONT_SANS if os.path.exists(FONT_SANS) else None

    # Build the FFmpeg filter chain:
    # 1. Scale design to 1080x1080
    # 2. Apply Ken Burns zoom (slow zoom in over 8 seconds)
    # 3. Create blurred background from design (scaled to 1080x1920, blurred)
    # 4. Overlay design centered on background
    # 5. Add text overlays

    total_frames = DURATION * FPS  # 200 frames

    # Ken Burns: slow zoom from 1.0 to 1.15
    # zoompan with z='1+0.15*on/duration_frames'
    zoom_expr = f"z='1+0.15*on/{total_frames}'"

    filter_parts = []

    # Input 0: design PNG — apply zoom
    filter_parts.append(
        f"[0:v]scale={DESIGN_SIZE}:{DESIGN_SIZE},"
        f"zoompan={zoom_expr}:d={total_frames}:s={DESIGN_SIZE}x{DESIGN_SIZE}:fps={FPS}[zoomed]"
    )

    # Create blurred background from the same image
    filter_parts.append(
        f"[0:v]scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
        f"crop={WIDTH}:{HEIGHT},"
        f"boxblur=40:10,"
        f"format=yuv420p[bg]"
    )

    # Overlay zoomed design on blurred background
    # Center the 1080x1080 design on the 1080x1920 canvas
    overlay_y = (HEIGHT - DESIGN_SIZE) // 2  # 420px from top
    filter_parts.append(
        f"[bg][zoomed]overlay=0:{overlay_y}[with_design]"
    )

    # Add text overlays
    current_label = "with_design"

    # Top text: Business name (Arabic)
    if font_kufi:
        escaped_name = escape_text(business_name)
        filter_parts.append(
            f"[{current_label}]drawtext=fontfile='{font_kufi}':"
            f"text='{escaped_name}':"
            f"fontsize=42:fontcolor=white:"
            f"x=(w-text_w)/2:y=80:"
            f"shadowcolor=black@0.6:shadowx=2:shadowy=2:"
            f"enable='between(t,0.5,{DURATION})'"
            f"[t1]"
        )
        current_label = "t1"

    # Bottom text: CTA (Arabic)
    if font_sans:
        escaped_cta = escape_text(cta)
        filter_parts.append(
            f"[{current_label}]drawtext=fontfile='{font_sans}':"
            f"text='{escaped_cta}':"
            f"fontsize=36:fontcolor=#D4AF37:"
            f"x=(w-text_w)/2:y={HEIGHT-120}:"
            f"shadowcolor=black@0.6:shadowx=2:shadowy=2:"
            f"enable='between(t,1.5,{DURATION})'"
            f"[t2]"
        )
        current_label = "t2"

    # Branding: nuhoot.xyz at bottom
    filter_parts.append(
        f"[{current_label}]drawtext=fontfile='{font_sans or font_kufi}':"
        f"text='nuhoot.xyz':"
        f"fontsize=24:fontcolor=white@0.7:"
        f"x=(w-text_w)/2:y={HEIGHT-60}:"
        f"enable='between(t,2,{DURATION})'"
        f"[final]"
    )

    # Build the full filter
    filter_complex = ";".join(filter_parts)

    cmd = [
        "ffmpeg", "-y",
        "-i", input_png,
        "-filter_complex", filter_complex,
        "-map", "[final]",
        "-t", str(DURATION),
        "-r", str(FPS),
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        output_mp4
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    if os.path.exists(output_mp4) and os.path.getsize(output_mp4) > 10000:
        size_kb = os.path.getsize(output_mp4) // 1024
        print(f"  ✅ {niche}: {size_kb}KB → {output_mp4}")
        return True
    else:
        print(f"  ❌ {niche}: Generation failed")
        if result.stderr:
            # Show last few lines of error
            lines = result.stderr.strip().split('\n')
            for line in lines[-5:]:
                print(f"     {line}")
        return False


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    niches = sys.argv[1:] if len(sys.argv) > 1 else list(BUSINESS_NAMES.keys())

    print(f"\n{'='*60}")
    print(f"  NUHOOT REELS GENERATOR — Phase 4")
    print(f"  Generating {len(niches)} reels...")
    print(f"{'='*60}\n")

    success = 0
    failed = 0

    for niche in niches:
        print(f"  [{niches.index(niche)+1}/{len(niches)}] {niche}...")
        if generate_reel(niche):
            success += 1
        else:
            failed += 1

    print(f"\n{'='*60}")
    print(f"  DONE: {success} succeeded, {failed} failed")
    print(f"  Output: {OUTPUT_DIR}/")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
