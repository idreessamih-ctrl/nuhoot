// ─────────────────────────────────────────────────────────────────────
// TIMELINE — Sequential / progress components
//   TimelineVertical · vertical timeline with dots
//   StepProgress     · horizontal step progress
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

// ─── TimelineVertical ─────────────────────────────────────────────────
export interface TimelineEvent {
  /** Time / date label (e.g. "٩:٠٠ ص"). */
  time: string;
  title: string;
  description: string;
}

export interface TimelineVerticalProps extends BaseBlockProps {
  /** Array of {time, title, description} — up to 5 shown. */
  events: TimelineEvent[];
}

export const TimelineVertical: React.FC<TimelineVerticalProps> = ({
  events,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const data = events.slice(0, 5);

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        padding: '18px 50px',
        flexShrink: 0,
        direction: 'rtl',
        zIndex: 5,
        ...style,
      }}
    >
      {data.map((event, i) => {
        const isLast = i === data.length - 1;
        return (
          <div
            key={i}
            style={{
              display: 'flex',
              flexDirection: 'row-reverse',
              gap: '16px',
              paddingBottom: isLast ? 0 : '22px',
            }}
          >
            {/* Dot + connector column */}
            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                flexShrink: 0,
              }}
            >
              <div
                style={{
                  width: '16px',
                  height: '16px',
                  borderRadius: '50%',
                  background: `linear-gradient(135deg, ${c.accent}, ${c.accent2})`,
                  border: `3px solid ${hexRgba(c.bg, '0.9')}`,
                  flexShrink: 0,
                  boxShadow: `0 0 0 2px ${hexRgba(c.accent, '0.3')}`,
                }}
              />
              {!isLast && (
                <div
                  style={{
                    width: '2px',
                    flex: 1,
                    minHeight: '30px',
                    background: hexRgba(c.accent, '0.25'),
                  }}
                />
              )}
            </div>
            {/* Content */}
            <div
              style={{
                flex: 1,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'flex-end',
                textAlign: 'right',
                direction: 'rtl',
                paddingBottom: isLast ? 0 : '0',
              }}
            >
              <span
                style={{
                  fontFamily: FONTS.sans,
                  fontSize: '13px',
                  fontWeight: 700,
                  color: c.accent,
                  marginBottom: '4px',
                  direction: 'rtl',
                }}
              >
                {event.time}
              </span>
              <span
                style={{
                  fontFamily: FONTS.kufi,
                  fontSize: '16px',
                  fontWeight: 800,
                  color: c.text,
                  marginBottom: '4px',
                  direction: 'rtl',
                }}
              >
                {event.title}
              </span>
              <span
                style={{
                  fontFamily: FONTS.sans,
                  fontSize: '14px',
                  color: c.text,
                  opacity: 0.72,
                  lineHeight: 1.5,
                  direction: 'rtl',
                }}
              >
                {event.description}
              </span>
            </div>
          </div>
        );
      })}
    </div>
  );
};

// ─── StepProgress ────────────────────────────────────────────────────
export interface StepItem {
  title: string;
  /** Lucide icon name. */
  icon: string;
}

export interface StepProgressProps extends BaseBlockProps {
  /** Array of {title, icon} — up to 5 shown. */
  steps: StepItem[];
  /** Index of the current step (0-based). */
  current: number;
}

export const StepProgress: React.FC<StepProgressProps> = ({
  steps,
  current,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const data = steps.slice(0, 5);

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        padding: '18px 50px',
        flexShrink: 0,
        direction: 'rtl',
        zIndex: 5,
        ...style,
      }}
    >
      <div
        style={{
          display: 'flex',
          alignItems: 'flex-start',
          justifyContent: 'space-between',
          direction: 'ltr',
        }}
      >
        {data.map((step, i) => {
          const isDone = i < current;
          const isCurrent = i === current;
          const isLast = i === data.length - 1;
          return (
            <React.Fragment key={i}>
              <div
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  flex: isLast ? undefined : 1,
                  minWidth: '70px',
                }}
              >
                {/* Circle with icon */}
                <div
                  style={{
                    width: '44px',
                    height: '44px',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    background: isDone
                      ? `linear-gradient(135deg, ${c.accent}, ${c.accent2})`
                      : isCurrent
                        ? c.accent
                        : hexRgba(c.accent, '0.12'),
                    border: `2px solid ${isDone || isCurrent ? c.accent : hexRgba(c.accent, '0.2')}`,
                    flexShrink: 0,
                    marginBottom: '8px',
                  }}
                >
                  <Icon
                    name={step.icon}
                    size={22}
                    color={isDone || isCurrent ? c.badgeText : c.accent}
                    colors={c}
                  />
                </div>
                {/* Title */}
                <span
                  style={{
                    fontFamily: FONTS.kufi,
                    fontSize: '13px',
                    fontWeight: isCurrent ? 800 : 600,
                    color: c.text,
                    opacity: isCurrent ? 1 : 0.7,
                    textAlign: 'center',
                    direction: 'rtl',
                    maxWidth: '90px',
                  }}
                >
                  {step.title}
                </span>
              </div>
              {/* Connector line */}
              {!isLast && (
                <div
                  style={{
                    flex: 1,
                    height: '3px',
                    borderRadius: '2px',
                    background:
                      i < current
                        ? `linear-gradient(90deg, ${c.accent}, ${c.accent2})`
                        : hexRgba(c.accent, '0.15'),
                    marginTop: '20px',
                    marginHorizontal: '4px',
                    marginLeft: '4px',
                    marginRight: '4px',
                  }}
                />
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};
