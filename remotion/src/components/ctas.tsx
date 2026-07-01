// ─────────────────────────────────────────────────────────────────────
// CTAs (Call-to-Action) — 4 components (all MODIFIED with depth, glow)
//   CTAButton   · pill button (MODIFIED: colored shadow, inner glow)
//   CTABanner    · full-width banner (MODIFIED: depth shadow)
//   CTAFloating  · floating action button (MODIFIED: accent shadow)
//   CTAInline    · inline text link (MODIFIED: glow underline)
// ─────────────────────────────────────────────────────────────────────

import React from 'react';
import {
  BaseBlockProps,
  ColorConfig,
  FONTS,
  hexRgba,
  optimalFontSize,
  toArabicDigits,
  truncateCta,
  useColors,
  depthShadow,
  accentShadow,
  innerGlowStyle,
} from './helpers';

// ─── CTAButton (MODIFIED: colored shadow, inner glow) ────────────────
export interface CTAButtonProps extends BaseBlockProps {
  text: string;
  arrow?: string;
  showArrow?: boolean;
  fontSize?: number;
  align?: 'right' | 'left' | 'center';
  /** Use colored accent shadow. Default true. */
  useAccentShadow?: boolean;
  /** Use inner glow. Default false. */
  useInnerGlow?: boolean;
}
export const CTAButton: React.FC<CTAButtonProps> = ({
  text,
  arrow = '←',
  showArrow = true,
  fontSize = 20,
  align = 'right',
  useAccentShadow = true,
  useInnerGlow = false,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const shortText = truncateCta(text);
  const fs = optimalFontSize(shortText, 500, fontSize);
  const ctaGradient = `linear-gradient(135deg, ${c.badgeBg} 0%, ${c.accent2} 100%)`;
  const justify = align === 'center' ? 'center' : align === 'left' ? 'flex-start' : 'flex-end';
  const shadow = useAccentShadow ? accentShadow(c.accent, 'medium') : depthShadow('medium');
  const glow = useInnerGlow ? innerGlowStyle(c.accent2, 'subtle') : {};

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: justify,
        padding: '8px 50px',
        flexShrink: 0,
        direction: 'rtl',
        zIndex: 5,
        ...style,
      }}
    >
      <div
        style={{
          background: ctaGradient,
          color: c.badgeText,
          padding: '14px 40px',
          borderRadius: '50px',
          fontSize: `${fs}px`,
          fontWeight: 800,
          fontFamily: FONTS.sans,
          boxShadow: `${shadow}, 0 0 0 1px rgba(255,255,255,0.12)`,
          direction: 'rtl',
          textAlign: 'center',
          maxWidth: '560px',
          display: 'inline-flex',
          alignItems: 'center',
          gap: '8px',
          ...glow,
        }}
      >
        {showArrow && arrow ? `${arrow} ` : ''}
        {shortText}
      </div>
    </div>
  );
};

// ─── CTABanner (MODIFIED: depth shadow) ──────────────────────────────
export interface CTABannerProps extends BaseBlockProps {
  text: string;
  subText?: string;
  arrow?: string;
  showArrow?: boolean;
  fontSize?: number;
}
export const CTABanner: React.FC<CTABannerProps> = ({
  text,
  subText,
  arrow = '←',
  showArrow = true,
  fontSize = 22,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const fs = optimalFontSize(text, 800, fontSize);

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        padding: '12px 50px',
        flexShrink: 0,
        direction: 'rtl',
        zIndex: 5,
        ...style,
      }}
    >
      <div
        style={{
          width: '100%',
          background: `linear-gradient(135deg, ${c.accent} 0%, ${c.accent2} 100%)`,
          borderRadius: '18px',
          padding: '20px 36px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          direction: 'rtl',
          boxShadow: depthShadow('medium'),
        }}
      >
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'flex-end',
            direction: 'rtl',
            textAlign: 'right',
            flex: 1,
          }}
        >
          <span
            style={{
              fontFamily: FONTS.kufi,
              fontSize: `${fs}px`,
              fontWeight: 900,
              color: c.badgeText,
              direction: 'rtl',
            }}
          >
            {text}
          </span>
          {subText && (
            <span
              style={{
                fontFamily: FONTS.sans,
                fontSize: '14px',
                fontWeight: 500,
                color: c.badgeText,
                opacity: 0.85,
                marginTop: '4px',
                direction: 'rtl',
              }}
            >
              {subText}
            </span>
          )}
        </div>
        {showArrow && arrow && (
          <div
            style={{
              width: '44px',
              height: '44px',
              borderRadius: '50%',
              background: hexRgba(c.badgeText, '0.2'),
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '22px',
              color: c.badgeText,
              flexShrink: 0,
            }}
          >
            {arrow}
          </div>
        )}
      </div>
    </div>
  );
};

// ─── CTAFloating (MODIFIED: accent shadow) ────────────────────────────
export interface CTAFloatingProps extends BaseBlockProps {
  text: string;
  position?: 'bottom-left' | 'bottom-right' | 'bottom-center';
  shape?: 'pill' | 'circle';
  icon?: string;
}
export const CTAFloating: React.FC<CTAFloatingProps> = ({
  text,
  position = 'bottom-left',
  shape = 'pill',
  icon,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const isCircle = shape === 'circle';
  const posStyle: React.CSSProperties =
    position === 'bottom-center'
      ? { bottom: '180px', left: '50%', transform: 'translateX(-50%)' }
      : position === 'bottom-right'
        ? { bottom: '180px', right: '50px' }
        : { bottom: '180px', left: '50px' };

  const size = isCircle ? 90 : undefined;

  return (
    <div
      style={{
        position: 'absolute',
        ...posStyle,
        zIndex: 20,
        ...style,
      }}
    >
      <div
        style={{
          width: isCircle ? `${size}px` : 'auto',
          height: isCircle ? `${size}px` : 'auto',
          borderRadius: isCircle ? '50%' : '50px',
          background: `linear-gradient(135deg, ${c.badgeBg} 0%, ${c.accent2} 100%)`,
          color: c.badgeText,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: isCircle ? 0 : '16px 32px',
          fontFamily: FONTS.kufi,
          fontSize: isCircle ? '14px' : '18px',
          fontWeight: 800,
          boxShadow: `${accentShadow(c.accent, 'strong')}, 0 0 0 2px rgba(255,255,255,0.15)`,
          direction: 'rtl',
          textAlign: 'center',
          border: `3px solid ${hexRgba(c.bg, '0.3')}`,
        }}
      >
        {isCircle && icon ? icon : text}
      </div>
    </div>
  );
};

// ─── CTAInline (MODIFIED: glow underline) ────────────────────────────
export interface CTAInlineProps extends BaseBlockProps {
  text: string;
  arrow?: string;
  showArrow?: boolean;
  fontSize?: number;
  align?: 'right' | 'left' | 'center';
  underline?: 'solid' | 'dashed' | 'none' | 'glow';
}
export const CTAInline: React.FC<CTAInlineProps> = ({
  text,
  arrow = '←',
  showArrow = true,
  fontSize = 18,
  align = 'right',
  underline = 'solid',
  colors,
  style,
}) => {
  const c = useColors(colors);
  const justify = align === 'center' ? 'center' : align === 'left' ? 'flex-start' : 'flex-end';
  const underlineStyle = underline === 'glow'
    ? `2px solid ${hexRgba(c.accent, '0.7')}`
    : underline === 'none'
      ? 'none'
      : `2px ${underline} ${hexRgba(c.accent, '0.5')}`;
  const glowShadow = underline === 'glow' ? `0 2px 12px ${hexRgba(c.accent, '0.4')}` : 'none';

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: justify,
        padding: '6px 50px',
        flexShrink: 0,
        direction: 'rtl',
        zIndex: 5,
        ...style,
      }}
    >
      <div
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '6px',
          fontFamily: FONTS.sans,
          fontSize: `${fontSize}px`,
          fontWeight: 700,
          color: c.accent,
          direction: 'rtl',
          paddingBottom: '4px',
          borderBottom: underlineStyle,
          boxShadow: glowShadow,
        }}
      >
        {showArrow && arrow ? `${arrow} ` : ''}
        {text}
      </div>
    </div>
  );
};
