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
