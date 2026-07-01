import React from 'react';
import { AbsoluteFill, staticFile } from 'remotion';

// ─── Niche Configuration ────────────────────────────────────
const NICHE_DATA: Record<string, any> = {
  restaurants:   {bg:'#F5C518',bg2:'#E5A800',accent:'#1A1A1A',accent2:'#E63946',text:'#1A1A1A',isDark:false,badgeBg:'#E63946',badgeText:'#FFFFFF',recipe:'A',kicker:'RIYADH · FINE DINING',         rating:4.7, reviews:324, discount:'٢٠٪'},
  cafes:         {bg:'#6F4E37',bg2:'#5C3D2E',accent:'#F5DEB3',accent2:'#D4A055',text:'#FFF8E7',isDark:true, badgeBg:'#D4A055',badgeText:'#3E2723',recipe:'A',kicker:'RIYADH · COFFEE HOUSE',         rating:4.8, reviews:189, discount:'١٥٪'},
  bakeries:      {bg:'#FF8C42',bg2:'#E07B30',accent:'#3E2723',accent2:'#FFE082',text:'#FFFFFF',isDark:false,badgeBg:'#E63946',badgeText:'#FFFFFF',recipe:'E',kicker:'RIYADH · ARTISAN BAKERY',       rating:4.5, reviews:142, discount:''},
  salons:        {bg:'#1A1A2E',bg2:'#16213E',accent:'#E94560',accent2:'#D4AF37',text:'#FFFFFF',isDark:true, badgeBg:'#E94560',badgeText:'#FFFFFF',recipe:'E',kicker:'RIYADH · BEAUTY & STYLE',        rating:4.9, reviews:267, discount:''},
  spas:          {bg:'#2D4A3E',bg2:'#1E3328',accent:'#A8D5BA',accent2:'#E8C5A0',text:'#E8F5E9',isDark:true, badgeBg:'#A8D5BA',badgeText:'#1E3328',recipe:'E',kicker:'RIYADH · WELLNESS SPA',          rating:4.8, reviews:98,  discount:''},
  barbershops:   {bg:'#0F0F0F',bg2:'#1A1A1A',accent:'#D4AF37',accent2:'#C0392B',text:'#FFFFFF',isDark:true, badgeBg:'#D4AF37',badgeText:'#0F0F0F',recipe:'B',kicker:"RIYADH · GENTLEMEN'S GROOMING",  rating:4.6, reviews:203, discount:''},
  gyms:          {bg:'#121212',bg2:'#1A1A1A',accent:'#FF6B35',accent2:'#FFD93D',text:'#FFFFFF',isDark:true, badgeBg:'#FF6B35',badgeText:'#0A0A0A',recipe:'D',kicker:'RIYADH · STRENGTH & FITNESS',     rating:4.7, reviews:411, discount:''},
  clinics:       {bg:'#E8F4F8',bg2:'#D1ECF1',accent:'#2DB8A8',accent2:'#E63946',text:'#1E3A52',isDark:false,badgeBg:'#2DB8A8',badgeText:'#FFFFFF',recipe:'C',kicker:'RIYADH · EXPERT CARE',           rating:4.8, reviews:356, discount:''},
  dentists:      {bg:'#E8F4F8',bg2:'#D1ECF1',accent:'#00A8D5',accent2:'#FFD93D',text:'#1E3A52',isDark:false,badgeBg:'#00A8D5',badgeText:'#FFFFFF',recipe:'C',kicker:'RIYADH · DENTAL CARE',            rating:4.9, reviews:178, discount:''},
  pharmacies:    {bg:'#E8F5E9',bg2:'#C8E6C9',accent:'#2E7D32',accent2:'#FF8C42',text:'#1B5E20',isDark:false,badgeBg:'#2E7D32',badgeText:'#FFFFFF',recipe:'C',kicker:'RIYADH · PHARMACY',               rating:4.6, reviews:234, discount:'١٠٪'},
  dermatology:   {bg:'#FCE4EC',bg2:'#F8BBD0',accent:'#C2185B',accent2:'#7B1FA2',text:'#4A148C',isDark:false,badgeBg:'#C2185B',badgeText:'#FFFFFF',recipe:'B',kicker:'RIYADH · DERMATOLOGY',             rating:4.7, reviews:156, discount:''},
  fashion:       {bg:'#1A1A2E',bg2:'#16213E',accent:'#E94560',accent2:'#D4AF37',text:'#FFFFFF',isDark:true, badgeBg:'#E94560',badgeText:'#FFFFFF',recipe:'B',kicker:'RIYADH · FASHION HOUSE',            rating:4.8, reviews:312, discount:''},
  perfumes:      {bg:'#1A1A1A',bg2:'#2A2A2A',accent:'#D4AF37',accent2:'#8B4513',text:'#FFFFFF',isDark:true, badgeBg:'#D4AF37',badgeText:'#1A1A1A',recipe:'B',kicker:'RIYADH · LUXURY FRAGRANCES',       rating:4.9, reviews:87,  discount:'٢٥٪'},
  law_firms:     {bg:'#0E1428',bg2:'#161E38',accent:'#B8CCE0',accent2:'#D4AF37',text:'#E8EDF5',isDark:true, badgeBg:'#B8CCE0',badgeText:'#0E1428',recipe:'C',kicker:'RIYADH · LEGAL SERVICES',          rating:4.7, reviews:94,  discount:''},
  real_estate:   {bg:'#0E1428',bg2:'#161E38',accent:'#D4AF37',accent2:'#48CAE4',text:'#E8EDF5',isDark:true, badgeBg:'#D4AF37',badgeText:'#0E1428',recipe:'C',kicker:'RIYADH · REAL ESTATE',             rating:4.6, reviews:278, discount:''},
  auto_shops:    {bg:'#1A1A1A',bg2:'#2A2A2A',accent:'#FF6B35',accent2:'#FFD93D',text:'#FFFFFF',isDark:true, badgeBg:'#FF6B35',badgeText:'#1A1A1A',recipe:'D',kicker:'RIYADH · AUTO SERVICE',            rating:4.5, reviews:167, discount:''},
  car_wash:      {bg:'#0A1929',bg2:'#102A43',accent:'#48CAE4',accent2:'#80DEEA',text:'#FFFFFF',isDark:true, badgeBg:'#48CAE4',badgeText:'#0A1929',recipe:'D',kicker:'RIYADH · CAR CARE',               rating:4.4, reviews:121, discount:'١٥٪'},
  cleaning:      {bg:'#E8F5E9',bg2:'#C8E6C9',accent:'#4CAF50',accent2:'#29B6F6',text:'#1B5E20',isDark:false,badgeBg:'#4CAF50',badgeText:'#FFFFFF',recipe:'A',kicker:'RIYADH · CLEANING SERVICES',       rating:4.6, reviews:198, discount:'٢٠٪'},
  hvac_ac:       {bg:'#0A1929',bg2:'#102A43',accent:'#48CAE4',accent2:'#FFD93D',text:'#FFFFFF',isDark:true, badgeBg:'#48CAE4',badgeText:'#0A1929',recipe:'D',kicker:'RIYADH · HVAC SERVICES',          rating:4.5, reviews:76,  discount:'١٥٪'},
  event_halls:   {bg:'#2D1B3D',bg2:'#1A0F28',accent:'#D4AF37',accent2:'#E94560',text:'#FFFFFF',isDark:true, badgeBg:'#D4AF37',badgeText:'#2D1B3D',recipe:'B',kicker:'RIYADH · EVENT VENUE',             rating:4.8, reviews:143, discount:''},
  training_centers:{bg:'#0E1428',bg2:'#161E38',accent:'#5C6BC0',accent2:'#FFD93D',text:'#E8EDF5',isDark:true,badgeBg:'#5C6BC0',badgeText:'#FFFFFF',recipe:'C',kicker:'RIYADH · TRAINING CENTER',       rating:4.7, reviews:112, discount:'١٠٪'},

  drive_thru_coffee:        {bg:'#2D1B14',bg2:'#4E342E',accent:'#D4A373',accent2:'#F5E6D3',text:'#FFFFFF',isDark:true,badgeBg:'#D4A373',badgeText:'#FFFFFF',recipe:'A',kicker:'JEDDAH · DRIVE-THRU COFFEE',rating:4.7, reviews:150, discount:'18%'},
  pet_grooming:        {bg:'#FDF6EC',bg2:'#F5E6D3',accent:'#E07A5F',accent2:'#3D405B',text:'#1A1A1A',isDark:false,badgeBg:'#E07A5F',badgeText:'#1A1A1A',recipe:'D',kicker:'RIYADH · PET GROOMING',rating:4.7, reviews:150, discount:'18%'},
  desert_glamping:        {bg:'#F9F1DF',bg2:'#D2B48C',accent:'#8B5A2B',accent2:'#243A3A',text:'#1A1A1A',isDark:false,badgeBg:'#8B5A2B',badgeText:'#1A1A1A',recipe:'B',kicker:'الرياض · مخيمات صحراوية فاخرة',rating:4.7, reviews:150, discount:'18%'},
};

const TRUST_BADGES: Record<string, string> = {
  restaurants:'شهادة صحية معتمدة',cafes:'حبوب مختارة',bakeries:'مخبز معتمد',
  salons:'خبيرات معتمدات',spas:'منتجات طبيعية',barbershops:'أدوات معقمة',
  gyms:'مدربون معتمدون',clinics:'تراخيص وزارة الصحة',dentists:'عيادة مرخصة',
  pharmacies:'صيدلية مرخصة',dermatology:'أطباء متخصصون',fashion:'أقمشة فاخرة',
  perfumes:'عطور أصلية',law_firms:'محامون مرخصون',real_estate:'وساطة معتمدة',
  auto_shops:'فنيون محترفون',car_wash:'منظفات آمنة',cleaning:'منظفات صديقة للبيئة',
  hvac_ac:'فنيون معتمدون',event_halls:'قاعة مجهزة',training_centers:'معتمد رسمياً',
};

// ─── Helpers ────────────────────────────────────────────────
const hexRgba = (hex: string, alpha: string) => {
  const h = hex.replace('#', '');
  const r = parseInt(h.substring(0, 2), 16);
  const g = parseInt(h.substring(2, 4), 16);
  const b = parseInt(h.substring(4, 6), 16);
  return `rgba(${r},${g},${b},${alpha})`;
};

const toArabicDigits = (s: string | number) =>
  String(s).split('').map((ch: string) => ch.match(/\d/) ? '٠١٢٣٤٥٦٧٨٩'[parseInt(ch)] : ch).join('');

const optimalFontSize = (text: string, maxWidth: number, baseSize: number) => {
  if (!text) return baseSize;
  const estimated = text.length * baseSize * 0.55;
  if (estimated > maxWidth) {
    return Math.max(baseSize * 0.65, baseSize * (maxWidth / estimated));
  }
  return baseSize;
};

// Truncate CTA to a button-friendly length
const truncateCta = (cta: string, maxLen = 45) => {
  if (!cta) return '';
  if (cta.length <= maxLen) return cta;
  // Try to cut at a natural break
  const truncated = cta.substring(0, maxLen);
  const lastSpace = truncated.lastIndexOf(' ');
  if (lastSpace > maxLen * 0.6) {
    return truncated.substring(0, lastSpace) + '…';
  }
  return truncated + '…';
};

// ─── Star Rating Component (CSS-based, not text chars) ──────
const StarRating: React.FC<{rating: number, color: string, size?: number}> = ({rating, color, size = 18}) => {
  const fullStars = Math.floor(rating);
  const hasHalf = rating % 1 >= 0.5;
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: '2px'}}>
      {Array.from({length: 5}).map((_, i) => {
        const filled = i < fullStars;
        const half = i === fullStars && hasHalf;
        return (
          <svg key={i} width={size} height={size} viewBox="0 0 24 24" style={{display: 'block'}}>
            <path
              d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
              fill={filled || half ? color : 'none'}
              stroke={color}
              strokeWidth="1.5"
              fillOpacity={filled ? 1 : (half ? 0.5 : 0.15)}
            />
          </svg>
        );
      })}
    </div>
  );
};

// ─── Decorative Elements ────────────────────────────────────
const ColorShapes: React.FC<{c: any}> = ({c}) => {
  const a1 = c.accent, a2 = c.accent2;
  const mult = c.shapeOpacityMult ?? 1.0;
  const shapes = [
    {x:70,y:180,s:40,t:'circle',c:a2,o:0.85*mult},{x:980,y:160,s:45,t:'diamond',c:a1,o:0.80*mult},
    {x:50,y:440,s:30,t:'circle',c:a1,o:0.75*mult},{x:1010,y:420,s:35,t:'circle',c:a2,o:0.85*mult},
    {x:100,y:680,s:38,t:'diamond',c:a2,o:0.80*mult},{x:970,y:700,s:32,t:'circle',c:a1,o:0.75*mult},
    {x:130,y:880,s:25,t:'circle',c:a2,o:0.70*mult},{x:930,y:900,s:28,t:'diamond',c:a1,o:0.75*mult},
  ];
  return (<>
    {shapes.map((s, i) => (
      <div key={i} style={{
        position:'absolute', top:`${s.y}px`, left:`${s.x}px`,
        width:`${s.s}px`, height:`${s.s}px`,
        background:hexRgba(s.c, String(s.o)),
        borderRadius: s.t === 'circle' ? '50%' : '4px',
        transform: s.t === 'diamond' ? 'rotate(45deg)' : 'none',
      }}/>
    ))}
  </>);
};

const RingFrame: React.FC<{c:any,type:string,opacity:number,size:number,color?:string}> = ({c, type, opacity, size, color}) => {
  const col = color || c.accent;
  const top = 165 + (750 - size) / 2;
  const left = (1080 - size) / 2;
  const border = type === 'dashed'
    ? `4px dashed ${hexRgba(col, String(opacity))}`
    : `3px solid ${hexRgba(col, String(opacity))}`;
  return <div style={{position:'absolute',top:`${top}px`,left:`${left}px`,width:`${size}px`,height:`${size}px`,borderRadius:'50%',border}}/>;
};

const Watermark: React.FC<{c:any,text:string,fs:number,color?:string}> = ({c, text, fs, color}) => {
  const col = color || c.accent;
  return <div style={{position:'absolute',top:'50%',left:'50%',transform:'translate(-50%,-50%)',fontSize:`${fs}px`,fontWeight:900,fontFamily:'Noto Kufi Arabic,serif',color:hexRgba(col,'0.07'),lineHeight:1,pointerEvents:'none'}}>{text}</div>;
};

const ColorPlateBottom: React.FC<{c:any,h?:number}> = ({c, h=300}) => (
  <>
    <div style={{position:'absolute',bottom:0,left:0,right:0,height:`${h}px`,background:c.bg2}}/>
    <div style={{position:'absolute',bottom:`${h}px`,left:0,right:0,height:'100px',background:`linear-gradient(180deg,transparent 0%,${hexRgba(c.bg2,'0.5')} 50%,${c.bg2} 100%)`}}/>
  </>
);

const CornerPlate: React.FC<{c:any,corner:string}> = ({c, corner}) => {
  const pos = corner === 'tl' ? {top:'-100px',left:'-100px'} : {bottom:'-100px',right:'-100px'};
  return <div style={{position:'absolute',width:'250px',height:'250px',borderRadius:'50%',background:c.accent2,opacity:0.15,...pos}}/>;
};

const OfferBadge: React.FC<{c:any,discount?:string}> = ({c, discount}) => {
  if (!discount) return null;
  return (
    <div style={{
      position:'absolute',top:'230px',right:'140px',width:'180px',height:'180px',borderRadius:'50%',
      background:`linear-gradient(135deg,${c.badgeBg} 0%,${c.accent2} 100%)`,color:c.badgeText,
      display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center',
      boxShadow:'0 15px 40px rgba(0,0,0,0.3),0 5px 15px rgba(0,0,0,0.15)',
      border:`5px solid ${c.bg}`,transform:`rotate(${c.badgeRotation ?? -12}deg)`,zIndex:10,
    }}>
      <span style={{fontSize:'52px',fontWeight:900,lineHeight:1}}>{discount}</span>
      <span style={{fontSize:'20px',fontWeight:700,marginTop:'4px'}}>خصم</span>
      <span style={{fontSize:'13px',fontWeight:600,opacity:0.85,marginTop:'2px'}}>عرض خاص</span>
    </div>
  );
};

const NewBadge: React.FC<{c:any}> = ({c}) => (
  <div style={{
    position:'absolute',top:'230px',right:'140px',width:'160px',height:'160px',borderRadius:'50%',
    background:`linear-gradient(135deg,${c.badgeBg} 0%,${c.accent2} 100%)`,color:c.badgeText,
    display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center',
    boxShadow:'0 15px 40px rgba(0,0,0,0.3),0 5px 15px rgba(0,0,0,0.15)',
    border:`5px solid ${c.bg}`,transform:`rotate(${c.badgeRotation ?? -12}deg)`,zIndex:10,
  }}>
    <span style={{fontSize:'32px',fontWeight:900,lineHeight:1}}>جديد</span>
    <span style={{fontSize:'14px',fontWeight:600,opacity:0.85,marginTop:'4px'}}>عندنا الآن</span>
  </div>
);

const RecipeElements: React.FC<{c:any}> = ({c}) => {
  const r = c.recipe;
  const toAr = (s:string) => toArabicDigits(s);

  if (r === 'A') return (<>
    <ColorPlateBottom c={c} h={300}/>
    <Watermark c={c} text={toAr('20')} fs={400} color={c.accent2}/>
    <RingFrame c={c} type="dashed" opacity={0.35} size={760} color={c.accent}/>
    <RingFrame c={c} type="solid" opacity={0.12} size={720} color={c.accent2}/>
    <CornerPlate c={c} corner="tl"/>
    <OfferBadge c={c} discount={c.discount || '٢٠٪'}/>
    <ColorShapes c={c}/>
  </>);
  if (r === 'B') return (<>
    <RingFrame c={c} type="solid" opacity={0.25} size={760} color={c.accent}/>
    <RingFrame c={c} type="solid" opacity={0.10} size={720} color={c.accent2}/>
    <CornerPlate c={c} corner="tl"/>
    <CornerPlate c={c} corner="br"/>
    <Watermark c={c} text="★" fs={350} color={c.accent2}/>
    <ColorShapes c={c}/>
  </>);
  if (r === 'C') return (<>
    <ColorPlateBottom c={c} h={280}/>
    <RingFrame c={c} type="solid" opacity={0.20} size={740} color={c.accent}/>
    <Watermark c={c} text="★★★★★" fs={200} color={c.accent2}/>
    <ColorShapes c={c}/>
  </>);
  if (r === 'D') return (<>
    <div style={{position:'absolute',top:0,left:0,width:'100%',height:'55%',background:c.bg2,clipPath:'polygon(0 0,100% 0,100% 65%,0 100%)'}}/>
    <RingFrame c={c} type="dashed" opacity={0.40} size={760} color={c.accent}/>
    <NewBadge c={c}/>
    <Watermark c={c} text="!" fs={400} color={c.accent2}/>
    <ColorShapes c={c}/>
  </>);
  if (r === 'E') return (<>
    <RingFrame c={c} type="solid" opacity={0.20} size={740} color={c.accent}/>
    <CornerPlate c={c} corner="tl"/>
    <Watermark c={c} text="+" fs={300} color={c.accent2}/>
    <ColorShapes c={c}/>
  </>);
  return null;
};

// ─── Main Nuhoot Post Component ─────────────────────────────
export interface DesignOverrides {
  bg?: string;
  bg2?: string;
  accent?: string;
  accent2?: string;
  text?: string;
  badgeBg?: string;
  badgeText?: string;
  bodyOpacity?: number;
  hashtagOpacity?: number;
  hashtagColor?: string;
  ctaArrow?: string;
  badgeRotation?: number;
  shapeOpacityMult?: number;
  gridAlpha?: number;
  headlineBaseSize?: number;
}

export interface NuhootPostProps {
  niche: string;
  headline: string;
  name: string;
  taglines: string[];
  hashtags: string[];
  cta: string;
  photoPath: string;
  designOverrides?: DesignOverrides;
}

export const NuhootPost: React.FC<NuhootPostProps> = ({
  niche, headline, name, taglines, hashtags, cta, photoPath, designOverrides,
}) => {
  const baseConfig = NICHE_DATA[niche];
  if (!baseConfig) return null;
  const dO = designOverrides || {};
  const c = { ...baseConfig, ...(dO.bg ? { bg: dO.bg } : {}),
    ...(dO.bg2 ? { bg2: dO.bg2 } : {}),
    ...(dO.accent ? { accent: dO.accent } : {}),
    ...(dO.accent2 ? { accent2: dO.accent2 } : {}),
    ...(dO.text ? { text: dO.text } : {}),
    ...(dO.badgeBg ? { badgeBg: dO.badgeBg } : {}),
    ...(dO.badgeText ? { badgeText: dO.badgeText } : {}),
  };

  const trust = TRUST_BADGES[niche] || 'معتمد';
  const headlineSize = optimalFontSize(headline, 850, dO.headlineBaseSize ?? 44);
  const shortCta = truncateCta(cta);
  const ctaSize = optimalFontSize(shortCta, 500, 20);
  const bgGradient = `linear-gradient(135deg, ${c.bg} 0%, ${c.bg2} 100%)`;
  const ctaGradient = `linear-gradient(135deg, ${c.badgeBg} 0%, ${c.accent2} 100%)`;
  const gridAlpha = dO.gridAlpha ?? (c.isDark ? 0.06 : 0.05);
  const bodyOpacity = dO.bodyOpacity ?? 0.92;
  const hashtagOpacity = dO.hashtagOpacity ?? 0.75;
  const hashtagColor = dO.hashtagColor ?? c.accent2;
  const ctaArrow = dO.ctaArrow !== undefined ? dO.ctaArrow : '←';
  const badgeRotation = dO.badgeRotation ?? -12;
  const shapeOpacityMult = dO.shapeOpacityMult ?? 1.0;
  // Inject override values into c so sub-components can use them
  c.badgeRotation = badgeRotation;
  c.shapeOpacityMult = shapeOpacityMult;
  const [t1, t2, t3] = taglines;

  // Subtle glow for dark themes to improve readability
  const glowOverlay = c.isDark ? (
    <div style={{
      position: 'absolute', inset: 0, pointerEvents: 'none',
      background: `radial-gradient(ellipse at 50% 30%, ${hexRgba(c.accent, '0.08')} 0%, transparent 60%)`,
    }}/>
  ) : null;

  const photoUrl = photoPath ? staticFile(photoPath) : '';

  return (
    <AbsoluteFill style={{
      background: bgGradient,
      fontFamily: 'Noto Sans Arabic, sans-serif',
      direction: 'rtl',
      textAlign: 'right',
      display: 'flex',
      flexDirection: 'column',
      overflow: 'hidden',
    }}>
      {/* Grid background */}
      <div style={{
        position: 'absolute', inset: 0, pointerEvents: 'none',
        backgroundImage: `linear-gradient(rgba(255,255,255,${gridAlpha}) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,${gridAlpha}) 1px,transparent 1px)`,
        backgroundSize: '45px 45px',
      }}/>

      {/* Glow overlay for dark themes */}
      {glowOverlay}

      {/* Decorative recipe elements */}
      <RecipeElements c={c}/>

      {/* Header: Kicker + Headline + Business Name */}
      <div style={{
        display: 'flex', flexDirection: 'column', alignItems: 'flex-end',
        padding: '40px 50px 0 50px', flexShrink: 0,
        direction: 'rtl', textAlign: 'right',
        zIndex: 5,
      }}>
        <span style={{
          fontFamily: 'Lato, sans-serif', fontSize: '15px', fontWeight: 700,
          letterSpacing: '0.25em', color: c.accent, textTransform: 'uppercase',
          direction: 'ltr', textAlign: 'left',
        }}>{c.kicker}</span>
        <h1 style={{
          fontFamily: 'Noto Kufi Arabic, serif', fontSize: `${headlineSize}px`,
          fontWeight: 900, color: c.text, marginTop: '8px', lineHeight: 1.25,
          direction: 'rtl', textAlign: 'right', margin: '8px 0 0 0',
          textShadow: c.isDark ? '0 2px 12px rgba(0,0,0,0.5)' : '0 2px 8px rgba(255,255,255,0.4)',
        }}>{headline}</h1>
        <div style={{
          width: '70px', height: '3px', borderRadius: '2px', marginTop: '12px', opacity: 0.9,
          background: `linear-gradient(90deg, ${c.accent}, ${c.accent2})`,
        }}/>
        <span style={{
          fontFamily: 'Noto Kufi Arabic, serif', fontSize: '20px', fontWeight: 500,
          color: c.accent2, marginTop: '8px', direction: 'rtl',
        }}>{name}</span>
      </div>

      {/* Photo */}
      {photoUrl && (
        <div style={{
          display: 'flex', justifyContent: 'center', alignItems: 'center',
          marginTop: '20px', flexShrink: 0, zIndex: 5,
        }}>
          <div style={{
            width: '620px', height: '370px', borderRadius: '24px', overflow: 'hidden',
            boxShadow: '0 25px 60px rgba(0,0,0,0.35), 0 0 0 2px rgba(255,255,255,0.08)',
          }}>
            <img src={photoUrl} style={{width: '100%', height: '100%', objectFit: 'cover'}}/>
          </div>
        </div>
      )}

      {/* Body text + CTA */}
      <div style={{
        display: 'flex', flexDirection: 'column', alignItems: 'flex-end',
        padding: '20px 50px 0 50px', gap: '16px', flexShrink: 0,
        direction: 'rtl', textAlign: 'right',
        zIndex: 5,
      }}>
        <div style={{
          display: 'flex', flexDirection: 'column', alignItems: 'flex-end',
          maxWidth: '700px', color: c.text, opacity: bodyOpacity, fontSize: '19px',
          fontFamily: 'Noto Sans Arabic, sans-serif', lineHeight: 1.6,
          textAlign: 'right', direction: 'rtl', gap: '4px',
        }}>
          {t1 && <div>{t1}</div>}
          {t2 && <div>{t2}</div>}
          {t3 && <div>{t3}</div>}
        </div>
        <div style={{
          background: ctaGradient, color: c.badgeText,
          padding: '14px 40px', borderRadius: '50px',
          fontSize: `${ctaSize}px`, fontWeight: 800,
          boxShadow: '0 8px 25px rgba(0,0,0,0.25), 0 0 0 1px rgba(255,255,255,0.12)',
          direction: 'rtl', textAlign: 'center',
          maxWidth: '560px',
        }}>{ctaArrow ? `${ctaArrow} ${shortCta}` : shortCta}</div>
      </div>

      {/* Footer: Rating + Trust + Hashtags */}
      <div style={{
        display: 'flex', flexDirection: 'column', alignItems: 'flex-end',
        padding: '10px 50px 25px 50px', gap: '8px', marginTop: 'auto',
        direction: 'rtl', textAlign: 'right',
        zIndex: 5,
      }}>
        <div style={{display: 'flex', alignItems: 'center', gap: '10px', direction: 'rtl'}}>
          <StarRating rating={c.rating} color={c.accent} size={18}/>
          <span style={{fontSize: '26px', fontWeight: 900, color: c.text}}>
            {toArabicDigits(c.rating.toFixed(1).replace('.', '٫'))}
          </span>
          <span style={{fontSize: '14px', color: c.text, opacity: 0.7}}>
            {toArabicDigits(c.reviews)} تقييم
          </span>
        </div>
        <div style={{
          display: 'inline-flex', alignItems: 'center', gap: '6px',
          fontSize: '14px', color: c.accent, opacity: 0.9, direction: 'rtl',
          background: hexRgba(c.accent, '0.12'),
          padding: '4px 14px', borderRadius: '20px',
        }}>
          <span>✦</span> {trust}
        </div>
        <div style={{
          fontSize: '13px', color: hashtagColor, direction: 'rtl', opacity: hashtagOpacity,
          fontFamily: 'Noto Sans Arabic, sans-serif',
        }}>{hashtags.join('  ')}</div>
        <div style={{
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          width: '100%', gap: '16px', paddingTop: '8px',
          borderTop: `1px solid ${hexRgba(c.accent, '0.25')}`,
        }}>
          <span style={{fontFamily: 'monospace', fontSize: '13px', color: c.accent, opacity: 0.8, direction: 'ltr'}}>nuhoot.xyz</span>
          <span style={{fontSize: '15px', color: c.accent, opacity: 0.9, direction: 'rtl', fontWeight: 600}}>نُهوت — التسويق الرقمي</span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
