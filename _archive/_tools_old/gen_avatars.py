"""Generate light-mode avatar concepts for 进化猫 B站 channel"""
from PIL import Image, ImageDraw
import math, os

SIZE = 1024
OUT_DIR = r"D:\Claude code_workspace\2026-06-16-youtube-content-pipeline\_runtime\avatars"
os.makedirs(OUT_DIR, exist_ok=True)

CORAL = (245, 90, 70)           # Coral main
CORAL_DIM = (220, 80, 60)       # Darker coral
CORAL_GLOW = (255, 130, 110)    # Light coral
CORAL_FAINT = (255, 200, 185)   # Very faint coral for bg accents
BG = (250, 248, 245)            # Warm off-white (like warm paper)
BG_ALT = (245, 240, 235)        # Slightly darker warm

def draw_rounded_rect(draw, xy, r, fill):
    x1, y1, x2, y2 = xy
    draw.pieslice([x1, y1, x1+2*r, y1+2*r], 180, 270, fill=fill)
    draw.pieslice([x2-2*r, y1, x2, y1+2*r], 270, 360, fill=fill)
    draw.pieslice([x1, y2-2*r, x1+2*r, y2], 90, 180, fill=fill)
    draw.pieslice([x2-2*r, y2-2*r, x2, y2], 0, 90, fill=fill)
    draw.rectangle([x1+r, y1, x2-r, y2], fill=fill)
    draw.rectangle([x1, y1+r, x2, y2-r], fill=fill)


# ═══════════════════ CONCEPT A: 频谱柱 ═══════════════════

def concept_a():
    img = Image.new("RGBA", (SIZE, SIZE), BG + (255,))
    draw = ImageDraw.Draw(img)

    cx, cy = SIZE // 2, SIZE // 2
    bar_count = 19
    bar_w = 28
    bar_gap = 8
    total_w = bar_count * (bar_w + bar_gap) - bar_gap
    start_x = cx - total_w // 2
    base_y = cy + 80

    for i in range(bar_count):
        if i < bar_count // 2:
            progress = i / (bar_count // 2)
        else:
            progress = (bar_count - 1 - i) / (bar_count // 2)
        height = int(40 + progress * 300)

        x = start_x + i * (bar_w + bar_gap)
        y = base_y - height

        dist = abs(i - bar_count // 2) / (bar_count // 2)
        alpha = 1.0 - dist * 0.5
        color = (
            int(CORAL[0] * alpha + CORAL_DIM[0] * (1-alpha)),
            int(CORAL[1] * alpha + CORAL_DIM[1] * (1-alpha)),
            int(CORAL[2] * alpha + CORAL_DIM[2] * (1-alpha))
        )
        draw_rounded_rect(draw, [x, y, x+bar_w, base_y], bar_w//2, fill=color)

    out = os.path.join(OUT_DIR, "concept_a_light.png")
    img.save(out, "PNG")
    print(f"A light: {out}")


# ═══════════════════ CONCEPT B: 猫耳信号 ═══════════════════

def concept_b():
    img = Image.new("RGBA", (SIZE, SIZE), BG + (255,))
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2 - 30

    # Subtle background wave rings
    for ring_r in range(120, 400, 60):
        for angle in range(0, 360, 2):
            rad = math.radians(angle)
            r = ring_r + math.sin(angle*6) * 3
            x = cx + int(r * math.cos(rad))
            y = cy + 30 + int(r * math.sin(rad))
            alpha = 30
            draw.point((x, y), fill=(CORAL_FAINT[0], CORAL_FAINT[1], CORAL_FAINT[2], alpha))

    # Left ear — signal arcs
    for frame in range(18):
        alpha = int(200 * (1 - abs(frame/18 - 0.5) * 1.5))
        if alpha < 15: alpha = 15
        pts = []
        for angle in range(180, 325, 4):
            rad = math.radians(angle)
            r = 230 + frame * 2.5 + math.sin(angle * 5) * 6
            x = cx - 100 + int(r * math.cos(rad))
            y = cy + 20 + int(r * math.sin(rad))
            pts.append((x, y))
        for j in range(len(pts)-1):
            draw.line([pts[j], pts[j+1]], fill=(CORAL[0], CORAL[1], CORAL[2], alpha), width=3)

    # Right ear
    for frame in range(18):
        alpha = int(200 * (1 - abs(frame/18 - 0.5) * 1.5))
        if alpha < 15: alpha = 15
        pts = []
        for angle in range(215, 360, 4):
            rad = math.radians(angle)
            r = 230 + frame * 2.5 + math.sin(angle * 5) * 6
            x = cx + 100 + int(r * math.cos(rad))
            y = cy + 20 + int(r * math.sin(rad))
            pts.append((x, y))
        for j in range(len(pts)-1):
            draw.line([pts[j], pts[j+1]], fill=(CORAL[0], CORAL[1], CORAL[2], alpha), width=3)

    # Center node glow
    for r in range(45, 0, -1):
        alpha = int(200 * (1 - r/45)**0.4)
        draw.ellipse([cx-r, cy+30-r, cx+r, cy+30+r],
                     fill=(CORAL_GLOW[0], CORAL_GLOW[1], CORAL_GLOW[2], alpha))
    draw.ellipse([cx-12, cy+18, cx+12, cy+42], fill=CORAL)

    out = os.path.join(OUT_DIR, "concept_b_light.png")
    img.save(out, "PNG")
    print(f"B light: {out}")


# ═══════════════════ CONCEPT C: 脉冲雷达 ═══════════════════

def concept_c():
    img = Image.new("RGBA", (SIZE, SIZE), BG + (255,))
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2

    for wave_idx in range(7):
        base_r = 90 + wave_idx * 55
        fade = 1.0 - wave_idx / 7
        for angle in range(0, 360, 3):
            rad = math.radians(angle)
            wobble = math.sin(angle * 8 + wave_idx) * 3 + math.sin(angle * 3) * 1.5
            r = base_r + wobble
            x = cx + int(r * math.cos(rad))
            y = cy + int(r * math.sin(rad))
            alpha = int(180 * fade)
            if alpha < 15: alpha = 15
            size = max(1, int(2.5 * fade))
            draw.ellipse([x-size, y-size, x+size, y+size],
                         fill=(CORAL[0], CORAL[1], CORAL[2], alpha))

    # Center pulse
    for r in range(55, 0, -1):
        alpha = int(255 * (1 - r/55)**0.25)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r],
                     fill=(CORAL_GLOW[0], CORAL_GLOW[1], CORAL_GLOW[2], alpha))
    draw.ellipse([cx-14, cy-14, cx+14, cy+14], fill=CORAL)

    # Scanning beam
    for r in range(90, 400, 8):
        rad = math.radians(42)
        x = cx + int(r * math.cos(rad))
        y = cy + int(r * math.sin(rad))
        alpha = int(80 * (1 - (r-90)/310))
        if alpha > 5:
            draw.ellipse([x-2, y-2, x+2, y+2],
                         fill=(CORAL[0], CORAL[1], CORAL[2], alpha))

    out = os.path.join(OUT_DIR, "concept_c_light.png")
    img.save(out, "PNG")
    print(f"C light: {out}")

concept_a()
concept_b()
concept_c()
print("Done")
