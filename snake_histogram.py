from collections import Counter
from PIL import Image, ImageDraw, ImageFont

# --- Data ---
data = [5, 5, 6, 6, 7, 5, 6, 6, 9, 6, 6, 6, 7]
counts = Counter(data)
values = sorted(counts.keys())       # [5, 6, 7, 9]
frequencies = [counts[v] for v in values]  # [3, 7, 2, 1]
max_freq = max(frequencies)

# --- Layout ---
BAR_W    = 110
BAR_GAP  = 60
SEG_H    = 56
HEAD_H   = 80
TOP_PAD  = 50
BOT_PAD  = 60
SIDE_PAD = 70

n         = len(values)
total_w   = n * BAR_W + (n - 1) * BAR_GAP
canvas_w  = total_w + 2 * SIDE_PAD
canvas_h  = TOP_PAD + HEAD_H + max_freq * SEG_H + BOT_PAD

# --- Palette ---
BG       = (14, 14, 28)
TONGUE   = (210, 35, 35)
EYE_W    = (255, 255, 255)
EYE_P    = (12, 12, 12)
LABEL_C  = (170, 170, 200)
TITLE_C  = (230, 230, 255)

# Per-snake colour schemes: (body_a, body_b, head, scale_highlight)
SCHEMES = [
    ((58, 180, 100),  (34, 120, 65),   (90, 210, 130),  (100, 200, 130)),  # green
    ((240, 140, 50),  (190, 95,  20),  (255, 175, 85),  (250, 160, 80)),   # orange
    ((80,  155, 230), (45,  100, 185), (115, 185, 255), (100, 175, 245)),  # blue
    ((215, 95,  170), (165, 50,  125), (245, 135, 200), (230, 115, 185)),  # pink
]

# --- Fonts ---
FONT_BOLD  = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
FONT_REG   = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
FONT_TITLE = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)

def text_center(draw, text, cx, y, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text((cx - w // 2, y), text, font=font, fill=fill)

def draw_frame(tongue_frac: float) -> Image.Image:
    img = Image.new('RGBA', (canvas_w, canvas_h), (*BG, 255))
    d   = ImageDraw.Draw(img, 'RGBA')

    ground_y = TOP_PAD + HEAD_H + max_freq * SEG_H

    # Subtle horizontal grid lines
    for i in range(1, max_freq + 1):
        gy = ground_y - i * SEG_H
        d.line([(SIDE_PAD - 15, gy), (SIDE_PAD + total_w + 15, gy)],
               fill=(255, 255, 255, 18), width=1)

    # Ground line
    d.line([(SIDE_PAD - 15, ground_y), (SIDE_PAD + total_w + 15, ground_y)],
           fill=(255, 255, 255, 60), width=2)

    for idx, (val, freq) in enumerate(zip(values, frequencies)):
        bx = SIDE_PAD + idx * (BAR_W + BAR_GAP)
        cx = bx + BAR_W // 2
        ca, cb, ch, cs = SCHEMES[idx % len(SCHEMES)]

        # --- Body segments ---
        for s in range(freq):
            sy   = ground_y - (s + 1) * SEG_H
            col  = ca if s % 2 == 0 else cb
            # Main segment
            d.rounded_rectangle([bx, sy, bx + BAR_W, sy + SEG_H],
                                 radius=10, fill=(*col, 255))
            # Scale dots (2 rows × 3 cols)
            for row in range(2):
                for col_i in range(3):
                    dx = bx + 16 + col_i * 33
                    dy = sy + 12 + row * 22
                    hi = tuple(min(255, c + 45) for c in col)
                    d.ellipse([dx - 6, dy - 4, dx + 6, dy + 4], fill=(*hi, 190))

        # --- Head ---
        hy  = ground_y - freq * SEG_H - HEAD_H
        hp  = 12  # head wider than body
        d.rounded_rectangle([bx - hp, hy, bx + BAR_W + hp, ground_y - freq * SEG_H],
                             radius=20, fill=(*ch, 255))

        # Eyes
        eye_y = hy + HEAD_H // 3
        for ex, px_off in [(bx + 20, 2), (bx + BAR_W - 20, -2)]:
            d.ellipse([ex - 11, eye_y - 11, ex + 11, eye_y + 11], fill=(*EYE_W, 255))
            d.ellipse([ex - 6 + px_off, eye_y - 6, ex + 6 + px_off, eye_y + 6],
                      fill=(*EYE_P, 255))
            # Gleam
            d.ellipse([ex - 2 + px_off, eye_y - 5, ex + 2 + px_off, eye_y - 1],
                      fill=(255, 255, 255, 200))

        # Nostrils
        ny = hy + int(HEAD_H * 0.68)
        for nx_off in [-11, 7]:
            d.ellipse([cx + nx_off, ny - 3, cx + nx_off + 7, ny + 3],
                      fill=(*cb, 255))

        # --- Tongue ---
        max_stem = 36
        max_fork = 16
        stem = int(max_stem * tongue_frac)
        fork = int(max_fork * tongue_frac)

        if stem > 4:
            d.line([(cx, hy), (cx, hy - stem)], fill=(*TONGUE, 255), width=3)
        if fork > 3:
            tip = hy - stem
            d.line([(cx, tip), (cx - fork, tip - fork)], fill=(*TONGUE, 255), width=2)
            d.line([(cx, tip), (cx + fork, tip - fork)], fill=(*TONGUE, 255), width=2)

        # --- Value label ---
        text_center(d, str(val), cx, ground_y + 14, FONT_BOLD, (*LABEL_C, 255))

        # --- Count label above head ---
        count_y = hy - 28
        text_center(d, str(freq), cx, count_y, FONT_REG, (*LABEL_C, 180))

    # Title
    text_center(d, "Snake Histogram", canvas_w // 2, 12, FONT_TITLE, (*TITLE_C, 255))

    return img.convert('RGB')


# --- Animation frames ---
# Tongue cycles: out → hold → retract → hold → repeat
tongue_states = [1.0, 1.0, 0.75, 0.4, 0.1, 0.0, 0.0, 0.1, 0.4, 0.75]
durations     = [110, 110,  75,  60,  55, 170, 170,  55,  60,  75]

frames = [draw_frame(t) for t in tongue_states]

# Convert to palette for GIF
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
print(f"Saved → {out_path}")
print(f"Canvas: {canvas_w} × {canvas_h}px, {len(frames)} frames")
