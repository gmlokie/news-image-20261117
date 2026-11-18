#!/usr/bin/env python3
"""Render news-image-20261117: Tuesday 17 November 2026 world news front page.
1024x1024 PNG, Pillow only, flat vector-style art drawn with shapes.
All 34 headlines are supplied by the task brief (verified 17 Nov 2026 reporting).
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
PAPER = (247, 242, 230)
INK = (20, 20, 20)
RED = (180, 35, 24)
NAVY = (29, 53, 87)
GREY = (90, 90, 90)
LIGHT_BLUE = (168, 184, 200)
SEA = (46, 110, 166)
SKY = (191, 217, 232)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")

def font(path, size):
    return ImageFont.truetype(path, int(round(size)))

def fit_font(draw, text, path, start, max_w):
    size = start
    while size > 10:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, size)

def wrap(draw, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def trim_to_width(draw, text, f, max_w):
    """Trim whole words until text fits; add ellipsis if trimmed."""
    if draw.textlength(text, font=f) <= max_w:
        return text
    words = text.split()
    while len(words) > 1 and draw.textlength(" ".join(words) + " \u2026", font=f) > max_w:
        words.pop()
    return " ".join(words) + " \u2026"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- Masthead ----
d.rectangle([0, 0, W, 6], fill=RED)
f_mast = font(BOLD, 19)
d.text((W // 2, 12), "THE WORLD IN ONE IMAGE", font=f_mast, fill=NAVY, anchor="ma")
f_date = fit_font(d, "TUESDAY 17 NOVEMBER 2026", BOLD, 44, 984)
d.text((W // 2, 34), "TUESDAY 17 NOVEMBER 2026", font=f_date, fill=INK, anchor="ma")
f_sub = fit_font(d, "34 STORIES \u00b7 6 CONTINENTS \u2014 EVERY STORY HAPPENED OR WAS FIRST REPORTED TODAY", BOLD, 16, 984)
d.text((W // 2, 84), "34 STORIES \u00b7 6 CONTINENTS \u2014 EVERY STORY HAPPENED OR WAS FIRST REPORTED TODAY",
       font=f_sub, fill=RED, anchor="ma")
d.line([24, 104, 1000, 104], fill=INK, width=2)

# ---- Lead panel ----
d.rectangle([24, 112, 1000, 352], outline=INK, width=2)
# Left art: x 32..424, y 120..344
ax0, ay0, ax1, ay1 = 32, 120, 424, 344
d.rectangle([ax0, ay0, ax1, ay1], fill=SKY)
d.rectangle([ax0, ay1 - 78, ax1, ay1], fill=SEA)
# sea waves
for wx in range(ax0 + 8, ax1 - 10, 28):
    d.arc([wx, ay1 - 42, wx + 24, ay1 - 26], 180, 360, fill=(255, 255, 255), width=2)
# bridge pillars
for px in (ax0 + 28, ax0 + 150, ax0 + 300, ax1 - 36):
    d.rectangle([px, ay1 - 150, px + 12, ay1 - 78], fill=(90, 96, 104))
# bridge deck: left span, gap (collapsed), right span
d.rectangle([ax0, ay1 - 158, ax0 + 168, ay1 - 142], fill=(107, 114, 128))
d.rectangle([ax0 + 236, ay1 - 158, ax1, ay1 - 142], fill=(107, 114, 128))
# fallen span in the sea, tilted
d.polygon([(ax0 + 172, ay1 - 52), (ax0 + 232, ay1 - 58), (ax0 + 228, ay1 - 44), (ax0 + 170, ay1 - 38)],
          fill=(107, 114, 128))
# explosion at the gap (kept fully inside the art box: ay0=120)
cx, cy = ax0 + 202, ay1 - 148
d.ellipse([cx - 30, cy - 22, cx + 30, cy + 22], fill=(255, 140, 0))
d.ellipse([cx - 18, cy - 14, cx + 18, cy + 14], fill=(255, 200, 40))
d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 240, 160))
# smoke (small, above explosion, inside box)
for sx, sy, sr in [(cx - 46, cy - 30, 13), (cx - 30, cy - 40, 15), (cx - 8, cy - 42, 13),
                   (cx + 40, cy - 34, 12), (cx + 52, cy - 44, 13)]:
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 120))
d.rectangle([ax0, ay0, ax1, ay1], outline=INK, width=1)

# Right text
tx = 440
f_kick = font(BOLD, 15)
d.text((tx, 124), "LEAD \u00b7 EUROPE \u2014 WAR IN UKRAINE", font=f_kick, fill=RED)
f_head = fit_font(d, "UKRAINE HITS KERCH BRIDGE", BOLD, 40, 1000 - tx - 8)
# wrap headline to max 2 lines
lines = wrap(d, "UKRAINE HITS KERCH BRIDGE", f_head, 1000 - tx - 8)
y = 150
for ln in lines[:2]:
    d.text((tx, y), ln, font=f_head, fill=INK)
    y += int(f_head.size * 1.12)
f_leadsub = font(REG, 19)
sub_lines = wrap(d, "Road span falls into the sea in the second strike in a day \u2014 as Russian missiles hit two Kyiv bridges.",
                 f_leadsub, 1000 - tx - 8)
y += 6
for ln in sub_lines:
    d.text((tx, y), ln, font=f_leadsub, fill=INK)
    y += 24
f_quote = font(REG, 15)
q_lines = wrap(d, "Zelenskyy called it an \u201cunprecedented operation\u201d; Russia claimed only \u201cminor\u201d damage.",
               f_quote, 1000 - tx - 8)
y += 4
for ln in q_lines:
    d.text((tx, y), ln, font=f_quote, fill=GREY)
    y += 20

# ---- Medium row ----
MEDIUM = [
    ("TANKERS MINED OFF HORMUZ", "Two ships ablaze; third US carrier arrives", "tanker"),
    ("IRAN DRONES HIT US RADAR BASE", "Bahrain says attack intercepted; no casualties", "radar"),
    ("TRUMP LANDS FOR ASEAN", "Xi\u2013Trump\u2013Putin summit set for Thursday in Shenzhen", "summit"),
    ("ESTONIA TO SHUT RUSSIA BORDER", "All crossings close 1 Dec after foiled arson plot", "border"),
]
mx0, my0, gap = 24, 360, 8
mw = (1024 - 48 - 3 * gap) // 4  # 238
for i, (head, sub, kind) in enumerate(MEDIUM):
    x0 = mx0 + i * (mw + gap)
    x1 = x0 + mw
    d.rectangle([x0, my0, x1, 496], outline=INK, width=1)
    d.line([x0, my0 + 52, x1, my0 + 52], fill=GREY, width=1)
    # icon area y 364..408
    ix, iy = x0 + 8, my0 + 6
    if kind == "tanker":
        # hull + bridge tower + two flames, sea line below
        d.rectangle([ix + 10, iy + 24, ix + 150, iy + 38], fill=(40, 40, 40))
        d.rectangle([ix + 115, iy + 10, ix + 150, iy + 24], fill=(90, 90, 90))
        for fx, fy in [(ix + 30, iy + 6), (ix + 62, iy + 2)]:
            d.polygon([(fx, fy + 18), (fx + 8, fy), (fx + 16, fy + 18)], fill=(255, 140, 0))
        d.rectangle([ix + 10, iy + 42, ix + 200, iy + 45], fill=SEA)
    elif kind == "radar":
        # radar dish: arc + mast + blip, drone at right
        d.arc([ix + 14, iy + 2, ix + 66, iy + 42], 180, 360, fill=NAVY, width=3)
        d.line([ix + 40, iy + 22, ix + 40, iy + 44], fill=INK, width=2)
        d.ellipse([ix + 36, iy + 18, ix + 44, iy + 26], fill=RED)
        d.polygon([(ix + 130, iy + 12), (ix + 150, iy + 18), (ix + 130, iy + 24), (ix + 110, iy + 18)], fill=GREY)
        d.ellipse([ix + 126, iy + 14, ix + 134, iy + 22], fill=INK)
        d.line([ix + 110, iy + 18, ix + 150, iy + 18], fill=GREY, width=1)
    elif kind == "summit":
        for j, col in enumerate([(180, 35, 24), (29, 53, 87), (200, 160, 0)]):
            fx = ix + 20 + j * 48
            d.line([fx, iy + 4, fx, iy + 40], fill=INK, width=2)
            d.polygon([(fx, iy + 4), (fx + 28, iy + 12), (fx, iy + 20)], fill=col)
        d.rectangle([ix + 10, iy + 40, ix + 190, iy + 44], fill=(107, 114, 128))
    else:  # border
        d.rectangle([ix + 10, iy + 8, ix + 18, iy + 44], fill=INK)
        d.rectangle([ix + 170, iy + 8, ix + 178, iy + 44], fill=INK)
        for j in range(5):
            col = RED if j % 2 == 0 else (255, 255, 255)
            d.rectangle([ix + 18 + j * 31, iy + 12, ix + 18 + (j + 1) * 31, iy + 22], fill=col, outline=INK)
        d.rectangle([ix + 10, iy + 40, ix + 178, iy + 44], fill=GREY)
    f_mh = font(BOLD, 17)
    ml = wrap(d, head, f_mh, mw - 16)
    yy = my0 + 60
    for ln in ml[:2]:
        d.text((x0 + 8, yy), ln, font=f_mh, fill=INK)
        yy += 20
    f_ms = font(REG, 13)
    sl = wrap(d, sub, f_ms, mw - 16)
    for ln in sl[:2]:
        d.text((x0 + 8, yy), ln, font=f_ms, fill=GREY)
        yy += 17

# ---- Map strip ----
d.rectangle([24, 504, 1000, 596], outline=INK, width=1)
f_cap = font(BOLD, 13)
d.text((32, 508), "WHERE THE DAY HAPPENED", font=f_cap, fill=NAVY)
# Stylised continents (light grey-blue polygons), map area y 528..592, x 40..984
continents = [
    # North America
    [(60, 534), (150, 528), (230, 534), (240, 552), (200, 566), (150, 570), (110, 560), (70, 548)],
    # Greenland
    [(268, 530), (292, 528), (296, 540), (276, 542)],
    # South America
    [(240, 572), (280, 570), (300, 580), (288, 592), (262, 590), (244, 580)],
    # Europe (small, separated from Asia by a gap)
    [(468, 534), (508, 530), (528, 538), (516, 550), (488, 550), (470, 542)],
    # Africa
    [(478, 556), (522, 554), (542, 566), (530, 588), (500, 590), (480, 572)],
    # Asia (large, starts east of Europe)
    [(548, 530), (700, 526), (820, 532), (860, 548), (830, 566), (740, 570), (640, 568), (556, 556)],
    # SE Asia / Indonesia dots chain
    [(760, 572), (800, 570), (830, 576), (800, 582), (765, 580)],
    # Australia
    [(800, 578), (860, 576), (880, 586), (850, 592), (808, 590)],
]
for poly in continents:
    d.polygon(poly, fill=LIGHT_BLUE, outline=(120, 140, 160))
# Red dots + labels: (x, y, label, label dx, dy)
dots = [
    (500, 542, "Kerch", 8, 6),
    (600, 556, "Hormuz", 8, 6),
    (812, 562, "Manila", 8, 6),
    (520, 532, "Tallinn", 8, -14),
    (742, 548, "Shenzhen", 8, -14),
]
f_dot = font(BOLD, 11)
for x, y, label, dx, dy in dots:
    d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=RED, outline=(255, 255, 255), width=1)
    d.text((x + dx, y + dy), label, font=f_dot, fill=RED)

# ---- Story grid ----
GRID = [
    (6, "EUROPE", "Russia hits two bridges over the Dnipro in Kyiv"),
    (7, "ASIA", "Japan scrambles jets as Russian planes enter airspace"),
    (8, "EUROPE", "Five EU states plan Rwanda return hub for 2027"),
    (9, "EUROPE", "UK sanctions eight firms building West Bank settlements"),
    (10, "EUROPE", "Witkoff and Kushner to meet Kyiv allies in Berlin"),
    (11, "USA", "US intel: Iran plots 'dirty bomb' strike on Trump team"),
    (12, "MIDEAST", "Houthis hit Saudi oil pipeline with drones"),
    (13, "MIDEAST", "Iraq army moves into Kataib Hezbollah stronghold"),
    (14, "MIDEAST", "Netanyahu warns Europe over Iran missiles"),
    (15, "MIDEAST", "Settlers kill 72-year-old woman in Jericho"),
    (16, "MIDEAST", "Israeli strikes hit Lebanon\u2013Syria border area"),
    (17, "MIDEAST", "Bahrain jails 64 for life over alleged Iran links"),
    (18, "ASIA", "US tightens AI-chip licences; Brazil among five named"),
    (19, "ASIA", "Reuters: China trains AI on US rivals' models"),
    (20, "ASIA", "Mongolia's president says he will resign"),
    (21, "WORLD", "128 states meet in Geneva on killer-robot ban"),
    (22, "AFRICA", "DR Congo Ebola 'out of control'; 5,500 dead"),
    (23, "AFRICA", "Two mass shootings kill 17 in South Africa"),
    (24, "AFRICA", "Six African states eye digital-trade accord"),
    (25, "AFRICA", "Guinea arrests 1,200 in gold-mining crackdown"),
    (26, "AFRICA", "WHO: Eritrea eliminates trachoma"),
    (27, "USA", "JPMorgan blames software bug for Monday outage"),
    (28, "USA", "Nvidia reports after bell; Wall St slides on AI fears"),
    (29, "USA", "Microsoft explains last week's global outage"),
    (30, "USA", "House Democrats unveil agenda; DC faces $4bn gap"),
    (31, "OCEANIA", "Australia sanctions over West Bank settlements"),
    (32, "OCEANIA", "PNG PM tells Xi: closing Taiwan office 'wasn't easy'"),
    (33, "WORLD", "COP31 talks tense over draft climate deal"),
    (34, "WORLD", "US-led AI security pact signed, incl. India, UAE"),
]
f_num = font(BOLD, 13)
f_reg = font(BOLD, 13)
f_headline = font(REG, 13)
left = GRID[:15]
right = GRID[15:]
d.line([508, 604, 508, 996], fill=(200, 190, 170), width=1)
for col_idx, col_items in enumerate((left, right)):
    cx0 = 24 if col_idx == 0 else 520
    col_w = 476
    for r, (n, region, headline) in enumerate(col_items):
        y = 606 + r * 26
        num_txt = f"{n:02d} \u00b7 "
        reg_txt = region + " \u2014 "
        w_num = d.textlength(num_txt, font=f_num)
        w_reg = d.textlength(reg_txt, font=f_reg)
        avail = col_w - w_num - w_reg
        head_txt = trim_to_width(d, headline, f_headline, avail)
        x = cx0
        d.text((x, y), num_txt, font=f_num, fill=RED)
        x += w_num
        d.text((x, y), reg_txt, font=f_reg, fill=NAVY)
        x += w_reg
        d.text((x, y), head_txt, font=f_headline, fill=INK)

# ---- Footer ----
d.line([24, 1000, 1000, 1000], fill=INK, width=1)
f_foot = font(REG, 13)
d.text((W // 2, 1004), "All 34 stories happened or were first reported on Tuesday 17 November 2026.",
       font=f_foot, fill=GREY, anchor="ma")

img.save("entry.png", format="PNG", optimize=True)
print("saved entry.png", img.size)
