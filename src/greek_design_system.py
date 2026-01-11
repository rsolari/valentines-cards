#!/usr/bin/env python3
"""
Greek Pottery Design System for Valentine's Cards

Inspired by ancient Greek black-figure and red-figure pottery,
featuring classic motifs like the meander (Greek key) pattern.

Card specs: 3.5" x 2.5" at 300 DPI = 1050 x 750 pixels
"""

import math
from PIL import Image, ImageDraw
from dataclasses import dataclass
from typing import Tuple, List, Optional
import random


# =============================================================================
# COLOR PALETTE - Greek Pottery
# =============================================================================

@dataclass
class GreekPalette:
    """
    Color palette inspired by ancient Greek pottery.

    Black-figure style: Black figures on terracotta background
    Red-figure style: Terracotta figures on black background
    """
    # Primary colors
    terracotta: str = "#CD6839"       # Main orange/red clay color
    black: str = "#1A1A1A"            # Pottery black (not pure black)

    # Variations for depth
    terracotta_light: str = "#E07B4A"  # Lighter terracotta for highlights
    terracotta_dark: str = "#A85430"   # Darker terracotta for shadows
    terracotta_pale: str = "#E8956A"   # Pale version for worn areas

    # Accent colors (used sparingly in Greek pottery)
    white: str = "#F5F0E6"            # Aged white/cream
    deep_red: str = "#8B2500"         # Deep red accent

    def as_rgb(self, color_name: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple."""
        hex_color = getattr(self, color_name)
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


# Default palette instance
PALETTE = GreekPalette()


# =============================================================================
# BORDER PATTERNS
# =============================================================================

def draw_greek_key_border(
    draw: ImageDraw,
    x: int, y: int,
    width: int, height: int,
    key_size: int = 20,
    fg_color: str = None,
    bg_color: str = None,
    direction: str = "horizontal"
):
    """
    Draw a Greek key (meander) pattern border.

    The meander is one of the most important symbols in Greek art,
    representing infinity, unity, and the eternal flow of life.

    Args:
        draw: PIL ImageDraw object
        x, y: Top-left corner position
        width, height: Dimensions of the border area
        key_size: Size of each key unit
        fg_color: Foreground (line) color
        bg_color: Background color
        direction: "horizontal" or "vertical"
    """
    fg = fg_color or PALETTE.black
    bg = bg_color or PALETTE.terracotta

    # Fill background
    draw.rectangle([x, y, x + width, y + height], fill=bg)

    line_width = max(2, key_size // 6)

    if direction == "horizontal":
        # Draw horizontal meander
        unit_width = key_size * 2
        num_units = width // unit_width + 1

        for i in range(num_units):
            ux = x + i * unit_width
            uy = y + height // 2 - key_size // 2

            # Draw one meander unit (simplified Greek key)
            # This creates the classic stepped spiral pattern
            points = [
                # Bottom horizontal line
                (ux, uy + key_size),
                (ux + key_size, uy + key_size),
                # Up
                (ux + key_size, uy + key_size // 2),
                # Left
                (ux + key_size // 2, uy + key_size // 2),
                # Up
                (ux + key_size // 2, uy),
                # Right to end
                (ux + unit_width, uy),
            ]

            # Draw as connected lines
            for j in range(len(points) - 1):
                draw.line([points[j], points[j + 1]], fill=fg, width=line_width)

            # Mirror pattern for second half
            points2 = [
                (ux + unit_width, uy),
                (ux + unit_width, uy + key_size // 2),
                (ux + key_size + key_size // 2, uy + key_size // 2),
                (ux + key_size + key_size // 2, uy + key_size),
                (ux + unit_width, uy + key_size),
            ]
            for j in range(len(points2) - 1):
                draw.line([points2[j], points2[j + 1]], fill=fg, width=line_width)

    # Draw border lines
    draw.line([(x, y), (x + width, y)], fill=fg, width=line_width)
    draw.line([(x, y + height), (x + width, y + height)], fill=fg, width=line_width)


def draw_triangle_border(
    draw: ImageDraw,
    x: int, y: int,
    width: int, height: int,
    triangle_width: int = 25,
    fg_color: str = None,
    bg_color: str = None,
    pointing: str = "down"
):
    """
    Draw a row of triangles (common Greek pottery border).

    Args:
        draw: PIL ImageDraw object
        x, y: Top-left corner position
        width, height: Dimensions of the border area
        triangle_width: Base width of each triangle
        fg_color: Triangle fill color
        bg_color: Background color
        pointing: "up" or "down"
    """
    fg = fg_color or PALETTE.black
    bg = bg_color or PALETTE.terracotta

    # Fill background
    draw.rectangle([x, y, x + width, y + height], fill=bg)

    num_triangles = width // triangle_width + 1

    for i in range(num_triangles):
        tx = x + i * triangle_width
        if pointing == "down":
            points = [
                (tx, y),
                (tx + triangle_width, y),
                (tx + triangle_width // 2, y + height)
            ]
        else:  # pointing up
            points = [
                (tx + triangle_width // 2, y),
                (tx, y + height),
                (tx + triangle_width, y + height)
            ]
        draw.polygon(points, fill=fg)


def draw_dot_border(
    draw: ImageDraw,
    x: int, y: int,
    width: int, height: int,
    dot_spacing: int = 15,
    dot_radius: int = 3,
    fg_color: str = None,
    bg_color: str = None
):
    """
    Draw a row of dots (simple Greek pottery border).
    """
    fg = fg_color or PALETTE.black
    bg = bg_color or PALETTE.terracotta

    # Fill background
    draw.rectangle([x, y, x + width, y + height], fill=bg)

    cy = y + height // 2
    num_dots = width // dot_spacing

    for i in range(num_dots + 1):
        cx = x + i * dot_spacing + dot_spacing // 2
        draw.ellipse(
            [cx - dot_radius, cy - dot_radius, cx + dot_radius, cy + dot_radius],
            fill=fg
        )


def draw_wave_border(
    draw: ImageDraw,
    x: int, y: int,
    width: int, height: int,
    wave_length: int = 30,
    fg_color: str = None,
    bg_color: str = None
):
    """
    Draw a wave/scroll pattern (running dog or Vitruvian scroll).
    """
    fg = fg_color or PALETTE.black
    bg = bg_color or PALETTE.terracotta

    # Fill background
    draw.rectangle([x, y, x + width, y + height], fill=bg)

    line_width = max(2, height // 8)
    cy = y + height // 2
    amplitude = height // 3

    # Draw wave using bezier-like curves
    points = []
    for px in range(x, x + width, 2):
        progress = (px - x) / wave_length
        py = cy + amplitude * math.sin(progress * 2 * math.pi)
        points.append((px, py))

    if len(points) > 1:
        draw.line(points, fill=fg, width=line_width)


# =============================================================================
# TEXTURE AND EFFECTS
# =============================================================================

def add_pottery_texture(image: Image, intensity: int = 15):
    """
    Add subtle speckle texture like aged pottery.
    """
    pixels = image.load()
    width, height = image.size

    for y in range(height):
        for x in range(width):
            if random.random() < 0.03:  # 3% of pixels get speckles
                r, g, b = pixels[x, y][:3]
                # Dark speckle
                factor = random.uniform(0.7, 0.9)
                pixels[x, y] = (
                    int(r * factor),
                    int(g * factor),
                    int(b * factor)
                )

    return image


# =============================================================================
# CARD TEMPLATE GENERATOR
# =============================================================================

def generate_greek_card_front(
    width: int = 1050,
    height: int = 750,
    border_width: int = 40,
    add_texture: bool = True
) -> Image:
    """
    Generate a card front with Greek pottery styling.

    Layout:
    - Outer triangle border
    - Greek key border
    - Inner dot border
    - Central area for minotaur art and text
    """
    img = Image.new('RGB', (width, height), PALETTE.terracotta)
    draw = ImageDraw.Draw(img)

    # Outer black border line
    draw.rectangle([0, 0, width-1, height-1], outline=PALETTE.black, width=3)

    # Top border - triangles pointing down
    draw_triangle_border(
        draw, border_width, 5,
        width - 2 * border_width, 30,
        triangle_width=22, pointing="down"
    )

    # Bottom border - triangles pointing up
    draw_triangle_border(
        draw, border_width, height - 35,
        width - 2 * border_width, 30,
        triangle_width=22, pointing="up"
    )

    # Greek key border below top triangles
    draw_greek_key_border(
        draw, border_width, 40,
        width - 2 * border_width, 35,
        key_size=15
    )

    # Greek key border above bottom triangles
    draw_greek_key_border(
        draw, border_width, height - 75,
        width - 2 * border_width, 35,
        key_size=15
    )

    # Left side decorative border (vertical dots)
    for i in range(10, height - 40, 20):
        draw.ellipse([12, i, 22, i + 10], fill=PALETTE.black)

    # Right side decorative border (vertical dots)
    for i in range(10, height - 40, 20):
        draw.ellipse([width - 22, i, width - 12, i + 10], fill=PALETTE.black)

    # Add texture
    if add_texture:
        img = add_pottery_texture(img)

    return img


def generate_greek_card_back(
    width: int = 1050,
    height: int = 750,
    border_width: int = 30
) -> Image:
    """
    Generate a card back template for the maze.
    Simpler borders to leave room for the maze.
    """
    img = Image.new('RGB', (width, height), PALETTE.terracotta)
    draw = ImageDraw.Draw(img)

    # Simple black border
    draw.rectangle([0, 0, width-1, height-1], outline=PALETTE.black, width=4)

    # Triangle borders only
    draw_triangle_border(
        draw, 10, 8,
        width - 20, 25,
        triangle_width=20, pointing="down"
    )

    draw_triangle_border(
        draw, 10, height - 33,
        width - 20, 25,
        triangle_width=20, pointing="up"
    )

    # Side dots
    for i in range(15, height - 35, 18):
        draw.ellipse([8, i, 16, i + 8], fill=PALETTE.black)
        draw.ellipse([width - 16, i, width - 8, i + 8], fill=PALETTE.black)

    return img


def main():
    import os

    output_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "templates")
    os.makedirs(output_dir, exist_ok=True)

    print("Greek Pottery Design System")
    print("=" * 40)
    print(f"Card size: 3.5\" x 2.5\" (1050 x 750 pixels at 300 DPI)")
    print()
    print("Color Palette:")
    print(f"  Terracotta: {PALETTE.terracotta}")
    print(f"  Black: {PALETTE.black}")
    print(f"  White: {PALETTE.white}")
    print()

    # Generate card front
    print("Generating card front template...")
    front = generate_greek_card_front()
    front_path = os.path.join(output_dir, "greek_card_front.png")
    front.save(front_path, dpi=(300, 300))
    print(f"Saved: {front_path}")

    # Generate card back
    print("Generating card back template...")
    back = generate_greek_card_back()
    back_path = os.path.join(output_dir, "greek_card_back.png")
    back.save(back_path, dpi=(300, 300))
    print(f"Saved: {back_path}")

    print()
    print("Templates generated!")
    print("The central area is ready for your minotaur pixel art.")


if __name__ == "__main__":
    main()
