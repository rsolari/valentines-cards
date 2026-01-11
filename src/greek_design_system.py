#!/usr/bin/env python3
"""
Greek Pottery Design System for Valentine's Cards

Inspired by ancient Greek black-figure and red-figure pottery,
featuring classic motifs like the meander (Greek key) pattern.

Card specs: 2.5" x 3.5" at 300 DPI = 750 x 1050 pixels (portrait)
"""

import os
import random
from PIL import Image, ImageDraw, ImageFont
from dataclasses import dataclass
from typing import Tuple


# =============================================================================
# COLOR PALETTE
# =============================================================================

@dataclass
class GreekPalette:
    """Color palette inspired by ancient Greek pottery."""
    terracotta: str = "#CD6839"
    black: str = "#1A1A1A"
    white: str = "#F5F0E6"

    def as_rgb(self, color_name: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple."""
        hex_color = getattr(self, color_name).lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


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
    """Draw a horizontal Greek key (meander) pattern border."""
    fg = fg_color or PALETTE.black
    bg = bg_color or PALETTE.terracotta

    draw.rectangle([x, y, x + width, y + height], fill=bg)

    margin_y = (height - key_size) // 2
    top_y = y + margin_y
    bottom_y = y + margin_y + key_size

    draw.line([(x, top_y), (x + width, top_y)], fill=fg, width=line_width)
    draw.line([(x, bottom_y), (x + width, bottom_y)], fill=fg, width=line_width)

    num_units = -(-width // key_size)  # Ceiling division to fill edge
    step = key_size // 4

    for i in range(num_units):
        ux = x + i * key_size

        if i % 2 == 0:
            draw.line([(ux, top_y), (ux, bottom_y - step)], fill=fg, width=line_width)
            draw.line([(ux, bottom_y - step), (ux + step * 3, bottom_y - step)], fill=fg, width=line_width)
            draw.line([(ux + step * 3, bottom_y - step), (ux + step * 3, top_y + step)], fill=fg, width=line_width)
            draw.line([(ux + step * 3, top_y + step), (ux + step, top_y + step)], fill=fg, width=line_width)
            draw.line([(ux + step, top_y + step), (ux + step, bottom_y - step * 2)], fill=fg, width=line_width)
            draw.line([(ux + step, bottom_y - step * 2), (ux + step * 2, bottom_y - step * 2)], fill=fg, width=line_width)
            draw.line([(ux + step * 2, bottom_y - step * 2), (ux + step * 2, top_y + step * 2)], fill=fg, width=line_width)
        else:
            draw.line([(ux, bottom_y), (ux, top_y + step)], fill=fg, width=line_width)
            draw.line([(ux, top_y + step), (ux + step * 3, top_y + step)], fill=fg, width=line_width)
            draw.line([(ux + step * 3, top_y + step), (ux + step * 3, bottom_y - step)], fill=fg, width=line_width)
            draw.line([(ux + step * 3, bottom_y - step), (ux + step, bottom_y - step)], fill=fg, width=line_width)
            draw.line([(ux + step, bottom_y - step), (ux + step, top_y + step * 2)], fill=fg, width=line_width)
            draw.line([(ux + step, top_y + step * 2), (ux + step * 2, top_y + step * 2)], fill=fg, width=line_width)
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
    """Draw a vertical Greek key (meander) pattern border."""
    fg = fg_color or PALETTE.black
    bg = bg_color or PALETTE.terracotta

    draw.rectangle([x, y, x + width, y + height], fill=bg)

    margin_x = (width - key_size) // 2
    left_x = x + margin_x
    right_x = x + margin_x + key_size

    draw.line([(left_x, y), (left_x, y + height)], fill=fg, width=line_width)
    draw.line([(right_x, y), (right_x, y + height)], fill=fg, width=line_width)

    num_units = -(-height // key_size)  # Ceiling division to fill edge
    step = key_size // 4

    for i in range(num_units):
        uy = y + i * key_size

        if i % 2 == 0:
            draw.line([(left_x, uy), (right_x - step, uy)], fill=fg, width=line_width)
            draw.line([(right_x - step, uy), (right_x - step, uy + step * 3)], fill=fg, width=line_width)
            draw.line([(right_x - step, uy + step * 3), (left_x + step, uy + step * 3)], fill=fg, width=line_width)
            draw.line([(left_x + step, uy + step * 3), (left_x + step, uy + step)], fill=fg, width=line_width)
            draw.line([(left_x + step, uy + step), (right_x - step * 2, uy + step)], fill=fg, width=line_width)
            draw.line([(right_x - step * 2, uy + step), (right_x - step * 2, uy + step * 2)], fill=fg, width=line_width)
            draw.line([(right_x - step * 2, uy + step * 2), (left_x + step * 2, uy + step * 2)], fill=fg, width=line_width)
        else:
            draw.line([(right_x, uy), (left_x + step, uy)], fill=fg, width=line_width)
            draw.line([(left_x + step, uy), (left_x + step, uy + step * 3)], fill=fg, width=line_width)
            draw.line([(left_x + step, uy + step * 3), (right_x - step, uy + step * 3)], fill=fg, width=line_width)
            draw.line([(right_x - step, uy + step * 3), (right_x - step, uy + step)], fill=fg, width=line_width)
            draw.line([(right_x - step, uy + step), (left_x + step * 2, uy + step)], fill=fg, width=line_width)
            draw.line([(left_x + step * 2, uy + step), (left_x + step * 2, uy + step * 2)], fill=fg, width=line_width)
            draw.line([(left_x + step * 2, uy + step * 2), (right_x - step * 2, uy + step * 2)], fill=fg, width=line_width)


# =============================================================================
# TEXTURE
# =============================================================================

def add_pottery_texture(image: Image) -> Image:
    """Add subtle speckle texture like aged pottery."""
    pixels = image.load()
    width, height = image.size

    for y in range(height):
        for x in range(width):
            if random.random() < 0.03:
                r, g, b = pixels[x, y][:3]
                factor = random.uniform(0.7, 0.9)
                pixels[x, y] = (int(r * factor), int(g * factor), int(b * factor))

    return image


# =============================================================================
# MAZE GENERATION
# =============================================================================

def generate_maze(rows: int, cols: int) -> list:
    """Generate a maze using recursive backtracker algorithm.

    Returns a 2D grid where each cell has walls: {'N': bool, 'S': bool, 'E': bool, 'W': bool}
    True = wall exists, False = passage
    """
    # Initialize grid with all walls
    grid = [[{'N': True, 'S': True, 'E': True, 'W': True} for _ in range(cols)] for _ in range(rows)]

    # Direction mappings
    directions = {
        'N': (-1, 0, 'S'),  # (row_delta, col_delta, opposite_wall)
        'S': (1, 0, 'N'),
        'E': (0, 1, 'W'),
        'W': (0, -1, 'E')
    }

    visited = [[False] * cols for _ in range(rows)]
    stack = [(0, 0)]  # Start at top-left
    visited[0][0] = True

    while stack:
        row, col = stack[-1]

        # Find unvisited neighbors
        neighbors = []
        for direction, (dr, dc, _) in directions.items():
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                neighbors.append((direction, nr, nc))

        if neighbors:
            # Choose random neighbor
            direction, nr, nc = random.choice(neighbors)
            _, _, opposite = directions[direction]

            # Remove walls between current and neighbor
            grid[row][col][direction] = False
            grid[nr][nc][opposite] = False

            visited[nr][nc] = True
            stack.append((nr, nc))
        else:
            stack.pop()

    # Create entrance (top) and exit (bottom)
    grid[0][cols // 2]['N'] = False  # Entrance at top center
    grid[rows - 1][cols // 2]['S'] = False  # Exit at bottom center

    return grid


def draw_mosaic_wall(
    draw: ImageDraw,
    x1: int, y1: int,
    x2: int, y2: int,
    tile_size: int = 6,
    gap: int = 2,
    base_color: str = None
):
    """Draw a wall segment as mosaic tiles."""
    base = base_color or PALETTE.black

    # Parse base color
    if base.startswith('#'):
        base_rgb = tuple(int(base.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    else:
        base_rgb = (26, 26, 26)  # Default black

    # Determine if horizontal or vertical
    if abs(x2 - x1) > abs(y2 - y1):
        # Horizontal wall
        start_x, end_x = min(x1, x2), max(x1, x2)
        y = y1
        x = start_x
        while x < end_x:
            # Vary color slightly for each tile
            factor = random.uniform(0.7, 1.3)
            tile_color = tuple(max(0, min(255, int(c * factor))) for c in base_rgb)

            tile_end = min(x + tile_size, end_x)
            half_tile = tile_size // 2
            draw.rectangle([x, y - half_tile, tile_end, y + half_tile], fill=tile_color)
            x += tile_size + gap
    else:
        # Vertical wall
        start_y, end_y = min(y1, y2), max(y1, y2)
        x = x1
        y = start_y
        while y < end_y:
            # Vary color slightly for each tile
            factor = random.uniform(0.7, 1.3)
            tile_color = tuple(max(0, min(255, int(c * factor))) for c in base_rgb)

            tile_end = min(y + tile_size, end_y)
            half_tile = tile_size // 2
            draw.rectangle([x - half_tile, y, x + half_tile, tile_end], fill=tile_color)
            y += tile_size + gap


def draw_maze(
    draw: ImageDraw,
    grid: list,
    x_offset: int,
    y_offset: int,
    cell_size: int,
    tile_size: int = 6,
    gap: int = 2,
    wall_color: str = None
):
    """Draw the maze on the image using mosaic tiles."""
    rows = len(grid)
    cols = len(grid[0])

    for row in range(rows):
        for col in range(cols):
            cell = grid[row][col]
            cx = x_offset + col * cell_size
            cy = y_offset + row * cell_size

            # Draw north wall
            if cell['N']:
                draw_mosaic_wall(draw, cx, cy, cx + cell_size, cy,
                               tile_size=tile_size, gap=gap, base_color=wall_color)

            # Draw west wall
            if cell['W']:
                draw_mosaic_wall(draw, cx, cy, cx, cy + cell_size,
                               tile_size=tile_size, gap=gap, base_color=wall_color)

    # Draw east border (right edge)
    for row in range(rows):
        cell = grid[row][cols - 1]
        if cell['E']:
            cx = x_offset + cols * cell_size
            cy = y_offset + row * cell_size
            draw_mosaic_wall(draw, cx, cy, cx, cy + cell_size,
                           tile_size=tile_size, gap=gap, base_color=wall_color)

    # Draw south border (bottom edge)
    for col in range(cols):
        cell = grid[rows - 1][col]
        if cell['S']:
            cx = x_offset + col * cell_size
            cy = y_offset + rows * cell_size
            draw_mosaic_wall(draw, cx, cy, cx + cell_size, cy,
                           tile_size=tile_size, gap=gap, base_color=wall_color)


# =============================================================================
# SHARED BORDER DRAWING
# =============================================================================

def draw_card_borders(
    draw: ImageDraw,
    width: int,
    height: int,
    border_width: int = 40,
    key_size: int = 32,
    line_w: int = 3
):
    """Draw Greek key borders and corner squares (shared by front and back)."""
    # Horizontal borders (top and bottom)
    draw_greek_key_border(draw, border_width, 5, width - 2 * border_width, 45, key_size=key_size, line_width=line_w)
    draw_greek_key_border(draw, border_width, height - 50, width - 2 * border_width, 45, key_size=key_size, line_width=line_w)

    # Vertical borders (left and right)
    draw_greek_key_border_vertical(draw, 5, border_width, 40, height - 2 * border_width, key_size=key_size, line_width=line_w)
    draw_greek_key_border_vertical(draw, width - 45, border_width, 40, height - 2 * border_width, key_size=key_size, line_width=line_w)

    # Corner squares
    for corners in [(5, 5, 45, 50), (width - 45, 5, width - 5, 50),
                    (5, height - 50, 45, height - 5), (width - 45, height - 50, width - 5, height - 5)]:
        draw.rectangle(corners, fill=PALETTE.terracotta, outline=PALETTE.black, width=line_w)


# =============================================================================
# CARD GENERATORS
# =============================================================================

def generate_greek_card_front(
    width: int = 750,
    height: int = 1050,
    border_width: int = 40,
    add_texture: bool = True,
    minotaur_path: str = None
) -> Image:
    """Generate card front with Greek pottery styling."""
    img = Image.new('RGB', (width, height), PALETTE.terracotta)
    draw = ImageDraw.Draw(img)

    draw_card_borders(draw, width, height, border_width)

    # Add minotaur artwork
    if minotaur_path:
        try:
            minotaur = Image.open(minotaur_path).convert('RGBA')
            content_width = width - 2 * (border_width + 10)
            content_height = height - 220

            minotaur_ratio = minotaur.width / minotaur.height
            content_ratio = content_width / content_height

            if minotaur_ratio > content_ratio:
                new_width = content_width
                new_height = int(content_width / minotaur_ratio)
            else:
                new_height = content_height
                new_width = int(content_height * minotaur_ratio)

            # Scale 15% larger
            new_width = int(new_width * 1.15)
            new_height = int(new_height * 1.15)

            minotaur = minotaur.resize((new_width, new_height), Image.Resampling.LANCZOS)

            x_pos = (width - new_width) // 2
            minotaur_top = 120
            minotaur_bottom = height - 200
            y_pos = minotaur_top + (minotaur_bottom - minotaur_top - new_height) // 2

            img = img.convert('RGBA')
            img.paste(minotaur, (x_pos, y_pos), minotaur)
            img = img.convert('RGB')

        except Exception as e:
            print(f"Could not load minotaur image: {e}")

    # Setup fonts
    base_dir = os.path.dirname(os.path.abspath(__file__))
    greek_font_path = os.path.join(base_dir, "..", "assets", "fonts", "Greek-Freak.ttf")

    draw = ImageDraw.Draw(img)

    # "Happy Valentines" title
    try:
        top_font = ImageFont.truetype(greek_font_path, 80)
    except:
        top_font = ImageFont.load_default()

    top_text = "Happy Valentine's"
    top_bbox = draw.textbbox((0, 0), top_text, font=top_font)
    top_x = (width - (top_bbox[2] - top_bbox[0])) // 2
    draw.text((top_x, 70), top_text, fill=PALETTE.black, font=top_font)

    # "You are aMAZEing!" with emphasis on MAZE
    try:
        small_font = ImageFont.truetype(greek_font_path, 42)
        big_font = ImageFont.truetype(greek_font_path, 90)
    except:
        small_font = big_font = ImageFont.load_default()

    part1, part2, part3 = "You are a", "MAZE", "ing!"

    bbox1 = draw.textbbox((0, 0), part1, font=small_font)
    bbox2 = draw.textbbox((0, 0), part2, font=big_font)
    bbox3 = draw.textbbox((0, 0), part3, font=small_font)

    w1, w2, w3 = bbox1[2] - bbox1[0], bbox2[2] - bbox2[0], bbox3[2] - bbox3[0]
    h1, h2 = bbox1[3] - bbox1[1], bbox2[3] - bbox2[1]

    text_y = height - 200 + (120 - h2) // 2
    start_x = (width - (w1 + w2 + w3)) // 2
    baseline_offset = h2 - h1

    draw.text((start_x, text_y + baseline_offset), part1, fill=PALETTE.black, font=small_font)
    draw.text((start_x + w1, text_y), part2, fill=PALETTE.black, font=big_font)
    draw.text((start_x + w1 + w2, text_y + baseline_offset), part3, fill=PALETTE.black, font=small_font)

    # Artist credit
    try:
        credit_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except:
        credit_font = ImageFont.load_default()

    credit_text = "art by Andrew Morris vanmorrisman@yahoo.co.uk"
    credit_bbox = draw.textbbox((0, 0), credit_text, font=credit_font)
    credit_x = width - (credit_bbox[2] - credit_bbox[0]) - 56
    draw.text((credit_x, height - 72), credit_text, fill=PALETTE.black, font=credit_font)

    if add_texture:
        img = add_pottery_texture(img)

    return img


def generate_greek_card_back(
    width: int = 750,
    height: int = 1050,
    border_width: int = 40,
    add_texture: bool = True
) -> Image:
    """Generate card back with maze and text."""
    img = Image.new('RGB', (width, height), PALETTE.terracotta)
    draw = ImageDraw.Draw(img)

    draw_card_borders(draw, width, height, border_width)

    # Calculate maze area (leave room for text at bottom)
    maze_margin = 60  # Inside the Greek key border
    text_area_height = 100  # Space for "From Felix" and credit
    maze_x = maze_margin
    maze_y = maze_margin
    maze_width = width - 2 * maze_margin
    maze_height = height - 2 * maze_margin - text_area_height

    # Maze parameters
    cell_size = 40  # Size of each maze cell
    maze_cols = maze_width // cell_size
    maze_rows = maze_height // cell_size

    # Center the maze in the available space
    actual_maze_width = maze_cols * cell_size
    actual_maze_height = maze_rows * cell_size
    maze_x = (width - actual_maze_width) // 2
    maze_y = maze_margin + (maze_height - actual_maze_height) // 2

    # Generate and draw maze
    grid = generate_maze(maze_rows, maze_cols)
    draw_maze(draw, grid, maze_x, maze_y, cell_size, tile_size=6, gap=2, wall_color="#C4A35A")

    # Setup fonts
    base_dir = os.path.dirname(os.path.abspath(__file__))
    greek_font_path = os.path.join(base_dir, "..", "assets", "fonts", "Greek-Freak.ttf")

    # "From Felix" text
    try:
        from_font = ImageFont.truetype(greek_font_path, 48)
    except:
        from_font = ImageFont.load_default()

    from_text = "From Felix"
    from_bbox = draw.textbbox((0, 0), from_text, font=from_font)
    from_x = (width - (from_bbox[2] - from_bbox[0])) // 2
    from_y = height - text_area_height - 20
    draw.text((from_x, from_y), from_text, fill=PALETTE.black, font=from_font)

    # "designed by Felix and his mom" credit
    try:
        credit_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except:
        credit_font = ImageFont.load_default()

    credit_text = "designed by Felix and his mom"
    credit_bbox = draw.textbbox((0, 0), credit_text, font=credit_font)
    credit_x = (width - (credit_bbox[2] - credit_bbox[0])) // 2
    credit_y = height - 70
    draw.text((credit_x, credit_y), credit_text, fill=PALETTE.black, font=credit_font)

    if add_texture:
        img = add_pottery_texture(img)

    return img


def main():
    base_dir = os.path.join(os.path.dirname(__file__), "..")
    output_dir = os.path.join(base_dir, "assets", "templates")
    os.makedirs(output_dir, exist_ok=True)

    # Check for minotaur image
    minotaur_path = os.path.join(base_dir, "assets", "artwork", "minotaur.png")
    if not os.path.exists(minotaur_path):
        minotaur_path = None

    print("Greek Pottery Design System")
    print("=" * 40)
    print("Card size: 2.5\" x 3.5\" portrait (750 x 1050 pixels at 300 DPI)")

    # Generate cards
    front = generate_greek_card_front(minotaur_path=minotaur_path)
    front.save(os.path.join(output_dir, "greek_card_front.png"), dpi=(300, 300))
    print("Saved: greek_card_front.png")

    back = generate_greek_card_back()
    back.save(os.path.join(output_dir, "greek_card_back.png"), dpi=(300, 300))
    print("Saved: greek_card_back.png")


if __name__ == "__main__":
    main()
