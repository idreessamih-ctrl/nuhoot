"""
Quality Gate — Automated image quality assessment using OpenCV.

Checks:
1. Contrast (standard deviation of grayscale — higher = better)
2. Color harmony (k-means dominant colors + harmony scoring)
3. Composition balance (rule of thirds — visual weight distribution)
4. Text readability (contrast between text and background regions)

Score > 0.75 = PASS, else FAIL (trigger retry with different seed)

License: Apache-2.0 (OpenCV)
"""

import cv2
import numpy as np
from typing import Tuple, Dict
from sklearn.cluster import KMeans


class QualityGate:
    """Assesses rendered image quality using computer vision."""

    MIN_SCORE = 0.75

    def assess(self, image_path: str) -> Tuple[bool, Dict]:
        """Run all quality checks on an image.

        Claude Blueprint Step 4: Quality Gates
        - Text contrast >7:1 (WCAG AAA)
        - Whitespace >20%
        - Text area <35% of canvas
        - Brand colors within luxury ratios (<15% accent)

        Returns:
            (passed, scores_dict)
        """
        img = cv2.imread(image_path)
        if img is None:
            return False, {"error": "Could not read image"}

        scores = {}

        # 1. Contrast assessment
        scores["contrast"] = self._check_contrast(img)

        # 2. Color harmony
        scores["harmony"] = self._check_color_harmony(img)

        # 3. Composition balance
        scores["balance"] = self._check_composition_balance(img)

        # 4. Text readability (top vs bottom region contrast)
        scores["readability"] = self._check_text_readability(img)

        # Claude Blueprint: New luxury quality gates
        # 5. Text contrast ratio (WCAG)
        scores["text_contrast_ratio"] = self._check_text_contrast_ratio(img)

        # 6. Whitespace percentage
        scores["whitespace"] = self._check_whitespace(img)

        # 7. Text coverage (should be <35% of canvas)
        scores["text_coverage"] = self._check_text_coverage(img)

        # 8. Accent color ratio (should be <15%)
        scores["accent_ratio"] = self._check_accent_ratio(img)

        # Overall score — weighted average
        # Original checks: 60%, Claude luxury checks: 40%
        original = (
            scores["contrast"] * 0.25
            + scores["harmony"] * 0.25
            + scores["balance"] * 0.25
            + scores["readability"] * 0.25
        )
        luxury = (
            scores["text_contrast_ratio"] * 0.35
            + scores["whitespace"] * 0.25
            + scores["text_coverage"] * 0.20
            + scores["accent_ratio"] * 0.20
        )
        overall = original * 0.6 + luxury * 0.4
        scores["overall"] = round(overall, 3)

        return overall >= self.MIN_SCORE, scores

    def _check_text_contrast_ratio(self, img: np.ndarray) -> float:
        """Claude Blueprint: Text contrast >7:1 (WCAG AAA).
        
        Measures the contrast ratio between bright pixels (text) and 
        dark pixels (background) in the text region.
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        
        # Sample bottom 45% (where text usually is)
        text_region = gray[int(h * 0.55):, :]
        if text_region.size == 0:
            return 0.5
        
        # Bright pixels = text, dark pixels = background
        bright = text_region[text_region > 180]
        dark = text_region[text_region < 80]
        
        if len(bright) == 0 or len(dark) == 0:
            return 0.5  # Can't measure, assume ok
        
        # WCAG contrast ratio formula
        L_bright = (bright.mean() / 255.0 + 0.05) / 10
        L_dark = (dark.mean() / 255.0 + 0.05) / 10
        
        if L_dark < 0.01:
            L_dark = 0.01
        
        ratio = L_bright / L_dark
        # 7:1 = 1.0, 4.5:1 = 0.6, 3:1 = 0.4
        return min(ratio / 7.0, 1.0)

    def _check_whitespace(self, img: np.ndarray) -> float:
        """Claude Blueprint: Whitespace >20% of canvas.
        
        Measures percentage of very dark pixels (background/whitespace area).
        In dark luxury designs, empty dark areas = whitespace.
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Very dark pixels (background, empty space)
        dark_ratio = (gray < 30).sum() / gray.size
        # 20%+ = 1.0, 10% = 0.5, 5% = 0.25
        return min(dark_ratio / 0.20, 1.0)

    def _check_text_coverage(self, img: np.ndarray) -> float:
        """Claude Blueprint: Text should not exceed 35% of canvas.
        
        Measures percentage of bright (text) pixels.
        Lower coverage = better (more whitespace).
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Bright pixels = text/accents
        bright_ratio = (gray > 180).sum() / gray.size
        # <15% text = 1.0, 25% = 0.7, 35% = 0.3, >35% = 0
        if bright_ratio < 0.15:
            return 1.0
        if bright_ratio < 0.25:
            return 0.7
        if bright_ratio < 0.35:
            return 0.3
        return 0.0

    def _check_accent_ratio(self, img: np.ndarray) -> float:
        """Claude Blueprint: Accent colors should be <15% of design.
        
        Measures percentage of gold/accent colored pixels.
        """
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # Gold/warm accent pixels: hue 20-50, saturation >50
        gold_mask = ((hsv[:, :, 0] >= 15) & (hsv[:, :, 0] <= 55) & 
                     (hsv[:, :, 1] > 80))
        gold_ratio = gold_mask.sum() / hsv[:, :, 0].size
        # <10% = 1.0, 15% = 0.5, >20% = 0.0
        if gold_ratio < 0.10:
            return 1.0
        if gold_ratio < 0.15:
            return 0.5
        return 0.0

    def _check_contrast(self, img: np.ndarray) -> float:
        """Assess image contrast via grayscale standard deviation.

        Higher std = more contrast = better visual impact.
        Normalized to 0-1 scale (std of 50+ = 1.0).
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        std = gray.std()
        return min(std / 50.0, 1.0)

    def _check_color_harmony(self, img: np.ndarray) -> float:
        """Assess color harmony using k-means clustering.

        Extracts dominant colors and checks if they form a harmonious palette
        (analogous, complementary, or monochromatic).
        """
        # Downsample for speed
        h, w = img.shape[:2]
        if h > 200:
            scale = 200 / h
            small = cv2.resize(img, None, fx=scale, fy=scale)
        else:
            small = img

        # Convert to RGB and reshape for k-means
        rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
        pixels = rgb.reshape(-1, 3)

        # Get top 3 dominant colors
        kmeans = KMeans(n_clusters=3, n_init=3, random_state=42)
        kmeans.fit(pixels)
        colors = kmeans.cluster_centers_

        # Check harmony: colors should be close in hue (analogous)
        # or form a complementary pair
        hsv_colors = []
        for c in colors:
            r, g, b = c / 255.0
            h, s, v = self._rgb_to_hsv(r, g, b)
            hsv_colors.append((h, s, v))

        # Calculate hue spread (lower = more harmonious)
        hues = [c[0] for c in hsv_colors if c[1] > 0.1]  # Only consider saturated colors
        if len(hues) < 2:
            return 0.7  # Monochrome is harmonious

        hue_spreads = []
        for i in range(len(hues)):
            for j in range(i + 1, len(hues)):
                diff = abs(hues[i] - hues[j])
                hue_spreads.append(min(diff, 360 - diff))

        avg_spread = sum(hue_spreads) / len(hue_spreads)

        # Score: lower spread = higher harmony
        # Spread of 0-30 = excellent (1.0), 30-60 = good (0.8), 60-120 = okay (0.6)
        if avg_spread < 30:
            return 1.0
        elif avg_spread < 60:
            return 0.8
        elif avg_spread < 120:
            return 0.6
        else:
            return 0.4

    def _check_composition_balance(self, img: np.ndarray) -> float:
        """Assess visual balance using the rule of thirds.

        Divides image into 3x3 grid and checks if visual weight
        is distributed across zones (not all in one corner).
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        # Calculate visual weight (brightness) per zone
        zone_h, zone_w = h // 3, w // 3
        weights = []
        for i in range(3):
            for j in range(3):
                zone = gray[i * zone_h:(i + 1) * zone_h, j * zone_w:(j + 1) * zone_w]
                weights.append(zone.mean())

        weights = np.array(weights).reshape(3, 3)

        # Good balance = weights distributed across zones
        # Check if center zone has content (focal point)
        center_weight = weights[1, 1]

        # Check if corners aren't all empty or all full
        corner_weights = [weights[0, 0], weights[0, 2], weights[2, 0], weights[2, 2]]
        corner_std = np.std(corner_weights)

        # Score: center should have content, corners should vary (not flat)
        score = min(center_weight / 128.0, 1.0) * 0.5 + min(corner_std / 30.0, 1.0) * 0.5
        return score

    def _check_text_readability(self, img: np.ndarray) -> float:
        """Check if there's sufficient contrast between text and background.

        Samples the bottom 40% of the image (where text usually is)
        and checks contrast against the top 60% (where the photo is).
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        # Bottom region (text area)
        text_region = gray[int(h * 0.6):, :]
        text_mean = text_region.mean()
        text_std = text_region.std()

        # Top region (photo area)
        photo_region = gray[:int(h * 0.6), :]
        photo_mean = photo_region.mean()

        # Contrast between regions
        region_contrast = abs(text_mean - photo_mean) / 255.0

        # Internal contrast in text region (text vs background)
        text_contrast = text_std / 50.0

        # Score: need both inter-region contrast and internal text contrast
        score = min(region_contrast * 2, 1.0) * 0.4 + min(text_contrast, 1.0) * 0.6
        return score

    def _rgb_to_hsv(self, r: float, g: float, b: float) -> Tuple[float, float, float]:
        """Convert RGB (0-1) to HSV (H: 0-360, S: 0-1, V: 0-1)."""
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        diff = max_val - min_val

        if diff == 0:
            h = 0
        elif max_val == r:
            h = 60 * (((g - b) / diff) % 6)
        elif max_val == g:
            h = 60 * ((b - r) / diff + 2)
        else:
            h = 60 * ((r - g) / diff + 4)

        s = 0 if max_val == 0 else diff / max_val
        v = max_val

        return h, s, v
