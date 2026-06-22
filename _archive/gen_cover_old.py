"""Generate B站 cover for Boris Cherny Sequoia video"""
from PIL import Image, ImageFont, ImageDraw, ImageFilter
import os

W, H = 1920, 1080
OUT = r"D:\Claude code_workspace\2026-06-16-youtube-content-pipeline\_runtime\boris_sequoia_2026\cover_bilibili.jpg"

# ── Fonts ──
FONT_ZH = r"C:\Windows\Fonts\NotoSansSC-VF.ttf"
FONT_EN = r"C:\Windows\Fonts\bahnschrift.ttf"
FONT_EN_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"  # Segoe UI Bold fallback for weight

# ── Canvas: deep near-black with subtle warm undertone ──
img = Image.new("RGB", (W, H), (10, 10, 16))
draw = ImageDraw.Draw(img)

# ── Background: subtle radial gradient ──
import math
for y in range(H):
    for x in range(W):
        dx = (x - W/2) / (W/2)
        dy = (y - H/2) / (H/2)
        dist = math.sqrt(dx*dx + dy*dy)
        # Radial highlight from center
        v = int(10 + 18 * (1 - dist))
        r = max(10, min(28, v))
        g = r
        b = max(16, min(36, int(16 + 20 * (1 - dist))))
        img.putpixel((x, y), (r, g, b))

# ── Accent line (Sequoia-inspired warm red) ──
ACCENT = (220, 60, 50)
draw.rectangle([80, 340, 120, 350], fill=ACCENT)

# ── Chinese Title (main) ──
try:
    font_zh_title = ImageFont.truetype(FONT_ZH, 72)
except:
    font_zh_title = ImageFont.truetype(FONT_ZH, 72)
    font_zh_title.set_variation_by_name("Bold") if hasattr(font_zh_title, 'set_variation_by_name') else None

# Use large size + manual weight
font_zh_title = ImageFont.truetype(FONT_ZH, 76)

zh_title = "编程已解决"
zh_bbox = draw.textbbox((0, 0), zh_title, font=font_zh_title)
zh_w = zh_bbox[2] - zh_bbox[0]
zh_x = 80
zh_y = 360

# Shadow (structural, bottom only)
draw.text((zh_x + 3, zh_y + 4), zh_title, font=font_zh_title, fill=(0, 0, 0, 80))
# Main text — warm white
draw.text((zh_x, zh_y), zh_title, font=font_zh_title, fill=(245, 242, 235))

# ── Subtitle line: "软件行业的印刷术时刻" ──
font_zh_sub = ImageFont.truetype(FONT_ZH, 56)
zh_sub = "软件行业的印刷术时刻"
zh_sub_bbox = draw.textbbox((0, 0), zh_sub, font=font_zh_sub)
draw.text((zh_x + 3, zh_y + 100 + 3), zh_sub, font=font_zh_sub, fill=(0, 0, 0, 60))
draw.text((zh_x, zh_y + 100), zh_sub, font=font_zh_sub, fill=(200, 195, 185))

# ── English title ──
font_en = ImageFont.truetype(FONT_EN, 28)
en_title = "CODING'S PRINTING PRESS MOMENT"
# Letter-spacing: add spaces
en_title_spaced = "  ".join(en_title)
draw.text((zh_x + 2, zh_y + 190 + 2), en_title_spaced, font=font_en, fill=(0, 0, 0, 50))
draw.text((zh_x, zh_y + 190), en_title_spaced, font=font_en, fill=(140, 130, 120))

# ── Boris name + badge ──
font_name = ImageFont.truetype(FONT_EN, 42)
name_text = "BORIS CHERNY"
name_spaced = "  ".join(name_text)
draw.text((zh_x + 2, zh_y + 260 + 2), name_spaced, font=font_name, fill=(0, 0, 0, 60))
draw.text((zh_x, zh_y + 260), name_spaced, font=font_name, fill=(230, 225, 215))

# ── Role subtitle ──
font_role = ImageFont.truetype(FONT_EN, 22)
role = "CREATOR OF CLAUDE CODE  ·  ANTHROPIC"
draw.text((zh_x + 1, zh_y + 320 + 1), role, font=font_role, fill=(0, 0, 0, 40))
draw.text((zh_x, zh_y + 320), role, font=font_role, fill=(150, 145, 135))

# ── Bottom bar: conference info ──
font_info = ImageFont.truetype(FONT_EN, 18)
info_line = "SEQUOIA CAPITAL  ·  AI ASCENT 2026  ·  40 MIN  ·  BILINGUAL SUBS"
info_bbox = draw.textbbox((0, 0), info_line, font=font_info)
info_w = info_bbox[2] - info_bbox[0]

# Bottom divider
draw.rectangle([80, H - 100, W - 80, H - 98], fill=(50, 50, 55))
draw.text((W - 80 - info_w + 1, H - 85 + 1), info_line, font=font_info, fill=(0, 0, 0, 40))
draw.text((W - 80 - info_w, H - 85), info_line, font=font_info, fill=(120, 118, 110))

# ── Top-right decorative element: subtle concentric rings ──
cx, cy = W - 220, 220
for r in [180, 140, 100, 60]:
    for angle in range(0, 360, 3):
        rad = math.radians(angle)
        x = int(cx + r * math.cos(rad))
        y = int(cy + r * math.sin(rad))
        # Very subtle dots
        alpha = 30 if r > 120 else 50
        if 0 <= x < W and 0 <= y < H:
            existing = img.getpixel((x, y))
            blend = min(255, existing[0] + alpha)
            img.putpixel((x, y), (min(255, blend), min(255, blend), min(255, blend + 5)))

# ── Save ──
img.save(OUT, "JPEG", quality=95, optimize=True)
size_kb = os.path.getsize(OUT) / 1024
print(f"Cover saved: {OUT}")
print(f"Size: {size_kb:.0f} KB ({'OK' if size_kb < 5120 else 'OVER 5MB!'})")
print(f"Dimensions: {W}×{H}")
