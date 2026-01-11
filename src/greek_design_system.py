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
    line_width: int = 3
):
    """
    Draw an authentic Greek key (meander) pattern border.

    This creates the classic square-spiral meander pattern seen on
    ancient Greek pottery like white-ground lekythoi.

    The meander is one of the most important symbols in Greek art,
    representing infinity, unity, and the eternal flow of life.

    Args:
        draw: PIL ImageDraw object
        x, y: Top-left corner position
        width, height: Dimensions of the border area
        key_size: Size of each key unit (the square spiral)
        fg_color: Foreground (line) color
        bg_color: Background color
        line_width: Thickness of the lines
    """
    fg = fg_color or PALETTE.black
    bg = bg_color or PALETTE.terracotta

    # Fill background
    draw.rectangle([x, y, x + width, y + height], fill=bg)

    # Calculate dimensions
    unit_width = key_size
    margin_y = (height - key_size) // 2
    top_y = y + margin_y
    bottom_y = y + margin_y + key_size

    # Draw top and bottom border lines
    draw.line([(x, top_y), (x + width, top_y)], fill=fg, width=line_width)
    draw.line([(x, bottom_y), (x + width, bottom_y)], fill=fg, width=line_width)

    # Draw the meander pattern - authentic square spiral style
    # Each unit is a square spiral that hooks down then back up
    num_units = width // unit_width

    step = key_size // 4  # Size of each step in the spiral

    for i in range(num_units):
        ux = x + i * unit_width

        if i % 2 == 0:
            # Downward spiral (starts from top line)
            # Vertical down from top
            draw.line([(ux, top_y), (ux, bottom_y - step)], fill=fg, width=line_width)
            # Hook right
            draw.line([(ux, bottom_y - step), (ux + step * 3, bottom_y - step)], fill=fg, width=line_width)
            # Hook up
            draw.line([(ux + step * 3, bottom_y - step), (ux + step * 3, top_y + step)], fill=fg, width=line_width)
            # Hook left (inner)
            draw.line([(ux + step * 3, top_y + step), (ux + step, top_y + step)], fill=fg, width=line_width)
            # Down to center
            draw.line([(ux + step, top_y + step), (ux + step, bottom_y - step * 2)], fill=fg, width=line_width)
            # Right to inner
            draw.line([(ux + step, bottom_y - step * 2), (ux + step * 2, bottom_y - step * 2)], fill=fg, width=line_width)
            # Up to connect
            draw.line([(ux + step * 2, bottom_y - step * 2), (ux + step * 2, top_y + step * 2)], fill=fg, width=line_width)
        else:
            # Upward spiral (starts from bottom line)
            # Vertical up from bottom
            draw.line([(ux, bottom_y), (ux, top_y + step)], fill=fg, width=line_width)
            # Hook right
            draw.line([(ux, top_y + step), (ux + step * 3, top_y + step)], fill=fg, width=line_width)
            # Hook down
            draw.line([(ux + step * 3, top_y + step), (ux + step * 3, bottom_y - step)], fill=fg, width=line_width)
            # Hook left (inner)
            draw.line([(ux + step * 3, bottom_y - step), (ux + step, bottom_y - step)], fill=fg, width=line_width)
            # Up to center
            draw.line([(ux + step, bottom_y - step), (ux + step, top_y + step * 2)], fill=fg, width=line_width)
            # Right to inner
            draw.line([(ux + step, top_y + step * 2), (ux + step * 2, top_y + step * 2)], fill=fg, width=line_width)
            # Down to connect
            draw.line([(ux + step * 2, top_y + step * 2), (ux + step * 2, bottom_y - step * 2)], fill=fg, width=line_width)


def draw_greek_key_border_vertical(
    draw: ImageDraw,
    x: int, y: int,
    width: int, height: int,
    key_size: int = 20,
    fg_color: str = None,
    bg_color: str = None,
    line_width: int = 3
):
    """
    Draw a vertical Greek key (meander) pattern border.

    Same as horizontal but rotated 90 degrees for side borders.
    """
    fg = fg_color or PALETTE.black
    bg = bg_color or PALETTE.terracotta

    # Fill background
    draw.rectangle([x, y, x + width, y + height], fill=bg)

    # Calculate dimensions
    unit_height = key_size
    margin_x = (width - key_size) // 2
    left_x = x + margin_x
    right_x = x + margin_x + key_size

    # Draw left and right border lines
    draw.line([(left_x, y), (left_x, y + height)], fill=fg, width=line_width)
    draw.line([(right_x, y), (right_x, y + height)], fill=fg, width=line_width)

    # Draw the meander pattern - vertical version
    num_units = height // unit_height
    step = key_size // 4

    for i in range(num_units):
        uy = y + i * unit_height

        if i % 2 == 0:
            # Rightward spiral (starts from left line)
            draw.line([(left_x, uy), (right_x - step, uy)], fill=fg, width=line_width)
            draw.line([(right_x - step, uy), (right_x - step, uy + step * 3)], fill=fg, width=line_width)
            draw.line([(right_x - step, uy + step * 3), (left_x + step, uy + step * 3)], fill=fg, width=line_width)
            draw.line([(left_x + step, uy + step * 3), (left_x + step, uy + step)], fill=fg, width=line_width)
            draw.line([(left_x + step, uy + step), (right_x - step * 2, uy + step)], fill=fg, width=line_width)
            draw.line([(right_x - step * 2, uy + step), (right_x - step * 2, uy + step * 2)], fill=fg, width=line_width)
            draw.line([(right_x - step * 2, uy + step * 2), (left_x + step * 2, uy + step * 2)], fill=fg, width=line_width)
        else:
            # Leftward spiral (starts from right line)
            draw.line([(right_x, uy), (left_x + step, uy)], fill=fg, width=line_width)
            draw.line([(left_x + step, uy), (left_x + step, uy + step * 3)], fill=fg, width=line_width)
            draw.line([(left_x + step, uy + step * 3), (right_x - step, uy + step * 3)], fill=fg, width=line_width)
            draw.line([(right_x - step, uy + step * 3), (right_x - step, uy + step)], fill=fg, width=line_width)
            draw.line([(right_x - step, uy + step), (left_x + step * 2, uy + step)], fill=fg, width=line_width)
            draw.line([(left_x + step * 2, uy + step), (left_x + step * 2, uy + step * 2)], fill=fg, width=line_width)
            draw.line([(left_x + step * 2, uy + step * 2), (right_x - step * 2, uy + step * 2)], fill=fg, width=line_width)


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
    width: int = 750,
    height: int = 1050,
    border_width: int = 40,
    add_texture: bool = True,
    minotaur_path: str = None
) -> Image:
    """
    Generate a card front with Greek pottery styling.

    Portrait orientation (short side on top) for 3.5" x 2.5" card.

    Layout:
    - Greek key meander borders on all four sides
    - Minotaur artwork in upper area
    - Space at bottom for Valentine's greeting
    """
    img = Image.new('RGB', (width, height), PALETTE.terracotta)
    draw = ImageDraw.Draw(img)

    key_size = 32
    line_w = 3

    # Top border - horizontal meander
    draw_greek_key_border(
        draw, border_width, 5,
        width - 2 * border_width, 45,
        key_size=key_size,
        line_width=line_w
    )

    # Bottom border - horizontal meander
    draw_greek_key_border(
        draw, border_width, height - 50,
        width - 2 * border_width, 45,
        key_size=key_size,
        line_width=line_w
    )

    # Left side - vertical meander
    draw_greek_key_border_vertical(
        draw, 5, border_width,
        40, height - 2 * border_width,
        key_size=key_size,
        line_width=line_w
    )

    # Right side - vertical meander
    draw_greek_key_border_vertical(
        draw, width - 45, border_width,
        40, height - 2 * border_width,
        key_size=key_size,
        line_width=line_w
    )

    # Corner squares to connect borders
    draw.rectangle([5, 5, 45, 50], fill=PALETTE.terracotta, outline=PALETTE.black, width=line_w)
    draw.rectangle([width - 45, 5, width - 5, 50], fill=PALETTE.terracotta, outline=PALETTE.black, width=line_w)
    draw.rectangle([5, height - 50, 45, height - 5], fill=PALETTE.terracotta, outline=PALETTE.black, width=line_w)
    draw.rectangle([width - 45, height - 50, width - 5, height - 5], fill=PALETTE.terracotta, outline=PALETTE.black, width=line_w)

    # Add minotaur artwork if provided
    if minotaur_path:
        try:
            print(f"Loading minotaur from: {minotaur_path}")
            minotaur = Image.open(minotaur_path).convert('RGBA')
            print(f"Minotaur loaded: {minotaur.size}, mode: {minotaur.mode}")

            # Calculate area for minotaur (upper portion, leaving room for text)
            content_width = width - 2 * (border_width + 10)
            content_height = height - 220  # Leave space at bottom for greeting
            print(f"Content area: {content_width}x{content_height}")

            # Scale minotaur to fit
            minotaur_ratio = minotaur.width / minotaur.height
            content_ratio = content_width / content_height

            if minotaur_ratio > content_ratio:
                # Width constrained
                new_width = content_width
                new_height = int(content_width / minotaur_ratio)
            else:
                # Height constrained
                new_height = content_height
                new_width = int(content_height * minotaur_ratio)

            print(f"Resizing minotaur to: {new_width}x{new_height}")
            minotaur = minotaur.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Center horizontally, position in upper area
            x_pos = (width - new_width) // 2
            y_pos = 60 + (content_height - new_height) // 2
            print(f"Pasting minotaur at position: ({x_pos}, {y_pos})")

            # Convert base image to RGBA to properly handle transparency
            img = img.convert('RGBA')

            # Composite minotaur onto card using alpha channel
            img.paste(minotaur, (x_pos, y_pos), minotaur)
            print("Minotaur pasted successfully!")

            # Convert back to RGB for saving
            img = img.convert('RGB')

        except Exception as e:
            import traceback
            print(f"Could not load minotaur image: {e}")
            traceback.print_exc()

    # Add Valentine's greeting in center-bottom area
    import os
    from PIL import ImageFont

    # Path to custom Greek-style font
    base_dir = os.path.dirname(os.path.abspath(__file__))
    greek_font_path = os.path.join(base_dir, "..", "assets", "fonts", "Greek-Freak.ttf")
    fallback_font_path = os.path.join(base_dir, "..", "assets", "fonts", "CaesarDressing-Regular.ttf")

    print(f"Looking for Greek-Freak font at: {greek_font_path}")
    print(f"Font exists: {os.path.exists(greek_font_path)}")

    try:
        # Use decorative Greek-style font
        if os.path.exists(greek_font_path):
            greeting_font = ImageFont.truetype(greek_font_path, 72)
            print(f"Loaded Greek-Freak font: {greeting_font.getname()}")
        elif os.path.exists(fallback_font_path):
            greeting_font = ImageFont.truetype(fallback_font_path, 52)
            print(f"Loaded fallback font: {greeting_font.getname()}")
        else:
            greeting_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
            print("Using DejaVu fallback")
    except Exception as e:
        print(f"Font error: {e}")
        greeting_font = ImageFont.load_default()

    greeting_text = "You are aMAZEing!"

    # Need to recreate draw object after image mode conversion
    draw = ImageDraw.Draw(img)

    # Get text bounding box to center it
    bbox = draw.textbbox((0, 0), greeting_text, font=greeting_font)
    text_width = bbox[2] - bbox[0]
    text_x = (width - text_width) // 2
    text_y = height - 145  # Position above the credit with better spacing

    draw.text((text_x, text_y), greeting_text, fill=PALETTE.black, font=greeting_font)

    # Add artist credit at bottom left
    try:
        credit_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except:
        credit_font = ImageFont.load_default()

    credit_text = "art by Andrew Morris vanmorrisman@yahoo.co.uk"
    # Center the credit text
    credit_bbox = draw.textbbox((0, 0), credit_text, font=credit_font)
    credit_width = credit_bbox[2] - credit_bbox[0]
    credit_x = (width - credit_width) // 2
    draw.text((credit_x, height - 75), credit_text, fill=PALETTE.black, font=credit_font)

    # Add texture (after compositing)
    if add_texture:
        img = add_pottery_texture(img)

    return img


def generate_greek_card_back(
    width: int = 750,
    height: int = 1050,
    border_width: int = 35
) -> Image:
    """
    Generate a card back template for the maze.
    Meander borders on all sides, leaving room for the maze.
    """
    img = Image.new('RGB', (width, height), PALETTE.terracotta)
    draw = ImageDraw.Draw(img)

    key_size = 28
    line_w = 2

    # Top border - horizontal meander
    draw_greek_key_border(
        draw, border_width, 5,
        width - 2 * border_width, 35,
        key_size=key_size,
        line_width=line_w
    )

    # Bottom border - horizontal meander
    draw_greek_key_border(
        draw, border_width, height - 40,
        width - 2 * border_width, 35,
        key_size=key_size,
        line_width=line_w
    )

    # Left side - vertical meander
    draw_greek_key_border_vertical(
        draw, 5, border_width,
        32, height - 2 * border_width,
        key_size=key_size,
        line_width=line_w
    )

    # Right side - vertical meander
    draw_greek_key_border_vertical(
        draw, width - 37, border_width,
        32, height - 2 * border_width,
        key_size=key_size,
        line_width=line_w
    )

    # Corner squares
    draw.rectangle([5, 5, 37, 40], fill=PALETTE.terracotta, outline=PALETTE.black, width=line_w)
    draw.rectangle([width - 37, 5, width - 5, 40], fill=PALETTE.terracotta, outline=PALETTE.black, width=line_w)
    draw.rectangle([5, height - 40, 37, height - 5], fill=PALETTE.terracotta, outline=PALETTE.black, width=line_w)
    draw.rectangle([width - 37, height - 40, width - 5, height - 5], fill=PALETTE.terracotta, outline=PALETTE.black, width=line_w)

    return img


def main():
    import os

    base_dir = os.path.join(os.path.dirname(__file__), "..")
    output_dir = os.path.join(base_dir, "assets", "templates")
    os.makedirs(output_dir, exist_ok=True)

    # Delete existing templates to ensure fresh generation
    front_path = os.path.join(output_dir, "greek_card_front.png")
    back_path = os.path.join(output_dir, "greek_card_back.png")
    for path in [front_path, back_path]:
        if os.path.exists(path):
            os.remove(path)
            print(f"Deleted: {path}")

    # Check for minotaur image
    minotaur_path = os.path.join(base_dir, "assets", "artwork", "minotaur.png")
    if not os.path.exists(minotaur_path):
        minotaur_path = None
        print("Note: No minotaur.png found in assets/artwork/")
        print("      Place your minotaur image there and re-run to include it.")
        print()

    print("Greek Pottery Design System")
    print("=" * 40)
    print("Card size: 2.5\" x 3.5\" portrait (750 x 1050 pixels at 300 DPI)")
    print()
    print("Color Palette:")
    print(f"  Terracotta: {PALETTE.terracotta}")
    print(f"  Black: {PALETTE.black}")
    print(f"  White: {PALETTE.white}")
    print()

    # Generate card front
    print("Generating card front template...")
    front = generate_greek_card_front(minotaur_path=minotaur_path)
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
