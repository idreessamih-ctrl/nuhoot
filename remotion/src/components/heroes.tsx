// ─────────────────────────────────────────────────────────────────────
// HEROES — Hero section components
//   HeroCentered · centered hero with large headline
//   HeroSplit    · split hero with photo on one side
// ─────────────────────────────────────────────────────────────────────

import React from 'react';
import {
  BaseBlockProps,
  ColorConfig,
  FONTS,
  hexRgba,
  resolvePhoto,
  toArabicDigits,
  useColors,
} from './helpers';
import { Icon } from './icon';

// ─── HeroCentered ─────────────────────────────────────────────────────
export interface HeroCenteredProps extends BaseBlockProps {
  /** Small kicker label above headline. */
  kicker: string;
  /** Large headline. */
  headline: string;
  /** Supporting subtext. */
  subtext: string;
  /** Optional Lucide icon name displayed above kicker. */
  iconName?: string;
}

export const HeroCentered: React.FC<HeroCenteredProps> = ({
  kicker,
  headline,
  subtext,
  iconName,
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
        textAlign: 'center',
        padding: '32px 50px',
        flexShrink: 0,
        direction: 'rtl',
        zIndex: 5,
        ...style,
      }}
    >
      {iconName && (
        <div
          style={{
            width: '64px',
            height: '64px',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: `linear-gradient(135deg, ${c.accent}, ${c.accent2})`,
            marginBottom: '18px',
            boxShadow: `0 8px 24px ${hexRgba(c.accent, '0.3')}`,
          }}
        >
          <Icon name={iconName} size={32} color={c.badgeText} colors={c} />
        </div>
      )}
      {/* Kicker */}
      <div
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '6px',
          padding: '5px 16px',
          borderRadius: '20px',
          background: hexRgba(c.accent, '0.12'),
          border: `1px solid ${hexRgba(c.accent, '0.28')}`,
          marginBottom: '16px',
        }}
      >
        <span
          style={{
            fontFamily: FONTS.sans,
            fontSize: '13px',
            fontWeight: 700,
            color: c.accent,
            direction: 'rtl',
          }}
        >
          {kicker}
        </span>
      </div>
      {/* Headline */}
      <h1
        style={{
          fontFamily: FONTS.kufi,
          fontSize: '44px',
          fontWeight: 900,
          color: c.text,
          lineHeight: 1.25,
          margin: '0 0 14px 0',
          direction: 'rtl',
          maxWidth: '900px',
        }}
      >
        {headline}
      </h1>
      {/* Gradient underline accent */}
      <div
        style={{
          width: '70px',
          height: '5px',
          borderRadius: '3px',
          background: `linear-gradient(90deg, ${c.accent}, ${c.accent2})`,
          marginBottom: '16px',
        }}
      />
      {/* Subtext */}
      <p
        style={{
          fontFamily: FONTS.sans,
          fontSize: '18px',
          color: c.text,
          opacity: 0.8,
          lineHeight: 1.6,
          margin: 0,
          direction: 'rtl',
          maxWidth: '760px',
        }}
      >
        {subtext}
      </p>
    </div>
  );
};

// ─── HeroSplit ────────────────────────────────────────────────────────
export interface HeroSplitProps extends BaseBlockProps {
  /** Large headline. */
  headline: string;
  /** Optional supporting text. */
  subtext?: string;
  /** Static-file path or URL for the photo. */
  photoPath: string;
  /** Which side the photo is on. Default 'left'. */
  side?: 'left' | 'right';
  /** Optional kicker label. */
  kicker?: string;
}

export const HeroSplit: React.FC<HeroSplitProps> = ({
  headline,
  subtext,
  photoPath,
  side = 'left',
  kicker,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const photoUrl = resolvePhoto(photoPath);
  const photoFirst = side === 'left';

  const photoBlock = (
    <div
      style={{
        flex: 1,
        borderRadius: '20px',
        overflow: 'hidden',
        background: photoUrl
          ? `url(${photoUrl}) center/cover no-repeat`
          : `linear-gradient(135deg, ${c.accent}, ${c.accent2})`,
        minHeight: '240px',
        border: `1px solid ${hexRgba(c.accent, '0.2')}`,
      }}
    />
  );

  const textBlock = (
    <div
      style={{
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-end',
        textAlign: 'right',
        justifyContent: 'center',
        padding: '10px 20px',
        direction: 'rtl',
      }}
    >
      {kicker && (
        <span
          style={{
            fontFamily: FONTS.sans,
            fontSize: '14px',
            fontWeight: 700,
            color: c.accent,
            marginBottom: '12px',
            direction: 'rtl',
          }}
        >
          {kicker}
        </span>
      )}
      <h1
        style={{
          fontFamily: FONTS.kufi,
          fontSize: '36px',
          fontWeight: 900,
          color: c.text,
          lineHeight: 1.3,
          margin: '0 0 12px 0',
          direction: 'rtl',
        }}
      >
        {headline}
      </h1>
      <div
        style={{
          width: '50px',
          height: '4px',
          borderRadius: '2px',
          background: `linear-gradient(90deg, ${c.accent}, ${c.accent2})`,
          marginBottom: '14px',
        }}
      />
      {subtext && (
        <p
          style={{
            fontFamily: FONTS.sans,
            fontSize: '16px',
            color: c.text,
            opacity: 0.82,
            lineHeight: 1.6,
            margin: 0,
            direction: 'rtl',
          }}
        >
          {subtext}
        </p>
      )}
    </div>
  );

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'stretch',
        gap: '20px',
        padding: '24px 50px',
        flexShrink: 0,
        direction: 'rtl',
        zIndex: 5,
        ...style,
      }}
    >
      {photoFirst ? photoBlock : textBlock}
      {photoFirst ? textBlock : photoBlock}
    </div>
  );
};
