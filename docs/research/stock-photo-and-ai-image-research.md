# Stock Photo APIs & AI Image Generation Tools — Research for Nuhoot

**Goal:** Enable dynamic photo selection and AI compositing for a Saudi Arabian
social media ad system. Currently Nuhoot uses **one hardcoded photo per niche**
(21 photos in `remotion/public/photos/`). This report evaluates all FOSS/free
options for evolving to dynamic, diverse, culturally-relevant imagery at zero cost.

**Stack context:** Python 3.12 + FastAPI backend, Remotion (React 19 / TypeScript)
rendering engine, FFmpeg, Kimi K2.7 AI orchestrator, 76 React components,
`resolvePhoto()` → `staticFile()` path resolution.

---

## PART 1: FREE STOCK PHOTO APIs

### 1.1 — Openverse API ⭐ BEST OVERALL FIT

| Attribute | Detail |
|---|---|
| **URL** | https://api.openverse.org |
| **License** | API itself: MIT; images carry their own CC licenses |
| **Cost** | Completely free, no API key required for anonymous access |
| **Rate limit** | **20 requests/min** (burst), **200 requests/day** (sustained) — anonymous. Higher with registered account. |
| **Auth** | Optional OAuth2 (register at openverse.org for higher limits) |
| **Content sources** | 800M+ items from Flickr, Wikimedia Commons, NASA, museums, etc. |
| **Image count (Saudi queries)** | "Saudi Arabia" → 240 results; "Riyadh" → 240; "Saudi restaurant food" → 22; "Arabic woman traditional" → 224 |
| **Arabic/Middle East content** | ✅ Excellent — real Flickr photos from Saudi photographers, actual Saudi locations (Abha, Al Khobar, Riyadh), real food (kabsa, ALBAIK) |
| **License filtering** | ✅ `license_type=commercial` filter, individual license field per result (by, by-sa, by-nc, by-nd, etc.) |
| **Source filtering** | ✅ `source=flickr`, `source=wikimedia`, etc. |
| **Emotion/pose filter** | ❌ No native emotion filter — relies on keyword search quality |
| **Niche filter** | ⚠️ Via keyword only (e.g., "Saudi restaurant interior", "Saudi barbershop") |
| **Thumbnail support** | ✅ Thumbnail URL returned per result |
| **Metadata returned** | title, creator, creator_url, license, license_version, source, tags, height, width, url, thumbnail, detail_url |

**Verified API response fields (live test):**
```json
{
  "title": "saudi fish market",
  "creator": "zbigphotography (1M+ views)",
  "license": "by-sa",
  "license_version": "2.0",
  "source": "flickr",
  "url": "https://live.staticflickr.com/4081/4866617130_3efb31c415_b.jpg",
  "thumbnail": "https://api.openverse.org/v1/images/.../thumbnail/",
  "tags": [{"name": "arab", "accuracy": null}],
  "height": 697, "width": 1024
}
```

**Python integration:**
```python
import httpx

async def search_openverse(query: str, license_type: str = "commercial") -> list[dict]:
    """Search Openverse for royalty-free images."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://api.openverse.org/v1/images/",
            params={"q": query, "license_type": license_type, "page_size": 20}
        )
        data = resp.json()
        return [
            {
                "url": r["url"],
                "thumbnail": r.get("thumbnail", ""),
                "license": r["license"],
                "creator": r.get("creator", ""),
                "attribution": r.get("attribution", ""),
                "title": r.get("title", ""),
                "width": r.get("width"),
                "height": r.get("height"),
            }
            for r in data.get("results", [])
        ]
```

**Pros for Nuhoot:**
- No API key needed (works immediately with current stack)
- Real photos of real Saudi locations — authentic, not stocky
- License metadata included — critical for PDPL/compliance
- Already integrates with `httpx` (existing dependency)
- Attribution data available (CC licenses require attribution)

**Cons:**
- Rate limit is tight (200/day anonymous) — would need to cache aggressively
- Quality is inconsistent (Flickr amateur photos mixed with professional)
- No orientation/aspect-ratio filter (would need client-side filtering)
- Many `by-nc-nd` results (non-commercial, no derivatives) — must filter

---

### 1.2 — Unsplash API

| Attribute | Detail |
|---|---|
| **URL** | https://unsplash.com/developers |
| **License** | Unsplash License (free to use, no attribution required for API use) |
| **Cost** | Free |
| **Rate limit** | **Demo mode: 50 requests/hour. Production (after approval): 5,000 requests/hour** |
| **Auth** | API key required (register app, get Access Key) |
| **Content** | 3M+ high-quality professional photos |
| **Arabic/Middle East content** | ⚠️ Limited — mostly Western photographers. Some Riyadh/Mecca/Medina shots but sparse for niche businesses (barbershops, clinics, etc.) |
| **Emotion filter** | ❌ No native emotion filter |
| **Pose filter** | ❌ No pose filter |
| **Niche filter** | ⚠️ Keyword search + `collections` parameter. Has `query`, `color` filter, `orientation` (landscape/portrait/squarish), `content_filter` (high/low) |
| **Color filter** | ✅ Filter by dominant color |
| **Orientation filter** | ✅ landscape, portrait, squarish |

**Key API parameters:**
- `query` — search keyword
- `color` — filter by hex color (useful for matching niche ColorConfig)
- `orientation` — landscape / portrait / squarish
- `content_filter` — high (safe) / low
- `collections` — search within specific collection IDs
- `order_by` — latest / relevant

**Python integration:**
```python
async def search_unsplash(query: str, orientation: str = "squarish") -> list[dict]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://api.unsplash.com/search/photos",
            params={"query": query, "orientation": orientation, "per_page": 30},
            headers={"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
        )
        data = resp.json()
        return [
            {
                "url": r["urls"]["regular"],
                "thumbnail": r["urls"]["thumb"],
                "color": r.get("color"),  # dominant color hex
                "width": r["width"],
                "height": r["height"],
                "alt": r.get("alt_description", ""),
                "photographer": r["user"]["name"],
            }
            for r in data.get("results", [])
        ]
```

**Pros for Nuhoot:**
- Highest quality photos of any free API (professional, curated)
- No attribution required (simplifies compliance)
- Color filter is excellent for matching niche ColorConfig palettes
- Orientation filter ensures photos fit component aspect ratios
- `download()` endpoint tracks usage (Unsplash requirement)

**Cons:**
- Demo mode only 50 req/hour until approved for production
- Very sparse Arabic/Saudi-specific content
- Western-centric — most results for "barbershop" show Western-style shops
- Approval process can take days/weeks
- Must call download endpoint to comply with API guidelines

---

### 1.3 — Pexels API

| Attribute | Detail |
|---|---|
| **URL** | https://www.pexels.com/api/ |
| **License** | Pexels License (free, no attribution required, no restriction on commercial use) |
| **Cost** | Free |
| **Rate limit** | **200 requests/hour** (generous for a free API) |
| **Auth** | API key required (instant registration, no approval wait) |
| **Content** | 3M+ photos + videos |
| **Arabic/Middle East content** | ⚠️ Limited but slightly better than Unsplash for Middle Eastern scenes. Has some Saudi/Arabic content. |
| **Emotion filter** | ❌ No emotion filter |
| **Pose filter** | ❌ No pose filter |
| **Niche filter** | ⚠️ Keyword search only |
| **Orientation filter** | ✅ landscape, portrait, square |
| **Color filter** | ✅ Filter by hex color or color name |
| **Video support** | ✅ Can search videos too (useful for Reels) |

**Key API parameters:**
- `query` — search keyword
- `orientation` — landscape / portrait / square
- `color` — hex color or named color
- `per_page` — up to 80
- `page` — pagination

**Python integration:**
```python
async def search_pexels(query: str, orientation: str = "square") -> list[dict]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://api.pexels.com/v1/search",
            params={"query": query, "orientation": orientation, "per_page": 80},
            headers={"Authorization": PEXELS_API_KEY}
        )
        data = resp.json()
        return [
            {
                "url": r["src"]["large"],
                "thumbnail": r["src"]["tiny"],
                "alt": r.get("alt", ""),
                "width": r["width"],
                "height": r["height"],
                "photographer": r["photographer"],
            }
            for r in data.get("photos", [])
        ]
```

**Pros for Nuhoot:**
- Instant API key (no approval wait — unlike Unsplash)
- No attribution required
- 200 req/hour is sufficient for cached batch fetching
- Video search for Reels content
- Good quality, professional photos
- `src` object provides multiple sizes (original, large, medium, small, tiny, portrait, landscape, square)

**Cons:**
- Still Western-centric for most niche queries
- No emotion/content classification
- No collections API for curated Saudi content

---

### 1.4 — Pixabay API

| Attribute | Detail |
|---|---|
| **URL** | https://pixabay.com/api/docs/ |
| **License** | Pixabay Content License (free, no attribution required, commercial use OK) |
| **Cost** | Free |
| **Rate limit** | **100 requests per 60 seconds** (per API key) |
| **Auth** | API key required (instant registration) |
| **Content** | 4M+ photos, videos, illustrations, vector graphics |
| **Arabic/Middle East content** | ⚠️ Very limited. Mostly generic stock. Some Middle Eastern architecture/landscapes but virtually no Saudi-specific business scenes. |
| **Emotion filter** | ✅ **Yes!** `image_type` includes "illustration" and "photo"; category "feelings" filters for emotional content |
| **Niche filter** | ✅ **Best of all APIs!** Categories: `backgrounds, fashion, nature, science, education, feelings, health, people, religion, places, animals, industry, computer, food, sports, transportation, travel, buildings, business, music` |
| **Color filter** | ✅ Filter by 14 colors: transparent, grayscale, red, orange, yellow, green, turquoise, blue, lilac, pink, white, gray, black, brown |
| **Orientation filter** | ✅ horizontal, vertical, all |
| **Editors choice** | ✅ `editors_choice=true` for highest quality |
| **Image type** | ✅ all, photo, illustration, vector |

**Verified categories (live from API docs):**
```
animals, backgrounds, buildings, business, computer, education,
fashion, feelings, food, health, industry, music, nature, people,
places, religion, science, sports, transportation, travel
```

**Verified color filter values:**
```
transparent, grayscale, red, orange, yellow, green, turquoise,
blue, lilac, pink, white, gray, black, brown
```

**Key API parameters:**
- `q` — search query (URL-encoded)
- `lang` — language: en, ar, de, fr, es, it, ja, ko, etc. (**Arabic supported!**)
- `image_type` — all / photo / illustration / vector
- `orientation` — all / horizontal / vertical
- `category` — see categories above
- `colors` — comma-separated color filter
- `editors_choice` — true/false
- `safesearch` — true/false
- `order` — popular / latest
- `per_page` — 3-200 (default 20)
- `min_width`, `min_height` — minimum dimensions

**Python integration:**
```python
async def search_pixabay(
    query: str,
    category: str = "",
    lang: str = "en",
    colors: str = "",
    image_type: str = "photo",
    orientation: str = "all",
    editors_choice: bool = False,
    min_width: int = 1080,
    per_page: int = 50,
) -> list[dict]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://pixabay.com/api/",
            params={
                "key": PIXABAY_API_KEY,
                "q": query,
                "lang": lang,
                "image_type": image_type,
                "orientation": orientation,
                "category": category,
                "colors": colors,
                "editors_choice": str(editors_choice).lower(),
                "safesearch": "true",
                "min_width": min_width,
                "per_page": per_page,
            }
        )
        data = resp.json()
        return [
            {
                "url": r["largeImageURL"],
                "thumbnail": r["previewURL"],
                "tags": r.get("tags", ""),
                "views": r.get("views", 0),
                "downloads": r.get("downloads", 0),
                "likes": r.get("likes", 0),
                "width": r.get("imageWidth"),
                "height": r.get("imageHeight"),
                "type": r.get("type"),
            }
            for r in data.get("hits", [])
        ]
```

**Pros for Nuhoot:**
- **Best filtering of any free API** — category, color, orientation, image type, editors choice
- `lang=ar` parameter for Arabic language search
- 100 req/min is the highest sustained rate limit
- No attribution required
- Includes illustrations and vectors (useful for icon-style graphics)
- `min_width`/`min_height` filters ensure high-res results
- Tags field can be parsed for content classification
- View/download/like counts for quality sorting

**Cons:**
- Very sparse Saudi-specific content
- Most "Saudi Arabia" results are generic desert/landscape shots
- Quality is more variable than Unsplash/Pexels
- Hotlinking required (or download and cache)

---

### 1.5 — Stock Photo API Comparison Matrix

| Feature | Openverse | Unsplash | Pexels | Pixabay |
|---|---|---|---|---|
| **Cost** | Free | Free | Free | Free |
| **Auth required** | No (anonymous) | Yes (API key) | Yes (API key) | Yes (API key) |
| **Rate limit** | 20/min, 200/day | 50/hr (demo), 5K/hr (prod) | 200/hr | 100/min |
| **Attribution needed** | Yes (CC licenses) | No | No | No |
| **Arabic content** | ✅ Best (real Flickr photos) | ❌ Minimal | ❌ Minimal | ❌ Minimal |
| **Saudi-specific** | ✅ Real locations | ❌ | ❌ | ❌ |
| **Category filter** | ❌ | ❌ | ❌ | ✅ 20 categories |
| **Color filter** | ❌ | ✅ Hex | ✅ Hex/name | ✅ 14 colors |
| **Orientation filter** | ❌ | ✅ | ✅ | ✅ |
| **Emotion filter** | ❌ | ❌ | ❌ | ⚠️ "feelings" category |
| **License filter** | ✅ commercial/non-commercial | N/A (all free) | N/A | N/A |
| **Image quality** | Variable (amateur→pro) | ⭐ Best | Good | Variable |
| **Video support** | ❌ | ❌ | ✅ | ✅ |
| **Illustrations** | ✅ | ❌ | ❌ | ✅ |
| **API key wait time** | None | Days (approval) | Instant | Instant |
| **Python integration** | `httpx` (existing dep) | `httpx` | `httpx` | `httpx` |

---

## PART 2: SELF-HOSTED AI IMAGE GENERATION

### 2.1 — Stable Diffusion XL (SDXL) ⭐ RECOMMENDED

| Attribute | Detail |
|---|---|
| **Model** | `stabilityai/stable-diffusion-xl-base-1.0` |
| **License** | **Open RAIL++-M** (CreativeML Open RAIL++-M License) — allows commercial use with usage-based restrictions |
| **Resolution** | 1024×1024 native (can generate other aspect ratios) |
| **VRAM needed** | ~8GB for fp16, ~6GB with xFormers, ~4GB with quantization |
| **Quality** | Excellent — state-of-the-art open model |
| **Inference library** | `diffusers` (Apache 2.0), `comfyui`, `AUTOMATIC1111` |
| **Arabic text in images** | ❌ Cannot render Arabic text accurately |
| **Saudi people generation** | ✅ **Yes** — can generate Middle Eastern/Saudi people with proper prompting ("Saudi Arabian man wearing thobe and shemagh", "Arab woman in abaya and hijab") |
| **Saudi scenes** | ✅ Can generate Riyadh skyline, Saudi interiors, desert landscapes, modern Saudi architecture |
| **Prompt adherence** | High — follows detailed prompts well with SDXL Refiner |

**Python integration (diffusers):**
```python
import torch
from diffusers import StableDiffusionXLPipeline

# Load once, reuse across requests
pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True,
)
pipe.to("cuda")
pipe.enable_model_cpu_offload()  # saves VRAM

def generate_saudi_photo(
    niche: str,
    prompt: str,
    negative_prompt: str = "low quality, blurry, deformed, extra limbs",
    width: int = 1024,
    height: int = 1024,
    steps: int = 30,
    guidance_scale: float = 7.0,
    seed: int | None = None,
) -> str:
    """Generate a Saudi-specific photo for a niche."""
    generator = torch.Generator("cuda").manual_seed(seed) if seed else None
    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=width,
        height=height,
        num_inference_steps=steps,
        guidance_scale=guidance_scale,
        generator=generator,
    ).images[0]
    path = f"/opt/nuhoot/assets/photos/ai_generated/{niche}_{seed or 'default'}.png"
    image.save(path)
    return path
```

**Saudi-specific prompt templates:**
```python
SAUDI_PROMPTS = {
    "restaurants": "Professional photo of a modern Saudi restaurant interior, "
                   "elegant Arabian decor, warm lighting, date palms, Arabic "
                   "calligraphy on walls, luxurious setting, high quality, 4k",
    "cafes": "Saudi Arabian specialty coffee shop, modern Riyadh cafe interior, "
             "Arabic coffee being served, elegant decor, warm ambient lighting",
    "barbershops": "Modern Saudi barbershop interior, Middle Eastern man "
                   "getting a haircut, professional grooming setting, clean "
                   "modern design, warm lighting",
    "salons": "Luxury Saudi beauty salon interior, elegant Arabic decor, "
              "modern styling chairs, soft lighting, premium atmosphere",
    "clinics": "Modern Saudi medical clinic interior, clean professional "
               "healthcare setting, Middle Eastern doctor, medical equipment",
    "perfumes": "Luxury Arabian perfume shop interior, oud and bakhoor "
                "display, elegant bottles, Arabic golden decor, premium "
                "atmosphere, warm lighting",
    "fashion": "Saudi Arabian fashion boutique, mannequins wearing abayas "
               "and thobes, modern Riyadh retail interior, elegant lighting",
    "real_estate": "Modern Saudi luxury villa exterior, Riyadh architecture, "
                   "contemporary Arabian design, palm trees, golden hour",
    # ... all 21 niches
}
```

---

### 2.2 — FLUX.1

| Attribute | Detail |
|---|---|
| **Models** | `FLUX.1-schnell` (Apache 2.0), `FLUX.1-dev` (non-commercial), `FLUX.1-pro` (paid API) |
| **License (schnell)** | **Apache 2.0** — fully open, commercial use OK ✅ |
| **License (dev)** | Non-commercial only — ❌ cannot use for Nuhoot (commercial) |
| **Resolution** | Up to 2048×2048 |
| **VRAM needed** | ~24GB for full precision, ~12GB with quantization/nf4 |
| **Quality** | ⭐ **Best of all open models** — rivals Midjourney/DALL-E 3 |
| **Arabic text** | ❌ Cannot render Arabic text |
| **Saudi people** | ✅ Excellent — superior prompt adherence, generates realistic diverse people |
| **Saudi scenes** | ✅ Excellent — best model for photorealistic scene generation |
| **Inference** | `diffusers` (Apache 2.0), supports 4-step schnell generation |

**Important:** Only **FLUX.1-schnell** is usable commercially. FLUX.1-dev is
non-commercial. The schnell variant uses only 4 inference steps (vs 30+ for
SDXL), making it **8× faster** while maintaining near-equal quality.

**Python integration (diffusers):**
```python
import torch
from diffusers import FluxPipeline

pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-schnell",
    torch_dtype=torch.bfloat16,
)
pipe.to("cuda")
pipe.enable_model_cpu_offload()

def generate_flux_image(prompt: str, seed: int | None = None) -> str:
    """Generate with FLUX.1-schnell (4 steps, Apache 2.0 license)."""
    generator = torch.Generator("cuda").manual_seed(seed) if seed else None
    image = pipe(
        prompt=prompt,
        num_inference_steps=4,       # schnell = 4 steps!
        guidance_scale=0.0,          # schnell uses no guidance
        generator=generator,
        height=1024,
        width=1024,
    ).images[0]
    return image
```

**VRAM optimization for FLUX:**
```python
# NF4 quantization — runs FLUX on 8GB VRAM
from transformers import T5EncoderModel
from diffusers import FluxTransformer2DModel
from optimum.quanto import quantize, freeze, qfloat8

text_encoder = T5EncoderModel.from_pretrained(
    "black-forest-labs/FLUX.1-schnell", subfolder="text_encoder_2"
)
quantize(text_encoder, weights=qfloat8)
freeze(text_encoder)

transformer = FluxTransformer2DModel.from_pretrained(
    "black-forest-labs/FLUX.1-schnell", subfolder="transformer"
)
quantize(transformer, weights=qfloat8)
freeze(transformer)

pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-schnell",
    text_encoder_2=text_encoder,
    transformer=transformer,
    torch_dtype=torch.bfloat16,
)
```

---

### 2.3 — Kandinsky 2.2

| Attribute | Detail |
|---|---|
| **Model** | `kandinsky-community/kandinsky-2-2-decoder` |
| **License** | **Apache 2.0** — fully open, commercial use OK ✅ |
| **Resolution** | 512×512 native (can upscale) |
| **VRAM needed** | ~4GB |
| **Quality** | Good but below SDXL and FLUX |
| **Saudi people** | ✅ Can generate, but less accurate than SDXL/FLUX |
| **Inference** | `diffusers` (Apache 2.0) |

**Python integration:**
```python
from diffusers import KandinskyV22Pipeline, KandinskyV22PriorPipeline

prior = KandinskyV22PriorPipeline.from_pretrained(
    "kandinsky-community/kandinsky-2-2-prior", torch_dtype=torch.float16
).to("cuda")
pipe = KandinskyV22Pipeline.from_pretrained(
    "kandinsky-community/kandinsky-2-2-decoder", torch_dtype=torch.float16
).to("cuda")

def generate_kandinsky(prompt: str):
    image_emb, zero_emb = prior(prompt, return_dict=False)
    image = pipe(image_embeds=image_emb, negative_image_embeds=zero_emb).images[0]
    return image
```

**Assessment:** Kandinsky is a viable lightweight option but quality is
noticeably below SDXL/FLUX. Use only if VRAM is extremely constrained (<4GB).

---

### 2.4 — ControlNet (Pose Control)

| Attribute | Detail |
|---|---|
| **Model** | `lllyasviel/sd-controlnet-openpose` (SD 1.5), `lllyasviel/ControlNet` (SDXL variants) |
| **License** | OpenRAIL (same as Stable Diffusion base) |
| **Purpose** | Control pose, composition, depth, edges of generated images |
| **Pose models** | OpenPose (body keypoints), Canny (edges), Depth (depth map), MLSD (lines), Scribble, Segmentation |
| **VRAM** | +2-4GB on top of base model |
| **Integration** | `diffusers` ControlNet pipeline |

**What this enables for Nuhoot:**
- Generate a Saudi person in a **specific pose** (holding product, sitting at desk, pointing)
- Use a **reference photo's composition** while changing the subject
- **Inpainting**: add a Saudi person into an existing product/environment photo
- **Img2img**: transform a stock photo into a Saudi-localized version

**Python integration (pose control):**
```python
import torch
from diffusers import StableDiffusionXLControlNetPipeline, ControlNetModel
from controlnet_aux import OpenposeDetector

# Load ControlNet for OpenPose
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-openpose", torch_dtype=torch.float16
)
pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    controlnet=controlnet,
    torch_dtype=torch.float16,
).to("cuda")

# Extract pose from a reference image
openpose = OpenposeDetector.from_pretrained("lllyasviel/ControlNet")

def generate_with_pose(reference_image, prompt: str):
    """Generate a Saudi person in the same pose as the reference image."""
    pose_map = openpose(reference_image)
    image = pipe(
        prompt=prompt,
        image=pose_map,
        num_inference_steps=30,
        guidance_scale=7.0,
    ).images[0]
    return image
```

---

### 2.5 — Inpainting (Adding Humans to Existing Photos)

| Attribute | Detail |
|---|---|
| **Model** | SDXL Inpainting / FLUX Inpainting |
| **License** | Same as base model (OpenRAIL++ for SDXL, Apache 2.0 for FLUX schnell) |
| **Purpose** | Modify specific regions of an existing image |
| **Use case** | Take a stock photo of a restaurant → inpaint a Saudi person into the scene |

**Python integration (SDXL inpainting):**
```python
from diffusers import StableDiffusionXLInpaintPipeline
from PIL import Image, ImageDraw

pipe = StableDiffusionXLInpaintPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
).to("cuda")

def add_saudi_person_to_scene(
    scene_path: str,           # existing photo (restaurant, clinic, etc.)
    person_prompt: str,        # "Saudi Arabian man in thobe sitting at table"
    mask_coords: tuple,        # (x, y, w, h) region to inpaint
) -> str:
    """Inpaint a Saudi person into an existing scene photo."""
    scene = Image.open(scene_path).convert("RGB").resize((1024, 1024))
    
    # Create mask (white = area to generate, black = keep)
    mask = Image.new("L", (1024, 1024), 0)  # black = keep all
    draw = ImageDraw.Draw(mask)
    x, y, w, h = mask_coords
    draw.rectangle([x, y, x + w, y + h], fill=255)  # white = regenerate
    
    result = pipe(
        prompt=person_prompt,
        image=scene,
        mask_image=mask,
        num_inference_steps=30,
        guidance_scale=7.5,
        strength=0.85,
    ).images[0]
    return result
```

---

### 2.6 — AI Generation Comparison Matrix

| Feature | SDXL | FLUX.1-schnell | FLUX.1-dev | Kandinsky 2.2 |
|---|---|---|---|---|
| **License** | OpenRAIL++-M | Apache 2.0 | Non-commercial | Apache 2.0 |
| **Commercial use** | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes |
| **Quality** | Excellent | ⭐ Best | ⭐ Best | Good |
| **Resolution** | 1024×1024 | 2048×2048 | 2048×2048 | 512×512 |
| **VRAM (fp16)** | ~8GB | ~24GB | ~24GB | ~4GB |
| **VRAM (quantized)** | ~4GB | ~8GB (nf4) | ~8GB (nf4) | ~3GB |
| **Steps needed** | 30 | 4 | 28 | 30 |
| **Time/image (A100)** | ~6s | ~2s | ~12s | ~4s |
| **Saudi people** | ✅ Good | ✅ Excellent | ✅ Excellent | ✅ Fair |
| **ControlNet support** | ✅ Mature | ⚠️ Emerging | ⚠️ Emerging | ✅ |
| **Inpainting** | ✅ Native | ✅ Via diffusers | ✅ Via diffusers | ✅ |
| **Best for** | General use | Speed + quality | N/A (license) | Low VRAM |

---

## PART 3: POST-PROCESSING TOOLS

### 3.1 — rembg (Background Removal)

| Attribute | Detail |
|---|---|
| **Package** | `rembg` (PyPI) |
| **Version** | 2.0.76 |
| **License** | **MIT** ✅ |
| **Summary** | Remove image background — FOSS alternative to remove.bg |
| **Models** | U2Net (general), ISNet (high quality), BRIA RMBG (best quality) |
| **GPU support** | ✅ CUDA support |
| **Quality** | Excellent for people/objects; struggles with hair/fine details |
| **Batch mode** | ✅ CLI and API for batch processing |
| **Speed** | ~1-2s per image on GPU, ~5-10s on CPU |

**Python integration:**
```python
from rembg import remove, new_session

# Use the highest-quality model
session = new_session("isnet")  # or "u2net", "bria"

def remove_background(image_path: str) -> bytes:
    """Remove background, return PNG with transparency."""
    with open(image_path, "rb") as f:
        input_data = f.read()
    output = remove(input_data, session=session)
    return output

# For use in Nuhoot pipeline:
# 1. AI generates a Saudi person → rembg removes background
# 2. Composite person onto niche-specific background in Remotion
# 3. Or: stock photo subject → rembg → composite onto AI-generated scene
```

**Nuhoot use case:** Generate a Saudi person with SDXL/FLUX → remove background
with rembg → composite onto existing niche photo in Remotion. This allows
**adding a Saudi person to ANY existing stock photo** without inpainting.

**Installation:**
```bash
pip install rembg[gpu]  # or rembg[cpu]
# Download models automatically on first use
```

---

### 3.2 — Real-ESRGAN (Image Upscaling)

| Attribute | Detail |
|---|---|
| **Package** | `realesrgan` (PyPI) |
| **Version** | 0.3.0 |
| **License** | **BSD-3-Clause** ✅ |
| **Summary** | Practical algorithm for general image restoration/upscaling |
| **Models** | RealESRGAN_x4plus (4× upscale), RealESRGAN_x2plus (2×), RealESRGAN_x4plus_anime_6B |
| **GPU support** | ✅ CUDA |
| **Quality** | Excellent — adds realistic detail during upscaling |
| **Speed** | ~2-3s per 512×512 → 2048×2048 on GPU |
| **Scale factor** | 2× or 4× |

**Python integration:**
```python
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet
import cv2
import numpy as np

# Initialize upscaler
model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64,
                num_block=23, num_grow_ch=32, scale=4)
upsampler = RealESRGANer(
    scale=4,
    model_path="weights/RealESRGAN_x4plus.pth",
    model=model,
    tile=0,        # 0 = auto, avoids OOM on large images
    tile_pad=10,
    pre_pad=0,
    half=True,     # fp16 for speed
    gpu_id=0,
)

def upscale_image(image_path: str, out_scale: float = 2.0) -> str:
    """Upscale image 2× or 4× with Real-ESRGAN."""
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    output, _ = upsampler.enhance(img, outscale=out_scale)
    out_path = image_path.replace(".", f"_upscaled.")
    cv2.imwrite(out_path, output)
    return out_path
```

**Nuhoot use case:** Upscale low-resolution Openverse/Flickr stock photos
(many are 1024×697 or smaller) to 2048×2048 for high-quality ad output.
Also useful for upscaling 512×512 AI-generated images (Kandinsky) to usable sizes.

---

### 3.3 — GFPGAN (Face Enhancement/Restoration)

| Attribute | Detail |
|---|---|
| **Package** | `gfpgan` (PyPI) |
| **Version** | 1.3.8 |
| **License** | **Apache 2.0** ✅ |
| **Summary** | Real-world face restoration — fixes blurry/damaged/low-res faces |
| **Models** | GFPGANv1.3 (general), GFPGANv1.4 (more natural), RestoreFormer |
| **GPU support** | ✅ CUDA |
| **Quality** | Excellent — dramatically improves AI-generated and low-res faces |
| **Speed** | ~1-2s per face on GPU |
| **Only faces** | Yes — detects and enhances faces, leaves rest of image untouched |

**Python integration:**
```python
from gfpgan import GFPGANer
import cv2

# Initialize face restorer
restorer = GFPGANer(
    model_path="weights/GFPGANv1.4.pth",
    upscale=1,        # don't upscale, just restore face
    arch="clean",     # clean architecture
    channel_multiplier=2,
    bg_upsampler=upsampler,  # optional: pass Real-ESRGAN for background too
)

def enhance_faces(image_path: str) -> str:
    """Enhance/restore faces in an image using GFPGAN."""
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    _, _, output = restorer.enhance(
        img,
        paste_back=True,   # paste restored face back onto original
        has_aligned=False,
        only_center_face=False,
    )
    out_path = image_path.replace(".", f"_enhanced.")
    cv2.imwrite(out_path, output)
    return out_path
```

**Nuhoot use case:** AI-generated Saudi people sometimes have facial
artifacts (distorted eyes, asymmetric features). GFPGAN fixes these in
post-processing. Also enhances faces in low-res stock photos.

**Pipeline integration (combined):**
```python
def full_enhancement_pipeline(image_path: str) -> str:
    """Complete post-processing: upscale → face enhance → background remove."""
    # Step 1: Upscale with Real-ESRGAN
    upscaled = upscale_image(image_path, out_scale=2.0)
    
    # Step 2: Enhance faces with GFPGAN
    enhanced = enhance_faces(upscaled)
    
    # Step 3: Remove background with rembg (optional)
    # final = remove_background(enhanced)
    
    return enhanced
```

---

### 3.4 — Post-Processing Tool Comparison

| Tool | License | Purpose | GPU | Speed | Quality |
|---|---|---|---|---|---|
| rembg | MIT | Background removal | ✅ | 1-2s/img | Excellent |
| Real-ESRGAN | BSD-3 | Upscaling 2×/4× | ✅ | 2-3s/img | Excellent |
| GFPGAN | Apache 2.0 | Face restoration | ✅ | 1-2s/face | Excellent |

**All three are FOSS, commercially usable, and integrate via Python with CUDA.**

---

## PART 4: INTEGRATION WITH NUHOOT STACK

### 4.1 — Current Architecture (as-is)

```
Kimi K2.7 generates JSON blueprint
    → pipeline_v3.py picks photoPath (e.g., "photos/restaurants.jpg")
    → DynamicComposer.tsx renders via Remotion
    → resolvePhoto("photos/restaurants.jpg") → staticFile()
    → Chromium renders PNG at 1080×1080
```

**Problem:** One photo per niche. 21 niches × 1 photo = 21 photos.
Every restaurant ad uses the same image. No variation, no personalization.

### 4.2 — Proposed Architecture (with dynamic photos)

```
Kimi K2.7 generates JSON blueprint
    → photo_selector.py (NEW) picks best photo for this business:
        1. Check local cache: /assets/photos/{niche}/{filename}
        2. If insufficient: query stock APIs (Pixabay/Pexels/Openverse)
        3. If needs Saudi-specific: AI generate (SDXL/FLUX)
        4. Post-process: rembg → Real-ESRGAN → GFPGAN
        5. Save to /remotion/public/photos/{niche}/{unique_id}.jpg
    → pipeline_v3.py photoPath = "photos/{niche}/{unique_id}.jpg"
    → Remotion renders as before
```

### 4.3 — Photo Selection Service (Python)

```python
"""
Nuhoot Photo Selection Service — chooses or generates the best photo
for a given business + niche combination.

Priority:
1. Pre-curated local photos (existing 10/niche = 210 total)
2. Stock API photos (Pixabay → Pexels → Openverse)
3. AI-generated photos (FLUX schnell → SDXL)
4. Post-processing pipeline (rembg → Real-ESRGAN → GFPGAN)
"""

import httpx
import asyncio
import hashlib
import os
from pathlib import Path
from typing import Optional

class PhotoSelector:
    def __init__(self):
        self.cache_dir = Path("/opt/nuhoot/assets/photos")
        self.public_dir = Path("/opt/nuhoot/remotion/public/photos")
        self.client = httpx.AsyncClient(timeout=30)
        
    async def select_photo(
        self,
        niche: str,
        business_name: str,
        mood: str = "sophisticated",
        orientation: str = "square",
        color_hint: Optional[str] = None,
    ) -> str:
        """Returns a Remotion-compatible photo path."""
        
        # Step 1: Check if we have enough local variety (aim for 20+ per niche)
        local_photos = list((self.cache_dir / niche).glob("*.jpg"))
        if len(local_photos) >= 20:
            # Pick based on mood/exposure matching
            return self._pick_best_local(niche, mood)
        
        # Step 2: Try stock APIs
        photo = await self._fetch_from_stock_apis(niche, color_hint, orientation)
        if photo:
            saved = await self._download_and_cache(photo, niche)
            return saved
        
        # Step 3: AI generate (for niches where stock is insufficient)
        photo_path = await self._ai_generate(niche, business_name, mood)
        return photo_path
    
    async def _fetch_from_stock_apis(self, niche, color, orientation):
        """Try Pixabay → Pexels → Openverse in order."""
        query = self._build_query(niche)
        
        # Pixabay (best filters, highest rate limit)
        if pixabay_key := os.getenv("PIXABAY_API_KEY"):
            results = await self._search_pixabay(query, niche, color, orientation)
            if results:
                return results[0]
        
        # Pexels (good quality, no attribution)
        if pexels_key := os.getenv("PEXELS_API_KEY"):
            results = await self._search_pexels(query, orientation)
            if results:
                return results[0]
        
        # Openverse (no key needed, has Arabic content)
        results = await self._search_openverse(query)
        if results:
            return results[0]
        
        return None
    
    async def _ai_generate(self, niche, business_name, mood):
        """Generate with FLUX schnell (Apache 2.0, 4 steps, fast)."""
        from .ai_generator import generate_flux_image
        prompt = self._build_saudi_prompt(niche, mood)
        image = generate_flux_image(prompt)
        path = f"photos/{niche}/ai_{hashlib.md5(prompt.encode()).hexdigest()[:8]}.png"
        image.save(self.public_dir / path)
        return path
    
    def _build_query(self, niche: str) -> str:
        """Build search query optimized for Saudi/Arabic content."""
        queries = {
            "restaurants": "restaurant interior dining Middle Eastern",
            "cafes": "coffee shop interior modern",
            "barbershops": "barbershop interior modern",
            "salons": "beauty salon interior luxury",
            "clinics": "medical clinic interior modern",
            "perfumes": "perfume bottle luxury display",
            "fashion": "fashion boutique clothing rack",
            "real_estate": "modern villa exterior luxury",
            # ... map all 21 niches
        }
        return queries.get(niche, niche)
    
    def _build_saudi_prompt(self, niche: str, mood: str) -> str:
        """Build a Saudi-specific AI generation prompt."""
        prompts = {
            "restaurants": f"Professional photo of a modern Saudi restaurant "
                          f"interior, elegant Arabian decor, {mood} mood, "
                          f"warm lighting, date palms, high quality, 4k",
            "barbershops": f"Modern Saudi barbershop interior, Middle Eastern "
                          f"man in thobe getting a haircut, professional setting, "
                          f"{mood} mood, clean modern design",
            # ... all 21 niches
        }
        return prompts.get(niche, f"Professional photo of a {niche.replace('_', ' ')}, {mood} mood, high quality")
```

### 4.4 — Remotion Integration (TypeScript side)

The existing `resolvePhoto()` function in `helpers.tsx` already handles
path resolution via `staticFile()`. The only change needed:

```typescript
// BEFORE (hardcoded):
// pipeline_v3.py sets: "photoPath": "photos/restaurants.jpg"
// → resolvePhoto("photos/restaurants.jpg") → staticFile("photos/restaurants.jpg")

// AFTER (dynamic):
// pipeline_v3.py sets: "photoPath": "photos/restaurants/ai_a1b2c3d4.png"
// → resolvePhoto("photos/restaurants/ai_a1b2c3d4.png") → staticFile(...)
// No Remotion code changes needed! Just organize files in subdirectories.
```

The `DynamicComposer.tsx` and `NuhootPost.tsx` components already accept
any photo path string. The pipeline just needs to pass unique paths instead
of the single hardcoded one.

---

## PART 5: RECOMMENDED APPROACH

### 🏆 Best Quality at Zero Cost — The Recommended Stack

```
┌─────────────────────────────────────────────────────────┐
│                   NUHOOT IMAGE PIPELINE                  │
│                                                          │
│  1. PHOTO SELECTION (Python service)                     │
│     ├─ Openverse API (free, no key, Arabic content)     │
│     ├─ Pixabay API (free, best filters, 100/min)        │
│     └─ Pexels API (free, good quality, 200/hr)         │
│         ↓ (if stock insufficient or Saudi-specific needed)│
│                                                          │
│  2. AI GENERATION (when needed)                          │
│     ├─ FLUX.1-schnell (Apache 2.0, 4 steps, fastest)    │
│     └─ SDXL fallback (OpenRAIL++, more ControlNet opts) │
│         ↓                                                  │
│  3. POST-PROCESSING PIPELINE                              │
│     ├─ Real-ESRGAN (upscale 2× for print quality)       │
│     ├─ GFPGAN (fix/enhance faces)                       │
│     └─ rembg (background removal for compositing)       │
│         ↓                                                  │
│  4. COMPOSITING (Remotion handles in-render)             │
│     └→ PhotoSingle/PhotoGrid/PhotoMosaic with any src  │
└─────────────────────────────────────────────────────────┘
```

### Detailed Recommendation Breakdown

**Layer 1 — Stock Photo Aggregation (first choice, zero compute):**

1. **Openverse** — Primary source for Saudi/Arabic content. No API key needed.
   Real Flickr photos of actual Saudi locations. Cache aggressively (the 200/day
   limit means pre-download batches during off-hours). Filter by `license_type=commercial`
   to ensure usable results.

2. **Pixabay** — Primary source for generic niche photos. Best category/color
   filters of any API. Use `category=food` for restaurants, `category=health` for
   clinics, etc. 100 req/min is the highest rate limit — use for bulk fetching.
   Register for instant API key.

3. **Pexels** — Supplementary source. Best raw photo quality after Unsplash.
   200 req/hour. Instant API key. Use when Pixabay/Openverse return insufficient
   results.

**⚠️ Skip Unsplash** — The 50 req/hour demo limit and multi-day approval process
for production makes it impractical for an automated system. The quality is
excellent but the friction is too high for a non-developer user.

**Layer 2 — AI Generation (when stock photos lack Saudi specificity):**

1. **FLUX.1-schnell** (Apache 2.0) — Primary AI generator.
   - 4 inference steps = ~2s per image
   - Best open model quality
   - Apache 2.0 = no license restrictions
   - Can run on 8GB VRAM with NF4 quantization
   - Use for: Saudi people, Saudi interiors, culturally-specific scenes

2. **SDXL** (OpenRAIL++-M) — Fallback + ControlNet use cases.
   - Better ControlNet ecosystem (OpenPose, Canny, Depth)
   - Better inpainting support
   - Use when: pose control needed, inpainting a person into a scene,
     or FLUX unavailable

3. **ControlNet** — For pose-controlled generation and inpainting.
   - Generate a Saudi person in a specific pose
   - Inpaint Saudi people into existing stock photos
   - Transform Western stock photos into Saudi-localized versions

**Layer 3 — Post-Processing (always apply):**

1. **Real-ESRGAN** — Upscale all photos to minimum 2048×2048.
   Essential for Openverse Flickr photos (often 1024×697).
   BSD-3 license, GPU accelerated.

2. **GFPGAN** — Enhance faces in all photos containing people.
   Fixes AI artifacts, improves low-res stock faces.
   Apache 2.0 license. Can be chained with Real-ESRGAN
   (pass upsampler as `bg_upsampler`).

3. **rembg** — Remove backgrounds for compositing.
   MIT license. Use when:
   - Adding an AI-generated Saudi person onto a stock background
   - Creating transparent PNGs for PhotoCircle/PhotoArch components
   - Isolating product photos from cluttered backgrounds

### Cost Analysis

| Component | Software Cost | Hardware Cost | Per-Image Cost |
|---|---|---|---|
| Openverse API | $0 | $0 (existing server) | $0 |
| Pixabay API | $0 | $0 | $0 |
| Pexels API | $0 | $0 | $0 |
| FLUX.1-schnell | $0 (Apache 2.0) | GPU instance (~$0.50/hr on-demand) | ~$0.001/img |
| SDXL | $0 (OpenRAIL++) | GPU instance (~$0.50/hr on-demand) | ~$0.003/img |
| Real-ESRGAN | $0 (BSD-3) | Same GPU | ~$0.0001/img |
| GFPGAN | $0 (Apache 2.0) | Same GPU | ~$0.0001/img |
| rembg | $0 (MIT) | Same GPU | ~$0.0001/img |

**Total per image: ~$0.001-0.004** (essentially free if GPU is already provisioned)

**Or completely $0** if running on the existing Nuhoot server with a GPU.

### Implementation Priority (for non-developer user)

**Phase 1 — Immediate (no GPU needed):**
- Add Pixabay + Pexels + Openverse API keys to `.env`
- Build `photo_selector.py` service (stock API aggregation)
- Pre-download 50+ photos per niche during off-hours
- Organize into `remotion/public/photos/{niche}/` subdirectories
- Update `pipeline_v3.py` to use dynamic paths

**Phase 2 — Medium term (needs GPU):**
- Deploy FLUX.1-schnell with diffusers on a GPU instance
- Generate Saudi-specific photos for niches where stock is insufficient
- Add Real-ESRGAN upscaling for all photos
- Add GFPGAN face enhancement for people photos

**Phase 3 — Advanced (full compositing):**
- Add ControlNet for pose-controlled generation
- Add inpainting pipeline (add Saudi people to existing scenes)
- Add rembg background removal for compositing
- Build automated quality scoring (OpenCV luminance/exposure analysis)

### Key Decisions

1. **Why not Unsplash?** — Approval process is a blocker for a non-developer.
   Pexels gives instant access with comparable quality at 200/hr.

2. **Why FLUX schnell over SDXL as primary?** — Apache 2.0 vs OpenRAIL++,
   4 steps vs 30 steps (8× faster), better quality. SDXL is the fallback
   only because of its superior ControlNet ecosystem.

3. **Why Openverse first for Arabic content?** — It's the only API with
   real Saudi photos from real Saudi photographers. No other API has
   authentic "kabsa" or "ALBAIK" or "Riyadh at night" results.

4. **Why all three post-processing tools?** — They solve different problems:
   Real-ESRGAN fixes resolution, GFPGAN fixes faces, rembg enables compositing.
   They chain together: upscale → enhance faces → remove background.

5. **No Remotion changes needed** — The existing `resolvePhoto()` → `staticFile()`
   architecture already supports any path. The only change is in the Python
   pipeline: pass unique photo paths instead of the hardcoded single path.

---

## Appendix A — Complete API Key Registration Links

| API | Registration URL | Key Type | Wait Time |
|---|---|---|---|
| Openverse | https://openverse.org/accounts/signup/ | OAuth2 token | Instant |
| Pixabay | https://pixabay.com/accounts/register/ | API key | Instant |
| Pexels | https://www.pexels.com/api/new/ | API key | Instant |
| Unsplash | https://unsplash.com/oauth/applications/new | Access key | Instant (demo) / Days (prod) |

## Appendix B — Environment Variables to Add

```env
# === Stock Photo APIs ===
PIXABAY_API_KEY=your_pixabay_key
PEXELS_API_KEY=your_pexels_key
OPENVERSE_API_TOKEN=optional_for_higher_limits

# === AI Image Generation ===
AI_IMAGE_MODEL=flux-schnell          # or sdxl
AI_IMAGE_DEVICE=cuda                  # or cpu
AI_IMAGE_VRAM_OPTIMIZATION=nf4       # for low VRAM
SDXL_MODEL_PATH=stabilityai/stable-diffusion-xl-base-1.0
FLUX_MODEL_PATH=black-forest-labs/FLUX.1-schnell

# === Post-Processing ===
REMBG_MODEL=isnet                    # isnet (best) or u2net (fast)
REALESRGAN_SCALE=2                   # 2x or 4x
GFPGAN_VERSION=1.4                   # 1.3 or 1.4
```

## Appendix C — VRAM Requirements Summary

| Configuration | VRAM Needed | What it runs |
|---|---|---|
| Minimum (stock APIs only) | 0GB (CPU only) | Openverse + Pixabay + Pexels |
| Light AI (Kandinsky) | 4GB | Kandinsky 2.2 + rembg (CPU) |
| Standard AI (SDXL) | 8GB | SDXL + Real-ESRGAN + GFPGAN + rembg |
| Optimal AI (FLUX schnell) | 12GB | FLUX schnell (NF4) + all post-processing |
| Full (FLUX + ControlNet) | 24GB | FLUX + ControlNet + inpainting + all tools |

## Appendix D — Existing Nuhoot Niches (21)

```
auto_shops, bakeries, barbershops, cafes, car_wash, cleaning,
clinics, dentists, dermatology, event_halls, fashion, gyms,
hvac_ac, law_firms, perfumes, pharmacies, real_estate,
restaurants, salons, spas, training_centers
```

Each currently has 10 photos in `/assets/photos/{niche}/` (210 total) but
only 1 is exposed to Remotion via `/remotion/public/photos/{nicche}.jpg`.

**Gender consideration (from pipeline_v3.py):**
- Male niches: `barbershops, gyms, auto_shops`
- Female niches: `salons, spas, dermatology, fashion`
- This should inform AI generation prompts (gender of people in generated images)
