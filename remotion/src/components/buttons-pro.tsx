// ─────────────────────────────────────────────────────────────────────
// BUTTONS PRO — Premium CTA button variants
//   CTAShimmer · button with shimmer animation overlay
//   CTAGlow · button with glow/shadow pulse
//   CTAOutline · outlined/ghost button
//   CTADual · dual-line button (main text + sub text)
//
// Inspired by: Magic UI buttons (MIT — see docs/ATTRIBUTIONS.md)
// Adapted: Framer Motion animations → static (Remotion still renders)
// ─────────────────────────────────────────────────────────────────────

import React from 'react';
import { BaseBlockProps, ColorConfig, FONTS, hexRgba, optimalFontSize, truncateCta, useColors } from './helpers';
import { Icon } from './icon';

// ─── CTAShimmer ───────────────────────────────────────────────────────
export interface CTAShimmerProps extends BaseBlockProps {
  text: string;
  iconName?: string;
  align?: 'right' | 'left' | 'center';
}

export const CTAShimmer: React.FC<CTAShimmerProps> = ({
  text,
  iconName = 'zap',
  align = 'right',
  colors,
  style,
}) => {
  const c = useColors(colors);
  const shortText = truncateCta(text);
  const fs = optimalFontSize(shortText, 500, 20);
  const justify = align === 'center' ? 'center' : align === 'left' ? 'flex-start' : 'flex-end';

  return (
    <div style={{ display: 'flex', justifyContent: justify, padding: '8px 50px', flexShrink: 0, direction: 'rtl', zIndex: 5, ...style }}>
      <div
        style={{
          position: 'relative',
          overflow: 'hidden',
          background: `linear-gradient(135deg, ${c.accent} 0%, ${c.accent2} 100%)`,
          color: c.badgeText,
          padding: '14px 36px',
          borderRadius: '50px',
          fontSize: `${fs}px`,
          fontWeight: 800,
          fontFamily: FONTS.sans,
          display: 'inline-flex',
          alignItems: 'center',
          gap: '10px',
          boxShadow: `0 8px 25px ${hexRgba(c.accent, '0.4')}, 0 0 0 1px rgba(255,255,255,0.15)`,
        }}
      >
        {/* Shimmer overlay */}
        <div
          style={{
            position: 'absolute',
            top: 0, left: '-100%', width: '50%', height: '100%',
            background: `linear-gradient(90deg, transparent, ${hexRgba('#FFFFFF', '0.3')}, transparent)`,
            transform: 'skewX(-20deg)',
          }}
        />
        <Icon name={iconName} size={18} color={c.badgeText} colors={c} />
        <span style={{ position: 'relative' }}>{shortText}</span>
      </div>
    </div>
  );
};

// ─── CTAGlow ───────────────────────────────────────────────────────────
export interface CTAGlowProps extends BaseBlockProps {
  text: string;
  iconName?: string;
  align?: 'right' | 'left' | 'center';
}

export const CTAGlow: React.FC<CTAGlowProps> = ({
  text,
  iconName = 'sparkles',
  align = 'right',
  colors,
  style,
}) => {
  const c = useColors(colors);
  const shortText = truncateCta(text);
  const fs = optimalFontSize(shortText, 500, 20);
  const justify = align === 'center' ? 'center' : align === 'left' ? 'flex-start' : 'flex-end';

  return (
    <div style={{ display: 'flex', justifyContent: justify, padding: '8px 50px', flexShrink: 0, direction: 'rtl', zIndex: 5, ...style }}>
      <div
        style={{
          background: hexRgba(c.accent, '0.15'),
          border: `2px solid ${c.accent}`,
          color: c.accent,
          padding: '14px 36px',
          borderRadius: '50px',
          fontSize: `${fs}px`,
          fontWeight: 800,
          fontFamily: FONTS.sans,
          display: 'inline-flex',
          alignItems: 'center',
          gap: '10px',
          boxShadow: `0 0 30px ${hexRgba(c.accent, '0.4')}, inset 0 0 20px ${hexRgba(c.accent, '0.1')}`,
        }}
      >
        <Icon name={iconName} size={18} color={c.accent} colors={c} />
        {shortText}
      </div>
    </div>
  );
};

// ─── CTAOutline ────────────────────────────────────────────────────────
export interface CTAOutlineProps extends BaseBlockProps {
  text: string;
  iconName?: string;
  align?: 'right' | 'left' | 'center';
}

export const CTAOutline: React.FC<CTAOutlineProps> = ({
  text,
  iconName = 'arrow-left',
  align = 'right',
  colors,
  style,
}) => {
  const c = useColors(colors);
  const shortText = truncateCta(text);
  const fs = optimalFontSize(shortText, 500, 18);
  const justify = align === 'center' ? 'center' : align === 'left' ? 'flex-start' : 'flex-end';

  return (
    <div style={{ display: 'flex', justifyContent: justify, padding: '8px 50px', flexShrink: 0, direction: 'rtl', zIndex: 5, ...style }}>
      <div
        style={{
          border: `2px solid ${hexRgba(c.accent, '0.5')}`,
          color: c.text,
          padding: '12px 32px',
          borderRadius: '12px',
          fontSize: `${fs}px`,
          fontWeight: 700,
          fontFamily: FONTS.sans,
          display: 'inline-flex',
          alignItems: 'center',
          gap: '8px',
          background: 'transparent',
        }}
      >
        {shortText}
        <Icon name={iconName} size={18} color={c.accent} colors={c} />
      </div>
    </div>
  );
};

// ─── CTADual ───────────────────────────────────────────────────────────
export interface CTADualProps extends BaseBlockProps {
  text: string;
  subText: string;
  iconName?: string;
  align?: 'right' | 'left' | 'center';
}

export const CTADual: React.FC<CTADualProps> = ({
  text,
  subText,
  iconName = 'phone',
  align = 'right',
  colors,
  style,
}) => {
  const c = useColors(colors);
  const justify = align === 'center' ? 'center' : align === 'left' ? 'flex-start' : 'flex-end';

  return (
    <div style={{ display: 'flex', justifyContent: justify, padding: '8px 50px', flexShrink: 0, direction: 'rtl', zIndex: 5, ...style }}>
      <div
        style={{
          background: `linear-gradient(135deg, ${c.accent} 0%, ${c.accent2} 100%)`,
          color: c.badgeText,
          padding: '16px 32px',
          borderRadius: '16px',
          display: 'inline-flex',
          alignItems: 'center',
          gap: '14px',
          boxShadow: '0 10px 30px rgba(0,0,0,0.25)',
        }}
      >
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', direction: 'rtl' }}>
          <span style={{ fontFamily: FONTS.kufi, fontSize: '20px', fontWeight: 900 }}>{text}</span>
          <span style={{ fontFamily: FONTS.sans, fontSize: '13px', opacity: 0.85 }}>{subText}</span>
        </div>
        <div style={{
          width: '40px', height: '40px', borderRadius: '50%',
          background: hexRgba('#FFFFFF', '0.2'),
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          flexShrink: 0,
        }}>
          <Icon name={iconName} size={20} color={c.badgeText} colors={c} />
        </div>
      </div>
    </div>
  );
};
