# Free GPU Hosting Options for Nuhoot AI Inference

**Date:** July 2026 · **Use case:** Remote GPU for Real-ESRGAN (4x upscale, ~6GB VRAM),
GFPGAN (face enhancement, ~4GB VRAM), SD inpainting (~6-8GB VRAM fp16).
Called from `/opt/nuhoot/eagle-eye/photo_enhancer.py` on CPU-only server.
**Minimum viable VRAM:** 8GB (T4-class). Ideal: 16GB+.

---

## Quick Comparison

| Service | Free GPU? | VRAM | Remote API? | Persistent? |
|---------|-----------|------|-------------|-------------|
| **Google Colab** Free | T4 (not guaranteed) | 16GB | Via ngrok tunnel | ❌ Ephemeral 12h |
| **Kaggle** Notebooks | 2× T4 | 32GB | Via tunnel | ❌ Ephemeral 12h |
| HuggingFace Spaces | ❌ CPU only | 0GB | REST API ✓ | ✓ Persistent |
| Lightning AI Studios | $15/mo credits | varies | Via tunnel | Ephemeral |
| RunPod | ❌ No free tier | — | — | — |
| Vast.ai | ❌ No free tier | — | — | — |
| Oracle Cloud Free | ❌ ARM CPU only | 0GB | Full VM | ✓ Persistent |
| Paperspace Gradient | ❌ Free = CPU | 0GB | — | — |
| **Modal** | $30/mo credits | up to A100 | **REST API ✓** | **✓ Persistent** |
| Replicate | Trial credits only | varies | REST API ✓ | ✓ Persistent |
| SD WebUI on Colab | T4 via Colab | 16GB | Via ngrok | ❌ Ephemeral |
| ComfyUI on Colab | T4 via Colab | 16GB | Via ngrok | ❌ Ephemeral |

---

## Detailed Analysis

### 1. Google Colab (Free Tier)
- **Free?** Yes, but T4 allocation not guaranteed — priority to paid users.
  Sessions die after ~90 min idle, 12h/day hard cap. May get CPU-only or rate-limited.
- **Remote API?** No native API. Run FastAPI inside Colab, expose via ngrok/cloudflared tunnel.
- **VRAM:** T4 = 16GB. Enough for all 3 tools.
- **Persistent?** No — ephemeral, filesystem wiped on disconnect.
- **Verdict:** Best free option for getting started.

### 2. Kaggle Notebooks (Free GPU)
- **Free?** Yes — 30 hrs/week GPU (2× T4 or P100). Phone verification required, no payment info.
- **Remote API?** Same as Colab — run server inside notebook, tunnel out.
- **VRAM:** 2× T4 = 32GB. Most free VRAM available. Enough to run all 3 models loaded simultaneously.
- **Persistent?** No — 12h session max. 30 hrs/week cap resets Monday. Notebooks + datasets persist.
- **Verdict:** Most free GPU hours; best for batch processing.

### 3. HuggingFace Spaces (Free Tier)
- **Free?** Free tier is **CPU-only**. GPU requires Pro ($9/mo) or Community Grant (apply, not guaranteed).
- **Remote API?** Yes — native persistent REST endpoint. This is the key advantage IF you get GPU access.
- **VRAM:** 0GB free. Pro: A10G 22GB. Grant: A10G or A100.
- **Persistent?** Yes — runs continuously with stable URL.
- **Verdict:** Not viable free. If you get a community grant, this becomes the best option.

### 4. Lightning AI Studios
- **Free?** $15/mo credits (~68 hrs T4). Not truly free — credit card needed.
- **Remote API?** Deploy as Lightning App with REST endpoint. Also supports tunneling.
- **VRAM:** T4 (16GB) or A10G (22GB).
- **Persistent?** Studios run while credits last. Apps can have persistent URLs.
- **Verdict:** Limited free credits, developer-oriented.

### 5. RunPod
- **Free?** No permanent free tier. Occasionally $10 promo credits for new accounts. Then ~$0.20/hr (T4).
- **Remote API?** Yes — RunPod Serverless gives REST API.
- **VRAM:** Any GPU (T4 16GB → A100 80GB).
- **Verdict:** Not free, but cheapest persistent serverless API if budget allows.

### 6. Vast.ai
- **Free?** No free tier. Pay-as-you-go (~$0.10/hr T4). Minimum ~$5-10 deposit.
- **Remote API?** Docker containers with exposed ports. SSH tunnel for API.
- **VRAM:** Marketplace of rented GPUs — choose anything.
- **Verdict:** Cheapest raw GPU, but not free.

### 7. Oracle Cloud Free Tier
- **Free?** Yes — 4 ARM Ampere A1 cores + 24GB RAM, always free. **But CPU-only.**
  Oracle GPU instances (A10, V100) are NOT in free tier.
- **Remote API?** Full VM — run anything.
- **VRAM:** 0GB (no GPU).
- **Verdict:** Great free VM but no GPU. Could serve as API gateway or run slow CPU inference.

### 8. Paperspace (Gradient)
- **Free?** Free notebooks are **CPU-only**. Free GPU notebooks were discontinued.
- **Remote API?** Gradient deployments expose REST endpoints, paid only.
- **VRAM:** 0GB free.
- **Verdict:** No free GPU. Not viable.

### 9. Modal ⭐
- **Free?** $30/mo credits for individuals. Requires credit card, not charged until credits exhausted.
  T4 ~$0.164/hr → ~180 hrs/mo. A10G ~$0.596/hr → ~50 hrs/mo.
- **Remote API?** **Yes — native persistent REST endpoint.** Deploy a Python function, get HTTPS URL.
- **VRAM:** T4 (16GB), A10G (22GB), A100 (40/80GB) — your choice.
- **Persistent?** URL is permanent. GPU spins up on-demand (cold start ~10-30s), scales to zero when idle.
  No charges when idle.
- **Verdict:** Best option for a persistent API with no daily maintenance.

### 10. Replicate
- **Free?** Trial credits for new accounts (~$0.10-1). No permanent free tier.
  SD inpainting ~$0.0025/run. Real-ESRGAN ~$0.001/run.
- **Remote API?** **Yes — native REST API.** Pre-hosted models (SD inpainting, Real-ESRGAN, GFPGAN).
  No deployment needed — just call the API.
- **VRAM:** Handled by Replicate.
- **Persistent?** Yes — permanent API endpoint.
- **Verdict:** Easiest setup (models already hosted), but not free long-term. Good for prototyping.

### 11. Stable Diffusion WebUI (A1111) on Colab
- **Free?** Uses Colab free tier (same T4/limits).
- **Remote API?** Built-in `--api` flag exposes REST endpoints (`/sdapi/v1/img2img`, `/sdapi/v1/inpaint`).
  Tunnel via ngrok.
- **VRAM:** T4 16GB — enough for SD 1.5 inpainting.
- **Persistent?** Ephemeral. Many pre-made notebooks exist; some now require Colab Pro.

### 12. ComfyUI on Colab
- **Free?** Uses Colab free tier.
- **Remote API?** REST API (`/prompt`, `/history`). More memory-efficient than A1111.
- **VRAM:** T4 16GB — enough for SD 1.5 inpainting fp16.
- **Persistent?** Ephemeral. Community notebooks available.

### 13. Other Options
- **Genesis Cloud:** $50 free credits for new users, then pay-as-you-go. Not permanently free.
- **Lambda Labs:** No free tier. Pay-as-you-go from ~$0.50/hr.

---

## Tunneling: Colab/Kaggle → Your Server

Colab/Kaggle run in restricted networks — you can't connect directly. Use a reverse tunnel.

### ngrok (Easiest)
```python
# Inside Colab/Kaggle, after starting your API server on port 8000:
!pip install pyngrok
from pyngrok import ngrok
ngrok.set_auth_token("YOUR_TOKEN")  # from dashboard.ngrok.com
public_url = ngrok.connect(8000)
print(f"API URL: {public_url}")
```
- Free: 1 tunnel, random subdomain (changes on restart), 40 conn/min.

### Cloudflare Tunnel (cloudflared)
```bash
!wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
!chmod +x cloudflared
!./cloudflared tunnel --url http://localhost:8000 &
```
- Free, no account, no connection limits. Random URL each time.

### Tunneling Limitations
- URLs change every session restart — must update server config each time.
- Free ngrok = 1 concurrent connection (serial processing only).
- Colab may block tunnel traffic (against ToS); Kaggle technically allows it.
- ~200-500ms latency overhead per request on top of inference time.

---

## TOP 3 Recommended Approaches

### 🥇 #1: Google Colab Free + ngrok (Best for getting started)

Easiest setup, T4 16GB handles all 3 tools, no payment info. Tradeoff: ephemeral —
re-run notebook daily, update ngrok URL.

**Setup:**

1. Sign up at [colab.research.google.com](https://colab.research.google.com)
2. Get ngrok token at [dashboard.ngrok.com](https://dashboard.ngrok.com/get-started)
3. New notebook → `Runtime → Change runtime type → T4 GPU`

**Cell 1 — Install + download weights:**
```python
!pip install -q fastapi uvicorn pyngrok realesrgan gfpgan basicsr diffusers transformers accelerate
import os; os.makedirs("/content/weights", exist_ok=True)
!wget -q -O /content/weights/RealESRGAN_x4plus.pth https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth
!wget -q -O /content/weights/GFPGANv1.4.pth https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth
```

**Cell 2 — Load models + start API:**
```python
import cv2, base64, io, threading, numpy as np, torch
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from pyngrok import ngrok
import uvicorn

ngrok.set_auth_token("YOUR_NGROK_TOKEN")  # ← paste your token

from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet
from gfpgan import GFPGANer

upsampler = RealESRGANer(scale=4, model_path="/content/weights/RealESRGAN_x4plus.pth",
    half=True, tile=400, model=RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64,
    num_block=23, num_grow_ch=32, scale=4))
restorer = GFPGANer(model_path="/content/weights/GFPGANv1.4.pth", upscale=1,
    arch="clean", channel_multiplier=2, bg_upsampler=upsampler)

sd_pipe = None  # lazy-load SD on first inpaint request
app = FastAPI()

@app.post("/enhance")
async def enhance(file: UploadFile):
    data = await file.read()
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    _, _, output = restorer.enhance(img, paste_back=True)
    _, buf = cv2.imencode(".png", output)
    return JSONResponse({"image": base64.b64encode(buf).decode()})

@app.post("/upscale")
async def upscale(file: UploadFile):
    data = await file.read()
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    output, _ = upsampler.enhance(img, outscale=4)
    _, buf = cv2.imencode(".png", output)
    return JSONResponse({"image": base64.b64encode(buf).decode()})

@app.post("/inpaint")
async def inpaint(file: UploadFile, mask: UploadFile, prompt: str = "a person"):
    global sd_pipe
    if sd_pipe is None:
        from diffusers import StableDiffusionInpaintPipeline
        sd_pipe = StableDiffusionInpaintPipeline.from_pretrained(
            "runwayml/stable-diffusion-inpainting", torch_dtype=torch.float16).to("cuda")
    from PIL import Image
    img = Image.open(io.BytesIO(await file.read())).resize((512, 512))
    m = Image.open(io.BytesIO(await mask.read())).resize((512, 512))
    result = sd_pipe(prompt=prompt, image=img, mask_image=m).images[0]
    buf = io.BytesIO(); result.save(buf, format="PNG")
    return JSONResponse({"image": base64.b64encode(buf.getvalue()).decode()})

public_url = ngrok.connect(8000)
print(f"🚀 API live at: {public_url}")
threading.Thread(target=uvicorn.run, args=(app,),
    kwargs={"host": "0.0.0.0", "port": 8000}, daemon=True).start()
```

**Call from your server** — add to `photo_enhancer.py`:
```python
import requests
def remote_enhance(image_path, endpoint="/enhance"):
    url = os.environ.get("GPU_API_URL", "") + endpoint
    with open(image_path, "rb") as f:
        r = requests.post(url, files={"file": f}, timeout=120)
    if r.status_code == 200:
        out = image_path.replace(".", "_gpu.")
        with open(out, "wb") as f:
            f.write(base64.b64decode(r.json()["image"]))
        return out
    return image_path  # fallback to original
```

**Daily routine:** Open notebook → `Run all` → copy new ngrok URL → set `GPU_API_URL`. ~3 min.

---

### 🥈 #2: Kaggle Notebooks + cloudflared (Most free GPU hours)

30 hrs/week dual T4 (32GB VRAM — all 3 models loaded at once). More reliable than Colab.
No payment info — just phone verification.

**Setup:**

1. Sign up at [kaggle.com](https://kaggle.com) → verify phone (Settings → Phone verification)
2. New notebook → `Settings → Accelerator → GPU T4 x2` → `Settings → Internet → On`
3. **Cell 1** — same install/weights as Colab #1 (paths use `/kaggle/working/`)
4. **Cell 2** — same model loading + FastAPI app, but use cloudflared instead of ngrok:
```python
import subprocess, time
!wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
!chmod +x cloudflared
proc = subprocess.Popen(["./cloudflared", "tunnel", "--url", "http://localhost:8000"],
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
time.sleep(5)
for line in iter(proc.stdout.readline, b''):
    line = line.decode()
    if "trycloudflare.com" in line:
        print(f"🚀 {line.strip()}"); break
# Then start uvicorn same as Colab
```
5. Call from server same as Colab #1.
6. **Weekly cap:** 30 hrs ≈ 100-200 enhancement batches. Resets Monday.

---

### 🥉 #3: Modal (Best persistent REST API)

Only option with a **persistent HTTPS endpoint** + GPU on free credits.
No daily re-run. URL never changes. $30/mo ≈ 180 T4 hrs (~6,000-10,000 enhancements).

**Setup:**

1. Sign up at [modal.com](https://modal.com) → add credit card (not charged until credits used)
2. Install Modal CLI on your server: `pip install modal && modal setup`
3. Create `/opt/nuhoot/eagle-eye/gpu_api.py`:
```python
import modal

app = modal.App("nuhoot-gpu")
image = (modal.Image.debian_slim()
    .pip_install("fastapi", "realesrgan", "gfpgan", "basicsr", "diffusers",
                 "transformers", "accelerate", "opencv-python-headless",
                 "pillow", "torch", "torchvision")
    .apt_install("libgl1")
    .run_commands("mkdir -p /weights && "
        "wget -O /weights/RealESRGAN_x4plus.pth "
        "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth && "
        "wget -O /weights/GFPGANv1.4.pth "
        "https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth"))

@app.function(image=image, gpu="T4", timeout=300)
@modal.web_endpoint(method="POST")
def enhance(file: bytes = modal.File()):
    import cv2, base64, numpy as np
    from realesrgan import RealESRGANer
    from basicsr.archs.rrdbnet_arch import RRDBNet
    from gfpgan import GFPGANer
    upsampler = RealESRGANer(scale=4, model_path="/weights/RealESRGAN_x4plus.pth",
        half=True, tile=400, model=RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64,
        num_block=23, num_grow_ch=32, scale=4))
    restorer = GFPGANer(model_path="/weights/GFPGANv1.4.pth", upscale=1,
        arch="clean", channel_multiplier=2, bg_upsampler=upsampler)
    img = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)
    _, _, output = restorer.enhance(img, paste_back=True)
    _, buf = cv2.imencode(".png", output)
    return {"image": base64.b64encode(buf).decode()}
```
4. Deploy: `modal deploy /opt/nuhoot/eagle-eye/gpu_api.py`
   → Output: `https://your-workspace--nuhoot-gpu-enhance.modal.run`
5. Set URL: `echo 'GPU_API_URL=https://...modal.run' >> /opt/nuhoot/.env`
6. Call from `photo_enhancer.py` using same `remote_enhance()` as Colab #1.
7. Monitor: `modal app logs` — $30/mo ≈ 180 T4 hours.

---

## Recommendation for Nuhoot

| Need | Best Choice |
|------|-------------|
| Zero cost, quick start | **Colab + ngrok** (#1) |
| Maximum free GPU hours | **Kaggle + cloudflared** (#2) |
| Persistent API, no daily maintenance | **Modal** (#3) |
| Easiest (models pre-hosted, but paid) | Replicate |

**Suggested path:** Start with Colab + ngrok (#1) to validate the pipeline
end-to-end. Once confirmed working, migrate to Modal (#3) for a persistent
API that `photo_enhancer.py` can call without daily intervention. If Modal
credits run out, fall back to Colab/Kaggle.

**Fallback safety:** `photo_enhancer.py` already returns the original image
if enhancement fails — so if the GPU endpoint is down, the pipeline continues
with un-enhanced photos. Add a `remote_enhance()` call before the local CPU
fallback for best results.
