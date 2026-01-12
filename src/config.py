"""
Configuration loader for card generation.

Loads card configuration from YAML files and provides defaults.
"""

import os
import yaml
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class ColorPalette:
    """Color palette for the card design."""
    primary: str = "#CD6839"      # Main background color (terracotta)
    secondary: str = "#1A1A1A"    # Text and outlines (black)
    accent: str = "#F5F0E6"       # Off-white/accent color

    def as_rgb(self, color: str) -> tuple:
        """Convert hex color to RGB tuple."""
        hex_color = color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


@dataclass
class FrontTextConfig:
    """Configuration for front card text."""
    header: str = "Happy Valentine's"
    header_font_size: int = 72
    # Pun line with emphasis - parts are: prefix, emphasized, suffix
    pun_prefix: str = "You are a"
    pun_emphasis: str = "MAZE"
    pun_suffix: str = "ing!"
    pun_font_size: int = 42
    pun_emphasis_font_size: int = 90
    # Artist credit
    credit: str = "art by Andrew Morris vanmorrisman@yahoo.co.uk"
    credit_font_size: int = 10


@dataclass
class BackTextConfig:
    """Configuration for back card text."""
    message: str = "From Felix"
    message_font_size: int = 48
    credit: str = "designed by Felix and his mom, Meghan"
    credit_font_size: int = 10
    # Maze labels
    start_label: str = "start"
    end_label: str = "end"


@dataclass
class MazeConfig:
    """Configuration for maze generation and rendering."""
    cell_size: int = 40
    # Wall renderer type: 'mosaic', 'solid', 'snake', 'dotted'
    wall_type: str = "mosaic"
    # Mosaic-specific settings
    tile_size: int = 6
    tile_gap: int = 2
    # Solid wall settings
    wall_thickness: int = 4
    # Snake-specific settings
    scale_size: int = 8
    scale_variation: float = 0.2
    # Dotted wall settings
    dot_size: int = 4
    dot_gap: int = 4
    # General settings
    wall_color: Optional[str] = None  # None = use secondary color


@dataclass
class CardConfig:
    """Complete card configuration."""
    # Basic info
    name: str = "valentine"
    description: str = "Valentine's Day card"

    # Hero image
    hero_image: Optional[str] = None  # Path relative to assets/artwork/
    hero_nudge_x: int = -12  # Optical adjustment for centering

    # Colors
    colors: ColorPalette = field(default_factory=ColorPalette)

    # Text
    front_text: FrontTextConfig = field(default_factory=FrontTextConfig)
    back_text: BackTextConfig = field(default_factory=BackTextConfig)

    # Maze
    maze: MazeConfig = field(default_factory=MazeConfig)

    # Card dimensions (at 300 DPI)
    width: int = 750   # 2.5 inches
    height: int = 1050  # 3.5 inches

    # Visual options
    add_texture: bool = True
    border_width: int = 40


def load_config(config_path: str) -> CardConfig:
    """Load card configuration from a YAML file.

    Args:
        config_path: Path to the YAML configuration file

    Returns:
        CardConfig object with loaded settings
    """
    with open(config_path, 'r') as f:
        data = yaml.safe_load(f)

    return _dict_to_config(data)


def _dict_to_config(data: Dict[str, Any]) -> CardConfig:
    """Convert a dictionary to a CardConfig object."""
    config = CardConfig()

    if not data:
        return config

    # Basic fields
    if 'name' in data:
        config.name = data['name']
    if 'description' in data:
        config.description = data['description']
    if 'hero_image' in data:
        config.hero_image = data['hero_image']
    if 'hero_nudge_x' in data:
        config.hero_nudge_x = data['hero_nudge_x']
    if 'width' in data:
        config.width = data['width']
    if 'height' in data:
        config.height = data['height']
    if 'add_texture' in data:
        config.add_texture = data['add_texture']
    if 'border_width' in data:
        config.border_width = data['border_width']

    # Colors
    if 'colors' in data:
        colors = data['colors']
        config.colors = ColorPalette(
            primary=colors.get('primary', config.colors.primary),
            secondary=colors.get('secondary', config.colors.secondary),
            accent=colors.get('accent', config.colors.accent),
        )

    # Front text
    if 'front_text' in data:
        ft = data['front_text']
        config.front_text = FrontTextConfig(
            header=ft.get('header', config.front_text.header),
            header_font_size=ft.get('header_font_size', config.front_text.header_font_size),
            pun_prefix=ft.get('pun_prefix', config.front_text.pun_prefix),
            pun_emphasis=ft.get('pun_emphasis', config.front_text.pun_emphasis),
            pun_suffix=ft.get('pun_suffix', config.front_text.pun_suffix),
            pun_font_size=ft.get('pun_font_size', config.front_text.pun_font_size),
            pun_emphasis_font_size=ft.get('pun_emphasis_font_size', config.front_text.pun_emphasis_font_size),
            credit=ft.get('credit', config.front_text.credit),
            credit_font_size=ft.get('credit_font_size', config.front_text.credit_font_size),
        )

    # Back text
    if 'back_text' in data:
        bt = data['back_text']
        config.back_text = BackTextConfig(
            message=bt.get('message', config.back_text.message),
            message_font_size=bt.get('message_font_size', config.back_text.message_font_size),
            credit=bt.get('credit', config.back_text.credit),
            credit_font_size=bt.get('credit_font_size', config.back_text.credit_font_size),
            start_label=bt.get('start_label', config.back_text.start_label),
            end_label=bt.get('end_label', config.back_text.end_label),
        )

    # Maze
    if 'maze' in data:
        m = data['maze']
        config.maze = MazeConfig(
            cell_size=m.get('cell_size', config.maze.cell_size),
            wall_type=m.get('wall_type', config.maze.wall_type),
            tile_size=m.get('tile_size', config.maze.tile_size),
            tile_gap=m.get('tile_gap', config.maze.tile_gap),
            wall_thickness=m.get('wall_thickness', config.maze.wall_thickness),
            scale_size=m.get('scale_size', config.maze.scale_size),
            scale_variation=m.get('scale_variation', config.maze.scale_variation),
            dot_size=m.get('dot_size', config.maze.dot_size),
            dot_gap=m.get('dot_gap', config.maze.dot_gap),
            wall_color=m.get('wall_color', config.maze.wall_color),
        )

    return config


def get_default_config() -> CardConfig:
    """Get the default Valentine's card configuration."""
    return CardConfig()


def save_config(config: CardConfig, output_path: str):
    """Save a card configuration to a YAML file.

    Args:
        config: CardConfig object to save
        output_path: Path to save the YAML file
    """
    data = {
        'name': config.name,
        'description': config.description,
        'hero_image': config.hero_image,
        'hero_nudge_x': config.hero_nudge_x,
        'width': config.width,
        'height': config.height,
        'add_texture': config.add_texture,
        'border_width': config.border_width,
        'colors': {
            'primary': config.colors.primary,
            'secondary': config.colors.secondary,
            'accent': config.colors.accent,
        },
        'front_text': {
            'header': config.front_text.header,
            'header_font_size': config.front_text.header_font_size,
            'pun_prefix': config.front_text.pun_prefix,
            'pun_emphasis': config.front_text.pun_emphasis,
            'pun_suffix': config.front_text.pun_suffix,
            'pun_font_size': config.front_text.pun_font_size,
            'pun_emphasis_font_size': config.front_text.pun_emphasis_font_size,
            'credit': config.front_text.credit,
            'credit_font_size': config.front_text.credit_font_size,
        },
        'back_text': {
            'message': config.back_text.message,
            'message_font_size': config.back_text.message_font_size,
            'credit': config.back_text.credit,
            'credit_font_size': config.back_text.credit_font_size,
            'start_label': config.back_text.start_label,
            'end_label': config.back_text.end_label,
        },
        'maze': {
            'cell_size': config.maze.cell_size,
            'wall_type': config.maze.wall_type,
            'tile_size': config.maze.tile_size,
            'tile_gap': config.maze.tile_gap,
            'wall_thickness': config.maze.wall_thickness,
            'scale_size': config.maze.scale_size,
            'scale_variation': config.maze.scale_variation,
            'dot_size': config.maze.dot_size,
            'dot_gap': config.maze.dot_gap,
            'wall_color': config.maze.wall_color,
        },
    }

    with open(output_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
