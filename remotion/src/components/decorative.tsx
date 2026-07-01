// ─────────────────────────────────────────────────────────────────────
// DECORATIVE — 10 components (4 original + 6 new)
//   DecorShapes      · scattered circles/diamonds
//   DecorRings       · concentric ring frames
//   DecorWatermark   · large faint background text/number
//   DecorGradient    · gradient color plate
//   ── NEW ──
//   Divider          · accent line with decorative center (Technique 5.1)
//   EdgeLabel        · rotated vertical text on canvas edge (Technique 5.5)
//   DecorVignette    · radial darkening at edges (Technique 4.8)
//   DecorDiagonal    · diagonal accent line (Technique 8.2)
//   ColorPanel       · solid color section background (Technique 2.4)
//   DecorCalligraphy · Arabic calligraphic stroke decoration (Technique 10.1)
// ─────────────────────────────────────────────────────────────────────

import React from 'react';
import { BaseBlockProps, ColorConfig, FONTS, hexRgba, toArabicDigits, useColors, vignetteStyle } from './helpers';

// ─── DecorShapes ──────────────────────────────────────────────────────
export interface DecorShape {
  x: number;
  y: number;
  size: number;
  type: 'circle' | 'diamond';
  color?: string;
  opacity?: number;
}

export interface DecorShapesProps extends BaseBlockProps {
  shapes?: DecorShape[];
  count?: number;
  opacityMult?: number;
}

const DEFAULT_SHAPES: DecorShape[] = [
  { x: 70, y: 180, size: 40, type: 'circle' },
  { x: 980, y: 160, size: 45, type: 'diamond' },
  { x: 50, y: 440, size: 30, type: 'circle' },
  { x: 1010, y: 420, size: 35, type: 'circle' },
  { x: 100, y: 680, size: 38, type: 'diamond' },
  { x: 970, y: 700, size: 32, type: 'circle' },
  { x: 130, y: 880, size: 25, type: 'circle' },
  { x: 930, y: 900, size: 28, type: 'diamond' },
];

export const DecorShapes: React.FC<DecorShapesProps> = ({
  shapes,
  count = 8,
  opacityMult = 1,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const list = shapes ?? DEFAULT_SHAPES.slice(0, count);
  const [a1, a2] = [c.accent, c.accent2];

  return (
    <>
      {list.map((s, i) => {
        const col = s.color ?? (i % 2 === 0 ? a2 : a1);
        const op = (s.opacity ?? (i % 2 === 0 ? 0.85 : 0.75)) * opacityMult;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              top: `${s.y}px`,
              left: `${s.x}px`,
              width: `${s.size}px`,
              height: `${s.size}px`,
              background: hexRgba(col, String(op)),
              borderRadius: s.type === 'circle' ? '50%' : '4px',
              transform: s.type === 'diamond' ? 'rotate(45deg)' : 'none',
              pointerEvents: 'none',
              ...style,
            }}
          />
        );
      })}
    </>
  );
};

// ─── DecorRings ───────────────────────────────────────────────────────
export interface DecorRing {
  size: number;
  type?: 'solid' | 'dashed';
  opacity?: number;
  color?: string;
}

export interface DecorRingsProps extends BaseBlockProps {
  rings?: DecorRing[];
  offsetY?: number;
}

const DEFAULT_RINGS: DecorRing[] = [
  { size: 760, type: 'dashed', opacity: 0.35 },
  { size: 720, type: 'solid', opacity: 0.12 },
];

export const DecorRings: React.FC<DecorRingsProps> = ({
  rings,
  offsetY = 0,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const list = rings ?? DEFAULT_RINGS;

  return (
    <>
      {list.map((ring, i) => {
        const col = ring.color ?? (i === 0 ? c.accent : c.accent2);
        const top = 165 + (750 - ring.size) / 2 + offsetY;
        const left = (1080 - ring.size) / 2;
        const border =
          ring.type === 'dashed'
            ? `4px dashed ${hexRgba(col, String(ring.opacity ?? 0.35))}`
            : `3px solid ${hexRgba(col, String(ring.opacity ?? 0.12))}`;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              top: `${top}px`,
              left: `${left}px`,
              width: `${ring.size}px`,
              height: `${ring.size}px`,
              borderRadius: '50%',
              border,
              pointerEvents: 'none',
              ...style,
            }}
          />
        );
      })}
    </>
  );
};

// ─── DecorWatermark ───────────────────────────────────────────────────
export interface DecorWatermarkProps extends BaseBlockProps {
  text: string | number;
  fontSize?: number;
  color?: string;
  opacity?: number;
  rotation?: number;
}

export const DecorWatermark: React.FC<DecorWatermarkProps> = ({
  text,
  fontSize = 400,
  color,
  opacity = 0.07,
  rotation = 0,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const col = color ?? c.accent;
  const display = typeof text === 'number' ? toArabicDigits(text) : text;

  return (
    <div
      style={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: `translate(-50%, -50%) rotate(${rotation}deg)`,
        fontSize: `${fontSize}px`,
        fontWeight: 900,
        fontFamily: FONTS.kufi,
        color: hexRgba(col, String(opacity)),
        lineHeight: 1,
        pointerEvents: 'none',
        whiteSpace: 'nowrap',
        ...style,
      }}
    >
      {display}
    </div>
  );
};

// ─── DecorGradient ────────────────────────────────────────────────────
export interface DecorGradientProps extends BaseBlockProps {
  position?: 'top' | 'bottom' | 'full';
  height?: number;
  gradient?: [string, string];
  fade?: boolean;
  /** Gradient angle in degrees. Default 135. */
  angle?: number;
}

export const DecorGradient: React.FC<DecorGradientProps> = ({
  position = 'bottom',
  height = 300,
  gradient,
  fade = true,
  angle = 135,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const [g1, g2] = gradient ?? [c.bg, c.bg2];
  const gradientAngle = c.gradientAngle ?? angle;

  if (position === 'full') {
    return (
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: `linear-gradient(${gradientAngle}deg, ${g1} 0%, ${g2} 100%)`,
          pointerEvents: 'none',
          ...style,
        }}
      />
    );
  }

  const isBottom = position === 'bottom';
  const plateStyle: React.CSSProperties = isBottom
    ? { bottom: 0, top: 'auto' }
    : { top: 0, bottom: 'auto' };

  return (
    <>
      <div
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          height: `${height}px`,
          background: g2,
          pointerEvents: 'none',
          ...plateStyle,
          ...style,
        }}
      />
      {fade && (
        <div
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            height: '100px',
            pointerEvents: 'none',
            ...(isBottom
              ? {
                  bottom: `${height}px`,
                  background: `linear-gradient(180deg, transparent 0%, ${hexRgba(g2, '0.5')} 50%, ${g2} 100%)`,
                }
              : {
                  top: `${height}px`,
                  background: `linear-gradient(0deg, transparent 0%, ${hexRgba(g2, '0.5')} 50%, ${g2} 100%)`,
                }),
          }}
        />
      )}
    </>
  );
};

// ═════════════════════════════════════════════════════════════════════
// NEW DECORATIVE COMPONENTS
// ═════════════════════════════════════════════════════════════════════

// ─── Divider (Technique 5.1) — Accent line with decorative center ────
export interface DividerProps extends BaseBlockProps {
  /** Width of the divider in px. Default 200. */
  width?: number;
  /** Height of the divider. Default 3. */
  height?: number;
  /** Center decoration character. Default '◆'. */
  centerChar?: string;
  /** Center decoration size. Default 20. */
  centerSize?: number;
  /** Alignment. Default 'center'. */
  align?: 'left' | 'center' | 'right';
}

export const Divider: React.FC<DividerProps> = ({
  width = 200,
  height = 3,
  centerChar = '◆',
  centerSize = 20,
  align = 'center',
  colors,
  style,
}) => {
  const c = useColors(colors);
  const justify = align === 'center' ? 'center' : align === 'left' ? 'flex-start' : 'flex-end';

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: justify,
        gap: '12px',
        padding: '12px 50px',
        flexShrink: 0,
        zIndex: 5,
        ...style,
      }}
    >
      <div
        style={{
          width: `${width / 2 - centerSize / 2}px`,
          height: `${height}px`,
          background: `linear-gradient(90deg, transparent, ${c.accent})`,
          borderRadius: '2px',
        }}
      />
      <span
        style={{
          fontSize: `${centerSize}px`,
          color: c.accent2,
          lineHeight: 1,
        }}
      >
        {centerChar}
      </span>
      <div
        style={{
          width: `${width / 2 - centerSize / 2}px`,
          height: `${height}px`,
          background: `linear-gradient(90deg, ${c.accent}, transparent)`,
          borderRadius: '2px',
        }}
      />
    </div>
  );
};

// ─── EdgeLabel (Technique 5.5) — Rotated vertical text on canvas edge ─
export interface EdgeLabelProps extends BaseBlockProps {
  text: string;
  /** Which edge. Default 'left'. */
  side?: 'left' | 'right';
  /** Vertical position. Default 'center'. */
  vertical?: 'top' | 'center' | 'bottom';
  /** Font size. Default 14. */
  fontSize?: number;
  /** Color override. */
  color?: string;
  /** Opacity. Default 0.5. */
  opacity?: number;
}

export const EdgeLabel: React.FC<EdgeLabelProps> = ({
  text,
  side = 'left',
  vertical = 'center',
  fontSize = 14,
  color,
  opacity = 0.5,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const col = color ?? c.accent2;

  const posStyle: React.CSSProperties = {
    position: 'absolute',
    [side]: '12px',
    ...(vertical === 'top'
      ? { top: '40px' }
      : vertical === 'bottom'
        ? { bottom: '180px' }
        : { top: '50%', transform: side === 'left' ? 'translateY(-50%) rotate(-90deg)' : 'translateY(-50%) rotate(90deg)' }),
    transformOrigin: 'center',
  };

  return (
    <div
      style={{
        ...posStyle,
        fontFamily: FONTS.lato,
        fontSize: `${fontSize}px`,
        fontWeight: 700,
        letterSpacing: '0.3em',
        textTransform: 'uppercase',
        color: hexRgba(col, String(opacity)),
        direction: 'ltr',
        writingMode: vertical === 'center' ? 'horizontal-tb' : 'vertical-rl',
        pointerEvents: 'none',
        zIndex: 3,
        ...style,
      }}
    >
      {text}
    </div>
  );
};

// ─── DecorVignette (Technique 4.8) — Radial darkening at edges ────────
export interface DecorVignetteProps extends BaseBlockProps {
  /** Vignette color. Default '#000000'. */
  color?: string;
  /** Intensity 0-1. Default 0.4. */
  intensity?: number;
}

export const DecorVignette: React.FC<DecorVignetteProps> = ({
  color,
  intensity = 0.4,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const col = color ?? '#000000';

  return (
    <div
      style={{
        ...vignetteStyle(col, intensity),
        ...style,
      }}
    />
  );
};

// ─── DecorDiagonal (Technique 8.2) — Diagonal accent line ────────────
export interface DecorDiagonalProps extends BaseBlockProps {
  /** Line angle in degrees. Default -15. */
  angle?: number;
  /** Line width in px. Default 4. */
  lineWidth?: number;
  /** Line length as % of canvas. Default 60. */
  length?: number;
  /** Color override. Default accent. */
  color?: string;
  /** Opacity. Default 0.15. */
  opacity?: number;
  /** Position. Default 'center'. */
  position?: 'top' | 'center' | 'bottom';
}

export const DecorDiagonal: React.FC<DecorDiagonalProps> = ({
  angle = -15,
  lineWidth = 4,
  length = 60,
  color,
  opacity = 0.15,
  position = 'center',
  colors,
  style,
}) => {
  const c = useColors(colors);
  const col = color ?? c.accent;
  const lineLength = 1080 * (length / 100);
  const topPos = position === 'top' ? '15%' : position === 'bottom' ? '75%' : '50%';

  return (
    <div
      style={{
        position: 'absolute',
        top: topPos,
        left: '50%',
        width: `${lineLength}px`,
        height: `${lineWidth}px`,
        background: `linear-gradient(90deg, transparent, ${hexRgba(col, String(opacity))}, transparent)`,
        transform: `translateX(-50%) rotate(${angle}deg)`,
        borderRadius: `${lineWidth / 2}px`,
        pointerEvents: 'none',
        zIndex: 2,
        ...style,
      }}
    />
  );
};

// ─── ColorPanel (Technique 2.4) — Solid color section background ─────
export interface ColorPanelProps extends BaseBlockProps {
  /** Panel position. Default 'bottom'. */
  position?: 'top' | 'bottom' | 'left' | 'right';
  /** Panel size in px. Default 300. */
  size?: number;
  /** Panel color override. Default accent at 0.1 opacity. */
  panelColor?: string;
  /** Panel opacity. Default 0.1. */
  opacity?: number;
  /** Border radius. Default 0. */
  radius?: number;
}

export const ColorPanel: React.FC<ColorPanelProps> = ({
  position = 'bottom',
  size = 300,
  panelColor,
  opacity = 0.1,
  radius = 0,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const col = panelColor ?? c.accent;

  const isHorizontal = position === 'top' || position === 'bottom';
  const posStyle: React.CSSProperties = isHorizontal
    ? {
        left: 0,
        right: 0,
        height: `${size}px`,
        ...(position === 'bottom' ? { bottom: 0 } : { top: 0 }),
      }
    : {
        top: 0,
        bottom: 0,
        width: `${size}px`,
        ...(position === 'right' ? { right: 0 } : { left: 0 }),
      };

  const radiusStyle: React.CSSProperties =
    radius > 0
      ? position === 'bottom'
        ? { borderRadius: `${radius}px ${radius}px 0 0` }
        : position === 'top'
          ? { borderRadius: `0 0 ${radius}px ${radius}px` }
          : { borderRadius: radius }
      : {};

  return (
    <div
      style={{
        position: 'absolute',
        ...posStyle,
        background: hexRgba(col, String(opacity)),
        pointerEvents: 'none',
        zIndex: 1,
        ...radiusStyle,
        ...style,
      }}
    />
  );
};

// ─── DecorCalligraphy (Technique 10.1) — Arabic calligraphic stroke ──
export interface DecorCalligraphyProps extends BaseBlockProps {
  /** Position X as %. Default 50. */
  posX?: number;
  /** Position Y as %. Default 50. */
  posY?: number;
  /** Size in px. Default 300. */
  size?: number;
  /** Opacity. Default 0.05. */
  opacity?: number;
  /** Color override. Default accent2. */
  color?: string;
  /** Rotation. Default 0. */
  rotation?: number;
}

export const DecorCalligraphy: React.FC<DecorCalligraphyProps> = ({
  posX = 50,
  posY = 50,
  size = 300,
  opacity = 0.05,
  color,
  rotation = 0,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const col = color ?? c.accent2;

  return (
    <svg
      style={{
        position: 'absolute',
        left: `${posX}%`,
        top: `${posY}%`,
        transform: `translate(-50%, -50%) rotate(${rotation}deg)`,
        width: `${size}px`,
        height: `${size}px`,
        opacity,
        pointerEvents: 'none',
        zIndex: 1,
        ...style,
      }}
      viewBox="0 0 200 200"
      fill="none"
    >
      {/* Flowing calligraphic stroke */}
      <path
        d="M20,100 Q60,20 100,80 T180,100 Q140,180 100,120 T20,100 Z"
        stroke={col}
        strokeWidth="3"
        fill="none"
        opacity="0.6"
      />
      <path
        d="M40,100 Q70,50 100,90 T160,100"
        stroke={col}
        strokeWidth="2"
        fill="none"
        opacity="0.4"
      />
      <circle cx="100" cy="100" r="60" stroke={col} strokeWidth="1" fill="none" opacity="0.2" />
    </svg>
  );
};
