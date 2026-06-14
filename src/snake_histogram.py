#!/usr/bin/env python3
"""
Snake Histogram Generator

Generates an animated GIF showing a histogram where each bar is a
serpentine (S-curved) green snake. Bins 1-10 are always shown.

Usage:
    python src/snake_histogram.py
    python src/snake_histogram.py --counts 3 0 5 2 7 1 4 0 6 3
    python src/snake_histogram.py --output assets/snake_histogram.gif
"""

import math
import random
import argparse
import os
from PIL import Image, ImageDraw, ImageFont

# ── Canvas ────────────────────────────────────────────────────────────────────
WIDTH = 820
HEIGHT = 520
MARGIN_LEFT = 60
MARGIN_RIGHT = 20
MARGIN_TOP = 40
MARGIN_BOTTOM = 80

# ── Colors ────────────────────────────────────────────────────────────────────
BG_COLOR = (20, 35, 20)
SNAKE_BODY = (60, 200, 60)
SNAKE_DARK = (25, 110, 25)
SNAKE_HIGHLIGHT = (130, 255, 130)
SNAKE_HEAD = (40, 170, 40)
TONGUE_COLOR = (220, 50, 50)
EYE_COLOR = (255, 215, 0)
PUPIL_COLOR = (0, 0, 0)
AXIS_COLOR = (180, 200, 180)
LABEL_COLOR = (200, 230, 200)
GRID_COLOR = (40, 65, 40)
TITLE_COLOR = (140, 255, 140)


def _lerp(a, b, t):
    return a + (b - a) * t


def _path_points(x_center, y_bottom, y_top, col_width):
    """Return the sinusoidal spine points for a snake bar."""
    height = y_bottom - y_top
    amplitude = col_width * 0.28
    frequency = (2 * math.pi) / 50.0
    steps = max(120, int(height * 2))
    pts = []
    for i in range(steps + 1):
        t = i / steps
        y = y_bottom - t * height
        x = x_center + amplitude * math.sin(frequency * t * height)
        pts.append((x, y))
    return pts


def _cumulative_distances(pts):
    """Return cumulative arc-length distances along pts."""
    cum = [0.0]
    for i in range(1, len(pts)):
        dx = pts[i][0] - pts[i - 1][0]
        dy = pts[i][1] - pts[i - 1][1]
        cum.append(cum[-1] + math.sqrt(dx * dx + dy * dy))
    return cum


def _point_at_dist(pts, cum, d):
    """Interpolate position and tangent direction at arc-length d."""
    if d <= 0:
        return pts[0], (0.0, -1.0)
    if d >= cum[-1]:
        return pts[-1], (0.0, -1.0)
    # binary-search for the segment
    lo, hi = 0, len(cum) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if cum[mid] < d:
            lo = mid
        else:
            hi = mid
    t = (d - cum[lo]) / max(1e-9, cum[hi] - cum[lo])
    x = pts[lo][0] + t * (pts[hi][0] - pts[lo][0])
    y = pts[lo][1] + t * (pts[hi][1] - pts[lo][1])
    dx = pts[hi][0] - pts[lo][0]
    dy = pts[hi][1] - pts[lo][1]
    length = math.sqrt(dx * dx + dy * dy) or 1e-9
    return (x, y), (dx / length, dy / length)


def _rotated_ellipse_poly(cx, cy, tang, rw, rh, n=12):
    """
    Return an n-point polygon for an ellipse centred at (cx,cy),
    with half-width rw perpendicular to tang and half-height rh along tang.
    """
    tx, ty = tang
    px, py = -ty, tx   # perpendicular
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n
        lx = rw * math.cos(a)   # across body
        ly = rh * math.sin(a)   # along body
        pts.append((cx + lx * px + ly * tx,
                    cy + lx * py + ly * ty))
    return pts


def draw_serpentine_body(draw, x_center, y_bottom, y_top, col_width, body_width=14):
    """
    Draw a serpentine snake body with overlapping scale ellipses that follow
    the sinusoidal spine.  Scales are wider than tall and overlap by ~40 %,
    creating a realistic roof-tile / reptile texture.
    """
    if y_top >= y_bottom:
        return None

    pts = _path_points(x_center, y_bottom, y_top, col_width)
    cum = _cumulative_distances(pts)
    total_len = cum[-1]

    rw = body_width * 0.62    # half-width of each scale (across body)
    rh = body_width * 0.45    # half-height of each scale (along body)
    spacing = rh * 1.2        # ~40 % overlap between rows

    # ── 1. Shadow ─────────────────────────────────────────────────────────────
    for i in range(len(pts) - 1):
        draw.line(
            [(pts[i][0] + 2, pts[i][1] + 2), (pts[i + 1][0] + 2, pts[i + 1][1] + 2)],
            fill=SNAKE_DARK, width=body_width + 4,
        )

    # ── 2. Base body so no gaps show through ──────────────────────────────────
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=SNAKE_BODY, width=body_width)

    # ── 3. Overlapping scale ellipses, tail → head ────────────────────────────
    d = spacing * 0.4
    while d < total_len:
        (cx, cy), tang = _point_at_dist(pts, cum, d)

        v = random.uniform(0.82, 1.18)
        sc       = tuple(max(0, min(255, int(c * v)))    for c in SNAKE_BODY)
        dark_sc  = tuple(max(0, int(c * 0.5))            for c in sc)
        hi_sc    = tuple(min(255, int(c * 1.5))          for c in sc)

        # Main scale
        poly = _rotated_ellipse_poly(cx, cy, tang, rw, rh)
        draw.polygon(poly, fill=sc, outline=dark_sc)

        # Small highlight in the upper-third of the scale
        hi_poly = _rotated_ellipse_poly(cx, cy, tang, rw * 0.5, rh * 0.3)
        draw.polygon(hi_poly, fill=hi_sc)

        d += spacing

    # ── 4. Thin centre highlight along the spine ───────────────────────────────
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=SNAKE_HIGHLIGHT,
                  width=max(1, body_width // 6))

    return pts


def draw_snake_head(draw, x, y, facing_right=True, size=18):
    """Draw a small snake head at position (x, y)."""
    hw = size
    hh = size // 2 + 4
    # Head oval
    draw.ellipse([x - hw, y - hh, x + hw, y + hh], fill=SNAKE_HEAD, outline=SNAKE_DARK)
    # Eye
    ex = x + (hw // 2 if facing_right else -hw // 2)
    ey = y - hh // 3
    draw.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=EYE_COLOR, outline=SNAKE_DARK)
    draw.ellipse([ex - 2, ey - 2, ex + 2, ey + 2], fill=PUPIL_COLOR)
    # Tongue
    tx = x + (hw if facing_right else -hw)
    draw.line([(x + (hw - 4 if facing_right else -(hw - 4)), y), (tx, y)],
              fill=TONGUE_COLOR, width=2)
    draw.line([(tx, y), (tx + (5 if facing_right else -5), y - 4)],
              fill=TONGUE_COLOR, width=2)
    draw.line([(tx, y), (tx + (5 if facing_right else -5), y + 4)],
              fill=TONGUE_COLOR, width=2)


def make_frame(counts, reveal_frac=1.0, show_head=True):
    """
    Render one animation frame.

    counts   : list of 10 integers, index 0 = bin 1, ..., index 9 = bin 10
    reveal_frac : 0.0 = nothing drawn, 1.0 = fully drawn (controls animation)
    """
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # ── Axes ──────────────────────────────────────────────────────────────────
    chart_left = MARGIN_LEFT
    chart_right = WIDTH - MARGIN_RIGHT
    chart_top = MARGIN_TOP
    chart_bottom = HEIGHT - MARGIN_BOTTOM

    chart_w = chart_right - chart_left
    chart_h = chart_bottom - chart_top

    max_count = 10  # fixed y-axis 0-10

    # Horizontal grid lines, one per integer 0-10
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except Exception:
        font = ImageFont.load_default()
    for g in range(max_count + 1):
        gy = chart_bottom - int(g / max_count * chart_h)
        draw.line([(chart_left, gy), (chart_right, gy)], fill=GRID_COLOR, width=1)
        draw.text((chart_left - 25, gy - 8), str(g), fill=AXIS_COLOR, font=font)

    # Axes lines
    draw.line([(chart_left, chart_top), (chart_left, chart_bottom)],
              fill=AXIS_COLOR, width=2)
    draw.line([(chart_left, chart_bottom), (chart_right, chart_bottom)],
              fill=AXIS_COLOR, width=2)

    # ── Title ─────────────────────────────────────────────────────────────────
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except Exception:
        title_font = ImageFont.load_default()
        label_font = ImageFont.load_default()

    title = "Dreamsnake Book Club Ratings"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    tx = (WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((tx, 8), title, fill=TITLE_COLOR, font=title_font)

    # ── Bars (serpentine snakes) ───────────────────────────────────────────────
    n_bins = 10
    col_total = chart_w / n_bins
    col_width = col_total * 0.65  # bar width
    col_gap = col_total * 0.35

    for i in range(n_bins):
        bin_label = str(i + 1)
        count = counts[i]

        col_center_x = chart_left + (i + 0.5) * col_total

        # X-axis label
        bbox = draw.textbbox((0, 0), bin_label, font=label_font)
        lw = bbox[2] - bbox[0]
        draw.text(
            (col_center_x - lw / 2, chart_bottom + 10),
            bin_label,
            fill=LABEL_COLOR,
            font=label_font,
        )

        if count == 0:
            continue

        # Bar height based on count, scaled by reveal_frac
        bar_full_h = int((count / max_count) * chart_h)
        bar_h = int(bar_full_h * reveal_frac)
        if bar_h < 4:
            continue

        y_bottom = chart_bottom - 1
        y_top = y_bottom - bar_h

        pts = draw_serpentine_body(
            draw,
            col_center_x,
            y_bottom,
            y_top,
            col_width,
            body_width=int(col_width * 0.28),
        )

        # Head at the tip (alternates left/right with the sine wave direction)
        if show_head and pts and reveal_frac > 0.05:
            tip = pts[-1]
            # Determine which direction the snake is facing at the tip
            if len(pts) >= 2:
                dx = pts[-1][0] - pts[-2][0]
                facing_right = dx >= 0
            else:
                facing_right = True
            draw_snake_head(draw, int(tip[0]), int(tip[1]),
                            facing_right=facing_right, size=int(col_width * 0.18))

    return img


def generate_histogram_gif(counts, output_path, fps=24, duration_s=1.5):
    """
    Generate an animated GIF where snakes grow upward into the histogram bars.

    counts      : list of exactly 10 non-negative integers
    output_path : path for the .gif file
    fps         : frames per second
    duration_s  : total animation duration in seconds
    """
    assert len(counts) == 10, "Need exactly 10 count values (bins 1-10)"

    n_frames = max(12, int(fps * duration_s))
    frames = []

    for f in range(n_frames):
        # Ease-in-out reveal
        t = f / (n_frames - 1)
        ease = t * t * (3 - 2 * t)  # smoothstep
        frame = make_frame(counts, reveal_frac=ease, show_head=(f > 0))
        frames.append(frame)

    # Hold the final frame a bit longer
    for _ in range(fps):
        frames.append(make_frame(counts, reveal_frac=1.0, show_head=True))

    frame_duration_ms = int(1000 / fps)

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        loop=0,
        duration=frame_duration_ms,
        optimize=False,
    )
    print(f"Saved: {output_path}  ({len(frames)} frames @ {fps} fps)")


def main():
    parser = argparse.ArgumentParser(description="Generate an animated snake histogram GIF.")
    parser.add_argument(
        "--counts",
        type=int,
        nargs=10,
        default=[0, 0, 0, 0, 3, 7, 2, 0, 1, 0],
        metavar="N",
        help="10 count values for bins 1-10 (default: sample data)",
    )
    parser.add_argument(
        "--output",
        default=os.path.join(
            os.path.dirname(__file__), "..", "assets", "snake_histogram.gif"
        ),
        help="Output GIF path",
    )
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--duration", type=float, default=1.5,
                        help="Animation grow duration in seconds")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    generate_histogram_gif(args.counts, args.output, fps=args.fps, duration_s=args.duration)


if __name__ == "__main__":
    main()
