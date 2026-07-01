// ─────────────────────────────────────────────────────────────────────
// FOOTERS — 4 components
//   FooterRating   · star rating + review count + trust badge
//   FooterHashtags · hashtag row with configurable color/opacity
//   FooterBranding · "نُهوت — التسويق الرقمي" + "nuhoot.xyz"
//   FooterComplete · rating + trust + hashtags + branding combined
// ─────────────────────────────────────────────────────────────────────

import React from 'react';
import {
  BaseBlockProps,
  ColorConfig,
  FONTS,
  hexRgba,
  StarRating,
  toArabicDigits,
  useColors,
} from './helpers';

// ─── FooterRating ─────────────────────────────────────────────────────
export interface FooterRatingProps extends BaseBlockProps {
  /** Star rating 0–5. */
  rating: number;
  /** Number of reviews. */
  reviews: number;
  /** Trust badge text (e.g. "حبوب مختارة"). */
  trustBadge?: string;
  /** Star size in px. Default 18. */
  starSize?: number;
}

export const FooterRating: React.FC<FooterRatingProps> = ({
  rating,
  reviews,
  trustBadge,
  starSize = 18,
  colors,
  style,
}) => {
  const c = useColors(colors);

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-end',
        gap: '8px',
        direction: 'rtl',
        textAlign: 'right',
        ...style,
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', direction: 'rtl' }}>
        <StarRating rating={rating} color={c.accent} size={starSize} />
        <span style={{ fontSize: '26px', fontWeight: 900, color: c.text, fontFamily: FONTS.kufi }}>
          {toArabicDigits(rating.toFixed(1).replace('.', '٫'))}
        </span>
        <span style={{ fontSize: '14px', color: c.text, opacity: 0.7, fontFamily: FONTS.sans }}>
          {toArabicDigits(reviews)} تقييم
        </span>
      </div>
      {trustBadge && (
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            fontSize: '14px',
            color: c.accent,
            opacity: 0.9,
            direction: 'rtl',
            background: hexRgba(c.accent, '0.12'),
            padding: '4px 14px',
            borderRadius: '20px',
            fontFamily: FONTS.sans,
          }}
        >
          <span>✦</span> {trustBadge}
        </div>
      )}
    </div>
  );
};

// ─── FooterHashtags ───────────────────────────────────────────────────
export interface FooterHashtagsProps extends BaseBlockProps {
  /** Hashtag strings (with or without #). */
  hashtags: string[];
  /** Color override for hashtags. */
  hashtagColor?: string;
  /** Opacity. Default 0.75. */
  opacity?: number;
  /** Font size in px. Default 13. */
  fontSize?: number;
}

export const FooterHashtags: React.FC<FooterHashtagsProps> = ({
  hashtags,
  hashtagColor,
  opacity = 0.75,
  fontSize = 13,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const col = hashtagColor ?? c.accent2;
  const normalized = hashtags.map((h) => (h.startsWith('#') ? h : `#${h}`));

  return (
    <div
      style={{
        fontSize: `${fontSize}px`,
        color: col,
        direction: 'rtl',
        opacity,
        fontFamily: FONTS.sans,
        textAlign: 'right',
        ...style,
      }}
    >
      {normalized.join('  ')}
    </div>
  );
};

// ─── FooterBranding ───────────────────────────────────────────────────
export interface FooterBrandingProps extends BaseBlockProps {
  /** Brand text. Default "نُهوت — التسويق الرقمي". */
  brandText?: string;
  /** URL text. Default "nuhoot.xyz". */
  urlText?: string;
  /** Show the top border separator. Default true. */
  showBorder?: boolean;
}

export const FooterBranding: React.FC<FooterBrandingProps> = ({
  brandText = 'نُهوت — التسويق الرقمي',
  urlText = 'nuhoot.xyz',
  showBorder = true,
  colors,
  style,
}) => {
  const c = useColors(colors);

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        width: '100%',
        gap: '16px',
        paddingTop: showBorder ? '8px' : 0,
        borderTop: showBorder ? `1px solid ${hexRgba(c.accent, '0.25')}` : 'none',
        ...style,
      }}
    >
      <span
        style={{
          fontFamily: 'monospace',
          fontSize: '13px',
          color: c.accent,
          opacity: 0.8,
          direction: 'ltr',
        }}
      >
        {urlText}
      </span>
      <span
        style={{
          fontSize: '15px',
          color: c.accent,
          opacity: 0.9,
          direction: 'rtl',
          fontWeight: 600,
          fontFamily: FONTS.kufi,
        }}
      >
        {brandText}
      </span>
    </div>
  );
};

// ─── FooterComplete ───────────────────────────────────────────────────
export interface FooterCompleteProps extends BaseBlockProps {
  rating: number;
  reviews: number;
  trustBadge?: string;
  hashtags: string[];
  hashtagColor?: string;
  hashtagOpacity?: number;
  brandText?: string;
  urlText?: string;
}

export const FooterComplete: React.FC<FooterCompleteProps> = ({
  rating,
  reviews,
  trustBadge,
  hashtags,
  hashtagColor,
  hashtagOpacity = 0.75,
  brandText,
  urlText,
  colors,
  style,
}) => {
  const c = useColors(colors);

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-end',
        padding: '10px 50px 25px 50px',
        gap: '8px',
        marginTop: 'auto',
        direction: 'rtl',
        textAlign: 'right',
        zIndex: 5,
        ...style,
      }}
    >
      <FooterRating
        rating={rating}
        reviews={reviews}
        trustBadge={trustBadge}
        colors={c}
      />
      <FooterHashtags
        hashtags={hashtags}
        hashtagColor={hashtagColor}
        opacity={hashtagOpacity}
        colors={c}
      />
      <FooterBranding brandText={brandText} urlText={urlText} colors={c} />
    </div>
  );
};
