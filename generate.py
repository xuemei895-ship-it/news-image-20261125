#!/usr/bin/env python3
"""Generate the 1024x1024 news front page for make.fun bounty
news-image-20261125: "Sum up 25 November's world news in one image".

Deterministic: no network, no randomness, no timestamps in the output.
Run:  python3 generate.py   (writes assets/entry.png)
The entry program (main.py) copies assets/entry.png to
$MAKEFUN_OUTPUT_DIR/entry.png, which the bounty brief explicitly allows:
"the simplest program copies an image the repository holds".

Stories (all verified from public reporting on 25 Nov 2026; see SOURCES.md):
  1. Zelenskiy confirms Ukraine drone strike on Russian ship in Gulf of Finland.
  2. Houthis hit Riyadh's tallest tower, 11 wounded.
  3. China investigates Politburo member Chen Jining.
  4. US jury convicts Huawei of stealing trade secrets.
  5. Trump awards Rudy Giuliani the Medal of Freedom.
  6. Hamas security chief killed in Israeli air strike on Gaza City.
Plus a ticker: Iraq seizes Kurdish oilfields, UN femicide stat, Senegal AFCON
title restored, Shein $100M FTC settlement, Iran currency plunge, Thanksgiving
turkeys pardoned.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "entry.png")

W = H = 1024
PAPER = (248, 244, 235)
INK = (24, 24, 24)
RED = (176, 32, 32)
BLUE = (28, 74, 118)
TEAL = (13, 108, 108)
GOLD = (172, 122, 20)
LIGHT = (234, 227, 212)
GREY = (98, 98, 98)
WHITE = (255, 255, 255)
YELLOW = (255, 213, 64)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_b(s):
    return font("DejaVuSerif-Bold.ttf", s)


def serif(s):
    return font("DejaVuSerif.ttf", s)


def sans_b(s):
    return font("DejaVuSans-Bold.ttf", s)


def sans(s):
    return font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- icons
def icon_ship(d, x, y, s, col):
    # hull and mast
    d.polygon([(x, y + s * 0.52), (x + s, y + s * 0.52),
               (x + s * 0.84, y + s * 0.82), (x + s * 0.16, y + s * 0.82)],
              fill=col)
    d.line([(x + s * 0.5, y + s * 0.52), (x + s * 0.5, y + s * 0.1)],
           fill=col, width=4)
    d.polygon([(x + s * 0.5, y + s * 0.12), (x + s * 0.84, y + s * 0.4),
               (x + s * 0.5, y + s * 0.4)], fill=col)
    for yy in (y + s * 0.9, y + s * 0.97):
        d.line([(x + 4, yy), (x + s - 4, yy)], fill=col, width=3)


def icon_tower(d, x, y, s, col):
    # skyscraper with a burst at the top
    d.rectangle([x + s * 0.34, y + s * 0.3, x + s * 0.66, y + s * 0.92],
                fill=col)
    d.polygon([(x + s * 0.5, y + s * 0.08), (x + s * 0.6, y + s * 0.26),
               (x + s * 0.5, y + s * 0.22), (x + s * 0.4, y + s * 0.26)],
              fill=col)
    for yy in (0.44, 0.58, 0.72):
        d.line([(x + s * 0.4, y + s * yy), (x + s * 0.6, y + s * yy)],
               fill=PAPER, width=3)


def icon_star(d, x, y, s, col):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.42
    pts = []
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=col)


def icon_chip(d, x, y, s, col):
    d.rectangle([x + s * 0.24, y + s * 0.24, x + s * 0.76, y + s * 0.76],
                outline=col, width=4)
    d.rectangle([x + s * 0.42, y + s * 0.42, x + s * 0.58, y + s * 0.58],
                fill=col)
    for i in range(3):
        off = s * (0.34 + 0.16 * i)
        d.line([(x + off, y + s * 0.08), (x + off, y + s * 0.24)],
               fill=col, width=3)
        d.line([(x + off, y + s * 0.76), (x + off, y + s * 0.92)],
               fill=col, width=3)
        d.line([(x + s * 0.08, y + off), (x + s * 0.24, y + off)],
               fill=col, width=3)
        d.line([(x + s * 0.76, y + off), (x + s * 0.92, y + off)],
               fill=col, width=3)


def icon_medal(d, x, y, s, col):
    cx, cy = x + s / 2, y + s * 0.58
    d.line([(x + s * 0.3, y + s * 0.08), (cx, y + s * 0.3)], fill=col, width=5)
    d.line([(x + s * 0.7, y + s * 0.08), (cx, y + s * 0.3)], fill=col, width=5)
    d.ellipse([cx - s * 0.3, cy - s * 0.3, cx + s * 0.3, cy + s * 0.3],
              outline=col, width=5)
    d.text((cx, cy), "*", font=sans_b(int(s * 0.42)), fill=col, anchor="mm")


def icon_burst(d, x, y, s, col):
    cx, cy = x + s / 2, y + s / 2
    for k in range(8):
        ang = math.radians(k * 45)
        d.line([(cx + 0.18 * s * math.cos(ang), cy + 0.18 * s * math.sin(ang)),
                (cx + 0.42 * s * math.cos(ang), cy + 0.42 * s * math.sin(ang))],
               fill=col, width=5)
    d.ellipse([cx - s * 0.14, cy - s * 0.14, cx + s * 0.14, cy + s * 0.14],
              fill=col)


ICONS = {"ship": icon_ship, "tower": icon_tower, "star": icon_star,
         "chip": icon_chip, "medal": icon_medal, "burst": icon_burst}

# ---------------------------------------------------------------- page
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# outer frame
d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
d.rectangle([20, 20, W - 21, H - 21], outline=INK, width=1)

# ---- masthead
d.text((W // 2, 44), "THE WORLD IN ONE PAGE", font=serif_b(62),
       fill=INK, anchor="ma")
d.text((W // 2, 118), "WEDNESDAY, 25 NOVEMBER 2026", font=sans_b(24),
       fill=RED, anchor="ma")
rule(d, 36, 152, W - 36, 3)
rule(d, 36, 158, W - 36, 1)

# ---- lead story: Gulf of Finland strike
LX, LW = 36, 600
y = 182
d.text((LX, y), "CONFLICT  ·  GULF OF FINLAND", font=sans_b(21), fill=RED)
y += 34
y = draw_lines(d, LX, y,
               wrap(d, "ZELENSKIY: UKRAINE HIT RUSSIAN SHIP",
                    serif_b(50), LW),
               serif_b(50), INK, 54)
y += 10
y = draw_lines(
    d, LX, y,
    wrap(d, "Kyiv says it was behind Saturday's drone strike on a Russian "
            "cargo ship.",
         serif(25), LW),
    serif(25), INK, 32)

# lead art: ship at sea under a grey sky, right side
AX, AY, AW, AH = 668, 178, 320, 268
d.rectangle([AX, AY, AX + AW, AY + AH], fill=BLUE)
d.rectangle([AX, AY, AX + AW, AY + 92], fill=(38, 92, 138))
# sun breaking through cloud
d.ellipse([AX + 216, AY + 18, AX + 268, AY + 70], fill=YELLOW)
d.ellipse([AX + 30, AY + 26, AX + 130, AY + 58], fill=(210, 222, 232))
d.ellipse([AX + 80, AY + 40, AX + 180, AY + 72], fill=(210, 222, 232))
# ship
sx, sy, ss = AX + 78, AY + 108, 164
d.polygon([(sx, sy + 44), (sx + ss, sy + 44),
           (sx + ss * 0.86, sy + 76), (sx + ss * 0.14, sy + 76)],
          fill=(232, 232, 228))
d.line([(sx + ss * 0.5, sy + 44), (sx + ss * 0.5, sy - 6)],
       fill=(232, 232, 228), width=5)
d.polygon([(sx + ss * 0.5, sy - 4), (sx + ss * 0.82, sy + 26),
           (sx + ss * 0.5, sy + 26)], fill=(255, 213, 64))
# waves
for wy in (AY + 200, AY + 214, AY + 228):
    for k in range(4):
        x0 = AX + 18 + k * 76
        d.arc([x0, wy - 8, x0 + 56, wy + 14], 200, 340,
              fill=(170, 205, 228), width=4)
d.text((AX + AW // 2, AY + AH - 38), "KYIV OWNS THE STRIKE",
       font=sans_b(22), fill=WHITE, anchor="ma")
rule(d, 36, 478, W - 36, 2)

# ---- section label
d.text((36, 492), "MORE FROM WEDNESDAY", font=sans_b(22), fill=RED)
d.text((W - 36, 492), "25 NOV 2026", font=sans_b(22), fill=GREY, anchor="ra")

STORIES = [
    ("MIDDLE EAST · RIYADH", "Houthis hit Riyadh's tallest tower",
     "11 wounded in the financial district; UK sanctions the Houthis.",
     "tower", RED),
    ("CHINA · SHANGHAI", "Beijing probes Politburo member Chen Jining",
     "Shanghai party chief under investigation, AP reports.",
     "star", GOLD),
    ("TECH · US COURT", "US jury convicts Huawei of trade-secret theft",
     "Verdict against the Chinese tech giant.",
     "chip", BLUE),
    ("USA · WASHINGTON", "Trump gives Giuliani the Medal of Freedom",
     "Highest US civilian honour for the ex-mayor.",
     "medal", GOLD),
    ("MIDDLE EAST · GAZA", "Hamas security chief killed in Gaza strike",
     "Seven killed in Israeli air strike despite ceasefire.",
     "burst", TEAL),
]

CW = (W - 72 - 16) // 2
CH, GAP = 138, 12
y0 = 524
for i, (kick, head, summ, icon, col) in enumerate(STORIES):
    row, c = divmod(i, 2)
    x = 36 + c * (CW + 16)
    y = y0 + row * (CH + GAP)
    d.rectangle([x, y, x + CW, y + CH], outline=INK, width=1)
    d.rectangle([x, y, x + 96, y + CH], fill=LIGHT)
    ICONS[icon](d, x + 12, y + 22, 72, col)
    tx = x + 112
    d.text((tx, y + 10), kick, font=sans_b(16), fill=RED)
    hy = draw_lines(d, tx, y + 32,
                    wrap(d, head, sans_b(22), CW - 128),
                    sans_b(22), INK, 27)
    draw_lines(d, tx, hy + 2,
               wrap(d, summ, sans(17), CW - 128), sans(17), GREY, 22)

# ticker box (6th cell)
x = 36 + CW + 16
y = y0 + 2 * (CH + GAP)
d.rectangle([x, y, x + CW, y + CH], fill=INK)
d.text((x + 16, y + 12), "ALSO TODAY", font=sans_b(16), fill=YELLOW)
draw_lines(d, x + 16, y + 38,
           wrap(d, "Iraq orders forces to seize Kurdish oilfields · "
                   "UN: five women killed each hour by relatives in 2025 · "
                   "Senegal gets 2025 AFCON title back · Shein pays $100M "
                   "in FTC settlement · Iran currency plunges",
                sans(17), CW - 32), sans(17), WHITE, 22)

# ---- footer
rule(d, 36, 972, W - 36, 1)
d.text((36, 982),
       "Compiled from public reporting, 25 Nov 2026: Reuters · SCMP · "
       "Associated Press · Gulf News · The Manila Times",
       font=sans(14), fill=GREY)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, format="PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
