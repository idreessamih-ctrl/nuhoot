// ─────────────────────────────────────────────────────────────────────
// PRICING — Price tags, discount displays
//   PriceTag · price with currency label
//   PriceStrike · old price struck through + new price
//   PriceCard · full pricing card with discount
//
// Inspired by: shadcn Card (MIT), custom design
// ─────────────────────────────────────────────────────────────────────

import React from 'react';
import { BaseBlockProps, ColorConfig, FONTS, hexRgba, toArabicDigits, useColors } from './helpers';
import { DiscountBadge } from './badges';

// ─── PriceTag ─────────────────────────────────────────────────────────
export interface PriceTagProps extends BaseBlockProps {
  price: string;
  /** Currency label (e.g. "ريال"). */
  currency?: string;
  /** Old price (struck through). */
  oldPrice?: string;
  /** Size. Default 'md'. */
  size?: 'sm' | 'md' | 'lg';
}

export const PriceTag: React.FC<PriceTagProps> = ({
  price,
  currency = 'ريال',
  oldPrice,
  size = 'md',
  colors,
  style,
}) => {
  const c = useColors(colors);
  const fontSizes = { sm: { price: '20px', currency: '12px' }, md: { price: '28px', currency: '14px' }, lg: { price: '36px', currency: '16px' } };

  return (
    <div style={{ display: 'flex', alignItems: 'baseline', gap: '6px', direction: 'rtl', ...style }}>
      {oldPrice && (
        <span style={{ fontFamily: FONTS.sans, fontSize: fontSizes[size].currency, color: c.text, opacity: 0.5, textDecoration: 'line-through' }}>
          {toArabicDigits(oldPrice)}
        </span>
      )}
      <span style={{ fontFamily: FONTS.kufi, fontSize: fontSizes[size].price, fontWeight: 900, color: c.accent }}>
        {toArabicDigits(price)}
      </span>
      <span style={{ fontFamily: FONTS.sans, fontSize: fontSizes[size].currency, color: c.text, opacity: 0.8 }}>
        {currency}
      </span>
    </div>
  );
};

// ─── PriceStrike ──────────────────────────────────────────────────────
export interface PriceStrikeProps extends BaseBlockProps {
  newPrice: string;
  oldPrice: string;
  currency?: string;
  /** Show discount percentage. */
  discountPercent?: number;
}

export const PriceStrike: React.FC<PriceStrikeProps> = ({
  newPrice,
  oldPrice,
  currency = 'ريال',
  discountPercent,
  colors,
  style,
}) => {
  const c = useColors(colors);

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', direction: 'rtl', ...style }}>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px' }}>
        <span style={{ fontFamily: FONTS.kufi, fontSize: '32px', fontWeight: 900, color: c.accent }}>
          {toArabicDigits(newPrice)}
        </span>
        <span style={{ fontFamily: FONTS.sans, fontSize: '14px', color: c.text, opacity: 0.8 }}>{currency}</span>
      </div>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px' }}>
        <span style={{ fontFamily: FONTS.sans, fontSize: '18px', color: c.text, opacity: 0.5, textDecoration: 'line-through' }}>
          {toArabicDigits(oldPrice)}
        </span>
        <span style={{ fontFamily: FONTS.sans, fontSize: '12px', color: c.text, opacity: 0.5 }}>{currency}</span>
      </div>
      {discountPercent != null && (
        <span style={{
          fontFamily: FONTS.sans, fontSize: '12px', fontWeight: 700, color: c.badgeText,
          background: c.accent, padding: '2px 8px', borderRadius: '8px',
        }}>
          {toArabicDigits(discountPercent)}%-
        </span>
      )}
    </div>
  );
};

// ─── PriceCard ────────────────────────────────────────────────────────
export interface PriceCardProps extends BaseBlockProps {
  title: string;
  price: string;
  oldPrice?: string;
  currency?: string;
  description?: string;
  discountPercent?: number;
}

export const PriceCard: React.FC<PriceCardProps> = ({
  title,
  price,
  oldPrice,
  currency = 'ريال',
  description,
  discountPercent,
  colors,
  style,
}) => {
  const c = useColors(colors);

  return (
    <div
      style={{
        position: 'relative',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-end',
        gap: '8px',
        padding: '24px',
        borderRadius: '20px',
        background: hexRgba(c.accent, '0.08'),
        border: `1px solid ${hexRgba(c.accent, '0.2')}`,
        direction: 'rtl',
        overflow: 'visible',
        ...style,
      }}
    >
      {discountPercent != null && (
        <div style={{ position: 'absolute', top: '-15px', left: '-15px' }}>
          <DiscountBadge percentage={discountPercent} size={70} colors={c} />
        </div>
      )}
      <span style={{ fontFamily: FONTS.kufi, fontSize: '18px', fontWeight: 800, color: c.text }}>{title}</span>
      <PriceStrike newPrice={price} oldPrice={oldPrice || price} currency={currency} colors={c} />
      {description && (
        <span style={{ fontFamily: FONTS.sans, fontSize: '13px', color: c.text, opacity: 0.7 }}>{description}</span>
      )}
    </div>
  );
};
