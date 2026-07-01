// ─────────────────────────────────────────────────────────────────────
// BADGES — 6 components (4 original + 2 new)
//   StatusBadge   · pill-shaped status indicator
//   RatingBadge   · star rating in a badge
//   TrustBadge    · shield/badge with text
//   DiscountBadge · circular discount percentage badge
//   ── NEW ──
//   SealBadge     · circular stamp/seal badge (Technique 10.6)
//   OfferRibbon   · diagonal offer/discount ribbon (Technique 10.8)
// ─────────────────────────────────────────────────────────────────────

import React from 'react';
import { BaseBlockProps, ColorConfig, FONTS, StarRating, hexRgba, toArabicDigits, useColors } from './helpers';
import { Icon } from './icon';

// ─── StatusBadge ──────────────────────────────────────────────────────
export interface StatusBadgeProps extends BaseBlockProps {
  text: string;
  iconName?: string;
  badgeColor?: string;
  size?: 'sm' | 'md' | 'lg';
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  text,
  iconName = 'check',
  badgeColor,
  size = 'md',
  colors,
  style,
}) => {
  const c = useColors(colors);
  const col = badgeColor ?? c.accent;
  const fontSizes = { sm: '12px', md: '14px', lg: '16px' };
  const iconSizes = { sm: 14, md: 16, lg: 20 };
  const padding = { sm: '4px 10px', md: '6px 14px', lg: '8px 18px' };

  return (
    <div
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '6px',
        background: hexRgba(col, '0.12'),
        border: `1px solid ${hexRgba(col, '0.3')}`,
        borderRadius: '20px',
        padding: padding[size],
        fontFamily: FONTS.sans,
        fontSize: fontSizes[size],
        fontWeight: 600,
        color: col,
        direction: 'rtl',
        ...style,
      }}
    >
      <Icon name={iconName} size={iconSizes[size]} color={col} colors={c} />
      <span>{text}</span>
    </div>
  );
};

// ─── RatingBadge ──────────────────────────────────────────────────────
export interface RatingBadgeProps extends BaseBlockProps {
  rating: number;
  reviews?: number;
  starSize?: number;
}

export const RatingBadge: React.FC<RatingBadgeProps> = ({
  rating,
  reviews,
  starSize = 16,
  colors,
  style,
}) => {
  const c = useColors(colors);

  return (
    <div
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '8px',
        background: hexRgba(c.accent, '0.1'),
        border: `1px solid ${hexRgba(c.accent, '0.2')}`,
        borderRadius: '16px',
        padding: '8px 16px',
        direction: 'rtl',
        ...style,
      }}
    >
      <StarRating rating={rating} color={c.accent} size={starSize} />
      <span style={{ fontFamily: FONTS.kufi, fontSize: '18px', fontWeight: 800, color: c.text }}>
        {toArabicDigits(rating.toFixed(1).replace('.', '٫'))}
      </span>
      {reviews != null && (
        <span style={{ fontFamily: FONTS.sans, fontSize: '13px', color: c.text, opacity: 0.7 }}>
          ({toArabicDigits(reviews)})
        </span>
      )}
    </div>
  );
};

// ─── TrustBadge ───────────────────────────────────────────────────────
export interface TrustBadgeProps extends BaseBlockProps {
  text: string;
  iconName?: string;
  showShield?: boolean;
}

export const TrustBadge: React.FC<TrustBadgeProps> = ({
  text,
  iconName = 'shield',
  showShield = true,
  colors,
  style,
}) => {
  const c = useColors(colors);

  return (
    <div
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '8px',
        padding: '8px 18px',
        borderRadius: '12px',
        background: `linear-gradient(135deg, ${hexRgba(c.accent, '0.15')}, ${hexRgba(c.accent2, '0.1')})`,
        border: `1px solid ${hexRgba(c.accent, '0.25')}`,
        direction: 'rtl',
        ...style,
      }}
    >
      {showShield && <Icon name={iconName} size={18} color={c.accent} colors={c} />}
      <span style={{ fontFamily: FONTS.kufi, fontSize: '14px', fontWeight: 700, color: c.accent2 }}>
        {text}
      </span>
    </div>
  );
};

// ─── DiscountBadge ────────────────────────────────────────────────────
export interface DiscountBadgeProps extends BaseBlockProps {
  percentage: number;
  size?: number;
  rotation?: number;
}

export const DiscountBadge: React.FC<DiscountBadgeProps> = ({
  percentage,
  size = 80,
  rotation = -15,
  colors,
  style,
}) => {
  const c = useColors(colors);

  return (
    <div
      style={{
        width: `${size}px`,
        height: `${size}px`,
        borderRadius: '50%',
        background: `linear-gradient(135deg, ${c.accent}, ${c.accent2})`,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        transform: `rotate(${rotation}deg)`,
        boxShadow: '0 8px 25px rgba(0,0,0,0.3)',
        border: `3px solid ${c.badgeText}`,
        flexShrink: 0,
        ...style,
      }}
    >
      <span style={{ fontFamily: FONTS.kufi, fontSize: `${size * 0.35}px`, fontWeight: 900, color: c.badgeText, lineHeight: 1 }}>
        {toArabicDigits(percentage)}%
      </span>
      <span style={{ fontFamily: FONTS.sans, fontSize: `${size * 0.14}px`, color: c.badgeText, opacity: 0.9, marginTop: '2px' }}>
        خصم
      </span>
    </div>
  );
};

// ═════════════════════════════════════════════════════════════════════
// NEW BADGE COMPONENTS
// ═════════════════════════════════════════════════════════════════════

// ─── SealBadge (Technique 10.6) — Circular stamp/seal ────────────────
export interface SealBadgeProps extends BaseBlockProps {
  /** Main text inside the seal. */
  text: string;
  /** Sub text (small line below). */
  subText?: string;
  /** Diameter in px. Default 100. */
  size?: number;
  /** Rotation. Default -8. */
  rotation?: number;
  /** Show double border. Default true. */
  doubleBorder?: boolean;
}

export const SealBadge: React.FC<SealBadgeProps> = ({
  text,
  subText,
  size = 100,
  rotation = -8,
  doubleBorder = true,
  colors,
  style,
}) => {
  const c = useColors(colors);

  return (
    <div
      style={{
        width: `${size}px`,
        height: `${size}px`,
        borderRadius: '50%',
        background: c.isDark ? hexRgba(c.accent2, '0.1') : hexRgba(c.accent, '0.05'),
        border: `2px solid ${c.accent2}`,
        ...(doubleBorder ? { boxShadow: `inset 0 0 0 3px ${hexRgba(c.accent2, '0.2')}, 0 4px 15px rgba(0,0,0,0.2)` } : { boxShadow: '0 4px 15px rgba(0,0,0,0.2)' }),
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        transform: `rotate(${rotation}deg)`,
        flexShrink: 0,
        ...style,
      }}
    >
      {/* Dotted outer ring */}
      <div style={{
        position: 'absolute',
        width: `${size - 10}px`,
        height: `${size - 10}px`,
        borderRadius: '50%',
        border: `1px dashed ${hexRgba(c.accent2, '0.4')}`,
      }} />
      <span style={{
        fontFamily: FONTS.kufi,
        fontSize: `${size * 0.16}px`,
        fontWeight: 900,
        color: c.accent2,
        textAlign: 'center',
        lineHeight: 1.2,
        direction: 'rtl',
      }}>
        {text}
      </span>
      {subText && (
        <span style={{
          fontFamily: FONTS.sans,
          fontSize: `${size * 0.09}px`,
          color: c.accent2,
          opacity: 0.7,
          marginTop: '2px',
        }}>
          {subText}
        </span>
      )}
    </div>
  );
};

// ─── OfferRibbon (Technique 10.8) — Diagonal offer/discount ribbon ────
export interface OfferRibbonProps extends BaseBlockProps {
  /** Ribbon text. */
  text: string;
  /** Position. Default 'top-right'. */
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left';
  /** Ribbon width. Default 200. */
  width?: number;
  /** Color override. Default accent. */
  color?: string;
}

export const OfferRibbon: React.FC<OfferRibbonProps> = ({
  text,
  position = 'top-right',
  width = 200,
  color,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const col = color ?? c.accent;

  const posStyle: React.CSSProperties = {
    position: 'absolute',
    ...(position === 'top-right'
      ? { top: '30px', right: '-40px', transform: 'rotate(45deg)' }
      : position === 'top-left'
        ? { top: '30px', left: '-40px', transform: 'rotate(-45deg)' }
        : position === 'bottom-right'
          ? { bottom: '30px', right: '-40px', transform: 'rotate(-45deg)' }
          : { bottom: '30px', left: '-40px', transform: 'rotate(45deg)' }),
    zIndex: 20,
  };

  return (
    <div
      style={{
        ...posStyle,
        width: `${width}px`,
        padding: '8px 0',
        background: col,
        textAlign: 'center',
        fontFamily: FONTS.kufi,
        fontSize: '14px',
        fontWeight: 800,
        color: c.badgeText,
        boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
        clipPath: 'polygon(0 0, 100% 0, 95% 50%, 100% 100%, 0 100%, 5% 50%)',
        ...style,
      }}
    >
      {text}
    </div>
  );
};
