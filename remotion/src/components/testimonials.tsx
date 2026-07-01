// ─────────────────────────────────────────────────────────────────────
// TESTIMONIALS — Social proof components
//   ReviewCard  · avatar circle + star rating + quote (Arabic RTL)
//   TweetCard   · social media style card with engagement metrics
//   QuoteLarge  · large pull-quote with decorative quotation marks
// ─────────────────────────────────────────────────────────────────────

import React from 'react';
import {
  BaseBlockProps,
  ColorConfig,
  FONTS,
  StarRating,
  hexRgba,
  toArabicDigits,
  useColors,
} from './helpers';
import { Icon } from './icon';

// ─── ReviewCard ────────────────────────────────────────────────────────
export interface ReviewCardProps extends BaseBlockProps {
  /** Reviewer name (Arabic or Latin). */
  author: string;
  /** Star rating 0–5. Default 5. */
  rating?: number;
  /** Quote / review text. */
  text: string;
  /** Seed for avatar gradient (e.g. initials or short string). */
  avatarSeed?: string;
}

export const ReviewCard: React.FC<ReviewCardProps> = ({
  author,
  rating = 5,
  text,
  avatarSeed,
  colors,
  style,
}) => {
  const c = useColors(colors);
  // Build initials from author name (first letter of up to two words).
  const initials = (avatarSeed || author || '')
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((w) => w.charAt(0))
    .join('');

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        padding: '16px 50px',
        flexShrink: 0,
        direction: 'rtl',
        zIndex: 5,
        ...style,
      }}
    >
      <div
        style={{
          position: 'relative',
          maxWidth: '680px',
          width: '100%',
          padding: '24px 26px',
          borderRadius: '20px',
          background: hexRgba(c.accent, '0.07'),
          border: `1px solid ${hexRgba(c.accent, '0.15')}`,
          borderRight: `5px solid ${c.accent}`,
          direction: 'rtl',
          textAlign: 'right',
        }}
      >
        {/* Header: avatar + name + stars */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            justifyContent: 'flex-end',
            direction: 'rtl',
            marginBottom: '14px',
          }}
        >
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
            <span
              style={{
                fontFamily: FONTS.kufi,
                fontSize: '17px',
                fontWeight: 800,
                color: c.text,
                direction: 'rtl',
              }}
            >
              {author}
            </span>
            <StarRating rating={rating} color={c.accent} size={15} style={{ marginTop: '4px' }} />
          </div>
          <div
            style={{
              width: '52px',
              height: '52px',
              borderRadius: '50%',
              background: `linear-gradient(135deg, ${c.accent}, ${c.accent2})`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '20px',
              fontWeight: 900,
              color: c.badgeText,
              fontFamily: FONTS.lato,
              flexShrink: 0,
              border: `2px solid ${hexRgba(c.accent2, '0.4')}`,
            }}
          >
            {initials || '؟'}
          </div>
        </div>
        {/* Quote text */}
        <p
          style={{
            fontFamily: FONTS.sans,
            fontSize: '16px',
            color: c.text,
            opacity: 0.9,
            lineHeight: 1.65,
            margin: 0,
            direction: 'rtl',
          }}
        >
          {text}
        </p>
      </div>
    </div>
  );
};

// ─── TweetCard ────────────────────────────────────────────────────────
export interface TweetCardProps extends BaseBlockProps {
  /** Display name. */
  author: string;
  /** Handle (without @). */
  handle: string;
  /** Tweet body text. */
  text: string;
  /** Number of likes. */
  likes?: number;
  /** Number of retweets / shares. */
  retweets?: number;
}

export const TweetCard: React.FC<TweetCardProps> = ({
  author,
  handle,
  text,
  likes = 0,
  retweets = 0,
  colors,
  style,
}) => {
  const c = useColors(colors);

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        padding: '16px 50px',
        flexShrink: 0,
        direction: 'rtl',
        zIndex: 5,
        ...style,
      }}
    >
      <div
        style={{
          position: 'relative',
          maxWidth: '640px',
          width: '100%',
          padding: '22px 24px',
          borderRadius: '20px',
          background: hexRgba(c.accent, '0.06'),
          border: `1px solid ${hexRgba(c.accent, '0.14')}`,
          direction: 'rtl',
        }}
      >
        {/* Header: avatar + name/handle */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            justifyContent: 'flex-end',
            direction: 'rtl',
            marginBottom: '12px',
          }}
        >
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
            <span
              style={{
                fontFamily: FONTS.kufi,
                fontSize: '16px',
                fontWeight: 800,
                color: c.text,
                direction: 'rtl',
              }}
            >
              {author}
            </span>
            <span
              style={{
                fontFamily: FONTS.sans,
                fontSize: '13px',
                color: c.text,
                opacity: 0.6,
                direction: 'ltr',
              }}
            >
              @{handle}
            </span>
          </div>
          <div
            style={{
              width: '46px',
              height: '46px',
              borderRadius: '50%',
              background: `linear-gradient(135deg, ${c.accent}, ${c.accent2})`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0,
            }}
          >
            <Icon name="sparkles" size={22} color={c.badgeText} colors={c} />
          </div>
        </div>
        {/* Body */}
        <p
          style={{
            fontFamily: FONTS.sans,
            fontSize: '16px',
            color: c.text,
            opacity: 0.92,
            lineHeight: 1.6,
            margin: '0 0 14px 0',
            direction: 'rtl',
          }}
        >
          {text}
        </p>
        {/* Engagement metrics */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '22px',
            justifyContent: 'flex-end',
            direction: 'rtl',
            borderTop: `1px solid ${hexRgba(c.accent, '0.12')}`,
            paddingTop: '12px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <Icon name="heart" size={16} color={c.accent} colors={c} />
            <span
              style={{
                fontFamily: FONTS.sans,
                fontSize: '13px',
                fontWeight: 600,
                color: c.text,
                opacity: 0.8,
                direction: 'ltr',
              }}
            >
              {toArabicDigits(likes)}
            </span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <Icon name="zap" size={16} color={c.accent2} colors={c} />
            <span
              style={{
                fontFamily: FONTS.sans,
                fontSize: '13px',
                fontWeight: 600,
                color: c.text,
                opacity: 0.8,
                direction: 'ltr',
              }}
            >
              {toArabicDigits(retweets)}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

// ─── QuoteLarge ───────────────────────────────────────────────────────
export interface QuoteLargeProps extends BaseBlockProps {
  /** The pull-quote text. */
  quote: string;
  /** Attribution name. */
  author: string;
  /** Author role / title (e.g. "مدير التسويق"). */
  role?: string;
}

export const QuoteLarge: React.FC<QuoteLargeProps> = ({
  quote,
  author,
  role,
  colors,
  style,
}) => {
  const c = useColors(colors);

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '24px 50px',
        flexShrink: 0,
        direction: 'rtl',
        zIndex: 5,
        ...style,
      }}
    >
      <div
        style={{
          position: 'relative',
          maxWidth: '820px',
          width: '100%',
          padding: '36px 44px 30px',
          borderRadius: '24px',
          background: hexRgba(c.accent, '0.06'),
          border: `1px solid ${hexRgba(c.accent, '0.13')}`,
          textAlign: 'center',
          direction: 'rtl',
        }}
      >
        {/* Decorative opening quote mark */}
        <span
          style={{
            position: 'absolute',
            top: '-6px',
            right: '24px',
            fontSize: '90px',
            fontFamily: FONTS.kufi,
            fontWeight: 900,
            color: hexRgba(c.accent, '0.22'),
            lineHeight: 1,
            direction: 'rtl',
          }}
        >
          ”
        </span>
        {/* Decorative closing quote mark */}
        <span
          style={{
            position: 'absolute',
            bottom: '-30px',
            left: '24px',
            fontSize: '90px',
            fontFamily: FONTS.kufi,
            fontWeight: 900,
            color: hexRgba(c.accent2, '0.22'),
            lineHeight: 1,
            direction: 'rtl',
          }}
        >
          „
        </span>
        {/* Quote text */}
        <p
          style={{
            fontFamily: FONTS.kufi,
            fontSize: '24px',
            fontWeight: 700,
            color: c.text,
            opacity: 0.96,
            lineHeight: 1.55,
            margin: '0 0 20px 0',
            direction: 'rtl',
          }}
        >
          {quote}
        </p>
        {/* Divider */}
        <div
          style={{
            width: '50px',
            height: '3px',
            borderRadius: '2px',
            background: `linear-gradient(90deg, ${c.accent}, ${c.accent2})`,
            margin: '0 auto 16px',
          }}
        />
        {/* Attribution */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '4px',
          }}
        >
          <span
            style={{
              fontFamily: FONTS.kufi,
              fontSize: '17px',
              fontWeight: 800,
              color: c.accent2,
              direction: 'rtl',
            }}
          >
            {author}
          </span>
          {role && (
            <span
              style={{
                fontFamily: FONTS.sans,
                fontSize: '14px',
                color: c.text,
                opacity: 0.7,
                direction: 'rtl',
              }}
            >
              {role}
            </span>
          )}
        </div>
      </div>
    </div>
  );
};
