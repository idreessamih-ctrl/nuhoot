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
