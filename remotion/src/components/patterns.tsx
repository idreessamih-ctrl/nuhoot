// ─────────────────────────────────────────────────────────────────────
// PATTERNS — 8 components (5 original + 3 new)
//   PatternGrid   · grid lines pattern
//   PatternDots   · dot matrix pattern
//   PatternHex    · hexagonal pattern
//   PatternRays   · radiating light rays
//   PatternBokeh  · floating bokeh circles
//   ── NEW ──
//   TextureGrain     · SVG noise/grain overlay (Technique 5.4)
//   PatternIslamic   · Islamic geometric pattern (Technique 10.2)
//   TextureOverlay   · Niche-specific texture overlay (Technique 9.4)
// ─────────────────────────────────────────────────────────────────────

import React from 'react';
import { BaseBlockProps, ColorConfig, hexRgba, useColors } from './helpers';

// ─── PatternGrid ──────────────────────────────────────────────────────
export interface PatternGridProps extends BaseBlockProps {
  cellSize?: number;
  lineWidth?: number;
  opacity?: number;
}

export const PatternGrid: React.FC<PatternGridProps> = ({
  cellSize = 40,
  lineWidth = 1,
  opacity = 0.08,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const col = hexRgba(c.accent, String(opacity));

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        backgroundImage: `linear-gradient(${col} ${lineWidth}px, transparent ${lineWidth}px), linear-gradient(90deg, ${col} ${lineWidth}px, transparent ${lineWidth}px)`,
        backgroundSize: `${cellSize}px ${cellSize}px`,
        pointerEvents: 'none',
        ...style,
      }}
    />
  );
};

// ─── PatternDots ───────────────────────────────────────────────────────
export interface PatternDotsProps extends BaseBlockProps {
  spacing?: number;
  dotSize?: number;
  opacity?: number;
}

export const PatternDots: React.FC<PatternDotsProps> = ({
  spacing = 30,
  dotSize = 2,
  opacity = 0.12,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const col = hexRgba(c.accent2, String(opacity));

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        backgroundImage: `radial-gradient(${col} ${dotSize}px, transparent ${dotSize}px)`,
        backgroundSize: `${spacing}px ${spacing}px`,
        pointerEvents: 'none',
        ...style,
      }}
    />
  );
};

// ─── PatternHex ────────────────────────────────────────────────────────
export interface PatternHexProps extends BaseBlockProps {
  size?: number;
  opacity?: number;
}

export const PatternHex: React.FC<PatternHexProps> = ({
  size = 30,
  opacity = 0.06,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const col = hexRgba(c.accent, String(opacity));
  const w = size * Math.sqrt(3);
  const h = size * 1.5;

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        backgroundImage: `url("data:image/svg+xml,${encodeURIComponent(
          `<svg xmlns='http://www.w3.org/2000/svg' width='${w * 2}' height='${h * 2}' viewBox='0 0 ${w * 2} ${h * 2}'>` +
          `<polygon points='${w},${0} ${w * 1.5},${h * 0.25} ${w * 1.5},${h * 0.75} ${w},${h} ${w * 0.5},${h * 0.75} ${w * 0.5},${h * 0.25}' fill='none' stroke='${col.replace(/rgba?\(|\)|\s/g, '')}' stroke-width='1'/>` +
          `</svg>`
        )}")`,
        backgroundSize: `${w * 2}px ${h * 2}px`,
        pointerEvents: 'none',
        ...style,
      }}
    />
  );
};

// ─── PatternRays ───────────────────────────────────────────────────────
export interface PatternRaysProps extends BaseBlockProps {
  count?: number;
  opacity?: number;
  centerX?: number;
  centerY?: number;
}

export const PatternRays: React.FC<PatternRaysProps> = ({
  count = 12,
  opacity = 0.06,
  centerX = 0.5,
  centerY = 0.3,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const rays = Array.from({ length: count }, (_, i) => {
    const angle = (i / count) * 360;
    return `linear-gradient(${angle}deg, ${hexRgba(c.accent, String(opacity))} 0%, transparent 50%)`;
  });

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        background: rays.join(', '),
        pointerEvents: 'none',
        ...style,
      }}
    />
  );
};

// ─── PatternBokeh ──────────────────────────────────────────────────────
export interface PatternBokehProps extends BaseBlockProps {
  count?: number;
  minSize?: number;
  maxSize?: number;
  opacity?: number;
}

export const PatternBokeh: React.FC<PatternBokehProps> = ({
  count = 15,
  minSize = 20,
  maxSize = 80,
  opacity = 0.08,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const seed = (i: number) => {
    const x = Math.sin(i * 9301 + 49297) * 233280;
    return x - Math.floor(x);
  };

  return (
    <div style={{ position: 'absolute', inset: 0, overflow: 'hidden', pointerEvents: 'none', ...style }}>
      {Array.from({ length: count }, (_, i) => {
        const size = minSize + seed(i) * (maxSize - minSize);
        const x = seed(i + 100) * 1080;
        const y = seed(i + 200) * 1080;
        const col = i % 2 === 0 ? c.accent : c.accent2;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: `${x}px`,
              top: `${y}px`,
              width: `${size}px`,
              height: `${size}px`,
              borderRadius: '50%',
              background: `radial-gradient(circle, ${hexRgba(col, String(opacity))} 0%, transparent 70%)`,
            }}
          />
        );
      })}
    </div>
  );
};

// ═════════════════════════════════════════════════════════════════════
// NEW PATTERN COMPONENTS
// ═════════════════════════════════════════════════════════════════════

// ─── TextureGrain (Technique 5.4) — SVG noise/grain overlay ──────────
export interface TextureGrainProps extends BaseBlockProps {
  /** Grain intensity 0-1. Default 0.05. */
  intensity?: number;
  /** Grain size. Default 1. */
  grainSize?: number;
}

export const TextureGrain: React.FC<TextureGrainProps> = ({
  intensity = 0.05,
  grainSize = 1,
  colors,
  style,
}) => {
  // Generate SVG turbulence noise
  const svgNoise = `<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'>
    <filter id='n'>
      <feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/>
      <feColorMatrix type='saturate' values='0'/>
    </filter>
    <rect width='100%' height='100%' filter='url(#n)' opacity='${intensity}'/>
  </svg>`;

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        backgroundImage: `url("data:image/svg+xml,${encodeURIComponent(svgNoise)}")`,
        backgroundSize: '200px 200px',
        mixBlendMode: 'overlay',
        opacity: intensity,
        pointerEvents: 'none',
        ...style,
      }}
    />
  );
};

// ─── PatternIslamic (Technique 10.2) — Islamic geometric 8-point star ─
export interface PatternIslamicProps extends BaseBlockProps {
  /** Star size in px. Default 60. */
  size?: number;
  /** Opacity. Default 0.06. */
  opacity?: number;
  /** Color override. Default accent2. */
  color?: string;
}

export const PatternIslamic: React.FC<PatternIslamicProps> = ({
  size = 60,
  opacity = 0.06,
  color,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const col = hexRgba(color || c.accent2, String(opacity));
  const tile = size * 2;

  // 8-pointed star + interlacing grid
  const starSvg = `<svg xmlns='http://www.w3.org/2000/svg' width='${tile}' height='${tile}' viewBox='0 0 ${tile} ${tile}'>
    <g fill='none' stroke='${col.replace(/rgba?\(|\)|\s/g, '')}' stroke-width='1'>
      <!-- 8-pointed star -->
      <polygon points='${size},${0} ${size * 1.2},${size * 0.3} ${tile},${size * 0.5} ${size * 1.2},${size * 0.7} ${size},${tile} ${size * 0.8},${size * 0.7} ${0},${size * 0.5} ${size * 0.8},${size * 0.3}' />
      <polygon points='${size * 0.5},${0} ${size * 0.7},${size * 0.2} ${size},${size * 0.5} ${size * 0.7},${size * 0.8} ${size * 0.5},${tile} ${size * 0.3},${size * 0.8} ${0},${size * 0.5} ${size * 0.3},${size * 0.2}' />
      <!-- Outer circle -->
      <circle cx='${size}' cy='${size * 0.5}' r='${size * 0.45}' />
    </g>
  </svg>`;

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        backgroundImage: `url("data:image/svg+xml,${encodeURIComponent(starSvg)}")`,
        backgroundSize: `${tile}px ${tile}px`,
        pointerEvents: 'none',
        ...style,
      }}
    />
  );
};

// ─── TextureOverlay (Technique 9.4) — Niche-specific texture ──────────
export interface TextureOverlayProps extends BaseBlockProps {
  /** Texture type. Default 'silk'. */
  type?: 'silk' | 'metal' | 'paper' | 'carbon' | 'marble';
  /** Opacity. Default 0.08. */
  opacity?: number;
}

export const TextureOverlay: React.FC<TextureOverlayProps> = ({
  type = 'silk',
  opacity = 0.08,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const col1 = hexRgba(c.accent, String(opacity));
  const col2 = hexRgba(c.accent2, String(opacity));

  const textures: Record<string, string> = {
    silk: `repeating-linear-gradient(45deg, ${col1} 0px, transparent 1px, ${col2} 2px, transparent 3px)`,
    metal: `repeating-linear-gradient(90deg, ${col1} 0px, transparent 2px, ${col2} 4px, transparent 6px)`,
    paper: `radial-gradient(${col1} 1px, transparent 1px)`,
    carbon: `repeating-conic-gradient(${col1} 0deg 90deg, ${col2} 90deg 180deg)`,
    marble: `linear-gradient(135deg, ${col1} 0%, transparent 30%, ${col2} 60%, transparent 80%)`,
  };

  const sizes: Record<string, string> = {
    silk: '4px 4px',
    metal: '6px 6px',
    paper: '3px 3px',
    carbon: '8px 8px',
    marble: '100% 100%',
  };

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        backgroundImage: textures[type],
        backgroundSize: sizes[type],
        pointerEvents: 'none',
        ...style,
      }}
    />
  );
};
