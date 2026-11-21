"""Draw the 20 November 2026 world-news image: flat vector, no external assets.

Six stories that broke or ran on that Friday, one per tile, each with its region
named so the day's breadth is visible at a glance. Everything is drawn from
code: shapes only, type from the system's Liberation faces.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = "#0A0F1C"
TILE = "#121A2E"
TILE_EDGE = "#26334F"
CREAM = "#F4EFE4"
DIM = "#A7B6CE"
ACCENT = "#E8B33C"
RED = "#D9534F"
TEAL = "#3FB8AF"
BLUE = "#5B8FD6"

FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


def center(d, box, text, font, fill):
    x0, y0, x1, y1 = box
    l, t, r, b = d.textbbox((0, 0), text, font=font)
    d.text((x0 + (x1 - x0 - (r - l)) / 2 - l, y0 + (y1 - y0 - (b - t)) / 2 - t),
           text, font=font, fill=fill)


def wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if d.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
        # a single word wider than the tile is broken rather than clipped
        while d.textlength(cur, font=font) > width and len(cur) > 1:
            cut = len(cur) - 1
            while cut > 1 and d.textlength(cur[:cut], font=font) > width:
                cut -= 1
            lines.append(cur[:cut])
            cur = cur[cut:]
    lines.append(cur)
    return lines


def fit(d, text, width, max_lines, hi=42, lo=26):
    """Largest size in [lo, hi] whose wrap stays within max_lines."""
    for size in range(hi, lo - 1, -1):
        font = f(FB, size)
        if len(wrap(d, text, font, width)) <= max_lines:
            return font, wrap(d, text, font, width)
    font = f(FB, lo)
    return font, wrap(d, text, font, width)


# ---------------- icons: drawn in a local square of side 2r at (cx, cy) ----------------

def icon_missile(d, cx, cy, r):
    """A big cruise missile descending, trail behind, burst where it lands."""
    ang = math.radians(38)
    ca, sa = math.cos(ang), math.sin(ang)

    def pt(a, b):
        return (cx + ca * a - sa * b, cy + sa * a + ca * b)

    # trail, short dashes trailing up-left from the tail
    for i in range(4):
        t0 = -r * 0.62 - i * r * 0.20
        t1 = t0 - r * 0.12
        d.line([pt(t0, 0), pt(t1, 0)], fill=DIM, width=max(3, int(r * 0.075)))
    # body: long, thick, unmistakable
    L, Wd = r * 0.62, r * 0.115
    d.polygon([pt(L, 0), pt(L * 0.62, -Wd), pt(-L * 0.66, -Wd),
               pt(-L * 0.66, Wd), pt(L * 0.62, Wd)], fill=CREAM)
    # nose cone
    d.polygon([pt(L, 0), pt(L * 0.62, -Wd), pt(L * 0.62, Wd)], fill=RED)
    # tail fins and mid wings
    d.polygon([pt(-L * 0.66, -Wd), pt(-L * 0.92, -Wd * 2.6), pt(-L * 0.40, -Wd)], fill=RED)
    d.polygon([pt(-L * 0.66, Wd), pt(-L * 0.92, Wd * 2.6), pt(-L * 0.40, Wd)], fill=RED)
    d.polygon([pt(L * 0.16, -Wd), pt(L * 0.34, -Wd * 2.3), pt(L * 0.46, -Wd)], fill=RED)
    d.polygon([pt(L * 0.16, Wd), pt(L * 0.34, Wd * 2.3), pt(L * 0.46, Wd)], fill=RED)
    # burst at the landing point, below the nose
    bx, by = pt(L * 1.02, r * 0.46)
    for a in range(0, 360, 40):
        rad = math.radians(a)
        rr = r * (0.32 if a % 80 == 0 else 0.22)
        d.line([bx + math.cos(rad) * r * 0.12, by + math.sin(rad) * r * 0.12,
                bx + math.cos(rad) * rr, by + math.sin(rad) * rr], fill=ACCENT,
               width=max(3, int(r * 0.07)))
    d.ellipse([bx - r * 0.12, by - r * 0.12, bx + r * 0.12, by + r * 0.12], fill=RED)


def icon_crash(d, cx, cy, r):
    """A falling market: bars stepping down under a descending arrow."""
    base = cy + r * 0.62
    heights = [0.95, 0.80, 0.66, 0.50, 0.34]
    bw = r * 0.19
    for i, hh in enumerate(heights):
        x = cx - r * 0.95 + i * r * 0.40
        top = base - hh * r
        d.rounded_rectangle([x, top, x + bw, base], radius=bw * 0.22,
                            fill=RED if i >= 3 else DIM)
    # arrow, down and to the right, clear of the bars
    ax0, ay0 = cx - r * 0.92, cy - r * 0.62
    ax1, ay1 = cx + r * 0.92, cy + r * 0.06
    d.line([ax0, ay0, ax1, ay1], fill=ACCENT, width=max(3, int(r * 0.085)))
    ang = math.atan2(ay1 - ay0, ax1 - ax0)
    for s in (0.42, -0.42):
        d.line([ax1, ay1, ax1 - math.cos(ang + s) * r * 0.30,
                ay1 - math.sin(ang + s) * r * 0.30], fill=ACCENT, width=max(3, int(r * 0.085)))


def icon_climate(d, cx, cy, r):
    """A solid globe with landmasses, and a smoking chimney stack."""
    gx, gy, gr = cx - r * 0.34, cy - r * 0.02, r * 0.56
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=TEAL)
    # landmasses, drawn as solid blue-green blobs cut from the disc
    d.ellipse([gx - gr * 0.62, gy - gr * 0.66, gx + gr * 0.10, gy - gr * 0.10], fill="#1F6F6A")
    d.ellipse([gx - gr * 0.30, gy + gr * 0.06, gx + gr * 0.44, gy + gr * 0.52], fill="#1F6F6A")
    d.ellipse([gx + gr * 0.34, gy - gr * 0.34, gx + gr * 0.72, gy + gr * 0.04], fill="#1F6F6A")
    # stack, tapered and venting
    x0 = cx + r * 0.52
    d.polygon([(x0 - r * 0.17, cy - r * 0.30), (x0 + r * 0.17, cy - r * 0.30),
               (x0 + r * 0.26, cy + r * 0.66), (x0 - r * 0.26, cy + r * 0.66)], fill=DIM)
    d.rectangle([x0 - r * 0.22, cy - r * 0.36, x0 + r * 0.22, cy - r * 0.26], fill=CREAM)
    for k in range(2):
        ry = cy - r * 0.50 - k * r * 0.22
        rr = r * (0.22 + 0.09 * k)
        d.ellipse([x0 - rr, ry - rr * 0.80, x0 + rr, ry + rr * 0.50], fill="#3A4761")


def icon_nuclear(d, cx, cy, r):
    """A missile on its pad, and a big bold radiation trefoil beside it."""
    # ground line
    d.line([cx - r * 0.95, cy + r * 0.66, cx + r * 0.30, cy + r * 0.66], fill=TILE_EDGE,
           width=max(3, int(r * 0.09)))
    # missile, nose up, thick
    mx = cx - r * 0.30
    d.polygon([(mx, cy - r * 0.96), (mx + r * 0.20, cy - r * 0.32), (mx - r * 0.20, cy - r * 0.32)],
              fill=CREAM)
    d.rectangle([mx - r * 0.20, cy - r * 0.32, mx + r * 0.20, cy + r * 0.46], fill=CREAM)
    d.rectangle([mx - r * 0.20, cy + r * 0.04, mx + r * 0.20, cy + r * 0.20], fill=RED)
    for side in (-1, 1):
        d.polygon([(mx + side * r * 0.20, cy + r * 0.26), (mx + side * r * 0.46, cy + r * 0.46),
                   (mx + side * r * 0.20, cy + r * 0.46)], fill=RED)
    # exhaust
    d.polygon([(mx - r * 0.14, cy + r * 0.48), (mx + r * 0.14, cy + r * 0.48),
               (mx, cy + r * 0.74)], fill=ACCENT)
    # radiation trefoil: solid yellow disc, three fat black blades, bold ring
    bx, by, br = cx + r * 0.56, cy - r * 0.06, r * 0.54
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=ACCENT)
    for k in range(3):
        a0 = -90 + k * 120 - 60
        d.pieslice([bx - br * 0.80, by - br * 0.80, bx + br * 0.80, by + br * 0.80],
                   a0, a0 + 70, fill=BG)
    d.ellipse([bx - br * 0.26, by - br * 0.26, bx + br * 0.26, by + br * 0.26], fill=BG)


def icon_tanker(d, cx, cy, r):
    """A tanker seen in silhouette, bow to the right, held at a closed strait."""
    # hull silhouette: one solid mass with a clear raked bow and a flat stern
    d.polygon([(cx - r * 0.92, cy + r * 0.16),
               (cx + r * 0.34, cy + r * 0.16),
               (cx + r * 0.92, cy - r * 0.10),
               (cx + r * 0.92, cy + r * 0.02),
               (cx + r * 0.40, cy + r * 0.34),
               (cx - r * 0.92, cy + r * 0.34)], fill=DIM)
    # deck cargo: three big domes, the tanker's signature
    for i in range(3):
        x = cx - r * 0.60 + i * r * 0.40
        d.pieslice([x - r * 0.19, cy - r * 0.20, x + r * 0.19, cy + r * 0.18], 180, 360, fill=CREAM)
    # aft bridge and funnel, tall and square so it reads at size
    d.rectangle([cx - r * 0.92, cy - r * 0.30, cx - r * 0.56, cy + r * 0.18], fill=CREAM)
    d.rectangle([cx - r * 0.86, cy - r * 0.52, cx - r * 0.64, cy - r * 0.30], fill=RED)
    # single bold waterline under the hull
    d.rectangle([cx - r * 0.96, cy + r * 0.40, cx + r * 0.96, cy + r * 0.56], fill=TEAL)
    # the closed gate, a red bar dropped across the channel ahead of the bow
    gy = cy - r * 0.64
    d.rectangle([cx + r * 0.52, gy - r * 0.05, cx + r * 0.98, gy + r * 0.05], fill=RED)
    d.rectangle([cx + r * 0.52, gy - r * 0.18, cx + r * 0.60, gy + r * 0.18], fill=RED)
    d.rectangle([cx + r * 0.90, gy - r * 0.18, cx + r * 0.98, gy + r * 0.18], fill=RED)


def icon_displaced(d, cx, cy, r):
    """A column of people walking out, one carrying a bundle."""
    xs = (-0.66, -0.02, 0.62)
    for i, off in enumerate(xs):
        x = cx + r * off
        hr = r * (0.20 if i != 1 else 0.23)
        hy = cy - r * (0.56 if i != 1 else 0.62)
        d.ellipse([x - hr, hy - hr, x + hr, hy + hr], fill=CREAM)
        # body, a tapered coat
        d.polygon([(x - hr * 1.5, cy - r * 0.24), (x + hr * 1.5, cy - r * 0.24),
                   (x + hr * 1.1, cy + r * 0.52), (x - hr * 1.1, cy + r * 0.52)], fill=CREAM)
        # legs, mid-stride
        d.line([x - hr * 0.4, cy + r * 0.50, x - hr * 0.9, cy + r * 0.78], fill=CREAM,
               width=max(3, int(r * 0.07)))
        d.line([x + hr * 0.4, cy + r * 0.50, x + hr * 0.8, cy + r * 0.78], fill=CREAM,
               width=max(3, int(r * 0.07)))
    # the bundle on the middle walker's back
    d.ellipse([cx + r * 0.10, cy - r * 0.34, cx + r * 0.44, cy - r * 0.02], fill=ACCENT)


TILES = [
    ("EUROPE", "MISSILES HIT POLAND", "NATO: a grave violation", icon_missile),
    ("MARKETS", "STOCKS IN CORRECTION", "AI selloff deepens", icon_crash),
    ("CLIMATE", "COP31 RUNS OVERTIME", "fossil-fuel deadlock", icon_climate),
    ("ASIA", "CHINA NUCLEAR BUILDUP", "Trump, after summit", icon_nuclear),
    ("MIDDLE EAST", "IRAN: NO DEAL", "strike threat grows", icon_tanker),
    ("AFRICA", "700,000 DISPLACED", "southern Ethiopia", icon_displaced),
]


def build():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    center(d, (0, 26, W, 58), "WORLD NEWS  ·  IN ONE IMAGE", f(FR, 25), DIM)
    center(d, (0, 52, W, 152), "20 NOVEMBER 2026", f(FB, 84), CREAM)
    d.line([54, 166, W - 54, 166], fill=ACCENT, width=4)

    cols, gap = 3, 18
    mx = 40
    tw = (W - 2 * mx - (cols - 1) * gap) // cols
    th = 360
    top0 = 188
    sub_font = f(FB, 24)
    tag_font = f(FB, 21)

    for i, (region, label, sub, icon) in enumerate(TILES):
        c, rw = i % cols, i // cols
        x = mx + c * (tw + gap)
        y = top0 + rw * (th + gap)
        d.rounded_rectangle([x, y, x + tw, y + th], radius=16, fill=TILE,
                            outline=TILE_EDGE, width=2)
        # region tag, top left
        tp = d.textlength(region, font=tag_font)
        d.rounded_rectangle([x + 14, y + 12, x + 14 + tp + 26, y + 46], radius=7, fill=ACCENT)
        d.text((x + 27, y + 19), region, font=tag_font, fill=BG)
        icon(d, x + tw // 2, y + 132, 84)
        font, lines = fit(d, label, tw - 30, 2)
        ly = y + 228 if len(lines) == 2 else y + 244
        for ln in lines:
            center(d, (x, ly, x + tw, ly + 34), ln, font, CREAM)
            ly += 36
        center(d, (x, y + th - 54, x + tw, y + th - 14), sub, sub_font, CREAM)

    center(d, (0, 958, W, 998),
           "Reported by AP, Reuters, AFP, BBC, PBS and UN News", f(FR, 21), DIM)
    return img


if __name__ == "__main__":
    im = build()
    im.save("/root/makefun/news-image-20261120/repo/entry.png", optimize=True)
    print("saved", im.size)
