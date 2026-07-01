// ─────────────────────────────────────────────────────────────────────
// FRAMES — 5 components (3 original + 2 new)
//   FramePolaroid  · polaroid-style frame with caption
//   FrameStack     · stacked photos with offset
//   FrameCircle    · circular framed photo
//   ── NEW ──
//   CornerBrackets · L-shaped corner decorations for photos (Technique 5.2)
//   FrameKeyline   · thin border frame around canvas (Technique 5.3)
// ─────────────────────────────────────────────────────────────────────

import React from 'react';
import { BaseBlockProps, ColorConfig, FONTS, hexRgba, resolvePhoto, useColors, depthShadow } from './helpers';

// ─── FramePolaroid ─────────────────────────────────────────────────────
export interface FramePolaroidProps extends BaseBlockProps {
  src: string;
  caption?: string;
  width?: number;
  ratio?: number;
  rotation?: number;
}

export const FramePolaroid: React.FC<FramePolaroidProps> = ({
  src,
  caption,
  width = 500,
  ratio = 1,
  rotation = -3,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const url = resolvePhoto(src);
  const photoH = width * ratio;

  return (
    <div style={{ display: 'flex', justifyContent: 'center', padding: '16px 50px', flexShrink: 0, zIndex: 5, ...style }}>
      <div
        style={{
          width: `${width}px`,
          background: c.isDark ? '#2A2A3A' : '#FFFFFF',
          padding: '16px 16px 50px 16px',
          borderRadius: '4px',
          boxShadow: depthShadow('deep'),
          transform: `rotate(${rotation}deg)`,
        }}
      >
        <div style={{ width: '100%', height: `${photoH}px`, overflow: 'hidden', borderRadius: '2px' }}>
          {url && <img src={url} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />}
        </div>
        {caption && (
          <div style={{
            position: 'absolute', bottom: '12px', left: 0, right: 0, textAlign: 'center',
          }}>
            <span style={{
              fontFamily: FONTS.kufi, fontSize: '16px', fontWeight: 600,
              color: c.isDark ? c.accent : '#333',
            }}>
              {caption}
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

// ─── FrameStack ────────────────────────────────────────────────────────
export interface FrameStackProps extends BaseBlockProps {
  photos: string[];
  photoWidth?: number;
  photoHeight?: number;
  offset?: number;
}

export const FrameStack: React.FC<FrameStackProps> = ({
  photos,
  photoWidth = 300,
  photoHeight = 300,
  offset = 30,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const resolved = photos.map(resolvePhoto);
  const totalWidth = photoWidth + offset * (resolved.length - 1);

  return (
    <div style={{
      display: 'flex', justifyContent: 'center', alignItems: 'center',
      padding: '20px 50px', flexShrink: 0, zIndex: 5,
      height: `${photoHeight + 40}px`, position: 'relative',
      ...style,
    }}>
      <div style={{ position: 'relative', width: `${totalWidth}px`, height: `${photoHeight}px` }}>
        {resolved.map((url, i) => {
          const isTop = i === resolved.length - 1;
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: `${i * offset}px`,
                top: `${(resolved.length - 1 - i) * 5}px`,
                width: `${photoWidth}px`,
                height: `${photoHeight}px`,
                borderRadius: '16px',
                overflow: 'hidden',
                boxShadow: isTop
                  ? `0 20px 40px rgba(0,0,0,0.4), 0 0 0 3px ${c.accent}`
                  : '0 10px 25px rgba(0,0,0,0.3)',
                zIndex: i + 1,
              }}
            >
              {url && <img src={url} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />}
            </div>
          );
        })}
      </div>
    </div>
  );
};

// ─── FrameCircle ───────────────────────────────────────────────────────
export interface FrameCircleProps extends BaseBlockProps {
  src: string;
  size?: number;
  borderWidth?: number;
  showRing?: boolean;
}

export const FrameCircle: React.FC<FrameCircleProps> = ({
  src,
  size = 200,
  borderWidth = 4,
  showRing = true,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const url = resolvePhoto(src);

  return (
    <div style={{ display: 'flex', justifyContent: 'center', padding: '16px', flexShrink: 0, zIndex: 5, ...style }}>
      <div
        style={{
          width: `${size}px`,
          height: `${size}px`,
          borderRadius: '50%',
          overflow: 'hidden',
          border: showRing ? `${borderWidth}px solid ${c.accent}` : 'none',
          boxShadow: showRing ? `0 0 30px ${hexRgba(c.accent, '0.4')}` : depthShadow('deep'),
        }}
      >
        {url && <img src={url} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />}
      </div>
    </div>
  );
};

// ═════════════════════════════════════════════════════════════════════
// NEW FRAME COMPONENTS
// ═════════════════════════════════════════════════════════════════════

// ─── CornerBrackets (Technique 5.2) — L-shaped corner decorations ────
export interface CornerBracketsProps extends BaseBlockProps {
  /** Bracket length in px. Default 40. */
  length?: number;
  /** Bracket thickness in px. Default 3. */
  thickness?: number;
  /** Which corners to show. Default all. */
  corners?: ('top-left' | 'top-right' | 'bottom-left' | 'bottom-right')[];
  /** Color override. Default accent. */
  color?: string;
  /** Opacity. Default 0.8. */
  opacity?: number;
  /** Inset from edge in px. Default 20. */
  inset?: number;
}

export const CornerBrackets: React.FC<CornerBracketsProps> = ({
  length = 40,
  thickness = 3,
  corners = ['top-left', 'top-right', 'bottom-left', 'bottom-right'],
  color,
  opacity = 0.8,
  inset = 20,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const col = hexRgba(color || c.accent, String(opacity));

  const bracketStyle = (corner: string): React.CSSProperties => {
    const isTop = corner.startsWith('top');
    const isLeft = corner.endsWith('left');
    return {
      position: 'absolute',
      [isTop ? 'top' : 'bottom']: `${inset}px`,
      [isLeft ? 'left' : 'right']: `${inset}px`,
      width: isLeft ? `${length}px` : `${thickness}px`,
      height: isLeft ? `${thickness}px` : `${length}px`,
      background: col,
      borderRadius: `${thickness}px`,
      pointerEvents: 'none',
    };
  };

  // Second arm of each L bracket
  const bracketArm = (corner: string): React.CSSProperties => {
    const isTop = corner.startsWith('top');
    const isLeft = corner.endsWith('left');
    return {
      position: 'absolute',
      [isTop ? 'top' : 'bottom']: `${inset}px`,
      [isLeft ? 'left' : 'right']: `${inset}px`,
      width: isLeft ? `${thickness}px` : `${length}px`,
      height: isLeft ? `${length}px` : `${thickness}px`,
      background: col,
      borderRadius: `${thickness}px`,
      pointerEvents: 'none',
    };
  };

  return (
    <>
      {corners.map((corner) => (
        <React.Fragment key={corner}>
          <div style={bracketStyle(corner)} />
          <div style={bracketArm(corner)} />
        </React.Fragment>
      ))}
    </>
  );
};

// ─── FrameKeyline (Technique 5.3) — Thin border frame around canvas ──
export interface FrameKeylineProps extends BaseBlockProps {
  /** Border width in px. Default 2. */
  borderWidth?: number;
  /** Inset from edge in px. Default 30. */
  inset?: number;
  /** Color override. Default accent2. */
  color?: string;
  /** Opacity. Default 0.3. */
  opacity?: number;
  /** Border radius. Default 12. */
  radius?: number;
}

export const FrameKeyline: React.FC<FrameKeylineProps> = ({
  borderWidth = 2,
  inset = 30,
  color,
  opacity = 0.3,
  radius = 12,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const col = hexRgba(color || c.accent2, String(opacity));

  return (
    <div
      style={{
        position: 'absolute',
        top: `${inset}px`,
        left: `${inset}px`,
        right: `${inset}px`,
        bottom: `${inset}px`,
        border: `${borderWidth}px solid ${col}`,
        borderRadius: `${radius}px`,
        pointerEvents: 'none',
        zIndex: 2,
        ...style,
      }}
    />
  );
};
