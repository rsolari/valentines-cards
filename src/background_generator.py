#!/usr/bin/env python3
"""
Background Pattern Generator for Valentine's Cards

Generates a harlequin diamond pattern with 8-pointed stars,
inspired by Mediterranean/Renaissance tile designs.

Card specs: 3.5" x 2.5" at 300 DPI = 1050 x 750 pixels
"""

import math
from PIL import Image, ImageDraw, ImageFilter
import random


def draw_8_pointed_star(draw, cx, cy, outer_radius, inner_radius, color, outline_color=None):
    """
    Draw an 8-pointed star at the specified center point.

    Args:
        draw: PIL ImageDraw object
        cx, cy: Center coordinates
        outer_radius: Radius to outer points
        inner_radius: Radius to inner points
        color: Fill color
        outline_color: Optional outline color
    """
    points = []
    for i in range(16):
        angle = math.pi / 8 * i - math.pi / 2  # Start from top
        if i % 2 == 0:
            # Outer point
            r = outer_radius
        else:
            # Inner point
            r = inner_radius
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append((x, y))

    draw.polygon(points, fill=color, outline=outline_color)


def add_texture(image, intensity=20):
    """Add subtle noise texture to make it look more vintage."""
    pixels = image.load()
    width, height = image.size

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y][:3]
            # Add random noise
            noise = random.randint(-intensity, intensity)
            r = max(0, min(255, r + noise))
            g = max(0, min(255, g + noise))
            b = max(0, min(255, b + noise))
            pixels[x, y] = (r, g, b)

    return image


def generate_harlequin_background(
    width=1050,
    height=750,
    diamond_width=150,
    diamond_height=200,
    blue_color=(65, 105, 170),      # Muted blue
    cream_color=(245, 235, 220),     # Warm cream
    gold_color=(180, 130, 70),       # Antique gold
    gold_dark=(140, 95, 50),         # Darker gold for depth
    add_vintage_texture=True
):
    """
    Generate a harlequin diamond pattern with 8-pointed stars.

    Returns a PIL Image at the specified dimensions.
    """
    # Create base image
    img = Image.new('RGB', (width, height), cream_color)
    draw = ImageDraw.Draw(img)

    # Calculate grid
    cols = (width // diamond_width) + 2
    rows = (height // (diamond_height // 2)) + 2

    # Draw diamonds in a checkerboard pattern
    for row in range(-1, rows + 1):
        for col in range(-1, cols + 1):
            # Calculate center of this diamond
            cx = col * diamond_width + (diamond_width // 2 if row % 2 == 1 else 0)
            cy = row * (diamond_height // 2)

            # Determine color based on checkerboard pattern
            is_blue = (row + col) % 2 == 0
            color = blue_color if is_blue else cream_color

            # Diamond vertices
            diamond = [
                (cx, cy - diamond_height // 2),  # Top
                (cx + diamond_width // 2, cy),    # Right
                (cx, cy + diamond_height // 2),   # Bottom
                (cx - diamond_width // 2, cy),    # Left
            ]

            # Draw diamond
            draw.polygon(diamond, fill=color)

            # Draw star in center
            star_outer = min(diamond_width, diamond_height) // 4
            star_inner = star_outer * 0.4

            # Add slight variation to gold color for visual interest
            gold_variation = tuple(
                max(0, min(255, c + random.randint(-15, 15)))
                for c in gold_color
            )

            draw_8_pointed_star(
                draw, cx, cy,
                outer_radius=star_outer,
                inner_radius=star_inner,
                color=gold_variation,
                outline_color=gold_dark
            )

    # Add vintage texture
    if add_vintage_texture:
        img = add_texture(img, intensity=12)
        # Slight blur for softer look
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))

    return img


def generate_valentine_background():
    """Generate the background with Valentine's color adjustments."""
    # Slightly warmer/pinker tones for Valentine's theme
    return generate_harlequin_background(
        blue_color=(70, 100, 165),       # Slightly softer blue
        cream_color=(255, 245, 240),      # Slightly pink-tinted cream
        gold_color=(185, 125, 65),        # Warm gold
        gold_dark=(145, 90, 45),
    )


def main():
    import os

    output_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "templates")
    os.makedirs(output_dir, exist_ok=True)

    print("Generating harlequin star background...")
    print("Card size: 3.5\" x 2.5\" (1050 x 750 pixels at 300 DPI)")
    print()

    # Generate main background
    img = generate_valentine_background()

    # Save at print resolution
    filepath = os.path.join(output_dir, "background_harlequin_stars.png")
    img.save(filepath, dpi=(300, 300))
    print(f"Saved: {filepath}")

    # Also generate a version with more visible grid for reference
    img_large = generate_harlequin_background(
        diamond_width=175,
        diamond_height=230,
    )
    filepath_large = os.path.join(output_dir, "background_harlequin_large.png")
    img_large.save(filepath_large, dpi=(300, 300))
    print(f"Saved: {filepath_large}")

    print()
    print("Background generated!")
    print("You can overlay white text boxes on this for your Valentine's greeting.")


if __name__ == "__main__":
    main()
