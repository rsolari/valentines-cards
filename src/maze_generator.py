#!/usr/bin/env python3
"""
Maze Generator for Valentine's Cards

This script generates mazes using different algorithms, helping you learn
about maze generation while creating puzzles for the back of Valentine's cards.

Card specs: 3.5" x 2.5" at 300 DPI = 1050 x 750 pixels
"""

import random
from enum import Enum
from typing import List, Tuple, Set, Optional
from dataclasses import dataclass
from PIL import Image, ImageDraw


class Algorithm(Enum):
    """Available maze generation algorithms."""
    DFS = "dfs"              # Depth-First Search (Recursive Backtracker)
    PRIMS = "prims"          # Prim's Algorithm
    KRUSKALS = "kruskals"    # Kruskal's Algorithm


@dataclass
class MazeConfig:
    """Configuration for maze generation."""
    width: int = 21         # Cells wide (use odd numbers for clean walls)
    height: int = 15        # Cells tall (use odd numbers for clean walls)
    cell_size: int = 40     # Pixels per cell
    wall_color: str = "#8B0000"      # Dark red for Valentine theme
    path_color: str = "#FFF0F5"      # Lavender blush background
    start_color: str = "#FF69B4"     # Hot pink for start
    end_color: str = "#FF1493"       # Deep pink for end
    wall_thickness: int = 2


class Maze:
    """
    A maze represented as a 2D grid.

    The maze uses a grid where:
    - True = path (walkable)
    - False = wall
    """

    def __init__(self, width: int, height: int):
        # Ensure odd dimensions for proper maze structure
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        # Start with all walls
        self.grid = [[False] * self.width for _ in range(self.height)]
        self.start = (1, 1)
        self.end = (self.width - 2, self.height - 2)

    def is_valid(self, x: int, y: int) -> bool:
        """Check if coordinates are within the maze bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_wall(self, x: int, y: int) -> bool:
        """Check if a cell is a wall."""
        return not self.grid[y][x] if self.is_valid(x, y) else True

    def carve(self, x: int, y: int):
        """Make a cell into a path."""
        if self.is_valid(x, y):
            self.grid[y][x] = True

    def __str__(self) -> str:
        """ASCII representation of the maze."""
        result = []
        for y, row in enumerate(self.grid):
            line = ""
            for x, cell in enumerate(row):
                if (x, y) == self.start:
                    line += "S "
                elif (x, y) == self.end:
                    line += "E "
                elif cell:
                    line += "  "
                else:
                    line += "##"
            result.append(line)
        return "\n".join(result)


def generate_dfs(maze: Maze) -> Maze:
    """
    Depth-First Search (Recursive Backtracker) Algorithm

    HOW IT WORKS:
    1. Start at a random cell and mark it as part of the maze
    2. While there are unvisited cells:
       a. If current cell has unvisited neighbors:
          - Choose a random unvisited neighbor
          - Remove the wall between current and chosen cell
          - Move to the chosen cell and mark it visited
       b. Else, backtrack to the previous cell

    CHARACTERISTICS:
    - Creates mazes with long, winding corridors
    - Has a "river" quality - paths tend to go far before branching
    - Relatively few dead ends compared to other algorithms
    - Good for mazes that should have one obvious "main path"

    TIME COMPLEXITY: O(n) where n is the number of cells
    SPACE COMPLEXITY: O(n) for the recursion stack
    """
    # Directions: right, down, left, up (moving by 2 to skip wall cells)
    directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]

    # Start from top-left path cell
    start_x, start_y = 1, 1
    maze.carve(start_x, start_y)

    # Stack for backtracking (iterative version to avoid recursion limit)
    stack = [(start_x, start_y)]

    while stack:
        x, y = stack[-1]

        # Find unvisited neighbors (2 cells away)
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if maze.is_valid(nx, ny) and maze.is_wall(nx, ny):
                neighbors.append((nx, ny, dx // 2, dy // 2))

        if neighbors:
            # Choose random neighbor
            nx, ny, wall_dx, wall_dy = random.choice(neighbors)
            # Carve through the wall
            maze.carve(x + wall_dx, y + wall_dy)
            # Carve the new cell
            maze.carve(nx, ny)
            # Add to stack
            stack.append((nx, ny))
        else:
            # Backtrack
            stack.pop()

    return maze


def generate_prims(maze: Maze) -> Maze:
    """
    Prim's Algorithm (Randomized)

    HOW IT WORKS:
    1. Start with a grid of walls
    2. Pick a random cell, mark it as part of the maze
    3. Add the cell's walls to a wall list
    4. While there are walls in the list:
       a. Pick a random wall from the list
       b. If only one of the cells the wall divides is visited:
          - Make the wall a passage
          - Mark the unvisited cell as part of the maze
          - Add the neighboring walls of the cell to the wall list
       c. Remove the wall from the list

    CHARACTERISTICS:
    - Creates mazes with many short dead ends
    - More "branchy" appearance than DFS
    - Tends to have a more uniform distribution of paths
    - The maze "grows" outward from the starting point

    TIME COMPLEXITY: O(n log n) with efficient data structures
    SPACE COMPLEXITY: O(n) for the frontier set
    """
    directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]

    # Start from a random odd cell
    start_x, start_y = 1, 1
    maze.carve(start_x, start_y)

    # Frontier: walls that could potentially be carved
    frontier: Set[Tuple[int, int, int, int]] = set()

    # Add initial frontier
    for dx, dy in directions:
        nx, ny = start_x + dx, start_y + dy
        if maze.is_valid(nx, ny):
            # Store: (wall_x, wall_y, cell_x, cell_y)
            frontier.add((start_x + dx // 2, start_y + dy // 2, nx, ny))

    while frontier:
        # Pick random wall from frontier
        wall = random.choice(list(frontier))
        frontier.remove(wall)
        wall_x, wall_y, cell_x, cell_y = wall

        # If the cell on the other side hasn't been visited
        if maze.is_wall(cell_x, cell_y):
            # Carve the wall and the cell
            maze.carve(wall_x, wall_y)
            maze.carve(cell_x, cell_y)

            # Add new frontier walls
            for dx, dy in directions:
                nx, ny = cell_x + dx, cell_y + dy
                if maze.is_valid(nx, ny) and maze.is_wall(nx, ny):
                    frontier.add((cell_x + dx // 2, cell_y + dy // 2, nx, ny))

    return maze


class UnionFind:
    """
    Union-Find (Disjoint Set) data structure for Kruskal's algorithm.

    This efficiently tracks which cells are connected and allows us to
    quickly determine if adding an edge would create a cycle.
    """

    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x: int) -> int:
        """Find the root of x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Unite two sets. Returns True if they were separate."""
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        # Union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True


def generate_kruskals(maze: Maze) -> Maze:
    """
    Kruskal's Algorithm (Randomized)

    HOW IT WORKS:
    1. Create a list of all walls between cells
    2. Create a set for each cell (using Union-Find)
    3. Randomly shuffle the wall list
    4. For each wall:
       a. If the cells on either side belong to different sets:
          - Remove the wall (make it a passage)
          - Join the two sets

    CHARACTERISTICS:
    - Creates mazes with very uniform texture
    - Dead ends are evenly distributed
    - No bias toward any particular pattern
    - Cells don't "know" about maze boundaries during generation

    WHY UNION-FIND?
    - We need to track connected components efficiently
    - Union-Find provides near O(1) operations for this
    - Without it, we'd need expensive traversals to check connectivity

    TIME COMPLEXITY: O(n * α(n)) ≈ O(n) where α is inverse Ackermann
    SPACE COMPLEXITY: O(n) for Union-Find structure
    """
    # First, carve out all potential path cells
    cells = []
    for y in range(1, maze.height, 2):
        for x in range(1, maze.width, 2):
            cells.append((x, y))
            maze.carve(x, y)

    # Create mapping from cell position to index
    cell_to_idx = {cell: i for i, cell in enumerate(cells)}

    # Create all possible walls (edges between adjacent cells)
    walls = []
    for x, y in cells:
        # Right neighbor
        if x + 2 < maze.width:
            walls.append((x, y, x + 2, y, x + 1, y))
        # Down neighbor
        if y + 2 < maze.height:
            walls.append((x, y, x, y + 2, x, y + 1))

    # Shuffle walls for randomness
    random.shuffle(walls)

    # Union-Find to track connected components
    uf = UnionFind(len(cells))

    for x1, y1, x2, y2, wall_x, wall_y in walls:
        idx1 = cell_to_idx[(x1, y1)]
        idx2 = cell_to_idx[(x2, y2)]

        # If cells are in different sets, remove wall and unite them
        if uf.union(idx1, idx2):
            maze.carve(wall_x, wall_y)

    return maze


def generate_maze(config: MazeConfig, algorithm: Algorithm = Algorithm.DFS) -> Maze:
    """Generate a maze using the specified algorithm."""
    maze = Maze(config.width, config.height)

    generators = {
        Algorithm.DFS: generate_dfs,
        Algorithm.PRIMS: generate_prims,
        Algorithm.KRUSKALS: generate_kruskals,
    }

    return generators[algorithm](maze)


def render_maze(maze: Maze, config: MazeConfig) -> Image.Image:
    """
    Render the maze as a PIL Image suitable for printing.

    For a 3.5" x 2.5" card at 300 DPI:
    - Total size: 1050 x 750 pixels
    - We add margins to center the maze
    """
    # Calculate maze dimensions
    maze_width = maze.width * config.cell_size
    maze_height = maze.height * config.cell_size

    # Card dimensions at 300 DPI
    card_width = 1050
    card_height = 750

    # Create image with card dimensions
    img = Image.new('RGB', (card_width, card_height), config.path_color)
    draw = ImageDraw.Draw(img)

    # Center the maze on the card
    offset_x = (card_width - maze_width) // 2
    offset_y = (card_height - maze_height) // 2

    # Draw walls
    for y in range(maze.height):
        for x in range(maze.width):
            px = offset_x + x * config.cell_size
            py = offset_y + y * config.cell_size

            if maze.is_wall(x, y):
                draw.rectangle(
                    [px, py, px + config.cell_size, py + config.cell_size],
                    fill=config.wall_color
                )

    # Draw start and end markers
    start_x = offset_x + maze.start[0] * config.cell_size
    start_y = offset_y + maze.start[1] * config.cell_size
    draw.ellipse(
        [start_x + 5, start_y + 5,
         start_x + config.cell_size - 5, start_y + config.cell_size - 5],
        fill=config.start_color
    )

    end_x = offset_x + maze.end[0] * config.cell_size
    end_y = offset_y + maze.end[1] * config.cell_size
    draw.rectangle(
        [end_x + 5, end_y + 5,
         end_x + config.cell_size - 5, end_y + config.cell_size - 5],
        fill=config.end_color
    )

    return img


def main():
    """Generate sample mazes with different algorithms."""
    import os

    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "mazes")
    os.makedirs(output_dir, exist_ok=True)

    config = MazeConfig()

    print("Valentine's Maze Generator")
    print("=" * 40)
    print(f"Maze size: {config.width}x{config.height} cells")
    print(f"Card size: 3.5\" x 2.5\" (1050x750 pixels at 300 DPI)")
    print()

    for algorithm in Algorithm:
        print(f"Generating {algorithm.value.upper()} maze...")

        # Generate maze
        maze = generate_maze(config, algorithm)

        # Print ASCII version
        print(f"\n{algorithm.value.upper()} Maze (ASCII):")
        print(maze)
        print()

        # Render and save image
        img = render_maze(maze, config)
        filename = f"maze_{algorithm.value}.png"
        filepath = os.path.join(output_dir, filename)
        img.save(filepath, dpi=(300, 300))
        print(f"Saved: {filepath}")
        print()

    print("=" * 40)
    print("All mazes generated!")
    print("\nAlgorithm Comparison:")
    print("- DFS: Long winding paths, fewer dead ends, 'river-like'")
    print("- Prim's: Many short branches, uniform distribution")
    print("- Kruskal's: Very uniform texture, evenly distributed dead ends")


if __name__ == "__main__":
    main()
