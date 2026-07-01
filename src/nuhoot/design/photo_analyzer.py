"""ORACLE Photo Intelligence — analyzes business photos and selects the right layout archetype."""

import cv2
import numpy as np
from PIL import Image
from dataclasses import dataclass, field
from typing import Optional
import os


@dataclass
class PhotoProfile:
    """Complete analysis of a business photo."""
    path: str
    width: int
    height: int
    orientation: str  # landscape, portrait, square
    content_type: str  # food_closeup, interior, dining_scene, exterior, generic
    focal_x: float  # 0..1
    focal_y: float  # 0..1
    object_position: str  # CSS object-position value
    luminance: float  # 0..1
    exposure_class: str  # dark, mid, bright
    safest_text_edge: str  # top, bottom, left, right
    dominant_color: str  # hex
    is_warm: bool
    scrim_strong: float  # 0.80..0.97
    scrim_mid: float
    archetype: str  # A, B, C, D
    card_w: str  # CSS px for Archetype C
    card_h: str
    # Claude Blueprint Step 2: Image-first design fields
    composition: str = ""  # left_heavy, right_heavy, centered, minimal
    lighting: str = ""  # natural, dramatic, soft, clinical
    mood: str = ""  # dramatic, serene, energetic, sophisticated
    recommended_template: int = 0  # Template ID 1-15
    text_position: str = "right"  # right, left, bottom, center


def _simple_saliency(img: np.ndarray) -> np.ndarray:
    """Spectral residual saliency without opencv-contrib. Returns 0..1 float map."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    h, w = gray.shape
    # Downsample for speed if large
    scale = 1.0
    if max(h, w) > 400:
        scale = 400.0 / max(h, w)
        gray = cv2.resize(gray, (int(w * scale), int(h * scale)))
        h, w = gray.shape

    # FFT-based spectral residual
    fft = np.fft.fft2(gray)
    mag = np.abs(fft)
    phase = np.angle(fft)
    log_mag = np.log(mag + 1e-6)
    # Smooth the log magnitude (average filter)
    kernel = np.ones((3, 3), np.float32) / 9.0
    avg = cv2.filter2D(log_mag, -1, kernel)
    residual = log_mag - avg
    # Reconstruct
    new_fft = np.exp(residual) * np.exp(1j * phase)
    smap = np.abs(np.fft.ifft2(new_fft))
    # Gaussian blur to smooth
    smap = cv2.GaussianBlur(smap, (9, 9), 0)
    # Normalize 0..1
    mn, mx = smap.min(), smap.max()
    smap = (smap - mn) / (mx - mn + 1e-6)
    return smap


def _classify_orientation(w: int, h: int) -> str:
    ar = w / h
    if ar >= 1.20:
        return "landscape"
    if ar <= 0.83:
        return "portrait"
    return "square"


def _classify_content(img: np.ndarray) -> str:
    """Lightweight heuristic content classifier."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 80, 160)
    edge_density = edges.mean() / 255.0

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 80,
                           minLineLength=img.shape[1] * 0.25, maxLineGap=10)
    long_lines = 0 if lines is None else len(lines)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    saturation = hsv[:, :, 1].mean() / 255.0
    # Warm pixels: hue 0-40 or 160-180
    warm_mask = ((hsv[:, :, 0] <= 40) | (hsv[:, :, 0] >= 160)) & (hsv[:, :, 1] > 40)
    warmth = warm_mask.mean()

    # Center mass concentration via simple spectral residual saliency
    smap = _simple_saliency(img)
    h, w = smap.shape[:2]
    center_region = smap[int(h * 0.25):int(h * 0.75), int(w * 0.25):int(w * 0.75)]
    center_mass = center_region.sum() / (smap.sum() + 1e-6)

    if edge_density > 0.12 and saturation > 0.35 and center_mass > 0.40 and long_lines < 6:
        return "food_closeup"
    if long_lines >= 8 and saturation < 0.50:
        return "interior"
    if warmth > 0.25 and center_mass < 0.55 and long_lines >= 4:
        return "dining_scene"
    return "generic"


def _detect_focal_point(img: np.ndarray) -> tuple:
    """Returns (focal_x, focal_y, object_position) using simple saliency."""
    smap = _simple_saliency(img)
    smap = (smap * 255).astype("uint8")

    M = cv2.moments(smap)
    cx = M["m10"] / (M["m00"] + 1e-6)
    cy = M["m01"] / (M["m00"] + 1e-6)

    h, w = smap.shape[:2]
    fx = cx / w
    fy = cy / h

    # Clamp to reasonable range
    fx = max(0.15, min(0.85, fx))
    fy = max(0.15, min(0.85, fy))

    obj_pos = f"{round(fx * 100)}% {round(fy * 100)}%"
    return fx, fy, obj_pos


def _analyze_exposure(img: np.ndarray) -> tuple:
    """Returns (luminance, exposure_class, safest_text_edge, scrim_strong, scrim_mid)."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    L = gray.mean() / 255.0

    h, w = gray.shape
    edges = {
        "top": gray[:int(h * 0.25), :].mean() / 255,
        "bottom": gray[int(h * 0.75):, :].mean() / 255,
        "left": gray[:, :int(w * 0.25)].mean() / 255,
        "right": gray[:, int(w * 0.75):].mean() / 255,
    }
    safest = min(edges, key=edges.get)
    cls = "dark" if L < 0.35 else "bright" if L > 0.65 else "mid"

    strong = max(0.80, min(0.97, 0.78 + (L - 0.35) * 0.6))
    mid = max(0.62, min(0.88, strong - 0.12))

    return L, cls, safest, strong, mid


def _extract_dominant_color(img: np.ndarray) -> tuple:
    """Returns (hex_color, is_warm)."""
    small = cv2.resize(img, (60, 60))
    data = small.reshape(-1, 3).astype("float32")
    _, labels, centers = cv2.kmeans(
        data, 3, None,
        (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 15, 1.0),
        3, cv2.KMEANS_PP_CENTERS)
    counts = np.bincount(labels.flatten())
    dominant = centers[np.argmax(counts)]
    b, g, r = int(dominant[0]), int(dominant[1]), int(dominant[2])
    hex_color = f"#{r:02X}{g:02X}{b:02X}"

    hsv = cv2.cvtColor(np.array([[[b, g, r]]], dtype=np.uint8), cv2.COLOR_BGR2HSV)[0][0]
    is_warm = 0 <= hsv[0] <= 40 or 160 <= hsv[0] <= 180
    return hex_color, is_warm


def _select_archetype(orientation: str, content_type: str) -> tuple:
    """Returns (archetype_letter, card_w, card_h)."""
    if orientation == "portrait":
        if content_type == "food_closeup":
            return "C", "560px", "700px"
        return "B", None, None
    if orientation == "landscape":
        return "A", None, None
    # Square
    if content_type == "food_closeup":
        return "C", "620px", "620px"
    return "D", None, None


def _classify_composition(focal_x: float, focal_y: float, smap: np.ndarray) -> str:
    """Classify photo composition for text placement (Claude Blueprint Step 2)."""
    h, w = smap.shape[:2]
    # Check density in quadrants
    q_left = smap[:, :int(w * 0.33)].sum()
    q_right = smap[:, int(w * 0.67):].sum()
    q_center = smap[int(h * 0.25):int(h * 0.75), int(w * 0.33):int(w * 0.67)].sum()
    total = smap.sum() + 1e-6
    
    center_ratio = q_center / total
    left_ratio = q_left / total
    right_ratio = q_right / total
    
    if center_ratio > 0.45:
        return "centered"
    if left_ratio > right_ratio * 1.3:
        return "left_heavy"
    if right_ratio > left_ratio * 1.3:
        return "right_heavy"
    if center_ratio < 0.25 and left_ratio < 0.35 and right_ratio < 0.35:
        return "minimal"
    return "balanced"


def _classify_lighting(luminance: float, is_warm: bool, img: np.ndarray) -> str:
    """Classify lighting type (Claude Blueprint Step 2)."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Contrast = std dev of luminance
    contrast = float(gray.std()) / 255.0
    
    if luminance < 0.35 and contrast > 0.25:
        return "dramatic"
    if luminance > 0.65 and not is_warm:
        return "clinical"
    if luminance > 0.60 and contrast < 0.20:
        return "soft"
    return "natural"


def _classify_mood(luminance: float, contrast: float, saturation: float, is_warm: bool) -> str:
    """Classify emotional mood of photo (Claude Blueprint Step 2)."""
    if luminance < 0.35 and contrast > 0.25:
        return "dramatic"
    if luminance > 0.55 and saturation < 0.30 and is_warm:
        return "serene"
    if luminance > 0.50 and saturation > 0.40:
        return "energetic"
    return "sophisticated"


def _recommend_template(composition: str, lighting: str, mood: str, 
                         content_type: str) -> tuple:
    """Recommend best template + text position based on photo analysis.
    
    Returns (template_id, text_position)
    """
    # Template selection matrix
    if composition == "left_heavy":
        return 1, "right"  # T01 Vertical Split — text on right
    if composition == "right_heavy":
        return 1, "left"  # T01 Vertical Split — text on left (reversed)
    if composition == "centered":
        if mood == "dramatic":
            return 11, "bottom"  # T11 Cinematic
        return 10, "center"  # T10 Framed Float
    if composition == "minimal":
        if mood == "energetic":
            return 15, "center"  # T15 Neon Edge
        return 12, "center"  # T12 Glass Morphism
    # balanced
    if mood == "dramatic":
        return 11, "bottom"  # T11 Cinematic
    if mood == "serene":
        return 1, "right"  # T01 Vertical Split
    if mood == "energetic":
        return 15, "center"  # T15 Neon Edge
    if mood == "sophisticated":
        return 14, "right"  # T14 Magazine Cover
    return 1, "right"  # Default


def analyze_photo(path: str) -> PhotoProfile:
    """Complete photo analysis → PhotoProfile with archetype selection."""
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Cannot read image: {path}")

    h, w = img.shape[:2]
    orientation = _classify_orientation(w, h)
    content_type = _classify_content(img)
    fx, fy, obj_pos = _detect_focal_point(img)
    L, exp_cls, safest, scrim_s, scrim_m = _analyze_exposure(img)
    dom_color, is_warm = _extract_dominant_color(img)
    archetype, card_w, card_h = _select_archetype(orientation, content_type)
    
    # Claude Blueprint Step 2: Image-first analysis
    smap = _simple_saliency(img)
    composition = _classify_composition(fx, fy, smap)
    lighting = _classify_lighting(L, is_warm, img)
    
    # Compute contrast and saturation for mood
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contrast = float(gray.std()) / 255.0
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    saturation = float(hsv[:, :, 1].mean()) / 255.0
    mood = _classify_mood(L, contrast, saturation, is_warm)
    
    rec_template, text_pos = _recommend_template(composition, lighting, mood, content_type)

    return PhotoProfile(
        path=path, width=w, height=h, orientation=orientation,
        content_type=content_type, focal_x=fx, focal_y=fy,
        object_position=obj_pos, luminance=L, exposure_class=exp_cls,
        safest_text_edge=safest, dominant_color=dom_color, is_warm=is_warm,
        scrim_strong=round(scrim_s, 2), scrim_mid=round(scrim_m, 2),
        archetype=archetype,
        card_w=card_w or "", card_h=card_h or "",
        composition=composition, lighting=lighting, mood=mood,
        recommended_template=rec_template, text_position=text_pos,
    )
