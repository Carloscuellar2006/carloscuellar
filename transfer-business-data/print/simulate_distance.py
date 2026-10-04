#!/usr/bin/env python3
"""Simulate the 18x24 yard sign as seen from a moving car.

Two things are modelled honestly:

1. ANGULAR SIZE.  A 24in-wide sign at D feet subtends 2*atan(1/D).  The
   scene places the sign at its true angular size for a 45-degree camera,
   so the "how big is it really" question gets a truthful answer.

2. VISUAL ACUITY.  A 20/20 eye resolves about 1 arcminute.  So a sign
   spanning T arcminutes carries at most T resolvable elements across --
   no more.  Downsampling the artwork to T pixels wide and magnifying it
   back is exactly what the eye does, and shows which type survives.

Legibility threshold used: a capital letter needs ~20 arcmin to be read
comfortably, which works out to D_max ~= 14.3 x cap-height-in-inches.
"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SIGN      = "yard-sign-18x24.png"
SIGN_W_IN, SIGN_H_IN = 24.0, 18.0
OUT       = "yard-sign-distance-sim.jpg"

INK   = (14, 16, 19)
PAPER = (243, 244, 242)
BLUE  = (47, 168, 232)
GRAY  = (150, 156, 162)

F_BOLD  = "fonts/Archivo-Bold.ttf"
F_BLACK = "fonts/Archivo-Black.ttf"

# measured cap heights from the build, in inches
ELEMENTS = [
    ("PRESSURE WASHING", 1.97),
    ("(256) 677-5992",   3.49),
    ("Guarantee line",   0.86),
    ("Service list",     0.38),
]

def fnt(p, s):
    return ImageFont.truetype(p, s)

def txt(d, xy, s, f, fill, anchor="la"):
    d.text(xy, s, font=f, fill=fill, anchor=anchor)

def subtend_deg(size_ft, dist_ft):
    return 2 * math.degrees(math.atan((size_ft / 2) / dist_ft))

def max_read_ft(cap_in, arcmin=20.0):
    """Distance at which a capital of cap_in inches subtends `arcmin`."""
    return 286.5 * cap_in / arcmin


# ---------------------------------------------------------------- scene ----
def build_scene(sign, dist_ft=50.0, lateral_ft=10.0, W=1800, H=820):
    """Driver's-eye view. 45deg horizontal FOV, eye 3.8ft off the road."""
    FOV, EYE = 60.0, 3.8
    ppd  = W / FOV                      # pixels per degree
    horiz = int(H * 0.46)

    img = Image.new("RGB", (W, H))
    d   = ImageDraw.Draw(img)

    # sky
    for y in range(horiz):
        t = y / horiz
        d.line([(0, y), (W, y)], fill=(int(150 + 65 * t), int(178 + 60 * t), int(205 + 45 * t)))
    # ground
    for y in range(horiz, H):
        t = (y - horiz) / (H - horiz)
        d.line([(0, y), (W, y)], fill=(int(74 + 40 * t), int(104 + 46 * t), int(52 + 30 * t)))

    def ground_y(dft):
        return horiz + ppd * math.degrees(math.atan(EYE / dft))

    def ground_x(dft, lat_ft):
        return W / 2 + ppd * math.degrees(math.atan(lat_ft / dft))

    # road: near edge sweeping past the camera on the left
    road = [(ground_x(d_, -6.0), ground_y(d_)) for d_ in (400, 200, 120, 80, 55, 38, 26, 18, 12, 8, 5.5)]
    road += [(0, H), (0, ground_y(400))]
    d.polygon(road, fill=(70, 72, 76))
    # curb
    d.line([(ground_x(d_, -6.0), ground_y(d_)) for d_ in (400, 120, 55, 26, 12, 5.5)],
           fill=(178, 178, 172), width=4)

    # house behind the sign
    hy, hx = ground_y(155.0), ground_x(155.0, 16.0)
    hw = ppd * subtend_deg(44.0, 155.0)
    hh = ppd * subtend_deg(17.0, 155.0)
    d.rectangle([hx - hw / 2, hy - hh, hx + hw / 2, hy], fill=(206, 200, 188))
    d.polygon([(hx - hw / 2 - 14, hy - hh), (hx + hw / 2 + 14, hy - hh), (hx, hy - hh * 1.62)],
              fill=(96, 84, 78))
    for i in range(4):
        wx = hx - hw / 2 + hw * (0.14 + 0.22 * i)
        d.rectangle([wx, hy - hh * 0.74, wx + hw * 0.098, hy - hh * 0.40], fill=(120, 140, 156))
    d.rectangle([hx - hw * 0.40, hy - hh * 0.52, hx - hw * 0.20, hy], fill=(150, 146, 140))

    # driveway
    d.polygon([(ground_x(155.0, 8.0), ground_y(155.0)), (ground_x(155.0, 17.0), ground_y(155.0)),
               (ground_x(28.0, 24.0), ground_y(28.0)), (ground_x(28.0, 3.0), ground_y(28.0))],
              fill=(176, 174, 168))

    # ---- the sign, at true angular size ----
    sw = ppd * subtend_deg(SIGN_W_IN / 12, dist_ft)
    sh = sw * (SIGN_H_IN / SIGN_W_IN)
    sx, base = ground_x(dist_ft, lateral_ft), ground_y(dist_ft)
    stake_px = ppd * subtend_deg(1.0, dist_ft)          # ~12in of stake showing

    s = sign.resize((max(2, int(sw)), max(2, int(sh))), Image.LANCZOS)
    sx0, sy0 = int(sx - sw / 2), int(base - stake_px - sh)
    for lx in (sx0 + sw * 0.3, sx0 + sw * 0.7):         # stake legs
        d.line([(lx, base - stake_px), (lx, base)], fill=(120, 120, 124), width=max(1, int(sw * 0.02)))
    img.paste(s, (sx0, sy0))
    d.rectangle([sx0 - 1, sy0 - 1, sx0 + int(sw), sy0 + int(sh)], outline=(30, 32, 34))

    # mailbox for scale (a mailbox is ~42in to the top)
    mby, mbx = ground_y(34.0), ground_x(34.0, 11.0)
    mbh = ppd * subtend_deg(3.5, 34.0)
    mbw = ppd * subtend_deg(1.6, 34.0)
    d.line([(mbx, mby), (mbx, mby - mbh)], fill=(92, 76, 62), width=max(2, int(mbw * 0.22)))
    d.rectangle([mbx - mbw / 2, mby - mbh - mbw * 0.5, mbx + mbw / 2, mby - mbh], fill=(64, 68, 74))

    d.rectangle([0, 0, W - 1, H - 1], outline=(60, 64, 68))
    return img, sw, sh


# ------------------------------------------------------------- acuity ------
def acuity(sign, dist_ft, out_w):
    """Resample to the number of elements a 20/20 eye can resolve, then magnify."""
    arcmin = subtend_deg(SIGN_W_IN / 12, dist_ft) * 60.0
    n = max(6, int(round(arcmin)))
    small = sign.resize((n, max(4, int(n * SIGN_H_IN / SIGN_W_IN))), Image.LANCZOS)
    return small.resize((out_w, int(out_w * SIGN_H_IN / SIGN_W_IN)), Image.LANCZOS), arcmin, n


sign = Image.open(SIGN).convert("RGB")

W = 1800
scene, sw, sh = build_scene(sign, dist_ft=50.0)

DISTS = [15, 25, 40, 60, 90]
PW, GAP, PAD = 320, 30, 46
strip_h = int(PW * SIGN_H_IN / SIGN_W_IN)

H = 96 + scene.height + 150 + strip_h + 400
out = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(out)

txt(d, (PAD, 30), "HOW IT READS FROM THE ROAD", fnt(F_BLACK, 40), PAPER)
txt(d, (W - PAD, 42), "18 x 24 in  ·  staked in a lawn", fnt(F_BOLD, 23), GRAY, anchor="ra")

out.paste(scene, ((W - scene.width) // 2, 96))
y = 96 + scene.height + 18
txt(d, (PAD, y), f"Driver's eye view at 50 ft — sign is {sw:.0f}px of this "
                 f"{scene.width}px frame ({subtend_deg(2.0,50):.1f}° of a 60° view). "
                 f"Mailbox at 34 ft for scale.", fnt(F_BOLD, 22), GRAY)

y += 66
txt(d, (PAD, y), "WHAT YOUR EYE ACTUALLY RESOLVES", fnt(F_BLACK, 30), PAPER)
txt(d, (PAD, y + 40), "Artwork resampled to the detail a 20/20 eye receives at each distance, "
                      "then magnified. Nothing is added — only what survives.",
    fnt(F_BOLD, 20), GRAY)

sy = y + 96
total = len(DISTS) * PW + (len(DISTS) - 1) * GAP
sx = (W - total) // 2
for dist in DISTS:
    view, arcmin, n = acuity(sign, dist, PW)
    out.paste(view, (sx, sy))
    d.rectangle([sx - 1, sy - 1, sx + PW, sy + strip_h], outline=(70, 74, 78))
    txt(d, (sx + PW // 2, sy + strip_h + 16), f"{dist} FT", fnt(F_BLACK, 30), BLUE, anchor="ma")
    txt(d, (sx + PW // 2, sy + strip_h + 54), f"{n} px of real detail", fnt(F_BOLD, 18), GRAY, anchor="ma")
    sx += PW + GAP

ly = sy + strip_h + 108
txt(d, (PAD, ly), "LEGIBILITY BY ELEMENT", fnt(F_BLACK, 28), PAPER)
ly += 44
for name, cap in ELEMENTS:
    comfy, thresh = cap * 10, max_read_ft(cap)
    txt(d, (PAD, ly), f"{name}", fnt(F_BOLD, 22), PAPER)
    txt(d, (PAD + 430, ly), f"{cap:.2f}in caps", fnt(F_BOLD, 22), GRAY)
    txt(d, (PAD + 640, ly), f"comfortable to {comfy:.0f} ft", fnt(F_BOLD, 22), BLUE)
    txt(d, (PAD + 960, ly), f"·  last legible ~{thresh:.0f} ft", fnt(F_BOLD, 22), GRAY)
    ly += 36

out.save(OUT, quality=93)
print(f"wrote {OUT}  ({out.width}x{out.height})")
print(f"\nangular size of a 24in sign:")
for dist in DISTS + [50]:
    deg = subtend_deg(2.0, dist)
    print(f"  {dist:3d} ft : {deg:5.2f}°  = {deg*60:6.1f} arcmin across")
print(f"\nat 25 mph you cover 36.7 ft/sec — 90ft to 15ft is about 2.0 seconds of view")
