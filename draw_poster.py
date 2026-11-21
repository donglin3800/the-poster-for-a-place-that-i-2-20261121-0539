#!/usr/bin/env python3
"""Draw VELMARA — a travel poster for a place that isn't there (1024x1024 PNG).

Dusk over a turquoise lagoon, rose-gold cliffs left and right framing the
view, ONE landmark: a single slender white lighthouse on the headland, lit
warm. A low large sun with a sun-path reflection on the water, a few small
boats, a few birds, dark foreground rocks. The only text is the place name.
Drawn with Pillow only, deterministic (fixed seed).
"""
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1024
HORIZON = 600
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

random.seed(20261121)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(draw, x0, y0, x1, y1, top, bottom):
    """Vertical gradient band."""
    h = y1 - y0
    for y in range(y0, y1):
        t = (y - y0) / max(1, h - 1)
        draw.line([(x0, y), (x1, y)], fill=lerp(top, bottom, t))


def main():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)

    # --- Sky: violet dusk at top -> peach near the horizon ---
    vgrad(d, 0, 0, W, HORIZON, (74, 58, 112), (252, 178, 130))
    # Warm band just above the horizon
    vgrad(d, 0, HORIZON - 130, W, HORIZON, (244, 158, 118), (255, 196, 140))

    # --- Sun: low, large, right of centre, with glow ---
    sun_cx, sun_cy, sun_r = 660, 520, 86
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r, a in [(330, 26), (280, 34), (230, 46), (180, 60), (140, 80)]:
        gd.ellipse([sun_cx - r, sun_cy - r, sun_cx + r, sun_cy + r],
                   fill=(255, 190, 110, a))
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"),
              (0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
              fill=(255, 226, 160))
    d.ellipse([sun_cx - sun_r + 10, sun_cy - sun_r + 10,
               sun_cx + sun_r - 10, sun_cy + sun_r - 10],
              fill=(255, 240, 200))

    # --- Distant headland silhouette across the water (low, hazy) ---
    d.polygon([(0, HORIZON), (300, HORIZON - 26), (470, HORIZON - 8),
               (640, HORIZON - 30), (760, HORIZON - 12), (W, HORIZON - 22),
               (W, HORIZON), (0, HORIZON)], fill=(122, 84, 118))

    # --- Water: teal, darker toward the bottom ---
    vgrad(d, 0, HORIZON, W, H, (42, 128, 138), (10, 48, 66))

    # --- Sun-path reflection: broken golden dashes under the sun ---
    # Drawn on an overlay so the shimmer fades naturally into the water.
    path = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(path)
    for y in range(HORIZON + 12, H - 50, 8):
        t = (y - HORIZON) / (H - HORIZON)
        half = 22 + t * 150
        alpha = int(max(30, 235 - t * 230))
        # a few short dashes per row, scattered across the band
        for _ in range(random.randint(2, 4)):
            cx = sun_cx + random.randint(-int(half), int(half))
            wdt = random.randint(10, 46)
            pd.line([(cx - wdt // 2, y), (cx + wdt // 2, y)],
                    fill=(255, 205, 130, alpha), width=3)
    # Bright core right under the sun: short dense dashes, tapering down
    for y in range(HORIZON + 6, HORIZON + 150, 6):
        t = (y - HORIZON) / 150
        half = 44 - t * 22
        alpha = int(235 - t * 120)
        cx = sun_cx + random.randint(-int(half), int(half))
        wdt = random.randint(14, 34)
        pd.line([(cx - wdt // 2, y), (cx + wdt // 2, y)],
                fill=(255, 220, 150, alpha), width=3)
    path = path.filter(ImageFilter.GaussianBlur(1))
    img.paste(Image.alpha_composite(img.convert("RGBA"), path).convert("RGB"),
              (0, 0))
    d = ImageDraw.Draw(img)

    # --- Cliffs: rose-gold, framing left and right ---
    # Left cliff, tall, sloping down toward the water
    left = [(0, 180), (60, 240), (96, 330), (120, 430), (150, 520),
            (168, 600), (150, HORIZON + 46), (0, HORIZON + 46), (0, 180)]
    d.polygon(left, fill=(196, 110, 96))
    # Left cliff face shading + strata
    d.polygon([(0, 300), (96, 330), (120, 430), (150, 520), (168, 600),
               (150, HORIZON + 46), (0, HORIZON + 46), (0, 300)],
              fill=(168, 88, 84))
    for y, x0, x1 in [(300, 8, 96), (380, 30, 116), (470, 60, 146),
                      (545, 100, 162)]:
        d.line([(x0, y), (x1, y)], fill=(214, 138, 116), width=3)
    # Warm rim light on the left cliff's inner edge
    d.line([(96, 330), (120, 430), (150, 520), (168, 600)],
           fill=(255, 196, 140), width=4)

    # Right cliff / headland, lower, carrying the lighthouse
    right = [(W, 260), (950, 300), (908, 400), (880, 500), (872, 600),
             (884, HORIZON + 40), (W, HORIZON + 40), (W, 260)]
    d.polygon(right, fill=(188, 102, 90))
    d.polygon([(950, 300), (908, 400), (880, 500), (872, 600),
               (884, HORIZON + 40), (W, HORIZON + 40), (W, 460), (962, 380)],
              fill=(158, 80, 76))
    for y, x0, x1 in [(380, 928, 1000), (470, 900, 1004), (550, 886, 1010)]:
        d.line([(x0, y), (x1, y)], fill=(206, 128, 108), width=3)
    d.line([(950, 300), (908, 400), (880, 500), (872, 600)],
           fill=(255, 190, 132), width=4)

    # --- THE lighthouse: one slender white tower on the right headland ---
    lx = 905          # tower centre x
    base_y = 596      # ground at headland top
    top_y = 330
    # Tapered tower
    d.polygon([(lx - 26, base_y), (lx - 14, top_y), (lx + 14, top_y),
               (lx + 26, base_y)], fill=(250, 244, 230))
    # Sunlit side / shaded side
    d.polygon([(lx - 2, top_y), (lx + 14, top_y), (lx + 26, base_y),
               (lx - 2, base_y)], fill=(228, 216, 198))
    d.polygon([(lx - 26, base_y), (lx - 14, top_y), (lx - 2, top_y),
               (lx - 2, base_y)], fill=(255, 250, 240))
    # Warm lit windows (three, glowing)
    for wy in (392, 448, 504):
        d.rectangle([lx - 6, wy, lx + 6, wy + 16], fill=(255, 196, 96))
        d.rectangle([lx - 6, wy, lx + 6, wy + 16], outline=(120, 80, 50),
                    width=1)
    # Gallery + lantern room
    d.rectangle([lx - 20, top_y - 14, lx + 20, top_y], fill=(52, 44, 52))
    d.rectangle([lx - 12, top_y - 38, lx + 12, top_y - 14],
                fill=(255, 214, 120))
    d.rectangle([lx - 12, top_y - 38, lx + 12, top_y - 14],
                outline=(52, 44, 52), width=2)
    d.polygon([(lx - 16, top_y - 38), (lx + 16, top_y - 38), (lx, top_y - 54)],
              fill=(52, 44, 52))
    # Lamp glow
    lamp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lamp)
    ld.ellipse([lx - 34, top_y - 60, lx + 34, top_y + 8],
               fill=(255, 220, 130, 90))
    lamp = lamp.filter(ImageFilter.GaussianBlur(10))
    img.paste(Image.alpha_composite(img.convert("RGBA"), lamp).convert("RGB"),
              (0, 0))
    d = ImageDraw.Draw(img)
    # Faint beam toward the sea (left), very subtle
    beam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(beam)
    bd.polygon([(lx - 10, top_y - 26), (lx - 10, top_y - 22),
                (560, top_y + 26), (560, top_y + 44)],
               fill=(255, 226, 150, 12))
    beam = beam.filter(ImageFilter.GaussianBlur(8))
    img.paste(Image.alpha_composite(img.convert("RGBA"), beam).convert("RGB"),
              (0, 0))
    d = ImageDraw.Draw(img)

    # --- Boats: three small ones on the lagoon ---
    def boat(bx, by, s, sail_col):
        d.polygon([(bx - 26 * s, by), (bx + 26 * s, by),
                   (bx + 16 * s, by + 10 * s), (bx - 16 * s, by + 10 * s)],
                  fill=(40, 34, 40))
        d.polygon([(bx, by - 34 * s), (bx, by), (bx + 20 * s, by)],
                  fill=sail_col)
        d.polygon([(bx, by - 26 * s), (bx, by), (bx - 15 * s, by)],
                  fill=(250, 244, 232))
        d.line([(bx, by - 36 * s), (bx, by)], fill=(40, 34, 40), width=2)
        # reflection
        d.line([(bx - 18 * s, by + 16 * s), (bx + 18 * s, by + 16 * s)],
               fill=(255, 200, 130), width=2)

    boat(330, 700, 1.0, (252, 236, 214))
    boat(520, 780, 0.7, (244, 180, 140))
    boat(760, 690, 0.55, (250, 244, 232))

    # --- Birds: a few small marks in the clear sky below the name ---
    for bx, by, s in [(300, 330, 14), (370, 305, 11), (430, 340, 9),
                      (560, 300, 10), (760, 330, 12)]:
        d.arc([bx - s, by - s // 2, bx, by + s // 2], start=200, end=340,
              fill=(52, 40, 52), width=3)
        d.arc([bx, by - s // 2, bx + s, by + s // 2], start=200, end=340,
              fill=(52, 40, 52), width=3)

    # --- Dark foreground rocks, bottom corners ---
    d.polygon([(0, H), (0, 930), (90, 880), (190, 920), (260, H)],
              fill=(24, 22, 30))
    d.line([(0, 930), (90, 880), (190, 920)], fill=(120, 90, 96), width=3)
    d.polygon([(W, H), (W, 940), (940, 892), (850, 928), (790, H)],
              fill=(22, 20, 28))
    d.line([(W, 940), (940, 892), (850, 928)], fill=(116, 86, 92), width=3)

    # --- Type: VELMARA, large cream serif caps in the clear sky ---
    name = "VELMARA"
    fsize = 118
    fnt = ImageFont.truetype(SERIF_B, fsize)
    # Letter-spaced width
    tracking = 26
    widths = [d.textlength(ch, font=fnt) for ch in name]
    total = sum(widths) + tracking * (len(name) - 1)
    x = (W - total) / 2
    y = 128
    # Soft halo + shadow on a separate layer, then crisp text
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    hx = x
    for ch, wch in zip(name, widths):
        hd.text((hx, y), ch, font=fnt, fill=(255, 226, 170, 200))
        hx += wch + tracking
    halo = halo.filter(ImageFilter.GaussianBlur(6))
    img.paste(Image.alpha_composite(img.convert("RGBA"), halo).convert("RGB"),
              (0, 0))
    d = ImageDraw.Draw(img)
    # Soft dark shadow for legibility over the bright sky
    sx = x
    for ch, wch in zip(name, widths):
        d.text((sx + 3, y + 4), ch, font=fnt, fill=(64, 40, 66))
        sx += wch + tracking
    sx = x
    for ch, wch in zip(name, widths):
        d.text((sx, y), ch, font=fnt, fill=(255, 246, 228))
        sx += wch + tracking

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
