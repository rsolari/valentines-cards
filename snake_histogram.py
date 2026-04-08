import math
from collections import Counter
from PIL import Image, ImageDraw, ImageFont

# --- Data ---
data = [5, 5, 6, 6, 7, 5, 6, 6, 9, 6, 6, 6, 7]
counts   = Counter(data)
values   = list(range(1, 11))
freqs    = [counts.get(v, 0) for v in values]
max_freq = max(freqs)

# --- Layout ---
BAR_W    = 72
BAR_GAP  = 16
SEG_H    = 58
HEAD_H   = 74   # vertical space reserved for the head above the body
TOP_PAD  = 80   # room for title + count labels
BOT_PAD  = 62

n        = len(values)
total_w  = n * BAR_W + (n - 1) * BAR_GAP
SIDE_PAD = 55
canvas_w = total_w + 2 * SIDE_PAD
canvas_h = TOP_PAD + HEAD_H + max_freq * SEG_H + BOT_PAD

# Baseline y (top of x-axis)
GROUND_Y = TOP_PAD + HEAD_H + max_freq * SEG_H

# --- Snake body parameters ---
BODY_R    = 14   # radius of each body circle
AMPLITUDE = 11   # left/right oscillation (px)
PERIOD    = 2.2  # segments per full sine wave

# --- Colours (all green) ---
C_DARK   = ( 28, 105,  52)   # outer / shadow
C_MID    = ( 52, 155,  80)   # mid-tone body
C_LIGHT  = ( 88, 200, 115)   # top highlight
C_SPEC   = (155, 235, 170)   # specular
C_HEAD   = ( 65, 175,  95)   # head fill
C_SCALE  = ( 42, 130,  65)   # scale marks

BG       = ( 14,  14,  28)
TONGUE   = (210,  35,  35)
EYE_W    = (255, 255, 255)
EYE_P    = ( 15,  15,  15)
LABEL_C  = (170, 170, 200)
TITLE_C  = (230, 230, 255)

FONT_BOLD  = ImageFont.truetype(
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
FONT_SM    = ImageFont.truetype(
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
FONT_TITLE = ImageFont.truetype(
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)


def text_center(d, text, cx, y, font, fill):
    bbox = d.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    d.text((cx - w // 2, y), text, font=font, fill=fill)


def body_points(cx, freq):
    """Sample points along the sine-wave spine of the snake body."""
    total_h  = freq * SEG_H
    period_h = PERIOD * SEG_H
    steps    = max(80, total_h * 6)
    pts = []
    for i in range(steps + 1):
        t     = i / steps
        y     = GROUND_Y - t * total_h
        phase = (t * total_h / period_h) * 2 * math.pi
        x     = cx + AMPLITUDE * math.sin(phase)
        pts.append((x, y))
    return pts


def draw_body(d, pts):
    """Draw serpentine snake body as layered overlapping circles."""
    # 1. Dark base silhouette
    for px, py in pts:
        r = BODY_R
        d.ellipse([px - r, py - r, px + r, py + r], fill=(*C_DARK, 255))

    # 2. Mid-tone (slightly smaller, offset up → light-from-above illusion)
    hi_r   = int(BODY_R * 0.72)
    hi_off = -4
    for px, py in pts[::2]:
        d.ellipse([px - hi_r, py + hi_off - hi_r,
                   px + hi_r, py + hi_off + hi_r], fill=(*C_MID, 230))

    # 3. Soft highlight ridge
    lr   = int(BODY_R * 0.38)
    loff = -7
    for px, py in pts[::3]:
        d.ellipse([px - lr, py + loff - lr,
                   px + lr, py + loff + lr], fill=(*C_LIGHT, 180))

    # 4. Specular gleam
    sr   = int(BODY_R * 0.18)
    soff = -9
    for px, py in pts[::5]:
        d.ellipse([px - sr, py + soff - sr,
                   px + sr, py + soff + sr], fill=(*C_SPEC, 130))

    # 5. Scale marks — small horizontal ovals spaced along the body
    step = max(1, len(pts) // (max(1, len(pts) // 12)))
    for i in range(0, len(pts), step):
        px, py = pts[i]
        sw, sh = int(BODY_R * 0.55), int(BODY_R * 0.28)
        d.ellipse([px - sw, py - sh, px + sw, py + sh],
                  fill=(*C_SCALE, 140))


def draw_head(d, cx, body_top_y, tongue_frac):
    """Draw the snake head above body_top_y and animate the tongue."""
    hw  = BODY_R + 10   # head half-width
    hh  = HEAD_H // 2   # head half-height
    hcy = body_top_y - hh

    # Head ellipse
    d.ellipse([cx - hw, hcy - hh, cx + hw, hcy + hh], fill=(*C_HEAD, 255))

    # Sheen on head
    d.ellipse([cx - int(hw * 0.55), hcy - int(hh * 0.65),
               cx + int(hw * 0.55), hcy + int(hh * 0.05)],
              fill=(*C_LIGHT, 90))

    # Eyes
    eye_y = int(hcy - hh * 0.22)
    for ex, px_off in [(cx - int(hw * 0.52), 1), (cx + int(hw * 0.52), -1)]:
        d.ellipse([ex - 10, eye_y - 10, ex + 10, eye_y + 10], fill=(*EYE_W, 255))
        d.ellipse([ex - 6 + px_off, eye_y - 6,
                   ex + 6 + px_off, eye_y + 6],  fill=(*EYE_P, 255))
        d.ellipse([ex - 2, eye_y - 5, ex + 2, eye_y - 1],
                  fill=(255, 255, 255, 210))   # gleam

    # Nostrils
    ny = int(hcy + hh * 0.52)
    for nx_off in [int(-hw * 0.32), int(hw * 0.32) - 6]:
        d.ellipse([cx + nx_off - 3, ny - 2, cx + nx_off + 3, ny + 2],
                  fill=(*C_DARK, 255))

    # Tongue (animated)
    tx        = cx
    t_start_y = hcy - hh          # tip of head (top)
    max_stem  = 30
    max_fork  = 13
    stem = int(max_stem * tongue_frac)
    fork = int(max_fork * tongue_frac)
    if stem > 4:
        d.line([(tx, t_start_y), (tx, t_start_y - stem)],
               fill=(*TONGUE, 255), width=3)
    if fork > 3:
        tip = t_start_y - stem
        d.line([(tx, tip), (tx - fork, tip - fork)], fill=(*TONGUE, 255), width=2)
        d.line([(tx, tip), (tx + fork, tip - fork)], fill=(*TONGUE, 255), width=2)

    return hcy - hh   # top-of-head y, for count label placement


def draw_frame(tongue_frac: float) -> Image.Image:
    img = Image.new('RGBA', (canvas_w, canvas_h), (*BG, 255))
    d   = ImageDraw.Draw(img, 'RGBA')

    # Grid lines
    for i in range(1, max_freq + 1):
        gy = GROUND_Y - i * SEG_H
        d.line([(SIDE_PAD - 10, gy), (SIDE_PAD + total_w + 10, gy)],
               fill=(255, 255, 255, 16), width=1)

    # Ground line
    d.line([(SIDE_PAD - 10, GROUND_Y), (SIDE_PAD + total_w + 10, GROUND_Y)],
           fill=(255, 255, 255, 55), width=2)

    for idx, (val, freq) in enumerate(zip(values, freqs)):
        bx = SIDE_PAD + idx * (BAR_W + BAR_GAP)
        cx = bx + BAR_W // 2

        # X-axis label (always shown, even for freq=0)
        text_center(d, str(val), cx, GROUND_Y + 14, FONT_BOLD, (*LABEL_C, 255))

        if freq == 0:
            continue

        # Serpentine body
        pts = body_points(cx, freq)
        draw_body(d, pts)

        # Head (body top is always at (cx, GROUND_Y - freq*SEG_H))
        body_top_y = GROUND_Y - freq * SEG_H
        head_top_y = draw_head(d, cx, body_top_y, tongue_frac)

        # Count label above the head
        text_center(d, str(freq), cx, head_top_y - 22, FONT_SM, (*LABEL_C, 200))

    # Title
    text_center(d, "Snake Histogram", canvas_w // 2, 14, FONT_TITLE, (*TITLE_C, 255))

    return img.convert('RGB')


# --- Animation: tongue flicker ---
tongue_states = [1.0, 1.0, 0.70, 0.35, 0.08, 0.0, 0.0, 0.08, 0.35, 0.70]
durations     = [110, 110,   75,   60,   55, 175, 175,   55,   60,   75]

frames   = [draw_frame(t) for t in tongue_states]
frames_p = [f.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=1)
            for f in frames]

out_path = '/home/user/valentines-cards/snake_histogram.gif'
frames_p[0].save(
    out_path,
    save_all=True,
    append_images=frames_p[1:],
    loop=0,
    duration=durations,
    optimize=False,
)
print(f"Saved → {out_path}  ({canvas_w}×{canvas_h}px, {len(frames)} frames)")
