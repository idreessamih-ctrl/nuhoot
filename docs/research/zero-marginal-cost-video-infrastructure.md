# Architecting Zero-Marginal-Cost Programmatic Video Infrastructure for Autonomous AI Agents

## Summary
Analysis of 5 FOSS alternatives to commercial video APIs (Creatomate, Shotstack) for programmatic Reels/TikTok generation.

## Key Finding: "Video as Data"
LLMs excel at JSON manipulation → render engines should accept JSON payloads, not React code or CLI commands.

## 5 FOSS Alternatives Ranked by Nuhoot Fit

### 1. FFmux — BEST FIT
- REST API over FFmpeg (Express.js, Docker-ready)
- JSON timeline schema with CSS-like scaling (cover/contain/fill)
- Async: POST /render → {jobId} → poll /status/{jobId}
- SRT subtitles, Google Fonts, audio ducking
- Zero marginal cost on bare-metal VPS ($20-40/month)

### 2. VideoFlow — JSON-Native WebGL Compositor
- TypeScript toolkit, 42+ GLSL effects, 25 transitions
- One JSON → three renderers (server MP4, browser MP4, live DOM)
- Server renderer uses headless Chromium + FFmpeg
- Can export static frames (PNG)

### 3. Remotion — React-Based
- Parameterized rendering: human builds template, agent passes inputProps
- renderMediaOnLambda() for video, renderStillOnLambda() for images
- Open-source API wrappers: dumpus-app/remotion-api
- LobeHub skill provides OpenAPI schema for agents

### 4. Editly — Declarative Node.js NLE
- Atop FFmpeg, streaming editing (no intermediate files)
- JSON "edit spec" with clips, layers, transitions
- Simplest for basic video assembly

### 5. MoviePy-MCP + Shottower — Python/MCP
- vidmagik-mcp: MoviePy via MCP (70+ tools discoverable by agents)
- Shottower: Drop-in Shotstack replacement (identical JSON schema)
- Shottower supports webhook callbacks for async orchestration

## Cost Comparison
| Architecture | Cost Model | Per-Render Cost |
|---|---|---|
| Commercial APIs | Per-render | $0.05 - $0.50 |
| Remotion on Lambda | Serverless | $0.001 - $0.021 |
| Remotion on Cloud Run | Containerized serverless | ~$0.0005 |
| FFmux/VideoFlow on VPS | Fixed monthly | $0.00 |
| Satori on Cloudflare Workers | Edge free tier | $0.00 |

## Recommended Architecture for Nuhoot
```
GLM 5.2 caption → JSON payload
                    ├→ Playwright/Satori → PNG post (CURRENT)
                    ├→ FFmux /render → MP4 Reel (PHASE 2)
                    └→ TTS audio + background music → mixed into Reel
```
