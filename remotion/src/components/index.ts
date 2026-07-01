// ─────────────────────────────────────────────────────────────────────
// Nuhoot Design Engine — Component Library Index
// ─────────────────────────────────────────────────────────────────────
// 76 components across 15+ categories (56 original + 20 new from design research)
//
//   Headers     (5): HeaderMinimal, HeaderGradient, HeaderSplit, HeaderOverlay, HeaderMixed
//   Photos      (10): PhotoSingle, PhotoGrid, PhotoMosaic, PhotoCarousel, PhotoFrame,
//                      PhotoArch, PhotoCircle, PhotoDiagonal, PhotoDuotone, PhotoDoubleFrame
//   Content     (5): ContentCards, ContentList, ContentStats, ContentQuotes, ContentFeatures
//   CTAs        (4): CTAButton, CTABanner, CTAFloating, CTAInline
//   Decorative  (10): DecorShapes, DecorRings, DecorWatermark, DecorGradient,
//                     Divider, EdgeLabel, DecorVignette, DecorDiagonal, ColorPanel, DecorCalligraphy
//   Footers     (4): FooterRating, FooterHashtags, FooterBranding, FooterComplete
//   Layouts     (5): LayoutStandard, LayoutSplit, LayoutAsymmetric, LayoutMagazine, LayoutPhotoFull
//   Icons       (2): Icon, IconBadge
//   Badges      (6): StatusBadge, RatingBadge, TrustBadge, DiscountBadge, SealBadge, OfferRibbon
//   Pricing     (3): PriceTag, PriceStrike, PriceCard
//   Premium CTAs(4): CTAShimmer, CTAGlow, CTAOutline, CTADual
//   Patterns    (8): PatternGrid, PatternDots, PatternHex, PatternRays, PatternBokeh,
//                    TextureGrain, PatternIslamic, TextureOverlay
//   Social      (2): SocialBar, ContactRow
//   Progress    (3): BarProgress, RingProgress, GoalMeter
//   Frames      (5): FramePolaroid, FrameStack, FrameCircle, CornerBrackets, FrameKeyline
// ─────────────────────────────────────────────────────────────────────

// ─── Shared helpers, types & primitives ──────────────────────────────
export {
  hexRgba,
  hexShift,
  toArabicDigits,
  optimalFontSize,
  truncateCta,
  rtlProps,
  resolvePhoto,
  useColors,
  DEFAULT_COLORS,
  FONTS,
  StarRating,
  depthShadow,
  accentShadow,
  GlassCard,
  GoldFoilText,
  typeScale,
  gradientTextStyle,
  goldFoilTextStyle,
  photoOverlayStyle,
  vignetteStyle,
  innerGlowStyle,
} from './helpers';

export type {
  ColorConfig,
  BaseBlockProps,
  RTLInfo,
  GlassCardProps,
} from './helpers';

// ─── Headers (5) ──────────────────────────────────────────────────────
export {
  HeaderMinimal,
  HeaderGradient,
  HeaderSplit,
  HeaderOverlay,
  HeaderMixed,
} from './headers';

export type {
  HeaderMinimalProps,
  HeaderGradientProps,
  HeaderSplitProps,
  HeaderOverlayProps,
  HeaderMixedProps,
} from './headers';

// ─── Photos (10) ──────────────────────────────────────────────────────
export {
  PhotoSingle,
  PhotoGrid,
  PhotoMosaic,
  PhotoCarousel,
  PhotoFrame,
  PhotoArch,
  PhotoCircle,
  PhotoDiagonal,
  PhotoDuotone,
  PhotoDoubleFrame,
} from './photos';

export type {
  PhotoSingleProps,
  PhotoGridProps,
  PhotoMosaicProps,
  PhotoCarouselProps,
  PhotoFrameProps,
  PhotoArchProps,
  PhotoCircleProps,
  PhotoDiagonalProps,
  PhotoDuotoneProps,
  PhotoDoubleFrameProps,
} from './photos';

// ─── Content (5) ───────────────────────────────────────────────────────
export {
  ContentCards,
  ContentList,
  ContentStats,
  ContentQuotes,
  ContentFeatures,
} from './content';

export type {
  ContentCardsProps,
  ContentListProps,
  ContentStatsProps,
  ContentQuotesProps,
  ContentFeaturesProps,
  ContentCardItem,
  StatItem,
  FeatureItem,
} from './content';

// ─── CTAs (4) ──────────────────────────────────────────────────────────
export {
  CTAButton,
  CTABanner,
  CTAFloating,
  CTAInline,
} from './ctas';

export type {
  CTAButtonProps,
  CTABannerProps,
  CTAFloatingProps,
  CTAInlineProps,
} from './ctas';

// ─── Decorative (10) ───────────────────────────────────────────────────
export {
  DecorShapes,
  DecorRings,
  DecorWatermark,
  DecorGradient,
  Divider,
  EdgeLabel,
  DecorVignette,
  DecorDiagonal,
  ColorPanel,
  DecorCalligraphy,
} from './decorative';

export type {
  DecorShapesProps,
  DecorRingsProps,
  DecorWatermarkProps,
  DecorGradientProps,
  DecorShape,
  DecorRing,
  DividerProps,
  EdgeLabelProps,
  DecorVignetteProps,
  DecorDiagonalProps,
  ColorPanelProps,
  DecorCalligraphyProps,
} from './decorative';

// ─── Footers (4) ──────────────────────────────────────────────────────
export {
  FooterRating,
  FooterHashtags,
  FooterBranding,
  FooterComplete,
} from './footers';

export type {
  FooterRatingProps,
  FooterHashtagsProps,
  FooterBrandingProps,
  FooterCompleteProps,
} from './footers';

// ─── Layouts (5) ──────────────────────────────────────────────────────
export {
  LayoutStandard,
  LayoutSplit,
  LayoutAsymmetric,
  LayoutMagazine,
  LayoutPhotoFull,
} from './layouts';

export type {
  LayoutStandardProps,
  LayoutSplitProps,
  LayoutAsymmetricProps,
  LayoutMagazineProps,
  LayoutPhotoFullProps,
} from './layouts';

// ─── Icons (2) ─────────────────────────────────────────────────────────
export { Icon, IconBadge, ICON_MAP } from './icon';
export type { IconProps, IconBadgeProps } from './icon';

// ─── Badges (6) ────────────────────────────────────────────────────────
export { StatusBadge, RatingBadge, TrustBadge, DiscountBadge, SealBadge, OfferRibbon } from './badges';
export type { StatusBadgeProps, RatingBadgeProps, TrustBadgeProps, DiscountBadgeProps, SealBadgeProps, OfferRibbonProps } from './badges';

// ─── Pricing (3) ──────────────────────────────────────────────────────
export { PriceTag, PriceStrike, PriceCard } from './pricing';
export type { PriceTagProps, PriceStrikeProps, PriceCardProps } from './pricing';

// ─── Premium CTAs (4) ──────────────────────────────────────────────────
export { CTAShimmer, CTAGlow, CTAOutline, CTADual } from './buttons-pro';
export type { CTAShimmerProps, CTAGlowProps, CTAOutlineProps, CTADualProps } from './buttons-pro';

// ─── Patterns (8) ──────────────────────────────────────────────────────
export { PatternGrid, PatternDots, PatternHex, PatternRays, PatternBokeh, TextureGrain, PatternIslamic, TextureOverlay } from './patterns';
export type { PatternGridProps, PatternDotsProps, PatternHexProps, PatternRaysProps, PatternBokehProps, TextureGrainProps, PatternIslamicProps, TextureOverlayProps } from './patterns';

// ─── Social (2) ────────────────────────────────────────────────────────
export { SocialBar, ContactRow } from './social';
export type { SocialBarProps, ContactRowProps } from './social';

// ─── Progress (3) ──────────────────────────────────────────────────────
export { BarProgress, RingProgress, GoalMeter } from './progress';
export type { BarProgressProps, RingProgressProps, GoalMeterProps } from './progress';

// ─── Frames (5) ────────────────────────────────────────────────────────
export { FramePolaroid, FrameStack, FrameCircle, CornerBrackets, FrameKeyline } from './frames';
export type { FramePolaroidProps, FrameStackProps, FrameCircleProps, CornerBracketsProps, FrameKeylineProps } from './frames';

// ─── Component Registry (for DynamicComposer whitelist) ──────────────
import {
  HeaderMinimal, HeaderGradient, HeaderSplit, HeaderOverlay, HeaderMixed,
} from './headers';
import {
  PhotoSingle, PhotoGrid, PhotoMosaic, PhotoCarousel, PhotoFrame,
  PhotoArch, PhotoCircle, PhotoDiagonal, PhotoDuotone, PhotoDoubleFrame,
} from './photos';
import {
  ContentCards, ContentList, ContentStats, ContentQuotes, ContentFeatures,
} from './content';
import { CTAButton, CTABanner, CTAFloating, CTAInline } from './ctas';
import {
  DecorShapes, DecorRings, DecorWatermark, DecorGradient,
  Divider, EdgeLabel, DecorVignette, DecorDiagonal, ColorPanel, DecorCalligraphy,
} from './decorative';
import { FooterRating, FooterHashtags, FooterBranding, FooterComplete } from './footers';
import {
  LayoutStandard, LayoutSplit, LayoutAsymmetric, LayoutMagazine, LayoutPhotoFull,
} from './layouts';
import { Icon, IconBadge } from './icon';
import { StatusBadge, RatingBadge, TrustBadge, DiscountBadge, SealBadge, OfferRibbon } from './badges';
import { PriceTag, PriceStrike, PriceCard } from './pricing';
import { CTAShimmer, CTAGlow, CTAOutline, CTADual } from './buttons-pro';
import { PatternGrid, PatternDots, PatternHex, PatternRays, PatternBokeh, TextureGrain, PatternIslamic, TextureOverlay } from './patterns';
import { SocialBar, ContactRow } from './social';
import { BarProgress, RingProgress, GoalMeter } from './progress';
import { FramePolaroid, FrameStack, FrameCircle, CornerBrackets, FrameKeyline } from './frames';

export const COMPONENT_REGISTRY: Record<string, React.FC<any>> = {
  // Headers (5)
  HeaderMinimal, HeaderGradient, HeaderSplit, HeaderOverlay, HeaderMixed,
  // Photos (10)
  PhotoSingle, PhotoGrid, PhotoMosaic, PhotoCarousel, PhotoFrame,
  PhotoArch, PhotoCircle, PhotoDiagonal, PhotoDuotone, PhotoDoubleFrame,
  // Content (5)
  ContentCards, ContentList, ContentStats, ContentQuotes, ContentFeatures,
  // CTAs (4)
  CTAButton, CTABanner, CTAFloating, CTAInline,
  // Decorative (10)
  DecorShapes, DecorRings, DecorWatermark, DecorGradient,
  Divider, EdgeLabel, DecorVignette, DecorDiagonal, ColorPanel, DecorCalligraphy,
  // Footers (4)
  FooterRating, FooterHashtags, FooterBranding, FooterComplete,
  // Layouts (5)
  LayoutStandard, LayoutSplit, LayoutAsymmetric, LayoutMagazine, LayoutPhotoFull,
  // Icons (2)
  Icon, IconBadge,
  // Badges (6)
  StatusBadge, RatingBadge, TrustBadge, DiscountBadge, SealBadge, OfferRibbon,
  // Pricing (3)
  PriceTag, PriceStrike, PriceCard,
  // Premium CTAs (4)
  CTAShimmer, CTAGlow, CTAOutline, CTADual,
  // Patterns (8)
  PatternGrid, PatternDots, PatternHex, PatternRays, PatternBokeh,
  TextureGrain, PatternIslamic, TextureOverlay,
  // Social (2)
  SocialBar, ContactRow,
  // Progress (3)
  BarProgress, RingProgress, GoalMeter,
  // Frames (5)
  FramePolaroid, FrameStack, FrameCircle, CornerBrackets, FrameKeyline,
};

export const ALLOWED_COMPONENTS = new Set(Object.keys(COMPONENT_REGISTRY));
