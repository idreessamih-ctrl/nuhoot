// ─────────────────────────────────────────────────────────────────────
// PROGRESS — Progress bars, rings, and meters
//   BarProgress · horizontal progress bar
//   RingProgress · circular progress ring
//   GoalMeter · goal/milestone meter with label
//
// Inspired by: Tremor ProgressBar (Apache-2.0), RVE progress patterns
// ─────────────────────────────────────────────────────────────────────

import React from 'react';
import { BaseBlockProps, ColorConfig, FONTS, hexRgba, toArabicDigits, useColors } from './helpers';

// ─── BarProgress ──────────────────────────────────────────────────────
export interface BarProgressProps extends BaseBlockProps {
  /** Progress value 0-100. */
  value: number;
  /** Label text. */
  label?: string;
  /** Show percentage text. Default true. */
  showPercent?: boolean;
  /** Bar height. Default 12. */
  height?: number;
  /** Color override for the fill. */
  fillColor?: string;
}

export const BarProgress: React.FC<BarProgressProps> = ({
  value,
  label,
  showPercent = true,
  height = 12,
  fillColor,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const clamped = Math.max(0, Math.min(100, value));
  const fill = fillColor ?? c.accent;

  return (
    <div style={{ padding: '8px 50px', flexShrink: 0, direction: 'rtl', zIndex: 5, ...style }}>
      {(label || showPercent) && (
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
          {label && <span style={{ fontFamily: FONTS.sans, fontSize: '14px', fontWeight: 600, color: c.text }}>{label}</span>}
          {showPercent && (
            <span style={{ fontFamily: FONTS.kufi, fontSize: '14px', fontWeight: 800, color: fill }}>
              {toArabicDigits(clamped)}%
            </span>
          )}
        </div>
      )}
      <div
        style={{
          width: '100%',
          height: `${height}px`,
          borderRadius: `${height / 2}px`,
          background: hexRgba(c.accent, '0.1'),
          overflow: 'hidden',
        }}
      >
        <div
          style={{
            width: `${clamped}%`,
            height: '100%',
            borderRadius: `${height / 2}px`,
            background: `linear-gradient(90deg, ${fill}, ${c.accent2})`,
            boxShadow: `0 0 10px ${hexRgba(fill, '0.5')}`,
          }}
        />
      </div>
    </div>
  );
};

// ─── RingProgress ──────────────────────────────────────────────────────
export interface RingProgressProps extends BaseBlockProps {
  /** Progress value 0-100. */
  value: number;
  /** Center text (e.g. "75%"). */
  centerText?: string;
  /** Ring size (diameter). Default 120. */
  size?: number;
  /** Stroke width. Default 10. */
  strokeWidth?: number;
}

export const RingProgress: React.FC<RingProgressProps> = ({
  value,
  centerText,
  size = 120,
  strokeWidth = 10,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const clamped = Math.max(0, Math.min(100, value));
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (clamped / 100) * circumference;
  const centerTextDisplay = centerText ?? `${toArabicDigits(clamped)}%`;

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '12px', flexShrink: 0, zIndex: 5, ...style }}>
      <div style={{ position: 'relative', width: `${size}px`, height: `${size}px` }}>
        <svg width={size} height={size} style={{ transform: 'rotate(-90deg)' }}>
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke={hexRgba(c.accent, '0.1')}
            strokeWidth={strokeWidth}
          />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke={c.accent}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
          />
        </svg>
        <div style={{
          position: 'absolute', inset: 0,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
        }}>
          <span style={{ fontFamily: FONTS.kufi, fontSize: `${size * 0.2}px`, fontWeight: 900, color: c.text }}>
            {centerTextDisplay}
          </span>
        </div>
      </div>
    </div>
  );
};

// ─── GoalMeter ─────────────────────────────────────────────────────────
export interface GoalMeterProps extends BaseBlockProps {
  current: number;
  goal: number;
  label?: string;
  /** Unit (e.g. "عميل", "حجز"). */
  unit?: string;
}

export const GoalMeter: React.FC<GoalMeterProps> = ({
  current,
  goal,
  label,
  unit = '',
  colors,
  style,
}) => {
  const c = useColors(colors);
  const percent = Math.min(100, (current / goal) * 100);

  return (
    <div style={{ padding: '12px 50px', flexShrink: 0, direction: 'rtl', zIndex: 5, ...style }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '8px' }}>
        <span style={{ fontFamily: FONTS.sans, fontSize: '14px', fontWeight: 600, color: c.text }}>
          {label || 'الهدف'}
        </span>
        <span style={{ fontFamily: FONTS.kufi, fontSize: '16px', fontWeight: 800, color: c.accent }}>
          {toArabicDigits(current)} / {toArabicDigits(goal)} {unit}
        </span>
      </div>
      <div style={{ width: '100%', height: '8px', borderRadius: '4px', background: hexRgba(c.accent, '0.1'), overflow: 'hidden' }}>
        <div style={{
          width: `${percent}%`, height: '100%', borderRadius: '4px',
          background: `linear-gradient(90deg, ${c.accent}, ${c.accent2})`,
        }} />
      </div>
    </div>
  );
};
