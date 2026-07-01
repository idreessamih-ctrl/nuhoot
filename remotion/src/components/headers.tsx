// ─────────────────────────────────────────────────────────────────────
// HEADERS — 5 components (4 modified + 1 new)
//   HeaderMinimal  · kicker + headline + business name (MODIFIED: letterSpacing, font selection)
//   HeaderGradient · gradient band header (MODIFIED: gradient text, gradientAngle)
//   HeaderSplit    · split header (MODIFIED: letterSpacing)
//   HeaderOverlay  · photo overlay header (MODIFIED: gradient text)
//   ── NEW ──
//   HeaderMixed    · multi-font headline with gradient text (Technique 1.2, 2.6)
// ─────────────────────────────────────────────────────────────────────

import React from 'react';
import {
  BaseBlockProps,
  ColorConfig,
  FONTS,
  hexRgba,
  optimalFontSize,
  resolvePhoto,
  useColors,
  gradientTextStyle,
  goldFoilTextStyle,
  typeScale,
} from './helpers';

// ─── HeaderMinimal (MODIFIED: font selection, letterSpacing, typeScale) ─
export interface HeaderMinimalProps extends BaseBlockProps {
  kicker?: string;
  headline: string;
  businessName?: string;
  headlineSize?: number;
  align?: 'right' | 'left' | 'center';
  /** Font family. Default 'kufi'. Use 'naskh' for traditional niches. */
  font?: 'kufi' | 'naskh' | 'sans';
  /** Letter spacing for headline. Default 0. */
  letterSpacing?: string;
  /** Type scale ratio. Default 1.333. */
  typeRatio?: number;
  /** Use gradient text fill. Default false. */
  useGradientText?: boolean;
}

export const HeaderMinimal: React.FC<HeaderMinimalProps> = ({
  kicker,
  headline,
  businessName,
  headlineSize = 44,
  align = 'right',
  font = 'kufi',
  letterSpacing = '0',
  typeRatio = 1.333,
  useGradientText = false,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const hs = optimalFontSize(headline, 850, headlineSize);
  const isCenter = align === 'center';
  const alignItems =
    align === 'center' ? 'center' : align === 'left' ? 'flex-start' : 'flex-end';
  const fontFamily = font === 'naskh' ? FONTS.naskh : font === 'sans' ? FONTS.sans : FONTS.kufi;
  const gradientStyle = useGradientText ? gradientTextStyle(c.accent, c.accent2) : {};

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems,
        padding: '40px 50px 0 50px',
        flexShrink: 0,
        direction: 'rtl',
        textAlign: align,
        zIndex: 5,
        ...style,
      }}
    >
      {kicker && (
        <span
          style={{
            fontFamily: FONTS.lato,
            fontSize: '15px',
            fontWeight: 700,
            letterSpacing: '0.25em',
            color: c.accent,
            textTransform: 'uppercase',
            direction: 'ltr',
            textAlign: align === 'center' ? 'center' : 'left',
          }}
        >
          {kicker}
        </span>
      )}
      <h1
        style={{
          fontFamily,
          fontSize: `${hs}px`,
          fontWeight: 900,
          color: useGradientText ? 'transparent' : c.text,
          lineHeight: 1.25,
          direction: 'rtl',
          textAlign: align,
          margin: '8px 0 0 0',
          letterSpacing,
          ...gradientStyle,
          textShadow: c.isDark && !useGradientText
            ? '0 2px 12px rgba(0,0,0,0.5)'
            : useGradientText ? 'none' : '0 2px 8px rgba(255,255,255,0.4)',
        }}
      >
        {headline}
      </h1>
      <div
        style={{
          width: '70px',
          height: '3px',
          borderRadius: '2px',
          marginTop: '12px',
          opacity: 0.9,
          background: `linear-gradient(90deg, ${c.accent}, ${c.accent2})`,
          alignSelf: alignItems,
        }}
      />
      {businessName && (
        <span
          style={{
            fontFamily: FONTS.kufi,
            fontSize: '20px',
            fontWeight: 500,
            color: c.accent2,
            marginTop: '8px',
            direction: 'rtl',
            textAlign: align,
          }}
        >
          {businessName}
        </span>
      )}
    </div>
  );
};

// ─── HeaderGradient (MODIFIED: gradient text, gradientAngle) ──────────
export interface HeaderGradientProps extends HeaderMinimalProps {
  gradient?: [string, string];
  bandHeight?: number;
  bandOpacity?: number;
}

export const HeaderGradient: React.FC<HeaderGradientProps> = ({
  kicker,
  headline,
  businessName,
  headlineSize = 44,
  align = 'right',
  font = 'kufi',
  letterSpacing = '0',
  useGradientText = false,
  gradient,
  bandHeight = 220,
  bandOpacity = 0.12,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const [g1, g2] = gradient ?? [c.accent, c.accent2];
  const hs = optimalFontSize(headline, 850, headlineSize);
  const alignItems =
    align === 'center' ? 'center' : align === 'left' ? 'flex-start' : 'flex-end';
  const fontFamily = font === 'naskh' ? FONTS.naskh : font === 'sans' ? FONTS.sans : FONTS.kufi;
  const gradientStyle = useGradientText ? gradientTextStyle(c.accent, c.accent2) : {};
  const angle = c.gradientAngle ?? 135;

  return (
    <div
      style={{
        position: 'relative',
        padding: '40px 50px 20px 50px',
        flexShrink: 0,
        direction: 'rtl',
        textAlign: align,
        zIndex: 5,
        ...style,
      }}
    >
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: `${bandHeight}px`,
          background: `linear-gradient(${angle}deg, ${hexRgba(g1, String(bandOpacity))} 0%, ${hexRgba(g2, String(bandOpacity))} 100%)`,
          borderRadius: '0 0 24px 24px',
        }}
      />
      <div style={{ position: 'relative', display: 'flex', flexDirection: 'column', alignItems }}>
        {kicker && (
          <span
            style={{
              fontFamily: FONTS.lato,
              fontSize: '15px',
              fontWeight: 700,
              letterSpacing: '0.25em',
              color: c.accent,
              textTransform: 'uppercase',
              direction: 'ltr',
              textAlign: align === 'center' ? 'center' : 'left',
            }}
          >
            {kicker}
          </span>
        )}
        <h1
          style={{
            fontFamily,
            fontSize: `${hs}px`,
            fontWeight: 900,
            color: useGradientText ? 'transparent' : c.text,
            lineHeight: 1.25,
            direction: 'rtl',
            textAlign: align,
            margin: '8px 0 0 0',
            letterSpacing,
            ...gradientStyle,
            textShadow: c.isDark && !useGradientText
              ? '0 2px 12px rgba(0,0,0,0.5)'
              : useGradientText ? 'none' : '0 2px 8px rgba(255,255,255,0.4)',
          }}
        >
          {headline}
        </h1>
        <div
          style={{
            width: '70px',
            height: '3px',
            borderRadius: '2px',
            marginTop: '12px',
            opacity: 0.9,
            background: `linear-gradient(90deg, ${c.accent}, ${c.accent2})`,
            alignSelf: alignItems,
          }}
        />
        {businessName && (
          <span
            style={{
              fontFamily: FONTS.kufi,
              fontSize: '20px',
              fontWeight: 500,
              color: c.accent2,
              marginTop: '8px',
              direction: 'rtl',
              textAlign: align,
            }}
          >
            {businessName}
          </span>
        )}
      </div>
    </div>
  );
};

// ─── HeaderSplit (MODIFIED: letterSpacing, font selection) ─────────────
export interface HeaderSplitProps extends BaseBlockProps {
  kicker?: string;
  headline: string;
  businessName?: string;
  headlineSize?: number;
  headlineSide?: 'left' | 'right';
  font?: 'kufi' | 'naskh' | 'sans';
  letterSpacing?: string;
}

export const HeaderSplit: React.FC<HeaderSplitProps> = ({
  kicker,
  headline,
  businessName,
  headlineSize = 40,
  headlineSide = 'right',
  font = 'kufi',
  letterSpacing = '0',
  colors,
  style,
}) => {
  const c = useColors(colors);
  const hs = optimalFontSize(headline, 480, headlineSize);
  const headlineOnRight = headlineSide === 'right';
  const fontFamily = font === 'naskh' ? FONTS.naskh : font === 'sans' ? FONTS.sans : FONTS.kufi;

  const headlineBlock = (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        flex: 1,
        alignItems: headlineOnRight ? 'flex-end' : 'flex-start',
        direction: 'rtl',
        textAlign: headlineOnRight ? 'right' : 'left',
      }}
    >
      {kicker && (
        <span
          style={{
            fontFamily: FONTS.lato,
            fontSize: '14px',
            fontWeight: 700,
            letterSpacing: '0.2em',
            color: c.accent,
            textTransform: 'uppercase',
            direction: 'ltr',
            textAlign: 'left',
            marginBottom: '6px',
          }}
        >
          {kicker}
        </span>
      )}
      <h1
        style={{
          fontFamily,
          fontSize: `${hs}px`,
          fontWeight: 900,
          color: c.text,
          lineHeight: 1.2,
          margin: 0,
          letterSpacing,
          textShadow: c.isDark
            ? '0 2px 10px rgba(0,0,0,0.4)'
            : '0 2px 8px rgba(255,255,255,0.4)',
        }}
      >
        {headline}
      </h1>
    </div>
  );

  const businessBlock = businessName ? (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: headlineOnRight ? 'flex-start' : 'flex-end',
        justifyContent: 'center',
        direction: 'rtl',
        textAlign: headlineOnRight ? 'left' : 'right',
        paddingLeft: headlineOnRight ? '24px' : 0,
        paddingRight: headlineOnRight ? 0 : '24px',
        borderLeft: headlineOnRight
          ? `2px solid ${hexRgba(c.accent, '0.3')}`
          : 'none',
        borderRight: headlineOnRight
          ? 'none'
          : `2px solid ${hexRgba(c.accent, '0.3')}`,
      }}
    >
      <span
        style={{
          fontFamily: FONTS.kufi,
          fontSize: '22px',
          fontWeight: 700,
          color: c.accent2,
          direction: 'rtl',
        }}
      >
        {businessName}
      </span>
      <span
        style={{
          fontFamily: FONTS.lato,
          fontSize: '12px',
          color: c.text,
          opacity: 0.6,
          letterSpacing: '0.15em',
          textTransform: 'uppercase',
          marginTop: '4px',
        }}
      >
        nuhoot.xyz
      </span>
    </div>
  ) : null;

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        padding: '40px 50px 10px 50px',
        flexShrink: 0,
        direction: 'rtl',
        zIndex: 5,
        ...style,
      }}
    >
      {headlineOnRight ? (
        <>
          {businessBlock}
          {headlineBlock}
        </>
      ) : (
        <>
          {headlineBlock}
          {businessBlock}
        </>
      )}
    </div>
  );
};

// ─── HeaderOverlay (MODIFIED: gradient text) ──────────────────────────
export interface HeaderOverlayProps extends BaseBlockProps {
  kicker?: string;
  headline: string;
  businessName?: string;
  photoPath: string;
  headlineSize?: number;
  overlayOpacity?: number;
  useGradientText?: boolean;
}

export const HeaderOverlay: React.FC<HeaderOverlayProps> = ({
  kicker,
  headline,
  businessName,
  photoPath,
  headlineSize = 48,
  overlayOpacity = 0.45,
  useGradientText = false,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const hs = optimalFontSize(headline, 900, headlineSize);
  const url = resolvePhoto(photoPath);
  const gradientStyle = useGradientText ? gradientTextStyle(c.accent, c.accent2) : {};

  return (
    <div
      style={{
        position: 'relative',
        width: '100%',
        height: '360px',
        flexShrink: 0,
        overflow: 'hidden',
        direction: 'rtl',
        zIndex: 5,
        ...style,
      }}
    >
      {url && (
        <img
          src={url}
          style={{
            position: 'absolute',
            inset: 0,
            width: '100%',
            height: '100%',
            objectFit: 'cover',
          }}
        />
      )}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: `linear-gradient(180deg, ${hexRgba(c.bg2, String(overlayOpacity * 0.6))} 0%, ${hexRgba(c.bg2, String(overlayOpacity))} 100%)`,
        }}
      />
      <div
        style={{
          position: 'relative',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-end',
          justifyContent: 'center',
          height: '100%',
          padding: '0 50px',
          textAlign: 'right',
          direction: 'rtl',
        }}
      >
        {kicker && (
          <span
            style={{
              fontFamily: FONTS.lato,
              fontSize: '15px',
              fontWeight: 700,
              letterSpacing: '0.25em',
              color: c.accent,
              textTransform: 'uppercase',
              direction: 'ltr',
              textAlign: 'left',
              textShadow: '0 2px 8px rgba(0,0,0,0.6)',
            }}
          >
            {kicker}
          </span>
        )}
        <h1
          style={{
            fontFamily: FONTS.kufi,
            fontSize: `${hs}px`,
            fontWeight: 900,
            color: useGradientText ? 'transparent' : '#FFFFFF',
            lineHeight: 1.25,
            margin: '8px 0 0 0',
            textAlign: 'right',
            direction: 'rtl',
            ...gradientStyle,
            textShadow: useGradientText ? 'none' : '0 3px 16px rgba(0,0,0,0.7)',
          }}
        >
          {headline}
        </h1>
        <div
          style={{
            width: '80px',
            height: '3px',
            borderRadius: '2px',
            marginTop: '12px',
            background: `linear-gradient(90deg, ${c.accent}, ${c.accent2})`,
          }}
        />
        {businessName && (
          <span
            style={{
              fontFamily: FONTS.kufi,
              fontSize: '20px',
              fontWeight: 600,
              color: c.accent2,
              marginTop: '8px',
              direction: 'rtl',
              textShadow: '0 2px 10px rgba(0,0,0,0.5)',
            }}
          >
            {businessName}
          </span>
        )}
      </div>
    </div>
  );
};

// ═════════════════════════════════════════════════════════════════════
// NEW HEADER COMPONENT
// ═════════════════════════════════════════════════════════════════════

// ─── HeaderMixed (Technique 1.2, 2.6) — Multi-font headline w/ gradient ─
export interface HeaderMixedProps extends BaseBlockProps {
  kicker?: string;
  /** Main headline (first part). */
  headline: string;
  /** Accent word rendered in different font/color (optional). */
  accentWord?: string;
  businessName?: string;
  headlineSize?: number;
  align?: 'right' | 'left' | 'center';
  /** Font for main headline. Default 'kufi'. */
  mainFont?: 'kufi' | 'naskh' | 'sans';
  /** Font for accent word. Default 'naskh'. */
  accentFont?: 'kufi' | 'naskh' | 'sans';
  /** Accent word style. Default 'gold'. */
  accentStyle?: 'gold' | 'gradient' | 'solid';
}

export const HeaderMixed: React.FC<HeaderMixedProps> = ({
  kicker,
  headline,
  accentWord,
  businessName,
  headlineSize = 44,
  align = 'right',
  mainFont = 'kufi',
  accentFont = 'naskh',
  accentStyle = 'gold',
  colors,
  style,
}) => {
  const c = useColors(colors);
  const hs = optimalFontSize(headline + (accentWord || ''), 850, headlineSize);
  const alignItems =
    align === 'center' ? 'center' : align === 'left' ? 'flex-start' : 'flex-end';
  const mainFamily = mainFont === 'naskh' ? FONTS.naskh : mainFont === 'sans' ? FONTS.sans : FONTS.kufi;
  const accentFamily = accentFont === 'naskh' ? FONTS.naskh : accentFont === 'sans' ? FONTS.sans : FONTS.kufi;

  const accentTextStyle: React.CSSProperties =
    accentStyle === 'gold' ? goldFoilTextStyle()
    : accentStyle === 'gradient' ? gradientTextStyle(c.accent, c.accent2)
    : { color: c.accent };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems,
        padding: '40px 50px 0 50px',
        flexShrink: 0,
        direction: 'rtl',
        textAlign: align,
        zIndex: 5,
        ...style,
      }}
    >
      {kicker && (
        <span
          style={{
            fontFamily: FONTS.lato,
            fontSize: '15px',
            fontWeight: 700,
            letterSpacing: '0.25em',
            color: c.accent,
            textTransform: 'uppercase',
            direction: 'ltr',
            textAlign: align === 'center' ? 'center' : 'left',
          }}
        >
          {kicker}
        </span>
      )}
      <h1
        style={{
          fontSize: `${hs}px`,
          fontWeight: 900,
          lineHeight: 1.25,
          direction: 'rtl',
          textAlign: align,
          margin: '8px 0 0 0',
          textShadow: '0 2px 12px rgba(0,0,0,0.5)',
        }}
      >
        <span style={{ fontFamily: mainFamily, color: c.text }}>
          {headline}
        </span>
        {accentWord && (
          <span style={{ fontFamily: accentFamily, ...accentTextStyle }}>
            {' '}{accentWord}
          </span>
        )}
      </h1>
      <div
        style={{
          width: '70px',
          height: '3px',
          borderRadius: '2px',
          marginTop: '12px',
          opacity: 0.9,
          background: `linear-gradient(90deg, ${c.accent}, ${c.accent2})`,
          alignSelf: alignItems,
        }}
      />
      {businessName && (
        <span
          style={{
            fontFamily: FONTS.kufi,
            fontSize: '20px',
            fontWeight: 500,
            color: c.accent2,
            marginTop: '8px',
            direction: 'rtl',
            textAlign: align,
          }}
        >
          {businessName}
        </span>
      )}
    </div>
  );
};
