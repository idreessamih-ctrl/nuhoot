# FOSS React Component Libraries — Research for Nuhoot Component Expansion

**Goal:** Expand the Nuhoot design-engine component library from 31 → 50+ reusable
design blocks by sourcing FOSS-licensed React/SVG components suitable for Arabic
social-media ad posts, stories, and reels.

**Render target:** Remotion (React 19). Components render server-side via Chromium —
**no `requestAnimationFrame`, no browser-only APIs, no CSS keyframe animations.**
Animation must be driven by `useCurrentFrame()` / `interpolate()` / `spring()`.
Existing components use **inline `style` objects**, a `ColorConfig` palette, and
`BaseBlockProps { colors?, style? }` (see `src/components/helpers.tsx`).

---

## Existing library (baseline — 31 components)

| Category | Count | Components |
|---|---|---|
| Headers | 4 | HeaderMinimal, HeaderGradient, HeaderSplit, HeaderOverlay |
| Photos | 5 | PhotoSingle, PhotoGrid, PhotoMosaic, PhotoCarousel, PhotoFrame |
| Content | 5 | ContentCards, ContentList, ContentStats, ContentQuotes, ContentFeatures |
| CTAs | 4 | CTAButton, CTABanner, CTAFloating, CTAInline |
| Decorative | 4 | DecorShapes, DecorRings, DecorWatermark, DecorGradient |
| Footers | 4 | FooterRating, FooterHashtags, FooterBranding, FooterComplete |
| Layouts | 4 | LayoutStandard, LayoutSplit, LayoutAsymmetric, LayoutMagazine |

Shared primitives in `helpers.tsx`: `hexRgba`, `toArabicDigits`, `optimalFontSize`,
`truncateCta`, `rtlProps`, `resolvePhoto`, `useColors`, `DEFAULT_COLORS`, `FONTS`,
`StarRating`.

---

## TIER 1 — Remotion-native templates (HIGHEST portability)

These already use `useCurrentFrame` / `interpolate` / `spring` / `useVideoConfig`,
inline styles, and no CSS keyframes — the **exact same idiom as Nuhoot**. They drop
straight into `src/components/` with only a wrapper to inject `ColorConfig` + RTL.

### 1.1 reactvideoeditor/remotion-templates  ⭐ TOP PICK
- **URL:** https://github.com/reactvideoeditor/remotion-templates
- **Stars:** 157
- **License:** ⚠️ **NONE** — no LICENSE file, no `package.json` license field.
  Under default copyright this is technically "all rights reserved" even though the
  README invites copying. **Recommended:** treat as *reference implementations* and
  reimplement the patterns in Nuhoot's own code, OR open an issue/PR asking the author
  to add MIT/Apache. Do NOT verbatim copy until a license is added.
- **What it offers:** 81 self-contained Remotion templates across 9 categories:
  - **Charts & Data (9):** bar/line/pie/donut/area charts, progress-bars, stat-counter, comparison-chart, circular-progress
  - **Text (9):** animated-text, bounce-text, bubble-pop-text, floating-bubble-text, glitch-text, popping-text, pulsing-text, slide-text, typewriter-subtitle
  - **Content Animation (9):** animated-list, card-flip, countdown-timer, notification-pop, particle-explosion, progress-steps, rotating-carousel, sound-wave, text-highlight
  - **Background (9):** bokeh-circles, geometric-patterns, gradient-shift, grid-pulse, liquid-wave, matrix-rain, noise-grain, pixel-transition, starfield
  - **Cinematic (9):** camera-shake, film-burn, ken-burns, letterbox-reveal, parallax-pan, spotlight-reveal, vignette-pulse, whip-pan, zoom-pulse
  - **Transition (9):** blinds, clock-wipe, cross-dissolve, fade-through-black, iris, morph, push, slide-wipe, zoom-through
  - **Logo & Branding (9):** logo blur/bounce/fade/glitch/scale-rotate/spin/split/stroke-draw/typewriter reveals
  - **Intro & Outro (9):** chapter-title, cinematic-title-intro, countdown-intro, credits-roll, **end-card** (subscribe CTA), lower-third, **quote-card**, subscribe-reminder, title-split
  - **Image & Media (9):** gallery-grid, image-carousel, image-comparison-slider, image-zoom-reveal, masonry-gallery, **photo-stack**, picture-in-picture, **polaroid-frame**, split-screen
- **Integration:** Reimplement the ~20 most relevant (charts, progress, backgrounds,
  polaroid-frame, photo-stack, quote-card, end-card, stat-counter, countdown-timer,
  notification-pop) as new files `src/components/charts.tsx`, `animations.tsx`,
  `frames.tsx`. Wrap each to read `ColorConfig` + apply `toArabicDigits()`/`rtlProps()`.
  **Highest ROI: ~20 new components with minimal adaptation.**

### 1.2 remotion-dev official templates
All under the `remotion-dev` org. License = NONE unless noted (Remotion itself is a
custom "Remotion Company" license for the framework, but the *template* repos are
example code — verify per-repo before verbatim copy).
| Repo | Stars | Use |
|---|---|---|
| `remotion-dev/template-tiktok` | 262 | TikTok-style captions (whisper.cpp) — caption overlays for reels |
| `remotion-dev/template-audiogram` | 262 | Podcast clip visuals — waveform + transcript |
| `remotion-dev/template-code-hike` | 213 | Code snippet animations |
| `remotion-dev/template-three` | 102 (MIT) | React-Three-Fiber 3D — 3D product showcases |
| `remotion-dev/template-still` | 47 | **Still-image rendering** — directly relevant to ad-post PNG export |
| `remotion-dev/template-overlay` | 15 | Stream overlays (lower-thirds, alerts) |
| `remotion-dev/template-prompt-to-video` | 117 | Prompt → storyboard → video pipeline (architectural reference) |
- **Integration:** `template-still` confirms the still-render path Nuhoot already uses.
  `template-overlay` lower-third/alert patterns map to Nuhoot footers & CTAs.
  `template-tiktok` caption timing logic is reusable for reel subtitles.

---

## TIER 2 — Copy-paste UI component libraries (need Tailwind→inline port)

These follow the shadcn "copy the source, own the code" philosophy. Source is MIT/
Apache. They use **Tailwind classes + `cn()` + CSS variables**, so they must be
ported to Nuhoot's inline-`style` + `ColorConfig` pattern — but the visual logic and
SVG are directly reusable. Porting effort is low-to-moderate per component.

### 2.1 magicuidesign/magicui  ⭐ STRONG PICK
- **URL:** https://github.com/magicuidesign/magicui
- **Stars:** 21,390
- **License:** MIT ✓ (confirmed `LICENSE.md`)
- **What it offers:** 77 animated components. Most relevant to Nuhoot:
  - **CTA buttons:** `shimmer-button`, `shiny-button`, `pulsating-button`, `rainbow-button`, `ripple-button`, `interactive-hover-button`
  - **Decorative backgrounds:** `grid-pattern`, `dot-pattern`, `hexagon-pattern`, `striped-pattern`, `retro-grid`, `flickering-grid`, `animated-grid-pattern`, `interactive-grid-pattern`, `noise-texture`, `warp-background`, `light-rays`, `meteors`, `particles`, `ripple`, `dot-pattern`
  - **Gradient/decorative text:** `animated-gradient-text`, `aurora-text`, `sparkles-text`, `shiny-text`, `animated-shiny-text`, `hyper-text`, `kinetic-text`, `text-animate`, `word-rotate`, `spinning-text`, `morphing-text`
  - **Cards/grids:** `bento-grid`, `magic-card`, `neon-gradient-card`, `border-beam`, `shine-border`, `backlight`
  - **Social proof:** `tweet-card`, `avatar-circles`, `client-tweet-card`, `number-ticker`, `marquee`
  - **Progress:** `animated-circular-progress-bar`, `scroll-progress` (adapt to frame-driven)
  - **Decorative:** `orbiting-circles`, `confetti`, `cool-mode`, `globe`, `icon-cloud`, `meteors`
- **Caveat:** Animation uses `motion/react` (Framer Motion) + `useInView`. In Remotion,
  replace `useInView`/`useSpring` with `useCurrentFrame()` + `interpolate()`.
- **Integration:** Create `src/components/buttons-pro.tsx` (6 CTA variants),
  `patterns.tsx` (8 background patterns), `social-proof.tsx` (tweet-card, avatars,
  marquee, number-ticker). Port ~20 components → **easily +15 new blocks.**

### 2.2 shadcn-ui/ui
- **URL:** https://github.com/shadcn-ui/ui
- **Stars:** 117,720
- **License:** MIT ✓
- **What it offers:** 227 registry items; the `apps/v4/registry/new-york-v4/` tree
  has `blocks/`, `charts/`, `ui/`, `examples/`. Block types include `dashboard-*`,
  `login-*`, `signup-*`, `sidebar-*` plus a `__components__.tsx` of primitives
  (badge, card, button, separator, etc.). The full marketing-block set (hero,
  pricing, testimonials, feature sections, CTAs) lives in the **shadcn blocks site**
  (`ui.shadcn.com/blocks`) — source is MIT.
- **Relevant primitives:** Badge, Card, Button, Separator, Avatar, Progress,
  Skeleton, Tooltip, Alert/Callout, Table.
- **Integration:** Port `Badge`, `Card`, `Progress`, `Avatar`, `Alert` primitives
  into `src/components/primitives.tsx`. These become low-level building blocks the
  DynamicComposer can compose. **+5 foundational primitives.**

### 2.3 tremorlabs/tremor (Tremor Raw)
- **URL:** https://github.com/tremorlabs/tremor
- **Stars:** 3,498
- **License:** Apache-2.0 ✓
- **What it offers:** 39 copy-paste React components incl. **Badge, Card, Button,
  Callout, ProgressBar, ProgressCircle, CategoryBar, BarList, Tracker, Tabs,
  TabNavigation, Divider, Toggle, Switch** + chart components (Area/Bar/Line/Donut/
  Pie/Spark/Combo).
- **Integration:** Port `Badge` → trust badges / status pills; `Callout` → promo
  banners; `ProgressBar`/`ProgressCircle` → sale countdowns & goal meters;
  `BarList` → ranked feature lists; `Tracker` → timeline/availability strips.
  Apache-2.0 requires NOTICE file attribution — add to `docs/ATTRIBUTIONS.md`.
  **+6 components (badges, callout, 2 progress, barlist, tracker).**

### 2.4 HeroUI (formerly NextUI)
- **URL:** https://github.com/heroui-inc/heroui
- **Stars:** 29,747
- **License:** Apache-2.0 ✓
- **Relevant:** Badge, Button, Card, Chip, Progress, Skeleton, Tooltip, Avatar,
  Divider, ScrollShadow. Polished marketing-ready defaults.
- **Integration:** Apache-2.0 (add NOTICE). Selectively port Chip (price tags),
  Badge variants, Progress ring. Useful as *visual reference* even if not imported.

---

## TIER 3 — SVG icon & illustration libraries (drop-in ASSETS)

These are pure SVG — no JS animation, no browser APIs. They work perfectly inside
Remotion and integrate as static decorative elements. **Lowest effort, highest safety.**

### 3.1 Icon sets (for badges, trust marks, feature glyphs)
| Library | URL | Stars | License | Icons |
|---|---|---|---|---|
| **lucide-icons/lucide** | github.com/lucide-icons/lucide | 23,208 | ISC ✓ | 1,500+ line icons; `lucide-react` npm pkg |
| **tabler/tabler-icons** | github.com/tabler/tabler-icons | 21,040 | MIT ✓ | 6,000+ icons incl. filled variants |
| **tailwindlabs/heroicons** | github.com/tailwindlabs/heroicons | 23,628 | MIT ✓ | 300+ outline/solid (React component form) |
| **feathericons/feather** | github.com/feathericons/feather | 25,952 | MIT ✓ | 280 classic line icons |
| **phosphor-icons/web** | github.com/phosphor-icons/web | 518 | MIT ✓ | 6 weights (thin→fill), 1,200+ icons |
| **react-icons/react-icons** | github.com/react-icons/react-icons | 12,603 | varied | aggregator: Font Awesome, Material, Boxicons, etc. — check each icon's license |
| **iconify/iconify** | github.com/iconify/iconify | 6,177 | MIT ✓ | universal framework, 200k+ icons on-demand |

- **Integration (recommended):** Add `lucide-react` (ISC) as a dependency — it's
  React-19 compatible, tree-shakeable, and the SVG `path` data can be embedded.
  Create `src/components/icon.tsx` — an `Icon` wrapper that renders any Lucide icon
  at a given size/color, RTL-aware. This single component unlocks **hundreds of
  glyph options** for badges, feature grids, trust marks, contact rows.
  Arabic-relevant icons: location pin, phone, clock, star, heart, check-circle,
  shield, truck, gift, tag, flame, crown.

### 3.2 Illustrations (decorative scenes & mascots)
| Library | URL | License | Notes |
|---|---|---|---|
| **themesberg/flowbite-illustrations** | github.com/themesberg/flowbite-illustrations | MIT ✓ | SVG illustration set built for Flowbite/Tailwind — recolorable |
| **storyset/storyset** | github.com/storyset/storyset | MIT ✓ | animated SVG illustrations, customizable colors |
| **unDraw** | undraw.co | ⚠️ "unDraw License" (free commercial, no attribution, but NOT OSI-approved) | 700+ flat illustrations; recolor to brand. Use only if "free commercial" is acceptable to legal; otherwise prefer Flowbite/Storyset |
| **googlefonts/noto-emoji** | github.com/googlefonts/noto-emoji | OFL-1.1 ✓ | full-color + monochrome emoji SVGs — great for expressive ad accents |
| **microsoft/fluentui-emoji** | github.com/microsoft/fluentui-emoji | MIT ✓ | modern 3D-style emoji, multiple skin tones |

- **Integration:** Bundle selected SVGs under `public/illustrations/` and reference
  via `resolvePhoto()`/`staticFile()`. Create `src/components/illustration.tsx`
  wrapper that injects `ColorConfig.accent` into SVG fills (string-replace).
  **+2 components (Illustration, Emoji).**

### 3.3 Flags & locale marks
| Library | URL | Stars | License |
|---|---|---|---|
| **Hatscripts/circle-flags** | github.com/Hatscripts/circle-flags | 1,530 | MIT ✓ | 400+ circular SVG country flags — Saudi flag for localization badges |
| **twitter/twemoji** | github.com/twitter/twemoji | 17,682 | MIT ✓ | emoji as SVG; CC-BY graphics — good for Arabic emoji rendering |

---

## TIER 4 — Pure-SVG npm packages (drop-in, server-safe)

Verified to have **no `requestAnimationFrame`/browser-only runtime deps**, so they
render correctly under Remotion's Chromium SSR.

### 4.1 react-nice-avatar
- **URL:** github.com/dabal-e/react-nice-avatar · npm: `react-nice-avatar`
- **License:** MIT ✓ · deps: `@babel/runtime`, `chroma-js`, `prop-types` (clean)
- **What:** Procedurally-generated cartoon avatars from a seed — perfect for
  testimonial cards & "customer" placeholders without storing real photos.
- **Integration:** Drop into `ContentQuotes`/testimonials. **+1 component
  (AvatarFace) feeding testimonial cards.**

### 4.2 react-social-icons
- **URL:** github.com/react-social-icons/react-social-icons · npm: `react-social-icons`
- **License:** MIT ✓ · deps: `@babel/runtime` only · React 19 compatible
- **What:** 30+ brand SVG icons (Instagram, WhatsApp, X, TikTok, Snapchat, etc.)
  with network-color defaults + mask/circle variants.
- **Integration:** Create `src/components/social-bar.tsx` — a row of platform
  icons for "follow us" footers & contact CTAs. **+1 component, high value for
  Saudi social marketing (WhatsApp/Instagram/Snapchat dominant).**

### 4.3 react-awesome-shapes
- **URL:** github.com/tejasag/react-awesome-shapes · npm: `react-awesome-shapes`
- **License:** MIT ✓
- **Caveat:** npm package is poorly packaged (bundles framer-motion/emotion/devDeps).
  **Recommended:** copy the SVG `<Shape>` source directly rather than installing.
- **What:** Blob, circle, hexagon, triangle, square decorative shapes with gradient
  fills & positioning props.
- **Integration:** Port the SVG into `src/components/decorative.tsx` as
  `DecorBlob`, `DecorHex`, `DecorTriangle` — extends the existing DecorShapes.
  **+3 decorative variants.**

### 4.4 Browser-ONLY packages (avoid direct install — port instead)
| Package | License | Issue | Fix |
|---|---|---|---|
| `react-countup` | MIT | uses `requestAnimationFrame` | reimplement with `interpolate(frame, [0,N], [0,target])` + `toArabicDigits` |
| `react-circular-progressbar` | MIT | CSS-based, RAF-driven | reimplement as SVG `<circle>` with `strokeDashoffset = interpolate(...)` |
| `@tremor/react` | Apache-2.0 | heavy, chart deps | use Tremor Raw (Tier 2.3) source copy instead |

---

## TIER 5 — Open-source Canva / banner-generator alternatives

Full design-tool platforms. Not drop-in components, but **architectural reference**
and extractable sub-systems (layer models, template schemas, export pipelines).

### 5.1 presenton/presenton
- **URL:** github.com/presenton/presenton · **Stars:** 8,608 · **License:** Apache-2.0 ✓
- **What:** Open-source AI presentation generator (Gamma/Canva alternative).
  Has a template/component model, AI-driven slide composition, and an API.
- **Relevance:** The AI→template→render pipeline mirrors Nuhoot's Kimi→JSON→
  DynamicComposer flow. Study its **template schema & theming system**.

### 5.2 clawnify/open-design
- **URL:** github.com/clawnify/open-design · **Stars:** 10 · **License:** MIT ✓
- **What:** Open-source Canva alternative — design editor for social-media
  graphics. Fabric.js + React. Layer/object model, text-on-canvas, export.
- **Relevance:** Its **object/layer schema** (text box, image, shape, gradient) is a
  reference for extending the DynamicComposer's JSON blueprint vocabulary.

### 5.3 tayfuntoprakcioglu/socialgen
- **URL:** github.com/tayfuntoprakcioglu/socialgen · **Stars:** 2 · **License:** MIT ✓
- **What:** Lightweight, privacy-focused, browser-only Canva alternative.

### 5.4 shields.io (badges/shields)
- **URL:** github.com/badges/shields · **Stars:** 26,883 · **License:** Apache-2.0 ✓
- **What:** Programmatic SVG badge generator (`badge.svg?label=...&message=...`).
- **Integration:** Don't embed the service; instead **copy the badge SVG template**
  into `src/components/badge.tsx` to render trust/quality badges ("★ 4.9",
  "موثوق", "100% أصلي") as crisp SVG. **+1 component.**

---

## TIER 6 — Animation libraries (adapt to Remotion frame model)

For advanced motion that Nuhoot's `useCurrentFrame` math can't easily express.

| Library | URL | Stars | License | Use in Remotion |
|---|---|---|---|---|
| **pmndrs/react-spring** | github.com/pmndrs/react-spring | 29,118 | MIT ✓ | physics springs; works but prefer Remotion's `spring()` |
| **juliangarnier/anime** | github.com/juliangarnier/anime | 70,557 | MIT ✓ | SVG path drawing, stagger; drive via frame→progress |
| **motion (Framer)** | github.com/framer/motion | — | MIT ✓ | used by Magic UI; replace `useInView` w/ frame checks |

- **Integration:** Prefer Remotion's native `spring({frame, fps, config})` and
  `interpolate()`. Use anime.js only for complex SVG `strokeDasharray` reveals
  (logo-draw, underline-grow) feeding a `frame` value.

---

## GAPS → SOLUTIONS MAP (targeting 50+ components)

Mapping the requested element types to concrete sources:

| Needed element | Source (best → alt) | New file | Est. components |
|---|---|---|---|
| Rating stars (enhanced) | existing StarRating + Lucide `Star` | (enhance) | 0 new |
| Badges / pills | Tremor `Badge` + shadcn Badge + shields.io SVG | `badges.tsx` | +3 (StatusBadge, RatingBadge, TrustBadge) |
| Price tags | shadcn Card + custom + Lucide `Tag` | `pricing.tsx` | +3 (PriceTag, PriceStrike, DiscountBadge) |
| Discount circles | RVE `circular-progress` + react-awesome-shapes | `decorative.tsx` | +2 (DiscountCircle, CountdownRing) |
| Promotional banners | Tremor `Callout` + Magic UI `marquee` + RVE `notification-pop` | `promos.tsx` | +3 (PromoBanner, MarqueeStrip, NotificationPop) |
| Gradient backgrounds | Magic UI `grid/dot/hex/striped-pattern`, RVE `gradient-shift`/`bokeh` | `patterns.tsx` | +4 (GridPattern, DotPattern, HexPattern, GradientShift) |
| Decorative shapes | react-awesome-shapes + Magic UI `meteors`/`orbiting-circles`/`particles` | `decorative.tsx` | +3 (DecorBlob, DecorMeteors, DecorOrbit) |
| CTA buttons (premium) | Magic UI shimmer/shiny/pulsating/rainbow/ripple | `buttons-pro.tsx` | +5 (CTAShimmer, CTAShiny, CTAPulse, CTARainbow, CTARipple) |
| Photo frames | RVE `polaroid-frame`/`photo-stack`/`picture-in-picture` | `frames.tsx` | +3 (FramePolaroid, FrameStack, FramePiP) |
| Progress bars | RVE `progress-bars`/`progress-steps` + Tremor `ProgressBar`/`ProgressCircle` | `progress.tsx` | +4 (BarProgress, RingProgress, StepProgress, GoalMeter) |
| Trust badges | shields.io SVG + react-social-icons + circle-flags | `trust.tsx` | +2 (TrustBadge, SocialBar) |
| Testimonial cards | Magic UI `tweet-card`/`avatar-circles` + react-nice-avatar + RVE `quote-card` | `testimonials.tsx` | +3 (TweetCard, ReviewCard, QuoteCard) |
| Feature grids | Magic UI `bento-grid` + shadcn blocks | `grids.tsx` | +2 (BentoGrid, FeatureGrid) |
| Hero sections | RVE `cinematic-title-intro`/`title-split` + Magic UI `hero-video-dialog` | `heroes.tsx` | +2 (HeroCinematic, HeroSplit) |
| Stat counters | RVE `stat-counter` + Magic UI `number-ticker` | `stats.tsx` | +2 (StatCounter, NumberTicker) |
| Countdown timers | RVE `countdown-timer`/`countdown-intro` | `timers.tsx` | +2 (CountdownTimer, CountdownRing) |
| Charts | RVE bar/line/donut/pie/area + Tremor charts | `charts.tsx` | +3 (BarChart, DonutChart, LineChart) |
| Icons (primitives) | lucide-react wrapper | `icon.tsx` | +1 (Icon) |
| Avatars/emoji | react-nice-avatar + noto-emoji + fluentui-emoji | `avatars.tsx` | +2 (AvatarFace, Emoji) |

**Conservative new-component count: ~49 new blocks** → combined with existing 31,
comfortably exceeds the 50+ target (the registry would hold 70–80 components).

---

## LICENSE COMPLIANCE SUMMARY

| License | Repos using it | Obligation |
|---|---|---|
| MIT | magicui, shadcn/ui, heroicons, feather, phosphor, react-nice-avatar, react-social-icons, react-awesome-shapes, storyset, flowbite-illustrations, open-design, socialgen, react-spring, anime, fluentui-emoji | retain copyright notice |
| ISC | lucide | retain copyright notice |
| Apache-2.0 | tremor, heroui, shields, presenton, reactvideoeditor(template-three) | retain NOTICE + state changes |
| OFL-1.1 | noto-emoji | retain copyright; font license |
| ⚠️ NONE | reactvideoeditor/remotion-templates, most remotion-dev/template-* | **reimplement, don't verbatim copy** |
| ⚠️ custom | unDraw (unDraw License) | free commercial, no attribution, but NOT OSI — legal review |

**Action:** Create `docs/ATTRIBUTIONS.md` listing every MIT/ISC/Apache source copied,
with copyright lines. For Apache-2.0 (Tremor, HeroUI, shields, presenton), also note
"State changes: adapted to inline-style/Remotion idiom."

---

## RECOMMENDED EXECUTION ORDER (by ROI)

1. **Icons primitive** — install `lucide-react` (ISC), create `icon.tsx`. Unlocks
   hundreds of glyphs for badges/features/trust. *(1 component, enables many.)*
2. **Magic UI port** — copy 15–20 components, swap `cn()`/Tailwind → inline styles +
   `ColorConfig`, swap Framer Motion → `useCurrentFrame`. Biggest visual win.
3. **Tremor port** — Badge, Callout, ProgressBar, ProgressCircle, BarList, Tracker
   (Apache, 6 components, all marketing-useful).
4. **RVE templates (reimplement)** — 10–15 Remotion-native patterns (charts, progress,
   polaroid, photo-stack, quote-card, stat-counter, countdown, bokeh, gradient-shift).
5. **Pure-SVG drops** — react-social-icons (SocialBar), react-nice-avatar (AvatarFace),
   shields.io badge template (TrustBadge), circle-flags (Saudi locale badge).
6. **Illustrations** — bundle Flowbite/Storyset SVGs into `public/illustrations/`,
   add `illustration.tsx` + `emoji.tsx` wrappers.

**Estimated effort:** ~3–5 days of porting to reach 50+ components with full
RTL/Arabic-digit/ColorConfig integration and license attributions.
