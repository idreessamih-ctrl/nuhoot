// ─────────────────────────────────────────────────────────────────────
// Nuhoot Design Engine — Shared Helpers, Types & Primitives
// ─────────────────────────────────────────────────────────────────────
// Expanded with 47 design techniques from professional research:
//   - Expanded ColorConfig (light/core/deep/glint variants)
//   - Noto Naskh Arabic font for traditional niches
//   - depthShadow() multi-layer shadow system
//   - accentShadow() colored shadow tinted with niche color
//   - GlassCard glassmorphism wrapper
//   - GoldFoilText metallic gold text effect
//   - typeScale() modular type ratio per niche
//   - gradientText() gradient clip on text
// ─────────────────────────────────────────────────────────────────────

import React from 'react';
import { staticFile } from 'remotion';

// ─── Expanded Color Configuration ─────────────────────────────────────
// Now includes light/core/deep/glint variants for full palette control.
export interface ColorConfig {
  bg: string;
  bg2: string;
  accent: string;
  accent2: string;
  text: string;
  isDark: boolean;
  badgeBg: string;
  badgeText: string;
  // Expanded palette variants (Technique 2.1)
  accentLight?: string;   // lighter shade of accent
  accentDeep?: string;    // deeper shade of accent
  accentGlint?: string;   // shimmer/highlight color
  gradientAngle?: number; // preferred gradient angle per niche (Technique 2.2)
}

// Neutral default so components never crash if colors are omitted.
export const DEFAULT_COLORS: ColorConfig = {
  bg: '#1A1A2E',
  bg2: '#16213E',
  accent: '#E94560',
  accent2: '#D4AF37',
  text: '#FFFFFF',
  isDark: true,
  badgeBg: '#E94560',
  badgeText: '#FFFFFF',
  accentLight: '#FF6B8A',
  accentDeep: '#B8334E',
  accentGlint: '#FFD700',
  gradientAngle: 135,
};

// ─── Base Block Props ─────────────────────────────────────────────────
export interface BaseBlockProps {
  colors?: ColorConfig;
  style?: React.CSSProperties;
}

export const useColors = (colors?: ColorConfig): ColorConfig =>
  colors ?? DEFAULT_COLORS;

// ─── hex → rgba ───────────────────────────────────────────────────────
export const hexRgba = (hex: string, alpha: string): string => {
  const h = hex.replace('#', '');
  const r = parseInt(h.substring(0, 2), 16);
  const g = parseInt(h.substring(2, 4), 16);
  const b = parseInt(h.substring(4, 6), 16);
  return `rgba(${r},${g},${b},${alpha})`;
};

// ─── hex lighten/darken ────────────────────────────────────────────────
// Lighten or darken a hex color by a percentage (-100 to 100).
export const hexShift = (hex: string, percent: number): string => {
  const h = hex.replace('#', '');
  const r = parseInt(h.substring(0, 2), 16);
  const g = parseInt(h.substring(2, 4), 16);
  const b = parseInt(h.substring(4, 6), 16);
  const amt = Math.round(2.55 * percent);
  const clamp = (v: number) => Math.max(0, Math.min(255, v));
  const nr = clamp(r + amt);
  const ng = clamp(g + amt);
  const nb = clamp(b + amt);
  return `#${nr.toString(16).padStart(2, '0')}${ng.toString(16).padStart(2, '0')}${nb.toString(16).padStart(2, '0')}`;
};

// ─── Arabic Digit Conversion ──────────────────────────────────────────
export const toArabicDigits = (s: string | number): string =>
  String(s)
    .split('')
    .map((ch: string) => (ch.match(/\d/) ? '٠١٢٣٤٥٦٧٨٩'[parseInt(ch)] : ch))
    .join('');

// ─── Auto-fit Font Size ───────────────────────────────────────────────
export const optimalFontSize = (
  text: string,
  maxWidth: number,
  baseSize: number,
): number => {
  if (!text) return baseSize;
  const estimated = text.length * baseSize * 0.55;
  if (estimated > maxWidth) {
    return Math.max(baseSize * 0.65, baseSize * (maxWidth / estimated));
  }
  return baseSize;
};

// ─── CTA Truncation ───────────────────────────────────────────────────
export const truncateCta = (cta: string, maxLen = 45): string => {
  if (!cta) return '';
  if (cta.length <= maxLen) return cta;
  const truncated = cta.substring(0, maxLen);
  const lastSpace = truncated.lastIndexOf(' ');
  if (lastSpace > maxLen * 0.6) {
    return truncated.substring(0, lastSpace) + '…';
  }
  return truncated + '…';
};

// ─── RTL Detection ────────────────────────────────────────────────────
export interface RTLInfo {
  direction: 'rtl' | 'ltr';
  textAlign: 'right' | 'left' | 'center';
  isArabic: boolean;
}

export const rtlProps = (text?: string): RTLInfo => {
  const isArabic = /[\u0600-\u06FF]/.test(text || '');
  return {
    direction: isArabic ? 'rtl' : 'ltr',
    textAlign: isArabic ? 'right' : 'left',
    isArabic,
  };
};

// ─── Photo Resolution ────────────────────────────────────────────────
export const resolvePhoto = (path: string): string => {
  if (!path) return '';
  if (/^(https?:|data:|blob:)/.test(path)) return path;
  return staticFile(path);
};

// ─── Expanded Font Stacks (Technique 1.2) ─────────────────────────────
// Added NotoNaskhArabic for traditional niches (perfumes, law_firms, etc.)
export const FONTS = {
  sans: 'Noto Sans Arabic, sans-serif',
  kufi: 'Noto Kufi Arabic, serif',
  naskh: 'Noto Naskh Arabic, serif',
  lato: 'Lato, sans-serif',
} as const;

// ─── Type Scale System (Technique 1.1) ───────────────────────────────
// Modular type ratios per niche. Returns scaled sizes from a base.
// Ratios: 1.200 (minor third), 1.250 (major third), 1.333 (perfect fourth),
//         1.414 (augmented fourth), 1.500 (perfect fifth), 1.618 (golden)
export const typeScale = (
  base: number,
  ratio: number,
  steps: number = 3,
): number[] => {
  const sizes: number[] = [];
  for (let i = 0; i <= steps; i++) {
    sizes.push(Math.round(base * Math.pow(ratio, i)));
  }
  return sizes;
};

// ─── Multi-Layer Shadow System (Technique 4.1) ───────────────────────
// Returns a compound boxShadow with 3 layers for realistic depth.
export const depthShadow = (
  intensity: 'subtle' | 'medium' | 'deep' | 'floating' = 'medium',
): string => {
  const presets = {
    subtle: '0 2px 8px rgba(0,0,0,0.12), 0 4px 16px rgba(0,0,0,0.08), 0 1px 3px rgba(0,0,0,0.1)',
    medium: '0 8px 24px rgba(0,0,0,0.25), 0 16px 48px rgba(0,0,0,0.15), 0 2px 8px rgba(0,0,0,0.12)',
    deep: '0 20px 60px rgba(0,0,0,0.4), 0 12px 32px rgba(0,0,0,0.25), 0 4px 12px rgba(0,0,0,0.15)',
    floating: '0 30px 80px rgba(0,0,0,0.45), 0 20px 50px rgba(0,0,0,0.3), 0 8px 20px rgba(0,0,0,0.2)',
  };
  return presets[intensity];
};

// ─── Colored Accent Shadow (Technique 4.4) ───────────────────────────
// Shadow tinted with the niche's accent color instead of black.
export const accentShadow = (
  accentColor: string,
  intensity: 'subtle' | 'medium' | 'strong' = 'medium',
): string => {
  const opacity = { subtle: '0.15', medium: '0.3', strong: '0.5' };
  return `0 12px 40px ${hexRgba(accentColor, opacity[intensity])}, 0 4px 12px ${hexRgba(accentColor, '0.2')}, 0 2px 6px rgba(0,0,0,0.15)`;
};

// ─── Glassmorphism Card (Technique 4.2) ─────────────────────────────
// Frosted glass effect with backdrop blur, semi-transparent bg, and border.
export interface GlassCardProps {
  children?: React.ReactNode;
  style?: React.CSSProperties;
  /** Blur amount in px. Default 20. */
  blur?: number;
  /** Background opacity. Default 0.08. */
  opacity?: number;
  /** Border color (defaults to accent). */
  borderColor?: string;
  /** Border opacity. Default 0.2. */
  borderOpacity?: number;
  /** Border radius. Default 20. */
  radius?: number;
}

export const GlassCard: React.FC<GlassCardProps> = ({
  children,
  style,
  blur = 20,
  opacity = 0.08,
  borderColor,
  borderOpacity = 0.2,
  radius = 20,
}) => {
  const borderCol = borderColor || '#FFFFFF';
  return (
    <div
      style={{
        background: `rgba(255,255,255,${opacity})`,
        backdropFilter: `blur(${blur}px)`,
        WebkitBackdropFilter: `blur(${blur}px)`,
        border: `1px solid ${hexRgba(borderCol, String(borderOpacity))}`,
        borderRadius: `${radius}px`,
        boxShadow: '0 8px 32px rgba(0,0,0,0.15), inset 0 1px 0 rgba(255,255,255,0.1)',
        ...style,
      }}
    >
      {children}
    </div>
  );
};

// ─── Gold Foil Text Effect (Technique 10.3) ─────────────────────────
// Metallic gold gradient applied as text fill.
export const goldFoilTextStyle = (): React.CSSProperties => ({
  background: 'linear-gradient(135deg, #8C6A2E 0%, #C9A25A 25%, #FBEFC0 50%, #C9A25A 75%, #8C6A2E 100%)',
  WebkitBackgroundClip: 'text',
  WebkitTextFillColor: 'transparent',
  backgroundClip: 'text',
  WebkitTextStroke: '0.5px rgba(201,162,90,0.3)',
});

// ─── Gradient Text (Technique 2.6) ──────────────────────────────────
// Apply a gradient as text fill for headlines.
export const gradientTextStyle = (
  color1: string,
  color2: string,
): React.CSSProperties => ({
  background: `linear-gradient(135deg, ${color1} 0%, ${color2} 100%)`,
  WebkitBackgroundClip: 'text',
  WebkitTextFillColor: 'transparent',
  backgroundClip: 'text',
});

// ─── Photo Gradient Overlay (Technique 4.3) ─────────────────────────
// Returns a gradient overlay for photos — dark at bottom for legibility.
export const photoOverlayStyle = (
  overlayColor: string = '#000000',
  opacity: number = 0.4,
): React.CSSProperties => ({
  position: 'absolute',
  inset: 0,
  background: `linear-gradient(180deg, transparent 0%, transparent 40%, ${hexRgba(overlayColor, String(opacity * 0.5))} 70%, ${hexRgba(overlayColor, String(opacity))} 100%)`,
  pointerEvents: 'none',
});

// ─── Vignette Effect (Technique 4.8) ────────────────────────────────
// Radial darkening at edges for cinematic depth.
export const vignetteStyle = (
  color: string = '#000000',
  intensity: number = 0.4,
): React.CSSProperties => ({
  position: 'absolute',
  inset: 0,
  background: `radial-gradient(ellipse at center, transparent 30%, ${hexRgba(color, String(intensity))} 100%)`,
  pointerEvents: 'none',
});

// ─── Inner Glow (Technique 4.7) ────────────────────────────────────
// Inset glow effect for buttons and cards.
export const innerGlowStyle = (
  glowColor: string,
  intensity: 'subtle' | 'medium' | 'strong' = 'medium',
): React.CSSProperties => {
  const blur = { subtle: 6, medium: 12, strong: 20 };
  const alpha = { subtle: '0.1', medium: '0.25', strong: '0.4' };
  return {
    boxShadow: `inset 0 0 ${blur[intensity]}px ${hexRgba(glowColor, alpha[intensity])}`,
  };
};

// ─── Star Rating (SVG-based) ─────────────────────────────────────────
export const StarRating: React.FC<{
  rating: number;
  color: string;
  size?: number;
  style?: React.CSSProperties;
}> = ({ rating, color, size = 18, style }) => {
  const fullStars = Math.floor(rating);
  const hasHalf = rating % 1 >= 0.5;
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '2px', ...style }}>
      {Array.from({ length: 5 }).map((_, i) => {
        const filled = i < fullStars;
        const half = i === fullStars && hasHalf;
        return (
          <svg
            key={i}
            width={size}
            height={size}
            viewBox="0 0 24 24"
            style={{ display: 'block' }}
          >
            <path
              d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
              fill={filled || half ? color : 'none'}
              stroke={color}
              strokeWidth="1.5"
              fillOpacity={filled ? 1 : half ? 0.5 : 0.15}
            />
          </svg>
        );
      })}
    </div>
  );
};
