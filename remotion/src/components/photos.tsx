// ─────────────────────────────────────────────────────────────────────
// PHOTOS — 10 components (5 original + 5 new)
//   PhotoSingle     · one photo, centered, rounded corners, shadow
//   PhotoGrid       · 2×2 or 1×3 grid of photos
//   PhotoMosaic     · asymmetric mosaic (1 large + 2 small)
//   PhotoCarousel   · horizontal row of photos (static for PNG)
//   PhotoFrame      · photo with decorative frame border
//   ── NEW ──
//   PhotoArch       · arch-shaped photo mask (Technique 6.1)
//   PhotoCircle     · large circular photo (Technique 6.2)
//   PhotoDiagonal   · diagonal-cut photo (Technique 6.3)
//   PhotoDuotone    · two-color gradient overlay (Technique 2.3)
//   PhotoDoubleFrame· double-framed photo (Technique 5.5)
// ─────────────────────────────────────────────────────────────────────

import React from 'react';
import {
  BaseBlockProps,
  ColorConfig,
  FONTS,
  hexRgba,
  resolvePhoto,
  useColors,
  depthShadow,
  photoOverlayStyle,
} from './helpers';

// ─── PhotoSingle (MODIFIED: added gradient overlay support) ─────────────
export interface PhotoSingleProps extends BaseBlockProps {
  src: string;
  width?: number;
  height?: number;
  radius?: number;
  /** Show gradient overlay at bottom for text legibility. Default false. */
  showOverlay?: boolean;
  /** Overlay color. Defaults to bg2. */
  overlayColor?: string;
  /** Overlay opacity 0-1. Default 0.4. */
  overlayOpacity?: number;
}

export const PhotoSingle: React.FC<PhotoSingleProps> = ({
  src,
  width = 620,
  height = 370,
  radius = 24,
  showOverlay = false,
  overlayColor,
  overlayOpacity = 0.4,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const url = resolvePhoto(src);
  const isFillMode = style && (style as any).height === '100%';
  const containerStyle: React.CSSProperties = isFillMode
    ? { width: '100%', height: '100%', borderRadius: `${radius}px`, overflow: 'hidden', boxShadow: depthShadow('deep'), position: 'relative' }
    : { width: `${width}px`, height: `${height}px`, borderRadius: `${radius}px`, overflow: 'hidden', boxShadow: depthShadow('deep'), position: 'relative' };

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100%',
        width: '100%',
        padding: '0 50px',
        flexShrink: 0,
        zIndex: 5,
        ...style,
      }}
    >
      <div style={containerStyle}>
        {url && (
          <img src={url} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        )}
        {showOverlay && (
          <div style={photoOverlayStyle(overlayColor || c.bg2, overlayOpacity)} />
        )}
      </div>
    </div>
  );
};

// ─── PhotoGrid ────────────────────────────────────────────────────────
export interface PhotoGridProps extends BaseBlockProps {
  photos: string[];
  layout?: '2x2' | '1x3' | '3x1';
  gap?: number;
  radius?: number;
  width?: number;
}

export const PhotoGrid: React.FC<PhotoGridProps> = ({
  photos,
  layout = '2x2',
  gap = 12,
  radius = 16,
  width = 620,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const resolved = photos.map(resolvePhoto);
  const cols = layout === '2x2' ? 2 : layout === '1x3' ? 3 : 1;
  const rows = layout === '2x2' ? 2 : layout === '3x1' ? 3 : 1;
  const cellW = (width - gap * (cols - 1)) / cols;
  const cellH = layout === '2x2' ? cellW * 0.62 : layout === '1x3' ? cellW : cellW * 0.66;
  const totalH = cellH * rows + gap * (rows - 1);

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        marginTop: '20px',
        flexShrink: 0,
        zIndex: 5,
        ...style,
      }}
    >
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: `repeat(${cols}, ${cellW}px)`,
          gridTemplateRows: `repeat(${rows}, ${cellH}px)`,
          gap: `${gap}px`,
          width: `${width}px`,
        }}
      >
        {resolved.slice(0, cols * rows).map((url, i) => (
          <div
            key={i}
            style={{
              borderRadius: `${radius}px`,
              overflow: 'hidden',
              boxShadow: `0 12px 30px rgba(0,0,0,0.25), 0 0 0 1px ${hexRgba(c.accent, '0.1')}`,
            }}
          >
            {url && (
              <img src={url} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

// ─── PhotoMosaic ──────────────────────────────────────────────────────
export interface PhotoMosaicProps extends BaseBlockProps {
  photos: string[];
  width?: number;
  gap?: number;
  radius?: number;
}

export const PhotoMosaic: React.FC<PhotoMosaicProps> = ({
  photos,
  width = 620,
  gap = 12,
  radius = 18,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const resolved = photos.map(resolvePhoto);
  const largeW = width * 0.58;
  const smallW = width - largeW - gap;
  const largeH = 370;
  const smallH = (largeH - gap) / 2;

  const tile = (url: string, w: number, h: number): React.CSSProperties => ({
    width: `${w}px`,
    height: `${h}px`,
    borderRadius: `${radius}px`,
    overflow: 'hidden',
    boxShadow: `0 15px 35px rgba(0,0,0,0.3), 0 0 0 1px ${hexRgba(c.accent, '0.1')}`,
  });

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        marginTop: '20px',
        flexShrink: 0,
        zIndex: 5,
        ...style,
      }}
    >
      <div style={{ display: 'flex', gap: `${gap}px`, width: `${width}px` }}>
        <div style={tile(resolved[0], largeW, largeH)}>
          {resolved[0] && (
            <img src={resolved[0]} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
          )}
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: `${gap}px` }}>
          <div style={tile(resolved[1], smallW, smallH)}>
            {resolved[1] && (
              <img src={resolved[1]} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            )}
          </div>
          <div style={tile(resolved[2], smallW, smallH)}>
            {resolved[2] && (
              <img src={resolved[2]} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// ─── PhotoCarousel ─────────────────────────────────────────────────────
export interface PhotoCarouselProps extends BaseBlockProps {
  photos: string[];
  photoWidth?: number;
  photoHeight?: number;
  overlap?: number;
  radius?: number;
}

export const PhotoCarousel: React.FC<PhotoCarouselProps> = ({
  photos,
  photoWidth = 260,
  photoHeight = 300,
  overlap = 40,
  radius = 20,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const resolved = photos.map(resolvePhoto);
  const totalWidth = resolved.length * photoWidth - overlap * (resolved.length - 1);
  const startX = (1080 - totalWidth) / 2;

  return (
    <div
      style={{
        position: 'relative',
        height: `${photoHeight + 40}px`,
        marginTop: '20px',
        flexShrink: 0,
        zIndex: 5,
        ...style,
      }}
    >
      {resolved.map((url, i) => {
        const x = startX + i * (photoWidth - overlap);
        const isFront = i === Math.floor(resolved.length / 2);
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: `${x}px`,
              top: '20px',
              width: `${photoWidth}px`,
              height: `${photoHeight}px`,
              borderRadius: `${radius}px`,
              overflow: 'hidden',
              boxShadow: isFront
                ? `0 25px 50px rgba(0,0,0,0.4), 0 0 0 3px ${hexRgba(c.accent, '0.5')}`
                : '0 15px 35px rgba(0,0,0,0.3)',
              zIndex: isFront ? 10 : 5 - Math.abs(i - Math.floor(resolved.length / 2)),
            }}
          >
            {url && (
              <img src={url} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            )}
          </div>
        );
      })}
    </div>
  );
};

// ─── PhotoFrame (MODIFIED: with gradient overlay support) ──────────────
export interface PhotoFrameProps extends BaseBlockProps {
  src: string;
  width?: number;
  height?: number;
  borderWidth?: number;
  caption?: string;
  showOverlay?: boolean;
  overlayOpacity?: number;
}

export const PhotoFrame: React.FC<PhotoFrameProps> = ({
  src,
  width = 560,
  height = 340,
  borderWidth = 12,
  caption,
  showOverlay = false,
  overlayOpacity = 0.4,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const url = resolvePhoto(src);
  const isFillMode = style && (style as any).height === '100%';
  const photoW = isFillMode ? '100%' : `${width}px`;
  const photoH = isFillMode ? '100%' : `${height}px`;
  const totalW = isFillMode ? '100%' : `${width + borderWidth * 2}px`;
  const totalH = isFillMode ? '100%' : `${height + borderWidth * 2 + (caption ? 50 : 0)}px`;

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100%',
        width: '100%',
        padding: '0 50px',
        flexShrink: 0,
        zIndex: 5,
        ...style,
      }}
    >
      <div
        style={{
          width: totalW,
          height: totalH,
          background: c.isDark ? hexRgba(c.accent, '0.08') : '#FFFFFF',
          borderRadius: '8px',
          padding: `${borderWidth}px`,
          boxShadow: depthShadow('deep'),
        }}
      >
        <div
          style={{
            width: photoW,
            height: photoH,
            overflow: 'hidden',
            borderRadius: '4px',
            position: 'relative',
          }}
        >
          {url && (
            <img src={url} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
          )}
          {showOverlay && (
            <div style={photoOverlayStyle(c.bg2, overlayOpacity)} />
          )}
        </div>
        {caption && (
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height: `${caption ? 50 : 0}px`,
              direction: 'rtl',
            }}
          >
            <span
              style={{
                fontFamily: FONTS.kufi,
                fontSize: '16px',
                fontWeight: 600,
                color: c.accent,
              }}
            >
              {caption}
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

// ═════════════════════════════════════════════════════════════════════
// NEW PHOTO COMPONENTS
// ═════════════════════════════════════════════════════════════════════

// ─── PhotoArch (Technique 6.1) — Arch-shaped photo mask ──────────────
export interface PhotoArchProps extends BaseBlockProps {
  src: string;
  width?: number;
  height?: number;
  showOverlay?: boolean;
  overlayOpacity?: number;
}

export const PhotoArch: React.FC<PhotoArchProps> = ({
  src,
  width = 480,
  height = 600,
  showOverlay = false,
  overlayOpacity = 0.4,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const url = resolvePhoto(src);
  const archRadius = width / 2;

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100%',
        width: '100%',
        padding: '0 50px',
        flexShrink: 0,
        zIndex: 5,
        ...style,
      }}
    >
      <div
        style={{
          width: `${width}px`,
          height: `${height}px`,
          borderRadius: `${archRadius}px ${archRadius}px 24px 24px`,
          overflow: 'hidden',
          boxShadow: depthShadow('deep'),
          position: 'relative',
          border: `2px solid ${hexRgba(c.accent, '0.2')}`,
        }}
      >
        {url && (
          <img src={url} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        )}
        {showOverlay && (
          <div style={photoOverlayStyle(c.bg2, overlayOpacity)} />
        )}
      </div>
    </div>
  );
};

// ─── PhotoCircle (Technique 6.2) — Large circular photo ───────────────
export interface PhotoCircleProps extends BaseBlockProps {
  src: string;
  /** Diameter in px. Default 400. */
  size?: number;
  /** Show ring border. Default true. */
  showRing?: boolean;
  /** Ring width in px. Default 6. */
  ringWidth?: number;
  showOverlay?: boolean;
  overlayOpacity?: number;
}

export const PhotoCircle: React.FC<PhotoCircleProps> = ({
  src,
  size = 400,
  showRing = true,
  ringWidth = 6,
  showOverlay = false,
  overlayOpacity = 0.4,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const url = resolvePhoto(src);

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '20px',
        flexShrink: 0,
        zIndex: 5,
        ...style,
      }}
    >
      <div
        style={{
          width: `${size}px`,
          height: `${size}px`,
          borderRadius: '50%',
          overflow: 'hidden',
          border: showRing ? `${ringWidth}px solid ${c.accent}` : 'none',
          boxShadow: showRing
            ? `0 0 40px ${hexRgba(c.accent, '0.3')}, ${depthShadow('deep')}`
            : depthShadow('deep'),
          position: 'relative',
        }}
      >
        {url && (
          <img src={url} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        )}
        {showOverlay && (
          <div style={photoOverlayStyle(c.bg2, overlayOpacity)} />
        )}
      </div>
    </div>
  );
};

// ─── PhotoDiagonal (Technique 6.3) — Diagonal-cut photo ──────────────
export interface PhotoDiagonalProps extends BaseBlockProps {
  src: string;
  width?: number;
  height?: number;
  /** Diagonal direction. Default 'left'. */
  direction?: 'left' | 'right';
  showOverlay?: boolean;
  overlayOpacity?: number;
}

export const PhotoDiagonal: React.FC<PhotoDiagonalProps> = ({
  src,
  width = 620,
  height = 380,
  direction = 'left',
  showOverlay = false,
  overlayOpacity = 0.4,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const url = resolvePhoto(src);
  const clipPath = direction === 'left'
    ? 'polygon(0 0, 100% 15%, 100% 100%, 0 85%)'
    : 'polygon(0 15%, 100% 0, 100% 85%, 0 100%)';

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100%',
        width: '100%',
        padding: '0 50px',
        flexShrink: 0,
        zIndex: 5,
        ...style,
      }}
    >
      <div
        style={{
          width: `${width}px`,
          height: `${height}px`,
          clipPath,
          overflow: 'hidden',
          boxShadow: depthShadow('deep'),
          position: 'relative',
        }}
      >
        {url && (
          <img src={url} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        )}
        {showOverlay && (
          <div style={photoOverlayStyle(c.bg2, overlayOpacity)} />
        )}
      </div>
    </div>
  );
};

// ─── PhotoDuotone (Technique 2.3) — Two-color gradient photo treatment ─
export interface PhotoDuotoneProps extends BaseBlockProps {
  src: string;
  width?: number;
  height?: number;
  radius?: number;
  /** First color of the duotone (shadows). Default accent. */
  shadowColor?: string;
  /** Second color of the duotone (highlights). Default accent2. */
  highlightColor?: string;
  /** Blend mode intensity 0-1. Default 0.6. */
  intensity?: number;
}

export const PhotoDuotone: React.FC<PhotoDuotoneProps> = ({
  src,
  width = 620,
  height = 370,
  radius = 24,
  shadowColor,
  highlightColor,
  intensity = 0.6,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const url = resolvePhoto(src);
  const sc = shadowColor || c.accent;
  const hc = highlightColor || c.accent2;

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100%',
        width: '100%',
        padding: '0 50px',
        flexShrink: 0,
        zIndex: 5,
        ...style,
      }}
    >
      <div
        style={{
          width: `${width}px`,
          height: `${height}px`,
          borderRadius: `${radius}px`,
          overflow: 'hidden',
          boxShadow: depthShadow('deep'),
          position: 'relative',
        }}
      >
        {url && (
          <img src={url} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        )}
        {/* Duotone shadow layer */}
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background: sc,
            mixBlendMode: 'multiply',
            opacity: intensity,
          }}
        />
        {/* Duotone highlight layer */}
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background: `linear-gradient(135deg, ${hc} 0%, transparent 60%)`,
            mixBlendMode: 'screen',
            opacity: intensity * 0.8,
          }}
        />
      </div>
    </div>
  );
};

// ─── PhotoDoubleFrame (Technique 5.5) — Double-framed photo ───────────
export interface PhotoDoubleFrameProps extends BaseBlockProps {
  src: string;
  width?: number;
  height?: number;
  /** Outer frame color. Default accent2. */
  outerColor?: string;
  /** Inner frame color. Default accent. */
  innerColor?: string;
  /** Frame gap in px. Default 8. */
  frameGap?: number;
}

export const PhotoDoubleFrame: React.FC<PhotoDoubleFrameProps> = ({
  src,
  width = 560,
  height = 340,
  outerColor,
  innerColor,
  frameGap = 8,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const url = resolvePhoto(src);
  const oc = outerColor || c.accent2;
  const ic = innerColor || c.accent;

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100%',
        width: '100%',
        padding: '0 50px',
        flexShrink: 0,
        zIndex: 5,
        ...style,
      }}
    >
      <div
        style={{
          width: `${width + frameGap * 2 + 8}px`,
          height: `${height + frameGap * 2 + 8}px`,
          borderRadius: '20px',
          background: oc,
          padding: `${frameGap + 4}px`,
          boxShadow: depthShadow('deep'),
        }}
      >
        <div
          style={{
            width: `${width + frameGap * 2}px`,
            height: `${height + frameGap * 2}px`,
            borderRadius: '16px',
            background: ic,
            padding: `${frameGap}px`,
          }}
        >
          <div
            style={{
              width: `${width}px`,
              height: `${height}px`,
              borderRadius: '12px',
              overflow: 'hidden',
            }}
          >
            {url && (
              <img src={url} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
