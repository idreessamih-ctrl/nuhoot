// ─────────────────────────────────────────────────────────────────────
// Nuhoot Design Engine — DynamicComposer (Phase 2)
// ─────────────────────────────────────────────────────────────────────
// The bridge between Kimi's JSON design blueprint and the rendered
// output. Takes a DesignBlueprint, validates it, and safely composes
// the registered component library into a single Remotion frame.
//
// Safety guarantees:
//   • Only whitelisted components (ALLOWED_COMPONENTS) are ever rendered.
//   • Each block is wrapped in an ErrorBoundary so one bad block can't
//     crash the whole composition — it is skipped with a console.error.
//   • Blueprint structure is validated before rendering; invalid
//     blueprints fall back to a safe empty frame.
//   • No eval / no dynamic import / no string→JSX parsing — the registry
//     is a static map compiled into the bundle, so there is no injection
//     surface.
// ─────────────────────────────────────────────────────────────────────

import React from 'react';
import { AbsoluteFill } from 'remotion';
import {
  COMPONENT_REGISTRY,
  ALLOWED_COMPONENTS,
  DEFAULT_COLORS,
} from './components';
import type { ColorConfig } from './components';
import { DRAMATIC_LAYOUTS } from './components/dramatic_layouts';
import type { DramaticProps } from './components/dramatic_layouts';

// ─── Blueprint Types ─────────────────────────────────────────────────
// The JSON contract that Kimi (the designer LLM) produces. These types
// are exported so both the Python prompt layer and any TS consumer share
// a single source of truth for the blueprint shape.

/**
 * A single block in the composition array.
 * Maps a string component name to its props.
 */
export interface DesignBlock {
  /** Unique id within the composition (used as the React key). */
  id: string;
  /** Component name — must exist in COMPONENT_REGISTRY & ALLOWED_COMPONENTS. */
  component: string;
  /** Props forwarded to the component (colors, style, text, photos, etc.). */
  props: Record<string, any>;
  /**
   * Flex grow value for layout distribution. 0 = natural height (default),
   * 1+ = grow to fill available space. Auto-assigned if omitted:
   * photos/overlays get flex:1, footers get marginTop:auto.
   */
  flex?: number;
}

/**
 * Global styles applied to the AbsoluteFill wrapper, plus optional
 * semantic color hints that are injected into blocks lacking their own
 * `colors` prop.
 */
export interface GlobalStyles {
  /** CSS background-color for the root frame. */
  backgroundColor?: string;
  /** CSS background (gradient, etc.) for the root frame. */
  background?: string;
  /** Font family for the root frame. */
  fontFamily?: string;
  /** Text direction. Defaults to 'rtl' for Arabic content. */
  direction?: 'rtl' | 'ltr';
  /** Semantic primary color — injected as default ColorConfig.accent. */
  primaryColor?: string;
  /** Semantic accent color — injected as default ColorConfig.accent2. */
  accentColor?: string;
  /** Text color for the root frame. */
  color?: string;
  /** Any additional CSS properties passed through to the wrapper. */
  [key: string]: any;
}

/**
 * The full blueprint produced by Kimi.
 */
export interface DesignBlueprint {
  /** Free-form label for the design pattern (e.g. "modern-split"). */
  designPattern?: string;
  /** Human-readable rationale (not rendered, kept for debugging). */
  rationale?: string;
  /** Ordered list of blocks to render top-to-bottom. */
  composition: DesignBlock[];
  /** Global styles + color hints applied to the whole frame. */
  globalStyles?: GlobalStyles;
  /** Optional Arabic copy metadata (not rendered directly). */
  arabicCopy?: Record<string, any>;
  /** If set, render a dramatic layout instead of composing blocks. */
  dramaticLayout?: string;
  /** Content props for the dramatic layout. */
  dramaticContent?: Partial<DramaticProps>;
}

/**
 * Props accepted by the DynamicComposer component.
 * The index signature makes this compatible with Remotion's
 * `Record<string, unknown>` composition typing.
 */
export interface DynamicComposerProps {
  /** The design blueprint from Kimi. */
  blueprint: DesignBlueprint;
  [key: string]: unknown;
}

// ─── Validation ───────────────────────────────────────────────────────

export interface ValidationResult {
  valid: boolean;
  errors: string[];
}

/**
 * Validate a blueprint's structure before rendering.
 * Checks: composition is a non-empty array, each block has id/component/
 * props, the component name is in the whitelist, and ids are unique.
 */
export const validateBlueprint = (bp: unknown): ValidationResult => {
  const errors: string[] = [];

  if (!bp || typeof bp !== 'object') {
    return { valid: false, errors: ['Blueprint is not an object.'] };
  }

  const blueprint = bp as Partial<DesignBlueprint>;

  if (!Array.isArray(blueprint.composition)) {
    errors.push('Blueprint.composition must be an array.');
    return { valid: false, errors };
  }

  if (blueprint.composition.length === 0) {
    errors.push('Blueprint.composition is empty.');
    return { valid: false, errors };
  }

  const seenIds = new Set<string>();

  blueprint.composition.forEach((block, i) => {
    const where = `block[${i}]`;

    if (!block || typeof block !== 'object') {
      errors.push(`${where}: not an object.`);
      return;
    }

    const b = block as Partial<DesignBlock>;

    if (typeof b.id !== 'string' || !b.id) {
      errors.push(`${where}: missing or invalid "id".`);
    } else if (seenIds.has(b.id)) {
      errors.push(`${where}: duplicate id "${b.id}".`);
    } else {
      seenIds.add(b.id);
    }

    if (typeof b.component !== 'string' || !b.component) {
      errors.push(`${where}: missing or invalid "component" name.`);
      return;
    }

    if (!ALLOWED_COMPONENTS.has(b.component)) {
      errors.push(
        `${where}: component "${b.component}" is not in the ALLOWED_COMPONENTS whitelist.`,
      );
    }

    if (b.props != null && typeof b.props !== 'object') {
      errors.push(`${where}: "props" must be an object.`);
    }
  });

  return { valid: errors.length === 0, errors };
};

// ─── Error Boundary (per-block) ──────────────────────────────────────
// React error boundaries must be class components. We wrap every block
// so that a single throwing component is skipped rather than nuking the
// whole render — important for unattended batch generation.

interface BoundaryState {
  hasError: boolean;
  error?: Error;
}

class BlockBoundary extends React.Component<
  { id: string; children: React.ReactNode },
  BoundaryState
> {
  state: BoundaryState = { hasError: false };

  static getDerivedStateFromError(error: Error): BoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    // eslint-disable-next-line no-console
    console.error(
      `[DynamicComposer] Block "${this.props.id}" threw during render:`,
      error,
      info.componentStack,
    );
  }

  render() {
    if (this.state.hasError) {
      // Graceful fallback: render nothing for the failed block.
      return null;
    }
    return this.props.children;
  }
}

// ─── Helpers ─────────────────────────────────────────────────────────

/**
 * Build a ColorConfig from GlobalStyles semantic hints, so blocks that
 * don't carry their own `colors` prop still inherit the blueprint's
 * palette. Falls back to DEFAULT_COLORS for any missing fields.
 */
const colorsFromGlobal = (g?: GlobalStyles): ColorConfig | undefined => {
  if (!g) return undefined;
  if (!g.primaryColor && !g.accentColor && !g.backgroundColor && !g.color) {
    return undefined;
  }
  const bg = g.backgroundColor || g.primaryColor || DEFAULT_COLORS.bg;
  const accent = g.primaryColor || g.accentColor || DEFAULT_COLORS.accent;
  const accent2 = g.accentColor || g.primaryColor || DEFAULT_COLORS.accent2;
  const text = g.color || DEFAULT_COLORS.text;
  // Heuristic: dark background → isDark true.
  const isDark = isColorDark(bg);
  return {
    bg,
    bg2: bg,
    accent,
    accent2,
    text,
    isDark,
    badgeBg: accent,
    badgeText: isDark ? '#FFFFFF' : '#1A1A1A',
  };
};

/**
 * Rough luminance check to decide if a background is "dark".
 * Used only to pick a sensible default for badgeText / text shadows.
 */
const isColorDark = (hex: string): boolean => {
  const h = hex.replace('#', '');
  if (h.length < 6) return true;
  const r = parseInt(h.substring(0, 2), 16);
  const g = parseInt(h.substring(2, 4), 16);
  const b = parseInt(h.substring(4, 6), 16);
  if (isNaN(r) || isNaN(g) || isNaN(b)) return true;
  // Perceived luminance (Rec. 709).
  const lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255;
  return lum < 0.5;
};

// CSS property keys that globalStyles may set directly on the wrapper.
const DIRECT_CSS_KEYS = new Set([
  'backgroundColor',
  'background',
  'backgroundImage',
  'backgroundSize',
  'backgroundPosition',
  'backgroundRepeat',
  'fontFamily',
  'fontSize',
  'fontWeight',
  'color',
  'direction',
  'textAlign',
  'padding',
  'margin',
  'overflow',
  'display',
  'flexDirection',
]);

/**
 * Convert GlobalStyles into a React.CSSProperties object for the
 * AbsoluteFill wrapper. Non-CSS keys (primaryColor, accentColor, etc.)
 * are filtered out.
 */
const globalToCss = (g?: GlobalStyles): React.CSSProperties => {
  if (!g) return {};
  const css: React.CSSProperties = {};
  for (const key of Object.keys(g)) {
    if (DIRECT_CSS_KEYS.has(key)) {
      (css as any)[key] = (g as any)[key];
    }
  }
  return css;
};

// ─── Single Block Renderer ────────────────────────────────────────────

// Components that should grow to fill available vertical space.
const FLEX_GROW_COMPONENTS = new Set([
  'PhotoSingle', 'PhotoGrid', 'PhotoMosaic', 'PhotoCarousel', 'PhotoFrame',
  'PhotoArch', 'PhotoCircle', 'PhotoDiagonal', 'PhotoDuotone', 'PhotoDoubleFrame',
  'FramePolaroid', 'FrameStack', 'FrameCircle',
]);

// Components that should stick to the bottom of the canvas.
const STICK_BOTTOM_COMPONENTS = new Set([
  'FooterComplete', 'FooterRating', 'FooterHashtags', 'FooterBranding',
]);

/**
 * Determines the flex/positioning style for a block wrapper based on
 * its component type and any explicit `flex` override in the blueprint.
 */
const getWrapperStyle = (block: DesignBlock): React.CSSProperties => {
  // Explicit flex from the blueprint takes priority.
  if (block.flex != null) {
    return { flex: block.flex, flexShrink: block.flex > 0 ? 1 : 0, minHeight: 0 };
  }
  // Auto: photos and overlays grow to fill space.
  if (FLEX_GROW_COMPONENTS.has(block.component)) {
    return { flex: 1, flexShrink: 1, minHeight: 0 };
  }
  // Auto: footers stick to the bottom.
  if (STICK_BOTTOM_COMPONENTS.has(block.component)) {
    return { flexShrink: 0, marginTop: 'auto' };
  }
  // Default: natural height, don't shrink.
  return { flexShrink: 0 };
};

interface RenderBlockProps {
  block: DesignBlock;
  globalColors?: ColorConfig;
}

/**
 * Renders one block: looks up the component, checks the whitelist,
 * injects global colors if the block doesn't carry its own, and wraps
 * the result in a per-block ErrorBoundary with proper flex sizing.
 */
const RenderBlock: React.FC<RenderBlockProps> = ({ block, globalColors }) => {
  const { id, component: name, props } = block;

  // Defense-in-depth: check both the registry AND the whitelist.
  if (!ALLOWED_COMPONENTS.has(name) || !COMPONENT_REGISTRY[name]) {
    console.error(
      `[DynamicComposer] Skipping block "${id}": component "${name}" is not allowed.`,
    );
    return null;
  }

  const Component = COMPONENT_REGISTRY[name];

  // Inject global colors if the block doesn't specify its own palette.
  const mergedProps =
    globalColors && props && !props.colors
      ? { ...props, colors: globalColors }
      : props || {};

  // Wrapper applies flex sizing so blocks fill the 1080×1080 canvas.
  const wrapperStyle = getWrapperStyle(block);
  const isFlexGrow = wrapperStyle.flex != null && wrapperStyle.flex > 0;

  // For flex-grow components, pass height:100% so they fill the wrapper.
  const fillStyle: React.CSSProperties = isFlexGrow
    ? { height: '100%', width: '100%' }
    : {};

  // Merge fill style into the component's own style prop without clobbering it.
  const finalProps = {
    ...mergedProps,
    style: { ...fillStyle, ...(mergedProps?.style || {}) },
  };

  return (
    <div style={{ ...wrapperStyle, display: 'flex', flexDirection: 'column' }}>
      <BlockBoundary id={id}>
        <Component key={id} {...finalProps} />
      </BlockBoundary>
    </div>
  );
};

// ─── Main Component ───────────────────────────────────────────────────

/**
 * DynamicComposer — renders a DesignBlueprint using the registered
 * component library. Safe by construction: whitelist + per-block error
 * boundaries + structural validation.
 */
export const DynamicComposer: React.FC<DynamicComposerProps> = ({
  blueprint,
}) => {
  // 0. Check for dramatic layout — bypass block composition entirely.
  if (blueprint.dramaticLayout && DRAMATIC_LAYOUTS[blueprint.dramaticLayout as keyof typeof DRAMATIC_LAYOUTS]) {
    const LayoutComp = DRAMATIC_LAYOUTS[blueprint.dramaticLayout as keyof typeof DRAMATIC_LAYOUTS];

    // Build ColorConfig from globalStyles.
    const g = blueprint.globalStyles;
    const globalColors = colorsFromGlobal(g);

    // Merge dramaticContent with colors from globalStyles.
    const contentProps: DramaticProps = {
      ...(blueprint.dramaticContent || {}),
      colors: globalColors,
    };

    return (
      <AbsoluteFill style={{ overflow: 'hidden' }}>
        <BlockBoundary id="dramatic">
          <LayoutComp {...contentProps} />
        </BlockBoundary>
      </AbsoluteFill>
    );
  }

  // 1. Validate the blueprint structure.
  const { valid, errors } = validateBlueprint(blueprint);
  if (!valid) {
    // eslint-disable-next-line no-console
    console.error(
      '[DynamicComposer] Invalid blueprint, rendering empty frame:',
      errors,
    );
    return (
      <AbsoluteFill
        style={{
          backgroundColor: '#1A1A2E',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: 'sans-serif',
          color: '#E94560',
          direction: 'rtl',
        }}
      >
        <div style={{ textAlign: 'center', padding: 40 }}>
          <div style={{ fontSize: 28, fontWeight: 800, marginBottom: 12 }}>
            ⚠ تصميل غير صالح
          </div>
          <div style={{ fontSize: 14, opacity: 0.7, direction: 'ltr' }}>
            Invalid design blueprint — see server logs for details.
          </div>
        </div>
      </AbsoluteFill>
    );
  }

  // 2. Resolve global styles + semantic colors.
  const g = blueprint.globalStyles;
  const globalColors = colorsFromGlobal(g);
  const wrapperStyle: React.CSSProperties = {
    // Default to RTL for Arabic content unless overridden.
    direction: g?.direction ?? 'rtl',
    textAlign: 'right',
    fontFamily: g?.fontFamily ?? 'Noto Sans Arabic, sans-serif',
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden',
    ...globalToCss(g),
  };

  // 3. Render each block.
  return (
    <AbsoluteFill style={wrapperStyle}>
      {blueprint.composition.map((block) => (
        <RenderBlock
          key={block.id}
          block={block}
          globalColors={globalColors}
        />
      ))}
    </AbsoluteFill>
  );
};

// ─── Sample Blueprint (default for the "dynamic" composition) ────────
// A minimal but complete blueprint so `npx remotion still ... dynamic`
// renders something sensible out of the box, and serves as a live spec
// for Kimi's output format.

export const SAMPLE_BLUEPRINT: DesignBlueprint = {
  designPattern: 'modern-split',
  rationale: 'Default sample blueprint demonstrating the composition format.',
  composition: [
    {
      id: 'header',
      component: 'HeaderGradient',
      props: {
        kicker: 'RIYADH · FINE DINING',
        headline: 'تجربة طعام لا تُنسى',
        businessName: 'مطاعم الذواقة',
        align: 'right',
      },
    },
    {
      id: 'stats',
      component: 'ContentStats',
      props: {
        stats: [
          { number: '4.7', label: 'تقييم العملاء' },
          { number: '324', label: 'مراجعة' },
          { number: '10', label: 'سنوات خبرة' },
        ],
      },
    },
    {
      id: 'cta',
      component: 'CTAButton',
      props: {
        text: 'احجز طاولتك الآن',
      },
    },
    {
      id: 'footer',
      component: 'FooterComplete',
      props: {
        rating: 4.7,
        reviews: 324,
        trustBadge: 'شهادة صحية معتمدة',
        hashtags: ['#مطاعم_الرياض', '#فاين_داينينج', '#ذواقة'],
      },
    },
  ],
  globalStyles: {
    backgroundColor: '#1A1A2E',
    fontFamily: 'Noto Sans Arabic, sans-serif',
    primaryColor: '#E94560',
    accentColor: '#D4AF37',
    color: '#FFFFFF',
    direction: 'rtl',
  },
};
