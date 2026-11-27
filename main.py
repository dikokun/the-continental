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
PAPER = (243, 236, 220); INK = (16, 24, 46); NAVY = (22, 64, 60)
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
    g = ImageOps.grayscale(cover(img, w, h)).point(lambda v: 0 if v < 55 else (80 if v < 115 else (140 if v < 175 else (200 if v < 215 else 255))))
    pal = {0: BLACK, 80: (120, 24, 18), 140: RED, 200: YELLOW, 255: (250, 244, 224)}
    out = Image.new("RGB", (w, h))
    px_g = g.load(); px_o = out.load()
    for yy in range(h):
        for xx in range(w): px_o[xx, yy] = pal[px_g[xx, yy]]
    dd = ImageDraw.Draw(out)
    for yy in range(0, h, 5):
        for xx in range(0, w, 5):
            if px_g[xx, yy] == 140: dd.ellipse([xx, yy, xx + 2, yy + 2], fill=BLACK)
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
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
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
def draw_map_big(d, img, x, y, w, h, title_col):
    # Locator map v2: real continent polygons (lon/lat), supersampled coasts,
    # pins projected from each story's actual coordinates + place labels.
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    d.text((x + 10, y + 5), "WHERE IT HAPPENED — PINS = STORY NUMBERS", font=arch(11, 900), fill=title_col)
    CONT = [
        [(-165,68),(-152,71),(-140,70),(-128,70),(-118,69),(-108,68),(-98,69),(-90,66),(-84,66),(-79,68),(-82,63),(-87,59),(-92,58),(-93,52),(-89,48),(-84,47),(-79,44),(-71,44),(-70,42),(-74,39),(-76,35),(-80,32),(-81,26),(-84,29),(-89,30),(-94,29),(-97,25),(-96,19),(-92,15),(-87,21),(-86,13),(-91,14),(-96,16),(-102,19),(-105,23),(-109,25),(-112,29),(-117,33),(-122,37),(-124,45),(-129,53),(-136,59),(-148,60),(-158,58),(-164,61)],
        [(-46,60),(-41,63),(-32,68),(-22,70),(-19,74),(-24,78),(-34,80),(-48,77),(-54,71),(-53,65)],
        [(-78,8),(-74,11),(-68,11),(-62,10),(-55,6),(-51,3),(-50,0),(-44,-3),(-36,-6),(-35,-9),(-38,-14),(-39,-20),(-41,-23),(-47,-26),(-52,-33),(-56,-37),(-62,-40),(-64,-44),(-66,-49),(-68,-54),(-70,-53),(-72,-48),(-73,-42),(-73,-35),(-71,-28),(-70,-20),(-70,-18),(-74,-15),(-78,-9),(-80,-5),(-81,0),(-78,3),(-77,6)],
        [(-6,35),(0,34),(10,34),(11,33),(20,31),(30,30),(33,30),(35,27),(37,23),(39,20),(41,16),(43,12),(48,11),(51,12),(46,6),(42,0),(40,-6),(39,-12),(37,-18),(35,-24),(33,-28),(29,-32),(25,-34),(20,-35),(18,-33),(16,-28),(14,-22),(13,-17),(12,-13),(13,-8),(9,-3),(9,1),(5,4),(-2,5),(-7,4),(-12,8),(-16,12),(-17,16),(-17,21),(-16,25),(-14,29),(-10,31)],
        [(-9,37),(-9,44),(-2,44),(-1,47),(-4,48),(-1,50),(1,52),(4,54),(7,56),(8,58),(11,58),(14,56),(19,56),(21,58),(24,60),(25,63),(23,66),(27,68),(32,70),(38,66),(45,68),(58,69),(70,70),(82,70),(94,71),(106,71),(118,72),(130,72),(142,72),(154,71),(164,70),(174,69),(178,66),(176,62),(169,60),(161,57),(156,51),(149,49),(142,46),(141,41),(139,37),(135,34),(131,33),(128,37),(124,39),(121,37),(120,31),(121,27),(117,24),(112,22),(109,18),(108,13),(107,8),(105,2),(102,1),(100,6),(98,10),(97,15),(94,17),(91,22),(88,21),(85,19),(81,15),(78,9),(76,12),(73,18),(70,21),(66,25),(61,25),(56,26),(52,26),(50,29),(48,30),(44,29),(42,32),(39,36),(36,36),(33,36),(29,36),(26,38),(23,36),(21,38),(18,40),(15,38),(13,41),(11,44),(8,44),(5,43),(2,42),(-1,39),(-3,37),(-6,36)],
        [(-5,50),(-3,52),(-4,54),(-6,56),(-8,58),(-5,58),(-3,57),(-1,55),(-1,52),(-2,51)],
        [(130,31),(132,33),(135,34),(138,35),(140,37),(141,40),(142,44),(140,45),(139,40),(137,36),(134,34),(131,32)],
        [(96,5),(100,2),(104,-2),(107,-6),(111,-7),(115,-8),(120,-9),(125,-10),(130,-8),(136,-3),(141,-3),(140,-7),(134,-8),(128,-9),(121,-10),(115,-10),(109,-8),(103,-5),(98,1)],
        [(113,-22),(114,-28),(115,-33),(118,-35),(124,-33),(130,-32),(133,-32),(136,-35),(138,-36),(140,-38),(145,-38),(147,-39),(150,-37),(153,-32),(153,-27),(151,-23),(149,-20),(146,-19),(143,-15),(142,-11),(140,-14),(139,-17),(136,-15),(135,-12),(132,-11),(129,-13),(126,-14),(122,-17),(118,-20)],
    ]
    LONLAT = {1: (30.5, 50.4), 2: (-73.9, 40.7), 3: (4.35, 50.85), 4: (34.3, 31.4),
              5: (125.75, 39.0), 6: (106.8, -6.6), 7: (-0.1, 51.5), 8: (6.96, 50.94),
              9: (31.2, 30.0), 10: (41.9, 44.6), 11: (-77.0, 38.9), 12: (139.7, 35.7),
              13: (126.98, 37.57), 14: (56.5, 26.6), 15: (30.5, 50.4)}
    SS = 3
    lw_, lh_ = (w - 12) * SS, (h - 28) * SS
    layer = Image.new("RGB", (lw_, lh_), NAVY)
    ld = ImageDraw.Draw(layer)
    def proj(lon, lat):
        return ((lon + 168) / 346.0 * lw_, (76 - lat) / 132.0 * lh_)
    for poly in CONT:
        ld.polygon([proj(lon, lat) for lon, lat in poly], fill=(233, 224, 198))
    img.paste(layer.resize((w - 12, h - 28), Image.LANCZOS), (x + 6, y + 24))
    illustrated = [hh["n"] for hh in HEROES] + [m["n"] for m in MIDS]
    pts = {}
    for n in sorted(illustrated):
        lon, lat = LONLAT[n]
        pts[n] = [x + 6 + (lon + 168) / 346.0 * (w - 12), y + 24 + (76 - lat) / 132.0 * (h - 28)]
    import math
    keys = sorted(pts)
    origin = {n: tuple(pts[n]) for n in keys}
    for _ in range(200):
        moved = False
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                a, b = pts[keys[i]], pts[keys[j]]
                dx, dy = b[0] - a[0], b[1] - a[1]
                dist = math.hypot(dx, dy)
                if dist < 22:
                    if dist < 0.01: dx, dy, dist = 1.0, 0.3, 1.04
                    push = (22 - dist) / 2.0
                    ux, uy = dx / dist, dy / dist
                    a[0] -= ux * push; a[1] -= uy * push
                    b[0] += ux * push; b[1] += uy * push
                    moved = True
        for n in keys:
            ox, oy = origin[n]
            vx, vy = pts[n][0] - ox, pts[n][1] - oy
            vd = math.hypot(vx, vy)
            if vd > 13:
                pts[n][0] = ox + vx / vd * 13; pts[n][1] = oy + vy / vd * 13
            pts[n][0] = min(max(pts[n][0], x + 12), x + w - 12)
            pts[n][1] = min(max(pts[n][1], y + 27), y + h - 11)
        if not moved: break
    for n in keys:
        px, py = pts[n]
        d.ellipse([px - 10, py - 10, px + 10, py + 10], fill=AMBER, outline=INK, width=2)
        st = str(n); f = arch(11, 900)
        d.text((px - tw(d, st, f) / 2, py - 6), st, font=f, fill=INK)
    for n, txt, side in [(2, "NEW YORK", "se"), (6, "BOGOR", "l"), (12, "TOKYO", "r")]:
        px, py = pts[n]; f = arch(7, 800); wtxt = tw(d, txt, f)
        if side == "r": lx, ly = px + 15, py - 4
        elif side == "se": lx, ly = px + 14, py + 12
        else: lx, ly = px - 13 - wtxt, py - 4
        d.text((lx, ly), txt, font=f, fill=(255, 246, 220))


def draw_datecheck(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 233, 220), outline=INK, width=1)
    d.rectangle([x, y, x + 6, y + h], fill=CRIMSON)
    d.text((x + 13, y + 4), "DATE CHECK — NOT THURSDAY, NOT PRINTED AS ITS NEWS:", font=arch(11, 900), fill=CRIMSON)
    if w > 470 or h < 76:
        colw = (w - 32) // 2
        for i, (s_, dd) in enumerate(DATE_CHECK):
            cx = x + 13 + (i // 3) * (colw + 12); cy = y + 24 + (i % 3) * 38
            lines = wrap(d, f"· {s_} ({dd})", inter(10.5, 500), colw)
            if len(lines) > 2: raise SystemExit(f"date check wide wraps: {s_}")
            for k, ln in enumerate(lines):
                d.text((cx, cy + k * 15), ln, font=inter(10.5, 500), fill=(52, 56, 64))
        return
    ty = y + 20
    for s, dd in DATE_CHECK:
        lines = wrap(d, f"· {s} ({dd})", inter(10, 500), w - 24)
        if len(lines) > 2: raise SystemExit(f"date check wraps: {s}")
        for l2 in lines:
            d.text((x + 13, ty), l2, font=inter(10, 500), fill=(52, 56, 64)); ty += 12
def draw_also(d, img, ax, y, aw, title):
    d.text((ax, y), "Also on Thursday", font=serif(20), fill=INK)
    note = "24 MORE DISPATCHES · 7 REGIONS IN THIS EDITION"
    d.text((ax + aw - tw(d, note, arch(9, 900)), y + 7), note, font=arch(9, 900), fill=CRIMSON)
    chips = [p.strip() for p in REGION_COUNTS.replace(" = 36 STORIES", "").split("·")]
    cols = [NAVY, CRIMSON, GREEN, (90, 60, 150), BLUE, (150, 110, 20), (20, 110, 110)]
    lx = ax
    for i, cp in enumerate(chips):
        wch = tw(d, cp, arch(8, 800)) + 12
        d.rectangle([lx, y + 27, lx + wch, y + 42], fill=cols[i % len(cols)])
        d.text((lx + 6, y + 30), cp, font=arch(8, 800), fill=WHITE)
        lx += wch + 6
    colw = (aw - 20) // 3; per = (len(ALSO) + 2) // 3
    for i, (n, region, code, text) in enumerate(ALSO):
        cx = ax + (i // per) * (colw + 10); cy = y + 52 + (i % per) * 15
        d.text((cx, cy), f"{n}", font=arch(11, 900), fill=CRIMSON)
        lines = wrap(d, text, inter(10.5, 500), colw - 26)
        if len(lines) > 1: raise SystemExit(f"also {n} wraps (A2)")
        d.text((cx + 24, cy + 1), lines[0], font=inter(10.5, 500), fill=(40, 44, 52))
    return y + 52 + per * 15 + 2
def footer(d, y, name):
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=1)
    d.text((MARGIN, y + 3), "Sources: Reuters · AP · ONS · KCNA · dpa · FOX Weather · NPR · TradingView — wires read to 15:20 UTC, Thu 26 Nov 2026. Scenes are drawn illustrations, not photographs.", font=inter(9, 400), fill=GREY)
    credit = f"{name} · DRAWN BY AN AI AGENT FOR MAKE.FUN · EVERY STORY HAPPENED OR WAS FIRST REPORTED ON THURSDAY 26 NOVEMBER 2026"
    if tw(d, credit, arch(9, 800)) > CW - 8: raise SystemExit("footer credit too wide")
    d.text((MARGIN, y + 14), credit, font=arch(9, 800), fill=INK)

HEAVY = {4, 5, 6, 9, 10, 14, 15}  # conflict / disaster mids -> woodcut in D

def grain(img, box, alpha=0.08):
    x0, y0, x1, y1 = (int(v) for v in box)
    reg = img.crop((x0, y0, x1, y1))
    noise = Image.effect_noise(reg.size, 22).convert("RGB")
    img.paste(Image.blend(reg, noise, alpha), (x0, y0))

def draw_statstrip(d, y):
    d.rectangle([MARGIN, y, W - MARGIN, y + 42], fill=NAVY)
    stats = [("113", "drones and missiles hit Kyiv in the night"),
             ("81.5M", "US travellers over the holiday weekend"),
             ("€45BN", "Ukraine loan fought over in Brussels"),
             ("77,000", "UK net migration — lowest since 1997")]
    cw4 = CW // 4
    for i, (fig, cap) in enumerate(stats):
        sx = MARGIN + i * cw4 + 12
        d.text((sx, y + 7), fig, font=serif(26), fill=AMBER)
        fw = tw(d, fig, serif(26))
        lines = wrap(d, cap, inter(9.5, 400), cw4 - fw - 26)
        for j, ln in enumerate(lines[:2]):
            d.text((sx + fw + 9, y + 8 + j * 12), ln, font=inter(9.5, 400), fill=(200, 206, 220))
        if i: d.line([MARGIN + i * cw4, y + 6, MARGIN + i * cw4, y + 36], fill=(52, 58, 74), width=1)

def hero_block(img, d, y, art_h, head_f, head_lh, art_fn):
    pw = (CW - 16) // 3
    end_max = y
    for i, hero in enumerate(HEROES):
        x = MARGIN + i * (pw + 8)
        art = Image.open(os.path.join(BASE, ART[hero["scene"]])).convert("RGB")
        img.paste(art_fn(art, pw, art_h), (x, y))
        grain(img, (x, y, x + pw, y + art_h))
        d.rectangle([x, y, x + pw, y + art_h], outline=INK, width=2)
        d.rectangle([x, y, x + 32, y + 21], fill=INK)
        d.text((x + 6, y + 3), f"{hero['n']:02d}", font=arch(13, 900), fill=WHITE)
        ty = y + art_h + 5
        cw_ = tw(d, hero["chip"], arch(10, 800)) + 12
        if tw(d, hero["banner"], arch(12, 900)) > pw - cw_ - 8: raise SystemExit(f"hero {hero['n']}: banner too wide for paper line")
        d.text((x, ty), hero["banner"], font=arch(12, 900), fill=CRIMSON)
        d.rectangle([x + pw - cw_, ty - 1, x + pw, ty + 15], fill=CHIP_COL[hero["chip"]])
        d.text((x + pw - cw_ + 6, ty + 1), hero["chip"], font=arch(10, 800), fill=WHITE)
        ty += 17
        head_lines = wrap(d, hero["head"], head_f, pw - 4)
        if len(head_lines) > 3: raise SystemExit(f"hero {hero['n']}: headline {len(head_lines)} lines")
        for ln in head_lines:
            d.text((x, ty), ln, font=head_f, fill=INK); ty += head_lh
        deck_lines = wrap(d, hero["deck"], inter(11, 400), pw - 4)
        if len(deck_lines) > 2: raise SystemExit(f"hero {hero['n']}: deck {len(deck_lines)} lines")
        for ln in deck_lines:
            d.text((x, ty + 1), ln, font=inter(11, 400), fill=(70, 74, 82)); ty += 12
        end_max = max(end_max, ty)
    return end_max + 4

def mid_plate_A(img, d, y, rowh, plate_h):
    colw = (CW - 16) // 3
    pw_ = 108
    for i, m in enumerate(MIDS):
        cx = MARGIN + (i % 3) * (colw + 8); cy = y + (i // 3) * rowh
        art = Image.open(os.path.join(BASE, MID_ART[m["n"]])).convert("RGB")
        img.paste(cover(art, pw_, plate_h), (cx, cy))
        grain(img, (cx, cy, cx + pw_, cy + plate_h))
        d.rectangle([cx, cy, cx + pw_, cy + plate_h], outline=INK, width=1)
        d.rectangle([cx, cy, cx + 27, cy + 18], fill=INK)
        d.text((cx + 4, cy + 2), f"{m['n']:02d}", font=arch(11, 900), fill=WHITE)
        tx = cx + pw_ + 10; twid = cx + colw - tx
        d.text((tx, cy + 1), f"{m['region']} · {m['field']}", font=arch(8, 800), fill=CRIMSON)
        cf = arch(9, 800); chw = tw(d, m["chip"], cf) + 11
        d.rectangle([cx + colw - chw, cy, cx + colw, cy + 14], fill=CHIP_COL[m["chip"]])
        d.text((cx + colw - chw + 6, cy + 2), m["chip"], font=cf, fill=WHITE)
        head_lines = wrap(d, m["head"], serif(17), twid)
        if len(head_lines) > 2: raise SystemExit(f"mid {m['n']}: headline {len(head_lines)} lines (A2)")
        ty = cy + 14
        for ln in head_lines:
            d.text((tx, ty), ln, font=serif(17), fill=INK); ty += 19
        dy = ty + 3
        d.text((tx, dy), m["fig"], font=arch(11, 900), fill=CRIMSON)
        figw = tw(d, m["fig"], arch(11, 900))
        words = m["deck"].split(); lines = []; cur = ""; first = True
        for wd in words:
            lim = twid - 12 - figw if first else twid
            t = (cur + " " + wd).strip()
            if tw(d, t, inter(10, 400)) <= lim: cur = t
            else: lines.append(cur); cur = wd; first = False
        if cur: lines.append(cur)
        maxlines = 3 if len(head_lines) == 1 else 2
        if not lines or len(lines) > maxlines: raise SystemExit(f"mid {m['n']}: deck {len(lines)} lines (A2)")
        for k, ln in enumerate(lines):
            lx = tx + 10 + figw if k == 0 else tx
            d.text((lx, dy + 1 + k * 12), ln, font=inter(10, 400), fill=(70, 74, 82))
        d.line([cx, cy + rowh - 3, cx + colw, cy + rowh - 3], fill=LIGHT)


def mid_large(img, d, y, plate_fn, fig_col_fn, bar_fn):
    colw = (CW - 16) // 3; rowh = 108; plate_h = 48
    for i, m in enumerate(MIDS):
        cx = MARGIN + (i % 3) * (colw + 8); cy = y + (i // 3) * rowh
        d.rectangle([cx, cy + 1, cx + 4, cy + 100], fill=bar_fn(m))
        d.text((cx + 9, cy), f"{m['n']:02d}", font=arch(15, 900), fill=BLUE)
        d.text((cx + 44, cy + 3), f"{m['region']} · {m['field']} · {m['part']}", font=arch(10, 800), fill=GREY)
        cf = arch(9, 800); chw = tw(d, m["chip"], cf) + 11
        d.rectangle([cx + colw - chw, cy, cx + colw, cy + 14], fill=CHIP_COL[m["chip"]])
        d.text((cx + colw - chw + 6, cy + 2), m["chip"], font=cf, fill=WHITE)
        plate, bcol, bw_ = plate_fn(m, colw, plate_h)
        img.paste(plate, (cx, cy + 16))
        d.rectangle([cx, cy + 16, cx + colw, cy + 16 + plate_h], outline=bcol, width=bw_)
        head_lines = wrap(d, m["head"], arch(12, 800), colw - 4)
        if len(head_lines) > 2: raise SystemExit(f"mid {m['n']}: headline {len(head_lines)} lines (large)")
        ty = cy + 67
        for ln in head_lines:
            d.text((cx + 2, ty), ln, font=arch(12, 800), fill=INK); ty += 13
        fy = cy + 94
        d.text((cx + 2, fy), m["fig"], font=arch(12, 900), fill=fig_col_fn(m))
        figw = tw(d, m["fig"], arch(12, 900))
        dl = wrap(d, m["deck"], inter(10, 400), colw - 24 - figw)
        if len(dl) > 1: raise SystemExit(f"mid {m['n']}: deck wraps (large)")
        d.text((cx + 12 + figw, fy + 1), dl[0], font=inter(10, 400), fill=(70, 74, 82))
        d.line([cx, cy + rowh - 2, cx + colw, cy + rowh - 2], fill=LIGHT)

def data_strip(m, w, h):
    s = Image.new("RGB", (w, h), NAVY); sd = ImageDraw.Draw(s)
    hs = [0.3 + ((m["n"] * (k + 3)) % 10) / 15.0 for k in range(9)]
    for k, hh in enumerate(hs):
        bx = 10 + k * 17; bh = int((h - 14) * hh)
        sd.rectangle([bx, h - 7 - bh, bx + 10, h - 7], fill=AMBER if k == len(hs) - 1 else (120, 140, 180))
    sd.text((w - tw(sd, m["fig"], arch(15, 900)) - 10, 8), m["fig"], font=arch(15, 900), fill=AMBER)
    sd.text((w - tw(sd, "THE FIGURE, DRAWN", arch(8, 800)) - 10, 30), "THE FIGURE, DRAWN", font=arch(8, 800), fill=(178, 186, 205))
    return s

def build_A():
    img = Image.new("RGB", (W, W), PAPER); d = ImageDraw.Draw(img)
    y = 10
    d.text((MARGIN, y), "THE", font=serif(19), fill=INK)
    d.text((MARGIN, y + 21), "CONTINENTAL", font=serif(19), fill=INK)
    d.text((MARGIN + 168, y - 2), "Thursday 26 November 2026", font=serif(46), fill=INK)
    for j, ln in enumerate(["DAY 330 OF 2026", "36 STORIES · 7 REGIONS", "WIRES TO 15:20 UTC"]):
        d.text((W - MARGIN - tw(d, ln, arch(9, 800)), y + 2 + j * 13), ln, font=arch(9, 800), fill=GREY)
    y += 56
    d.rectangle([MARGIN, y, W - MARGIN, y + 24], fill=NAVY)
    tx = MARGIN + 12
    for i, t in enumerate(["KYIV HIT BY 113 DRONES", "PARADE GROUNDED — A FIRST IN 100 YEARS", "€45BN LOAN FIGHT IN BRUSSELS"]):
        d.text((tx, y + 6), t, font=arch(10.5, 800), fill=WHITE)
        tx += tw(d, t, arch(10.5, 800))
        if i < 2:
            d.text((tx + 10, y + 6), "•", font=arch(10.5, 800), fill=AMBER)
            tx += 30
    y += 30
    y = hero_block(img, d, y, 150, serif(28), 32, lambda a, w, h: cover(a, w, h))
    y += 2
    mid_plate_A(img, d, y, 84, 78)
    y += 3 * 84 - 2
    y += 8
    draw_statstrip(d, y)
    y += 42
    y += 10
    end = draw_also(d, img, MARGIN, y, CW, "")
    bot = end + 8
    draw_map_big(d, img, MARGIN, bot, 430, 150, AMBER)
    draw_datecheck(d, MARGIN + 444, bot, CW - 444, 150)
    footer(d, bot + 154, "THE CONTINENTAL")
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
    pw = (CW - 16) // 3; ph = 92
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
    mid_large(img, d, y, lambda m, w, h: (data_strip(m, w, h), INK, 1), lambda m: CRIMSON, lambda m: NAVY)
    y += 4 * 108 + 2
    bot = y
    end = draw_also(d, img, MARGIN, bot, 540, "ALSO THURSDAY — 21 MORE, FLAGGED")
    mx = MARGIN + 554; mw = CW - 554
    draw_map(d, img, mx, bot, mw, 100, AMBER)
    draw_datecheck(d, mx, bot + 110, mw, 100)
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
    y = hero_block(img, d, y, 70, arch(15, 900), 17, lambda a, w, h: halftone(a, w, h))
    d.rectangle([MARGIN, y, W - MARGIN, y + 18], fill=BLACK)
    d.text((MARGIN + 8, y + 3), "THE DAY IN FULL", font=arch(12, 900), fill=YELLOW)
    y += 22
    mid_large(img, d, y,
        lambda m, w, h: (halftone(Image.open(os.path.join(BASE, MID_ART[m["n"]])).convert("RGB"), w, h), BLACK, 2),
        lambda m: RED, lambda m: RED)
    y += 4 * 108 + 2
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
    pw = (CW - 16) // 3; art_h = 70
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
    _ht = "THE DAY IN FULL — INK FOLLOWS WEIGHT"
    d.text((MARGIN, y), _ht, font=serif(15), fill=INK)
    d.line([MARGIN + tw(d, _ht, serif(15)) + 12, y + 9, W - MARGIN, y + 9], fill=INK, width=2)
    y += 19
    mid_large(img, d, y,
        lambda m, w, h: (cover(Image.open(os.path.join(BASE, f"art/{'wood' if m['n'] in HEAVY else 'flat'}-mid-{m['n']:02d}.webp")).convert("RGB"), w, h), CRIMSON if m["n"] in HEAVY else NAVY, 2 if m["n"] in HEAVY else 1),
        lambda m: CRIMSON if m["n"] in HEAVY else NAVY, lambda m: CRIMSON if m["n"] in HEAVY else NAVY)
    y += 4 * 108 + 2
    bot = y
    draw_map(d, img, MARGIN, bot, 452, 112, AMBER)
    draw_datecheck(d, MARGIN, bot + 122, 452, 88)
    end = draw_also(d, img, MARGIN + 466, bot, CW - 466, "ALSO THURSDAY — 21 MORE, FLAGGED")
    footer(d, max(bot + 216, end) + 2, "THE CROSSWIRE")
    return img


def build_W():
    img = Image.new("RGB", (W, W), PAPER); d = ImageDraw.Draw(img)
    PART_COL = {"NIGHT": NAVY, "MORNING": (176, 116, 20), "AFTERNOON": TEAL, "EVENING": CRIMSON}
    y = 10
    d.text((MARGIN, y), "THE DAYWATCH", font=arch(21, 900), fill=CRIMSON)
    d.text((MARGIN + 218, y + 5), "ONE DAY · ONE CLOCK · EVERY STORY AT ITS HOUR", font=arch(12, 800), fill=GREY)
    y += 24
    d.text((MARGIN, y), "THURSDAY 26 NOVEMBER 2026", font=arch(44, 900), fill=INK)
    slab_x = W - MARGIN - 150
    d.rectangle([slab_x, y - 24, W - MARGIN, y + 47], fill=INK)
    d.text((slab_x + 14, y - 18), "DAY 330", font=arch(15, 900), fill=AMBER)
    d.text((slab_x + 14, y + 2), "OF 2026", font=arch(15, 900), fill=WHITE)
    d.text((slab_x + 14, y + 22), "36 STORIES", font=arch(15, 900), fill=WHITE)
    y += 48
    d.text((MARGIN, y), REGION_COUNTS, font=arch(14, 900), fill=INK)
    y += 18
    rib_y = y; seg_w = CW / 4.0
    parts = [("NIGHT 00-06", NAVY), ("MORNING 06-12", (176, 116, 20)), ("AFTERNOON 12-18", TEAL), ("EVENING 18-24", CRIMSON)]
    for i, (label, col) in enumerate(parts):
        x0 = MARGIN + i * seg_w
        d.rectangle([x0, rib_y, x0 + seg_w - 2, rib_y + 15], fill=col)
        d.text((x0 + 8, rib_y + 2), label, font=arch(11, 900), fill=WHITE)
    bar_y = rib_y + 18
    d.rectangle([MARGIN, bar_y, W - MARGIN, bar_y + 15], fill=(232, 226, 208))
    plotted = [(h["hour"], h["n"]) for h in HEROES] + [(m["hour"], m["n"]) for m in MIDS]
    for j, (hr, n) in enumerate(sorted(plotted)):
        px = MARGIN + hr * CW / 24.0; py = bar_y + (3 if j % 2 == 0 else 10)
        d.ellipse([px - 7, py - 4, px + 7, py + 10], fill=INK)
        s = str(n); d.text((px - tw(d, s, arch(8, 900)) / 2, py - 2), s, font=arch(8, 900), fill=AMBER)
    y = bar_y + 18
    d.rectangle([MARGIN, y, W - MARGIN, y + 38], fill=INK)
    rw = CW // 6
    for i, (fig, cap) in enumerate(RAIL):
        rx = MARGIN + i * rw + 10
        d.text((rx, y + 3), fig, font=arch(18, 900), fill=AMBER)
        for j, ln in enumerate(wrap(d, cap, arch(7, 700), rw - 16)[:2]):
            d.text((rx, y + 23 + j * 8), ln, font=arch(7, 700), fill=(178, 186, 205))
        if i: d.line([MARGIN + i * rw, y + 5, MARGIN + i * rw, y + 33], fill=(52, 58, 74), width=1)
    y += 39
    y = hero_block(img, d, y, 70, arch(16, 900), 18, lambda a, w, h: cover(a, w, h))
    d.text((MARGIN, y), "THE DAY IN FULL - BY THE CLOCK", font=arch(13, 900), fill=INK)
    d.line([MARGIN + 252, y + 7, W - MARGIN, y + 7], fill=INK, width=2)
    y += 14
    mid_large(img, d, y,
        lambda m, w, h: (cover(Image.open(os.path.join(BASE, MID_ART[m["n"]])).convert("RGB"), w, h), INK, 1),
        lambda m: PART_COL[m["part"]], lambda m: PART_COL[m["part"]])
    y += 4 * 108 + 2
    bot = y
    draw_map(d, img, MARGIN, bot, 452, 112, AMBER)
    draw_datecheck(d, MARGIN, bot + 122, 452, 88)
    end = draw_also(d, img, MARGIN + 466, bot, CW - 466, "ALSO THURSDAY - 21 MORE, FLAGGED")
    footer(d, max(bot + 216, end) + 2, "THE DAYWATCH")
    return img

BUILDERS = {"A": build_A, "B": build_B, "C": build_C, "D": build_D, "W": build_W}
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
