# Valentine's Cards - Pixel Minotaur Maze

A creative project combining pixel art and maze algorithms to create printable Valentine's cards.

## Project Overview

Create unique Valentine's cards featuring:
- **Front**: Pixel art minotaur with a Valentine's greeting
- **Back**: A procedurally generated maze puzzle

## Card Specifications

| Property | Value |
|----------|-------|
| Size | 3.5" x 2.5" (standard trading card) |
| Resolution | 300 DPI (recommended for print) |
| Pixel Dimensions | 1050 x 750 pixels |
| Bleed Area | Add 0.125" (37.5px) on each side for print bleed |
| Safe Zone | Keep important content 0.125" from edges |

## Project Structure

```
valentines-cards/
├── assets/
│   ├── artwork/        # Minotaur artwork and Valentine designs
│   ├── mazes/          # Generated maze images
│   └── templates/      # Print-ready card templates
├── src/                # Maze generation scripts
├── docs/               # Documentation and tutorials
└── README.md
```

## Learning Goals

### Pixel Art
- Understanding pixel art constraints and techniques
- Working with limited color palettes
- Creating character designs at small resolutions

### Maze Algorithms
- Depth-First Search (recursive backtracker)
- Prim's Algorithm
- Kruskal's Algorithm
- Understanding maze properties (solution path, dead ends, difficulty)

## Getting Started

1. See `docs/pixel-art-tools.md` for recommended pixel art editors
2. Run `python src/maze_generator.py` to create maze designs
3. Combine front and back designs using your preferred image editor

## The Minotaur Theme

In Greek mythology, the Minotaur dwelt in a labyrinth. This Valentine's card plays on that theme:
- The minotaur on the front offers a Valentine's greeting
- The maze on the back is "the minotaur's labyrinth"
- A fun puzzle element makes the card interactive!

## License

This project is for personal/educational use.
