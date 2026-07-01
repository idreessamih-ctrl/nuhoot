"""
Saudi SME Social Media Templates - Complete Template Library
5 Professional 1080x1080 Templates with Full Space-Filling Design

Each template is a function that takes:
- photo_b64: Base64 encoded photo string
- data: Dict with business info (name, headline, taglines, rating, reviews, etc.)
- colors: Dict with niche-specific colors

Author: Senior Saudi Marketing Agency Creative Director
"""

from typing import Dict, Optional, List


def get_base_styles() -> str:
    """Common styles shared across all templates"""
    return """
        @import url('https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;500;600;700;800;900&family=Noto+Sans+Arabic:wght@400;500;600;700;800&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        .container {
            width: 1080px;
            height: 1080px;
            position: relative;
            overflow: hidden;
            font-family: 'Noto Kufi Arabic', 'Noto Sans Arabic', sans-serif;
            direction: rtl;
        }
        
        /* Utility Classes */
        .absolute { position: absolute; }
        .relative { position: relative; }
        .flex { display: flex; }
        .flex-col { flex-direction: column; }
        .items-center { align-items: center; }
        .justify-center { justify-content: center; }
        .justify-between { justify-content: space-between; }
        .gap-1 { gap: 8px; }
        .gap-2 { gap: 16px; }
        .text-center { text-align: center; }
        .text-right { text-align: right; }
        
        /* Animation Keyframes */
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 0.6; }
            50% { opacity: 1; }
        }
        
        @keyframes shimmer {
            0% { background-position: -200% center; }
            100% { background-position: 200% center; }
        }
    """


def get_islamic_pattern_svg(color: str = "rgba(255,255,255,0.1)") -> str:
    """Generate Islamic geometric pattern as inline SVG"""
    return f'''<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <pattern id="islamicPattern" x="0" y="0" width="50" height="50" patternUnits="userSpaceOnUse">
                <path d="M25 0 L50 25 L25 50 L0 25 Z" fill="none" stroke="{color}" stroke-width="1"/>
                <circle cx="25" cy="25" r="8" fill="none" stroke="{color}" stroke-width="1"/>
                <path d="M25 17 L25 33 M17 25 L33 25" stroke="{color}" stroke-width="1"/>
                <circle cx="0" cy="0" r="4" fill="{color}"/>
                <circle cx="50" cy="0" r="4" fill="{color}"/>
                <circle cx="0" cy="50" r="4" fill="{color}"/>
                <circle cx="50" cy="50" r="4" fill="{color}"/>
            </pattern>
        </defs>
        <rect width="100" height="100" fill="url(#islamicPattern)"/>
    </svg>'''


# =============================================================================
# TEMPLATE 1: MAGAZINE LAYOUT
# =============================================================================

def template_magazine(photo_b64: str, data: Dict, colors: Dict) -> str:
    """
    MAGAZINE TEMPLATE
    
    Concept: Multi-zone editorial layout inspired by premium Saudi lifestyle magazines.
    Features a dominant photo area with sophisticated side panels, info blocks, and
    layered design elements. Every zone is filled with purposeful content - no dead space.
    
    Space-Filling Elements Used:
    1. Side Panel (right) - 280px with gradient, icons, hours
    2. Icon Cluster - 6 feature icons in grid
    3. Hours Card - Operating hours with Islamic pattern
    4. Contact Strip - Bottom bar with phone/location
    5. Corner Ornaments - Decorative Arabic geometric shapes
    6. Background Blobs - Soft gradient orbs
    7. Wave Divider - Separating photo from content
    8. Trust Badges - Certification/quality marks
    9. Pattern Overlay - Subtle Islamic geometry on side panel
    10. Decorative Diamonds - Scattered accent shapes
    
    Dark/Light Adaptation:
    - Dark niches: Light text, glowing accents, darker overlays
    - Light niches: Dark text, subtle shadows, lighter overlays
    """
    
    # Extract data with defaults
    business_name = data.get('business_name', 'اسم النشاط التجاري')
    headline = data.get('headline', 'عنوان رئيسي جذاب')
    kicker = data.get('kicker', 'عرض حصري')
    taglines = data.get('taglines', ['جودة عالية', 'خدمة متميزة', 'أسعار منافسة'])
    rating = data.get('rating', 4.8)
    reviews = data.get('reviews', 127)
    domain = data.get('domain', 'example.sa')
    hours = data.get('hours', '٩ص - ١١م')
    phone = data.get('phone', '٠٥٠٠٠٠٠٠٠٠')
    features = data.get('features', ['واي فاي', 'مواقف', 'توصيل', 'دفع إلكتروني', 'حجز مسبق', 'عروض'])
    
    # Colors
    bg_grad = colors.get('bg_grad', 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)')
    accent = colors.get('accent', '#e94560')
    accent_light = colors.get('accent_light', '#ff6b6b')
    text_color = colors.get('text', '#ffffff')
    pill_bg = colors.get('pill_bg', 'rgba(255,255,255,0.15)')
    pill_text = colors.get('pill_text', '#ffffff')
    is_dark = colors.get('is_dark', True)
    
    # Generate star rating HTML
    full_stars = int(rating)
    has_half = rating - full_stars >= 0.5
    stars_html = ''.join(['<span class="star full">★</span>' for _ in range(full_stars)])
    if has_half:
        stars_html += '<span class="star half">★</span>'
    stars_html += ''.join(['<span class="star empty">☆</span>' for _ in range(5 - full_stars - (1 if has_half else 0))])
    
    # Feature icons mapping
    feature_icons = {
        'واي فاي': '📶', 'مواقف': '🅿️', 'توصيل': '🚗', 'دفع إلكتروني': '💳',
        'حجز مسبق': '📅', 'عروض': '🏷️', 'أطفال': '👶', 'عائلات': '👨‍👩‍👧',
        'vip': '👑', 'قهوة': '☕', 'حلويات': '🍰', 'صحي': '🥗'
    }
    
    html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1080, height=1080">
    <title>{business_name}</title>
    <style>
        {get_base_styles()}
        
        :root {{
            --bg-grad: {bg_grad};
            --accent: {accent};
            --accent-light: {accent_light};
            --text: {text_color};
            --pill-bg: {pill_bg};
            --pill-text: {pill_text};
            --shadow-3d: 
                1px 1px 0 {accent},
                2px 2px 0 {accent},
                3px 3px 0 rgba(0,0,0,0.3),
                4px 4px 0 rgba(0,0,0,0.2),
                5px 5px 15px rgba(0,0,0,0.4);
        }}
        
        .magazine-container {{
            width: 1080px;
            height: 1080px;
            background: var(--bg-grad);
            position: relative;
            overflow: hidden;
            display: grid;
            grid-template-columns: 1fr 280px;
            grid-template-rows: 1fr;
        }}
        
        /* Background Blobs */
        .blob {{
            position: absolute;
            border-radius: 50%;
            filter: blur(60px);
            opacity: 0.4;
            z-index: 1;
        }}
        .blob-1 {{
            width: 400px;
            height: 400px;
            background: var(--accent);
            top: -100px;
            right: -100px;
        }}
        .blob-2 {{
            width: 300px;
            height: 300px;
            background: var(--accent-light);
            bottom: 100px;
            left: -50px;
        }}
        .blob-3 {{
            width: 200px;
            height: 200px;
            background: var(--accent);
            bottom: -50px;
            right: 200px;
            opacity: 0.3;
        }}
        
        /* Main Photo Area */
        .photo-zone {{
            position: relative;
            z-index: 2;
            padding: 30px;
            display: flex;
            flex-direction: column;
        }}
        
        .photo-wrapper {{
            flex: 1;
            position: relative;
            border-radius: 24px;
            overflow: hidden;
            box-shadow: 
                0 20px 60px rgba(0,0,0,0.4),
                inset 0 0 0 3px rgba(255,255,255,0.1);
        }}
        
        .main-photo {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        
        .photo-overlay {{
            position: absolute;
            inset: 0;
            background: linear-gradient(
                to top,
                rgba(0,0,0,0.8) 0%,
                rgba(0,0,0,0.4) 30%,
                transparent 60%
            );
        }}
        
        /* Kicker Label */
        .kicker {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: var(--accent);
            color: white;
            padding: 10px 24px;
            border-radius: 30px;
            font-size: 18px;
            font-weight: 700;
            letter-spacing: 1px;
            box-shadow: 0 8px 25px rgba(233,69,96,0.4);
            z-index: 10;
            animation: pulse 2s ease-in-out infinite;
        }}
        
        /* Content Over Photo */
        .photo-content {{
            position: absolute;
            bottom: 0;
            right: 0;
            left: 0;
            padding: 40px;
            z-index: 5;
        }}
        
        /* Business Name Badge */
        .business-badge {{
            display: inline-flex;
            align-items: center;
            gap: 12px;
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            padding: 12px 24px;
            border-radius: 50px;
            margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.2);
        }}
        
        .business-badge .icon {{
            width: 36px;
            height: 36px;
            background: var(--accent);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        }}
        
        .business-badge .name {{
            font-size: 20px;
            font-weight: 700;
            color: white;
        }}
        
        /* 3D Headline */
        .headline-3d {{
            font-size: 52px;
            font-weight: 900;
            color: white;
            text-shadow: var(--shadow-3d);
            line-height: 1.2;
            margin-bottom: 24px;
            max-width: 90%;
        }}
        
        /* Tagline Pills */
        .tagline-pills {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 20px;
        }}
        
        .pill {{
            background: var(--pill-bg);
            color: var(--pill-text);
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 16px;
            font-weight: 600;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.3s, background 0.3s;
        }}
        
        .pill:hover {{
            transform: translateY(-3px);
            background: var(--accent);
        }}
        
        /* Rating Block */
        .rating-block {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}
        
        .stars {{
            display: flex;
            gap: 4px;
        }}
        
        .star {{
            font-size: 24px;
            color: #ffd700;
        }}
        
        .star.empty {{
            color: rgba(255,255,255,0.3);
        }}
        
        .rating-text {{
            font-size: 18px;
            color: rgba(255,255,255,0.9);
        }}
        
        .rating-number {{
            font-weight: 800;
            color: white;
            font-size: 22px;
        }}
        
        /* Side Panel */
        .side-panel {{
            background: linear-gradient(180deg, 
                rgba(255,255,255,0.08) 0%, 
                rgba(255,255,255,0.03) 100%);
            backdrop-filter: blur(20px);
            position: relative;
            z-index: 3;
            display: flex;
            flex-direction: column;
            padding: 30px 20px;
            border-right: 1px solid rgba(255,255,255,0.1);
        }}
        
        /* Pattern Overlay on Side Panel */
        .pattern-overlay {{
            position: absolute;
            inset: 0;
            opacity: 0.05;
            background-image: url("data:image/svg+xml,{get_islamic_pattern_svg().replace('"', "'").replace('#', '%23')}");
            background-size: 100px 100px;
            pointer-events: none;
        }}
        
        /* Icon Cluster */
        .icon-cluster {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            margin-bottom: 30px;
            position: relative;
            z-index: 2;
        }}
        
        .feature-icon {{
            background: rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 16px 12px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.05);
            transition: all 0.3s;
        }}
        
        .feature-icon:hover {{
            background: var(--accent);
            transform: translateY(-5px);
        }}
        
        .feature-icon .emoji {{
            font-size: 28px;
            display: block;
            margin-bottom: 8px;
        }}
        
        .feature-icon .label {{
            font-size: 12px;
            color: rgba(255,255,255,0.8);
            font-weight: 500;
        }}
        
        /* Hours Card */
        .hours-card {{
            background: linear-gradient(135deg, var(--accent), var(--accent-light));
            border-radius: 20px;
            padding: 24px 20px;
            margin-bottom: 20px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(233,69,96,0.3);
        }}
        
        .hours-card::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
        }}
        
        .hours-card .title {{
            font-size: 14px;
            color: rgba(255,255,255,0.8);
            margin-bottom: 8px;
            position: relative;
        }}
        
        .hours-card .time {{
            font-size: 28px;
            font-weight: 800;
            color: white;
            position: relative;
        }}
        
        .hours-card .icon {{
            position: absolute;
            top: 15px;
            left: 15px;
            font-size: 24px;
            opacity: 0.8;
        }}
        
        /* Trust Badge */
        .trust-badge {{
            background: rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        .trust-badge .shield {{
            font-size: 36px;
            margin-bottom: 10px;
        }}
        
        .trust-badge .text {{
            font-size: 13px;
            color: rgba(255,255,255,0.8);
            line-height: 1.5;
        }}
        
        /* Decorative Diamonds */
        .diamond {{
            position: absolute;
            width: 12px;
            height: 12px;
            background: var(--accent);
            transform: rotate(45deg);
            opacity: 0.6;
        }}
        
        .diamond-1 {{ top: 100px; left: 50px; }}
        .diamond-2 {{ top: 300px; left: 30px; animation: float 3s ease-in-out infinite; }}
        .diamond-3 {{ bottom: 200px; left: 60px; }}
        
        /* Corner Ornaments */
        .corner-ornament {{
            position: absolute;
            width: 80px;
            height: 80px;
            z-index: 10;
        }}
        
        .corner-ornament.top-left {{
            top: 0;
            left: 0;
            border-top: 4px solid var(--accent);
            border-left: 4px solid var(--accent);
            border-top-left-radius: 20px;
        }}
        
        .corner-ornament.bottom-right {{
            bottom: 80px;
            right: 290px;
            border-bottom: 4px solid var(--accent);
            border-right: 4px solid var(--accent);
            border-bottom-right-radius: 20px;
        }}
        
        /* Contact Strip */
        .contact-strip {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 70px;
            background: rgba(0,0,0,0.6);
            backdrop-filter: blur(10px);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 40px;
            z-index: 20;
            border-top: 1px solid rgba(255,255,255,0.1);
        }}
        
        .contact-item {{
            display: flex;
            align-items: center;
            gap: 12px;
            color: white;
        }}
        
        .contact-item .icon {{
            width: 40px;
            height: 40px;
            background: var(--accent);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        }}
        
        .contact-item .text {{
            font-size: 16px;
            font-weight: 600;
        }}
        
        .brand-footer {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .brand-footer .logo {{
            width: 36px;
            height: 36px;
            background: white;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            color: var(--accent);
            font-size: 18px;
        }}
        
        .brand-footer .domain {{
            color: rgba(255,255,255,0.8);
            font-size: 16px;
        }}
        
        /* Stats in side panel */
        .stats-mini {{
            display: flex;
            justify-content: space-around;
            margin-top: auto;
            padding-top: 20px;
            border-top: 1px solid rgba(255,255,255,0.1);
        }}
        
        .stat-item {{
            text-align: center;
        }}
        
        .stat-item .number {{
            font-size: 24px;
            font-weight: 800;
            color: var(--accent-light);
        }}
        
        .stat-item .label {{
            font-size: 11px;
            color: rgba(255,255,255,0.6);
        }}
    </style>
</head>
<body>
    <div class="magazine-container">
        <!-- Background Blobs -->
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <div class="blob blob-3"></div>
        
        <!-- Corner Ornaments -->
        <div class="corner-ornament top-left"></div>
        <div class="corner-ornament bottom-right"></div>
        
        <!-- Decorative Diamonds -->
        <div class="diamond diamond-1"></div>
        <div class="diamond diamond-2"></div>
        <div class="diamond diamond-3"></div>
        
        <!-- Main Photo Zone -->
        <div class="photo-zone">
            <div class="photo-wrapper">
                <img src="data:image/jpeg;base64,{photo_b64}" alt="{business_name}" class="main-photo">
                <div class="photo-overlay"></div>
                
                <!-- Kicker -->
                <div class="kicker">{kicker}</div>
                
                <!-- Content Over Photo -->
                <div class="photo-content">
                    <!-- Business Badge -->
                    <div class="business-badge">
                        <div class="icon">🏪</div>
                        <span class="name">{business_name}</span>
                    </div>
                    
                    <!-- 3D Headline -->
                    <h1 class="headline-3d">{headline}</h1>
                    
                    <!-- Tagline Pills -->
                    <div class="tagline-pills">
                        {''.join([f'<span class="pill">{tag}</span>' for tag in taglines[:3]])}
                    </div>
                    
                    <!-- Rating -->
                    <div class="rating-block">
                        <div class="stars">{stars_html}</div>
                        <span class="rating-text">
                            <span class="rating-number">{rating}</span> ({reviews} تقييم)
                        </span>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Side Panel -->
        <div class="side-panel">
            <div class="pattern-overlay"></div>
            
            <!-- Icon Cluster -->
            <div class="icon-cluster">
                {''.join([f'''
                <div class="feature-icon">
                    <span class="emoji">{feature_icons.get(feat, "✨")}</span>
                    <span class="label">{feat}</span>
                </div>
                ''' for feat in features[:6]])}
            </div>
            
            <!-- Hours Card -->
            <div class="hours-card">
                <span class="icon">🕐</span>
                <div class="title">ساعات العمل</div>
                <div class="time">{hours}</div>
            </div>
            
            <!-- Trust Badge -->
            <div class="trust-badge">
                <div class="shield">🛡️</div>
                <div class="text">موثق من وزارة التجارة<br>سجل تجاري معتمد</div>
            </div>
            
            <!-- Mini Stats -->
            <div class="stats-mini">
                <div class="stat-item">
                    <div class="number">+{reviews}</div>
                    <div class="label">عميل سعيد</div>
                </div>
                <div class="stat-item">
                    <div class="number">5</div>
                    <div class="label">سنوات خبرة</div>
                </div>
            </div>
        </div>
        
        <!-- Contact Strip -->
        <div class="contact-strip">
            <div class="contact-item">
                <div class="icon">📞</div>
                <span class="text">{phone}</span>
            </div>
            <div class="contact-item">
                <div class="icon">📍</div>
                <span class="text">الرياض، المملكة العربية السعودية</span>
            </div>
            <div class="brand-footer">
                <div class="logo">M</div>
                <span class="domain">{domain}</span>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    return html


# =============================================================================
# TEMPLATE 2: COLLAGE LAYOUT
# =============================================================================

def template_collage(photo_b64: str, data: Dict, colors: Dict, 
                     extra_photos: List[str] = None) -> str:
    """
    COLLAGE TEMPLATE
    
    Concept: Dynamic multi-photo grid layout perfect for showcasing variety - 
    ideal for restaurants (dishes), salons (styles), gyms (facilities), etc.
    Main hero photo with 3 supporting photos, all with overlaid badges and info.
    
    Space-Filling Elements Used:
    1. Multi-Photo Grid - 1 large + 3 small photos
    2. Price Burst - Rotating badge with offer price
    3. Spec Pills - Photo-specific labels on each image
    4. Geometric Shapes - Triangles and circles as accents
    5. Wave Divider - Organic shape between sections
    6. Certification Badges - Quality/halal/organic marks
    7. Glow Effects - Neon-style accent glows
    8. Stats Block - Numbers with icons
    9. Icon Strip - Feature icons in a row
    10. Gradient Mesh - Complex background gradient
    
    Dark/Light Adaptation:
    - Dark: Bright accent glows, light text, glass morphism
    - Light: Subtle shadows, dark text, soft overlays
    """
    
    business_name = data.get('business_name', 'اسم النشاط التجاري')
    headline = data.get('headline', 'عنوان رئيسي جذاب')
    kicker = data.get('kicker', 'عرض حصري')
    taglines = data.get('taglines', ['جودة عالية', 'خدمة متميزة', 'أسعار منافسة'])
    rating = data.get('rating', 4.8)
    reviews = data.get('reviews', 127)
    domain = data.get('domain', 'example.sa')
    price = data.get('price', '٩٩')
    specs = data.get('specs', ['طازج', 'عضوي', 'محلي', 'حلال'])
    
    bg_grad = colors.get('bg_grad', 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)')
    accent = colors.get('accent', '#ff6b6b')
    accent_light = colors.get('accent_light', '#feca57')
    text_color = colors.get('text', '#ffffff')
    pill_bg = colors.get('pill_bg', 'rgba(255,255,255,0.2)')
    pill_text = colors.get('pill_text', '#ffffff')
    
    # Use main photo for all if no extras provided
    photos = [photo_b64] + (extra_photos or [photo_b64, photo_b64, photo_b64])[:3]
    
    # Star rating
    full_stars = int(rating)
    stars_html = ''.join(['<span class="star">★</span>' for _ in range(full_stars)])
    stars_html += ''.join(['<span class="star empty">☆</span>' for _ in range(5 - full_stars)])
    
    html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1080, height=1080">
    <title>{business_name}</title>
    <style>
        {get_base_styles()}
        
        :root {{
            --bg-grad: {bg_grad};
            --accent: {accent};
            --accent-light: {accent_light};
            --text: {text_color};
            --pill-bg: {pill_bg};
            --pill-text: {pill_text};
            --glow: 0 0 40px {accent}80;
        }}
        
        .collage-container {{
            width: 1080px;
            height: 1080px;
            background: var(--bg-grad);
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }}
        
        /* Gradient Mesh Background */
        .gradient-mesh {{
            position: absolute;
            inset: 0;
            background: 
                radial-gradient(ellipse at 20% 20%, {accent}40 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, {accent_light}30 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(255,255,255,0.1) 0%, transparent 70%);
            z-index: 1;
        }}
        
        /* Geometric Shapes */
        .geo-shape {{
            position: absolute;
            z-index: 2;
            opacity: 0.6;
        }}
        
        .triangle {{
            width: 0;
            height: 0;
            border-left: 40px solid transparent;
            border-right: 40px solid transparent;
            border-bottom: 70px solid var(--accent);
        }}
        
        .triangle-1 {{ top: 50px; left: 50px; transform: rotate(15deg); }}
        .triangle-2 {{ bottom: 150px; right: 100px; transform: rotate(-30deg); opacity: 0.4; }}
        
        .circle-shape {{
            border-radius: 50%;
            border: 3px solid var(--accent-light);
        }}
        
        .circle-1 {{ width: 100px; height: 100px; top: 200px; right: 30px; }}
        .circle-2 {{ width: 60px; height: 60px; bottom: 300px; left: 40px; }}
        
        /* Header Section */
        .header-section {{
            padding: 30px 40px 20px;
            position: relative;
            z-index: 10;
        }}
        
        .header-top {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 20px;
        }}
        
        /* Business Badge */
        .business-badge {{
            display: flex;
            align-items: center;
            gap: 15px;
            background: rgba(0,0,0,0.3);
            backdrop-filter: blur(15px);
            padding: 15px 25px;
            border-radius: 60px;
            border: 1px solid rgba(255,255,255,0.2);
        }}
        
        .business-badge .avatar {{
            width: 50px;
            height: 50px;
            background: var(--accent);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            box-shadow: var(--glow);
        }}
        
        .business-badge .info {{
            text-align: right;
        }}
        
        .business-badge .name {{
            font-size: 22px;
            font-weight: 800;
            color: white;
        }}
        
        .business-badge .rating {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 4px;
        }}
        
        .business-badge .stars {{
            color: #ffd700;
            font-size: 14px;
        }}
        
        .business-badge .rating-text {{
            font-size: 13px;
            color: rgba(255,255,255,0.8);
        }}
        
        /* Kicker */
        .kicker {{
            background: var(--accent);
            color: white;
            padding: 12px 28px;
            border-radius: 30px;
            font-size: 18px;
            font-weight: 700;
            box-shadow: var(--glow);
            animation: pulse 2s ease-in-out infinite;
        }}
        
        /* 3D Headline */
        .headline-3d {{
            font-size: 56px;
            font-weight: 900;
            color: white;
            text-shadow: 
                2px 2px 0 var(--accent),
                4px 4px 0 rgba(0,0,0,0.3),
                6px 6px 20px rgba(0,0,0,0.4);
            line-height: 1.1;
            margin-bottom: 15px;
        }}
        
        /* Tagline Pills */
        .tagline-pills {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }}
        
        .pill {{
            background: var(--pill-bg);
            color: var(--pill-text);
            padding: 10px 22px;
            border-radius: 25px;
            font-size: 16px;
            font-weight: 600;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.15);
        }}
        
        /* Photo Grid */
        .photo-grid {{
            flex: 1;
            display: grid;
            grid-template-columns: 1.5fr 1fr;
            grid-template-rows: 1fr 1fr;
            gap: 15px;
            padding: 0 40px;
            position: relative;
            z-index: 10;
        }}
        
        .photo-card {{
            position: relative;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }}
        
        .photo-card.main {{
            grid-row: span 2;
        }}
        
        .photo-card img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        
        .photo-card .overlay {{
            position: absolute;
            inset: 0;
            background: linear-gradient(to top, rgba(0,0,0,0.6) 0%, transparent 50%);
        }}
        
        /* Spec Pills on Photos */
        .spec-pill {{
            position: absolute;
            bottom: 15px;
            right: 15px;
            background: rgba(255,255,255,0.95);
            color: #333;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 700;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        
        /* Price Burst */
        .price-burst {{
            position: absolute;
            top: 20px;
            left: 20px;
            width: 100px;
            height: 100px;
            background: var(--accent);
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-shadow: var(--glow);
            animation: float 3s ease-in-out infinite;
            z-index: 20;
        }}
        
        .price-burst::before {{
            content: '';
            position: absolute;
            inset: -5px;
            border: 3px dashed rgba(255,255,255,0.5);
            border-radius: 50%;
            animation: spin 10s linear infinite;
        }}
        
        @keyframes spin {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}
        
        .price-burst .label {{
            font-size: 12px;
            color: rgba(255,255,255,0.9);
        }}
        
        .price-burst .price {{
            font-size: 32px;
            font-weight: 900;
            color: white;
        }}
        
        .price-burst .currency {{
            font-size: 12px;
            color: rgba(255,255,255,0.9);
        }}
        
        /* Certification Badges */
        .cert-badges {{
            position: absolute;
            top: 15px;
            right: 15px;
            display: flex;
            gap: 8px;
            z-index: 15;
        }}
        
        .cert-badge {{
            width: 45px;
            height: 45px;
            background: rgba(255,255,255,0.95);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        
        /* Wave Divider */
        .wave-divider {{
            height: 60px;
            position: relative;
            z-index: 5;
            margin-top: -30px;
        }}
        
        .wave-divider svg {{
            width: 100%;
            height: 100%;
        }}
        
        /* Footer Section */
        .footer-section {{
            padding: 20px 40px 30px;
            position: relative;
            z-index: 10;
        }}
        
        /* Stats Block */
        .stats-block {{
            display: flex;
            justify-content: space-around;
            background: rgba(0,0,0,0.3);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        .stat {{
            text-align: center;
        }}
        
        .stat .icon {{
            font-size: 28px;
            margin-bottom: 8px;
        }}
        
        .stat .number {{
            font-size: 28px;
            font-weight: 900;
            color: var(--accent-light);
        }}
        
        .stat .label {{
            font-size: 13px;
            color: rgba(255,255,255,0.7);
        }}
        
        /* Trust Badge */
        .trust-badge {{
            position: absolute;
            bottom: 100px;
            left: 40px;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 12px 20px;
            border-radius: 30px;
            display: flex;
            align-items: center;
            gap: 10px;
            border: 1px solid rgba(255,255,255,0.2);
        }}
        
        .trust-badge .shield {{
            font-size: 24px;
        }}
        
        .trust-badge .text {{
            font-size: 14px;
            color: white;
        }}
        
        /* Icon Strip */
        .icon-strip {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 15px;
        }}
        
        .icon-item {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 6px;
        }}
        
        .icon-item .icon {{
            width: 50px;
            height: 50px;
            background: rgba(255,255,255,0.15);
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }}
        
        .icon-item .label {{
            font-size: 12px;
            color: rgba(255,255,255,0.8);
        }}
        
        /* Brand Footer */
        .brand-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 15px;
            border-top: 1px solid rgba(255,255,255,0.1);
        }}
        
        .brand-footer .logo-group {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .brand-footer .logo {{
            width: 40px;
            height: 40px;
            background: white;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            color: var(--accent);
            font-size: 20px;
        }}
        
        .brand-footer .domain {{
            color: rgba(255,255,255,0.8);
            font-size: 18px;
        }}
        
        .brand-footer .cta {{
            background: white;
            color: #333;
            padding: 12px 30px;
            border-radius: 30px;
            font-size: 16px;
            font-weight: 700;
        }}
        
        /* Glow Effects */
        .glow-orb {{
            position: absolute;
            border-radius: 50%;
            filter: blur(40px);
            z-index: 1;
        }}
        
        .glow-1 {{
            width: 200px;
            height: 200px;
            background: var(--accent);
            top: 100px;
            right: -50px;
            opacity: 0.5;
        }}
        
        .glow-2 {{
            width: 150px;
            height: 150px;
            background: var(--accent-light);
            bottom: 200px;
            left: -30px;
            opacity: 0.4;
        }}
    </style>
</head>
<body>
    <div class="collage-container">
        <!-- Background Effects -->
        <div class="gradient-mesh"></div>
        <div class="glow-orb glow-1"></div>
        <div class="glow-orb glow-2"></div>
        
        <!-- Geometric Shapes -->
        <div class="geo-shape triangle triangle-1"></div>
        <div class="geo-shape triangle triangle-2"></div>
        <div class="geo-shape circle-shape circle-1"></div>
        <div class="geo-shape circle-shape circle-2"></div>
        
        <!-- Header -->
        <div class="header-section">
            <div class="header-top">
                <div class="business-badge">
                    <div class="avatar">🏪</div>
                    <div class="info">
                        <div class="name">{business_name}</div>
                        <div class="rating">
                            <span class="stars">{stars_html}</span>
                            <span class="rating-text">{rating} ({reviews})</span>
                        </div>
                    </div>
                </div>
                <div class="kicker">{kicker}</div>
            </div>
            
            <h1 class="headline-3d">{headline}</h1>
            
            <div class="tagline-pills">
                {''.join([f'<span class="pill">{tag}</span>' for tag in taglines[:3]])}
            </div>
        </div>
        
        <!-- Photo Grid -->
        <div class="photo-grid">
            <!-- Main Photo -->
            <div class="photo-card main">
                <img src="data:image/jpeg;base64,{photos[0]}" alt="Main">
                <div class="overlay"></div>
                <div class="cert-badges">
                    <div class="cert-badge">✓</div>
                    <div class="cert-badge">🏆</div>
                </div>
                <div class="spec-pill">{specs[0] if specs else 'مميز'}</div>
                
                <!-- Price Burst -->
                <div class="price-burst">
                    <span class="label">يبدأ من</span>
                    <span class="price">{price}</span>
                    <span class="currency">ريال</span>
                </div>
            </div>
            
            <!-- Secondary Photos -->
            <div class="photo-card">
                <img src="data:image/jpeg;base64,{photos[1]}" alt="Photo 2">
                <div class="overlay"></div>
                <div class="spec-pill">{specs[1] if len(specs) > 1 else 'طازج'}</div>
            </div>
            
            <div class="photo-card">
                <img src="data:image/jpeg;base64,{photos[2]}" alt="Photo 3">
                <div class="overlay"></div>
                <div class="spec-pill">{specs[2] if len(specs) > 2 else 'جديد'}</div>
            </div>
        </div>
        
        <!-- Trust Badge -->
        <div class="trust-badge">
            <span class="shield">🛡️</span>
            <span class="text">جودة مضمونة ١٠٠٪</span>
        </div>
        
        <!-- Footer -->
        <div class="footer-section">
            <!-- Stats Block -->
            <div class="stats-block">
                <div class="stat">
                    <div class="icon">👥</div>
                    <div class="number">+{reviews}</div>
                    <div class="label">عميل سعيد</div>
                </div>
                <div class="stat">
                    <div class="icon">⭐</div>
                    <div class="number">{rating}</div>
                    <div class="label">تقييم</div>
                </div>
                <div class="stat">
                    <div class="icon">🏆</div>
                    <div class="number">5</div>
                    <div class="label">سنوات</div>
                </div>
            </div>
            
            <!-- Brand Footer -->
            <div class="brand-footer">
                <div class="logo-group">
                    <div class="logo">M</div>
                    <span class="domain">{domain}</span>
                </div>
                <div class="cta">احجز الآن ←</div>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    return html


# =============================================================================
# TEMPLATE 3: INFOGRAPHIC — Data-rich layout filling space with stats & icons
# =============================================================================

def template_infographic(photo_b64, data, colors):
    business_name = data.get('business_name', 'اسم النشاط')
    headline = data.get('headline', 'عنوان رئيسي')
    kicker = data.get('kicker', 'الأفضل في الرياض')
    taglines = data.get('taglines', ['خبرة واسعة', 'نتائج مضمونة', 'أسعار شفافة'])
    rating = data.get('rating', '٤٫٧')
    reviews = data.get('reviews', 200)
    reviews_str = data.get('reviews_str', str(reviews))
    domain = data.get('domain', 'nuhoot.xyz')
    trust_badge = data.get('trust_badge', '')
    brand_ar = data.get('brand_ar', 'نُهوت — التسويق الرقمي')
    
    bg_grad = colors.get('bg_grad', 'linear-gradient(135deg,#0c0c0c 0%,#1a1a2e 50%,#16213e 100%)')
    accent = colors.get('accent', '#00d9ff')
    accent_light = colors.get('accent_light', '#00ff88')
    text_color = colors.get('text', '#ffffff')
    text_3d = colors.get('text_3d_shadows', '1px 1px 0 #006680,2px 2px 0 rgba(0,0,0,0.3),3px 3px 10px rgba(0,0,0,0.4)')
    
    return '''<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;700;900&family=Noto+Sans+Arabic:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
html,body{width:1080px;height:1080px;overflow:hidden;font-family:'Noto Sans Arabic',sans-serif;}
.info-bg{width:1080px;height:1080px;background:{bg_grad};position:relative;overflow:hidden;direction:rtl;}
.info-bg::before{content:'';position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,0.03) 1px,transparent 1px);background-size:40px 40px;z-index:1;}
.blob{position:absolute;border-radius:50%;filter:blur(60px);z-index:1;}
.blob-a{width:350px;height:350px;background:{accent};opacity:0.15;top:-100px;left:-80px;}
.blob-b{width:300px;height:300px;background:{accent_light};opacity:0.1;bottom:-80px;right:-60px;}
.info-header{position:absolute;top:0;left:0;right:0;padding:35px 50px 20px;z-index:10;display:flex;justify-content:space-between;align-items:flex-start;}
.info-kicker{font-size:14px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:{accent};}
.info-biz{background:{accent};color:white;padding:8px 20px;border-radius:30px;font-size:18px;font-weight:700;font-family:'Noto Kufi Arabic',serif;box-shadow:0 4px 15px rgba(0,0,0,0.2);display:inline-block;}
.info-headline{font-family:'Noto Kufi Arabic',serif;font-size:46px;font-weight:900;color:{text_color};text-shadow:{text_3d};margin-top:10px;line-height:1.2;}
.accent-bar{width:80px;height:3px;background:{accent};border-radius:2px;margin-top:12px;}
.info-left{position:absolute;top:170px;right:50px;width:460px;z-index:5;display:flex;flex-direction:column;gap:20px;}
.info-photo{width:100%;height:340px;border-radius:20px;overflow:hidden;box-shadow:0 20px 50px rgba(0,0,0,0.4);position:relative;}
.info-photo img{width:100%;height:100%;object-fit:cover;}
.info-photo::after{content:'';position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,0.5),transparent 50%);}
.stats-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
.stat-card{background:rgba(255,255,255,0.08);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:18px;text-align:center;}
.stat-num{font-size:32px;font-weight:900;color:{accent};text-shadow:0 0 20px {accent}60;}
.stat-lbl{font-size:13px;color:rgba(255,255,255,0.6);margin-top:4px;}
.info-right{position:absolute;top:170px;left:50px;width:460px;z-index:5;display:flex;flex-direction:column;gap:16px;}
.sec-label{font-size:13px;font-weight:700;color:{accent};text-transform:uppercase;letter-spacing:0.15em;margin-bottom:8px;}
.feat-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;}
.feat-item{display:flex;align-items:center;gap:8px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:12px 14px;}
.feat-icon{width:28px;height:28px;background:{accent}20;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:14px;}
.feat-text{font-size:14px;color:{text_color} ;font-weight:600;}
.rating-block{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:20px;}
.rating-row{display:flex;align-items:center;gap:12px;margin-bottom:12px;}
.rating-num{font-size:36px;font-weight:900;color:{accent};}
.rating-stars{color:#FFD700;font-size:22px;}
.rating-reviews{font-size:14px;color:rgba(255,255,255,0.6);}
.rating-bar{width:100%;height:8px;background:rgba(255,255,255,0.1);border-radius:10px;overflow:hidden;}
.rating-fill{height:100%;background:linear-gradient(90deg,{accent},{accent_light});border-radius:10px;width:94%;}
.cert-row{display:flex;flex-wrap:wrap;gap:8px;}
.cert-chip{display:inline-flex;align-items:center;gap:6px;background:{accent}20;border:1px solid {accent}40;color:{accent_light};padding:8px 14px;border-radius:20px;font-size:13px;font-weight:600;}
.tag-pills{display:flex;flex-wrap:wrap;gap:8px;}
.tag-pill{background:rgba(255,255,255,0.1);color:white;padding:10px 18px;border-radius:30px;font-size:15px;font-weight:600;box-shadow:0 4px 15px rgba(0,0,0,0.15);}
.info-footer{position:absolute;bottom:0;left:0;right:0;padding:16px 50px;z-index:10;display:flex;justify-content:space-between;align-items:center;border-top:1px solid rgba(255,255,255,0.1);}
.info-footer span{font-size:15px;color:{accent};opacity:0.7;}
.diamond{position:absolute;width:10px;height:10px;background:{accent};transform:rotate(45deg);opacity:0.3;z-index:2;}
</style></head><body>
<div class="info-bg">
  <div class="blob blob-a"></div><div class="blob blob-b"></div>
  <div class="diamond" style="top:12%;left:8%;"></div>
  <div class="diamond" style="top:30%;right:5%;width:6px;height:6px;"></div>
  <div class="diamond" style="bottom:25%;left:12%;width:8px;height:8px;"></div>
  <div class="diamond" style="bottom:40%;right:8%;"></div>
  <div class="info-header">
    <div>
      <span class="info-kicker">{kicker}</span>
      <h1 class="info-headline">{headline}</h1>
      <div class="accent-bar"></div>
    </div>
    <span class="info-biz">{business_name}</span>
  </div>
  <div class="info-left">
    <div class="info-photo"><img src="data:image/jpeg;base64,{photo_b64}"></div>
    <div class="stats-grid">
      <div class="stat-card"><div class="stat-num">+٥٠٠</div><div class="stat-lbl">عميل سعيد</div></div>
      <div class="stat-card"><div class="stat-num">+١٠</div><div class="stat-lbl">سنوات خبرة</div></div>
      <div class="stat-card"><div class="stat-num">٩٨٪</div><div class="stat-lbl">نسبة رضا</div></div>
      <div class="stat-card"><div class="stat-num">٢٤/٧</div><div class="stat-lbl">دعم متواصل</div></div>
    </div>
  </div>
  <div class="info-right">
    <div>
      <div class="sec-label">✦ مميزاتنا</div>
      <div class="feat-grid">
        <div class="feat-item"><div class="feat-icon">✓</div><span class="feat-text">استشارات مجانية</span></div>
        <div class="feat-item"><div class="feat-icon">✓</div><span class="feat-text">فريق متخصص</span></div>
        <div class="feat-item"><div class="feat-icon">✓</div><span class="feat-text">ضمان الجودة</span></div>
        <div class="feat-item"><div class="feat-icon">✓</div><span class="feat-text">متابعة مستمرة</span></div>
        <div class="feat-item"><div class="feat-icon">✓</div><span class="feat-text">دعم فني</span></div>
        <div class="feat-item"><div class="feat-icon">✓</div><span class="feat-text">حلول مبتكرة</span></div>
      </div>
    </div>
    <div class="rating-block">
      <div class="rating-row">
        <span class="rating-num">{rating}</span>
        <span class="rating-stars">★★★★☆</span>
        <span class="rating-reviews">{reviews_str} تقييم</span>
      </div>
      <div class="rating-bar"><div class="rating-fill"></div></div>
    </div>
    <div>
      <div class="sec-label">✦ الشهادات</div>
      <div class="cert-row">
        <span class="cert-chip">✓ موثق</span>
        <span class="cert-chip">✓ معتمد</span>
        
      </div>
    </div>
    <div>
      <div class="sec-label">✦ ليش تختارونا</div>
      <div class="tag-pills">
        {taglines_html}
      </div>
    </div>
  </div>
  <div class="info-footer">
    <span>{brand_ar}</span>
    <span>{domain}</span>
  </div>
</div>
</body></html>'''

    taglines_html = ''.join([f'<span class="tag-pill">{t}</span>' for t in taglines])
    trust_badge_chip = f'<span class="cert-chip">✓ {trust_badge}</span>' if trust_badge else ''
    
    # Use .format() instead of f-strings to avoid brace conflicts
    html = html_template.format(
        bg_grad=bg_grad, accent=accent, accent_light=accent_light,
        text_color=text_color, text_3d=text_3d,
        kicker=kicker, headline=headline, business_name=business_name,
        photo_b64=photo_b64, rating=rating, reviews_str=reviews_str,
        taglines_html=taglines_html, brand_ar=brand_ar, domain=domain,
    )
    return html


# =============================================================================
# TEMPLATE 4: BILLBOARD — Full-bleed photo with overlaid glass elements
# =============================================================================

def template_billboard(photo_b64, data, colors):
    business_name = data.get('business_name', 'اسم النشاط')
    headline = data.get('headline', 'عنوان رئيسي')
    kicker = data.get('kicker', 'الأفضل في الرياض')
    taglines = data.get('taglines', ['جودة عالية', 'خدمة مميزة', 'أسعار منافسة'])
    rating = data.get('rating', '٤٫٧')
    reviews = data.get('reviews', 200)
    reviews_str = data.get('reviews_str', str(reviews))
    domain = data.get('domain', 'nuhoot.xyz')
    trust_badge = data.get('trust_badge', '')
    brand_ar = data.get('brand_ar', 'نُهوت — التسويق الرقمي')
    
    accent = colors.get('accent', '#e94560')
    accent_light = colors.get('accent_light', '#ff6b6b')
    pill_bg = colors.get('pill_bg', 'rgba(255,255,255,0.15)')
    pill_text = colors.get('pill_text', '#ffffff')
    
    pills_html = ''.join([f'<span class="bb-pill" style="background:{accent};">{t}</span>' for t in taglines])
    trust_html = f'<span class="bb-trust">✦ {trust_badge}</span>' if trust_badge else ''
    
    return f'<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><link href="https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;700;900&family=Noto+Sans+Arabic:wght@400;600;700;900&display=swap" rel="stylesheet"><style>*{{margin:0;padding:0;box-sizing:border-box;}}html,body{{width:1080px;height:1080px;overflow:hidden;font-family:"Noto Sans Arabic",sans-serif;}}.bb{{width:1080px;height:1080px;position:relative;overflow:hidden;direction:rtl;}}.bb img.bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:1;}}.bb::after{{content:"";position:absolute;inset:0;z-index:2;background:linear-gradient(0deg,rgba(0,0,0,0.92) 0%,rgba(0,0,0,0.5) 35%,rgba(0,0,0,0.2) 60%,rgba(0,0,0,0.4) 100%);}}.bb-top{{position:absolute;top:35px;left:50px;right:50px;z-index:10;display:flex;justify-content:space-between;align-items:flex-start;}}.bb-kicker{{background:rgba(255,255,255,0.15);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,0.2);color:white;padding:8px 18px;border-radius:30px;font-size:14px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;}}.bb-badge{{background:{accent};color:white;padding:8px 20px;border-radius:30px;font-size:18px;font-weight:700;font-family:"Noto Kufi Arabic",serif;box-shadow:0 8px 25px {accent}80;}}.bb-side{{position:absolute;top:50%;right:30px;transform:translateY(-50%);z-index:10;display:flex;flex-direction:column;gap:14px;}}.bb-icon{{width:48px;height:48px;background:rgba(255,255,255,0.15);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,0.2);border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:22px;box-shadow:0 4px 15px rgba(0,0,0,0.2);}}.bb-price{{position:absolute;top:140px;left:40px;z-index:10;width:100px;height:100px;background:linear-gradient(135deg,{accent},{accent_light});border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 8px 30px {accent}80;}}.bb-price-lbl{{font-size:11px;color:rgba(255,255,255,0.9);}}.bb-price-val{{font-size:32px;font-weight:900;color:white;line-height:1;}}.bb-price-unit{{font-size:12px;color:rgba(255,255,255,0.9);}}.bb-center{{position:absolute;top:48%;left:50%;transform:translate(-50%,-50%);z-index:10;text-align:center;width:80%;}}.bb-headline{{font-family:"Noto Kufi Arabic",serif;font-size:54px;font-weight:900;color:white;text-shadow:2px 2px 0 {accent},4px 4px 0 rgba(0,0,0,0.5),6px 6px 20px rgba(0,0,0,0.6);line-height:1.15;}}.bb-line{{width:100px;height:3px;background:{accent_light};border-radius:2px;margin:16px auto;}}.bb-bottom{{position:absolute;bottom:0;left:0;right:0;z-index:10;padding:30px 50px 25px;}}.bb-glass{{background:rgba(255,255,255,0.1);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.15);border-radius:24px;padding:24px 30px;display:flex;flex-direction:column;gap:16px;box-shadow:0 -10px 40px rgba(0,0,0,0.3);}}.bb-pills{{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;}}.bb-pill{{color:white;padding:10px 20px;border-radius:30px;font-size:15px;font-weight:600;box-shadow:0 4px 15px rgba(0,0,0,0.2);}}.bb-info{{display:flex;justify-content:space-between;align-items:center;gap:20px;}}.bb-rating{{display:flex;align-items:center;gap:10px;}}.bb-stars{{color:#FFD700;font-size:24px;}}.bb-rating-num{{font-size:28px;font-weight:900;color:white;}}.bb-reviews{{font-size:15px;color:rgba(255,255,255,0.6);}}.bb-trust{{font-size:14px;color:{accent_light};}}.bb-footer{{display:flex;justify-content:space-between;align-items:center;padding-top:12px;border-top:1px solid rgba(255,255,255,0.1);}}.bb-footer span{{font-size:14px;color:rgba(255,255,255,0.5);}}.bb-corner{{position:absolute;width:50px;height:50px;z-index:5;pointer-events:none;}}.bb-corner::before,.bb-corner::after{{content:"";position:absolute;background:{accent_light};opacity:0.6;}}.bb-corner::before{{width:100%;height:2px;}}.bb-corner::after{{width:2px;height:100%;}}.bb-tl{{top:20px;left:20px;}}.bb-tl::before{{top:0;left:0;}}.bb-tl::after{{top:0;left:0;}}.bb-tr{{top:20px;right:20px;}}.bb-tr::before{{top:0;right:0;}}.bb-tr::after{{top:0;right:0;}}</style></head><body><div class="bb"><img class="bg" src="data:image/jpeg;base64,{photo_b64}"><div class="bb-corner bb-tl"></div><div class="bb-corner bb-tr"></div><div class="bb-top"><span class="bb-kicker">{kicker}</span><span class="bb-badge">{business_name}</span></div><div class="bb-side"><div class="bb-icon">⭐</div><div class="bb-icon">📍</div><div class="bb-icon">📞</div><div class="bb-icon">🕐</div></div><div class="bb-price"><span class="bb-price-lbl">يبدأ من</span><span class="bb-price-val">٩٩</span><span class="bb-price-unit">ر.س</span></div><div class="bb-center"><h1 class="bb-headline">{headline}</h1><div class="bb-line"></div></div><div class="bb-bottom"><div class="bb-glass"><div class="bb-pills">{pills_html}</div><div class="bb-info"><div class="bb-rating"><span class="bb-stars">★★★★<span style="opacity:0.3">★</span></span><span class="bb-rating-num">{rating}</span><span class="bb-reviews">{reviews_str} تقييم</span></div>{trust_html}</div><div class="bb-footer"><span>{brand_ar}</span><span>{domain}</span></div></div></div></div></body></html>'


# =============================================================================
# TEMPLATE 5: CARD STACK — Layered cards with depth shadows
# =============================================================================

def template_cardstack(photo_b64, data, colors):
    business_name = data.get('business_name', 'اسم النشاط')
    headline = data.get('headline', 'عنوان رئيسي')
    kicker = data.get('kicker', 'الأفضل في الرياض')
    taglines = data.get('taglines', ['جودة عالية', 'خدمة مميزة', 'أسعار منافسة'])
    rating = data.get('rating', '٤٫٧')
    reviews = data.get('reviews', 200)
    reviews_str = data.get('reviews_str', str(reviews))
    domain = data.get('domain', 'nuhoot.xyz')
    trust_badge = data.get('trust_badge', '')
    brand_ar = data.get('brand_ar', 'نُهوت — التسويق الرقمي')
    
    bg_grad = colors.get('bg_grad', 'linear-gradient(135deg,#1a1a2e 0%,#0f0f1e 100%)')
    accent = colors.get('accent', '#e94560')
    accent_light = colors.get('accent_light', '#ff6b6b')
    text_color = colors.get('text', '#ffffff')
    pill_bg = colors.get('pill_bg', 'rgba(255,255,255,0.1)')
    pill_text = colors.get('pill_text', '#ffffff')
    text_3d = colors.get('text_3d_shadows', f'1px 1px 0 {accent},2px 2px 0 rgba(0,0,0,0.3),3px 3px 10px rgba(0,0,0,0.4)')
    
    feat_html = ''.join([f'<div class="cs-feat"><div class="cs-check">✓</div><span>{t}</span></div>' for t in taglines])
    pills_html = ''.join([f'<span class="cs-pill" style="background:{pill_bg};color:{pill_text};">{t}</span>' for t in taglines])
    trust_html = f'<span class="cs-trust">✦ {trust_badge}</span>' if trust_badge else ''
    
    return f'<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><link href="https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;700;900&family=Noto+Sans+Arabic:wght@400;600;700;900&display=swap" rel="stylesheet"><style>*{{margin:0;padding:0;box-sizing:border-box;}}html,body{{width:1080px;height:1080px;overflow:hidden;font-family:"Noto Sans Arabic",sans-serif;}}.cs{{width:1080px;height:1080px;background:{bg_grad};position:relative;overflow:hidden;direction:rtl;}}.cs::before{{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,0.02) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,0.02) 1px,transparent 1px);background-size:40px 40px;z-index:1;}}.cs-blob{{position:absolute;border-radius:50%;filter:blur(80px);z-index:1;}}.cs-b1{{width:400px;height:400px;background:{accent};opacity:0.1;top:-100px;right:-100px;}}.cs-b2{{width:300px;height:300px;background:{accent_light};opacity:0.08;bottom:-50px;left:-50px;}}.cs-header{{position:absolute;top:30px;left:0;right:0;padding:0 45px;z-index:10;display:flex;justify-content:space-between;align-items:flex-start;}}.cs-kicker{{font-size:13px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:{accent};}}.cs-biz{{background:{accent};color:white;padding:6px 18px;border-radius:30px;font-size:16px;font-weight:700;font-family:"Noto Kufi Arabic",serif;box-shadow:0 4px 15px {accent}40;}}.cs-headline{{position:absolute;top:85px;right:45px;left:45px;z-index:10;text-align:right;}}.cs-headline h1{{font-family:"Noto Kufi Arabic",serif;font-size:48px;font-weight:900;color:{text_color};text-shadow:{text_3d};line-height:1.15;}}.cs-divider{{width:70px;height:3px;background:{accent};border-radius:2px;margin-top:14px;}}.cs-photo{{position:absolute;top:200px;right:45px;width:540px;height:380px;border-radius:20px;overflow:hidden;z-index:5;box-shadow:0 25px 60px rgba(0,0,0,0.4),0 0 0 1px rgba(255,255,255,0.1);}}.cs-photo img{{width:100%;height:100%;object-fit:cover;}}.cs-photo-badge{{position:absolute;top:15px;right:15px;background:rgba(0,0,0,0.6);backdrop-filter:blur(10px);color:white;padding:8px 14px;border-radius:20px;font-size:13px;font-weight:600;z-index:6;border:1px solid rgba(255,255,255,0.15);}}.cs-info{{position:absolute;top:220px;left:45px;width:400px;background:rgba(255,255,255,0.08);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.12);border-radius:20px;padding:24px;z-index:8;box-shadow:0 20px 50px rgba(0,0,0,0.3);display:flex;flex-direction:column;gap:14px;}}.cs-info-label{{font-size:12px;font-weight:700;color:{accent};text-transform:uppercase;letter-spacing:0.15em;}}.cs-feat{{display:flex;align-items:center;gap:10px;font-size:14px;color:{text_color};}}.cs-check{{width:20px;height:20px;background:{accent}30;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:12px;color:{accent_light};}}.cs-stats{{position:absolute;bottom:200px;left:45px;width:400px;background:rgba(255,255,255,0.06);backdrop-filter:blur(15px);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:20px 24px;z-index:7;box-shadow:0 15px 40px rgba(0,0,0,0.25);}}.cs-stats-row{{display:flex;justify-content:space-around;gap:12px;}}.cs-stat{{text-align:center;}}.cs-stat-num{{font-size:28px;font-weight:900;color:{accent};text-shadow:0 0 15px {accent}40;}}.cs-stat-lbl{{font-size:12px;color:rgba(255,255,255,0.5);margin-top:2px;}}.cs-bottom{{position:absolute;bottom:60px;left:45px;right:45px;background:rgba(255,255,255,0.08);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.12);border-radius:20px;padding:20px 28px;z-index:8;box-shadow:0 15px 40px rgba(0,0,0,0.3);display:flex;flex-direction:column;gap:14px;}}.cs-pills{{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;}}.cs-pill{{padding:9px 18px;border-radius:30px;font-size:14px;font-weight:600;box-shadow:0 4px 12px rgba(0,0,0,0.15);}}.cs-brow{{display:flex;justify-content:space-between;align-items:center;}}.cs-rating{{display:flex;align-items:center;gap:10px;}}.cs-stars{{color:#FFD700;font-size:22px;}}.cs-rnum{{font-size:26px;font-weight:900;color:{text_color};}}.cs-reviews{{font-size:14px;color:rgba(255,255,255,0.5);}}.cs-trust{{font-size:13px;color:{accent_light};}}.cs-footer{{display:flex;justify-content:space-between;align-items:center;padding-top:10px;border-top:1px solid rgba(255,255,255,0.08);}}.cs-footer span{{font-size:13px;color:rgba(255,255,255,0.4);}}.cs-diamond{{position:absolute;width:8px;height:8px;background:{accent};transform:rotate(45deg);opacity:0.3;z-index:2;}}</style></head><body><div class="cs"><div class="cs-blob cs-b1"></div><div class="cs-blob cs-b2"></div><div class="cs-diamond" style="top:15%;left:8%;"></div><div class="cs-diamond" style="top:45%;right:3%;"></div><div class="cs-diamond" style="bottom:35%;left:10%;width:6px;height:6px;"></div><div class="cs-header"><span class="cs-kicker">{kicker}</span><span class="cs-biz">{business_name}</span></div><div class="cs-headline"><h1>{headline}</h1><div class="cs-divider"></div></div><div class="cs-photo"><img src="data:image/jpeg;base64,{photo_b64}"><div class="cs-photo-badge">✦ مميز</div></div><div class="cs-info"><span class="cs-info-label">✦ ليش تختارونا</span>{feat_html}</div><div class="cs-stats"><div class="cs-stats-row"><div class="cs-stat"><div class="cs-stat-num">+٥٠٠</div><div class="cs-stat-lbl">عميل</div></div><div class="cs-stat"><div class="cs-stat-num">+١٠</div><div class="cs-stat-lbl">سنوات</div></div><div class="cs-stat"><div class="cs-stat-num">٩٨٪</div><div class="cs-stat-lbl">رضا</div></div></div></div><div class="cs-bottom"><div class="cs-pills">{pills_html}</div><div class="cs-brow"><div class="cs-rating"><span class="cs-stars">★★★★<span style="opacity:0.3">★</span></span><span class="cs-rnum">{rating}</span><span class="cs-reviews">{reviews_str} تقييم</span></div>{trust_html}</div><div class="cs-footer"><span>{brand_ar}</span><span>{domain}</span></div></div></div></body></html>'


# =============================================================================
# REGISTRY
# =============================================================================

TEMPLATES = {
    1: ("Magazine", template_magazine),
    2: ("Collage", template_collage),
    3: ("Infographic", template_infographic),
    4: ("Billboard", template_billboard),
    5: ("Card Stack", template_cardstack),
}


def generate_html(template_id, photo_path, data, colors=None, niche="restaurants"):
    import base64
    with open(photo_path, "rb") as f:
        photo_b64 = base64.b64encode(f.read()).decode()
    
    if colors is None:
        from nuhoot.design.v5_alive import _get_colors
        colors = _get_colors(niche)
    
    name, func = TEMPLATES[template_id]
    return func(photo_b64, data, colors)
