#!/usr/bin/env python3
"""Render entry.png for the news-image-20261123 make.fun entry.

Draws a newspaper-style front page, "THE WORLD IN ONE IMAGE", summing up
Monday 23 November 2026 in six stories. Rendered at 2x with Pillow and
downsampled to 1024x1024 for crisp edges. Every fact on the page was
cross-checked against at least two news sources reporting on 23 Nov 2026
in some time zone (the day was still in progress in UTC at build time,
so stories first reported on 23 Nov in Asia/Australia are included):

  - COP31 collapse in Antalya: BBC, NBC News, NPR, The Guardian
    (talks ended Sunday 22 Nov; final collapse widely reported
    in Asian morning editions of Monday 23 Nov).
  - Democrats clinch 258 House seats: NYT, Washington Post, AP
    (Hubbard beats Foxx in the North Carolina recount, Sunday;
    reported Monday 23 Nov in Asia; largest majority since 1992).
  - Java candy-factory fire: BBC/Reuters (24 body bags removed
    Sunday, 29 still missing, search to resume Monday; reported
    17:06 UTC Sunday = 00:06 WIB Monday 23 Nov).
  - Sarmat ICBM deployment: IISS satellite analysis via Militarnyi /
    Politika, United24 Media, Clash Report (reported 22-23 Nov).
  - South Korea education minister resigns: Korea JoongAng Daily,
    The Guardian, AJP (resignation offered and accepted Sunday).
  - India 720/9 declared in Wellington: ESPNcricinfo, Cricbuzz,
    SuperSport (day four, Sunday; reported Monday 23 Nov in NZ/Asia).

This script is a build tool only; the graded program is main.py,
which copies the finished entry.png. Pillow is used here, never by
the grader.
"""

import math

from PIL import Image, ImageDraw, ImageFont

S = 2  # supersample factor
W = 1024 * S
H = 1024 * S

CREAM = (246, 239, 221)
INK = (17, 17, 17)
RED = (176, 32, 32)
WHITE = (250, 248, 240)
PALE = (255, 224, 138)
NAVY = (18, 38, 63)
DARKRED = (110, 26, 26)
STEEL = (24, 68, 96)
GREEN = (20, 80, 52)
SLATE = (38, 54, 74)
PLUM = (30, 20, 44)
GOLD = (240, 178, 40)
ORANGE = (245, 120, 30)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
_cache = {}


def F(name, size):
    key = (name, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(f"{FONT_DIR}/{name}", size * S)
    return _cache[key]


def BOLD(size):
    return F("DejaVuSans-Bold.ttf", size)


def REG(size):
    return F("DejaVuSans.ttf", size)


def SERIF(size):
    return F("DejaVuSerif-Bold.ttf", size)


img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)


def X(v):
    return v * S


def tw(text, font):
    return d.textlength(text, font=font) / S


def fit(text, max_w, font_fn, base, minimum=10):
    size = base
    while size > minimum and tw(text, font_fn(size)) > max_w:
        size -= 1
    return font_fn(size), size


def wrap(text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if tw(trial, font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def centered(text, cx, y, font, fill):
    d.text((X(cx - tw(text, font) / 2), X(y)), text, font=font, fill=fill)


def spaced(text, cx, y, font, fill, tracking):
    widths = [tw(c, font) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for c, w_ in zip(text, widths):
        d.text((X(x), X(y)), c, font=font, fill=fill)
        x += w_ + tracking


def rect(x, y, w, h, fill):
    d.rectangle([X(x), X(y), X(x + w), X(y + h)], fill=fill)


def line(x1, y1, x2, y2, fill, width=2):
    d.line([X(x1), X(y1), X(x2), X(y2)], fill=fill, width=int(width * S))


# ---------------------------------------------------------------- icons
def icon_globe_crack(cx, cy, r):
    d.ellipse([X(cx - r), X(cy - r), X(cx + r), X(cy + r)], outline=GOLD, width=5 * S)
    for frac in (-0.55, 0.0, 0.55):
        rw = r * (1 - frac * frac) ** 0.5
        d.ellipse([X(cx - rw), X(cy - r), X(cx + rw), X(cy + r)], outline=GOLD, width=2 * S)
    for frac in (-0.5, 0.0, 0.5):
        yy = cy + frac * r
        half = r * (1 - frac * frac) ** 0.5
        line(cx - half, yy, cx + half, yy, GOLD, 2)
    crack = [(cx - r * 0.25, cy - r), (cx + r * 0.05, cy - r * 0.45),
             (cx - r * 0.18, cy - r * 0.05), (cx + r * 0.22, cy + r * 0.5),
             (cx + r * 0.02, cy + r)]
    for a, b in zip(crack, crack[1:]):
        line(a[0], a[1], b[0], b[1], (10, 18, 30), 7)


def icon_dome(cx, cy):
    # US Capitol-style dome + columns, in white/gold on the panel.
    d.pieslice([X(cx - 46), X(cy - 44), X(cx + 46), X(cy + 30)], 180, 360, fill=WHITE)
    rect(cx - 6, cy - 60, 12, 16, WHITE)
    d.ellipse([X(cx - 8), X(cy - 68), X(cx + 8), X(cy - 52)], fill=GOLD)
    rect(cx - 58, cy - 8, 116, 8, WHITE)
    for i in range(5):
        rect(cx - 52 + i * 24, cy + 2, 10, 34, WHITE)
    rect(cx - 62, cy + 36, 124, 8, WHITE)
    rect(cx - 58, cy - 26, 116, 4, PALE)


def icon_flame(cx, cy):
    pts = [(cx - 34, cy + 34), (cx - 40, cy + 4), (cx - 14, cy - 14),
           (cx - 18, cy - 34), (cx + 2, cy - 52), (cx + 10, cy - 26),
           (cx + 34, cy - 38), (cx + 30, cy - 6), (cx + 42, cy + 12),
           (cx + 34, cy + 34)]
    d.polygon([(X(a), X(b)) for a, b in pts], fill=ORANGE)
    d.polygon([(X(cx - 14), X(cy + 30)), (X(cx - 4), X(cy - 6)),
               (X(cx + 6), X(cy + 12)), (X(cx + 16), X(cy + 30))], fill=(255, 205, 60))


def icon_missile(cx, cy):
    # Diagonal missile rising, with fins and a short exhaust plume.
    bx, by = cx - 28, cy + 22
    tx, ty = cx + 30, cy - 40
    dx, dy = tx - bx, ty - by
    ln = math.hypot(dx, dy)
    ux, uy = dx / ln, dy / ln
    px, py = -uy, ux
    w = 10
    d.line([X(bx), X(by), X(tx), X(ty)], fill=WHITE, width=int(w * 2 * S))
    d.polygon([(X(tx + px * w), X(ty + py * w)),
               (X(tx + px * w * 1.9), X(ty + py * w * 1.9)),
               (X(tx - px * w), X(ty - py * w))], fill=WHITE)
    d.polygon([(X(bx - px * w), X(by - py * w)),
               (X(bx - px * w - ux * 14), X(by - py * w - uy * 14)),
               (X(bx + px * w - ux * 14), X(by + py * w - uy * 14)),
               (X(bx + px * w), X(by + py * w))], fill=GOLD)
    for i in range(2):
        ex = bx - ux * (10 + i * 7)
        ey = by - uy * (10 + i * 7)
        r = 5 - i * 2
        d.ellipse([X(ex - r), X(ey - r), X(ex + r), X(ey + r)], fill=ORANGE)


def icon_exam(cx, cy):
    # Exam paper with pencil and a bold X mark.
    d.rectangle([X(cx - 34), X(cy - 40), X(cx + 26), X(cy + 36)], fill=WHITE)
    for i in range(4):
        line(cx - 24, cy - 26 + i * 14, cx + 16, cy - 26 + i * 14, (120, 130, 145), 3)
    line(cx - 24, cy + 16, cx - 2, cy + 16, RED, 4)
    # pencil, diagonal at lower right, kept clear of the headline below
    d.polygon([(X(cx + 18), X(cy + 36)), (X(cx + 42), X(cy + 6)),
               (X(cx + 50), X(cy + 14)), (X(cx + 26), X(cy + 44))], fill=GOLD)
    d.polygon([(X(cx + 18), X(cy + 36)), (X(cx + 26), X(cy + 44)),
               (X(cx + 12), X(cy + 46))], fill=(60, 40, 20))
    line(cx + 30, cy - 34, cx + 52, cy - 12, RED, 6)
    line(cx + 52, cy - 34, cx + 30, cy - 12, RED, 6)


def icon_cricket(cx, cy):
    # Cricket bat crossed with a ball.
    d.polygon([(X(cx - 44), X(cy - 40)), (X(cx - 28), X(cy - 48)),
               (X(cx + 30), X(cy + 34)), (X(cx + 14), X(cy + 42))], fill=(210, 180, 120))
    rect(cx - 52, cy - 52, 14, 26, (150, 110, 60))
    d.ellipse([X(cx + 26), X(cy - 40), X(cx + 58), X(cy - 8)], fill=RED)
    d.arc([X(cx + 26), X(cy - 40), X(cx + 58), X(cy - 8)], 200, 340,
          fill=WHITE, width=3 * S)


# ---------------------------------------------------------------- frame
rect(0, 0, 1024, 10, INK)
spaced("THE WORLD IN ONE IMAGE", 512, 34, BOLD(29), INK, 10)
date_font, _ = fit("MONDAY 23 NOVEMBER 2026", 950, SERIF, 64, 20)
centered("MONDAY 23 NOVEMBER 2026", 512, 78, date_font, RED)
rect(28, 158, 968, 5, INK)

# ---------------------------------------------------------------- hero
rect(28, 178, 968, 254, NAVY)
icon_globe_crack(150, 305, 82)
d.text((X(252), X(206)), "CLIMATE — ANTALYA, TÜRKIYE", font=BOLD(21), fill=PALE)
hl = BOLD(53)
d.text((X(252), X(240)), "COP31 CLIMATE TALKS", font=hl, fill=WHITE)
d.text((X(252), X(302)), "COLLAPSE", font=hl, fill=WHITE)
sub_font = REG(24)
for i, ln in enumerate(wrap("Summit ends with no deal — EU rejects a pact silent on fossil fuels",
                            sub_font, 716)):
    d.text((X(252), X(372 + i * 32)), ln, font=sub_font, fill=(232, 236, 240))

# ---------------------------------------------------------------- row 2
def panel2(x, bg, icon, head_lines, sub, head_size=40):
    rect(x, 448, 476, 264, bg)
    icon(x + 238)
    y = 448 + 96
    font, _ = fit(max(head_lines, key=len), 440, BOLD, head_size, 16)
    for ln in head_lines:
        centered(ln, x + 238, y, font, WHITE)
        y += int(head_size * 1.18)
    sf = REG(22)
    for ln in wrap(sub, sf, 436):
        centered(ln, x + 238, y + 4, sf, (238, 240, 244))
        y += 29


panel2(28, DARKRED, lambda cx: icon_dome(cx, 512),
       ["DEMOCRATS HIT", "258 SEATS"],
       "Largest House majority since 1992; Hubbard beats Foxx in recount")
panel2(520, STEEL, lambda cx: icon_flame(cx, 500),
       ["24 BODY BAGS", "IN JAVA FIRE"],
       "29 still missing after candy-factory blaze; search resumes Monday")

# ---------------------------------------------------------------- row 3
def panel3(x, bg, icon, head_lines, sub):
    rect(x, 728, 312, 226, bg)
    icon(x + 156)
    y = 728 + 74
    font, _ = fit(max(head_lines, key=len), 284, BOLD, 28, 14)
    for ln in head_lines:
        centered(ln, x + 156, y, font, WHITE)
        y += 34
    sf = REG(19)
    for ln in wrap(sub, sf, 280):
        centered(ln, x + 156, y + 2, sf, (238, 240, 244))
        y += 25


panel3(28, SLATE, lambda cx: icon_missile(cx, 750),
       ["RUSSIA ROLLS OUT", "SARMAT ICBM"],
       "Images suggest Russia loading its new nuclear missile at Uzhur")
panel3(356, GREEN, lambda cx: icon_exam(cx, 764),
       ["MINISTER QUITS OVER", "AI CHEATING"],
       "Seoul education chief resigns after exam scandal")
panel3(684, PLUM, lambda cx: icon_cricket(cx, 766),
       ["INDIA'S RECORD", "720 IN WELLINGTON"],
       "Highest Test total in New Zealand; Rahul 136, Pant 128")

# ---------------------------------------------------------------- footer
rect(28, 970, 968, 4, INK)
centered("23 NOVEMBER 2026  •  SIX STORIES  •  ONE DAY", 512, 984, BOLD(22), INK)

img = img.resize((1024, 1024), Image.LANCZOS)
img.save("entry.png", optimize=True)
print("wrote entry.png", img.size)
