"""
Wall Renderers for Maze Generation.

This module provides different wall rendering styles for mazes.
Each renderer implements the same interface for drawing walls.
"""

import random
from abc import ABC, abstractmethod
from PIL import ImageDraw
from typing import Optional


class WallRenderer(ABC):
    """Abstract base class for maze wall renderers."""

    def __init__(self, base_color: str = "#1A1A1A"):
        """Initialize the renderer with a base wall color.

        Args:
            base_color: Hex color string for walls
        """
        self.base_color = base_color
        self.base_rgb = self._hex_to_rgb(base_color)

    def _hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    @abstractmethod
    def draw_wall(
        self,
        draw: ImageDraw,
        x1: int, y1: int,
        x2: int, y2: int
    ):
        """Draw a wall segment from (x1, y1) to (x2, y2).

        Args:
            draw: PIL ImageDraw object
            x1, y1: Start coordinates
            x2, y2: End coordinates
        """
        pass

    def draw_maze(
        self,
        draw: ImageDraw,
        grid: list,
        x_offset: int,
        y_offset: int,
        cell_size: int
    ):
        """Draw the complete maze on the image.

        Args:
            draw: PIL ImageDraw object
            grid: 2D grid from maze generator
            x_offset: X position of maze top-left
            y_offset: Y position of maze top-left
            cell_size: Size of each maze cell in pixels
        """
        rows = len(grid)
        cols = len(grid[0])

        for row in range(rows):
            for col in range(cols):
                cell = grid[row][col]
                cx = x_offset + col * cell_size
                cy = y_offset + row * cell_size

                # Draw north wall
                if cell['N']:
                    self.draw_wall(draw, cx, cy, cx + cell_size, cy)

                # Draw west wall
                if cell['W']:
                    self.draw_wall(draw, cx, cy, cx, cy + cell_size)

        # Draw east border (right edge)
        for row in range(rows):
            cell = grid[row][cols - 1]
            if cell['E']:
                cx = x_offset + cols * cell_size
                cy = y_offset + row * cell_size
                self.draw_wall(draw, cx, cy, cx, cy + cell_size)

        # Draw south border (bottom edge)
        for col in range(cols):
            cell = grid[rows - 1][col]
            if cell['S']:
                cx = x_offset + col * cell_size
                cy = y_offset + rows * cell_size
                self.draw_wall(draw, cx, cy, cx + cell_size, cy)


class MosaicWallRenderer(WallRenderer):
    """Renders walls as mosaic tiles - small rectangles with gaps and color variation."""

    def __init__(
        self,
        base_color: str = "#1A1A1A",
        tile_size: int = 6,
        gap: int = 2
    ):
        """Initialize the mosaic renderer.

        Args:
            base_color: Hex color string for tiles
            tile_size: Size of each tile in pixels
            gap: Gap between tiles in pixels
        """
        super().__init__(base_color)
        self.tile_size = tile_size
        self.gap = gap

    def draw_wall(
        self,
        draw: ImageDraw,
        x1: int, y1: int,
        x2: int, y2: int
    ):
        """Draw a wall segment as mosaic tiles."""
        # Determine if horizontal or vertical
        if abs(x2 - x1) > abs(y2 - y1):
            # Horizontal wall
            start_x, end_x = min(x1, x2), max(x1, x2)
            y = y1
            x = start_x
            while x < end_x:
                # Vary color slightly for each tile
                factor = random.uniform(0.7, 1.3)
                tile_color = tuple(max(0, min(255, int(c * factor))) for c in self.base_rgb)

                tile_end = min(x + self.tile_size, end_x)
                half_tile = self.tile_size // 2
                draw.rectangle([x, y - half_tile, tile_end, y + half_tile], fill=tile_color)
                x += self.tile_size + self.gap
        else:
            # Vertical wall
            start_y, end_y = min(y1, y2), max(y1, y2)
            x = x1
            y = start_y
            while y < end_y:
                # Vary color slightly for each tile
                factor = random.uniform(0.7, 1.3)
                tile_color = tuple(max(0, min(255, int(c * factor))) for c in self.base_rgb)

                tile_end = min(y + self.tile_size, end_y)
                half_tile = self.tile_size // 2
                draw.rectangle([x - half_tile, y, x + half_tile, tile_end], fill=tile_color)
                y += self.tile_size + self.gap


class SolidWallRenderer(WallRenderer):
    """Renders walls as solid lines."""

    def __init__(
        self,
        base_color: str = "#1A1A1A",
        thickness: int = 4
    ):
        """Initialize the solid wall renderer.

        Args:
            base_color: Hex color string for walls
            thickness: Line thickness in pixels
        """
        super().__init__(base_color)
        self.thickness = thickness

    def draw_wall(
        self,
        draw: ImageDraw,
        x1: int, y1: int,
        x2: int, y2: int
    ):
        """Draw a wall segment as a solid line."""
        draw.line([(x1, y1), (x2, y2)], fill=self.base_color, width=self.thickness)


class SnakeWallRenderer(WallRenderer):
    """Renders walls with a snake/serpent scale pattern.

    Creates a textured wall that looks like snake scales,
    perfect for snake-themed mazes.
    """

    def __init__(
        self,
        base_color: str = "#2E8B57",  # Sea green default
        scale_size: int = 8,
        scale_variation: float = 0.2
    ):
        """Initialize the snake wall renderer.

        Args:
            base_color: Hex color string for scales
            scale_size: Size of each scale in pixels
            scale_variation: Color variation factor (0-1)
        """
        super().__init__(base_color)
        self.scale_size = scale_size
        self.scale_variation = scale_variation

    def _draw_scale(self, draw: ImageDraw, cx: int, cy: int, horizontal: bool, row_offset: int = 0):
        """Draw a single snake scale with realistic overlapping pattern."""
        # Vary color for each scale - lighter in center, darker at edges
        variation = 1.0 + random.uniform(-self.scale_variation, self.scale_variation)
        scale_color = tuple(max(0, min(255, int(c * variation))) for c in self.base_rgb)

        # Darker outline color
        outline_color = tuple(max(0, int(c * 0.6)) for c in self.base_rgb)

        # Highlight color for 3D effect
        highlight = tuple(min(255, int(c * 1.3)) for c in scale_color)

        half = self.scale_size // 2
        quarter = self.scale_size // 4

        if horizontal:
            # Draw U-shaped scale pointing down (like fish/snake scales)
            # Main scale body
            draw.ellipse(
                [cx - half, cy - half, cx + half, cy + half + quarter],
                fill=scale_color,
                outline=outline_color
            )
            # Highlight arc at top
            draw.arc(
                [cx - half + 2, cy - half + 2, cx + half - 2, cy + quarter],
                start=200, end=340,
                fill=highlight,
                width=1
            )
        else:
            # Draw scale pointing sideways for vertical walls
            draw.ellipse(
                [cx - half - quarter, cy - half, cx + half, cy + half],
                fill=scale_color,
                outline=outline_color
            )
            # Highlight arc
            draw.arc(
                [cx - half - quarter + 2, cy - half + 2, cx + half - 2, cy + half - 2],
                start=110, end=250,
                fill=highlight,
                width=1
            )

    def draw_wall(
        self,
        draw: ImageDraw,
        x1: int, y1: int,
        x2: int, y2: int
    ):
        """Draw a wall segment as overlapping snake scales."""
        # Determine if horizontal or vertical
        if abs(x2 - x1) > abs(y2 - y1):
            # Horizontal wall - draw two rows of overlapping scales
            start_x, end_x = min(x1, x2), max(x1, x2)
            y = y1

            # First row
            x = start_x + self.scale_size // 2
            while x < end_x:
                self._draw_scale(draw, x, y - 2, horizontal=True, row_offset=0)
                x += self.scale_size - 1

            # Second row (offset for overlap effect)
            x = start_x + self.scale_size
            while x < end_x:
                self._draw_scale(draw, x, y + 2, horizontal=True, row_offset=1)
                x += self.scale_size - 1
        else:
            # Vertical wall - draw two columns of overlapping scales
            start_y, end_y = min(y1, y2), max(y1, y2)
            x = x1

            # First column
            y = start_y + self.scale_size // 2
            while y < end_y:
                self._draw_scale(draw, x - 2, y, horizontal=False, row_offset=0)
                y += self.scale_size - 1

            # Second column (offset)
            y = start_y + self.scale_size
            while y < end_y:
                self._draw_scale(draw, x + 2, y, horizontal=False, row_offset=1)
                y += self.scale_size - 1

    @staticmethod
    def draw_snake_head(draw: ImageDraw, cx: int, cy: int, size: int, color: str, direction: str = "down"):
        """Draw a snake head at the maze entrance.

        Args:
            draw: PIL ImageDraw object
            cx, cy: Center position
            size: Size of the head
            color: Hex color for the snake
            direction: 'up', 'down', 'left', 'right'
        """
        # Parse color
        hex_color = color.lstrip('#')
        base_rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        dark_rgb = tuple(max(0, int(c * 0.6)) for c in base_rgb)
        light_rgb = tuple(min(255, int(c * 1.2)) for c in base_rgb)

        half = size // 2
        quarter = size // 4

        if direction == "down":
            # Head shape - elongated oval pointing down
            draw.ellipse([cx - half, cy - quarter, cx + half, cy + half + quarter],
                        fill=base_rgb, outline=dark_rgb)
            # Eyes
            eye_y = cy
            draw.ellipse([cx - quarter - 2, eye_y - 3, cx - quarter + 4, eye_y + 3],
                        fill=(255, 215, 0), outline=dark_rgb)  # Gold eyes
            draw.ellipse([cx + quarter - 4, eye_y - 3, cx + quarter + 2, eye_y + 3],
                        fill=(255, 215, 0), outline=dark_rgb)
            # Pupils (slits)
            draw.line([(cx - quarter + 1, eye_y - 2), (cx - quarter + 1, eye_y + 2)],
                     fill=(0, 0, 0), width=2)
            draw.line([(cx + quarter - 1, eye_y - 2), (cx + quarter - 1, eye_y + 2)],
                     fill=(0, 0, 0), width=2)
            # Forked tongue
            tongue_y = cy + half + quarter
            draw.line([(cx, tongue_y), (cx, tongue_y + size // 3)], fill=(200, 50, 50), width=2)
            draw.line([(cx, tongue_y + size // 3), (cx - 4, tongue_y + size // 2)], fill=(200, 50, 50), width=2)
            draw.line([(cx, tongue_y + size // 3), (cx + 4, tongue_y + size // 2)], fill=(200, 50, 50), width=2)

        elif direction == "up":
            # Head pointing up
            draw.ellipse([cx - half, cy - half - quarter, cx + half, cy + quarter],
                        fill=base_rgb, outline=dark_rgb)
            eye_y = cy - quarter
            draw.ellipse([cx - quarter - 2, eye_y - 3, cx - quarter + 4, eye_y + 3],
                        fill=(255, 215, 0), outline=dark_rgb)
            draw.ellipse([cx + quarter - 4, eye_y - 3, cx + quarter + 2, eye_y + 3],
                        fill=(255, 215, 0), outline=dark_rgb)
            draw.line([(cx - quarter + 1, eye_y - 2), (cx - quarter + 1, eye_y + 2)],
                     fill=(0, 0, 0), width=2)
            draw.line([(cx + quarter - 1, eye_y - 2), (cx + quarter - 1, eye_y + 2)],
                     fill=(0, 0, 0), width=2)
            tongue_y = cy - half - quarter
            draw.line([(cx, tongue_y), (cx, tongue_y - size // 3)], fill=(200, 50, 50), width=2)
            draw.line([(cx, tongue_y - size // 3), (cx - 4, tongue_y - size // 2)], fill=(200, 50, 50), width=2)
            draw.line([(cx, tongue_y - size // 3), (cx + 4, tongue_y - size // 2)], fill=(200, 50, 50), width=2)

    @staticmethod
    def draw_snake_tail(draw: ImageDraw, cx: int, cy: int, size: int, color: str, direction: str = "up"):
        """Draw a snake tail at the maze exit.

        Args:
            draw: PIL ImageDraw object
            cx, cy: Center position
            size: Size of the tail
            color: Hex color for the snake
            direction: 'up', 'down', 'left', 'right'
        """
        # Parse color
        hex_color = color.lstrip('#')
        base_rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        dark_rgb = tuple(max(0, int(c * 0.6)) for c in base_rgb)

        half = size // 2

        if direction == "up":
            # Tail tapering upward
            points = [
                (cx - half, cy + half),      # Bottom left
                (cx + half, cy + half),      # Bottom right
                (cx + 3, cy - half),         # Top right (tapered)
                (cx - 3, cy - half),         # Top left (tapered)
            ]
            draw.polygon(points, fill=base_rgb, outline=dark_rgb)
            # Rattle segments
            for i in range(3):
                seg_y = cy - half - (i * 6) - 4
                seg_width = 4 - i
                draw.ellipse([cx - seg_width, seg_y - 3, cx + seg_width, seg_y + 3],
                           fill=base_rgb, outline=dark_rgb)

        elif direction == "down":
            # Tail tapering downward
            points = [
                (cx - half, cy - half),
                (cx + half, cy - half),
                (cx + 3, cy + half),
                (cx - 3, cy + half),
            ]
            draw.polygon(points, fill=base_rgb, outline=dark_rgb)
            for i in range(3):
                seg_y = cy + half + (i * 6) + 4
                seg_width = 4 - i
                draw.ellipse([cx - seg_width, seg_y - 3, cx + seg_width, seg_y + 3],
                           fill=base_rgb, outline=dark_rgb)


class DottedWallRenderer(WallRenderer):
    """Renders walls as dotted lines."""

    def __init__(
        self,
        base_color: str = "#1A1A1A",
        dot_size: int = 4,
        gap: int = 4
    ):
        """Initialize the dotted wall renderer.

        Args:
            base_color: Hex color string for dots
            dot_size: Diameter of each dot in pixels
            gap: Gap between dots in pixels
        """
        super().__init__(base_color)
        self.dot_size = dot_size
        self.gap = gap

    def draw_wall(
        self,
        draw: ImageDraw,
        x1: int, y1: int,
        x2: int, y2: int
    ):
        """Draw a wall segment as dots."""
        radius = self.dot_size // 2

        if abs(x2 - x1) > abs(y2 - y1):
            # Horizontal wall
            start_x, end_x = min(x1, x2), max(x1, x2)
            y = y1
            x = start_x + radius
            while x < end_x:
                draw.ellipse(
                    [x - radius, y - radius, x + radius, y + radius],
                    fill=self.base_color
                )
                x += self.dot_size + self.gap
        else:
            # Vertical wall
            start_y, end_y = min(y1, y2), max(y1, y2)
            x = x1
            y = start_y + radius
            while y < end_y:
                draw.ellipse(
                    [x - radius, y - radius, x + radius, y + radius],
                    fill=self.base_color
                )
                y += self.dot_size + self.gap


# Registry of available wall renderers
WALL_RENDERERS = {
    'mosaic': MosaicWallRenderer,
    'solid': SolidWallRenderer,
    'snake': SnakeWallRenderer,
    'dotted': DottedWallRenderer,
}


def get_wall_renderer(
    wall_type: str,
    base_color: str = "#1A1A1A",
    **kwargs
) -> WallRenderer:
    """Factory function to get a wall renderer by type.

    Args:
        wall_type: Type of wall renderer ('mosaic', 'solid', 'snake', 'dotted')
        base_color: Hex color string for walls
        **kwargs: Additional arguments for the specific renderer

    Returns:
        WallRenderer instance

    Raises:
        ValueError: If wall_type is not recognized
    """
    if wall_type not in WALL_RENDERERS:
        available = ', '.join(WALL_RENDERERS.keys())
        raise ValueError(f"Unknown wall type '{wall_type}'. Available types: {available}")

    renderer_class = WALL_RENDERERS[wall_type]

    # Build kwargs based on renderer type
    renderer_kwargs = {'base_color': base_color}

    if wall_type == 'mosaic':
        if 'tile_size' in kwargs:
            renderer_kwargs['tile_size'] = kwargs['tile_size']
        if 'tile_gap' in kwargs or 'gap' in kwargs:
            renderer_kwargs['gap'] = kwargs.get('tile_gap', kwargs.get('gap', 2))
    elif wall_type == 'solid':
        if 'wall_thickness' in kwargs or 'thickness' in kwargs:
            renderer_kwargs['thickness'] = kwargs.get('wall_thickness', kwargs.get('thickness', 4))
    elif wall_type == 'snake':
        if 'scale_size' in kwargs:
            renderer_kwargs['scale_size'] = kwargs['scale_size']
        if 'scale_variation' in kwargs:
            renderer_kwargs['scale_variation'] = kwargs['scale_variation']
    elif wall_type == 'dotted':
        if 'dot_size' in kwargs:
            renderer_kwargs['dot_size'] = kwargs['dot_size']
        if 'gap' in kwargs:
            renderer_kwargs['gap'] = kwargs['gap']

    return renderer_class(**renderer_kwargs)
