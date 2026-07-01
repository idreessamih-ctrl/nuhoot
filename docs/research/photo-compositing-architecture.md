# AI-Powered Photo Compositing Architecture (FOSS)

**Goal:** Evolve Nuhoot from *one hardcoded photo per niche* (`photos/{niche}.jpg`,
21 images) to a dynamic pipeline: Kimi K2.7 selects → PIL/OpenCV composites →
SD inpaints humans → Real-ESRGAN/GFPGAN/rembg enhance — all before Remotion renders.

**Stack:** Python 3.12 · PIL · OpenCV · Real-ESRGAN · GFPGAN · rembg · SD WebUI API
(or ComfyUI) · SQLite · Kimi K2.7 (umans API) · Remotion (React/TS) · FFmpeg.
**Constraints:** FOSS only, no paid APIs, user is NOT a developer (single-command pipeline).

---

## 1 — Letting Kimi K2.7 Choose the Best Photos (Prompt Engineering)

**Problem:** Kimi is text-only — it cannot *see* photos, so it must choose from
a text-catalog of photo metadata (schema in §5).

### Step 1 — Build a photo catalog

Each photo in `/opt/nuhoot/remotion/public/photos/` gets a SQLite row with
`id`, `niche`, `caption`, `tags` (JSON array), `has_human`, `mood`, `colors`.

### Step 2 — Inject the catalog into Kimi's prompt

Add this block to `COMPONENT_CATALOG` in `pipeline_v3.py`:

```python
PHOTO_CATALOG = """
AVAILABLE PHOTOS for niche "{niche}" (pick by id):
- restaurants_01: kabsa platter, top-down, warm, no people, 1920x1080
- restaurants_02: restaurant interior, wide, no people, 2000x1333
- restaurants_03: chef plating, side angle, has human, 1600x1067
- restaurants_04: dessert table, close-up, no people, 2048x1365
RULES:
- PhotoSingle/PhotoArch → pick 1 id
- PhotoGrid/FrameStack    → pick 2-4 ids (vary angles: 1 wide + 1 close + 1 detail)
- PhotoMosaic             → pick exactly 3 ids (1 hero + 2 supporting)
- Prefer variety: do NOT pick 3 top-down shots for a grid
- If the ad mentions a person, prefer ids with has_human=true
"""
```

### Step 3 — Parse Kimi's photo choice from JSON

Kimi already outputs `src` or `photos[]` props. In the blueprint validator
(~line 315 of `pipeline_v3.py`), resolve ids → paths:

```python
PHOTO_DB = {}  # id -> metadata, loaded from SQLite (see §5)

def resolve_photo_id(photo_id, niche):
    """restaurants_03 -> photos/restaurants_03.jpg"""
    row = PHOTO_DB.get(photo_id)
    if not row or row["niche"] != niche:
        return f"photos/{niche}.jpg"  # fallback to existing hardcoded photo
    return row["path"]
```

### Step 4 — Re-prompt if Kimi picks a bad combo

If Kimi picks 3 photos with identical tags (e.g. all "top-down"), add feedback:
*"Your 3 photo picks are too similar (all top-down). Re-pick with at least one
wide-angle and one close-up."* Uses the same feedback loop at line 477 of `pipeline_v3.py`.

---

## 2 — Compositing 2-3 Photos into One Image (PIL/OpenCV)

**When:** Kimi picks `PhotoGrid`/`PhotoMosaic` but we want a single pre-composited
image (Remotion loads one `src` — simpler rendering).

```python
from PIL import Image, ImageDraw

def round_corners(im, radius):
    """Apply rounded-corner alpha mask."""
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, *im.size], radius, fill=255)
    im.putalpha(mask)
    return im
```

### Pattern A — Side-by-side strip (2 photos)

```python
def composite_strip(paths, gap=20, bg="#0F0F14"):
    imgs = [Image.open(p).convert("RGB") for p in paths]
    h = min(im.height for im in imgs)
    imgs = [im.resize((int(im.width * h / im.height), h)) for im in imgs]
    w = sum(im.width for im in imgs) + gap * (len(imgs) - 1)
    canvas = Image.new("RGB", (w, h), bg)
    x = 0
    for im in imgs:
        canvas.paste(im, (x, 0)); x += im.width + gap
    return canvas
```

### Pattern B — Collage with rounded corners (3 photos)

```python
def composite_collage(paths, out_w=1200, out_h=800):
    """1 large on left (60%), 2 stacked on right (40%)."""
    canvas = Image.new("RGB", (out_w, out_h), "#0F0F14")
    main = Image.open(paths[0]).convert("RGB").resize((int(out_w*0.58), out_h))
    top  = Image.open(paths[1]).convert("RGB").resize((int(out_w*0.38), out_h//2-10))
    bot  = Image.open(paths[2]).convert("RGB").resize((int(out_w*0.38), out_h//2-10))
    canvas.paste(round_corners(main, 20), (10, 0))
    canvas.paste(round_corners(top, 16),  (int(out_w*0.60), 0))
    canvas.paste(round_corners(bot, 16),  (int(out_w*0.60), out_h//2+10))
    return canvas
```

### Pattern C — Blend with gradient mask (hero + texture overlay)

```python
import numpy as np, cv2

def composite_blend(bg_path, overlay_path, out):
    bg = cv2.imread(bg_path)
    fg = cv2.resize(cv2.imread(overlay_path), (bg.shape[1], bg.shape[0]))
    mask = np.linspace(1.0, 0.0, bg.shape[1]).reshape(-1, 1, 1)  # left=fg
    cv2.imwrite(out, (fg * mask + bg * (1 - mask)).astype(np.uint8))
```

---

## 3 — Adding Humans to Existing Photos (Stable Diffusion Inpainting)

**Use case:** A restaurant interior photo has no people. We add a customer
seated at a table to make the ad feel alive.

### Option A — Stable Diffusion WebUI API (AUTOMATIC1111)

```python
import requests, base64
WEBUI_URL = "http://127.0.0.1:7860"

def inpaint_add_human(image_path, mask_path, prompt, out):
    """mask_path: white where to paint, black where to keep."""
    b64 = lambda p: base64.b64encode(open(p, "rb").read()).decode()
    resp = requests.post(f"{WEBUI_URL}/sdapi/v1/img2img", json={
        "init_images": [b64(image_path)], "mask": b64(mask_path), "prompt": prompt,
        "negative_prompt": "deformed, extra limbs, bad hands, watermark, text",
        "denoising_strength": 0.75, "inpainting_fill": 1, "inpaint_full_res": True,
        "steps": 30, "cfg_scale": 7.5, "width": 768, "height": 768,
        "sampler_name": "DPM++ 2M Karras"})
    open(out, "wb").write(base64.b64decode(resp.json()["images"][0]))
```
**Model:** Use DreamShaper or a community Saudi/Arab fine-tune. For culturally
appropriate dress add to prompt: *"Saudi man wearing thobe"* / *"Saudi woman wearing abaya"*.

### Generating the mask programmatically

```python
def make_human_mask(image_path, out, box):
    """box = (x1, y1, x2, y2) region to inpaint. White=paint."""
    import cv2, numpy as np
    img = cv2.imread(image_path)
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    x1, y1, x2, y2 = box
    mask[y1:y2, x1:x2] = 255
    cv2.imwrite(out, cv2.GaussianBlur(mask, (51, 51), 0))  # feather edges
```

### Option B — ComfyUI API (alternative, see §6)

ComfyUI exposes `/prompt` (JSON workflow graph) + WebSocket. Supports chaining
inpaint→upscale→face-enhance in one graph. **Start with WebUI API (simpler);
move to ComfyUI when you need batch/multi-step graphs.**

---

## 4 — Photo Enhancement Pipeline

Three FOSS tools. Chain: **remove bg → upscale → face enhance**
(or upscale → face-enhance if keeping background).

### 4a — Real-ESRGAN (upscaling)

`pip install realesrgan` — downloads `RealESRGAN_x4plus.pth` on first run.

```python
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet
import cv2

upsampler = RealESRGANer(scale=4,
    model_path="weights/RealESRGAN_x4plus.pth",
    model=RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64,
                  num_block=23, num_grow_ch=32, scale=4),
    half=True)  # fp16 — 2x faster, half VRAM

def upscale(image_path, out):
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    cv2.imwrite(out, upsampler.enhance(img, outscale=4)[0])
```
4x upscale of 1080p needs ~6 GB VRAM. Use `tile=400` if VRAM is tight.

### 4b — GFPGAN (face restoration/enhancement)

`pip install gfpgan`

```python
from gfpgan import GFPGANer
import cv2

restorer = GFPGANer(model_path="weights/GFPGANv1.4.pth", upscale=1,
                    arch="clean", channel_multiplier=2)

def enhance_faces(image_path, out):
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    cv2.imwrite(out, restorer.enhance(img, paste_back=True)[2])
```
**Tip:** Pass the `RealESRGANer` instance as `bg_upsampler` to `GFPGANer` —
does upscale + face-fix in one call.

### 4c — rembg (background removal)

`pip install rembg[gpu]` (or `rembg` for CPU)

```python
from rembg import remove
from PIL import Image
import io

def remove_bg(image_path, out):
    with open(image_path, "rb") as f:
        out_bytes = remove(f.read())               # PNG with alpha
    Image.open(io.BytesIO(out_bytes)).save(out)    # transparent PNG
```
**Use case:** Cut out a product/person, composite onto a branded gradient
background (PatternGrid / DecorGradient component).

### Combined enhancement function

```python
def enhance_photo(image_path, out, do_upscale=True, do_face=True, do_cutout=False):
    cur = image_path
    if do_cutout: remove_bg(cur, out); cur = out
    if do_upscale: upscale(cur, out); cur = out
    if do_face:    enhance_faces(cur, out)
```

---

## 5 — Local Photo Database (SQLite)

**Why SQLite over filesystem:** We need to query "all restaurant photos with
no humans, warm mood, wide-angle" — SQL beats `ls | grep`.

### Schema

```sql
CREATE TABLE photos (
    id TEXT PRIMARY KEY,          -- restaurants_03
    path TEXT NOT NULL,           -- photos/restaurants_03.jpg
    niche TEXT NOT NULL,          -- restaurants
    caption TEXT, tags TEXT,      -- "kabsa platter"; JSON ["food","top-down"]
    mood TEXT, has_human INTEGER DEFAULT 0,
    gender TEXT DEFAULT 'plural', width INTEGER, height INTEGER,
    dominant_colors TEXT,         -- JSON ["#8B4513","#D4A574"]
    source TEXT,                  -- openverse | ai_generated
    license TEXT,                 -- cc-by-sa | cc0 | generated
    used_count INTEGER DEFAULT 0, last_used TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE composites (
    id TEXT PRIMARY KEY, niche TEXT NOT NULL, path TEXT NOT NULL,
    source_ids TEXT NOT NULL,    -- JSON ["restaurants_01","restaurants_03"]
    technique TEXT, ad_id TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX idx_photos_niche ON photos(niche);
CREATE INDEX idx_photos_niche_human ON photos(niche, has_human);
```

### Python helper

```python
import sqlite3

conn = sqlite3.connect("/opt/nuhoot/photos/photos.db")
conn.row_factory = sqlite3.Row

def photos_for_niche(niche, has_human=None, limit=10):
    q, p = "SELECT * FROM photos WHERE niche = ?", [niche]
    if has_human is not None: q += " AND has_human = ?"; p.append(int(has_human))
    q += " ORDER BY used_count ASC, RANDOM() LIMIT ?"  # least-used first
    p.append(limit)
    return [dict(r) for r in conn.execute(q, p).fetchall()]

def mark_used(photo_id):
    conn.execute("UPDATE photos SET used_count = used_count + 1, "
                 "last_used = datetime('now') WHERE id = ?", [photo_id])
    conn.commit()
```

### Auto-tagging existing photos

For the 21 current photos with no metadata, extract basic features with OpenCV:

```python
def auto_tag(image_path):
    img = cv2.imread(image_path)
    rgb = img.mean(axis=(0, 1))[::-1]  # BGR→RGB
    aspect = img.shape[1] / img.shape[0]
    return {
        "dominant_colors": [f"#{int(rgb[0]):02X}{int(rgb[1]):02X}{int(rgb[2]):02X}"],
        "mood": "bright" if img.mean() > 128 else "dark",
        "tags": ["wide-angle"] if aspect > 1.5 else (["portrait"] if aspect < 0.8 else ["standard"]),
    }
```

---

## 6 — ComfyUI vs Stable Diffusion WebUI API

| Capability | SD WebUI (A1111) | ComfyUI |
|---|---|---|
| Inpainting via API | ✅ `/sdapi/v1/img2img` | ✅ `/prompt` + workflow JSON |
| Batch processing | ⚠️ Loop in Python | ✅ Native queue |
| Chain inpaint→upscale→face | ⚠️ Multiple API calls | ✅ One workflow graph |
| ControlNet (pose guidance) | ✅ | ✅ |
| FOSS license | ✅ AGPL-3.0 | ✅ GPL-3.0 |

**Recommendation for Nuhoot:**

- **Phase 1 (now):** SD WebUI API on `localhost:7860` for inpainting only.
  Simple REST calls, well-documented.
- **Phase 2 (scale):** ComfyUI for a single workflow graph (inpaint →
  Real-ESRGAN → GFPGAN in one API call). Saves disk I/O.
- **Phase 3 (optional):** OpenPose ControlNet to force inpainted humans into
  specific poses (seated, holding product). Both tools support it.

---

## 7 — End-to-End Data Flow

```
1. KIMI SELECTS
   Kimi prompt includes PHOTO_CATALOG → returns JSON with photo ids
   "src":"restaurants_03" or "photos":["r_01","r_02","r_04"]
                        ↓
2. RESOLVE & DOWNLOAD
   resolve_photo_id() → SQLite lookup → file path
   If Openverse URL → download to remotion/public/photos/{niche}_{id}.jpg
                        ↓
3. COMPOSITE (if multi-photo component)
   PhotoGrid/Mosaic/FrameStack → composite_strip/collage/blend()
   → save as photos/{niche}_composite_{ad_id}.jpg, replace "photos" with single "src"
                        ↓
4. INPAINT (optional — if adding humans)
   make_human_mask() → SD WebUI inpaint_add_human()
   prompt: "Saudi {gender} in {niche} setting"
                        ↓
5. ENHANCE
   enhance_photo(): Real-ESRGAN 4x → GFPGAN face fix → overwrite file
                        ↓
6. RENDER (existing pipeline)
   blueprint → Remotion → PNG/MP4 → OpenCV measures → Kimi feedback loop (existing in v3)
```

### Wiring into `pipeline_v3.py`

Insert between Kimi JSON parse (~line 315) and Remotion render:

```python
# ─── Photo Compositing Stage (NEW) ─────────────────────────────
for block in blueprint["composition"]:
    if block["component"] in ("PhotoGrid", "PhotoMosaic", "FrameStack"):
        ids = block["props"].get("photos", [])
        paths = [resolve_photo_id(pid, niche) for pid in ids]
        if len(paths) >= 2:
            comp = f"photos/{niche}_composite_{ad_id}.jpg"
            composite_collage(paths).save(f"/opt/nuhoot/remotion/public/{comp}", quality=92)
            block["component"] = "PhotoSingle"          # collapse to single
            block["props"] = {"src": comp, "showOverlay": True}
            for pid in ids: mark_used(pid)               # track reuse in SQLite
    elif block["component"] in ("PhotoSingle", "PhotoArch", "PhotoCircle"):
        src = block["props"].get("src", "")
        if not src.startswith("photos/"):                # Kimi used an id
            block["props"]["src"] = resolve_photo_id(src, niche)
            mark_used(src)

# ─── Enhancement Stage (NEW) ──────────────────────────────────
final = f"/opt/nuhoot/remotion/public/photos/{niche}_composite_{ad_id}.jpg"
if os.path.exists(final):
    enhance_photo(final, final, do_upscale=True, do_face=True)
```

---

## Quick-Start Checklist

1. `pip install pillow opencv-python realesrgan gfpgan rembg httpx`
2. Download weights: `RealESRGAN_x4plus.pth` + `GFPGANv1.4.pth` → `/opt/nuhoot/photos/weights/`
3. Init SQLite DB (`/opt/nuhoot/photos/photos.db`) with the schema above; populate by looping `photos/*.jpg` through `auto_tag()`
4. Install SD WebUI: `git clone` AUTOMATIC1111 repo → `./webui.sh --api-only`
5. Add `PHOTO_CATALOG` block to Kimi's prompt in `pipeline_v3.py`; insert the compositing + enhancement stage before Remotion render
6. Test: `python pipeline_v3.py --niche restaurants --iterations 1`

## File Layout

```
/opt/nuhoot/
├── photos/{photos.db, weights/*.pth}      ← SQLite catalog + model weights
├── remotion/public/photos/
│   ├── {niche}.jpg                        ← existing fallback (21 images)
│   └── {niche}_composite_{ad_id}.jpg      ← composited output
├── eagle-eye/
│   ├── pipeline_v3.py                     ← modified (photo catalog + composite stage)
│   └── photo_pipeline.py                  ← NEW: composite/inpaint/enhance functions
└── docs/research/photo-compositing-architecture.md
```

---

*Document version: 1.0 · Targets Nuhoot pipeline v3 · All tools FOSS.*
