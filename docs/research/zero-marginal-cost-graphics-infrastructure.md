# Architecting Zero-Marginal-Cost Visual Automation: Agentic Workflows for Dynamic Social Media Graphics

## Summary
Analysis of 5 FOSS and commercial rendering engines for autonomous static graphic generation, focusing on smart auto-layout and agent-friendly integration.

## Key Finding: Auto-Layout Solves Overlap
Absolute positioning (what Nuhoot currently uses) breaks when GLM generates longer text. Constraint-based layout (Flexbox/Yoga) automatically pushes elements down, preventing overlap.

## 5 Solutions Ranked by Nuhoot Fit

### 1. Satori + PixelServe + Jellypod MCP — BEST FIT
- HTML/CSS → SVG → PNG WITHOUT browser (Yoga Flexbox engine)
- 50-150ms per render (vs 2.5s with Playwright)
- Zero cost on Cloudflare Workers free tier
- PixelServe: FOSS Bun microservice, Redis cache, multi-core
- Jellypod MCP: Agent generates images from JSX via MCP tool calls
- Trade-off: No ::before/::after, no CSS Grid (replaceable with divs)

### 2. Orshot — Commercial Smart Stacking
- "Smart Stacking": text grows → CTA pushes down automatically
- Visual editor (Canva-like), Canva/Figma imports
- $39/mo for 1500 renders, overage $36/1k (no hard limits)
- Native MCP server
- Best commercial option for non-developers

### 3. Templated.io — Developer-First MCP
- Drag-and-drop editor with real-time preview
- AI Template Generator (natural language → template)
- $29/mo for 1000 renders
- Official MCP package (mcp-server-templated)

### 4. NCA Toolkit — FOSS Playwright (what Nuhoot currently does)
- Self-hosted Flask + Playwright + FFmpeg + MinIO
- Full CSS3 support (Grid, Flexbox, everything)
- Docker, $10-20/mo VPS, zero marginal cost
- Good baseline; Satori is the upgrade path

### 5. Butterfly Social — FOSS Headless DOM Capture
- Screenshots existing web components
- Perfect auto-layout (browser handles it)
- Docker, $5 VPS, aggressive caching
- Good if brand already has web components

## Auto-Layout: The Core Problem Solved
```
Current (absolute):     top:620px → breaks if headline is long
Satori (flexbox):       flex-column → text grows, CTA pushes down
Orshot (smart stack):   text expands → surrounding elements shift
```

## Infrastructure Comparison
| Type | Tools | Technology | Cost | RAM Needs |
|---|---|---|---|---|
| Edge Compute | Satori, Jellypod | WASM, React JSX | $0 (CF free) | Very low |
| Microservice | PixelServe | Bun, Libvips | $5-10/mo VPS | Low |
| Headless Browser | NCA, Butterfly | Playwright, Chromium | $10-20/mo VPS | High (2GB+) |

## Migration Path: Playwright → Satori
1. Replace `.stage::before` with regular `<div>` for grid pattern
2. Replace absolute `top:Xpx` with flex-column containers
3. Keep circles, badges, color plates as flex children
4. Keep Google Fonts (Satori supports font injection)
5. Deploy on Cloudflare Workers or $5 VPS with PixelServe
