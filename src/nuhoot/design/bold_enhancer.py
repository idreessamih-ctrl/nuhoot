#!/usr/bin/env python3
"""
Nuhoot Bold Design v2 — COLOR PLATES + SAUDI SLANG.
- Shapes now use 2 colors (accent + accent2) at FULL opacity
- Color plates: solid blocks of contrasting color
- All copy rewritten in authentic Saudi dialect
"""
import base64, sys, os
sys.path.insert(0, '/opt/nuhoot/src')
os.chdir('/opt/nuhoot')
from pathlib import Path
from PIL import Image
import numpy as np
from playwright.sync_api import sync_playwright
from nuhoot.design.niche_text_engine import generate_text
from nuhoot.design.niche_config import get_trust_badge

_AR = "٠١٢٣٤٥٦٧٨٩"
_to_ar = lambda s: "".join(_AR[int(c)] if c.isdigit() else c for c in str(s))

def photo_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def best_photo(niche):
    photos = sorted(Path(f"/opt/nuhoot/assets/photos/{niche}").glob("*.jpg"))
    if not photos:
        return None
    best, best_skin = photos[0], 0
    for p in photos:
        arr = np.array(Image.open(p).convert('RGB'))
        r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
        skin = np.mean((r > 95) & (g > 40) & (b > 20) & (r > g) & (r > b) & (r - g > 15))
        if skin > best_skin:
            best_skin, best = skin, p
    return str(best)

def square_crop(path):
    img = Image.open(path).convert('RGB')
    w, h = img.size
    s = min(w, h)
    return img.crop(((w-s)//2, (h-s)//2, (w-s)//2+s, (h-s)//2+s))

# ═══════════════════════════════════════════════════════
# SAUDI SLANG COPY — authentic Riyadh dialect
# ═══════════════════════════════════════════════════════
BUSINESS = {
    "restaurants":   {"name":"مطعم النخبة","headline":"أكلك يفتح النفس","kicker":"RIYADH • FINE DINING","taglines":["أكل يقرمس","أسعار تسوى","أجواء تجنن"],"trust":"تقييم عالي على خرائط جوجل","rating":"٤٫٧","reviews":320,"cta":"زورونا الحين","hashtags":["#مطعم_النخبة","#الرياض","#أكل_سعودي","#تجربة_حلوة"]},
    "cafes":         {"name":"قهوة الصباح","headline":"قهوتك على كيفك","kicker":"RIYADH • COFFEE HOUSE","taglines":["دقة فقهوة","مكان يرتبط","خدمة تخبل"],"trust":"حبوب محمصة كل يوم","rating":"٤٫٦","reviews":180,"cta":"مر حياك","hashtags":["#قهوة_مختصة","#الرياض","#كوفي","#وقت_القهوة"]},
    "bakeries":      {"name":"مخبز الحلو","headline":"طازج من الفرن","kicker":"RIYADH • ARTISAN BAKERY","taglines":["ريحته تسوى","معجنات لازبة","حلويات تخبل"],"trust":"فرن حجري أصلي","rating":"٤٫٨","reviews":240,"cta":"اطلب الحين","hashtags":["#مخبز","#طازج","#الرياض","#معجنات"]},
    "salons":        {"name":"صالون لمسة فن","headline":"ستايلك يفرض نفسه","kicker":"RIYADH • BEAUTY & STYLE","taglines":["لمسة تفرق","نتايج تشوفينها","خبيرات يفهمونك"],"trust":"خبيرات معتمدات","rating":"٤٫٩","reviews":450,"cta":"احجزي موعدك","hashtags":["#صالون_الرياض","#جمال","#لمسة_فن","#ستايل"]},
    "spas":          {"name":"سبا الورد","headline":"ريّح جسمك ورح بالك","kicker":"RIYADH • WELLNESS SPA","taglines":["مساج يريحك","أجواء تهديك","عناية تحسينها"],"trust":"معالجات مرخصات","rating":"٤٫٧","reviews":160,"cta":"احجزي جلستك","hashtags":["#سبا","#استرخاء","#الرياض","#عناية"]},
    "barbershops":   {"name":"حلاقة الأناقة","headline":"شكلك يبي يفرق","kicker":"RIYADH • PREMIUM BARBER","taglines":["قصات تبان فيك","حلاقة نظيفة","عناية باللحية"],"trust":"أفضل حلاقين بالرياض","rating":"٤٫٨","reviews":310,"cta":"احجز موعدك","hashtags":["#حلاقة","#الرياض","#قصات","#أناقة"]},
    "gyms":          {"name":"نادي الأبطال","headline":"فكها وطلع قوتك","kicker":"RIYADH • FITNESS","taglines":["ما فيه أعذار","مدربين يرفعونك","جسمك يستاهل"],"trust":"نتايج مضمونة","rating":"٤٫٨","reviews":280,"cta":"اشترك الحين","hashtags":["#لياقة","#رياضة","#الرياض","#جيم"]},
    "clinics":       {"name":"عيادة الشفاء","headline":"صحتك غالية علينا","kicker":"RIYADH • HEALTHCARE","taglines":["دكترة يفهمون","تشخيص دقيق","متابعة حلوة"],"trust":"معتمدة من وزارة الصحة","rating":"٤٫٦","reviews":510,"cta":"احجز موعدك","hashtags":["#عيادة","#صحة","#الرياض","#شفاء"]},
    "dentists":      {"name":"مركز الابتسامة","headline":"ابتسامتك تسوى","kicker":"RIYADH • DENTAL CARE","taglines":["تبييض يبيض","زراعة مضمونة","ابتسامة تفرق"],"trust":"أحدث التقنيات","rating":"٤٫٧","reviews":290,"cta":"احجز وأبتسم","hashtags":["#أسنان","#ابتسامة","#الرياض","#بياض"]},
    "pharmacies":    {"name":"صيدلية الرعاية","headline":"دواك عندنا","kicker":"RIYADH • PHARMACY","taglines":["أدوية أصلية","استشارة مجانية","توصيل يوصلك"],"trust":"مرخصة وزارة الصحة","rating":"٤٫٥","reviews":420,"cta":"اطلب دوابك","hashtags":["#صيدلية","#دواء","#الرياض","#صحة"]},
    "dermatology":   {"name":"مركز الجلدية","headline":"بشرتك تستاهل","kicker":"RIYADH • DERMATOLOGY","taglines":["نتايج تشوفينها","ليزر متطور","متابعة شخصية"],"trust":"استشاريين معتمدين","rating":"٤٫٨","reviews":190,"cta":"احجزي استشارتك","hashtags":["#بشرة","#جلدية","#الرياض","#ليزر"]},
    "fashion":       {"name":"أزياء الليل","headline":"لبسك يميزك","kicker":"RIYADH • FASHION HOUSE","taglines":["تشكيلة تجنن","خامات فخمة","ستايل يفرض نفسه"],"trust":"دار أزياء رائدة","rating":"٤٫٦","reviews":150,"cta":"زوري المجموعة","hashtags":["#أزياء","#موضة","#الرياض","#ستايل"]},
    "perfumes":      {"name":"عطور المسك","headline":"ريحتك تسبقك","kicker":"RIYADH • LUXURY PERFUMES","taglines":["عود يبقى","مسك يفوح","خلطات حصرية"],"trust":"عطور معتمدة دولياً","rating":"٤٫٩","reviews":190,"cta":"جرّب الحين","hashtags":["#عطور","#عود","#مسك","#الرياض"]},
    "law_firms":     {"name":"مكتب العدالة","headline":"حقك ما يضيع","kicker":"RIYADH • LEGAL SERVICES","taglines":["استشارة قانونية","تمثيل قدام المحكمة","صياغة عقود"],"trust":"محامين معتمدين وزارة العدل","rating":"٤٫٥","reviews":95,"cta":"استشر المحامين","hashtags":["#محاماة","#حقوق","#الرياض","#استشارة"]},
    "real_estate":   {"name":"عقارات الرياض","headline":"بيتك يبدأ من هنا","kicker":"RIYADH • REAL ESTATE","taglines":["بيع وشراء","إدارة أملاك","تقييم عقاري"],"trust":"عقارات موثقة ومسجلة","rating":"٤٫٤","reviews":130,"cta":"تواصل وياانا","hashtags":["#عقارات","#بيت","#الرياض","#استثمار"]},
    "auto_shops":    {"name":"ورشة المحترف","headline":"سيارتك بأيد أمينة","kicker":"RIYADH • AUTO SERVICE","taglines":["صيانة شاملة","فحص كمبيوتر","قطع أصلية"],"trust":"ضمان على الصيانة","rating":"٤٫٣","reviews":210,"cta":"احجز صيانتك","hashtags":["#صيانة","#سيارات","#الرياض","#ورشة"]},
    "car_wash":      {"name":"غسيل لمعان","headline":"سيارتك تلمع كالجديد","kicker":"RIYADH • CAR CARE","taglines":["غسيل خارجي وداخلي","تلميع يلمع","شمع يحمي"],"trust":"تلميع احترافي مضمون","rating":"٤٫٢","reviews":170,"cta":"اعطنا سيارتك","hashtags":["#غسيل","#سيارات","#الرياض","#لمعان"]},
    "cleaning":      {"name":"نظافة النخبة","headline":"بيتك يفرق","kicker":"RIYADH • CLEANING SERVICES","taglines":["تنظيف شامل","تعقيم يطمنك","فريق يخبل"],"trust":"مواد آمنة ومصرح بها","rating":"٤٫٦","reviews":220,"cta":"احجز فريقك","hashtags":["#تنظيف","#بيت","#الرياض","#نظافة"]},
    "hvac_ac":       {"name":"تبريد الرياض","headline":"برودة تريحك","kicker":"RIYADH • HVAC SERVICES","taglines":["تركيب وصيانة","تكييف مركزي","خدمة سريعة"],"trust":"صيانة معتمدة","rating":"٤٫٤","reviews":140,"cta":"اطلب الصيانة","hashtags":["#تكييف","#صيانة","#الرياض","#تبريد"]},
    "event_halls":   {"name":"قاعة الأحلام","headline":"لحظاتك تستاهل","kicker":"RIYADH • EVENT VENUE","taglines":["قاعات فخمة","تنسيق كامل","أكل يفتح النفس"],"trust":"خبرة بتنظيم المناسبات","rating":"٤٫٧","reviews":260,"cta":"احجز تاريخك","hashtags":["#قاعة","#مناسبات","#الرياض","#أحلام"]},
    "training_centers":{"name":"مركز التميز","headline":"طوّر نفسك","kicker":"RIYADH • TRAINING CENTER","taglines":["دورات معتمدة","مدربين خبراء","شهادات معترف بها"],"trust":"شهادات معتمدة","rating":"٤٫٥","reviews":180,"cta":"سجل الحين","hashtags":["#تدريب","#دورات","#الرياض","#تطوير"]},
}

# ═══════════════════════════════════════════════════════
# NICHE DATA — now with accent2 (CONTRASTING color)
# ═══════════════════════════════════════════════════════
NICHE_DATA = {
    "restaurants":   {"bg":"#F5C518","bg2":"#E5A800","accent":"#1A1A1A","accent2":"#E63946","text":"#1A1A1A","pill_bg":"#1A1A1A","pill_text":"#FFFFFF","is_dark":False,"badge_bg":"#E63946","badge_text":"#FFFFFF","recipe":"A"},
    "cafes":         {"bg":"#6F4E37","bg2":"#5C3D2E","accent":"#F5DEB3","accent2":"#D4A055","text":"#FFF8E7","pill_bg":"#F5DEB3","pill_text":"#3E2723","is_dark":True,"badge_bg":"#D4A055","badge_text":"#3E2723","recipe":"A"},
    "bakeries":      {"bg":"#FF8C42","bg2":"#E07B30","accent":"#3E2723","accent2":"#FFE082","text":"#FFFFFF","pill_bg":"#FFFFFF","pill_text":"#3E2723","is_dark":False,"badge_bg":"#E63946","badge_text":"#FFFFFF","recipe":"E"},
    "salons":        {"bg":"#1A1A2E","bg2":"#16213E","accent":"#E94560","accent2":"#D4AF37","text":"#FFFFFF","pill_bg":"#E94560","pill_text":"#FFFFFF","is_dark":True,"badge_bg":"#E94560","badge_text":"#FFFFFF","recipe":"E"},
    "spas":          {"bg":"#2D4A3E","bg2":"#1E3328","accent":"#A8D5BA","accent2":"#E8C5A0","text":"#E8F5E9","pill_bg":"#A8D5BA","pill_text":"#1E3328","is_dark":True,"badge_bg":"#A8D5BA","badge_text":"#1E3328","recipe":"E"},
    "barbershops":   {"bg":"#0F0F0F","bg2":"#1A1A1A","accent":"#D4AF37","accent2":"#C0392B","text":"#FFFFFF","pill_bg":"#D4AF37","pill_text":"#0F0F0F","is_dark":True,"badge_bg":"#D4AF37","badge_text":"#0F0F0F","recipe":"B"},
    "gyms":          {"bg":"#0A0A0A","bg2":"#1A1A1A","accent":"#FF6B35","accent2":"#FFD93D","text":"#FFFFFF","pill_bg":"#FF6B35","pill_text":"#0A0A0A","is_dark":True,"badge_bg":"#FF6B35","badge_text":"#0A0A0A","recipe":"D"},
    "clinics":       {"bg":"#E8F4F8","bg2":"#D1ECF1","accent":"#2DB8A8","accent2":"#E63946","text":"#1E3A52","pill_bg":"#2DB8A8","pill_text":"#FFFFFF","is_dark":False,"badge_bg":"#2DB8A8","badge_text":"#FFFFFF","recipe":"C"},
    "dentists":      {"bg":"#E8F4F8","bg2":"#D1ECF1","accent":"#00A8D5","accent2":"#FFD93D","text":"#1E3A52","pill_bg":"#00A8D5","pill_text":"#FFFFFF","is_dark":False,"badge_bg":"#00A8D5","badge_text":"#FFFFFF","recipe":"C"},
    "pharmacies":    {"bg":"#E8F5E9","bg2":"#C8E6C9","accent":"#2E7D32","accent2":"#FF8C42","text":"#1B5E20","pill_bg":"#2E7D32","pill_text":"#FFFFFF","is_dark":False,"badge_bg":"#2E7D32","badge_text":"#FFFFFF","recipe":"C"},
    "dermatology":   {"bg":"#FCE4EC","bg2":"#F8BBD0","accent":"#C2185B","accent2":"#7B1FA2","text":"#4A148C","pill_bg":"#C2185B","pill_text":"#FFFFFF","is_dark":False,"badge_bg":"#C2185B","badge_text":"#FFFFFF","recipe":"B"},
    "fashion":       {"bg":"#1A1A2E","bg2":"#16213E","accent":"#E94560","accent2":"#D4AF37","text":"#FFFFFF","pill_bg":"#E94560","pill_text":"#FFFFFF","is_dark":True,"badge_bg":"#E94560","badge_text":"#FFFFFF","recipe":"B"},
    "perfumes":      {"bg":"#1A1A1A","bg2":"#2A2A2A","accent":"#D4AF37","accent2":"#8B4513","text":"#FFFFFF","pill_bg":"#D4AF37","pill_text":"#1A1A1A","is_dark":True,"badge_bg":"#D4AF37","badge_text":"#1A1A1A","recipe":"B"},
    "law_firms":     {"bg":"#0E1428","bg2":"#161E38","accent":"#B8CCE0","accent2":"#D4AF37","text":"#E8EDF5","pill_bg":"#B8CCE0","pill_text":"#0E1428","is_dark":True,"badge_bg":"#B8CCE0","badge_text":"#0E1428","recipe":"C"},
    "real_estate":   {"bg":"#0E1428","bg2":"#161E38","accent":"#D4AF37","accent2":"#48CAE4","text":"#E8EDF5","pill_bg":"#D4AF37","pill_text":"#0E1428","is_dark":True,"badge_bg":"#D4AF37","badge_text":"#0E1428","recipe":"C"},
    "auto_shops":    {"bg":"#1A1A1A","bg2":"#2A2A2A","accent":"#FF6B35","accent2":"#FFD93D","text":"#FFFFFF","pill_bg":"#FF6B35","pill_text":"#1A1A1A","is_dark":True,"badge_bg":"#FF6B35","badge_text":"#1A1A1A","recipe":"D"},
    "car_wash":      {"bg":"#0A1929","bg2":"#102A43","accent":"#48CAE4","accent2":"#80DEEA","text":"#FFFFFF","pill_bg":"#48CAE4","pill_text":"#0A1929","is_dark":True,"badge_bg":"#48CAE4","badge_text":"#0A1929","recipe":"D"},
    "cleaning":      {"bg":"#E8F5E9","bg2":"#C8E6C9","accent":"#4CAF50","accent2":"#29B6F6","text":"#1B5E20","pill_bg":"#4CAF50","pill_text":"#FFFFFF","is_dark":False,"badge_bg":"#4CAF50","badge_text":"#FFFFFF","recipe":"A"},
    "hvac_ac":       {"bg":"#0A1929","bg2":"#102A43","accent":"#48CAE4","accent2":"#FFD93D","text":"#FFFFFF","pill_bg":"#48CAE4","pill_text":"#0A1929","is_dark":True,"badge_bg":"#48CAE4","badge_text":"#0A1929","recipe":"D"},
    "event_halls":   {"bg":"#2D1B3D","bg2":"#1A0F28","accent":"#D4AF37","accent2":"#E94560","text":"#FFFFFF","pill_bg":"#D4AF37","pill_text":"#2D1B3D","is_dark":True,"badge_bg":"#D4AF37","badge_text":"#2D1B3D","recipe":"B"},
    "training_centers":{"bg":"#0E1428","bg2":"#161E38","accent":"#5C6BC0","accent2":"#FFD93D","text":"#E8EDF5","pill_bg":"#5C6BC0","pill_text":"#FFFFFF","is_dark":True,"badge_bg":"#5C6BC0","badge_text":"#FFFFFF","recipe":"C"},
}

def hex_rgba(hex_color, alpha):
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return "rgba(%d,%d,%d,%s)" % (r, g, b, alpha)

# ═══════════════════════════════════════════════════════
# COLOR PLATE SHAPES — now using BOTH accent + accent2 at FULL opacity
# ═══════════════════════════════════════════════════════
def _color_shapes(c):
    """Bold shapes using accent + accent2 at FULL color, not faded."""
    a1 = c["accent"]
    a2 = c["accent2"]
    bg = c["bg"]
    
    # Alternate between accent and accent2 for visual variety
    # Shapes are at 60-90% opacity — BOLD and COLORED
    shapes = [
        # (x, y, size, type, color, opacity)
        (70, 180, 40, "circle", a2, 0.85),
        (980, 160, 45, "diamond", a1, 0.80),
        (50, 440, 30, "circle", a1, 0.75),
        (1010, 420, 35, "circle", a2, 0.85),
        (100, 680, 38, "diamond", a2, 0.80),
        (970, 700, 32, "circle", a1, 0.75),
        (130, 880, 25, "circle", a2, 0.70),
        (930, 900, 28, "diamond", a1, 0.75),
        # Small accent dots
        (200, 150, 12, "circle", a1, 0.60),
        (880, 230, 10, "circle", a2, 0.65),
        (160, 580, 14, "circle", a2, 0.55),
        (920, 560, 12, "circle", a1, 0.60),
    ]
    
    html = ""
    for (x, y, size, stype, color, opacity) in shapes:
        col = hex_rgba(color, str(opacity))
        if stype == "circle":
            html += '<div style="position:absolute;top:%dpx;left:%dpx;width:%dpx;height:%dpx;border-radius:50%%;background:%s;z-index:2;"></div>\n' % (y, x, size, size, col)
        elif stype == "diamond":
            html += '<div style="position:absolute;top:%dpx;left:%dpx;width:%dpx;height:%dpx;background:%s;z-index:2;transform:rotate(45deg);"></div>\n' % (y, x, size, size, col)
    return html

def _color_plate(c, position="bottom"):
    """Solid color plate — bold block of accent2 color."""
    if position == "bottom":
        return '<div style="position:absolute;bottom:0;left:0;right:0;height:280px;background:%s;z-index:0;"></div>\n<div style="position:absolute;bottom:280px;left:0;right:0;height:50px;background:linear-gradient(180deg,transparent 0%%,%s 100%%);z-index:0;pointer-events:none;"></div>\n' % (c["bg2"], c["bg2"])
    elif position == "diagonal":
        return '<div style="position:absolute;top:0;left:0;width:100%%;height:55%%;background:%s;z-index:0;clip-path:polygon(0 0,100%% 0,100%% 65%%,0 100%%);"></div>\n' % c["bg2"]
    return ""

def _color_plate_accent2(c, x, y, w, h, opacity=0.15):
    """A solid plate of accent2 color — a touch of contrasting color."""
    return '<div style="position:absolute;top:%dpx;left:%dpx;width:%dpx;height:%dpx;background:%s;opacity:%s;z-index:0;border-radius:8px;"></div>\n' % (y, x, w, h, c["accent2"], opacity)

def _ring_frame(c, style_type="dashed", opacity=0.30, size=760, color=None):
    """Ring frame — now can use accent2 color."""
    col = color or c["accent"]
    top = 165 + (750 - size) // 2
    left = (1080 - size) // 2
    if style_type == "dashed":
        border = "4px dashed %s" % hex_rgba(col, str(opacity))
    elif style_type == "solid":
        border = "3px solid %s" % hex_rgba(col, str(opacity))
    elif style_type == "double":
        return ('<div style="position:absolute;top:%dpx;left:%dpx;width:%dpx;height:%dpx;border-radius:50%%;border:3px solid %s;z-index:1;"></div>\n'
                '<div style="position:absolute;top:%dpx;left:%dpx;width:%dpx;height:%dpx;border-radius:50%%;border:1px solid %s;z-index:1;"></div>\n'
                % (top, left, size, size, hex_rgba(c["accent"], str(opacity)),
                   top+20, left+20, size-40, size-40, hex_rgba(c["accent2"], str(opacity*0.5))))
    return '<div style="position:absolute;top:%dpx;left:%dpx;width:%dpx;height:%dpx;border-radius:50%%;border:%s;z-index:1;"></div>\n' % (top, left, size, size, border)

def _offer_badge(c, discount_text, sub_text):
    """Offer badge with gradient using accent2."""
    return """<div style="position:absolute;top:240px;right:160px;width:180px;height:180px;border-radius:50%%;
    background:linear-gradient(135deg,%s 0%%,%s 100%%);color:%s;
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    box-shadow:0 15px 40px rgba(0,0,0,0.3),0 5px 15px rgba(0,0,0,0.15);
    z-index:15;border:5px solid %s;transform:rotate(-12deg);">
    <span style="font-size:48px;font-weight:900;line-height:1;">%s</span>
    <span style="font-size:18px;font-weight:700;margin-top:4px;">%s</span>
    <span style="font-size:12px;font-weight:600;opacity:0.8;margin-top:2px;">عرض خاص</span>
    </div>""" % (c["badge_bg"], c["accent2"], c["badge_text"], c["bg"], discount_text, sub_text)

def _watermark(c, text, font_size=380, color=None):
    col = color or c["accent"]
    return '<div style="position:absolute;top:50%%;left:50%%;transform:translate(-50%%,-50%%);font-size:%dpx;font-weight:900;font-family:Noto Kufi Arabic,serif;color:%s;z-index:1;line-height:1;pointer-events:none;">%s</div>\n' % (font_size, hex_rgba(col, "0.06"), text)

def _corner_plate(c, corner="tl"):
    """Corner color plate — bold quarter circle of accent2."""
    if corner == "tl":
        return '<div style="position:absolute;top:-100px;left:-100px;width:250px;height:250px;border-radius:50%%;background:%s;opacity:0.15;z-index:0;pointer-events:none;"></div>\n' % c["accent2"]
    else:
        return '<div style="position:absolute;bottom:-100px;right:-100px;width:250px;height:250px;border-radius:50%%;background:%s;opacity:0.15;z-index:0;pointer-events:none;"></div>\n' % c["accent2"]

def _dots_line(c, x, y, count=6, use_accent2=False):
    color = c["accent2"] if use_accent2 else c["accent"]
    html = '<div style="position:absolute;top:%dpx;left:%dpx;display:flex;gap:10px;z-index:2;">' % (y, x)
    for _ in range(count):
        html += '<div style="width:8px;height:8px;border-radius:50%%;background:%s;opacity:0.6;"></div>' % color
    html += '</div>\n'
    return html

# ═══════════════════════════════════════════════════════
# RECIPES — now with COLOR PLATES + multi-color shapes
# ═══════════════════════════════════════════════════════
def recipe_A(c, biz):
    """Offer Focus — bold offer badge + color plate bottom + multi-color shapes"""
    e = ""
    e += _watermark(c, _to_ar("20"), 400, c["accent2"])
    e += _ring_frame(c, "dashed", 0.35, 760, c["accent"])
    e += _ring_frame(c, "solid", 0.12, 720, c["accent2"])
    e += _color_plate(c, "bottom")
    e += _corner_plate(c, "tl")
    e += _offer_badge(c, _to_ar("20"), "خصم ٪")
    e += _color_shapes(c)
    e += _dots_line(c, 900, 130, 6)
    return e

def recipe_B(c, biz):
    """Premium Showcase — double ring (2 colors) + gold accents + corner plates"""
    e = ""
    e += _ring_frame(c, "double", 0.25, 760)
    e += _corner_plate(c, "tl")
    e += _corner_plate(c, "br")
    e += _watermark(c, "★", 350, c["accent2"])
    e += _color_shapes(c)
    e += _dots_line(c, 900, 120, 4, True)
    return e

def recipe_C(c, biz):
    """Trust Builder — clean color plate + subtle multi-color accents"""
    e = ""
    e += _color_plate(c, "bottom")
    e += _ring_frame(c, "solid", 0.20, 740, c["accent"])
    e += _watermark(c, "★★★★★", 200, c["accent2"])
    e += _color_shapes(c)
    e += _dots_line(c, 900, 140, 5)
    # Add accent2 color plate touch
    e += _color_plate_accent2(c, 0, 0, 8, 200, 0.80)
    e += _color_plate_accent2(c, 1072, 0, 8, 200, 0.80)
    return e

def recipe_D(c, biz):
    """Energy Burst — diagonal split + bold shapes + NEW badge"""
    e = ""
    e += _color_plate(c, "diagonal")
    e += _ring_frame(c, "dashed", 0.40, 760, c["accent"])
    e += _offer_badge(c, "جديد", "NEW")
    e += _watermark(c, "!", 400, c["accent2"])
    e += _color_shapes(c)
    # Add plus signs in accent2
    e += '<div style="position:absolute;top:160px;left:70px;width:40px;height:40px;z-index:2;">'
    e += '<div style="position:absolute;left:50%%;top:0;width:5px;height:100%%;background:%s;transform:translateX(-50%%);border-radius:3px;"></div>' % c["accent2"]
    e += '<div style="position:absolute;top:50%%;left:0;width:100%%;height:5px;background:%s;transform:translateY(-50%%);border-radius:3px;"></div></div>\n'
    e += '<div style="position:absolute;top:750px;left:960px;width:35px;height:35px;z-index:2;">'
    e += '<div style="position:absolute;left:50%%;top:0;width:4px;height:100%%;background:%s;transform:translateX(-50%%);border-radius:3px;"></div>' % c["accent2"]
    e += '<div style="position:absolute;top:50%%;left:0;width:100%%;height:4px;background:%s;transform:translateY(-50%%);border-radius:3px;"></div></div>\n'
    return e

def recipe_E(c, biz):
    """Elegant Minimal — subtle ring + accent2 touches"""
    e = ""
    e += _ring_frame(c, "solid", 0.20, 740, c["accent"])
    e += _corner_plate(c, "tl")
    e += _watermark(c, "✦", 300, c["accent2"])
    e += _color_shapes(c)
    e += _dots_line(c, 900, 130, 5, True)
    return e

RECIPES = {"A": recipe_A, "B": recipe_B, "C": recipe_C, "D": recipe_D, "E": recipe_E}

# ═══════════════════════════════════════════════════════
# MAIN TEMPLATE
# ═══════════════════════════════════════════════════════
def build_html(b64, biz, niche):
    c = NICHE_DATA[niche]
    recipe = c["recipe"]
    is_dark = c.get("is_dark", False)
    accent = c["accent"]
    accent2 = c["accent2"]
    bg = c["bg"]
    bg2 = c["bg2"]
    text_color = c["text"]
    t1, t2, t3 = biz["taglines"]
    rating = biz["rating"]
    reviews = _to_ar(biz["reviews"])
    trust = biz["trust"]
    grid_alpha = "0.06" if is_dark else "0.05"
    
    recipe_fn = RECIPES[recipe]
    recipe_html = recipe_fn(c, biz)
    
    html = """<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;700;900&family=Noto+Sans+Arabic:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:1080px; height:1080px; overflow:hidden; background:%s; font-family:'Noto Sans Arabic',sans-serif; -webkit-font-smoothing:antialiased; }
.stage { position:relative; width:1080px; height:1080px; overflow:hidden; background:%s; }
.stage::before { content:''; position:absolute; inset:0; z-index:0; pointer-events:none;
  background-image:linear-gradient(rgba(0,0,0,%s) 1px,transparent 1px),linear-gradient(90deg,rgba(0,0,0,%s) 1px,transparent 1px);
  background-size:45px 45px; }
.display { font-family:'Noto Kufi Arabic',serif; font-weight:900; line-height:1.2; direction:rtl; word-break:keep-all; text-shadow:0 2px 4px rgba(0,0,0,0.1); }
.label { font-family:'Lato',sans-serif; font-size:16px; font-weight:700; letter-spacing:0.25em; text-transform:uppercase; }
.pill { display:inline-block; background:%s; color:%s; padding:11px 26px; border-radius:50px; font-size:19px; font-weight:700; white-space:nowrap; box-shadow:0 6px 18px rgba(0,0,0,0.15); }
.stars { filter:drop-shadow(0 2px 4px rgba(0,0,0,0.1)); }
</style></head><body>
<div class="stage" data-niche="%s" data-recipe="%s">
  %s
  <div style="position:absolute;top:45px;left:0;right:0;padding:0 50px;text-align:right;z-index:10;">
    <span class="label" style="color:%s;">%s</span>
    <h1 class="display" style="font-size:58px;color:%s;margin-top:8px;">%s</h1>
    <div style="width:80px;height:4px;background:%s;border-radius:2px;margin-top:14px;opacity:0.8;"></div>
    <span style="font-family:'Noto Kufi Arabic',serif;font-size:24px;font-weight:500;color:%s;margin-top:8px;display:inline-block;">%s</span>
  </div>
  <div style="position:absolute;top:320px;left:50%%;transform:translateX(-50%%);width:680px;height:460px;border-radius:24px;overflow:hidden;z-index:10;box-shadow:0 40px 100px rgba(0,0,0,0.35),0 0 0 1px rgba(255,255,255,0.1);">
    <img src="data:image/jpeg;base64,%s" style="width:100%%;height:100%%;object-fit:cover;object-position:center;">
  </div>
  <div style="position:absolute;bottom:30px;left:0;right:0;padding:0 50px;display:flex;flex-direction:column;gap:14px;align-items:flex-end;z-index:10;">
    <div style="display:flex;gap:10px;flex-wrap:wrap;justify-content:flex-end;">
      <span class="pill">%s</span>
      <span class="pill">%s</span>
      <span class="pill">%s</span>
    </div>
    <div style="display:flex;align-items:center;gap:12px;direction:rtl;">
      <span class="stars" style="font-size:24px;color:%s;">★★★★<span style="opacity:0.3">★</span></span>
      <span style="font-size:30px;font-weight:900;color:%s;">%s</span>
      <span style="font-size:18px;color:%s;opacity:0.7;">%s تقييم</span>
    </div>
    <div style="font-size:16px;color:%s;opacity:0.8;">✦ %s</div>
    <div style="font-size:15px;color:%s;direction:rtl;opacity:0.6;">%s</div>
    <div style="display:flex;justify-content:space-between;align-items:center;width:100%%;gap:16px;padding-top:10px;border-top:1px solid %s;">
      <span style="font-family:'Noto Mono',monospace;font-size:16px;color:%s;opacity:0.6;">nuhoot.xyz</span>
      <span style="font-size:18px;color:%s;opacity:0.7;">نُهوت — التسويق الرقمي</span>
    </div>
  </div>
  <!-- CTA Button — bold accent2 color -->
  <div style="position:absolute;bottom:280px;left:50%%;transform:translateX(-50%%);z-index:12;
    background:%s;color:%s;padding:14px 40px;border-radius:50px;
    font-size:22px;font-weight:800;font-family:'Noto Sans Arabic',sans-serif;
    box-shadow:0 8px 25px rgba(0,0,0,0.2);white-space:nowrap;">
    ← %s
  </div>
</div>
</body></html>""" % (
        bg, bg, grid_alpha, grid_alpha,
        c["pill_bg"], c["pill_text"],
        niche, recipe,
        recipe_html,
        accent, biz["kicker"],
        text_color, biz["headline"],
        accent, accent2, biz["name"],
        b64,
        t1, t2, t3,
        accent, text_color, rating,
        accent, reviews,
        accent, trust,
        accent2, " ".join(biz.get("hashtags", [])),
        hex_rgba(accent, "0.2"),
        accent, accent,
        c["badge_bg"], c["badge_text"], biz.get("cta", "زورونا"),
    )
    return html

# ═══════════════════════════════════════════════════════
# RENDER
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    CHROMIUM = "/snap/chromium/current/usr/lib/chromium-browser/chrome"
    OUT = Path("/tmp/nuhoot-bold-v2")
    OUT.mkdir(exist_ok=True)
    
    niches = sorted(NICHE_DATA.keys())
    print("Rendering %d niches — COLOR PLATES + SAUDI SLANG..." % len(niches), flush=True)
    
    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            executable_path=CHROMIUM,
            args=["--no-sandbox","--disable-dev-shm-usage","--disable-gpu",
                  "--force-device-scale-factor=2","--hide-scrollbars"],
        )
        rendered, errors = 0, 0
        for niche in niches:
            c = NICHE_DATA[niche]
            
            # Use the REAL text engine — natural Saudi Arabic, 10 variants per niche
            text = generate_text(niche=niche, seed=0)
            biz = {
                "name": text["business_name"],
                "headline": text["headline"],
                "kicker": text["kicker"],
                "taglines": text["taglines"],
                "cta": text.get("cta", "زورونا"),
                "hashtags": text.get("hashtags", []),
                "trust": get_trust_badge(niche),
                "rating": text.get("rating", "٤٫٧"),
                "reviews": text.get("reviews", 200),
            }
            
            photo_path = best_photo(niche)
            if not photo_path:
                continue
            
            sq = square_crop(photo_path)
            sq_path = "/tmp/_boldv2_sq_%s.jpg" % niche
            sq.save(sq_path, quality=95)
            b64 = photo_b64(sq_path)
            
            html = build_html(b64, biz, niche)
            html_path = OUT / ("%s.html" % niche)
            html_path.write_text(html, encoding="utf-8")
            
            png_path = OUT / ("%s.png" % niche)
            try:
                page = browser.new_page(viewport={"width":1080,"height":1080})
                page.set_content(html)
                page.wait_for_timeout(2500)
                page.screenshot(path=str(png_path), type="png")
                page.close()
                rendered += 1
                print("  %s [Recipe %s]: %s (%dKB)" % (niche, c["recipe"], png_path, png_path.stat().st_size//1024), flush=True)
            except Exception as e:
                print("  ERROR %s: %s" % (niche, e), flush=True)
                errors += 1
        
        browser.close()
    
    print("\nDone! %d rendered, %d errors" % (rendered, errors), flush=True)
