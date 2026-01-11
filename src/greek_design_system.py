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
    """Generate card front with Greek pottery styling.

    Layout spec (tightened for high-impact):
    - Inner margins: 54px top/bottom, 48-54px left/right
    - Header top padding: 78px from inner border
    - Header to illustration gap: 72px
    - Illustration: ~640px height target (58-65% of card), centered
    - Illustration to pun gap: 72px
    - Pun baseline to bottom inner border: 84px
    - Credit: 6-7pt at 80-85% opacity, 48-54px from inner border
    """
    img = Image.new('RGB', (width, height), PALETTE.terracotta)
    draw = ImageDraw.Draw(img)

    # Layout constants - tightened for dramatic impact
    INNER_MARGIN_TOP = 54
    INNER_MARGIN_BOTTOM = 54
    INNER_MARGIN_LEFT = 48
    INNER_MARGIN_RIGHT = 48
    HEADER_TOP_PADDING = 78
    HEADER_TO_ILLUSTRATION_GAP = 72
    ILLUSTRATION_TO_PUN_GAP = 72
    PUN_BOTTOM_PADDING = 84
    CENTER_X = width // 2  # 375
    OPTICAL_NUDGE_X = -12  # Nudge left if art mass leans right
    CREDIT_OFFSET_RIGHT = 48
    CREDIT_OFFSET_BOTTOM = 48

    draw_card_borders(draw, width, height, border_width)

    # Setup fonts
    base_dir = os.path.dirname(os.path.abspath(__file__))
    greek_font_path = os.path.join(base_dir, "..", "assets", "fonts", "Greek-Freak.ttf")

    # Calculate header position (reduced 10% from 80pt for balance with larger art)
    try:
        header_font = ImageFont.truetype(greek_font_path, 72)
    except:
        header_font = ImageFont.load_default()

    header_text = "Happy Valentine's"
    header_bbox = draw.textbbox((0, 0), header_text, font=header_font)
    header_width = header_bbox[2] - header_bbox[0]
    header_height = header_bbox[3] - header_bbox[1]
    header_x = CENTER_X - header_width // 2
    header_y = INNER_MARGIN_TOP + HEADER_TOP_PADDING

    # Calculate pun line position (from bottom)
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
    pun_total_width = w1 + w2 + w3

    # Pun baseline from bottom inner border
    pun_baseline_y = height - INNER_MARGIN_BOTTOM - PUN_BOTTOM_PADDING
    pun_start_x = CENTER_X - pun_total_width // 2

    # Calculate illustration zone
    illustration_top = header_y + header_height + HEADER_TO_ILLUSTRATION_GAP
    illustration_bottom = pun_baseline_y - h2 - ILLUSTRATION_TO_PUN_GAP
    illustration_zone_height = illustration_bottom - illustration_top
    illustration_zone_width = width - INNER_MARGIN_LEFT - INNER_MARGIN_RIGHT

    # Add minotaur artwork
    if minotaur_path:
        try:
            minotaur = Image.open(minotaur_path).convert('RGBA')

            minotaur_ratio = minotaur.width / minotaur.height
            zone_ratio = illustration_zone_width / illustration_zone_height

            if minotaur_ratio > zone_ratio:
                new_width = illustration_zone_width
                new_height = int(illustration_zone_width / minotaur_ratio)
            else:
                new_height = illustration_zone_height
                new_width = int(illustration_zone_height * minotaur_ratio)

            minotaur = minotaur.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Center in illustration zone with optical nudge
            x_pos = CENTER_X - new_width // 2 + OPTICAL_NUDGE_X
            y_pos = illustration_top + (illustration_zone_height - new_height) // 2

            img = img.convert('RGBA')
            img.paste(minotaur, (x_pos, y_pos), minotaur)
            img = img.convert('RGB')

        except Exception as e:
            print(f"Could not load minotaur image: {e}")

    draw = ImageDraw.Draw(img)

    # Draw header
    draw.text((header_x, header_y), header_text, fill=PALETTE.black, font=header_font)

    # Draw pun line with baseline alignment
    baseline_offset = h2 - h1
    pun_y = pun_baseline_y - h2
    draw.text((pun_start_x, pun_y + baseline_offset), part1, fill=PALETTE.black, font=small_font)
    draw.text((pun_start_x + w1, pun_y), part2, fill=PALETTE.black, font=big_font)
    draw.text((pun_start_x + w1 + w2, pun_y + baseline_offset), part3, fill=PALETTE.black, font=small_font)

    # Artist credit (6-7pt ≈ 8-10px at 300dpi, with 80-85% opacity)
    # Pinned to bottom, just above the Greek key border
    try:
        credit_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except:
        credit_font = ImageFont.load_default()

    credit_text = "art by Andrew Morris vanmorrisman@yahoo.co.uk"
    credit_bbox = draw.textbbox((0, 0), credit_text, font=credit_font)
    credit_width = credit_bbox[2] - credit_bbox[0]
    credit_height = credit_bbox[3] - credit_bbox[1]
    credit_x = width - INNER_MARGIN_RIGHT - credit_width
    credit_y = height - 50 - credit_height - 6  # Just above bottom border (border starts at height-50)

    # Draw credit with ~80% opacity (slightly lighter to not compete with art)
    credit_color = "#3D3D3D"  # ~80% opacity black on terracotta
    draw.text((credit_x, credit_y), credit_text, fill=credit_color, font=credit_font)

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
    draw_maze(draw, grid, maze_x, maze_y, cell_size, tile_size=6, gap=2)

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
