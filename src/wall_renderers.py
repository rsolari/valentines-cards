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

    def _draw_scale(self, draw: ImageDraw, cx: int, cy: int, horizontal: bool):
        """Draw a single snake scale."""
        # Vary color for each scale
        variation = 1.0 + random.uniform(-self.scale_variation, self.scale_variation)
        scale_color = tuple(max(0, min(255, int(c * variation))) for c in self.base_rgb)

        half = self.scale_size // 2
        if horizontal:
            # Draw overlapping semicircle pattern for horizontal walls
            draw.ellipse(
                [cx - half, cy - half, cx + half, cy + half],
                fill=scale_color,
                outline=tuple(max(0, int(c * 0.7)) for c in self.base_rgb)
            )
        else:
            # Draw overlapping semicircle pattern for vertical walls
            draw.ellipse(
                [cx - half, cy - half, cx + half, cy + half],
                fill=scale_color,
                outline=tuple(max(0, int(c * 0.7)) for c in self.base_rgb)
            )

    def draw_wall(
        self,
        draw: ImageDraw,
        x1: int, y1: int,
        x2: int, y2: int
    ):
        """Draw a wall segment as snake scales."""
        # Determine if horizontal or vertical
        if abs(x2 - x1) > abs(y2 - y1):
            # Horizontal wall
            start_x, end_x = min(x1, x2), max(x1, x2)
            y = y1
            x = start_x + self.scale_size // 2
            while x < end_x:
                self._draw_scale(draw, x, y, horizontal=True)
                x += self.scale_size - 2  # Overlap scales slightly
        else:
            # Vertical wall
            start_y, end_y = min(y1, y2), max(y1, y2)
            x = x1
            y = start_y + self.scale_size // 2
            while y < end_y:
                self._draw_scale(draw, x, y, horizontal=False)
                y += self.scale_size - 2  # Overlap scales slightly


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
