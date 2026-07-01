// ─────────────────────────────────────────────────────────────────────
// LAYOUTS — 5 components (4 original modified + 1 new)
//   LayoutStandard   · vertical stack (MODIFIED: variable padding)
//   LayoutSplit      · left/right split (MODIFIED: golden ratio default)
//   LayoutAsymmetric · photo offset (MODIFIED: overlapping elements)
//   LayoutMagazine   · large photo + columns (MODIFIED: variable ratio)
//   ── NEW ──
//   LayoutPhotoFull  · full-bleed photo background (Technique 6.7)
// ─────────────────────────────────────────────────────────────────────

import React from 'react';
import { AbsoluteFill } from 'remotion';
import { BaseBlockProps, ColorConfig, FONTS, hexRgba, useColors, resolvePhoto } from './helpers';

// ─── LayoutStandard (MODIFIED: variable section padding) ──────────────
export interface LayoutStandardProps extends BaseBlockProps {
  header?: React.ReactNode;
  photo?: React.ReactNode;
  content?: React.ReactNode;
  cta?: React.ReactNode;
  footer?: React.ReactNode;
  decorative?: React.ReactNode;
  background?: string;
  /** Section padding override (Technique 7.2). Default '40px 50px'. */
  sectionPadding?: string;
}

export const LayoutStandard: React.FC<LayoutStandardProps> = ({
  header,
  photo,
  content,
  cta,
  footer,
  decorative,
  background,
  sectionPadding,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const bg = background ?? `linear-gradient(${c.gradientAngle ?? 135}deg, ${c.bg} 0%, ${c.bg2} 100%)`;

  return (
    <AbsoluteFill
      style={{
        background: bg,
        fontFamily: FONTS.sans,
        direction: 'rtl',
        textAlign: 'right',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
        ...style,
      }}
    >
      {decorative}
      {header}
      {photo}
      {content}
      {cta}
      {footer}
    </AbsoluteFill>
  );
};

// ─── LayoutSplit (MODIFIED: golden ratio default 0.618) ───────────────
export interface LayoutSplitProps extends BaseBlockProps {
  left?: React.ReactNode;
  right?: React.ReactNode;
  /** Width ratio of left column. Default 0.618 (golden ratio). */
  leftRatio?: number;
  gap?: number;
  header?: React.ReactNode;
  footer?: React.ReactNode;
  decorative?: React.ReactNode;
  background?: string;
}

export const LayoutSplit: React.FC<LayoutSplitProps> = ({
  left,
  right,
  leftRatio = 0.618,
  gap = 0,
  header,
  footer,
  decorative,
  background,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const bg = background ?? `linear-gradient(${c.gradientAngle ?? 135}deg, ${c.bg} 0%, ${c.bg2} 100%)`;
  const leftWidth = `${leftRatio * 100}%`;
  const rightWidth = `${(1 - leftRatio) * 100}%`;

  return (
    <AbsoluteFill
      style={{
        background: bg,
        fontFamily: FONTS.sans,
        direction: 'rtl',
        overflow: 'hidden',
        display: 'flex',
        flexDirection: 'column',
        ...style,
      }}
    >
      {decorative}
      {header}
      <div style={{ display: 'flex', flex: 1, minHeight: 0 }}>
        <div
          style={{
            width: leftWidth,
            display: 'flex',
            alignItems: 'stretch',
            justifyContent: 'center',
            overflow: 'hidden',
          }}
        >
          {left}
        </div>
        <div
          style={{
            width: rightWidth,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            padding: '20px 40px',
            direction: 'rtl',
            textAlign: 'right',
            gap: '16px',
          }}
        >
          {right}
        </div>
      </div>
      {footer}
    </AbsoluteFill>
  );
};

// ─── LayoutAsymmetric (MODIFIED: overlapping elements support) ───────
export interface LayoutAsymmetricProps extends BaseBlockProps {
  photo?: React.ReactNode;
  content?: React.ReactNode;
  cta?: React.ReactNode;
  footer?: React.ReactNode;
  header?: React.ReactNode;
  photoSide?: 'left' | 'right';
  photoOffset?: number;
  /** Photo width as %. Default 55. */
  photoWidth?: number;
  /** Content overlap in px (Technique 3.4). Default 0. */
  contentOverlap?: number;
  decorative?: React.ReactNode;
  background?: string;
}

export const LayoutAsymmetric: React.FC<LayoutAsymmetricProps> = ({
  photo,
  content,
  cta,
  footer,
  header,
  photoSide = 'left',
  photoOffset = 0,
  photoWidth = 55,
  contentOverlap = 0,
  decorative,
  background,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const bg = background ?? `linear-gradient(${c.gradientAngle ?? 135}deg, ${c.bg} 0%, ${c.bg2} 100%)`;
  const isLeft = photoSide === 'left';

  return (
    <AbsoluteFill
      style={{
        background: bg,
        fontFamily: FONTS.sans,
        direction: 'rtl',
        overflow: 'hidden',
        display: 'flex',
        flexDirection: 'column',
        ...style,
      }}
    >
      {decorative}
      {header}
      <div style={{ position: 'relative', flex: 1, display: 'flex', flexDirection: 'column' }}>
        {photo && (
          <div
            style={{
              position: 'absolute',
              top: '0',
              [isLeft ? 'left' : 'right']: `${photoOffset}px`,
              width: `${photoWidth}%`,
              zIndex: 3,
            }}
          >
            {photo}
          </div>
        )}
        <div
          style={{
            position: 'relative',
            zIndex: 5,
            display: 'flex',
            flexDirection: 'column',
            gap: '14px',
            padding: '20px 50px',
            [isLeft ? 'marginRight' : 'marginLeft']: 'auto',
            width: `${100 - photoWidth + (contentOverlap / 1080 * 100)}%`,
            direction: 'rtl',
            textAlign: 'right',
            marginTop: '10px',
          }}
        >
          {content}
          {cta}
        </div>
      </div>
      {footer}
    </AbsoluteFill>
  );
};

// ─── LayoutMagazine (MODIFIED: variable ratio) ────────────────────────
export interface LayoutMagazineProps extends BaseBlockProps {
  photo?: React.ReactNode;
  header?: React.ReactNode;
  leftColumn?: React.ReactNode;
  rightColumn?: React.ReactNode;
  cta?: React.ReactNode;
  footer?: React.ReactNode;
  /** Column width ratio (left). Default 0.618 (golden ratio). */
  leftRatio?: number;
  decorative?: React.ReactNode;
  background?: string;
}

export const LayoutMagazine: React.FC<LayoutMagazineProps> = ({
  photo,
  header,
  leftColumn,
  rightColumn,
  cta,
  footer,
  leftRatio = 0.618,
  decorative,
  background,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const bg = background ?? `linear-gradient(${c.gradientAngle ?? 135}deg, ${c.bg} 0%, ${c.bg2} 100%)`;

  return (
    <AbsoluteFill
      style={{
        background: bg,
        fontFamily: FONTS.sans,
        direction: 'rtl',
        overflow: 'hidden',
        display: 'flex',
        flexDirection: 'column',
        ...style,
      }}
    >
      {decorative}
      {header}
      <div style={{ display: 'flex', justifyContent: 'center', padding: '0', flexShrink: 0 }}>
        {photo}
      </div>
      <div
        style={{
          display: 'flex',
          flex: 1,
          minHeight: 0,
          padding: '16px 40px',
          gap: '24px',
        }}
      >
        <div
          style={{
            width: `${leftRatio * 100}%`,
            display: 'flex',
            flexDirection: 'column',
            direction: 'rtl',
            textAlign: 'right',
          }}
        >
          {leftColumn}
        </div>
        <div
          style={{
            width: `${(1 - leftRatio) * 100}%`,
            display: 'flex',
            flexDirection: 'column',
            direction: 'rtl',
            textAlign: 'right',
          }}
        >
          {rightColumn}
        </div>
      </div>
      {cta}
      {footer}
    </AbsoluteFill>
  );
};

// ═════════════════════════════════════════════════════════════════════
// NEW LAYOUT COMPONENT
// ═════════════════════════════════════════════════════════════════════

// ─── LayoutPhotoFull (Technique 6.7) — Full-bleed photo background ───
export interface LayoutPhotoFullProps extends BaseBlockProps {
  /** Background photo path. */
  photoPath: string;
  /** Content blocks rendered on top of the photo. */
  content?: React.ReactNode;
  /** Header block. */
  header?: React.ReactNode;
  /** CTA block. */
  cta?: React.ReactNode;
  /** Footer block. */
  footer?: React.ReactNode;
  decorative?: React.ReactNode;
  /** Dark overlay opacity. Default 0.55. */
  overlayOpacity?: number;
  /** Gradient direction. Default 'bottom' (darker at bottom). */
  gradientDirection?: 'bottom' | 'top' | 'both';
}

export const LayoutPhotoFull: React.FC<LayoutPhotoFullProps> = ({
  photoPath,
  content,
  header,
  cta,
  footer,
  decorative,
  overlayOpacity = 0.55,
  gradientDirection = 'bottom',
  colors,
  style,
}) => {
  const c = useColors(colors);
  const url = resolvePhoto(photoPath);

  const overlayBg = gradientDirection === 'both'
    ? `linear-gradient(180deg, ${hexRgba(c.bg, String(overlayOpacity * 0.7))} 0%, transparent 30%, transparent 70%, ${hexRgba(c.bg, String(overlayOpacity))} 100%)`
    : gradientDirection === 'top'
      ? `linear-gradient(0deg, transparent 0%, ${hexRgba(c.bg, String(overlayOpacity))} 100%)`
      : `linear-gradient(180deg, ${hexRgba(c.bg, String(overlayOpacity * 0.5))} 0%, ${hexRgba(c.bg, String(overlayOpacity))} 100%)`;

  return (
    <AbsoluteFill
      style={{
        background: c.bg,
        fontFamily: FONTS.sans,
        direction: 'rtl',
        textAlign: 'right',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
        ...style,
      }}
    >
      {/* Full-bleed photo */}
      {url && (
        <img
          src={url}
          style={{
            position: 'absolute',
            inset: 0,
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            zIndex: 0,
          }}
        />
      )}
      {/* Dark overlay */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: overlayBg,
          zIndex: 1,
        }}
      />
      {/* Content */}
      <div style={{ position: 'relative', zIndex: 2, display: 'flex', flexDirection: 'column', height: '100%' }}>
        {decorative}
        {header}
        {content}
        {cta}
        {footer}
      </div>
    </AbsoluteFill>
  );
};
