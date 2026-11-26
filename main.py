#!/usr/bin/env python3
"""ALT renderer — MODE set per candidate. Same verified slate as DAYWATCH v2."""
import os, sys, tempfile, zipfile, math
HERE = os.path.dirname(os.path.abspath(__file__))
MODE = "A"  # A | B | C

def _load_pillow():
    if os.environ.get("ALT_SKIP_VENDOR"): return
    vdir = os.path.join(HERE, "vendor")
    for name in sorted(os.listdir(vdir)):
        if name.endswith(".whl"):
            dest = os.path.join(tempfile.mkdtemp(prefix="pil-"), "x")
            with zipfile.ZipFile(os.path.join(vdir, name)) as zf:
                zf.extractall(dest)
            sys.path.insert(0, dest)
            return
    raise RuntimeError("vendored Pillow wheel not found")
_load_pillow()
sys.path.insert(0, HERE)
from PIL import Image, ImageDraw, ImageFont, ImageOps
from slate import HEROES, MIDS, ALSO, REGION_COUNTS, RAIL, DATE_CHECK, PINS

W = 1024; MARGIN = 22; CW = W - 2 * MARGIN
PAPER = (243, 236, 220); INK = (16, 24, 46); NAVY = (20, 33, 61)
GOLD = (197, 142, 32); AMBER = (232, 163, 61); CRIMSON = (179, 58, 43)
RED = (200, 32, 26); YELLOW = (245, 197, 49); BLACK = (18, 18, 18)
TEAL = (10, 118, 110); GREY = (96, 100, 108); LIGHT = (224, 216, 198)
WHITE = (255, 255, 255); GREEN = (30, 110, 60); BLUE = (23, 64, 178)
BASE = HERE; FD = os.path.join(BASE, "fonts")
ART = {"kyiv": "art/hero-kyiv.webp", "storm": "art/hero-storm.webp", "summit": "art/hero-summit.webp"}
MID_ART = {n: f"art/mid-{n:02d}.webp" for n in range(4, 16)}
_cache = {}
def F(name, size):
    key = (name, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(os.path.join(FD, name), size, layout_engine=ImageFont.Layout.BASIC)
    return _cache[key]
def arch(size, w=800): return F({700: "Archivo-700.ttf", 800: "Archivo-800.ttf", 900: "Archivo-900.ttf"}[w], size)
def inter(size, w=400): return F({400: "Inter-400.ttf", 500: "Inter-500.ttf", 600: "Inter-600.ttf", 700: "Inter-700.ttf"}[w], size)
def serif(size): return F("NotoSerifDisplay-Bold.ttf", size)
def serifb(size): return F("NotoSerif-Bold.ttf", size)
def tw(d, s, f):
    b = d.textbbox((0, 0), s, font=f); return b[2] - b[0]
def wrap(d, s, f, width):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if tw(d, t, f) <= width or not cur: cur = t
        else: lines.append(cur); cur = wd
    if cur: lines.append(cur)
    return lines
CHIP_COL = {"CONFIRMED": GREEN, "REPORTED": BLUE, "OFFICIAL": (90, 60, 150), "CLAIM": CRIMSON}
REGION_TICK = {"ASIA": BLUE, "EUROPE": GREEN, "MIDDLE EAST": (178, 84, 30), "AMERICAS": (110, 52, 160), "OCEANIA": TEAL, "AFRICA": GOLD, "GLOBAL": GREY}
def chip(d, x, y, label, color, size=11):
    f = arch(size, 800); wdt = tw(d, label, f) + 14
    d.rectangle([x, y, x + wdt, y + size + 5], fill=color)
    d.text((x + 7, y + 2), label, font=f, fill=WHITE)
    return wdt
def flag(img, x, y, code, w=24, h=16):
    f = Image.new("RGB", (w, h), PAPER); fd = ImageDraw.Draw(f)
    def H(stripes):
        yy = 0.0
        for i, (col, fr) in enumerate(stripes):
            y2 = h if i == len(stripes) - 1 else yy + fr * h
            fd.rectangle([0, int(yy), w, int(y2)], fill=col); yy = y2
    def disc(cx, cy, r, col): fd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    if code == "UA": H([((0, 87, 183), .5), ((255, 215, 0), .5)])
    elif code == "RU": H([((255, 255, 255), 1/3), ((0, 57, 166), 1/3), ((213, 0, 50), 1/3)])
    elif code == "LT": H([((253, 185, 19), 1/3), ((0, 106, 68), 1/3), ((198, 47, 44), 1/3)])
    elif code == "MM":
        H([((254, 203, 0), 1/3), ((52, 178, 51), 1/3), ((234, 40, 57), 1/3)]); disc(w/2, h/2, 3, (255, 255, 255))
    elif code == "PS":
        H([((0, 0, 0), 1/3), ((255, 255, 255), 1/3), ((0, 122, 61), 1/3)]); fd.polygon([(0, 0), (9, h / 2), (0, h)], fill=(206, 17, 38))
    elif code == "AU":
        fd.rectangle([0, 0, w, h], fill=(0, 43, 127)); fd.rectangle([0, 0, 11, 8], fill=(1, 33, 105))
        fd.rectangle([4, 0, 6, 8], fill=(255, 255, 255)); fd.rectangle([0, 3, 11, 5], fill=(255, 255, 255))
        fd.rectangle([5, 0, 6, 8], fill=(200, 16, 46)); fd.rectangle([0, 3, 11, 4], fill=(200, 16, 46))
        for sx, sy in [(18, 4), (21, 9), (17, 13)]: disc(sx, sy, 1, (255, 255, 255))
    elif code == "US":
        for i in range(7): fd.rectangle([0, i * h / 7, w, (i + 1) * h / 7], fill=(179, 34, 52) if i % 2 == 0 else (255, 255, 255))
        fd.rectangle([0, 0, 11, h * 4 / 7], fill=(10, 49, 97))
    elif code == "EU":
        fd.rectangle([0, 0, w, h], fill=(0, 51, 153))
        for k in range(6): disc(w/2 + 6 * math.cos(k * 1.047), h/2 + 6 * math.sin(k * 1.047), 1, (255, 204, 0))
    elif code == "IT":
        fd.rectangle([0, 0, 8, h], fill=(0, 140, 69)); fd.rectangle([16, 0, w, h], fill=(205, 33, 58))
    else:
        fd.ellipse([4, 1, w - 4, h - 1], outline=BLUE, width=1); fd.ellipse([w/2 - 4, 1, w/2 + 4, h - 1], outline=BLUE, width=1); fd.line([4, h/2, w - 4, h/2], fill=BLUE)
    img.paste(f, (x, y)); ImageDraw.Draw(img).rectangle([x, y, x + w - 1, y + h - 1], outline=(130, 126, 116))
def cover(img, w, h, focal=(0.5, 0.45)):
    sw, sh = img.size; scale = max(w / sw, h / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    r = img.resize((nw, nh), Image.LANCZOS); fx, fy = focal
    x0 = min(max(int(fx * nw - w / 2), 0), nw - w); y0 = min(max(int(fy * nh - h / 2), 0), nh - h)
    return r.crop((x0, y0, x0 + w, y0 + h))
def halftone(img, w, h):
    g = ImageOps.grayscale(cover(img, w, h)).point(lambda v: 0 if v < 70 else (110 if v < 140 else (190 if v < 200 else 255)))
    pal = {0: BLACK, 110: RED, 190: YELLOW, 255: (250, 244, 224)}
    out = Image.new("RGB", (w, h))
    px_g = g.load(); px_o = out.load()
    for yy in range(h):
        for xx in range(w): px_o[xx, yy] = pal[px_g[xx, yy]]
    dd = ImageDraw.Draw(out)
    for yy in range(0, h, 5):
        for xx in range(0, w, 5):
            if px_g[xx, yy] == 110: dd.ellipse([xx, yy, xx + 2, yy + 2], fill=BLACK)
    return out
LAND = [
"                                                  ",
"    oooooooo           ooo ooooooooooooooooooo    ",
"  oooooooooooo       oooooooooooooooooooooooooo   ",
"  ooooooooooo         oooooooooooooooooooooooo    ",
"   ooooooooo           ooooo oooooooooooooooo     ",
"    ooooooo             ooo   oooooooooooooo      ",
"     ooooo              ooooo  ooooooooooo        ",
"      oooo             ooooooo   oooooooo         ",
"      ooo              oooooooo   ooooo           ",
"     oooo               oooooo     ooo  o  o      ",
"     ooooo               oooo      oo  oooo       ",
"      oooo               ooo            ooooo     ",
"      oooo               oo             oooo      ",
"       ooo                                        ",
"       oo                                         ",
"                                                  ",
"                                                  ",
"                                                  ",
]
def draw_map(d, img, x, y, w, h, title_col):
    d.rectangle([x, y, x + w, y + h], fill=INK)
    d.text((x + 10, y + 5), "WHERE IT HAPPENED — PINS = STORY NUMBERS", font=arch(11, 900), fill=title_col)
    for r in range(len(LAND)):
        line = LAND[r].ljust(50)
        for c in range(50):
            if line[c] == "o":
                d.ellipse([x + 10 + c * (w - 20) / 50, y + 24 + r * (h - 30) / 18, x + 12.5 + c * (w - 20) / 50, y + 26.5 + r * (h - 30) / 18], fill=(158, 172, 200))
    for n, (fx, fy) in PINS.items():
        px, py = x + 10 + fx * (w - 20), y + 22 + fy * (h - 28)
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=AMBER)
        s = str(n); d.text((px - tw(d, s, arch(7, 900)) / 2, py - 3), s, font=arch(7, 900), fill=INK)
def draw_datecheck(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 233, 220), outline=INK, width=1)
    d.rectangle([x, y, x + 6, y + h], fill=CRIMSON)
    d.text((x + 13, y + 4), "DATE CHECK — NOT THURSDAY, NOT PRINTED AS ITS NEWS:", font=arch(11, 900), fill=CRIMSON)
    ty = y + 20
    for s, dd in DATE_CHECK:
        lines = wrap(d, f"· {s} ({dd})", inter(10, 500), w - 24)
        if len(lines) > 2: raise SystemExit(f"date check wraps: {s}")
        for l2 in lines:
            d.text((x + 13, ty), l2, font=inter(10, 500), fill=(52, 56, 64)); ty += 12
def draw_also(d, img, ax, y, aw, title):
    d.rectangle([ax, y, ax + aw, y + 19], fill=INK)
    d.text((ax + 9, y + 3), title, font=arch(12, 900), fill=WHITE)
    acolw = (aw - 10) // 2
    for i, (n, region, code, text) in enumerate(ALSO):
        cx = ax + (i % 2) * (acolw + 10); cy = y + 23 + (i // 2) * 18
        if i // 2 == 10: cx = ax; cy = y + 23 + 10 * 18
        flag(img, cx, cy, code)
        d.text((cx + 29, cy + 2), f"{n:02d}", font=arch(12, 900), fill=BLUE)
        lines = wrap(d, text, inter(10, 500), acolw - 60)
        if len(lines) > 1: raise SystemExit(f"also {n} wraps")
        d.text((cx + 58, cy + 3), lines[0], font=inter(10, 500), fill=(40, 44, 52))
    ly = y + 23 + 11 * 18 + 1; lx = ax
    d.text((lx, ly), "HOW SURE:", font=arch(10, 900), fill=INK); lx += tw(d, "HOW SURE:", arch(10, 900)) + 6
    for label, col, note in [("CONFIRMED", GREEN, "wire-verified"), ("OFFICIAL", (90, 60, 150), "statement"), ("REPORTED", BLUE, "attributed"), ("CLAIM", CRIMSON, "one side")]:
        lx += chip(d, lx, ly - 2, label, col, size=9) + 5
        d.text((lx, ly), note, font=inter(9, 400), fill=GREY); lx += tw(d, note, inter(9, 400)) + 7
    return ly + 18
def footer(d, y, name):
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=1)
    d.text((MARGIN, y + 3), "Sources: Reuters · AP · ONS · KCNA · dpa · FOX Weather · NPR · TradingView — wires read to 15:20 UTC, Thu 26 Nov 2026. Scenes are drawn illustrations, not photographs.", font=inter(9, 400), fill=GREY)
    d.text((MARGIN, y + 14), f"{name} · DRAWN BY AN AI AGENT FOR MAKE.FUN · EVERY STORY HAPPENED, OR WAS FIRST REPORTED, ON THURSDAY 26 NOVEMBER 2026 IN SOME TIME ZONE", font=arch(9, 800), fill=INK)

HEAVY = {4, 5, 6, 9, 10, 14, 15}  # conflict / disaster mids -> woodcut in D

def hero_block(img, d, y, art_h, head_f, head_lh, art_fn):
    pw = (CW - 16) // 3
    for i, hero in enumerate(HEROES):
        x = MARGIN + i * (pw + 8)
        art = Image.open(os.path.join(BASE, ART[hero["scene"]])).convert("RGB")
        img.paste(art_fn(art, pw, art_h), (x, y))
        d.rectangle([x, y, x + pw, y + 20], fill=REGION_TICK[hero["region"]])
        d.text((x + 8, y + 3), f"{hero['n']:02d} · {hero['region']} · {hero['field']}", font=arch(11, 800), fill=WHITE)
        cw_ = tw(d, hero["chip"], arch(10, 800)) + 12
        d.rectangle([x + pw - cw_ - 4, y + 2, x + pw - 4, y + 18], fill=CHIP_COL[hero["chip"]])
        d.text((x + pw - cw_ + 2, y + 4), hero["chip"], font=arch(10, 800), fill=WHITE)
        by = y + art_h - 20
        bf = arch(12, 900); bw_ = tw(d, hero["banner"], bf) + 14
        if bw_ > pw - 8: raise SystemExit(f"hero {hero['n']}: banner too wide")
        d.rectangle([x + 4, by, x + 4 + bw_, by + 18], fill=CRIMSON)
        d.text((x + 11, by + 3), hero["banner"], font=bf, fill=WHITE)
        ty = y + art_h + 6
        head_lines = wrap(d, hero["head"], head_f, pw - 4)
        if len(head_lines) > 3: raise SystemExit(f"hero {hero['n']}: headline {len(head_lines)} lines")
        for ln in head_lines:
            d.text((x, ty), ln, font=head_f, fill=INK); ty += head_lh
        deck_lines = wrap(d, hero["deck"], inter(11, 400), pw - 4)
        if len(deck_lines) > 2: raise SystemExit(f"hero {hero['n']}: deck {len(deck_lines)} lines")
        for ln in deck_lines:
            d.text((x, ty + 1), ln, font=inter(11, 400), fill=(70, 74, 82)); ty += 12
        d.rectangle([x, y, x + pw, y + art_h], outline=INK, width=2)
    return y + art_h + 6 + 3 * head_lh + 26

def mid_plate_A(img, d, y, rowh, plate_h):
    colw = (CW - 16) // 3
    for i, m in enumerate(MIDS):
        cx = MARGIN + (i % 3) * (colw + 8); cy = y + (i // 3) * rowh
        d.text((cx, cy), f"{m['n']:02d}", font=arch(14, 900), fill=BLUE)
        d.text((cx + 40, cy + 2), f"{m['region']} · {m['field']} · {m['part']}", font=arch(9, 800), fill=GREY)
        cf = arch(9, 800); chw = tw(d, m["chip"], cf) + 11
        d.rectangle([cx + colw - chw, cy, cx + colw, cy + 14], fill=CHIP_COL[m["chip"]])
        d.text((cx + colw - chw + 6, cy + 2), m["chip"], font=cf, fill=WHITE)
        art = Image.open(os.path.join(BASE, MID_ART[m["n"]])).convert("RGB")
        img.paste(cover(art, colw, plate_h), (cx, cy + 16))
        d.rectangle([cx, cy + 16, cx + colw, cy + 16 + plate_h], outline=INK, width=1)
        ty = cy + 20 + plate_h
        head_lines = wrap(d, m["head"], arch(12, 800), colw - 2)
        if len(head_lines) > 2: raise SystemExit(f"mid {m['n']}: headline {len(head_lines)} lines (A)")
        for ln in head_lines:
            d.text((cx, ty), ln, font=arch(12, 800), fill=INK); ty += 14
        fy = cy + rowh - 14
        d.text((cx, fy), m["fig"], font=arch(12, 900), fill=CRIMSON)
        figw = tw(d, m["fig"], arch(12, 900))
        dl = wrap(d, m["deck"], inter(9, 400), colw - 16 - figw)
        if len(dl) > 1: raise SystemExit(f"mid {m['n']}: deck wraps (A)")
        d.text((cx + 10 + figw, fy + 1), dl[0], font=inter(9, 400), fill=(70, 74, 82))
        d.line([cx, cy + rowh - 3, cx + colw, cy + rowh - 3], fill=LIGHT)

def build_A():
    img = Image.new("RGB", (W, W), PAPER); d = ImageDraw.Draw(img)
    y = 12
    d.text((MARGIN, y), "THE CONTINENTAL", font=serif(32), fill=INK)
    d.text((MARGIN + 330, y + 16), "ALL THE DAY, ON ONE SHEET", font=arch(11, 800), fill=GREY)
    slab_x = W - MARGIN - 150
    d.rectangle([slab_x, y, W - MARGIN, y + 40], fill=NAVY)
    d.text((slab_x + 12, y + 4), "DAY 330 OF 2026", font=arch(12, 900), fill=AMBER)
    d.text((slab_x + 12, y + 21), "36 STORIES", font=arch(12, 900), fill=WHITE)
    y += 42
    d.text((MARGIN, y), "Thursday 26 November 2026", font=serif(38), fill=CRIMSON)
    y += 44
    d.text((MARGIN, y), REGION_COUNTS, font=arch(13, 900), fill=INK)
    d.line([MARGIN, y + 17, W - MARGIN, y + 17], fill=GOLD, width=3)
    y += 21
    d.rectangle([MARGIN, y, W - MARGIN, y + 34], fill=NAVY)
    rw = CW // 6
    for i, (fig, cap) in enumerate(RAIL):
        rx = MARGIN + i * rw + 10
        d.text((rx, y + 2), fig, font=arch(17, 900), fill=AMBER)
        for j, ln in enumerate(wrap(d, cap, arch(7, 700), rw - 16)[:2]):
            d.text((rx, y + 21 + j * 8), ln, font=arch(7, 700), fill=(178, 186, 205))
        if i: d.line([MARGIN + i * rw, y + 4, MARGIN + i * rw, y + 30], fill=(52, 58, 74), width=1)
    y += 37
    y = hero_block(img, d, y, 88, serif(15), 17, lambda a, w, h: cover(a, w, h))
    d.text((MARGIN, y), "THE DAY IN FULL", font=serif(16), fill=INK)
    d.line([MARGIN + 150, y + 9, W - MARGIN, y + 9], fill=INK, width=2)
    y += 20
    mid_plate_A(img, d, y, 96, 34)
    y += 4 * 96 + 2
    bot = y
    draw_map(d, img, MARGIN, bot, 452, 112, AMBER)
    draw_datecheck(d, MARGIN, bot + 122, 452, 88)
    end = draw_also(d, img, MARGIN + 466, bot, CW - 466, "ALSO THURSDAY — 21 MORE, FLAGGED")
    footer(d, max(bot + 216, end) + 2, "THE CONTINENTAL")
    return img

def data_hero(d, x, y, pw, ph, hero):
    d.rectangle([x, y, x + pw, y + ph], fill=NAVY)
    d.text((x + 10, y + 6), f"{hero['n']:02d} · {hero['region']} · {hero['field']}", font=arch(11, 800), fill=AMBER)
    cw_ = tw(d, hero["chip"], arch(10, 800)) + 12
    d.rectangle([x + pw - cw_ - 4, y + 3, x + pw - 4, y + 19], fill=CHIP_COL[hero["chip"]])
    d.text((x + pw - cw_ + 2, y + 5), hero["chip"], font=arch(10, 800), fill=WHITE)
    gy = y + 30; gw = pw - 20
    if hero["n"] == 1:
        d.text((x + 10, gy), "DRONES LAUNCHED 113", font=arch(10, 800), fill=WHITE)
        d.rectangle([x + 10, gy + 14, x + 10 + gw, gy + 26], fill=CRIMSON)
        d.text((x + 10, gy + 30), "DOWNED OR JAMMED 87", font=arch(10, 800), fill=WHITE)
        d.rectangle([x + 10, gy + 44, x + 10 + int(gw * 87 / 113), gy + 56], fill=TEAL)
        d.text((x + 10, gy + 62), "7 WOUNDED IN KYIV · MISSILES AS WELL AS DRONES", font=arch(9, 800), fill=AMBER)
    elif hero["n"] == 2:
        d.text((x + 10, gy), "81.5M TRAVELLERS (AAA)", font=arch(10, 800), fill=WHITE)
        d.rectangle([x + 10, gy + 14, x + 10 + gw, gy + 26], fill=TEAL)
        d.text((x + 10, gy + 30), "GUSTS 65 MPH · 400,000+ HOMES DARK", font=arch(10, 800), fill=WHITE)
        d.rectangle([x + 10, gy + 44, x + 10 + int(gw * 0.65), gy + 56], fill=AMBER)
        d.text((x + 10, gy + 62), "MACY'S PARADE: FIRST POSTPONEMENT IN 100 YEARS", font=arch(9, 800), fill=AMBER)
    else:
        d.text((x + 10, gy), "BUDGET 2028–34: €1.582TN", font=arch(10, 800), fill=WHITE)
        d.rectangle([x + 10, gy + 14, x + 10 + gw, gy + 26], fill=GOLD)
        d.text((x + 10, gy + 30), "UKRAINE LOAN FOUGHT OVER: €45BN", font=arch(10, 800), fill=WHITE)
        d.rectangle([x + 10, gy + 44, x + 10 + max(14, int(gw * 45 / 1582 * 6)), gy + 56], fill=CRIMSON)
        d.text((x + 10, gy + 62), "€100BN FOR UKRAINE INSIDE THE BUDGET", font=arch(9, 800), fill=AMBER)

def build_B():
    img = Image.new("RGB", (W, W), PAPER); d = ImageDraw.Draw(img)
    y = 12
    d.text((MARGIN, y), "THE LEDGER", font=serif(32), fill=INK)
    d.text((MARGIN + 218, y + 16), "THE DAY IN FIGURES — EVERY STORY, MEASURED", font=arch(11, 800), fill=GREY)
    slab_x = W - MARGIN - 150
    d.rectangle([slab_x, y, W - MARGIN, y + 40], fill=INK)
    d.text((slab_x + 12, y + 4), "DAY 330 OF 2026", font=arch(12, 900), fill=AMBER)
    d.text((slab_x + 12, y + 21), "36 STORIES", font=arch(12, 900), fill=WHITE)
    y += 42
    d.text((MARGIN, y), "Thursday 26 November 2026", font=serif(38), fill=INK)
    y += 44
    d.text((MARGIN, y), REGION_COUNTS, font=arch(13, 900), fill=INK)
    d.line([MARGIN, y + 17, W - MARGIN, y + 17], fill=INK, width=3)
    y += 21
    pw = (CW - 16) // 3; ph = 108
    for i, hero in enumerate(HEROES):
        x = MARGIN + i * (pw + 8)
        data_hero(d, x, y, pw, ph, hero)
        ty = y + ph + 6
        head_lines = wrap(d, hero["head"], arch(15, 900), pw - 4)
        if len(head_lines) > 3: raise SystemExit(f"B hero {hero['n']} headline")
        for ln in head_lines:
            d.text((x, ty), ln, font=arch(15, 900), fill=INK); ty += 17
        deck_lines = wrap(d, hero["deck"], inter(11, 400), pw - 4)
        if len(deck_lines) > 2: raise SystemExit(f"B hero {hero['n']} deck")
        for ln in deck_lines:
            d.text((x, ty + 1), ln, font=inter(11, 400), fill=(70, 74, 82)); ty += 12
    y += ph + 6 + 51 + 26
    d.text((MARGIN, y), "THE DAY IN FULL — EACH STORY WITH ITS FIGURE", font=arch(13, 900), fill=INK)
    d.line([MARGIN + 380, y + 7, W - MARGIN, y + 7], fill=INK, width=2)
    y += 16
    colw = (CW - 16) // 3; rowh = 92
    for i, m in enumerate(MIDS):
        cx = MARGIN + (i % 3) * (colw + 8); cy = y + (i // 3) * rowh
        d.rectangle([cx, cy, cx + 54, cy + 84], fill=NAVY)
        hs = [0.35 + ((m["n"] * (k + 3)) % 10) / 16.0 for k in range(4)]
        for k, hh in enumerate(hs):
            bx = cx + 7 + k * 11; bh = int(30 * hh)
            d.rectangle([bx, cy + 44 - bh, bx + 7, cy + 44], fill=AMBER if k == 3 else (120, 140, 180))
        d.text((cx + 5, cy + 50), "FIG.", font=arch(8, 800), fill=(178, 186, 205))
        d.text((cx + 5, cy + 62), f"Nº{m['n']}", font=arch(11, 900), fill=WHITE)
        tx = cx + 62
        d.text((tx, cy), f"{m['region']} · {m['field']}", font=arch(9, 800), fill=GREY)
        cf = arch(9, 800); chw = tw(d, m["chip"], cf) + 11
        d.rectangle([cx + colw - chw, cy, cx + colw, cy + 14], fill=CHIP_COL[m["chip"]])
        d.text((cx + colw - chw + 6, cy + 2), m["chip"], font=cf, fill=WHITE)
        head_lines = wrap(d, m["head"], arch(12, 800), colw - 66)
        if len(head_lines) > 3: raise SystemExit(f"B mid {m['n']} headline {len(head_lines)}")
        for j, ln in enumerate(head_lines):
            d.text((tx, cy + 15 + j * 14), ln, font=arch(12, 800), fill=INK)
        fy = cy + 60
        d.text((tx, fy), m["fig"], font=arch(12, 900), fill=CRIMSON)
        figw = tw(d, m["fig"], arch(12, 900))
        dl = wrap(d, m["deck"], inter(9, 400), colw - 66 - figw - 8)
        if len(dl) > 2: raise SystemExit(f"B mid {m['n']} deck")
        for j, ln in enumerate(dl):
            d.text((tx + 8 + figw, fy + 1 + j * 11), ln, font=inter(9, 400), fill=(70, 74, 82))
        d.line([cx, cy + rowh - 3, cx + colw, cy + rowh - 3], fill=LIGHT)
    y += 4 * rowh + 2
    bot = y
    end = draw_also(d, img, MARGIN, bot, 540, "ALSO THURSDAY — 21 MORE, FLAGGED")
    mx = MARGIN + 554; mw = CW - 554
    draw_map(d, img, mx, bot, mw, 112, AMBER)
    draw_datecheck(d, mx, bot + 122, mw, 88)
    footer(d, max(bot + 216, end) + 2, "THE LEDGER")
    return img

def build_C():
    img = Image.new("RGB", (W, W), (250, 244, 224)); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 66], fill=RED)
    d.text((MARGIN, 8), "DAYBREAK", font=arch(38, 900), fill=BLACK)
    d.text((MARGIN + 238, 26), "THURSDAY 26 NOVEMBER 2026", font=arch(17, 900), fill=(250, 244, 224))
    d.rectangle([W - MARGIN - 150, 10, W - MARGIN, 56], fill=BLACK)
    d.text((W - MARGIN - 138, 15), "DAY 330 · 2026", font=arch(12, 900), fill=YELLOW)
    d.text((W - MARGIN - 138, 32), "36 STORIES", font=arch(12, 900), fill=WHITE)
    y = 74
    d.text((MARGIN, y), REGION_COUNTS, font=arch(13, 900), fill=BLACK)
    y += 20
    d.rectangle([MARGIN, y, W - MARGIN, y + 34], fill=BLACK)
    rw = CW // 6
    for i, (fig, cap) in enumerate(RAIL):
        rx = MARGIN + i * rw + 10
        d.text((rx, y + 2), fig, font=arch(17, 900), fill=YELLOW)
        for j, ln in enumerate(wrap(d, cap, arch(7, 700), rw - 16)[:2]):
            d.text((rx, y + 21 + j * 8), ln, font=arch(7, 700), fill=(200, 200, 200))
        if i: d.line([MARGIN + i * rw, y + 4, MARGIN + i * rw, y + 30], fill=(70, 70, 70), width=1)
    y += 37
    y = hero_block(img, d, y, 84, arch(15, 900), 17, lambda a, w, h: halftone(a, w, h))
    d.rectangle([MARGIN, y, W - MARGIN, y + 18], fill=BLACK)
    d.text((MARGIN + 8, y + 3), "THE DAY IN FULL", font=arch(12, 900), fill=YELLOW)
    y += 22
    colw = (CW - 16) // 3; rowh = 94; plate_w, plate_h = 92, 46
    for i, m in enumerate(MIDS):
        cx = MARGIN + (i % 3) * (colw + 8); cy = y + (i // 3) * rowh
        d.rectangle([cx, cy + 1, cx + 4, cy + 88], fill=RED)
        d.text((cx + 9, cy), f"{m['n']:02d}", font=arch(15, 900), fill=BLUE)
        d.text((cx + 44, cy + 3), f"{m['region']} · {m['field']} · {m['part']}", font=arch(10, 800), fill=GREY)
        cf = arch(9, 800); chw = tw(d, m["chip"], cf) + 11
        d.rectangle([cx + colw - chw, cy, cx + colw, cy + 14], fill=CHIP_COL[m["chip"]])
        d.text((cx + colw - chw + 6, cy + 2), m["chip"], font=cf, fill=WHITE)
        art = Image.open(os.path.join(BASE, MID_ART[m["n"]])).convert("RGB")
        img.paste(halftone(art, plate_w, plate_h), (cx + colw - plate_w, cy + 16))
        d.rectangle([cx + colw - plate_w, cy + 16, cx + colw, cy + 16 + plate_h], outline=BLACK, width=2)
        head_lines = wrap(d, m["head"], arch(13, 800), colw - plate_w - 20)
        if len(head_lines) > 3: raise SystemExit(f"C mid {m['n']} headline")
        for j, ln in enumerate(head_lines):
            d.text((cx + 9, cy + 16 + j * 15), ln, font=arch(13, 800), fill=BLACK)
        fy = cy + 64
        d.text((cx + 9, fy), m["fig"], font=arch(13, 900), fill=RED)
        figw = tw(d, m["fig"], arch(13, 900))
        dl = wrap(d, m["deck"], inter(10, 400), colw - 22 - figw)
        if len(dl) > 2: raise SystemExit(f"C mid {m['n']} deck")
        for j, ln in enumerate(dl):
            d.text((cx + 13 + figw, fy + 2 + j * 12), ln, font=inter(10, 400), fill=(70, 74, 82))
        d.line([cx, cy + rowh - 3, cx + colw, cy + rowh - 3], fill=(220, 205, 170))
    y += 4 * rowh + 2
    bot = y
    draw_map(d, img, MARGIN, bot, 452, 112, YELLOW)
    draw_datecheck(d, MARGIN, bot + 122, 452, 88)
    end = draw_also(d, img, MARGIN + 466, bot, CW - 466, "ALSO THURSDAY — 21 MORE, FLAGGED")
    footer(d, max(bot + 216, end) + 2, "DAYBREAK")
    return img

def build_D():
    img = Image.new("RGB", (W, W), PAPER); d = ImageDraw.Draw(img)
    y = 12
    d.text((MARGIN, y), "THE CROSSWIRE", font=serif(32), fill=INK)
    d.text((MARGIN + 262, y + 16), "ONE DAY · TWO INKS · EACH WITH ITS MEANING", font=arch(11, 800), fill=GREY)
    slab_x = W - MARGIN - 150
    d.rectangle([slab_x, y, W - MARGIN, y + 40], fill=NAVY)
    d.text((slab_x + 12, y + 4), "DAY 330 OF 2026", font=arch(12, 900), fill=AMBER)
    d.text((slab_x + 12, y + 21), "36 STORIES", font=arch(12, 900), fill=WHITE)
    y += 42
    d.text((MARGIN, y), "Thursday 26 November 2026", font=serif(38), fill=CRIMSON)
    y += 44
    d.text((MARGIN, y), REGION_COUNTS, font=arch(13, 900), fill=INK)
    d.line([MARGIN, y + 17, W - MARGIN, y + 17], fill=GOLD, width=3)
    y += 21
    # HOW TO READ legend: the style split is the coding axis
    d.rectangle([MARGIN, y, W - MARGIN, y + 22], fill=(238, 233, 220), outline=INK, width=1)
    d.rectangle([MARGIN, y, MARGIN + 26, y + 22], fill=CRIMSON)
    lx = MARGIN + 34
    d.text((lx, y + 5), "HOW TO READ:", font=arch(11, 900), fill=INK); lx += tw(d, "HOW TO READ:", arch(11, 900)) + 8
    d.rectangle([lx, y + 5, lx + 16, y + 17], fill=CRIMSON); lx += 22
    t1 = "WOODCUT PLATES = WAR, DISASTER, LOSS — THE DAY'S WEIGHT"
    d.text((lx, y + 5), t1, font=arch(11, 800), fill=INK); lx += tw(d, t1, arch(11, 800)) + 14
    d.rectangle([lx, y + 5, lx + 16, y + 17], fill=NAVY); lx += 22
    d.text((lx, y + 5), "FLAT PLATES = MARKETS, TALKS, THE DAY'S BUSINESS", font=arch(11, 800), fill=INK)
    y += 25
    # heroes: woodcut (all three carry weight: strike, storm, summit fight)
    pw = (CW - 16) // 3; art_h = 84
    for i, hero in enumerate(HEROES):
        x = MARGIN + i * (pw + 8)
        art = Image.open(os.path.join(BASE, f"art/wood-hero-{hero['scene']}.webp")).convert("RGB")
        img.paste(cover(art, pw, art_h), (x, y))
        d.rectangle([x, y, x + pw, y + 20], fill=REGION_TICK[hero["region"]])
        d.text((x + 8, y + 3), f"{hero['n']:02d} · {hero['region']} · {hero['field']}", font=arch(11, 800), fill=WHITE)
        cw_ = tw(d, hero["chip"], arch(10, 800)) + 12
        d.rectangle([x + pw - cw_ - 4, y + 2, x + pw - 4, y + 18], fill=CHIP_COL[hero["chip"]])
        d.text((x + pw - cw_ + 2, y + 4), hero["chip"], font=arch(10, 800), fill=WHITE)
        by = y + art_h - 20
        bf = arch(12, 900); bw_ = tw(d, hero["banner"], bf) + 14
        if bw_ > pw - 8: raise SystemExit(f"D hero {hero['n']} banner")
        d.rectangle([x + 4, by, x + 4 + bw_, by + 18], fill=CRIMSON)
        d.text((x + 11, by + 3), hero["banner"], font=bf, fill=WHITE)
        ty = y + art_h + 6
        head_lines = wrap(d, hero["head"], serif(15), pw - 4)
        if len(head_lines) > 3: raise SystemExit(f"D hero {hero['n']} headline")
        for ln in head_lines:
            d.text((x, ty), ln, font=serif(15), fill=INK); ty += 17
        deck_lines = wrap(d, hero["deck"], inter(11, 400), pw - 4)
        if len(deck_lines) > 2: raise SystemExit(f"D hero {hero['n']} deck")
        for ln in deck_lines:
            d.text((x, ty + 1), ln, font=inter(11, 400), fill=(70, 74, 82)); ty += 12
        d.rectangle([x, y, x + pw, y + art_h], outline=CRIMSON, width=3)
    y += art_h + 6 + 51 + 26
    d.text((MARGIN, y), "THE DAY IN FULL — INK FOLLOWS WEIGHT", font=serif(15), fill=INK)
    d.line([MARGIN + 320, y + 9, W - MARGIN, y + 9], fill=INK, width=2)
    y += 19
    colw = (CW - 16) // 3; rowh = 94; plate_w, plate_h = 92, 46
    for i, m in enumerate(MIDS):
        cx = MARGIN + (i % 3) * (colw + 8); cy = y + (i // 3) * rowh
        heavy = m["n"] in HEAVY
        d.rectangle([cx, cy + 1, cx + 4, cy + 88], fill=CRIMSON if heavy else NAVY)
        d.text((cx + 9, cy), f"{m['n']:02d}", font=arch(15, 900), fill=BLUE)
        d.text((cx + 44, cy + 3), f"{m['region']} · {m['field']} · {m['part']}", font=arch(10, 800), fill=GREY)
        cf = arch(9, 800); chw = tw(d, m["chip"], cf) + 11
        d.rectangle([cx + colw - chw, cy, cx + colw, cy + 14], fill=CHIP_COL[m["chip"]])
        d.text((cx + colw - chw + 6, cy + 2), m["chip"], font=cf, fill=WHITE)
        kind = "wood" if heavy else "flat"
        art = Image.open(os.path.join(BASE, f"art/{kind}-mid-{m['n']:02d}.webp")).convert("RGB")
        img.paste(cover(art, plate_w, plate_h), (cx + colw - plate_w, cy + 16))
        d.rectangle([cx + colw - plate_w, cy + 16, cx + colw, cy + 16 + plate_h], outline=CRIMSON if heavy else NAVY, width=2 if heavy else 1)
        head_lines = wrap(d, m["head"], arch(13, 800), colw - plate_w - 20)
        if len(head_lines) > 3: raise SystemExit(f"D mid {m['n']} headline")
        for j, ln in enumerate(head_lines):
            d.text((cx + 9, cy + 16 + j * 15), ln, font=arch(13, 800), fill=INK)
        fy = cy + 64
        d.text((cx + 9, fy), m["fig"], font=arch(13, 900), fill=CRIMSON if heavy else NAVY)
        figw = tw(d, m["fig"], arch(13, 900))
        dl = wrap(d, m["deck"], inter(10, 400), colw - 22 - figw)
        if len(dl) > 2: raise SystemExit(f"D mid {m['n']} deck")
        for j, ln in enumerate(dl):
            d.text((cx + 13 + figw, fy + 2 + j * 12), ln, font=inter(10, 400), fill=(70, 74, 82))
        d.line([cx, cy + rowh - 3, cx + colw, cy + rowh - 3], fill=LIGHT)
    y += 4 * rowh + 2
    bot = y
    draw_map(d, img, MARGIN, bot, 452, 112, AMBER)
    draw_datecheck(d, MARGIN, bot + 122, 452, 88)
    end = draw_also(d, img, MARGIN + 466, bot, CW - 466, "ALSO THURSDAY — 21 MORE, FLAGGED")
    footer(d, max(bot + 216, end) + 2, "THE CROSSWIRE")
    return img

BUILDERS = {"A": build_A, "B": build_B, "C": build_C, "D": build_D}
def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = BUILDERS[MODE]()
    path = os.path.join(out_dir, "entry.png")
    img.save(path)
    if os.path.getsize(path) > 1_000_000:
        img.convert("RGB").quantize(colors=256, method=Image.MEDIANCUT).save(path, optimize=True)
    print("wrote entry.png", img.size, os.path.getsize(path))
if __name__ == "__main__":
    main()
