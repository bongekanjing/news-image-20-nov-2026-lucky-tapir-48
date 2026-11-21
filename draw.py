"""Draw the 20 November 2026 world-news page: a broadsheet in one square.

Thirty-six stories that happened or were first reported on that Friday, grouped
by region, laid out with the hierarchy of a front page: three leads, ten cards,
twenty-three briefs. Everything is drawn from code -- shapes only, type from the
system's Liberation faces. No photographs, no external assets.

Run: python3 draw.py   (writes entry.png beside this file)
"""
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- geometry --
W = H = 1024          # the finished size, in design units
S = 2                 # drawn at twice the size, then halved, so small type is clean
M = 24                # page margin

# ------------------------------------------------------------------ colour --
PAPER = "#FBF8F1"
INK = "#15130F"
INK2 = "#46423A"
GREY = "#837C6E"
FAINT = "#C9C2B2"
RED = "#C0392B"

REGION_COLOR = {
    "Europe": "#2E5FA3",
    "Asia": "#B23A3A",
    "Middle East": "#B8791F",
    "Africa": "#3F7A4B",
    "Americas": "#6A4C93",
    "Oceania": "#2A8A8A",
    "Global": "#6B7280",
}

# ------------------------------------------------------------------- fonts --
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"

_FONTS = {}


def _font(path, size):
    key = (path, int(round(size * S)))
    if key not in _FONTS:
        _FONTS[key] = ImageFont.truetype(path, key[1])
    return _FONTS[key]

# --------------------------------------------------------------- the paper --


class Page:
    """A drawing surface addressed in 1024-unit design coordinates."""

    def __init__(self):
        self.im = Image.new("RGB", (W * S, H * S), PAPER)
        self.d = ImageDraw.Draw(self.im)
        self.bottom = 0

    # -- measurement, in design units
    def font(self, path, size):
        return _font(path, size)

    def tw(self, text, font):
        return self.d.textlength(text, font=font) / S

    def wrap(self, text, font, width):
        words, lines, cur = text.split(), [], ""
        for w in words:
            trial = (cur + " " + w).strip()
            if not cur or self.tw(trial, font) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = w
                # a single token wider than the column is broken, never clipped
                while self.tw(cur, font) > width and len(cur) > 1:
                    cut = len(cur)
                    while cut > 1 and self.tw(cur[:cut], font) > width:
                        cut -= 1
                    lines.append(cur[:cut])
                    cur = cur[cut:]
        if cur:
            lines.append(cur)
        return lines

    def fit(self, text, path, width, max_lines, hi, lo):
        """Largest size whose wrap fits max_lines; the smallest size otherwise."""
        for size in range(int(hi), int(lo) - 1, -1):
            f = self.font(path, size)
            lines = self.wrap(text, f, width)
            if len(lines) <= max_lines:
                return f, lines
        f = self.font(path, lo)
        return f, self.wrap(text, f, width)[:max_lines]

    # -- primitives, in design units
    def text(self, x, y, s, f, fill, anchor="la"):
        self.d.text((x * S, y * S), s, font=f, fill=fill, anchor=anchor)

    def rect(self, box, fill=None, outline=None, width=1):
        self.d.rectangle([box[0] * S, box[1] * S, box[2] * S, box[3] * S],
                         fill=fill, outline=outline,
                         width=max(1, int(round(width * S))))

    def rrect(self, box, radius, fill=None, outline=None, width=1):
        self.d.rounded_rectangle([box[0] * S, box[1] * S, box[2] * S, box[3] * S],
                                 radius=radius * S, fill=fill, outline=outline,
                                 width=max(1, int(round(width * S))))

    def line(self, pts, fill, width=1):
        self.d.line([(x * S, y * S) for x, y in pts], fill=fill,
                    width=max(1, int(round(width * S))), joint="curve")

    def poly(self, pts, fill=None):
        self.d.polygon([(x * S, y * S) for x, y in pts], fill=fill)

    def ellipse(self, box, fill=None, outline=None, width=1):
        self.d.ellipse([box[0] * S, box[1] * S, box[2] * S, box[3] * S],
                       fill=fill, outline=outline,
                       width=max(1, int(round(width * S))))

    def arc(self, box, a0, a1, fill, width=2):
        self.d.arc([box[0] * S, box[1] * S, box[2] * S, box[3] * S], a0, a1,
                   fill=fill, width=max(1, int(round(width * S))))

    def pieslice(self, box, a0, a1, fill):
        self.d.pieslice([box[0] * S, box[1] * S, box[2] * S, box[3] * S], a0, a1, fill=fill)

    def rule(self, x0, x1, y, weight=1, color=INK):
        self.rect([x0, y, x1, y + weight], fill=color)

    def save(self, path):
        self.im.resize((W, H), Image.LANCZOS).save(path, optimize=True)


# ----------------------------------------------------------------- icons ----
# Each draws inside the box (x, y, w, h). Flat shapes, two or three colours.

def icon_bridge(p, x, y, w, h, c):
    """A bridge deck on piers, struck, with a blast over the span."""
    deck = y + h * 0.72
    p.rect([x + w * 0.04, deck, x + w * 0.96, deck + h * 0.09], fill=INK2)
    for i in range(3):
        px = x + w * (0.16 + i * 0.30)
        p.rect([px, deck, px + w * 0.055, y + h * 0.99], fill=INK2)
    # arch under the deck
    p.arc([x + w * 0.10, deck - h * 0.30, x + w * 0.46, deck + h * 0.24], 190, 350, INK2, 3)
    p.arc([x + w * 0.50, deck - h * 0.30, x + w * 0.86, deck + h * 0.24], 190, 350, INK2, 3)
    # blast: a bright star above the span
    cx, cy, r = x + w * 0.52, y + h * 0.30, min(w, h) * 0.30
    for k in range(8):
        a = k * 45
        import math
        dx, dy = math.cos(math.radians(a)), math.sin(math.radians(a))
        p.poly([(cx + dx * r, cy + dy * r), (cx + dx * r * 0.36 - dy * r * 0.20,
                                             cy + dy * r * 0.36 + dx * r * 0.20),
                (cx + dx * r * 0.36 + dy * r * 0.20, cy + dy * r * 0.36 - dx * r * 0.20)],
               RED)
    p.ellipse([cx - r * 0.30, cy - r * 0.30, cx + r * 0.30, cy + r * 0.30], fill="#F2C14E")


def icon_cyclone(p, x, y, w, h, c):
    """A tight spiral over a coastline: the storm's signature."""
    cx, cy = x + w * 0.50, y + h * 0.46
    r = min(w, h) * 0.42
    for i, (rr, a0, a1, wd) in enumerate([(1.00, 200, 520, 4), (0.72, 180, 500, 4),
                                          (0.45, 210, 530, 4)]):
        p.arc([cx - r * rr, cy - r * rr, cx + r * rr, cy + r * rr], a0, a1, c, wd)
    p.ellipse([cx - r * 0.11, cy - r * 0.11, cx + r * 0.11, cy + r * 0.11], fill=INK)
    # coast and sea at the foot
    p.rect([x + w * 0.02, y + h * 0.92, x + w * 0.98, y + h * 0.96], fill=FAINT)
    for i in range(3):
        x0 = x + w * (0.10 + i * 0.30)
        p.arc([x0, y + h * 0.86, x0 + w * 0.18, y + h * 0.96], 190, 350, c, 3)


def icon_chart(p, x, y, w, h, c):
    """Bars stepping down, and a hard arrow through them."""
    base = y + h * 0.90
    heights = [0.62, 0.52, 0.40, 0.28, 0.18, 0.10]
    for i, hh in enumerate(heights):
        bx = x + w * (0.06 + i * 0.15)
        p.rect([bx, base - h * hh * 1.35, bx + w * 0.10, base], fill=c)
    p.line([(x + w * 0.08, y + h * 0.22), (x + w * 0.90, y + h * 0.62)], RED, 4)
    p.poly([(x + w * 0.90, y + h * 0.62), (x + w * 0.80, y + h * 0.60),
            (x + w * 0.86, y + h * 0.50)], RED)


def icon_deal(p, x, y, w, h, c):
    """Two sides meeting: a handshake reduced to two wedges and a clasp."""
    p.poly([(x + w * 0.04, y + h * 0.34), (x + w * 0.46, y + h * 0.34),
            (x + w * 0.46, y + h * 0.66), (x + w * 0.04, y + h * 0.66)], c)
    p.poly([(x + w * 0.54, y + h * 0.34), (x + w * 0.96, y + h * 0.34),
            (x + w * 0.96, y + h * 0.66), (x + w * 0.54, y + h * 0.66)], INK2)
    p.rect([x + w * 0.42, y + h * 0.44, x + w * 0.58, y + h * 0.56], fill="#F2C14E")
    p.rule(x + w * 0.02, x + w * 0.98, y + h * 0.86, 2, c)


def icon_climate(p, x, y, w, h, c):
    """A globe under a flame: the summit and the argument inside it."""
    r = min(w, h) * 0.30
    cx, cy = x + w * 0.34, y + h * 0.58
    p.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    p.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.20, cy + r * 0.05], fill="#FBF8F1")
    p.ellipse([cx - r * 0.10, cy + r * 0.10, cx + r * 0.62, cy + r * 0.60], fill="#FBF8F1")
    # flame, drawn as two nested teardrops
    fx, fy = x + w * 0.74, y + h * 0.56
    p.poly([(fx, fy - h * 0.34), (fx + w * 0.14, fy - h * 0.02),
            (fx + w * 0.06, fy + h * 0.16), (fx - w * 0.06, fy + h * 0.16),
            (fx - w * 0.14, fy - h * 0.02)], RED)
    p.poly([(fx, fy - h * 0.14), (fx + w * 0.06, fy + h * 0.02),
            (fx + w * 0.02, fy + h * 0.14), (fx - w * 0.02, fy + h * 0.14),
            (fx - w * 0.06, fy + h * 0.02)], "#F2C14E")
    p.rule(x + w * 0.02, x + w * 0.98, y + h * 0.92, 2, c)


def icon_missile(p, x, y, w, h, c):
    """A missile on its way down, and the trace it came along."""
    mx = x + w * 0.56
    p.line([(x + w * 0.10, y + h * 0.10), (mx - w * 0.04, y + h * 0.40)], FAINT, 2)
    # body
    p.poly([(mx, y + h * 0.26), (mx + w * 0.10, y + h * 0.46),
            (mx - w * 0.10, y + h * 0.46)], c)
    p.rect([mx - w * 0.10, y + h * 0.46, mx + w * 0.10, y + h * 0.74], fill=INK2)
    p.rect([mx - w * 0.10, y + h * 0.56, mx + w * 0.10, y + h * 0.62], fill=RED)
    for s in (-1, 1):
        p.poly([(mx + s * w * 0.10, y + h * 0.64), (mx + s * w * 0.24, y + h * 0.76),
                (mx + s * w * 0.10, y + h * 0.76)], RED)
    p.poly([(mx - w * 0.06, y + h * 0.74), (mx + w * 0.06, y + h * 0.74),
            (mx, y + h * 0.90)], "#F2C14E")


def icon_strike(p, x, y, w, h, c):
    """A placard held up, with a crowd bar under it."""
    p.rect([x + w * 0.16, y + h * 0.12, x + w * 0.84, y + h * 0.56], fill=c)
    p.rect([x + w * 0.46, y + h * 0.56, x + w * 0.54, y + h * 0.98], fill=INK2)
    for i in range(3):
        ly = y + h * (0.22 + i * 0.11)
        p.rect([x + w * 0.26, ly, x + w * (0.60 - i * 0.08), ly + h * 0.045], fill=PAPER)
    p.rect([x + w * 0.04, y + h * 0.90, x + w * 0.96, y + h * 0.94], fill=INK2)


def icon_militia(p, x, y, w, h, c):
    """An armoured vehicle: hull, turret, barrel, road wheels."""
    base = y + h * 0.80
    p.poly([(x + w * 0.06, y + h * 0.56), (x + w * 0.20, y + h * 0.34),
            (x + w * 0.78, y + h * 0.34), (x + w * 0.94, y + h * 0.56)], c)
    p.rect([x + w * 0.06, y + h * 0.56, x + w * 0.94, y + h * 0.72], fill=c)
    p.rect([x + w * 0.34, y + h * 0.22, x + w * 0.62, y + h * 0.34], fill=INK2)
    p.rect([x + w * 0.60, y + h * 0.25, x + w * 0.98, y + h * 0.30], fill=INK2)
    for i in range(4):
        wx = x + w * (0.16 + i * 0.20)
        p.ellipse([wx, base - h * 0.06, wx + w * 0.14, base + h * 0.10], fill=INK2)


def icon_nuclear(p, x, y, w, h, c):
    """The trefoil, plain and bold."""
    r = min(w, h) * 0.40
    cx, cy = x + w * 0.50, y + h * 0.50
    p.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#F2C14E")
    for k in range(3):
        a0 = -90 + k * 120 - 56
        p.pieslice([cx - r * 0.82, cy - r * 0.82, cx + r * 0.82, cy + r * 0.82],
                   a0, a0 + 66, INK)
    p.ellipse([cx - r * 0.26, cy - r * 0.26, cx + r * 0.26, cy + r * 0.26], fill="#F2C14E")


def icon_defence(p, x, y, w, h, c):
    """Two aircraft in echelon, drawn as swept chevrons."""
    for i, (dx, dy) in enumerate([(0.0, 0.30), (0.16, 0.02)]):
        ax, ay = x + w * (0.12 + dx), y + h * (0.66 - dy)
        p.poly([(ax, ay), (ax + w * 0.42, ay - h * 0.16), (ax + w * 0.30, ay + h * 0.06),
                (ax + w * 0.40, ay + h * 0.20), (ax + w * 0.16, ay + h * 0.10)],
               c if i == 0 else INK2)
    p.rule(x + w * 0.02, x + w * 0.98, y + h * 0.92, 2, c)


def icon_gavel(p, x, y, w, h, c):
    """A gavel head and its block: a court deciding."""
    p.rect([x + w * 0.14, y + h * 0.74, x + w * 0.86, y + h * 0.86], fill=INK2)
    p.rect([x + w * 0.36, y + h * 0.62, x + w * 0.64, y + h * 0.74], fill=c)
    # head, tilted above the block
    p.poly([(x + w * 0.44, y + h * 0.18), (x + w * 0.70, y + h * 0.06),
            (x + w * 0.80, y + h * 0.24), (x + w * 0.54, y + h * 0.36)], c)
    p.line([(x + w * 0.52, y + h * 0.34), (x + w * 0.28, y + h * 0.62)], INK2, 5)


def icon_currency(p, x, y, w, h, c):
    """A banknote with a falling arrow across it."""
    p.rect([x + w * 0.08, y + h * 0.30, x + w * 0.92, y + h * 0.74], fill=c, width=2)
    p.ellipse([x + w * 0.42, y + h * 0.42, x + w * 0.58, y + h * 0.62], fill=c)
    p.line([(x + w * 0.12, y + h * 0.18), (x + w * 0.88, y + h * 0.60)], RED, 4)
    p.poly([(x + w * 0.88, y + h * 0.60), (x + w * 0.76, y + h * 0.58),
            (x + w * 0.84, y + h * 0.47)], RED)
    p.rect([x + w * 0.08, y + h * 0.86, x + w * 0.92, y + h * 0.90], fill=FAINT)


def icon_blast(p, x, y, w, h, c):
    """A strike: a starburst over broken ground."""
    import math
    cx, cy, r = x + w * 0.50, y + h * 0.44, min(w, h) * 0.38
    for k in range(10):
        a = k * 36
        dx, dy = math.cos(math.radians(a)), math.sin(math.radians(a))
        p.poly([(cx + dx * r, cy + dy * r),
                (cx + dx * r * 0.34 - dy * r * 0.19, cy + dy * r * 0.34 + dx * r * 0.19),
                (cx + dx * r * 0.34 + dy * r * 0.19, cy + dy * r * 0.34 - dx * r * 0.19)], c)
    p.ellipse([cx - r * 0.26, cy - r * 0.26, cx + r * 0.26, cy + r * 0.26], fill="#F2C14E")
    p.rect([x + w * 0.04, y + h * 0.88, x + w * 0.96, y + h * 0.93], fill=INK2)


def icon_people(p, x, y, w, h, c):
    """Three figures on the move: heads and bodies, the middle one taller."""
    specs = [(0.22, 0.62), (0.50, 0.50), (0.78, 0.62)]
    for i, (fx, top) in enumerate(specs):
        cx = x + w * fx
        hr = min(w, h) * 0.10
        hy = y + h * top
        p.ellipse([cx - hr, hy - hr, cx + hr, hy + hr], fill=c if i != 1 else INK2)
        bw = min(w, h) * 0.13
        p.poly([(cx - bw, hy + hr * 1.2), (cx + bw, hy + hr * 1.2),
                (cx + bw * 0.75, y + h * 0.94), (cx - bw * 0.75, y + h * 0.94)],
               c if i != 1 else INK2)


def icon_derrick(p, x, y, w, h, c):
    """A drilling derrick over a wellhead, with a flare of new oil."""
    base = y + h * 0.86
    # derrick: an A-frame of cross-braced legs
    apex = (x + w * 0.50, y + h * 0.10)
    for side in (-1, 1):
        p.line([apex, (x + w * (0.50 + side * 0.26), base)], c, 3)
    for k in range(3):
        yy = y + h * (0.30 + k * 0.17)
        half = w * (0.10 + k * 0.055)
        p.line([(x + w * 0.50 - half, yy), (x + w * 0.50 + half, yy + h * 0.10)], INK2, 2)
        p.line([(x + w * 0.50 + half, yy), (x + w * 0.50 - half, yy + h * 0.10)], INK2, 2)
    p.rect([x + w * 0.36, base, x + w * 0.64, base + h * 0.07], fill=INK2)
    p.rect([x + w * 0.02, base + h * 0.07, x + w * 0.98, base + h * 0.11], fill=FAINT)


def icon_hospital(p, x, y, w, h, c):
    """A cross on a slab: the hospital, stated plainly."""
    p.rect([x + w * 0.10, y + h * 0.28, x + w * 0.90, y + h * 0.88], fill=c)
    cw, ch = w * 0.14, h * 0.34
    p.rect([x + w * 0.50 - cw / 2, y + h * 0.40, x + w * 0.50 + cw / 2, y + h * 0.40 + ch],
           fill=PAPER)
    p.rect([x + w * 0.50 - ch / 2, y + h * 0.40 + ch / 2 - cw / 2,
            x + w * 0.50 + ch / 2, y + h * 0.40 + ch / 2 + cw / 2], fill=PAPER)
    p.rect([x + w * 0.02, y + h * 0.90, x + w * 0.98, y + h * 0.94], fill=FAINT)


def icon_bat(p, x, y, w, h, c):
    """A cricket bat and a ball: the score, in two shapes."""
    p.poly([(x + w * 0.16, y + h * 0.88), (x + w * 0.34, y + h * 0.88),
            (x + w * 0.40, y + h * 0.30), (x + w * 0.24, y + h * 0.26)], c)
    p.line([(x + w * 0.28, y + h * 0.28), (x + w * 0.36, y + h * 0.06)], INK2, 5)
    br = min(w, h) * 0.13
    p.ellipse([x + w * 0.66 - br, y + h * 0.60 - br, x + w * 0.66 + br, y + h * 0.60 + br],
              fill=RED)
    p.arc([x + w * 0.66 - br, y + h * 0.60 - br, x + w * 0.66 + br, y + h * 0.60 + br],
          40, 140, PAPER, 2)


def icon_server(p, x, y, w, h, c):
    """Racks of servers, stacked, with a lit row each."""
    for i in range(3):
        ry = y + h * (0.18 + i * 0.24)
        p.rect([x + w * 0.14, ry, x + w * 0.86, ry + h * 0.18], fill=c)
        for k in range(3):
            p.rect([x + w * (0.20 + k * 0.20), ry + h * 0.06,
                    x + w * (0.20 + k * 0.20) + w * 0.04, ry + h * 0.11], fill=PAPER)
        p.rect([x + w * 0.74, ry + h * 0.05, x + w * 0.80, ry + h * 0.12], fill="#F2C14E")


def icon_robot(p, x, y, w, h, c):
    """A machine head with a visor and an antenna: the autonomous weapon."""
    p.rect([x + w * 0.18, y + h * 0.30, x + w * 0.82, y + h * 0.82], fill=c)
    p.rect([x + w * 0.28, y + h * 0.44, x + w * 0.72, y + h * 0.58], fill=INK)
    p.ellipse([x + w * 0.33, y + h * 0.47, x + w * 0.40, y + h * 0.55], fill="#F2C14E")
    p.ellipse([x + w * 0.60, y + h * 0.47, x + w * 0.67, y + h * 0.55], fill="#F2C14E")
    p.line([(x + w * 0.50, y + h * 0.30), (x + w * 0.50, y + h * 0.12)], INK2, 4)
    p.ellipse([x + w * 0.45, y + h * 0.04, x + w * 0.55, y + h * 0.14], fill=RED)
    for k in range(3):
        p.rect([x + w * (0.32 + k * 0.14), y + h * 0.64,
                x + w * (0.32 + k * 0.14) + w * 0.07, y + h * 0.70], fill=PAPER)


def icon_probe(p, x, y, w, h, c):
    """A deep-space probe: dish, bus and two panels."""
    p.ellipse([x + w * 0.34, y + h * 0.12, x + w * 0.66, y + h * 0.44], outline=c, width=4)
    p.rect([x + w * 0.44, y + h * 0.44, x + w * 0.56, y + h * 0.60], fill=INK2)
    for side in (-1, 1):
        p.rect([x + w * (0.50 + side * 0.38) - w * 0.10, y + h * 0.46,
                x + w * (0.50 + side * 0.38) + w * 0.10, y + h * 0.58], fill=c)
        p.line([(x + w * 0.50, y + h * 0.52), (x + w * (0.50 + side * 0.28), y + h * 0.52)],
               INK2, 2)
    p.line([(x + w * 0.50, y + h * 0.60), (x + w * 0.50, y + h * 0.88)], INK2, 3)


def icon_planet(p, x, y, w, h, c):
    """A planet with a rover track across it."""
    r = min(w, h) * 0.32
    cx, cy = x + w * 0.50, y + h * 0.46
    p.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    p.ellipse([cx - r * 0.42, cy - r * 0.52, cx + r * 0.10, cy - r * 0.06], fill=PAPER)
    p.ellipse([cx + r * 0.10, cy + r * 0.14, cx + r * 0.56, cy + r * 0.50], fill=PAPER)
    p.arc([cx - r * 1.55, cy - r * 0.30, cx + r * 1.55, cy + r * 0.30], 0, 360, INK2, 2)


def icon_art(p, x, y, w, h, c):
    """A framed mask: the returned object."""
    p.rect([x + w * 0.16, y + h * 0.10, x + w * 0.84, y + h * 0.90], outline=INK2, width=3)
    p.ellipse([x + w * 0.34, y + h * 0.22, x + w * 0.66, y + h * 0.72], fill=c)
    for side in (-1, 1):
        p.ellipse([x + w * 0.50 + side * w * 0.07 - w * 0.035, y + h * 0.38,
                   x + w * 0.50 + side * w * 0.07 + w * 0.035, y + h * 0.45], fill=INK)
    p.rect([x + w * 0.44, y + h * 0.56, x + w * 0.56, y + h * 0.60], fill=INK)


def icon_ship(p, x, y, w, h, c):
    """A cargo ship on a swell, with a warning burst above it."""
    p.poly([(x + w * 0.10, y + h * 0.58), (x + w * 0.90, y + h * 0.58),
            (x + w * 0.80, y + h * 0.76), (x + w * 0.20, y + h * 0.76)], fill=c)
    p.rect([x + w * 0.26, y + h * 0.44, x + w * 0.62, y + h * 0.58], fill=INK2)
    p.rect([x + w * 0.66, y + h * 0.36, x + w * 0.78, y + h * 0.58], fill=INK2)
    for i in range(3):
        x0 = x + w * (0.14 + i * 0.26)
        p.arc([x0, y + h * 0.76, x0 + w * 0.22, y + h * 0.88], 190, 350, c, 3)
    import math
    cx, cy, r = x + w * 0.50, y + h * 0.20, min(w, h) * 0.13
    for k in range(8):
        a = k * 45
        dx, dy = math.cos(math.radians(a)), math.sin(math.radians(a))
        p.poly([(cx + dx * r, cy + dy * r),
                (cx + dx * r * 0.40 - dy * r * 0.18, cy + dy * r * 0.40 + dx * r * 0.18),
                (cx + dx * r * 0.40 + dy * r * 0.18, cy + dy * r * 0.40 - dx * r * 0.18)], RED)


ICON = {
    "bridge": icon_bridge, "cyclone": icon_cyclone, "chart": icon_chart,
    "deal": icon_deal, "climate": icon_climate, "missile": icon_missile,
    "strike": icon_strike, "militia": icon_militia, "nuclear": icon_nuclear,
    "defence": icon_defence, "gavel": icon_gavel, "currency": icon_currency,
    "blast": icon_blast, "people": icon_people, "derrick": icon_derrick,
    "hospital": icon_hospital, "bat": icon_bat, "server": icon_server,
    "robot": icon_robot, "probe": icon_probe, "planet": icon_planet,
    "art": icon_art, "ship": icon_ship,
}




# ---------------------------------------------------------------- stories ---
# Every story below happened, or was first reported, on Friday 20 November 2026.
# Fields: number, region, dateline, beat, headline, standfirst, sources, icon.
LEADS = [
    (1, "Europe", "KYIV, UKRAINE", "WAR",
     "Russian missiles hit three Kyiv bridges",
     "An overnight barrage of 100-plus missiles and about 400 drones killed at least "
     "eight people across Ukraine and cut power and water in the capital.",
     "Kyiv Independent, Reuters", "bridge"),
    (2, "Asia", "ODISHA, INDIA", "CYCLONE",
     "Cyclone Akvan comes ashore in eastern India",
     "The storm crossed near Gopalpur after more than 300,000 people were moved to "
     "shelters: the third severe cyclone on that coast in a month.",
     "IMD, Reuters", "cyclone"),
    (3, "Global", "TAIPEI \u00b7 SEOUL \u00b7 TOKYO", "MARKETS",
     "An AI sell-off sinks Asia's markets",
     "Taiwan fell 6.2% for its worst week since 1991; Seoul lost 5.2% and Tokyo 5.1%, "
     "with chipmakers leading the slide.",
     "Al Jazeera, Reuters", "chart"),
]

CARDS = [
    (4, "Europe", "BRUSSELS", "BREXIT",
     "UK and EU seal a 'reset' deal", "Food trade, youth visas and a carbon link, ten years after the vote.",
     "Reuters, NYT", "deal"),
    (5, "Europe", "ANTALYA", "CLIMATE",
     "COP31 runs past its deadline with no deal", "The draft drops all mention of fossil fuels; talks go into overtime.",
     "Reuters, Guardian", "climate"),
    (6, "Europe", "WARSAW", "SECURITY",
     "A Russian missile lands in Poland", "NATO calls the airspace violation grave; Warsaw calls it a provocation.",
     "PBS, AFP", "missile"),
    (7, "Europe", "ROME", "LABOUR",
     "A general strike hits Italy", "Workers and students protest the budget; transport and schools stop.",
     "Reuters, FT", "strike"),
    (8, "Europe", "BRUSSELS", "UKRAINE",
     "EU adds \u20ac1bn in military aid", "Drones, air defence and ammunition, under the European Peace Facility.",
     "Council of the EU", "defence"),
    (9, "Middle East", "BAGHDAD", "IRAQ",
     "Iraqi troops enter a militia stronghold", "Security forces deploy into Jurf al-Sakhar, held by Iran-backed groups.",
     "NBC, VOA", "militia"),
    (10, "Middle East", "TEHRAN", "IRAN",
     "Trump: Iran will not make an 'acceptable' deal", "He says Tehran wants a deal on its own terms as talk turns to next steps.",
     "AP, Times of Israel", "nuclear"),
    (11, "Middle East", "SOUTHERN LEBANON", "LEBANON",
     "Israeli strikes hit four districts", "Attacks in the south cause fires and damage, hours after a strike on Riyadh.",
     "Middle East Monitor", "blast"),
    (12, "Africa", "MOYALE, ETHIOPIA", "DISPLACEMENT",
     "Nearly 700,000 displaced in the south", "Fighting on the Moyale border drives one of the year's largest displacements.",
     "Islamic Relief, Africanews", "people"),
    (13, "Africa", "TURKANA, KENYA", "ENERGY",
     "Kenya spuds its first production oil well", "Crude from Turkana is targeted for December, exports for March.",
     "Capital FM, The Star", "derrick"),
    (14, "Americas", "SAN SALVADOR", "POLITICS",
     "Bukele files to run for a third term", "A constitutional change lets him seek office again, to 2033.",
     "Al Jazeera, Le Monde", "gavel"),
    (15, "Americas", "BRASILIA", "BRAZIL",
     "Bolsonaro hospitalised with an obstruction", "The former president is treated for an intestinal blockage, his son says.",
     "Reuters, CNN", "hospital"),
    (16, "Americas", "MEXICO CITY", "MIGRATION",
     "Mexico issues 4,700 visas to Cubans", "Humanitarian visas granted as a new caravan of about 300 crosses the south.",
     "Yeni Safak, U.S. News", "people"),
    (17, "Asia", "NEW DELHI", "DEFENCE",
     "India and Japan deepen defence ties", "Focus on underwater and missile technology, with shared concern over China.",
     "Bloomberg, ThePrint", "defence"),
    (18, "Asia", "SEOUL", "POLITICS",
     "Ruling party moves to impeach the chief justice", "The Democratic Party formally adopts the drive over a ruling on Lee's trials.",
     "Yonhap", "gavel"),
    (19, "Asia", "JAKARTA", "ECONOMY",
     "Indonesia's rupiah hovers at record lows", "The currency stays near its weakest level as the central bank manages the slide.",
     "Bloomberg, FXStreet", "currency"),
    (20, "Asia", "COLOMBO", "RATES",
     "Sri Lanka raises its policy rate", "The central bank tightens to pull inflation back to target.",
     "Bloomberg", "currency"),
    (21, "Asia", "ULAN BATOR", "POLITICS",
     "Mongolia's president resigns", "The resignation sets the stage for an early presidential election.",
     "U.S. News", "gavel"),
    (22, "Oceania", "CANBERRA", "DIPLOMACY",
     "Australia and China agree to AI talks", "The two sides will hold high-level talks on artificial intelligence.",
     "ABC Australia, SCMP", "deal"),
    (23, "Oceania", "WELLINGTON", "CRICKET",
     "Phillips makes 118 against India", "New Zealand reach 317-6 at lunch on day two of the first test.",
     "AP", "bat"),
    (24, "Global", "NEW YORK", "MARKETS",
     "Wall Street slides into a correction", "The S&P 500 and Dow close in correction; the Nasdaq turns negative for the year.",
     "NYT, Reuters", "chart"),
    (25, "Global", "NEW YORK", "TECH",
     "Trump threatens penalties over AI data centres abroad", "He says he will penalise US firms that build them outside the country.",
     "AP, NBC", "server"),
    (26, "Global", "BEIJING", "NUCLEAR",
     "China's nuclear buildup is 'hot and heavy'", "Trump's warning comes a day after his summit with Xi in Shenzhen.",
     "AP", "nuclear"),
    (27, "Global", "GENEVA", "AI",
     "UN talks on 'killer robots' drag past deadline", "Russia stalls a bid to regulate autonomous weapons as time runs out.",
     "Euronews, U.S. News", "robot"),
    (28, "Global", "HOUSTON", "SPACE",
     "Voyager 1 stops sending science data", "The probe falls silent ahead of its light-day milestone; NASA has a plan.",
     "Live Science", "probe"),
    (29, "Global", "PASADENA", "SPACE",
     "Perseverance halts work on Mars", "The rover and the Odyssey orbiter pause science because of glitches.",
     "Space.com", "planet"),
    (30, "Europe", "PARIS", "CULTURE",
     "Benin asks for 35 looted artefacts back", "The request goes to a Paris museum for works taken in the colonial era.",
     "Africanews", "art"),
    (31, "Africa", "JOHANNESBURG", "SOCIETY",
     "South Africa: 581 women killed in three months", "The quarterly crime figures show killings averaging about 60 a day.",
     "Africanews, BBC", "people"),
    (32, "Africa", "MOGADISHU", "DIPLOMACY",
     "Somali protesters back expelling the UAE envoy", "Crowds come out in support of the government's move against the ambassador.",
     "Africanews", "people"),
    (33, "Americas", "WASHINGTON", "TRADE",
     "Hegseth restricts military ties with Canada", "The defence secretary curbs cooperation, the Washington Post reports.",
     "Washington Post", "defence"),
    (34, "Asia", "SHENZHEN", "SUMMIT",
     "Xi urges a trust-based partnership with Australia", "The two leaders meet in Shenzhen as Canberra balances trade and security.",
     "SCMP, Bloomberg", "deal"),
    (35, "Europe", "LONDON", "EUROPE",
     "Protests over pay sweep across Europe", "Young people stage coordinated marches for wages, services and living costs.",
     "Guardian, Euronews", "strike"),
    (36, "Global", "DUBAI", "ENERGY",
     "Gunmen fire on a cargo ship off Yemen", "The UK maritime agency reports the attack in the Red Sea approaches.",
     "UKMTO", "ship"),
]

REGION_ORDER = ["Europe", "Asia", "Middle East", "Africa", "Americas", "Oceania", "Global"]


def region_counts():
    counts = {}
    for row in (LEADS + CARDS):
        counts[row[1]] = counts.get(row[1], 0) + 1
    return counts


# ----------------------------------------------------------------- layout ---
STATS = [
    ("3", "Kyiv bridges damaged in the overnight barrage"),
    ("300,000+", "people evacuated before Akvan made landfall"),
    ("\u22126.2%", "Taiwan's index, its worst week since 1991"),
    ("\u20ac1bn", "new EU military aid for Ukraine"),
    ("700,000", "people displaced by fighting in southern Ethiopia"),
    ("4,700", "humanitarian visas Mexico issued to Cubans"),
]


def section_bar(p, y, h=4):
    p.rect([M, y, W - M, y + h], fill=INK)
    return y + h


def masthead(p, y):
    """The flag: the date, set as the largest thing on the page."""
    p.text(M, y, "THE WORLD IN ONE DAY", p.font(SANS_B, 11), RED)
    p.text(W - M, y + 1, "A VIEW OF THE WORLD'S NEWS", p.font(SANS_B, 9), GREY, anchor="ra")
    y += 16

    f = p.font(SERIF_B, 62)
    p.text(M, y, "Friday 20 November 2026", f, INK)
    y += 66

    # the deck: four teasers, comma-separated by interpuncts
    deck = ("Russian missiles hit three Kyiv bridges  \u00b7  Cyclone Akvan strikes India  \u00b7  "
            "An AI sell-off sinks Asia's markets  \u00b7  UK and EU seal a reset deal")
    f = p.font(SERIF_I, 15)
    for line in p.wrap(deck, f, W - 2 * M - 260):
        p.text(M, y, line, f, INK2)
        y += 18
    # the standing note, in the deck's right gutter
    note = p.font(SANS_B, 9)
    p.text(W - M, y - 36, "36 STORIES", note, RED, anchor="ra")
    p.text(W - M, y - 24, "7 REGIONS", note, INK2, anchor="ra")
    p.text(W - M, y - 12, "ALL ON ONE DAY", note, GREY, anchor="ra")
    y += 6
    return section_bar(p, y, 3)


def stat_strip(p, y):
    """Six numbers from the day, in a banded strip."""
    n = len(STATS)
    gap = 10
    cw = (W - 2 * M - gap * (n - 1)) / n
    ch = 46
    p.rect([M, y, W - M, y + ch], fill="#F1EBDE")
    for i, (num, label) in enumerate(STATS):
        x = M + i * (cw + gap)
        if i:
            p.rect([x - gap / 2 - 0.5, y + 8, x - gap / 2 + 0.5, y + ch - 8], fill=FAINT)
        p.text(x + 7, y + 5, num, p.font(SERIF_B, 21), INK)
        f = p.font(SANS_R, 7.6)
        ty = y + 30
        for line in p.wrap(label, f, cw - 12)[:2]:
            p.text(x + 7, ty, line, f, INK2)
            ty += 9
    return y + ch + 8


def region_bar(p, y):
    """The seven regions, each with its colour and its story count."""
    counts = region_counts()
    x = M
    f = p.font(SANS_B, 8.5)
    for region in REGION_ORDER:
        label = f"{region.upper()} {counts.get(region, 0)}"
        wd = p.tw(label, f) + 16
        p.rrect([x, y, x + wd, y + 16], 3, fill=REGION_COLOR[region])
        p.text(x + 8, y + 4.5, label, f, PAPER)
        x += wd + 5
    return y + 16 + 9


def kicker(p, x, y, n, region, dateline, beat, color, size=7.4):
    """The story's number, colour dot, dateline and beat."""
    f = p.font(SANS_B, size)
    p.text(x, y, f"{n}", p.font(SANS_B, size + 1.4), color)
    x += p.tw(f"{n} ", f) + 1
    p.ellipse([x, y + size * 0.42, x + 4, y + size * 0.42 + 4], fill=color)
    x += 8
    p.text(x, y, f"{dateline} \u00b7 {beat}", f, INK2)
    return y + size + 5


def lead(p, x, y, w, h, story):
    """One of the three leads: picture, kicker, headline, standfirst, source."""
    n, region, dateline, beat, head, stand, src, ic = story
    color = REGION_COLOR[region]
    iw = w
    ih = h * 0.47
    p.rect([x, y, x + iw, y + ih], fill="#EFE8D9")
    ICON[ic](p, x + iw * 0.06, y + ih * 0.08, iw * 0.88, ih * 0.84, color)
    p.text(x + 4, y + ih - 11, "Original drawing", p.font(SANS_R, 6.6), GREY)
    yy = y + ih + 7
    yy = kicker(p, x, yy, n, region, dateline, beat, color)
    f, lines = p.fit(head, SERIF_B, w, 2, 25, 13)
    for line in lines:
        p.text(x, yy, line, f, INK)
        yy += f.size / S * 1.04
    yy += 2
    f = p.font(SANS_R, 8.4)
    for line in p.wrap(stand, f, w)[:5]:
        p.text(x, yy, line, f, INK2)
        yy += 10.4
    p.text(x, y + h - 9, src, p.font(SANS_R, 6.8), GREY)


def card(p, x, y, w, h, story):
    """One of the ten cards: small picture, kicker, headline, one-line standfirst."""
    n, region, dateline, beat, head, stand, src, ic = story
    color = REGION_COLOR[region]
    iw = w
    ih = h * 0.50
    p.rect([x, y, x + iw, y + ih], fill="#EFE8D9")
    ICON[ic](p, x + iw * 0.10, y + ih * 0.10, iw * 0.80, ih * 0.80, color)
    yy = y + ih + 5
    yy = kicker(p, x, yy, n, region, dateline, beat, color, size=6.6)
    f, lines = p.fit(head, SERIF_B, w, 2, 16, 9.5)
    for line in lines[:2]:
        p.text(x, yy, line, f, INK)
        yy += f.size / S * 1.02
    yy += 1
    f = p.font(SANS_R, 7.0)
    for line in p.wrap(stand, f, w)[:2]:
        p.text(x, yy, line, f, INK2)
        yy += 8.4


def briefs(p, x, y, w, rows, ncols=3):
    """The rest of the day, as numbered one-liners."""
    p.text(x, y, "ALSO ON FRIDAY 20 NOVEMBER", p.font(SANS_B, 9), RED)
    p.text(x, y + 13, f"{len(rows)} more stories, each dated that day", p.font(SANS_I, 7.6), GREY)
    y += 27
    colw = (w - 12 * (ncols - 1)) / ncols
    per = (len(rows) + ncols - 1) // ncols
    for c in range(ncols):
        cx = x + c * (colw + 12)
        cy = y
        for story in rows[c * per:(c + 1) * per]:
            n, region, dateline, beat, head, stand, src, ic = story
            color = REGION_COLOR[region]
            p.text(cx, cy, f"{n}", p.font(SANS_B, 7.6), color)
            f = p.font(SANS_R, 7.2)
            lines = p.wrap(head, f, colw - 13)[:2]
            ty = cy
            for line in lines:
                p.text(cx + 13, ty, line, f, INK)
                ty += 8.6
            p.text(cx + 13, ty, src.split(",")[0], p.font(SANS_R, 6.4), GREY)
            cy = ty + 9.6


def date_check(p, x, y, w):
    """The note that keeps the page honest about the one-day rule."""
    p.rect([x, y, x + w, y + 2], fill=RED)
    p.text(x, y + 6, "DATE CHECK", p.font(SANS_B, 8.4), RED)
    f = p.font(SANS_R, 7.4)
    body = ("Left out as Thursday 19 November's news: the World Court's ruling on Myanmar and "
            "Tonga's drought emergency. Not yet happened, so not shown: any final COP31 text.")
    ty = y + 18
    for line in p.wrap(body, f, w)[:3]:
        p.text(x, ty, line, f, INK2)
        ty += 9
    return ty


def build():
    p = Page()
    counts = region_counts()
    total = len(LEADS) + len(CARDS)

    y = M
    y = masthead(p, y)
    y = stat_strip(p, y)
    y = region_bar(p, y)
    y = section_bar(p, y, 2)

    # --- the three leads
    lead_top = y + 9
    lead_h = 232
    gap = 16
    lw = (W - 2 * M - gap * 2) / 3
    for i, story in enumerate(LEADS):
        lead(p, M + i * (lw + gap), lead_top, lw, lead_h, story)
        if i:
            p.rect([M + i * (lw + gap) - gap / 2 - 0.5, lead_top,
                    M + i * (lw + gap) - gap / 2 + 0.5, lead_top + lead_h], fill=FAINT)
    y = lead_top + lead_h + 8
    y = section_bar(p, y, 2)

    # --- the ten cards, 5 x 2
    card_top = y + 9
    cols, rows_ = 5, 2
    cg = 11
    cw = (W - 2 * M - cg * (cols - 1)) / cols
    chh = 148
    grid = CARDS[:cols * rows_]
    for i, story in enumerate(grid):
        c, r = i % cols, i // cols
        card(p, M + c * (cw + cg), card_top + r * (chh + 10), cw, chh, story)
    y = card_top + rows_ * chh + 10 * (rows_ - 1) + 7
    y = section_bar(p, y, 2)

    # --- the footer: briefs on the left, the map slot and date check on the right
    y += 9
    foot_h = H - M - y
    brief_w = (W - 2 * M) * 0.66
    briefs(p, M, y, brief_w, CARDS[cols * rows_:])
    # the date check sits in the right third, under a small world map
    rx = M + brief_w + 22
    rw = W - M - rx
    map_h = foot_h - 78
    draw_map(p, rx, y, rw, map_h)
    date_check(p, rx, y + map_h + 6, rw)

    p.save("entry.png")
    print(f"wrote entry.png: {total} dated stories, {len(REGION_ORDER)} regions, "
          f"{sum(counts.values())} numbered")
    return p


def draw_map(p, x, y, w, h):
    """A small world map: the story regions in their colours."""
    p.text(x, y, "WHERE IT HAPPENED", p.font(SANS_B, 8.4), RED)
    p.text(x, y + 12, "Each region, and how many of the day's stories it holds",
           p.font(SANS_R, 6.6), GREY)
    # a simple graticule with blocks standing for regions, in their colours
    top = y + 26
    bw = (w - 8 * 2) / 7
    order = ["Americas", "Europe", "Africa", "Middle East", "Asia", "Oceania", "Global"]
    counts = region_counts()
    mx = max(counts.values())
    for i, region in enumerate(order):
        bh = max(4.0, (h - 40) * (counts.get(region, 0) / mx))
        bx = x + i * bw + 4
        p.rect([bx, top + (h - 46) - bh, bx + bw - 8, top + (h - 46)],
               fill=REGION_COLOR[region])
        p.text(bx + (bw - 8) / 2, top + (h - 46) - bh - 9,
               str(counts.get(region, 0)), p.font(SANS_B, 7.4), INK, anchor="ma")
    p.rect([x, top + (h - 46), x + w, top + (h - 46) + 1], fill=FAINT)
    for i, region in enumerate(order):
        f = p.font(SANS_R, 5.6)
        lbl = region[:7].upper()
        p.text(x + i * bw + 4 + (bw - 8) / 2, top + (h - 46) + 3, lbl, f, GREY, anchor="ma")


if __name__ == "__main__":
    build()
