// ─────────────────────────────────────────────────────────────────────
// COUNTERS — Numeric display components
//   StatCounter     · large number with label (e.g. "500+ عميل")
//   NumberTicker    · row of 3–4 animated-style numbers
//   AchievementBar  · labeled progress with icon
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

// ─── StatCounter ───────────────────────────────────────────────────────
export interface StatCounterProps extends BaseBlockProps {
  /** The numeric value (e.g. 500, "4.8"). */
  value: string | number;
  /** Label below the number (e.g. "عميل"). */
  label: string;
  /** Suffix appended to number (e.g. "+", "%"). */
  suffix?: string;
}

export const StatCounter: React.FC<StatCounterProps> = ({
  value,
  label,
  suffix,
  colors,
  style,
}) => {
  const c = useColors(colors);

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '20px 50px',
        flexShrink: 0,
        direction: 'rtl',
        zIndex: 5,
        ...style,
      }}
    >
      <div
        style={{
          display: 'flex',
          alignItems: 'baseline',
          gap: '3px',
          direction: 'ltr',
        }}
      >
        <span
          style={{
            fontFamily: FONTS.kufi,
            fontSize: '64px',
            fontWeight: 900,
            color: c.accent,
            lineHeight: 1,
            direction: 'ltr',
          }}
        >
          {toArabicDigits(value)}
        </span>
        {suffix && (
          <span
            style={{
              fontFamily: FONTS.kufi,
              fontSize: '34px',
              fontWeight: 800,
              color: c.accent2,
              direction: 'ltr',
            }}
          >
            {suffix}
          </span>
        )}
      </div>
      <span
        style={{
          fontFamily: FONTS.sans,
          fontSize: '16px',
          fontWeight: 600,
          color: c.text,
          opacity: 0.8,
          marginTop: '8px',
          direction: 'rtl',
        }}
      >
        {label}
      </span>
    </div>
  );
};

// ─── NumberTicker ─────────────────────────────────────────────────────
export interface TickerItem {
  value: string | number;
  label: string;
}

export interface NumberTickerProps extends BaseBlockProps {
  /** Array of {value, label} — up to 4 shown. */
  numbers: TickerItem[];
  /** Gap between items in px. Default 20. */
  gap?: number;
}

export const NumberTicker: React.FC<NumberTickerProps> = ({
  numbers,
  gap = 20,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const data = numbers.slice(0, 4);

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
      {data.map((item, i) => (
        <div
          key={i}
          style={{
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '22px 10px',
            borderRadius: '18px',
            background: hexRgba(c.accent, '0.07'),
            border: `1px solid ${hexRgba(c.accent, '0.14')}`,
            textAlign: 'center',
          }}
        >
          {/* Faux ticker bar above number for "animated" feel */}
          <div
            style={{
              width: '40px',
              height: '4px',
              borderRadius: '2px',
              background: `linear-gradient(90deg, ${c.accent}, ${c.accent2})`,
              marginBottom: '12px',
            }}
          />
          <span
            style={{
              fontFamily: FONTS.kufi,
              fontSize: '38px',
              fontWeight: 900,
              color: c.accent,
              lineHeight: 1,
              direction: 'ltr',
            }}
          >
            {toArabicDigits(item.value)}
          </span>
          <span
            style={{
              fontFamily: FONTS.sans,
              fontSize: '13px',
              fontWeight: 600,
              color: c.text,
              opacity: 0.75,
              marginTop: '8px',
              direction: 'rtl',
            }}
          >
            {item.label}
          </span>
        </div>
      ))}
    </div>
  );
};

// ─── AchievementBar ───────────────────────────────────────────────────
export interface AchievementBarProps extends BaseBlockProps {
  /** Title / label for the achievement. */
  title: string;
  /** Current value. */
  value: number;
  /** Maximum value (bar fills value/max). */
  max: number;
  /** Lucide icon name. Default 'award'. */
  icon?: string;
}

export const AchievementBar: React.FC<AchievementBarProps> = ({
  title,
  value,
  max,
  icon = 'award',
  colors,
  style,
}) => {
  const c = useColors(colors);
  const pct = max > 0 ? Math.min(100, Math.round((value / max) * 100)) : 0;

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        padding: '16px 50px',
        flexShrink: 0,
        direction: 'rtl',
        zIndex: 5,
        ...style,
      }}
    >
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          justifyContent: 'flex-end',
          direction: 'rtl',
          marginBottom: '10px',
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
            {title}
          </span>
          <span
            style={{
              fontFamily: FONTS.sans,
              fontSize: '13px',
              fontWeight: 600,
              color: c.accent,
              direction: 'ltr',
            }}
          >
            {toArabicDigits(value)} / {toArabicDigits(max)}
          </span>
        </div>
        <div
          style={{
            width: '40px',
            height: '40px',
            borderRadius: '10px',
            background: `linear-gradient(135deg, ${c.accent}, ${c.accent2})`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexShrink: 0,
          }}
        >
          <Icon name={icon} size={22} color={c.badgeText} colors={c} />
        </div>
      </div>
      {/* Track */}
      <div
        style={{
          position: 'relative',
          width: '100%',
          height: '12px',
          borderRadius: '6px',
          background: hexRgba(c.accent, '0.1'),
          overflow: 'hidden',
          direction: 'ltr',
        }}
      >
        <div
          style={{
            width: `${pct}%`,
            height: '100%',
            borderRadius: '6px',
            background: `linear-gradient(90deg, ${c.accent2}, ${c.accent})`,
          }}
        />
      </div>
    </div>
  );
};
