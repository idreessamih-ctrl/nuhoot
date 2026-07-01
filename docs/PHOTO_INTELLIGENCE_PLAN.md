# Nuhoot Photo Intelligence System — Implementation Plan

## Overview

Evolves Nuhoot from **one hardcoded photo per niche** (21 images) into an AI-powered photo intelligence system: Kimi K2.7 selects the best photo(s) from a SQLite catalog, PIL composites multi-photo layouts into single images, and Real-ESRGAN + GFPGAN + rembg enhance photos before Remotion renders. All tools are FOSS; the user runs `python pipeline_v3.py` as before — no new commands.

---

## Phase 1 — Photo Database
**Create:** `/opt/nuhoot/eagle-eye/photo_db.py` · **Deps:** `pip install httpx opencv-python pillow numpy`

```python
#!/usr/bin/env python3
"""Nuhoot Photo Database — SQLite catalog + Openverse population + auto-tagging."""
import json, os, sqlite3, time
import cv2, numpy as np, httpx

DB_PATH = "/opt/nuhoot/photos/photos.db"
PHOTOS_DIR = "/opt/nuhoot/remotion/public/photos"

NICHES = ["restaurants","cafes","bakeries","salons","spas","barbershops","gyms",
    "clinics","dentists","pharmacies","dermatology","fashion","perfumes","law_firms",
    "real_estate","auto_shops","car_wash","cleaning","hvac_ac","event_halls",
    "training_centers"]

OPENVERSE_QUERIES = {
    "restaurants":"Saudi restaurant food kabsa","cafes":"Saudi Arabia coffee shop",
    "bakeries":"Arabic bakery bread dessert","salons":"beauty salon interior modern",
    "spas":"luxury spa wellness interior","barbershops":"barbershop interior modern",
    "gyms":"gym fitness equipment interior","clinics":"modern medical clinic interior",
    "dentists":"dental clinic modern","pharmacies":"pharmacy shelves medicine",
    "dermatology":"skincare clinic treatment","fashion":"Saudi fashion abaya boutique",
    "perfumes":"luxury perfume bottle oud","law_firms":"law office professional interior",
    "real_estate":"Saudi Riyadh modern villa","auto_shops":"auto mechanic garage workshop",
    "car_wash":"car wash detailing shine","cleaning":"clean service professional home",
    "hvac_ac":"air conditioner installation technician","event_halls":"Saudi wedding hall decoration",
    "training_centers":"classroom training education modern",
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS photos (
    id TEXT PRIMARY KEY, path TEXT NOT NULL, niche TEXT NOT NULL, caption TEXT,
    tags TEXT, mood TEXT, has_human INTEGER DEFAULT 0, gender TEXT DEFAULT 'plural',
    width INTEGER, height INTEGER, dominant_colors TEXT, source TEXT, license TEXT,
    used_count INTEGER DEFAULT 0, last_used TEXT,
    created_at TEXT DEFAULT (datetime('now')));
CREATE TABLE IF NOT EXISTS composites (
    id TEXT PRIMARY KEY, niche TEXT NOT NULL, path TEXT NOT NULL, source_ids TEXT NOT NULL,
    technique TEXT, ad_id TEXT, created_at TEXT DEFAULT (datetime('now')));
CREATE INDEX IF NOT EXISTS idx_photos_niche ON photos(niche);
CREATE INDEX IF NOT EXISTS idx_photos_niche_human ON photos(niche, has_human);
"""

def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn

def auto_tag(image_path):
    """Extract visual features from a photo using OpenCV."""
    img = cv2.imread(image_path)
    if img is None: return None
    h, w = img.shape[:2]
    mean_rgb = img.mean(axis=(0,1))[::-1]  # BGR→RGB
    brightness = float(img.mean())
    aspect = w / h
    shot = "wide-angle" if aspect > 1.5 else ("portrait" if aspect < 0.8 else "standard")
    r, g, b = mean_rgb
    mood = "warm" if r > g > b else ("cool" if b > r else "neutral")
    # Human detection heuristic: skin-tone pixel ratio
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    skin = cv2.inRange(hsv, np.array([0,30,60]), np.array([25,170,255]))
    has_human = 1 if skin.sum() / (h*w*255) > 0.03 else 0
    return {"width":w,"height":h,"mood":"bright" if brightness>128 else "dark",
        "has_human":has_human,"tags":json.dumps([shot,mood]),
        "dominant_colors":json.dumps([f"#{int(mean_rgb[0]):02X}{int(mean_rgb[1]):02X}{int(mean_rgb[2]):02X}"])}

def tag_existing_photos():
    conn = get_db(); tagged = 0
    for niche in NICHES:
        fp = os.path.join(PHOTOS_DIR, f"{niche}.jpg")
        if not os.path.exists(fp): continue
        pid = f"{niche}_00"; tags = auto_tag(fp)
        if not tags: continue
        conn.execute("INSERT OR REPLACE INTO photos (id,path,niche,caption,tags,mood,"
            "has_human,width,height,dominant_colors,source,license) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (pid,f"photos/{niche}.jpg",niche,f"{niche} default photo",tags["tags"],
             tags["mood"],tags["has_human"],tags["width"],tags["height"],tags["dominant_colors"],
             "local","owned"))
        tagged += 1
    conn.commit(); conn.close()
    print(f"✓ Tagged {tagged} existing photos → {DB_PATH}")

def search_openverse(query, page_size=20):
    try:
        resp = httpx.get("https://api.openverse.org/v1/images/",
            params={"q":query,"license_type":"commercial","page_size":page_size}, timeout=30)
        resp.raise_for_status(); return resp.json().get("results",[])
    except Exception as e:
        print(f"  ⚠️ Openverse error for '{query}': {e}"); return []

def populate_from_openverse(max_per_niche=5):
    """Download up to N photos per niche from Openverse (no API key, 20 req/min)."""
    conn = get_db(); total = 0
    for niche in NICHES:
        query = OPENVERSE_QUERIES.get(niche, niche.replace("_"," "))
        results = search_openverse(query, page_size=max_per_niche+5); added = 0
        for r in results:
            if added >= max_per_niche: break
            url = r.get("url","")
            if not url.startswith("http"): continue
            pid = f"{niche}_{added+1:02d}"
            if conn.execute("SELECT id FROM photos WHERE id=?",(pid,)).fetchone(): continue
            fname = f"{niche}_{added+1:02d}.jpg"
            fp = os.path.join(PHOTOS_DIR, fname)
            try:
                data = httpx.get(url, timeout=60, follow_redirects=True).content
                with open(fp,"wb") as f: f.write(data)
            except Exception as e:
                print(f"  ⚠️ Download failed: {e}"); continue
            tags = auto_tag(fp)
            if not tags: continue
            conn.execute("INSERT OR REPLACE INTO photos (id,path,niche,caption,tags,mood,"
                "has_human,width,height,dominant_colors,source,license) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (pid,f"photos/{fname}",niche,r.get("title",""),tags["tags"],tags["mood"],
                 tags["has_human"],tags["width"],tags["height"],tags["dominant_colors"],
                 "openverse",r.get("license","cc-by")))
            added += 1; total += 1; time.sleep(3.5)  # rate limit
        conn.commit(); print(f"  {niche}: +{added} from Openverse")
    conn.close(); print(f"✓ Populated {total} photos from Openverse")

def photos_for_niche(niche, has_human=None, limit=10):
    conn = get_db(); q,p = "SELECT * FROM photos WHERE niche = ?",[niche]
    if has_human is not None: q += " AND has_human = ?"; p.append(int(has_human))
    q += " ORDER BY used_count ASC, RANDOM() LIMIT ?"; p.append(limit)
    rows = [dict(r) for r in conn.execute(q,p).fetchall()]; conn.close(); return rows

def get_photo_catalog_text(niche, limit=10):
    """Build PHOTO_CATALOG block for Kimi's prompt."""
    photos = photos_for_niche(niche, limit=limit)
    if not photos:
        return f'\nAVAILABLE PHOTOS for niche "{niche}": (none — use photos/{niche}.jpg)\n'
    lines = [f'\nAVAILABLE PHOTOS for niche "{niche}" (pick by id):']
    for ph in photos:
        tags = json.loads(ph.get("tags","[]"))
        human = "has human" if ph.get("has_human") else "no people"
        dims = f"{ph.get('width','?')}x{ph.get('height','?')}"
        lines.append(f'- {ph["id"]}: {ph.get("caption","photo")}, {", ".join(tags)}, {human}, {dims}')
    lines += ["RULES:","- PhotoSingle/PhotoArch/PhotoCircle → pick 1 id",
        "- PhotoGrid/PhotoMosaic/FrameStack → pick 2-3 ids (vary angles)",
        '- If ad mentions a person, prefer ids with "has human"',
        '- Use the id as the "src" value (e.g. "src": "restaurants_01")']
    return "\n".join(lines)+"\n"

def resolve_photo_id(photo_id, niche):
    """restaurants_03 → photos/restaurants_03.jpg (fallback to default)."""
    conn = get_db()
    row = conn.execute("SELECT path FROM photos WHERE id=? AND niche=?",(photo_id,niche)).fetchone()
    conn.close()
    if row: return row["path"]
    if photo_id.startswith("photos/") or photo_id.startswith("/"): return photo_id
    return f"photos/{niche}.jpg"

def mark_used(photo_id):
    conn = get_db()
    conn.execute("UPDATE photos SET used_count=used_count+1, last_used=datetime('now') WHERE id=?",(photo_id,))
    conn.commit(); conn.close()

def record_composite(cid, niche, path, source_ids, technique, ad_id):
    conn = get_db()
    conn.execute("INSERT OR REPLACE INTO composites (id,niche,path,source_ids,technique,ad_id) VALUES (?,?,?,?,?,?)",
        (cid,niche,path,json.dumps(source_ids),technique,ad_id))
    conn.commit(); conn.close()

if __name__ == "__main__":
    import sys; cmd = sys.argv[1] if len(sys.argv)>1 else "init"
    if cmd == "init": tag_existing_photos()
    elif cmd == "openverse": populate_from_openverse(int(sys.argv[2]) if len(sys.argv)>2 else 5)
    elif cmd == "stats":
        conn = get_db()
        for n in NICHES:
            print(f"  {n:20s}: {conn.execute('SELECT COUNT(*) FROM photos WHERE niche=?',(n,)).fetchone()[0]} photos")
        conn.close()
    else: print("Usage: python photo_db.py [init|openverse N|stats]")
```

**Verify:** `python photo_db.py init` → "✓ Tagged 21 existing photos"; `python photo_db.py openverse 5` → ~105 photos added.

---

## Phase 2 — Kimi Photo Selection (modify `pipeline_v3.py`)

**Deps:** Phase 1 `photo_db.py`.

### Patch 1 — Add import (line 15-19)

**Old:**
```python
import json, time, base64, re, os, sys, subprocess, shutil
import requests
import cv2
import numpy as np
from PIL import Image, ImageDraw
```
**New:**
```python
import json, time, base64, re, os, sys, subprocess, shutil
import requests
import cv2
import numpy as np
from PIL import Image, ImageDraw
from photo_db import (
    get_photo_catalog_text, resolve_photo_id, mark_used, record_composite,
)
```

### Patch 2 — Inject PHOTO_CATALOG into Kimi prompt (line 417-418)

**Old:**
```python
- Photo: {photo_path}
- Target audience: {gender} — use "{gender_word}" for addressing
```
**New:**
```python
- Photo: {photo_path}
- Target audience: {gender} — use "{gender_word}" for addressing

{get_photo_catalog_text(niche)}
```

### Patch 3 — Update photo assignment instruction (line 425)

**Old:**
```python
- PHOTO: Use {assigned_photo} component with src="photos/{niche}.jpg"
```
**New:**
```python
- PHOTO: Use {assigned_photo} component with src set to a photo id from the AVAILABLE PHOTOS list above (e.g. "src": "restaurants_01"). For PhotoGrid/Mosaic/FrameStack, set "photos" to an array of 2-3 ids.
```

### Patch 4 — Update src rule (line 451)

**Old:**
```python
7. For photos use "src" prop (NOT photoPath): "src": "photos/{niche}.jpg"
```
**New:**
```python
7. For photos use "src" prop with a photo ID from the AVAILABLE PHOTOS list (e.g. "src": "restaurants_01"). Do NOT use "photos/{niche}.jpg" directly — always pick an id.
```

### Patch 5 — Add photo ID resolution to normalize_blueprint (line 336-339)

**Old:**
```python
        # FooterComplete: remove businessName (not a valid prop)
        if comp == "FooterComplete":
            props.pop("businessName", None)
        # Remove "colors" from props — system injects from globalStyles
```
**New:**
```python
        # Resolve photo IDs → file paths
        niche = blueprint.get("_niche", "")
        if comp in SRC_PHOTOS:
            src_val = props.get("src", "")
            if src_val and not src_val.startswith("photos/") and not src_val.startswith("/"):
                resolved = resolve_photo_id(src_val, niche)
                props["src"] = resolved
                mark_used(src_val)
        if comp in ARRAY_PHOTOS:
            photo_list = props.get("photos", [])
            resolved_list = []
            for pid in photo_list:
                if pid and not pid.startswith("photos/") and not pid.startswith("/"):
                    resolved = resolve_photo_id(pid, niche)
                    resolved_list.append(resolved)
                    mark_used(pid)
                else:
                    resolved_list.append(pid)
            props["photos"] = resolved_list
        # FooterComplete: remove businessName (not a valid prop)
        if comp == "FooterComplete":
            props.pop("businessName", None)
        # Remove "colors" from props — system injects from globalStyles
```

### Patch 6 — Pass niche into blueprint (line 625-627)

**Old:**
```python
            comp_count = len(blueprint.get("composition", []))
            pattern = blueprint.get("designPattern", "unknown")
            print(f"  ✓ Pattern: {pattern}, Components: {comp_count}")
```
**New:**
```python
            blueprint["_niche"] = niche  # for photo ID resolution
            comp_count = len(blueprint.get("composition", []))
            pattern = blueprint.get("designPattern", "unknown")
            print(f"  ✓ Pattern: {pattern}, Components: {comp_count}")
```

**Verify:** `python -c "from photo_db import get_photo_catalog_text; print(get_photo_catalog_text('restaurants'))"` shows photo IDs with tags.

---

## Phase 3 — Photo Compositing

**Create:** `/opt/nuhoot/eagle-eye/photo_compositor.py`
**Deps:** `pip install pillow opencv-python numpy`

```python
#!/usr/bin/env python3
"""Nuhoot Photo Compositor — Merge 2-3 photos into single composites."""
import os, cv2, numpy as np
from PIL import Image, ImageDraw

PHOTOS_DIR = "/opt/nuhoot/remotion/public/photos"

def _resolve_path(ref):
    if ref.startswith("/"): return ref
    if ref.startswith("photos/"): return os.path.join("/opt/nuhoot/remotion/public", ref)
    return os.path.join(PHOTOS_DIR, ref)

def round_corners(im, radius):
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0,0,im.size[0],im.size[1]], radius=radius, fill=255)
    im.putalpha(mask); return im

def composite_strip(paths, gap=20, bg="#0F0F14"):
    """Pattern A: Side-by-side horizontal strip (2 photos)."""
    imgs = [Image.open(_resolve_path(p)).convert("RGB") for p in paths]
    h = min(im.height for im in imgs)
    imgs = [im.resize((int(im.width*h/im.height), h), Image.LANCZOS) for im in imgs]
    w = sum(im.width for im in imgs) + gap*(len(imgs)-1)
    canvas = Image.new("RGB", (w, h), bg); x = 0
    for im in imgs:
        canvas.paste(im, (x, 0)); x += im.width + gap
    return canvas

def composite_collage(paths, out_w=1200, out_h=800, bg="#0F0F14"):
    """Pattern B: 1 large left (58%) + 2 stacked right (38%). Needs 3 paths."""
    canvas = Image.new("RGB", (out_w, out_h), bg)
    main = Image.open(_resolve_path(paths[0])).convert("RGB").resize((int(out_w*0.58), out_h), Image.LANCZOS)
    sw, sh = int(out_w*0.38), (out_h-20)//2
    top = Image.open(_resolve_path(paths[1])).convert("RGB").resize((sw, sh), Image.LANCZOS)
    bot = Image.open(_resolve_path(paths[2])).convert("RGB").resize((sw, sh), Image.LANCZOS)
    canvas.paste(round_corners(main, 20), (10, 0))
    canvas.paste(round_corners(top, 16), (int(out_w*0.60), 0))
    canvas.paste(round_corners(bot, 16), (int(out_w*0.60), sh+20))
    return canvas

def composite_blend(bg_path, overlay_path, out_w=1200, out_h=800):
    """Pattern C: Gradient blend — overlay fades left→right into background."""
    bg = cv2.resize(cv2.imread(_resolve_path(bg_path)), (out_w, out_h))
    fg = cv2.resize(cv2.imread(_resolve_path(overlay_path)), (out_w, out_h))
    mask = np.linspace(1.0, 0.0, out_w).reshape(1, -1, 1)
    mask = np.broadcast_to(mask, (out_h, out_w, 3)).astype(np.float32)
    blended = (fg*mask + bg*(1-mask)).astype(np.uint8)
    return Image.fromarray(cv2.cvtColor(blended, cv2.COLOR_BGR2RGB))

def composite_photos(paths, niche, ad_id, technique="auto"):
    """Main entry: pick compositing pattern by photo count. Returns 'photos/xxx.jpg'."""
    if len(paths) < 2: return paths[0] if paths else None
    if technique == "auto":
        technique = "strip" if len(paths) == 2 else "collage"
    if technique == "strip": result = composite_strip(paths)
    elif technique == "collage": result = composite_collage(paths)
    elif technique == "blend": result = composite_blend(paths[0], paths[1])
    else: result = composite_strip(paths)
    fname = f"{niche}_composite_{ad_id}.jpg"
    result.save(os.path.join(PHOTOS_DIR, fname), quality=92)
    print(f"    📸 Composite saved: photos/{fname} ({len(paths)} photos, {technique})")
    return f"photos/{fname}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3: print("Usage: python photo_compositor.py niche photo1 photo2 [photo3]"); sys.exit(1)
    print(composite_photos(sys.argv[2:], sys.argv[1], "test"))
```

**Verify:** `python photo_compositor.py restaurants photos/restaurants.jpg photos/cafes.jpg` → creates `restaurants_composite_test.jpg`.

---

## Phase 4 — Photo Enhancement

**Create:** `/opt/nuhoot/eagle-eye/photo_enhancer.py`
**Deps:** `pip install realesrgan gfpgan rembg basicsr torch torchvision`
**Weights:**
```bash
mkdir -p /opt/nuhoot/photos/weights
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -O /opt/nuhoot/photos/weights/RealESRGAN_x4plus.pth
wget https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth -O /opt/nuhoot/photos/weights/GFPGANv1.4.pth
```

```python
#!/usr/bin/env python3
"""Nuhoot Photo Enhancer — Real-ESRGAN + GFPGAN + rembg. Falls back gracefully."""
import os, cv2, io
from PIL import Image

WEIGHTS_DIR = "/opt/nuhoot/photos/weights"
_upsampler = None; _restorer = None

def _get_upsampler():
    global _upsampler
    if _upsampler is not None: return _upsampler
    try:
        from realesrgan import RealESRGANer
        from basicsr.archs.rrdbnet_arch import RRDBNet
        mp = os.path.join(WEIGHTS_DIR, "RealESRGAN_x4plus.pth")
        if not os.path.exists(mp): print("  ⚠️ Real-ESRGAN weights not found"); return None
        _upsampler = RealESRGANer(scale=4, model_path=mp, half=True, tile=400,
            model=RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4))
        return _upsampler
    except ImportError: print("  ⚠️ realesrgan not installed"); return None
    except Exception as e: print(f"  ⚠️ Real-ESRGAN init failed: {e}"); return None

def _get_restorer():
    global _restorer
    if _restorer is not None: return _restorer
    try:
        from gfpgan import GFPGANer
        mp = os.path.join(WEIGHTS_DIR, "GFPGANv1.4.pth")
        if not os.path.exists(mp): print("  ⚠️ GFPGAN weights not found"); return None
        _restorer = GFPGANer(model_path=mp, upscale=1, arch="clean",
            channel_multiplier=2, bg_upsampler=_get_upsampler())
        return _restorer
    except ImportError: print("  ⚠️ gfpgan not installed"); return None
    except Exception as e: print(f"  ⚠️ GFPGAN init failed: {e}"); return None

def remove_bg(image_path, out_path):
    try:
        from rembg import remove
        with open(image_path, "rb") as f: inp = f.read()
        Image.open(io.BytesIO(remove(inp))).save(out_path)
        print(f"    ✂️  Background removed: {out_path}"); return out_path
    except ImportError: print("  ⚠️ rembg not installed"); return image_path
    except Exception as e: print(f"  ⚠️ rembg failed: {e}"); return image_path

def upscale_image(image_path, out_path):
    up = _get_upsampler()
    if up is None: return image_path
    try:
        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        output, _ = up.enhance(img, outscale=4)
        cv2.imwrite(out_path, output)
        print(f"    🔼 Upscaled 4x: {out_path}"); return out_path
    except Exception as e: print(f"  ⚠️ Upscale failed: {e}"); return image_path

def enhance_faces(image_path, out_path):
    r = _get_restorer()
    if r is None: return image_path
    try:
        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        _, _, output = r.enhance(img, paste_back=True)
        cv2.imwrite(out_path, output)
        print(f"    😊 Faces enhanced: {out_path}"); return out_path
    except Exception as e: print(f"  ⚠️ Face enhance failed: {e}"); return image_path

def enhance_photo(image_path, out_path=None, do_upscale=True, do_face=True, do_cutout=False):
    """Chain: bg removal → upscale → face enhance. Falls back gracefully."""
    if not image_path.startswith("/"):
        image_path = os.path.join("/opt/nuhoot/remotion/public", image_path)
    if out_path is None: out_path = image_path
    cur = image_path; tmp = out_path + ".tmp.png"
    try:
        if do_cutout: cur = remove_bg(cur, tmp)
        if do_upscale: cur = upscale_image(cur, tmp)
        if do_face: cur = enhance_faces(cur, tmp)
        if cur == tmp and os.path.exists(tmp): os.replace(tmp, out_path); cur = out_path
        elif os.path.exists(tmp): os.remove(tmp)
        return cur
    except Exception as e:
        print(f"  ⚠️ Enhancement failed: {e}")
        if os.path.exists(tmp): os.remove(tmp)
        return image_path

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2: print("Usage: python photo_enhancer.py <image> [--cutout]"); sys.exit(1)
    print(f"Result: {enhance_photo(sys.argv[1], do_cutout='--cutout' in sys.argv)}")
```

**Verify:** `python photo_enhancer.py /opt/nuhoot/remotion/public/photos/restaurants.jpg` → prints upscale/face messages (or graceful warnings if no GPU/weights).

---

## Phase 5 — Pipeline Integration (modify `pipeline_v3.py`)

Insert compositing + enhancement **between** Kimi JSON parse and Remotion render.

### Patch — Insert Step 1.5 (line 634-637)

**Old:**
```python
            # Step 2: Render with DynamicComposer
            print("  [2] Rendering with DynamicComposer...")
            render_path = f"{RENDER_DIR}/{niche}_iter{iteration}.png"
            success = render_blueprint(blueprint, render_path)
```
**New:**
```python
            # Step 1.5: Photo compositing + enhancement (NEW)
            print("  [1.5] Processing photos...")
            from photo_compositor import composite_photos
            from photo_enhancer import enhance_photo
            from photo_db import record_composite
            ad_id = f"{niche}_iter{iteration}"

            for block in blueprint.get("composition", []):
                comp = block.get("component", "")
                props = block.get("props", {})

                # Multi-photo components → composite into single image
                if comp in ("PhotoGrid", "PhotoMosaic", "FrameStack"):
                    photo_ids = props.get("photos", [])
                    if len(photo_ids) >= 2:
                        comp_path = composite_photos(photo_ids, niche, ad_id)
                        if comp_path:
                            block["component"] = "PhotoSingle"
                            block["props"] = {"src": comp_path, "showOverlay": True}
                            record_composite(ad_id, niche, comp_path,
                                            photo_ids, comp, ad_id)
                            abs_comp = os.path.join("/opt/nuhoot/remotion/public", comp_path)
                            enhance_photo(abs_comp, do_upscale=False, do_face=True)

                # Single-photo components → enhance
                elif comp in ("PhotoSingle", "PhotoFrame", "PhotoArch", "PhotoCircle",
                              "PhotoDiagonal", "PhotoDuotone", "PhotoDoubleFrame",
                              "FramePolaroid", "FrameCircle", "HeaderOverlay"):
                    src = props.get("src", "")
                    if src and src.startswith("photos/"):
                        abs_src = os.path.join("/opt/nuhoot/remotion/public", src)
                        if os.path.exists(abs_src):
                            enhance_photo(abs_src, do_upscale=False, do_face=True)

            # Step 2: Render with DynamicComposer
            print("  [2] Rendering with DynamicComposer...")
            render_path = f"{RENDER_DIR}/{niche}_iter{iteration}.png"
            success = render_blueprint(blueprint, render_path)
```

**Why `do_upscale=False`:** 4x upscaling every iteration is too slow/VRAM-heavy. Upscale is a one-time batch job (Phase 6). GFPGAN face-fix is fast enough for per-iteration use.

**Data flow:** `generate_blueprint()` (Kimi picks IDs) → `normalize_blueprint()` (IDs→paths) → **[NEW] compositing** (multi-photo→single) → **[NEW] enhancement** (face-fix) → `render_blueprint()` → existing quality loop.

---

## Phase 6 — Testing

```bash
cd /opt/nuhoot/eagle-eye

# Phase 1: Database
python photo_db.py init          # → "✓ Tagged 21 existing photos"
python photo_db.py openverse 5   # → ~105 photos added (~15 min)
python photo_db.py stats         # → count per niche

# Phase 2: Kimi Selection
python -c "from photo_db import get_photo_catalog_text; print(get_photo_catalog_text('restaurants'))"
python -c "from photo_db import resolve_photo_id as r; assert r('restaurants_00','restaurants')=='photos/restaurants.jpg'; assert r('bad','restaurants')=='photos/restaurants.jpg'; print('✓ OK')"

# Phase 3: Compositing
python photo_compositor.py restaurants photos/restaurants.jpg photos/cafes.jpg
ls -la /opt/nuhoot/remotion/public/photos/restaurants_composite_test.jpg  # >10KB

# Phase 4: Enhancement
python photo_enhancer.py /opt/nuhoot/remotion/public/photos/restaurants.jpg
# GPU+weights: "🔼 Upscaled 4x" + "😊 Faces enhanced" / Without: graceful warnings

# Phase 5: Full Pipeline
python pipeline_v3.py restaurants
# → [1] Kimi → [1.5] Processing photos → [2] Render → [3] OpenCV → [4] Tesseract → [5] Critique
ls /opt/nuhoot/remotion/public/photos/restaurants_composite_*.jpg

# Batch upscale (one-time, not per-iteration)
python -c "import glob; from photo_enhancer import upscale_image; [upscale_image(f,f) for f in glob.glob('/opt/nuhoot/remotion/public/photos/*.jpg') if '_composite_' not in f]; print('✓ done')"
```
---

## Install Order & Files

```bash
pip install httpx opencv-python pillow numpy realesrgan gfpgan rembg basicsr torch torchvision
mkdir -p /opt/nuhoot/photos/weights
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -O /opt/nuhoot/photos/weights/RealESRGAN_x4plus.pth
wget https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth -O /opt/nuhoot/photos/weights/GFPGANv1.4.pth
cd /opt/nuhoot/eagle-eye && python photo_db.py init && python photo_db.py openverse 5
python pipeline_v3.py restaurants
```

**Files:** CREATE `photo_db.py` (SQLite+Openverse+auto-tag) · CREATE `photo_compositor.py` (PIL strip/collage/blend) · CREATE `photo_enhancer.py` (Real-ESRGAN+GFPGAN+rembg) · MODIFY `pipeline_v3.py` (6 patches) · CREATE `photos/photos.db` (auto)
