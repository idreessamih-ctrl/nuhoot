"""
Procedural Background Generator — Cairo + Perlin noise.

Generates deterministic, seed-based luxury backgrounds:
- Warm gold luxury (organic Perlin noise → gold gradients)
- Cool platinum (geometric patterns + silver tones)
- Monochrome gold accent (minimal texture + single gold glow)

Same seed = same background. No AI randomness. Fully reproducible.

License: MIT (Cairo is LGPL, noise is MIT)
"""

import cairo
import noise as perlin_noise
import math
import os
import random
from typing import List, Tuple


class BackgroundGenerator:
    """Generates procedural luxury backgrounds using Cairo + Perlin noise."""

    def __init__(self, width: int = 1080, height: int = 1080):
        self.width = width
        self.height = height

    def generate(
        self,
        style: str,
        bg_colors: List[Tuple[float, float, float]],
        seed: int,
        output_path: str,
    ) -> str:
        """Generate a procedural background image.

        Args:
            style: Background style ('warm_gold_luxury', 'cool_platinum', 'monochrome_gold')
            bg_colors: List of RGB tuples (0-1) for the color palette
            seed: Deterministic seed for reproducibility
            output_path: Where to save the PNG

        Returns:
            Path to the generated background image
        """
        random.seed(seed)

        if style == "warm_gold_luxury":
            self._generate_warm_gold(bg_colors, seed, output_path)
        elif style == "cool_platinum":
            self._generate_cool_platinum(bg_colors, seed, output_path)
        elif style == "monochrome_gold":
            self._generate_monochrome_gold(bg_colors, seed, output_path)
        else:
            self._generate_warm_gold(bg_colors, seed, output_path)

        return output_path

    def _create_surface(self) -> Tuple[cairo.ImageSurface, cairo.Context]:
        """Create a Cairo surface and context."""
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        ctx = cairo.Context(surface)
        return surface, ctx

    def _perlin_value(self, x: float, y: float, seed: int, octaves: int = 4) -> float:
        """Get Perlin noise value at (x, y) with given seed."""
        return perlin_noise.pnoise2(
            x / 100.0,
            y / 100.0,
            octaves=octaves,
            persistence=0.5,
            lacunarity=2.0,
            repeatx=self.width,
            repeaty=self.height,
            base=seed % 255,
        )

    def _generate_warm_gold(
        self,
        colors: List[Tuple[float, float, float]],
        seed: int,
        output_path: str,
    ):
        """Generate warm gold luxury background with Perlin noise texture."""
        surface, ctx = self._create_surface()

        # Base fill — deepest color
        c0 = colors[0]
        ctx.set_source_rgb(c0[0], c0[1], c0[2])
        ctx.rectangle(0, 0, self.width, self.height)
        ctx.fill()

        # Perlin noise texture — paint in 4x4 blocks for performance
        step = 4
        gold = (0.83, 0.69, 0.22)  # #D4AF37 in 0-1
        for y in range(0, self.height, step):
            for x in range(0, self.width, step):
                n = self._perlin_value(x, y, seed)
                # Normalize 0-1
                intensity = (n + 1) / 2
                # Only show gold where noise is above threshold
                if intensity > 0.55:
                    alpha = (intensity - 0.55) / 0.45  # 0-1 within the high range
                    alpha = min(alpha * 0.35, 0.35)  # Cap at 35% opacity
                    ctx.set_source_rgba(gold[0], gold[1], gold[2], alpha)
                    ctx.rectangle(x, y, step, step)
                    ctx.fill()

        # Radial gradient — atmospheric glow from upper center
        glow_x = self.width * 0.5
        glow_y = self.height * 0.25
        glow_r = self.width * 0.6
        pat = cairo.RadialGradient(glow_x, glow_y, 0, glow_x, glow_y, glow_r)
        pat.add_color_stop_rgba(0, 0.83, 0.69, 0.22, 0.08)  # Gold glow center
        pat.add_color_stop_rgba(0.5, 0.5, 0.35, 0.1, 0.03)
        pat.add_color_stop_rgba(1, 0, 0, 0, 0)
        ctx.set_source(pat)
        ctx.rectangle(0, 0, self.width, self.height)
        ctx.fill()

        # Bottom darkening gradient for text legibility
        pat2 = cairo.LinearGradient(0, self.height * 0.4, 0, self.height)
        pat2.add_color_stop_rgba(0, 0, 0, 0, 0)
        pat2.add_color_stop_rgba(0.5, 0.02, 0.01, 0.0, 0.4)
        pat2.add_color_stop_rgba(1, 0.0, 0.0, 0.0, 0.85)
        ctx.set_source(pat2)
        ctx.rectangle(0, 0, self.width, self.height)
        ctx.fill()

        # Vignette
        self._draw_vignette(ctx, intensity=0.6)

        # Islamic geometric pattern — subtle overlay
        self._draw_islamic_pattern(ctx, alpha=0.025, color=(0.83, 0.69, 0.22))

        # Film grain
        self._draw_film_grain(ctx, seed=seed, intensity=0.04)

        surface.write_to_png(output_path)
        surface.finish()

    def _generate_cool_platinum(
        self,
        colors: List[Tuple[float, float, float]],
        seed: int,
        output_path: str,
    ):
        """Generate cool platinum background with geometric patterns."""
        surface, ctx = self._create_surface()

        # Base fill
        c0 = colors[0]
        ctx.set_source_rgb(c0[0], c0[1], c0[2])
        ctx.rectangle(0, 0, self.width, self.height)
        ctx.fill()

        # Perlin noise — silver/platinum tones
        step = 4
        silver = (0.85, 0.88, 0.95)
        for y in range(0, self.height, step):
            for x in range(0, self.width, step):
                n = self._perlin_value(x, y, seed + 100)
                intensity = (n + 1) / 2
                if intensity > 0.6:
                    alpha = (intensity - 0.6) / 0.4 * 0.2
                    ctx.set_source_rgba(silver[0], silver[1], silver[2], alpha)
                    ctx.rectangle(x, y, step, step)
                    ctx.fill()

        # Radial glow — cool blue
        glow_x = self.width * 0.5
        glow_y = self.height * 0.3
        glow_r = self.width * 0.5
        pat = cairo.RadialGradient(glow_x, glow_y, 0, glow_x, glow_y, glow_r)
        pat.add_color_stop_rgba(0, 0.4, 0.5, 0.8, 0.06)
        pat.add_color_stop_rgba(1, 0, 0, 0, 0)
        ctx.set_source(pat)
        ctx.rectangle(0, 0, self.width, self.height)
        ctx.fill()

        # Bottom fade
        pat2 = cairo.LinearGradient(0, self.height * 0.5, 0, self.height)
        pat2.add_color_stop_rgba(0, 0, 0, 0, 0)
        pat2.add_color_stop_rgba(1, 0.02, 0.03, 0.05, 0.9)
        ctx.set_source(pat2)
        ctx.rectangle(0, 0, self.width, self.height)
        ctx.fill()

        # Geometric pattern — hexagonal
        self._draw_hexagonal_pattern(ctx, alpha=0.02, color=(0.7, 0.8, 1.0))

        # Vignette
        self._draw_vignette(ctx, intensity=0.55)

        # Film grain
        self._draw_film_grain(ctx, seed=seed + 50, intensity=0.035)

        surface.write_to_png(output_path)
        surface.finish()

    def _generate_monochrome_gold(
        self,
        colors: List[Tuple[float, float, float]],
        seed: int,
        output_path: str,
    ):
        """Generate minimal monochrome background with gold accent."""
        surface, ctx = self._create_surface()

        # Pure dark base
        c0 = colors[0]
        ctx.set_source_rgb(c0[0], c0[1], c0[2])
        ctx.rectangle(0, 0, self.width, self.height)
        ctx.fill()

        # Subtle Perlin texture — very faint
        step = 4
        for y in range(0, self.height, step):
            for x in range(0, self.width, step):
                n = self._perlin_value(x, y, seed + 200)
                intensity = (n + 1) / 2
                if intensity > 0.7:
                    alpha = (intensity - 0.7) / 0.3 * 0.08
                    ctx.set_source_rgba(0.15, 0.15, 0.15, alpha)
                    ctx.rectangle(x, y, step, step)
                    ctx.fill()

        # Single gold radial glow — center
        glow_x = self.width * 0.5
        glow_y = self.height * 0.4
        glow_r = self.width * 0.35
        pat = cairo.RadialGradient(glow_x, glow_y, 0, glow_x, glow_y, glow_r)
        pat.add_color_stop_rgba(0, 0.83, 0.69, 0.22, 0.06)
        pat.add_color_stop_rgba(0.5, 0.5, 0.4, 0.1, 0.02)
        pat.add_color_stop_rgba(1, 0, 0, 0, 0)
        ctx.set_source(pat)
        ctx.rectangle(0, 0, self.width, self.height)
        ctx.fill()

        # Subtle gold ring (concentric)
        for i in range(3):
            r = self.width * (0.3 + i * 0.15)
            ctx.set_source_rgba(0.83, 0.69, 0.22, 0.015)
            ctx.set_line_width(0.5)
            ctx.arc(glow_x, glow_y, r, 0, 2 * math.pi)
            ctx.stroke()

        # Vignette
        self._draw_vignette(ctx, intensity=0.5)

        # Film grain
        self._draw_film_grain(ctx, seed=seed + 100, intensity=0.03)

        surface.write_to_png(output_path)
        surface.finish()

    def _draw_vignette(self, ctx: cairo.Context, intensity: float = 0.6):
        """Draw a radial vignette."""
        pat = cairo.RadialGradient(
            self.width / 2, self.height / 2, self.width * 0.2,
            self.width / 2, self.height / 2, self.width * 0.7,
        )
        pat.add_color_stop_rgba(0, 0, 0, 0, 0)
        pat.add_color_stop_rgba(0.5, 0, 0, 0, intensity * 0.3)
        pat.add_color_stop_rgba(1, 0, 0, 0, intensity)
        ctx.set_source(pat)
        ctx.rectangle(0, 0, self.width, self.height)
        ctx.fill()

    def _draw_islamic_pattern(self, ctx: cairo.Context, alpha: float = 0.025, color=(0.83, 0.69, 0.22)):
        """Draw a subtle Islamic geometric tessellation pattern."""
        ctx.set_source_rgba(color[0], color[1], color[2], alpha)
        ctx.set_line_width(0.5)

        spacing = 80
        for y in range(0, self.height + spacing, spacing):
            for x in range(0, self.width + spacing, spacing):
                # 6-pointed star
                cx, cy = x, y
                for angle_offset in [0, 60, 120]:
                    angle = math.radians(angle_offset)
                    x1 = cx + 40 * math.cos(angle)
                    y1 = cy + 40 * math.sin(angle)
                    x2 = cx + 40 * math.cos(angle + math.pi / 3)
                    y2 = cy + 40 * math.sin(angle + math.pi / 3)
                    ctx.move_to(x1, y1)
                    ctx.line_to(x2, y2)
                    ctx.stroke()

    def _draw_hexagonal_pattern(self, ctx: cairo.Context, alpha: float = 0.02, color=(0.7, 0.8, 1.0)):
        """Draw a subtle hexagonal pattern."""
        ctx.set_source_rgba(color[0], color[1], color[2], alpha)
        ctx.set_line_width(0.5)

        hex_size = 50
        hex_w = hex_size * 2
        hex_h = hex_size * math.sqrt(3)

        for row in range(-1, int(self.height / hex_h) + 2):
            for col in range(-1, int(self.width / (hex_w * 1.5)) + 2):
                cx = col * hex_w * 1.5
                cy = row * hex_h + (hex_h / 2 if col % 2 else 0)

                ctx.move_to(cx + hex_size, cy)
                for i in range(5):
                    angle = math.radians(60 * (i + 1))
                    ctx.line_to(cx + hex_size * math.cos(angle), cy + hex_size * math.sin(angle))
                ctx.close_path()
                ctx.stroke()

    def _draw_film_grain(self, ctx: cairo.Context, seed: int, intensity: float = 0.04):
        """Draw random film grain noise."""
        rng = random.Random(seed)
        step = 2  # 2x2 pixel blocks for finer grain

        for y in range(0, self.height, step):
            for x in range(0, self.width, step):
                val = rng.random()
                if val > 0.5:
                    alpha = (val - 0.5) * 2 * intensity
                    ctx.set_source_rgba(1, 1, 1, alpha)
                else:
                    alpha = (0.5 - val) * 2 * intensity
                    ctx.set_source_rgba(0, 0, 0, alpha)
                ctx.rectangle(x, y, step, step)
                ctx.fill()
