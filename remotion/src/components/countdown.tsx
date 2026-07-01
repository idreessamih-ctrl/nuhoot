// ─────────────────────────────────────────────────────────────────────
// COUNTDOWN — Time-based urgency components
//   CountdownTimer · sale countdown display with boxes (days/hours/min)
//   CountdownRing  · circular countdown ring with percentage
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

// ─── CountdownTimer ───────────────────────────────────────────────────
export interface CountdownTimerProps extends BaseBlockProps {
  /** Days remaining. */
  days: number;
  /** Hours remaining. */
  hours: number;
  /** Minutes remaining. */
  minutes: number;
  /** Optional label above the timer. */
  label?: string;
}

export const CountdownTimer: React.FC<CountdownTimerProps> = ({
  days,
  hours,
  minutes,
  label,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const units = [
    { value: days, label: 'يوم' },
    { value: hours, label: 'ساعة' },
    { value: minutes, label: 'دقيقة' },
  ];

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: '18px 50px',
        flexShrink: 0,
        direction: 'rtl',
        zIndex: 5,
        ...style,
      }}
    >
      {label && (
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            marginBottom: '14px',
          }}
        >
          <Icon name="clock" size={18} color={c.accent} colors={c} />
          <span
            style={{
              fontFamily: FONTS.kufi,
              fontSize: '16px',
              fontWeight: 700,
              color: c.text,
              direction: 'rtl',
            }}
          >
            {label}
          </span>
        </div>
      )}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          direction: 'ltr',
        }}
      >
        {units.map((unit, i) => (
          <React.Fragment key={i}>
            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                minWidth: '80px',
                padding: '14px 10px',
                borderRadius: '14px',
                background: `linear-gradient(160deg, ${hexRgba(
                  c.accent,
                  '0.16',
                )}, ${hexRgba(c.accent2, '0.1')})`,
                border: `1px solid ${hexRgba(c.accent, '0.3')}`,
              }}
            >
              <span
                style={{
                  fontFamily: FONTS.kufi,
                  fontSize: '34px',
                  fontWeight: 900,
                  color: c.text,
                  lineHeight: 1,
                  direction: 'ltr',
                }}
              >
                {toArabicDigits(String(unit.value).padStart(2, '0'))}
              </span>
              <span
                style={{
                  fontFamily: FONTS.sans,
                  fontSize: '12px',
                  fontWeight: 600,
                  color: c.accent,
                  marginTop: '6px',
                  direction: 'rtl',
                }}
              >
                {unit.label}
              </span>
            </div>
            {i < units.length - 1 && (
              <span
                style={{
                  fontFamily: FONTS.kufi,
                  fontSize: '28px',
                  fontWeight: 900,
                  color: c.accent2,
                  lineHeight: 1,
                }}
              >
                :
              </span>
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};

// ─── CountdownRing ────────────────────────────────────────────────────
export interface CountdownRingProps extends BaseBlockProps {
  /** Percentage complete (0–100). */
  percentage: number;
  /** Label inside the ring. */
  label?: string;
  /** Ring diameter in px. Default 140. */
  size?: number;
}

export const CountdownRing: React.FC<CountdownRingProps> = ({
  percentage,
  label,
  size = 140,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const pct = Math.max(0, Math.min(100, percentage));
  const radius = (size - 16) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (pct / 100) * circumference;

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '18px 50px',
        flexShrink: 0,
        direction: 'rtl',
        zIndex: 5,
        ...style,
      }}
    >
      <div
        style={{
          position: 'relative',
          width: `${size}px`,
          height: `${size}px`,
        }}
      >
        <svg
          width={size}
          height={size}
          viewBox={`0 0 ${size} ${size}`}
          style={{ display: 'block', transform: 'rotate(-90deg)' }}
        >
          {/* Track */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke={hexRgba(c.accent, '0.12')}
            strokeWidth="10"
          />
          {/* Progress */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke={c.accent}
            strokeWidth="10"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
          />
        </svg>
        {/* Center content */}
        <div
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <span
            style={{
              fontFamily: FONTS.kufi,
              fontSize: '30px',
              fontWeight: 900,
              color: c.text,
              lineHeight: 1,
              direction: 'ltr',
            }}
          >
            {toArabicDigits(pct)}%
          </span>
          {label && (
            <span
              style={{
                fontFamily: FONTS.sans,
                fontSize: '12px',
                fontWeight: 600,
                color: c.text,
                opacity: 0.7,
                marginTop: '4px',
                direction: 'rtl',
              }}
            >
              {label}
            </span>
          )}
        </div>
      </div>
    </div>
  );
};
