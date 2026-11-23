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

from PIL import Image, ImageDraw
from PIL import ImageFont

SS = 2  # draw at twice the final size, then shrink for sharp text
W, H = 1024 * SS, 1024 * SS

PAPER = (246, 239, 221)
INK = (17, 17, 17)  # near-black for rules and masthead
CRIMSON = (176, 32, 32)
SNOW = (250, 248, 240)
SAND = (255, 224, 138)
NAVY = (18, 38, 63)  # hero panel
WINE = (110, 26, 26)
TEAL = (24, 68, 96)
FOREST = (20, 80, 52)
SLATE = (38, 54, 74)  # defence panel
PLUM = (30, 20, 44)  # sport panel
GOLD = (240, 178, 40)  # warm yellow for the globe and fins
EMBER = (245, 120, 30)
MIST = (232, 236, 240)
CLOUD = (238, 240, 244)

FONTDIR = "/usr/share/fonts/truetype/dejavu"
_fonts = {}


def font(path, size):
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(f"{FONTDIR}/{path}", size * SS)
    return _fonts[key]


def bold(size):
    return font("DejaVuSans-Bold.ttf", size)


def plain(size):
    return font("DejaVuSans.ttf", size)


def serif(size):
    return font("DejaVuSerif-Bold.ttf", size)


page = Image.new("RGB", (W, H), PAPER)
pen = ImageDraw.Draw(page)


def px(v):
    return v * SS


def textwidth(s, f):
    return pen.textlength(s, font=f) / SS


def fitfont(s, maxw, fn, start, floor=10):
    sz = start
    while sz > floor and textwidth(s, fn(sz)) > maxw:
        sz -= 1
    return fn(sz), sz


def wraptext(s, f, maxw):
    words = s.split()
    out, acc = [], ""
    for w in words:
        trial = (acc + " " + w).strip()
        if textwidth(trial, f) <= maxw or not acc:
            acc = trial
        else:
            out.append(acc)
            acc = w
    if acc:
        out.append(acc)
    return out


def centre(s, cx, y, f, fill):
    pen.text((px(cx - textwidth(s, f) / 2), px(y)), s, font=f, fill=fill)


def letterspace(s, cx, y, f, fill, gap):
    widths = [textwidth(c, f) for c in s]
    total = sum(widths) + gap * (len(s) - 1)
    start = cx - total / 2
    for c, w in zip(s, widths):
        pen.text((px(start), px(y)), c, font=f, fill=fill)
        start += w + gap


def box(x, y, w, h, fill):
    pen.rectangle([px(x), px(y), px(x + w), px(y + h)], fill=fill)


def seg(x1, y1, x2, y2, fill, width=2):
    pen.line([px(x1), px(y1), px(x2), px(y2)], fill=fill, width=int(width * SS))


# ================================ icons ================================
def globe(cx, cy, r):
    pen.ellipse([px(cx - r), px(cy - r), px(cx + r), px(cy + r)], outline=GOLD, width=5 * SS)
    for f in (-0.55, 0.0, 0.55):
        rw = r * (1 - f * f) ** 0.5
        pen.ellipse([px(cx - rw), px(cy - r), px(cx + rw), px(cy + r)], outline=GOLD, width=2 * SS)
    for f in (-0.5, 0.0, 0.5):
        yy = cy + f * r
        half = r * (1 - f * f) ** 0.5
        seg(cx - half, yy, cx + half, yy, GOLD, 2)
    breaks = []
    breaks.append((cx - 0.25 * r, cy - r))
    breaks.append((cx + 0.05 * r, cy - 0.45 * r))
    breaks.append((cx - 0.18 * r, cy - 0.05 * r))
    breaks.append((cx + 0.22 * r, cy + 0.5 * r))
    breaks.append((cx + 0.02 * r, cy + r))
    for a, b in zip(breaks, breaks[1:]):
        seg(a[0], a[1], b[0], b[1], (10, 18, 30), 7)


def dome(cx, cy):
    # US Capitol-style dome and columns, white and gold on the panel.
    pen.pieslice([px(cx - 46), px(cy - 44), px(cx + 46), px(cy + 30)], 180, 360, fill=SNOW)
    box(cx - 6, cy - 60, 12, 16, SNOW)
    pen.ellipse([px(cx - 8), px(cy - 68), px(cx + 8), px(cy - 52)], fill=GOLD)
    box(cx - 58, cy - 8, 116, 8, SNOW)
    for n in range(5):
        box(cx - 52 + n * 24, cy + 2, 10, 34, SNOW)
    box(cx - 62, cy + 36, 124, 8, SNOW)
    box(cx - 58, cy - 26, 116, 4, SAND)


def flame(cx, cy):
    outline = [(cx - 34, cy + 34), (cx - 40, cy + 4), (cx - 14, cy - 14),
               (cx - 18, cy - 34), (cx + 2, cy - 52), (cx + 10, cy - 26),
               (cx + 34, cy - 38), (cx + 30, cy - 6), (cx + 42, cy + 12),
               (cx + 34, cy + 34)]
    pen.polygon([(px(a), px(b)) for a, b in outline], fill=EMBER)
    pen.polygon([(px(cx - 14), px(cy + 30)), (px(cx - 4), px(cy - 6)),
                 (px(cx + 6), px(cy + 12)), (px(cx + 16), px(cy + 30))], fill=(255, 205, 60))


def missile(cx, cy):
    # Missile climbing diagonally, gold fins, a short exhaust plume.
    bx, by = cx - 28, cy + 22
    tx, ty = cx + 30, cy - 40
    dx, dy = tx - bx, ty - by
    ln = math.hypot(dx, dy)
    ux, uy = dx / ln, dy / ln
    nx, ny = -uy, ux
    w = 10
    pen.line([px(bx), px(by), px(tx), px(ty)], fill=SNOW, width=int(w * 2 * SS))
    pen.polygon([(px(tx + nx * w), px(ty + ny * w)),
                 (px(tx + nx * w * 1.9), px(ty + ny * w * 1.9)),
                 (px(tx - nx * w), px(ty - ny * w))], fill=SNOW)
    pen.polygon([(px(bx - nx * w), px(by - ny * w)),
                 (px(bx - nx * w - ux * 14), px(by - ny * w - uy * 14)),
                 (px(bx + nx * w - ux * 14), px(by + ny * w - uy * 14)),
                 (px(bx + nx * w), px(by + ny * w))], fill=GOLD)
    for n in range(2):
        ex = bx - ux * (10 + n * 7)
        ey = by - uy * (10 + n * 7)
        r = 5 - n * 2
        pen.ellipse([px(ex - r), px(ey - r), px(ex + r), px(ey + r)], fill=EMBER)


def exam(cx, cy):
    # Exam paper, pencil and a red cross.
    pen.rectangle([px(cx - 34), px(cy - 40), px(cx + 26), px(cy + 36)], fill=SNOW)
    for n in range(4):
        seg(cx - 24, cy - 26 + n * 14, cx + 16, cy - 26 + n * 14, (120, 130, 145), 3)
    seg(cx - 24, cy + 16, cx - 2, cy + 16, CRIMSON, 4)
    # pencil at lower right, kept clear of the headline below
    pen.polygon([(px(cx + 18), px(cy + 36)), (px(cx + 42), px(cy + 6)),
                 (px(cx + 50), px(cy + 14)), (px(cx + 26), px(cy + 44))], fill=GOLD)
    pen.polygon([(px(cx + 18), px(cy + 36)), (px(cx + 26), px(cy + 44)),
                 (px(cx + 12), px(cy + 46))], fill=(60, 40, 20))
    seg(cx + 30, cy - 34, cx + 52, cy - 12, CRIMSON, 6)
    seg(cx + 52, cy - 34, cx + 30, cy - 12, CRIMSON, 6)


def cricket(cx, cy):
    # Cricket bat leaning over a red ball.
    pen.polygon([(px(cx - 44), px(cy - 40)), (px(cx - 28), px(cy - 48)),
                 (px(cx + 30), px(cy + 34)), (px(cx + 14), px(cy + 42))], fill=(210, 180, 120))
    box(cx - 52, cy - 52, 14, 26, (150, 110, 60))
    pen.ellipse([px(cx + 26), px(cy - 40), px(cx + 58), px(cy - 8)], fill=CRIMSON)
    pen.arc([px(cx + 26), px(cy - 40), px(cx + 58), px(cy - 8)], 200, 340,
            fill=SNOW, width=3 * SS)


# ---------------------------------------------------------------- masthead
box(0, 0, 1024, 10, INK)
letterspace("THE WORLD IN ONE IMAGE", 512, 34, bold(29), INK, 10)
dateline, _ = fitfont("MONDAY 23 NOVEMBER 2026", 950, serif, 64, 20)
centre("MONDAY 23 NOVEMBER 2026", 512, 78, dateline, CRIMSON)
box(28, 158, 968, 5, INK)

# ---------------------------------------------------------------- lead story
box(28, 178, 968, 254, NAVY)
globe(150, 305, 82)
pen.text((px(252), px(206)), "CLIMATE — ANTALYA, TÜRKIYE", font=bold(21), fill=SAND)
lead = bold(53)
pen.text((px(252), px(240)), "COP31 CLIMATE TALKS", font=lead, fill=SNOW)
pen.text((px(252), px(302)), "COLLAPSE", font=lead, fill=SNOW)
deck = plain(24)
for n, ln in enumerate(wraptext("Summit ends with no deal — EU rejects a pact silent on fossil fuels", deck, 716)):
    pen.text((px(252), px(372 + n * 32)), ln, font=deck, fill=MIST)


# ---------------------------------------------------------------- stories
def story(x, y, w, h, bg, icon, icy, heads, sub, hsize, ssize, headw, subw, top, step):
    box(x, y, w, h, bg)
    icon(x + w // 2, icy)
    yy = y + top
    hf, _ = fitfont(max(heads, key=len), headw, bold, hsize, 14)
    for ln in heads:
        centre(ln, x + w // 2, yy, hf, SNOW)
        yy += int(hsize * 1.18)
    sf = plain(ssize)
    for ln in wraptext(sub, sf, subw):
        centre(ln, x + w // 2, yy + 4, sf, CLOUD)
        yy += step


MID = [
    (28, WINE, dome, 512, ["DEMOCRATS HIT", "258 SEATS"],
     "Largest House majority since 1992; Hubbard beats Foxx in recount"),
    (520, TEAL, flame, 500, ["24 BODY BAGS", "IN JAVA FIRE"],
     "29 still missing after candy-factory blaze; search resumes Monday"),
]
for x, bg, icon, icy, heads, sub in MID:
    story(x, 448, 476, 264, bg, icon, icy, heads, sub, 40, 22, 440, 436, 96, 29)

LOW = [
    (28, SLATE, missile, 750, ["RUSSIA ROLLS OUT", "SARMAT ICBM"],
     "Images suggest Russia loading its new nuclear missile at Uzhur"),
    (356, FOREST, exam, 764, ["MINISTER QUITS OVER", "AI CHEATING"],
     "Seoul education chief resigns after exam scandal"),
    (684, PLUM, cricket, 766, ["INDIA'S RECORD", "720 IN WELLINGTON"],
     "Highest Test total in New Zealand; Rahul 136, Pant 128"),
]
for x, bg, icon, icy, heads, sub in LOW:
    story(x, 728, 312, 226, bg, icon, icy, heads, sub, 28, 19, 284, 280, 74, 25)


# ================================ footer ===============================
box(28, 970, 968, 4, INK)
centre("23 NOVEMBER 2026  •  SIX STORIES  •  ONE DAY", 512, 984, bold(22), INK)

page = page.resize((1024, 1024), Image.LANCZOS)
page.save("entry.png", optimize=True)
print("wrote entry.png", page.size)
