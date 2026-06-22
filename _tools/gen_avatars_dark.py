"""Generate 3 avatar concepts for 进化猫 B站 channel"""
from PIL import Image, ImageDraw, ImageFont
import math, os

SIZE = 1024  # 1:1 square, will be resized for B站
OUT_DIR = r"D:\Claude code_workspace\2026-06-16-youtube-content-pipeline\_runtime\avatars"
os.makedirs(OUT_DIR, exist_ok=True)

CORAL = (255, 107, 87)       # Primary coral
CORAL_DIM = (200, 70, 55)    # Darker coral
CORAL_GLOW = (255, 140, 120) # Light coral glow
BG = (14, 14, 20)            # Near-black with slight warmth

def draw_rounded_rect(draw, xy, r, fill):
    x1, y1, x2, y2 = xy
    draw.rectangle([x1+r, y1, x2-r, y2], fill=fill)
    draw.rectangle([x1, y1+r, x2, y2-r], fill=fill)
    draw.pieslice([x1, y1, x1+2*r, y1+2*r], 180, 270, fill=fill)
    draw.pieslice([x2-2*r, y1, x2, y1+2*r], 270, 360, fill=fill)
    draw.pieslice([x1, y2-2*r, x1+2*r, y2], 90, 180, fill=fill)
    draw.pieslice([x2-2*r, y2-2*r, x2, y2], 0, 90, fill=fill)

def radial_gradient(size, inner_color, outer_color):
    """Generate radial gradient background"""
    img = Image.new("RGBA", (size, size), (0,0,0,0))
    cx = cy = size // 2
    for y in range(size):
        for x in range(size):
            dx = (x - cx) / cx
            dy = (y - cy) / cy
            dist = math.sqrt(dx*dx + dy*dy)
            t = min(1.0, dist)
            r = int(outer_color[0] + (inner_color[0] - outer_color[0]) * (1-t))
            g = int(outer_color[1] + (inner_color[1] - outer_color[1]) * (1-t))
            b = int(outer_color[2] + (inner_color[2] - outer_color[2]) * (1-t))
            img.putpixel((x, y), (r, g, b, 255))
    return img


# ═══════════════════════════════════════════
# CONCEPT A: 频谱进化 — ascending spectrum bars
# ═══════════════════════════════════════════

def concept_a():
    img = radial_gradient(SIZE, (22, 22, 32), BG)
    draw = ImageDraw.Draw(img)

    # Spectrum bars — ascending heights, coral gradient
    cx, cy = SIZE // 2, SIZE // 2
    bar_count = 19
    bar_w = 28
    bar_gap = 8
    total_w = bar_count * (bar_w + bar_gap) - bar_gap
    start_x = cx - total_w // 2
    base_y = cy + 60

    for i in range(bar_count):
        # Height: rising then falling (envelope shape)
        if i < bar_count // 2:
            progress = i / (bar_count // 2)
        else:
            progress = (bar_count - 1 - i) / (bar_count // 2)
        height = int(40 + progress * 280)

        x = start_x + i * (bar_w + bar_gap)
        y = base_y - height

        # Color: brighter at center
        dist_from_center = abs(i - bar_count // 2) / (bar_count // 2)
        alpha = 1.0 - dist_from_center * 0.6
        color = (
            int(CORAL[0] * alpha + CORAL_DIM[0] * (1-alpha)),
            int(CORAL[1] * alpha + CORAL_DIM[1] * (1-alpha)),
            int(CORAL[2] * alpha + CORAL_DIM[2] * (1-alpha))
        )

        # Rounded bar
        r = bar_w // 2
        draw_rounded_rect(draw, [x, y, x+bar_w, base_y], r, fill=color)

    # Bottom subtle glow line
    for i in range(256):
        alpha = int(15 * (1 - i/256))
        draw.rectangle([start_x, base_y+i, start_x+total_w, base_y+i+1],
                       fill=(CORAL[0], CORAL[1], CORAL[2], alpha))

    out = os.path.join(OUT_DIR, "concept_a_spectrum.png")
    img.save(out, "PNG")
    print(f"A: {out}")


# ═══════════════════════════════════════════
# CONCEPT B: 信号猫耳 — subtle cat ear arcs from waveform
# ═══════════════════════════════════════════

def concept_b():
    img = radial_gradient(SIZE, (22, 22, 32), BG)
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2 - 30

    # Two ear-like arcs made of signal waves
    # Left ear
    for frame in range(20):
        t = frame / 20
        alpha = int(180 * (1 - abs(t - 0.5) * 1.5))
        if alpha <= 0: alpha = 10
        # Arc points
        pts = []
        for angle in range(180, 325, 3):
            rad = math.radians(angle)
            r = 240 + frame * 3 + math.sin(angle * 5) * 8
            x = cx - 100 + int(r * math.cos(rad))
            y = cy + 20 + int(r * math.sin(rad))
            pts.append((x, y))
        if len(pts) > 1:
            for j in range(len(pts)-1):
                draw.line([pts[j], pts[j+1]], fill=(CORAL[0], CORAL[1], CORAL[2], alpha), width=3)

    # Right ear (mirrored)
    for frame in range(20):
        t = frame / 20
        alpha = int(180 * (1 - abs(t - 0.5) * 1.5))
        if alpha <= 0: alpha = 10
        pts = []
        for angle in range(215, 360, 3):
            rad = math.radians(angle)
            r = 240 + frame * 3 + math.sin(angle * 5) * 8
            x = cx + 100 + int(r * math.cos(rad))
            y = cy + 20 + int(r * math.sin(rad))
            pts.append((x, y))
        if len(pts) > 1:
            for j in range(len(pts)-1):
                draw.line([pts[j], pts[j+1]], fill=(CORAL[0], CORAL[1], CORAL[2], alpha), width=3)

    # Center node — bright coral dot
    for r in range(40, 0, -1):
        alpha = int(255 * (1 - r/40)**0.5)
        draw.ellipse([cx-r, cy+30-r, cx+r, cy+30+r],
                     fill=(CORAL_GLOW[0], CORAL_GLOW[1], CORAL_GLOW[2], alpha))

    # Central solid dot
    draw.ellipse([cx-12, cy+18, cx+12, cy+42], fill=CORAL)

    out = os.path.join(OUT_DIR, "concept_b_cat_ears.png")
    img.save(out, "PNG")
    print(f"B: {out}")


# ═══════════════════════════════════════════
# CONCEPT C: 脉冲雷达 — concentric expanding waves
# ═══════════════════════════════════════════

def concept_c():
    img = radial_gradient(SIZE, (22, 22, 32), BG)
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2

    # Expanding circular waves
    wave_gap = 50
    for wave_idx in range(8):
        base_r = 80 + wave_idx * wave_gap
        for angle in range(0, 360, 2):
            rad = math.radians(angle)
            # Add subtle noise/wave to circle edge
            wobble = math.sin(angle * 8 + wave_idx) * 4 + math.sin(angle * 3) * 2
            r = base_r + wobble
            x = cx + int(r * math.cos(rad))
            y = cy + int(r * math.sin(rad))

            # Brightness fades outward
            fade = 1.0 - wave_idx / 8
            alpha = int(200 * fade)
            if alpha < 20: alpha = 20

            # Point size varies
            size = max(1, int(3 * fade))
            draw.ellipse([x-size, y-size, x+size, y+size],
                         fill=(CORAL[0], CORAL[1], CORAL[2], alpha))

    # Center core — bright pulse
    for r in range(50, 0, -1):
        alpha = int(255 * (1 - r/50)**0.3)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r],
                     fill=(CORAL_GLOW[0], CORAL_GLOW[1], CORAL_GLOW[2], alpha))

    # Center dot
    draw.ellipse([cx-15, cy-15, cx+15, cy+15], fill=CORAL)

    # Scanning beam (subtle)
    beam_angle = 45  # degrees
    for r in range(80, 380, 5):
        rad = math.radians(beam_angle)
        x = cx + int(r * math.cos(rad))
        y = cy + int(r * math.sin(rad))
        alpha = int(100 * (1 - (r-80)/300))
        draw.ellipse([x-2, y-2, x+2, y+2],
                     fill=(CORAL_GLOW[0], CORAL_GLOW[1], CORAL_GLOW[2], max(10, alpha)))

    out = os.path.join(OUT_DIR, "concept_c_radar.png")
    img.save(out, "PNG")
    print(f"C: {out}")


concept_a()
concept_b()
concept_c()
print("Done — 3 concepts generated")
