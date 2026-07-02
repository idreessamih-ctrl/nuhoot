// ─────────────────────────────────────────────────────────────────────
// DRAMATIC LAYOUTS — 6 Completely Different Visual Compositions
// ─────────────────────────────────────────────────────────────────────
// Each layout is a COMPLETE design, not a column of cards.
// They are structurally different — not just "different components in same order."
//
// 1. HeroFullBleed   — Photo fills entire canvas, text overlay (Netflix poster style)
// 2. SplitScreen     — 45% color block + 55% photo, side by side
// 3. MagazineCover   — Photo 65% top, headline overlaps boundary, content strip bottom
// 4. BoldPoster      — Giant typography hero, photo as small accent, aggressive color
// 5. OverlappingCards — Photos cascade/overlap, text floats in negative space
// 6. MinimalLuxury   — 60% negative space, arch photo, gold accents, ultra-premium
// ─────────────────────────────────────────────────────────────────────

import React from 'react';
import {
  ColorConfig,
  DEFAULT_COLORS,
  useColors,
  hexRgba,
  hexShift,
  toArabicDigits,
  truncateCta,
  rtlProps,
  resolvePhoto,
  FONTS,
  depthShadow,
  accentShadow,
  optimalFontSize,
} from './helpers';

// ─── Shared Types ────────────────────────────────────────────────────
export interface DramaticProps {
  colors?: ColorConfig;
  kicker?: string;
  headline?: string;
  businessName?: string;
  taglines?: string[];
  bodyText?: string;
  ctaText?: string;
  rating?: number;
  ratingCount?: number;
  hashtags?: string[];
  trustBadge?: string;
  photoPath?: string;
  photoPath2?: string;
  photoPath3?: string;
  style?: React.CSSProperties;
}

const W = 1080;
const H = 1080;

// ════════════════════════════════════════════════════════════════════
// 1. HERO FULL-BLEED — Photo fills entire canvas, text overlay
//    Like a Netflix poster or Instagram story ad
// ════════════════════════════════════════════════════════════════════
export const HeroFullBleed: React.FC<DramaticProps> = ({
  colors = DEFAULT_COLORS,
  kicker,
  headline,
  businessName,
  taglines = [],
  bodyText,
  ctaText,
  rating = 4.7,
  ratingCount = 15,
  hashtags = [],
  trustBadge,
  photoPath,
}) => {
  const c = useColors(colors);
  const rtl = rtlProps(headline);

  return (
    <div style={{
      width: W, height: H, position: 'relative', overflow: 'hidden',
      background: c.bg, fontFamily: FONTS.sans,
    }}>
      {/* Full-bleed photo */}
      {photoPath && (
        <img
          src={resolvePhoto(photoPath)}
          style={{
            position: 'absolute', top: 0, left: 0, width: '100%', height: '100%',
            objectFit: 'cover', zIndex: 1,
          }}
        />
      )}

      {/* Gradient overlay — dark at bottom, transparent at top */}
      <div style={{
        position: 'absolute', bottom: 0, left: 0, width: '100%', height: '75%',
        background: `linear-gradient(to top, ${c.bg} 5%, ${hexRgba(c.bg, '0.85')} 30%, ${hexRgba(c.bg, '0.3')} 70%, transparent 100%)`,
        zIndex: 2,
      }} />

      {/* Top badge — minimal, top-right */}
      {trustBadge && (
        <div style={{
          position: 'absolute', top: 50, right: 50, zIndex: 5,
          background: hexRgba(c.accent, '0.9'),
          padding: '8px 24px', borderRadius: 30,
          fontSize: 22, fontWeight: 700, color: '#fff',
          backdropFilter: 'blur(10px)',
          boxShadow: depthShadow('subtle'),
        }}>
          {trustBadge}
        </div>
      )}

      {/* Kicker — top left, small */}
      {kicker && (
        <div style={{
          position: 'absolute', top: 55, left: 50, zIndex: 5,
          fontSize: 24, color: hexRgba(c.accentGlint || c.accent, '0.95'),
          fontWeight: 600, letterSpacing: '0.05em',
          textShadow: '0 2px 8px rgba(0,0,0,0.6)',
        }}>
          {kicker}
        </div>
      )}

      {/* Content block — bottom of canvas */}
      <div style={{
        position: 'absolute', bottom: 80, left: 50, right: 50, zIndex: 5,
        display: 'flex', flexDirection: 'column', gap: 20,
      }}>
        {/* Massive headline */}
        {headline && (
          <div style={{
            fontSize: 72, fontWeight: 900, color: '#fff',
            lineHeight: 1.1, direction: rtl.direction, textAlign: rtl.textAlign,
            textShadow: '0 4px 24px rgba(0,0,0,0.7)',
            fontFamily: FONTS.kufi,
          }}>
            {headline}
          </div>
        )}

        {/* Business name — accent color */}
        {businessName && (
          <div style={{
            fontSize: 32, fontWeight: 700,
            color: c.accentGlint || c.accent,
            direction: rtl.direction, textAlign: rtl.textAlign,
          }}>
            {businessName}
          </div>
        )}

        {/* Tagline pills — inline */}
        {taglines.length > 0 && (
          <div style={{
            display: 'flex', gap: 12, flexWrap: 'wrap',
            direction: rtl.direction, justifyContent: rtl.textAlign === 'right' ? 'flex-end' : 'flex-start',
          }}>
            {taglines.slice(0, 3).map((tag, i) => (
              <div key={i} style={{
                background: hexRgba(c.accent, '0.25'),
                border: `1.5px solid ${hexRgba(c.accent, '0.6')}`,
                padding: '6px 18px', borderRadius: 20,
                fontSize: 20, color: '#fff', fontWeight: 500,
                backdropFilter: 'blur(8px)',
              }}>
                {tag}
              </div>
            ))}
          </div>
        )}

        {/* CTA + Rating row */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: 24,
          direction: rtl.direction,
        }}>
          {ctaText && (
            <div style={{
              background: c.accent, color: '#fff',
              padding: '16px 40px', borderRadius: 35,
              fontSize: 26, fontWeight: 800,
              boxShadow: accentShadow(c.accent, 'medium'),
              boxShadow: depthShadow('medium'),
            }}>
              {truncateCta(ctaText, 35)}
            </div>
          )}
          {/* Rating */}
          <div style={{
            display: 'flex', alignItems: 'center', gap: 8,
          }}>
            <span style={{ color: c.accentGlint || '#FFD700', fontSize: 28 }}>
              {'★'.repeat(Math.round(rating))}
            </span>
            <span style={{ color: '#fff', fontSize: 24, fontWeight: 700 }}>
              {toArabicDigits(rating)}
            </span>
            <span style={{ color: hexRgba('#fff', '0.6'), fontSize: 18 }}>
              ({toArabicDigits(ratingCount)})
            </span>
          </div>
        </div>

        {/* Hashtags */}
        {hashtags.length > 0 && (
          <div style={{
            fontSize: 16, color: hexRgba(c.accentGlint || c.accent, '0.7'),
            direction: rtl.direction, textAlign: rtl.textAlign,
          }}>
            {hashtags.slice(0, 4).join('  ')}
          </div>
        )}
      </div>

      {/* Footer */}
      <div style={{
        position: 'absolute', bottom: 0, left: 0, right: 0, zIndex: 6,
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        padding: '12px 50px',
        background: hexRgba(c.bg, '0.8'),
        borderTop: `1px solid ${hexRgba(c.accent, '0.3')}`,
      }}>
        <span style={{ color: c.accentGlint || c.accent, fontSize: 16, fontWeight: 600 }}>
          نُهوت — التسويق الرقمي
        </span>
        <span style={{ color: hexRgba('#fff', '0.5'), fontSize: 16 }}>
          nuhoot.xyz
        </span>
      </div>
    </div>
  );
};

// ════════════════════════════════════════════════════════════════════
// 2. SPLIT SCREEN — Left color block + right photo, side by side
//    Bold geometric contrast, no cards
// ════════════════════════════════════════════════════════════════════
export const SplitScreen: React.FC<DramaticProps> = ({
  colors = DEFAULT_COLORS,
  kicker,
  headline,
  businessName,
  taglines = [],
  bodyText,
  ctaText,
  rating = 4.7,
  ratingCount = 15,
  hashtags = [],
  trustBadge,
  photoPath,
}) => {
  const c = useColors(colors);
  const rtl = rtlProps(headline);
  const splitWidth = Math.round(W * 0.45); // 45% text, 55% photo

  return (
    <div style={{
      width: W, height: H, position: 'relative', overflow: 'hidden',
      background: c.bg, fontFamily: FONTS.sans, display: 'flex',
    }}>
      {/* LEFT: Color block with all text */}
      <div style={{
        width: splitWidth, height: '100%',
        background: `linear-gradient(${c.gradientAngle || 160}deg, ${c.bg}, ${c.bg2})`,
        display: 'flex', flexDirection: 'column', justifyContent: 'center',
        padding: '60px 50px', position: 'relative',
      }}>
        {/* Decorative accent strip */}
        <div style={{
          position: 'absolute', top: 0, right: 0, width: 6, height: '100%',
          background: `linear-gradient(to bottom, ${c.accent}, ${c.accent2})`,
        }} />

        {kicker && (
          <div style={{
            fontSize: 22, color: c.accent, fontWeight: 600,
            marginBottom: 16, letterSpacing: '0.05em',
          }}>
            {kicker}
          </div>
        )}

        {headline && (
          <div style={{
            fontSize: 56, fontWeight: 900, color: c.text,
            lineHeight: 1.15, marginBottom: 20,
            direction: rtl.direction, textAlign: rtl.textAlign,
            fontFamily: FONTS.kufi,
          }}>
            {headline}
          </div>
        )}

        {/* Accent line */}
        <div style={{
          width: 60, height: 4, background: c.accent,
          borderRadius: 2, marginBottom: 24,
        }} />

        {businessName && (
          <div style={{
            fontSize: 28, fontWeight: 700, color: c.accentGlint || c.accent,
            marginBottom: 20, direction: rtl.direction, textAlign: rtl.textAlign,
          }}>
            {businessName}
          </div>
        )}

        {/* Body text — no cards, just text */}
        {bodyText && (
          <div style={{
            fontSize: 22, color: hexRgba(c.text, '0.75'), lineHeight: 1.6,
            marginBottom: 24, direction: rtl.direction, textAlign: rtl.textAlign,
          }}>
            {bodyText}
          </div>
        )}

        {/* Taglines as list, not pills */}
        {taglines.length > 0 && (
          <div style={{
            display: 'flex', flexDirection: 'column', gap: 10, marginBottom: 28,
            direction: rtl.direction, textAlign: rtl.textAlign,
          }}>
            {taglines.slice(0, 3).map((tag, i) => (
              <div key={i} style={{
                fontSize: 20, color: c.text, display: 'flex', alignItems: 'center', gap: 10,
                flexDirection: rtl.direction === 'rtl' ? 'row-reverse' : 'row',
              }}>
                <span style={{ color: c.accent, fontSize: 14 }}>◆</span>
                {tag}
              </div>
            ))}
          </div>
        )}

        {ctaText && (
          <div style={{
            display: 'inline-block', background: c.accent, color: '#fff',
            padding: '14px 36px', borderRadius: 30,
            fontSize: 24, fontWeight: 800, alignSelf: rtl.direction === 'rtl' ? 'flex-end' : 'flex-start',
            boxShadow: accentShadow(c.accent, 'medium'), boxShadow: depthShadow('subtle'),
          }}>
            {truncateCta(ctaText, 30)}
          </div>
        )}

        {/* Rating — minimal */}
        <div style={{
          marginTop: 20, display: 'flex', alignItems: 'center', gap: 8,
          flexDirection: rtl.direction === 'rtl' ? 'row-reverse' : 'row',
        }}>
          <span style={{ color: c.accentGlint || '#FFD700', fontSize: 22 }}>
            {'★'.repeat(Math.round(rating))}
          </span>
          <span style={{ color: c.text, fontSize: 20, fontWeight: 700 }}>
            {toArabicDigits(rating)}
          </span>
          <span style={{ color: hexRgba(c.text, '0.5'), fontSize: 16 }}>
            ({toArabicDigits(ratingCount)} تقييم)
          </span>
        </div>
      </div>

      {/* RIGHT: Full-height photo */}
      <div style={{
        flex: 1, height: '100%', position: 'relative', overflow: 'hidden',
      }}>
        {photoPath && (
          <img
            src={resolvePhoto(photoPath)}
            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          />
        )}
        {/* Trust badge floating on photo */}
        {trustBadge && (
          <div style={{
            position: 'absolute', bottom: 100, left: 30,
            background: hexRgba(c.bg, '0.9'),
            border: `2px solid ${c.accent}`,
            padding: '10px 24px', borderRadius: 25,
            fontSize: 20, color: c.text, fontWeight: 600,
            backdropFilter: 'blur(10px)',
          }}>
            {trustBadge}
          </div>
        )}
        {/* Hashtags on photo bottom */}
        {hashtags.length > 0 && (
          <div style={{
            position: 'absolute', bottom: 60, left: 30, right: 30,
            fontSize: 16, color: hexRgba('#fff', '0.8'),
            textShadow: '0 2px 6px rgba(0,0,0,0.5)',
          }}>
            {hashtags.slice(0, 3).join('  ')}
          </div>
        )}
      </div>

      {/* Footer — spans full width */}
      <div style={{
        position: 'absolute', bottom: 0, left: 0, right: 0,
        display: 'flex', justifyContent: 'space-between',
        padding: '10px 50px',
        background: hexRgba(c.bg, '0.85'),
        borderTop: `1px solid ${hexRgba(c.accent, '0.3')}`,
      }}>
        <span style={{ color: c.accentGlint || c.accent, fontSize: 15, fontWeight: 600 }}>
          نُهوت — التسويق الرقمي
        </span>
        <span style={{ color: hexRgba('#fff', '0.5'), fontSize: 15 }}>
          nuhoot.xyz
        </span>
      </div>
    </div>
  );
};

// ════════════════════════════════════════════════════════════════════
// 3. MAGAZINE COVER — Photo 65% top, headline overlaps, content strip
//    Like a fashion magazine cover
// ════════════════════════════════════════════════════════════════════
export const MagazineCover: React.FC<DramaticProps> = ({
  colors = DEFAULT_COLORS,
  kicker,
  headline,
  businessName,
  taglines = [],
  bodyText,
  ctaText,
  rating = 4.7,
  ratingCount = 15,
  hashtags = [],
  trustBadge,
  photoPath,
}) => {
  const c = useColors(colors);
  const rtl = rtlProps(headline);
  const photoHeight = Math.round(H * 0.62); // Golden ratio

  return (
    <div style={{
      width: W, height: H, position: 'relative', overflow: 'hidden',
      background: c.bg, fontFamily: FONTS.sans,
    }}>
      {/* Photo — top 62% */}
      <div style={{
        width: '100%', height: photoHeight, position: 'relative', overflow: 'hidden',
      }}>
        {photoPath && (
          <img
            src={resolvePhoto(photoPath)}
            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          />
        )}
        {/* Gradient fade at bottom of photo */}
        <div style={{
          position: 'absolute', bottom: 0, left: 0, width: '100%', height: '40%',
          background: `linear-gradient(to bottom, transparent, ${c.bg})`,
        }} />
      </div>

      {/* Kicker — top, centered on photo */}
      {kicker && (
        <div style={{
          position: 'absolute', top: 50, left: 0, right: 0,
          textAlign: 'center', zIndex: 5,
          fontSize: 26, color: '#fff', fontWeight: 600,
          textShadow: '0 2px 12px rgba(0,0,0,0.6)',
          letterSpacing: '0.1em',
        }}>
          {kicker}
        </div>
      )}

      {/* OVERLAPPING headline — sits at the photo/text boundary */}
      {headline && (
        <div style={{
          position: 'absolute', top: photoHeight - 60, left: 50, right: 50, zIndex: 10,
          fontSize: 68, fontWeight: 900, color: '#fff',
          lineHeight: 1.1, direction: rtl.direction, textAlign: rtl.textAlign,
          fontFamily: FONTS.kufi,
          textShadow: `0 4px 30px ${hexRgba(c.bg, '0.9')}, 0 2px 8px rgba(0,0,0,0.5)`,
        }}>
          {headline}
        </div>
      )}

      {/* Business name + accent bar */}
      <div style={{
        position: 'absolute', top: photoHeight + 80, left: 50, right: 50, zIndex: 5,
        display: 'flex', alignItems: 'center', gap: 16,
        flexDirection: rtl.direction === 'rtl' ? 'row-reverse' : 'row',
      }}>
        {businessName && (
          <span style={{
            fontSize: 34, fontWeight: 700,
            color: c.accentGlint || c.accent,
            direction: rtl.direction,
          }}>
            {businessName}
          </span>
        )}
        <div style={{ flex: 1, height: 2, background: hexRgba(c.accent, '0.4') }} />
      </div>

      {/* Content strip — bottom area */}
      <div style={{
        position: 'absolute', bottom: 120, left: 50, right: 50, zIndex: 5,
      }}>
        {/* Taglines as horizontal list */}
        {taglines.length > 0 && (
          <div style={{
            display: 'flex', gap: 30, marginBottom: 24,
            direction: rtl.direction,
            justifyContent: rtl.textAlign === 'right' ? 'flex-end' : 'flex-start',
          }}>
            {taglines.slice(0, 3).map((tag, i) => (
              <div key={i} style={{
                fontSize: 22, color: hexRgba(c.text, '0.85'), fontWeight: 500,
                borderRight: rtl.direction === 'rtl' ? `2px solid ${c.accent}` : 'none',
                borderLeft: rtl.direction === 'ltr' ? `2px solid ${c.accent}` : 'none',
                paddingRight: rtl.direction === 'rtl' ? 12 : 0,
                paddingLeft: rtl.direction === 'ltr' ? 12 : 0,
              }}>
                {tag}
              </div>
            ))}
          </div>
        )}

        {/* CTA + Rating */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: 24,
          direction: rtl.direction,
        }}>
          {ctaText && (
            <div style={{
              background: c.accent, color: '#fff',
              padding: '14px 36px', borderRadius: 30,
              fontSize: 24, fontWeight: 800,
              boxShadow: accentShadow(c.accent, 'medium'), boxShadow: depthShadow('subtle'),
            }}>
              {truncateCta(ctaText, 30)}
            </div>
          )}
          {trustBadge && (
            <span style={{
              fontSize: 18, color: hexRgba(c.accentGlint || c.accent, '0.8'),
              border: `1px solid ${hexRgba(c.accent, '0.4')}`,
              padding: '6px 18px', borderRadius: 15,
            }}>
              {trustBadge}
            </span>
          )}
          <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            <span style={{ color: c.accentGlint || '#FFD700', fontSize: 22 }}>
              {'★'.repeat(Math.round(rating))}
            </span>
            <span style={{ color: c.text, fontSize: 20, fontWeight: 700 }}>
              {toArabicDigits(rating)}
            </span>
            <span style={{ color: hexRgba(c.text, '0.5'), fontSize: 16 }}>
              ({toArabicDigits(ratingCount)})
            </span>
          </div>
        </div>

        {hashtags.length > 0 && (
          <div style={{
            marginTop: 16, fontSize: 16,
            color: hexRgba(c.accent, '0.6'),
            direction: rtl.direction, textAlign: rtl.textAlign,
          }}>
            {hashtags.slice(0, 4).join('  ')}
          </div>
        )}
      </div>

      {/* Footer */}
      <div style={{
        position: 'absolute', bottom: 0, left: 0, right: 0,
        display: 'flex', justifyContent: 'space-between',
        padding: '10px 50px',
        background: hexRgba(c.bg, '0.85'),
        borderTop: `1px solid ${hexRgba(c.accent, '0.3')}`,
      }}>
        <span style={{ color: c.accentGlint || c.accent, fontSize: 15, fontWeight: 600 }}>
          نُهوت — التسويق الرقمي
        </span>
        <span style={{ color: hexRgba('#fff', '0.5'), fontSize: 15 }}>
          nuhoot.xyz
        </span>
      </div>
    </div>
  );
};

// ════════════════════════════════════════════════════════════════════
// 4. BOLD POSTER — Giant typography hero, photo as small accent
//    Aggressive, typographic, minimal
// ════════════════════════════════════════════════════════════════════
export const BoldPoster: React.FC<DramaticProps> = ({
  colors = DEFAULT_COLORS,
  kicker,
  headline,
  businessName,
  taglines = [],
  bodyText,
  ctaText,
  rating = 4.7,
  ratingCount = 15,
  hashtags = [],
  trustBadge,
  photoPath,
}) => {
  const c = useColors(colors);
  const rtl = rtlProps(headline);

  return (
    <div style={{
      width: W, height: H, position: 'relative', overflow: 'hidden',
      background: `linear-gradient(${c.gradientAngle || 135}deg, ${c.bg}, ${c.bg2})`,
      fontFamily: FONTS.sans,
    }}>
      {/* Aggressive diagonal color block */}
      <div style={{
        position: 'absolute', top: -100, right: -200,
        width: 600, height: 600,
        background: hexRgba(c.accent, '0.15'),
        transform: 'rotate(25deg)',
        borderRadius: 80,
      }} />
      <div style={{
        position: 'absolute', bottom: -150, left: -150,
        width: 500, height: 500,
        background: hexRgba(c.accent2, '0.1'),
        transform: 'rotate(-15deg)',
        borderRadius: 60,
      }} />

      {/* Kicker — top, LEFT side only (avoid photo area) */}
      {kicker && (
        <div style={{
          position: 'absolute', top: 60, left: 50, right: 540,
          fontSize: 24, fontWeight: 700, color: c.accent,
          direction: rtl.direction, textAlign: rtl.textAlign,
          letterSpacing: '0.08em',
        }}>
          {kicker}
        </div>
      )}

      {/* GIANT headline — LEFT side, constrained width to not overlap photo */}
      {headline && (
        <div style={{
          position: 'absolute', top: 110, left: 50, right: 540,
          fontSize: 64, fontWeight: 900, color: c.text,
          lineHeight: 1.1, direction: rtl.direction, textAlign: rtl.textAlign,
          fontFamily: FONTS.kufi,
          textShadow: `0 0 60px ${hexRgba(c.accent, '0.3')}`,
        }}>
          {headline}
        </div>
      )}

      {/* Business name — below headline, accent color */}
      {businessName && (
        <div style={{
          position: 'absolute', top: 290, left: 50, right: 540,
          fontSize: 32, fontWeight: 800,
          color: c.accentGlint || c.accent,
          direction: rtl.direction, textAlign: rtl.textAlign,
        }}>
          {businessName}
        </div>
      )}

      {/* Photo — large rectangle, RIGHT side */}
      {photoPath && (
        <div style={{
          position: 'absolute', top: 80, right: 50,
          width: 440, height: 400, borderRadius: 20,
          overflow: 'hidden',
          border: `5px solid ${c.accent}`,
          boxShadow: depthShadow('floating'),
          zIndex: 3,
        }}>
          <img
            src={resolvePhoto(photoPath)}
            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          />
        </div>
      )}

      {/* Taglines — below business name, LEFT side */}
      {taglines.length > 0 && (
        <div style={{
          position: 'absolute', top: 510, left: 50, right: 540,
          display: 'flex', flexDirection: 'column', gap: 12,
          direction: rtl.direction, textAlign: rtl.textAlign,
        }}>
          {taglines.slice(0, 3).map((tag, i) => (
            <div key={i} style={{
              fontSize: 24, fontWeight: 600, color: c.text,
              display: 'flex', alignItems: 'center', gap: 12,
              flexDirection: rtl.direction === 'rtl' ? 'row-reverse' : 'row',
            }}>
              <span style={{
                width: 10, height: 10, borderRadius: '50%',
                background: c.accent, flexShrink: 0,
              }} />
              {tag}
            </div>
          ))}
        </div>
      )}

      {/* CTA — full width bar */}
      {ctaText && (
        <div style={{
          position: 'absolute', bottom: 140, left: 50, right: 50,
          background: c.accent, color: '#fff',
          padding: '18px 40px', borderRadius: 14,
          fontSize: 28, fontWeight: 900,
          textAlign: 'center',
          boxShadow: accentShadow(c.accent, 'medium'),
        }}>
          {truncateCta(ctaText, 40)}
        </div>
      )}

      {/* Rating — single clean line, full width */}
      <div style={{
        position: 'absolute', bottom: 85, left: 50, right: 50,
        display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 12,
      }}>
        <span style={{ color: c.accentGlint || '#FFD700', fontSize: 22 }}>
          {'★'.repeat(Math.round(rating))}
        </span>
        <span style={{ color: c.text, fontSize: 20, fontWeight: 700 }}>
          {toArabicDigits(rating)}
        </span>
        <span style={{ color: hexRgba(c.text, '0.5'), fontSize: 16 }}>
          ({toArabicDigits(ratingCount)} تقييم)
        </span>
        {trustBadge && (
          <>
            <span style={{ color: hexRgba(c.accent, '0.4'), fontSize: 16 }}>·</span>
            <span style={{ fontSize: 16, color: c.accent, fontWeight: 600 }}>
              {trustBadge}
            </span>
          </>
        )}
      </div>

      {/* Hashtags — subtle */}
      {hashtags.length > 0 && (
        <div style={{
          position: 'absolute', bottom: 60, left: 50, right: 50,
          fontSize: 15, color: hexRgba(c.accent, '0.5'),
          direction: rtl.direction, textAlign: 'center',
        }}>
          {hashtags.slice(0, 3).join('  ')}
        </div>
      )}

      {/* Footer */}
      <div style={{
        position: 'absolute', bottom: 0, left: 0, right: 0,
        display: 'flex', justifyContent: 'space-between',
        padding: '10px 50px',
        background: hexRgba(c.bg, '0.9'),
        borderTop: `1px solid ${hexRgba(c.accent, '0.3')}`,
        fontFamily: FONTS.kufi,
      }}>
        <span style={{ color: c.accentGlint || c.accent, fontSize: 14, fontWeight: 600 }}>
          نُهوت — التسويق الرقمي
        </span>
        <span style={{ color: hexRgba('#fff', '0.4'), fontSize: 14 }}>
          nuhoot.xyz
        </span>
      </div>
    </div>
  );
};

// ════════════════════════════════════════════════════════════════════
// 5. OVERLAPPING CARDS — Photos cascade/overlap, text floats
//    Dynamic, modern, social-media native
// ════════════════════════════════════════════════════════════════════
export const OverlappingCards: React.FC<DramaticProps> = ({
  colors = DEFAULT_COLORS,
  kicker,
  headline,
  businessName,
  taglines = [],
  bodyText,
  ctaText,
  rating = 4.7,
  ratingCount = 15,
  hashtags = [],
  trustBadge,
  photoPath,
  photoPath2,
  photoPath3,
}) => {
  const c = useColors(colors);
  const rtl = rtlProps(headline);

  return (
    <div style={{
      width: W, height: H, position: 'relative', overflow: 'hidden',
      background: `linear-gradient(${c.gradientAngle || 145}deg, ${c.bg}, ${c.bg2})`,
      fontFamily: FONTS.sans,
    }}>
      {/* Decorative circles */}
      <div style={{
        position: 'absolute', top: -80, right: -80,
        width: 300, height: 300, borderRadius: '50%',
        background: hexRgba(c.accent, '0.08'),
      }} />

      {/* Kicker */}
      {kicker && (
        <div style={{
          position: 'absolute', top: 55, left: 50,
          fontSize: 24, color: c.accent, fontWeight: 600,
          letterSpacing: '0.05em',
        }}>
          {kicker}
        </div>
      )}

      {/* Headline — top left, large */}
      {headline && (
        <div style={{
          position: 'absolute', top: 95, left: 50, right: 300,
          fontSize: 60, fontWeight: 900, color: c.text,
          lineHeight: 1.15, direction: rtl.direction, textAlign: rtl.textAlign,
          fontFamily: FONTS.kufi,
        }}>
          {headline}
        </div>
      )}

      {/* Overlapping photos — cascade top-right to center */}
      {/* Photo 1 — large, top right */}
      {photoPath && (
        <div style={{
          position: 'absolute', top: 80, right: 50,
          width: 380, height: 380, borderRadius: 24,
          overflow: 'hidden',
          border: `5px solid ${hexRgba(c.accent, '0.3')}`,
          zIndex: 3,
          boxShadow: depthShadow('deep'),
        }}>
          <img src={resolvePhoto(photoPath)} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        </div>
      )}

      {/* Photo 2 — medium, offset, overlapping */}
      {photoPath2 && (
        <div style={{
          position: 'absolute', top: 280, right: 200,
          width: 280, height: 280, borderRadius: 20,
          overflow: 'hidden',
          border: `4px solid ${c.bg}`,
          zIndex: 4,
          boxShadow: depthShadow('floating'),
        }}>
          <img src={resolvePhoto(photoPath2)} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        </div>
      )}

      {/* Photo 3 — small accent */}
      {photoPath3 && (
        <div style={{
          position: 'absolute', top: 480, right: 60,
          width: 180, height: 180, borderRadius: 16,
          overflow: 'hidden',
          border: `4px solid ${c.accent}`,
          zIndex: 5,
          boxShadow: depthShadow('medium'),
        }}>
          <img src={resolvePhoto(photoPath3)} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        </div>
      )}

      {/* Business name */}
      {businessName && (
        <div style={{
          position: 'absolute', top: 420, left: 50, right: 400,
          fontSize: 34, fontWeight: 800,
          color: c.accentGlint || c.accent,
          direction: rtl.direction, textAlign: rtl.textAlign,
        }}>
          {businessName}
        </div>
      )}

      {/* Taglines — floating in left space */}
      {taglines.length > 0 && (
        <div style={{
          position: 'absolute', top: 490, left: 50, right: 420,
          display: 'flex', flexDirection: 'column', gap: 12,
          direction: rtl.direction, textAlign: rtl.textAlign,
        }}>
          {taglines.slice(0, 3).map((tag, i) => (
            <div key={i} style={{
              display: 'flex', alignItems: 'center', gap: 12,
              flexDirection: rtl.direction === 'rtl' ? 'row-reverse' : 'row',
            }}>
              <div style={{
                width: 36, height: 36, borderRadius: 10,
                background: hexRgba(c.accent, '0.2'),
                border: `1.5px solid ${hexRgba(c.accent, '0.5')}`,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                color: c.accent, fontSize: 18, fontWeight: 800, flexShrink: 0,
              }}>
                {toArabicDigits(i + 1)}
              </div>
              <span style={{ fontSize: 22, color: c.text, fontWeight: 500 }}>{tag}</span>
            </div>
          ))}
        </div>
      )}

      {/* CTA + rating row */}
      <div style={{
        position: 'absolute', bottom: 130, left: 50, right: 50,
        display: 'flex', alignItems: 'center', gap: 24,
        direction: rtl.direction,
      }}>
        {ctaText && (
          <div style={{
            background: c.accent, color: '#fff',
            padding: '16px 40px', borderRadius: 30,
            fontSize: 26, fontWeight: 800,
            boxShadow: accentShadow(c.accent, 'medium'), boxShadow: depthShadow('medium'),
          }}>
            {truncateCta(ctaText, 32)}
          </div>
        )}
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span style={{ color: c.accentGlint || '#FFD700', fontSize: 22 }}>
            {'★'.repeat(Math.round(rating))}
          </span>
          <span style={{ color: c.text, fontSize: 20, fontWeight: 700 }}>
            {toArabicDigits(rating)}
          </span>
          <span style={{ color: hexRgba(c.text, '0.5'), fontSize: 16 }}>
            ({toArabicDigits(ratingCount)})
          </span>
        </div>
        {trustBadge && (
          <span style={{
            fontSize: 16, color: hexRgba(c.accent, '0.8'),
            border: `1px solid ${hexRgba(c.accent, '0.4')}`,
            padding: '4px 16px', borderRadius: 12,
          }}>
            {trustBadge}
          </span>
        )}
      </div>

      {hashtags.length > 0 && (
        <div style={{
          position: 'absolute', bottom: 80, left: 50, right: 50,
          fontSize: 16, color: hexRgba(c.accent, '0.5'),
          direction: rtl.direction, textAlign: rtl.textAlign,
        }}>
          {hashtags.slice(0, 4).join('  ')}
        </div>
      )}

      {/* Footer */}
      <div style={{
        position: 'absolute', bottom: 0, left: 0, right: 0,
        display: 'flex', justifyContent: 'space-between',
        padding: '10px 50px',
        background: hexRgba(c.bg, '0.9)'),
        borderTop: `1px solid ${hexRgba(c.accent, '0.3')}`,
      }}>
        <span style={{ color: c.accentGlint || c.accent, fontSize: 15, fontWeight: 600 }}>
          نُهوت — التسويق الرقمي
        </span>
        <span style={{ color: hexRgba('#fff', '0.5'), fontSize: 15 }}>
          nuhoot.xyz
        </span>
      </div>
    </div>
  );
};

// ════════════════════════════════════════════════════════════════════
// 6. MINIMAL LUXURY — 60% negative space, arch photo, gold accents
//    Ultra-premium, elegant, like a luxury brand ad
// ════════════════════════════════════════════════════════════════════
export const MinimalLuxury: React.FC<DramaticProps> = ({
  colors = DEFAULT_COLORS,
  kicker,
  headline,
  businessName,
  taglines = [],
  bodyText,
  ctaText,
  rating = 4.7,
  ratingCount = 15,
  hashtags = [],
  trustBadge,
  photoPath,
}) => {
  const c = useColors(colors);
  const rtl = rtlProps(headline);

  return (
    <div style={{
      width: W, height: H, position: 'relative', overflow: 'hidden',
      background: `linear-gradient(${c.gradientAngle || 180}deg, ${c.bg2}, ${c.bg})`,
      fontFamily: FONTS.naskh,
    }}>
      {/* Subtle decorative line — top */}
      <div style={{
        position: 'absolute', top: 60, left: '50%',
        transform: 'translateX(-50%)',
        width: 120, height: 1,
        background: hexRgba(c.accentGlint || c.accent, '0.6'),
      }} />

      {/* Kicker — centered, small, elegant */}
      {kicker && (
        <div style={{
          position: 'absolute', top: 80, left: 0, right: 0,
          textAlign: 'center',
          fontSize: 22, color: c.accentGlint || c.accent,
          fontWeight: 500, letterSpacing: '0.15em',
        }}>
          {kicker}
        </div>
      )}

      {/* Arch-shaped photo — center, premium */}
      {photoPath && (
        <div style={{
          position: 'absolute', top: 140, left: '50%',
          transform: 'translateX(-50%)',
          width: 420, height: 480,
          borderRadius: '210px 210px 0 0', // Arch shape
          overflow: 'hidden',
          border: `2px solid ${hexRgba(c.accentGlint || c.accent, '0.3')}`,
          boxShadow: depthShadow('subtle'),
        }}>
          <img src={resolvePhoto(photoPath)} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
          {/* Gold frame inside arch */}
          <div style={{
            position: 'absolute', inset: 8,
            borderRadius: '200px 200px 0 0',
            border: `1px solid ${hexRgba(c.accentGlint || c.accent, '0.4')}`,
          }} />
        </div>
      )}

      {/* Headline — centered below arch, elegant */}
      {headline && (
        <div style={{
          position: 'absolute', top: 660, left: 50, right: 50,
          textAlign: 'center',
          fontSize: 52, fontWeight: 700, color: c.text,
          lineHeight: 1.2, direction: rtl.direction,
          fontFamily: FONTS.naskh,
        }}>
          {headline}
        </div>
      )}

      {/* Business name — gold accent */}
      {businessName && (
        <div style={{
          position: 'absolute', top: 740, left: 0, right: 0,
          textAlign: 'center',
          fontSize: 28, fontWeight: 600,
          color: c.accentGlint || c.accent,
          direction: rtl.direction,
        }}>
          {businessName}
        </div>
      )}

      {/* Taglines — centered, inline with separator */}
      {taglines.length > 0 && (
        <div style={{
          position: 'absolute', top: 800, left: 0, right: 0,
          display: 'flex', justifyContent: 'center', gap: 20,
          direction: rtl.direction,
        }}>
          {taglines.slice(0, 3).map((tag, i) => (
            <React.Fragment key={i}>
              {i > 0 && <span style={{ color: hexRgba(c.accent, '0.3'), fontSize: 18 }}>·</span>}
              <span style={{
                fontSize: 20, color: hexRgba(c.text, '0.7'), fontWeight: 400,
              }}>
                {tag}
              </span>
            </React.Fragment>
          ))}
        </div>
      )}

      {/* CTA — minimal outline button */}
      {ctaText && (
        <div style={{
          position: 'absolute', top: 870, left: '50%',
          transform: 'translateX(-50%)',
          border: `1.5px solid ${c.accent}`,
          padding: '12px 40px', borderRadius: 0, // Sharp corners = luxury
          fontSize: 22, fontWeight: 600, color: c.accent,
          background: 'transparent',
          letterSpacing: '0.05em',
        }}>
          {truncateCta(ctaText, 30)}
        </div>
      )}

      {/* Rating — minimal, centered */}
      <div style={{
        position: 'absolute', top: 940, left: 0, right: 0,
        display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 8,
      }}>
        <span style={{ color: c.accentGlint || '#FFD700', fontSize: 18 }}>
          {'★'.repeat(Math.round(rating))}
        </span>
        <span style={{ color: hexRgba(c.text, '0.6'), fontSize: 18 }}>
          {toArabicDigits(rating)} · {toArabicDigits(ratingCount)} تقييم
        </span>
      </div>

      {/* Trust badge — minimal */}
      {trustBadge && (
        <div style={{
          position: 'absolute', top: 975, left: 0, right: 0,
          textAlign: 'center',
          fontSize: 16, color: hexRgba(c.accent, '0.5'),
        }}>
          {trustBadge}
        </div>
      )}

      {/* Hashtags — very subtle */}
      {hashtags.length > 0 && (
        <div style={{
          position: 'absolute', bottom: 60, left: 0, right: 0,
          textAlign: 'center',
          fontSize: 14, color: hexRgba(c.accent, '0.3)'),
        }}>
          {hashtags.slice(0, 3).join('  ·  ')}
        </div>
      )}

      {/* Footer — minimal */}
      <div style={{
        position: 'absolute', bottom: 20, left: 0, right: 0,
        display: 'flex', justifyContent: 'space-between',
        padding: '0 50px',
      }}>
        <span style={{ color: hexRgba(c.accentGlint || c.accent, '0.6'), fontSize: 14, fontWeight: 500 }}>
          نُهوت — التسويق الرقمي
        </span>
        <span style={{ color: hexRgba('#fff', '0.3'), fontSize: 14 }}>
          nuhoot.xyz
        </span>
      </div>
    </div>
  );
};

// ─── Export registry ─────────────────────────────────────────────────
export const DRAMATIC_LAYOUTS = {
  HeroFullBleed,
  SplitScreen,
  MagazineCover,
  BoldPoster,
  OverlappingCards,
  MinimalLuxury,
};

export const DRAMATIC_LAYOUT_NAMES = Object.keys(DRAMATIC_LAYOUTS);
