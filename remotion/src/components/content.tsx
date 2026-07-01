// ─────────────────────────────────────────────────────────────────────
// CONTENT — 5 components (all MODIFIED with glassmorphism, depth, variety)
//   ContentCards    · 3 cards (MODIFIED: glassmorphism, varied sizes)
//   ContentList     · bullet list (MODIFIED: custom bullet shapes)
//   ContentStats    · stats (MODIFIED: size gradient, glassmorphism)
//   ContentQuotes   · review (MODIFIED: glassmorphism)
//   ContentFeatures · icon features (MODIFIED: glassmorphism, Lucide icons)
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
  depthShadow,
  GlassCard,
  typeScale,
} from './helpers';
import { Icon } from './icon';

// ─── ContentCards (MODIFIED: glassmorphism, varied sizes) ────────────
export interface ContentCardItem {
  title: string;
  description: string;
}
export interface ContentCardsProps extends BaseBlockProps {
  items: ContentCardItem[];
  gap?: number;
  cardOpacity?: number;
  /** Use glassmorphism effect. Default false. */
  glass?: boolean;
}
export const ContentCards: React.FC<ContentCardsProps> = ({
  items,
  gap = 16,
  cardOpacity = 0.08,
  glass = false,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const cards = items.slice(0, 3);

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        gap: `${gap}px`,
        padding: '16px 50px',
        flexShrink: 0,
        direction: 'rtl',
        zIndex: 5,
        ...style,
      }}
    >
      {cards.map((card, i) => (
        <div
          key={i}
          style={{
            flex: 1,
            background: glass
              ? `rgba(255,255,255,${cardOpacity})`
              : hexRgba(c.accent, String(cardOpacity)),
            backdropFilter: glass ? 'blur(20px)' : 'none',
            WebkitBackdropFilter: glass ? 'blur(20px)' : 'none',
            borderRadius: '16px',
            padding: '20px 18px',
            border: `1px solid ${hexRgba(c.accent, glass ? '0.2' : '0.15')}`,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'flex-end',
            textAlign: 'right',
            direction: 'rtl',
            minHeight: '140px',
            boxShadow: glass ? '0 8px 32px rgba(0,0,0,0.15), inset 0 1px 0 rgba(255,255,255,0.1)' : 'none',
          }}
        >
          <div
            style={{
              width: '36px',
              height: '36px',
              borderRadius: '50%',
              background: `linear-gradient(135deg, ${c.accent}, ${c.accent2})`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '12px',
              fontSize: '16px',
              fontWeight: 900,
              color: c.badgeText,
              fontFamily: FONTS.lato,
            }}
          >
            {toArabicDigits(i + 1)}
          </div>
          <h3
            style={{
              fontFamily: FONTS.kufi,
              fontSize: '18px',
              fontWeight: 800,
              color: c.text,
              margin: '0 0 8px 0',
              direction: 'rtl',
            }}
          >
            {card.title}
          </h3>
          <p
            style={{
              fontFamily: FONTS.sans,
              fontSize: '14px',
              color: c.text,
              opacity: 0.8,
              lineHeight: 1.5,
              margin: 0,
              direction: 'rtl',
            }}
          >
            {card.description}
          </p>
        </div>
      ))}
    </div>
  );
};

// ─── ContentList (MODIFIED: custom bullet shapes) ─────────────────────
export interface ContentListProps extends BaseBlockProps {
  items: string[];
  bullet?: string;
  fontSize?: number;
  /** Bullet style. Default 'diamond'. */
  bulletStyle?: 'diamond' | 'dot' | 'arrow' | 'check' | 'star';
  /** Use glassmorphism. Default false. */
  glass?: boolean;
}
export const ContentList: React.FC<ContentListProps> = ({
  items,
  bullet = '✦',
  fontSize = 18,
  bulletStyle = 'diamond',
  glass = false,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const bullets = { diamond: '◆', dot: '●', arrow: '◄', check: '✓', star: '★' };
  const bChar = bullets[bulletStyle] || bullet;

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-end',
        padding: '16px 50px',
        gap: '12px',
        flexShrink: 0,
        direction: 'rtl',
        textAlign: 'right',
        zIndex: 5,
        ...style,
      }}
    >
      {items.map((item, i) => (
        <div
          key={i}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            direction: 'rtl',
            padding: glass ? '8px 16px' : '0',
            borderRadius: glass ? '12px' : '0',
            background: glass ? `rgba(255,255,255,0.05)` : 'transparent',
            backdropFilter: glass ? 'blur(10px)' : 'none',
          }}
        >
          <span
            style={{
              fontFamily: FONTS.sans,
              fontSize: `${fontSize}px`,
              color: c.text,
              opacity: 0.9,
              lineHeight: 1.5,
              direction: 'rtl',
            }}
          >
            {item}
          </span>
          <span
            style={{
              fontSize: `${fontSize * 0.7}px`,
              color: c.accent,
              flexShrink: 0,
            }}
          >
            {bChar}
          </span>
        </div>
      ))}
    </div>
  );
};

// ─── ContentStats (MODIFIED: size gradient, glassmorphism) ────────────
export interface StatItem {
  number: string;
  label: string;
  unit?: string;
}
export interface ContentStatsProps extends BaseBlockProps {
  stats: StatItem[];
  gap?: number;
  /** Use glassmorphism. Default false. */
  glass?: boolean;
  /** Apply size gradient (first stat largest). Default true. */
  sizeGradient?: boolean;
}
export const ContentStats: React.FC<ContentStatsProps> = ({
  stats,
  gap = 20,
  glass = false,
  sizeGradient = true,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const data = stats.slice(0, 4);
  const baseSizes = typeScale(28, 1.2, data.length - 1);

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'stretch',
        gap: `${gap}px`,
        padding: '20px 50px',
        flexShrink: 0,
        direction: 'rtl',
        zIndex: 5,
        ...style,
      }}
    >
      {data.map((stat, i) => {
        const numSize = sizeGradient ? baseSizes[i] || 40 : 40;
        return (
          <div
            key={i}
            style={{
              flex: 1,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              padding: '18px 8px',
              borderRadius: '16px',
              background: glass
                ? `rgba(255,255,255,0.06)`
                : hexRgba(c.accent, '0.06'),
              backdropFilter: glass ? 'blur(20px)' : 'none',
              WebkitBackdropFilter: glass ? 'blur(20px)' : 'none',
              border: `1px solid ${hexRgba(c.accent, '0.12')}`,
              textAlign: 'center',
              boxShadow: glass ? '0 8px 32px rgba(0,0,0,0.12), inset 0 1px 0 rgba(255,255,255,0.08)' : 'none',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'baseline', gap: '2px' }}>
              <span
                style={{
                  fontFamily: FONTS.kufi,
                  fontSize: `${numSize}px`,
                  fontWeight: 900,
                  color: c.accent,
                  lineHeight: 1,
                  direction: 'ltr',
                }}
              >
                {toArabicDigits(stat.number)}
              </span>
              {stat.unit && (
                <span
                  style={{
                    fontFamily: FONTS.kufi,
                    fontSize: `${Math.round(numSize * 0.55)}px`,
                    fontWeight: 700,
                    color: c.accent2,
                  }}
                >
                  {stat.unit}
                </span>
              )}
            </div>
            <span
              style={{
                fontFamily: FONTS.sans,
                fontSize: '14px',
                fontWeight: 600,
                color: c.text,
                opacity: 0.75,
                marginTop: '6px',
                direction: 'rtl',
              }}
            >
              {stat.label}
            </span>
          </div>
        );
      })}
    </div>
  );
};

// ─── ContentQuotes (MODIFIED: glassmorphism) ─────────────────────────
export interface ContentQuotesProps extends BaseBlockProps {
  quote: string;
  author: string;
  rating?: number;
  quoteMark?: string;
  glass?: boolean;
}
export const ContentQuotes: React.FC<ContentQuotesProps> = ({
  quote,
  author,
  rating = 5,
  quoteMark = '«',
  glass = false,
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
          maxWidth: '780px',
          padding: '28px 36px',
          borderRadius: '20px',
          background: glass
            ? `rgba(255,255,255,0.07)`
            : hexRgba(c.accent, '0.07'),
          backdropFilter: glass ? 'blur(20px)' : 'none',
          WebkitBackdropFilter: glass ? 'blur(20px)' : 'none',
          border: `1px solid ${hexRgba(c.accent, '0.15')}`,
          borderRight: `5px solid ${c.accent}`,
          direction: 'rtl',
          textAlign: 'right',
          boxShadow: glass ? '0 8px 32px rgba(0,0,0,0.15), inset 0 1px 0 rgba(255,255,255,0.08)' : 'none',
        }}
      >
        <span
          style={{
            position: 'absolute',
            top: '8px',
            left: '20px',
            fontSize: '60px',
            fontFamily: FONTS.kufi,
            color: hexRgba(c.accent, '0.2'),
            lineHeight: 1,
          }}
        >
          {quoteMark}
        </span>
        <p
          style={{
            fontFamily: FONTS.sans,
            fontSize: '19px',
            color: c.text,
            opacity: 0.95,
            lineHeight: 1.6,
            margin: '0 0 14px 0',
            direction: 'rtl',
          }}
        >
          {quote}
        </p>
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            justifyContent: 'flex-end',
            direction: 'rtl',
          }}
        >
          <span
            style={{
              fontFamily: FONTS.kufi,
              fontSize: '16px',
              fontWeight: 700,
              color: c.accent2,
              direction: 'rtl',
            }}
          >
            {author}
          </span>
          <StarRating rating={rating} color={c.accent} size={16} />
        </div>
      </div>
    </div>
  );
};

// ─── ContentFeatures (MODIFIED: glassmorphism, Lucide icons) ──────────
export interface FeatureItem {
  /** Lucide icon name or emoji. */
  icon: string;
  title: string;
  description: string;
}
export interface ContentFeaturesProps extends BaseBlockProps {
  features: FeatureItem[];
  direction?: 'row' | 'column';
  gap?: number;
  glass?: boolean;
}
export const ContentFeatures: React.FC<ContentFeaturesProps> = ({
  features,
  direction = 'row',
  gap = 16,
  glass = false,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const items = features.slice(0, 3);
  const isRow = direction === 'row';

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: isRow ? 'row' : 'column',
        justifyContent: 'center',
        gap: `${gap}px`,
        padding: '16px 50px',
        flexShrink: 0,
        direction: 'rtl',
        zIndex: 5,
        ...style,
      }}
    >
      {items.map((feat, i) => {
        // Check if the icon is a Lucide icon name (lowercase letters)
        const isLucideIcon = /^[a-z]/.test(feat.icon);
        return (
          <div
            key={i}
            style={{
              flex: isRow ? 1 : undefined,
              display: 'flex',
              flexDirection: isRow ? 'column' : 'row-reverse',
              alignItems: 'center',
              gap: '12px',
              padding: '16px',
              borderRadius: '14px',
              background: glass
                ? `rgba(255,255,255,0.05)`
                : hexRgba(c.accent, '0.05'),
              backdropFilter: glass ? 'blur(15px)' : 'none',
              WebkitBackdropFilter: glass ? 'blur(15px)' : 'none',
              textAlign: 'center',
              border: glass ? `1px solid ${hexRgba(c.accent, '0.1')}` : 'none',
            }}
          >
            <div
              style={{
                width: '48px',
                height: '48px',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: `linear-gradient(135deg, ${hexRgba(c.accent, '0.2')}, ${hexRgba(c.accent2, '0.2')})`,
                border: `1px solid ${hexRgba(c.accent, '0.25')}`,
                fontSize: '24px',
                flexShrink: 0,
              }}
            >
              {isLucideIcon ? (
                <Icon name={feat.icon} size={24} color={c.accent} colors={c} />
              ) : (
                feat.icon
              )}
            </div>
            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: isRow ? 'center' : 'flex-end',
                direction: 'rtl',
                textAlign: isRow ? 'center' : 'right',
              }}
            >
              <span
                style={{
                  fontFamily: FONTS.kufi,
                  fontSize: '17px',
                  fontWeight: 800,
                  color: c.text,
                  marginBottom: '4px',
                  direction: 'rtl',
                }}
              >
                {feat.title}
              </span>
              <span
                style={{
                  fontFamily: FONTS.sans,
                  fontSize: '13px',
                  color: c.text,
                  opacity: 0.7,
                  lineHeight: 1.4,
                  direction: 'rtl',
                }}
              >
                {feat.description}
              </span>
            </div>
          </div>
        );
      })}
    </div>
  );
};
