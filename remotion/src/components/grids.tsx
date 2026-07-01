// ─────────────────────────────────────────────────────────────────────
// GRIDS — Layout grid components
//   BentoGrid   · asymmetric bento grid layout
//   FeatureGrid · 2x2 or 3x2 icon + title grid
// ─────────────────────────────────────────────────────────────────────

import React from 'react';
import {
  BaseBlockProps,
  ColorConfig,
  FONTS,
  hexRgba,
  toArabicDigits,
  useColors,
} from './helpers';
import { Icon } from './icon';

// ─── BentoGrid ────────────────────────────────────────────────────────
export interface BentoItem {
  title: string;
  description: string;
  /** Lucide icon name. */
  icon: string;
  /** Tile size. 'lg' spans 2 cols, 'wide' spans 2 rows. Default 'md'. */
  size?: 'sm' | 'md' | 'lg' | 'wide';
}

export interface BentoGridProps extends BaseBlockProps {
  /** Array of {title, description, icon, size} — up to 6 shown. */
  items: BentoItem[];
  /** Gap between tiles in px. Default 14. */
  gap?: number;
}

export const BentoGrid: React.FC<BentoGridProps> = ({
  items,
  gap = 14,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const tiles = items.slice(0, 6);

  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gridAutoRows: '1fr',
        gap: `${gap}px`,
        padding: '16px 50px',
        flexShrink: 0,
        direction: 'rtl',
        zIndex: 5,
        ...style,
      }}
    >
      {tiles.map((tile, i) => {
        const span = tile.size === 'lg' ? 'span 2' : tile.size === 'wide' ? 'span 2' : 'span 1';
        const colSpan = tile.size === 'lg' ? span : undefined;
        const rowSpan = tile.size === 'wide' ? span : undefined;
        return (
          <div
            key={i}
            style={{
              gridColumn: colSpan,
              gridRow: rowSpan,
              padding: '18px 20px',
              borderRadius: '18px',
              background: hexRgba(c.accent, '0.06'),
              border: `1px solid ${hexRgba(c.accent, '0.13')}`,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'flex-end',
              textAlign: 'right',
              direction: 'rtl',
              minHeight: '100px',
            }}
          >
            <div
              style={{
                width: '40px',
                height: '40px',
                borderRadius: '10px',
                background: `linear-gradient(135deg, ${hexRgba(c.accent, '0.22')}, ${hexRgba(
                  c.accent2,
                  '0.18',
                )})`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '12px',
                flexShrink: 0,
                border: `1px solid ${hexRgba(c.accent, '0.25')}`,
              }}
            >
              <Icon name={tile.icon} size={22} color={c.accent} colors={c} />
            </div>
            <span
              style={{
                fontFamily: FONTS.kufi,
                fontSize: '16px',
                fontWeight: 800,
                color: c.text,
                marginBottom: '6px',
                direction: 'rtl',
              }}
            >
              {tile.title}
            </span>
            <span
              style={{
                fontFamily: FONTS.sans,
                fontSize: '13px',
                color: c.text,
                opacity: 0.72,
                lineHeight: 1.5,
                direction: 'rtl',
              }}
            >
              {tile.description}
            </span>
          </div>
        );
      })}
    </div>
  );
};

// ─── FeatureGrid ──────────────────────────────────────────────────────
export interface FeatureGridItem {
  /** Lucide icon name. */
  icon: string;
  title: string;
}

export interface FeatureGridProps extends BaseBlockProps {
  /** Array of {icon, title} — up to 6 shown (2x2 or 3x2). */
  features: FeatureGridItem[];
  /** Columns count. Default 3. */
  columns?: number;
  /** Gap in px. Default 14. */
  gap?: number;
}

export const FeatureGrid: React.FC<FeatureGridProps> = ({
  features,
  columns = 3,
  gap = 14,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const items = features.slice(0, 6);

  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: `repeat(${columns}, 1fr)`,
        gap: `${gap}px`,
        padding: '16px 50px',
        flexShrink: 0,
        direction: 'rtl',
        zIndex: 5,
        ...style,
      }}
    >
      {items.map((feat, i) => (
        <div
          key={i}
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            textAlign: 'center',
            padding: '20px 14px',
            borderRadius: '16px',
            background: hexRgba(c.accent, '0.05'),
            border: `1px solid ${hexRgba(c.accent, '0.1')}`,
          }}
        >
          <div
            style={{
              width: '52px',
              height: '52px',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              background: `linear-gradient(135deg, ${hexRgba(c.accent, '0.2')}, ${hexRgba(
                c.accent2,
                '0.2',
              )})`,
              border: `1px solid ${hexRgba(c.accent, '0.25')}`,
              marginBottom: '12px',
            }}
          >
            <Icon name={feat.icon} size={26} color={c.accent} colors={c} />
          </div>
          <span
            style={{
              fontFamily: FONTS.kufi,
              fontSize: '15px',
              fontWeight: 700,
              color: c.text,
              direction: 'rtl',
            }}
          >
            {feat.title}
          </span>
        </div>
      ))}
    </div>
  );
};
