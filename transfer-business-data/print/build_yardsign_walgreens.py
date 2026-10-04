#!/usr/bin/env python3
"""Big Spring — 18 x 24 in LANDSCAPE yard sign, built for Walgreens Photo.

No photos: headline -> guarantee + QR -> phone -> services footer.

Walgreens upload rules (from their Upload FAQ):
  * JPEG, PNG or HEIC only -- no PDF
  * 8-bit RGB / sRGB only
  * under 150 MB and under 100 megapixels; use "Full Resolution" for posters
Walgreens trims somewhere between the safe area and the bleed line, so every
background runs into a 0.125 in bleed and all text sits >= 0.5 in inside trim.
"""
import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import qrcode
from qrcode.constants import ERROR_CORRECT_Q

DPI = 300
TRIM_W_IN, TRIM_H_IN = 24.0, 18.0          # landscape
BLEED_IN, SAFE_IN    = 0.125, 0.50

def inch(v): return int(round(v * DPI))

W, H   = inch(TRIM_W_IN), inch(TRIM_H_IN)  # trim canvas
BLEED  = inch(BLEED_IN)
SAFE   = inch(SAFE_IN)

INK   = (12, 13, 15)
PAPER = (246, 246, 244)
BLUE  = (47, 168, 232)

F_COND = "fonts/Archivo-Black-w70.ttf"     # condensed: taller caps at a given width
F_BOLD = "fonts/Archivo-Bold.ttf"

QR_URL = ("https://bigspringpressurewashing.com/quote"
          "?utm_source=yard-sign-18x24&utm_medium=print&utm_campaign=job-site")

BOXES = []                                  # (label, l, t, r, b) for the safe check


def font(p, s): return ImageFont.truetype(p, s)


def cap(d, s, f): return d.textbbox((0, 0), s, font=f)


def text_w(f, s, tracking=0):
    return int(sum(f.getlength(c) for c in s) + tracking * (len(s) - 1)) if tracking \
        else int(f.getlength(s))


def fit_width(s, path, target_w, tracking=0):
    lo, hi, best = 10, 4000, 10
    while lo <= hi:
        mid = (lo + hi) // 2
        if text_w(font(path, mid), s, tracking) <= target_w:
            best, lo = mid, mid + 1
        else:
            hi = mid - 1
    return best


def cap_h(d, s, path, size):
    bb = cap(d, s, font(path, size))
    return bb[3] - bb[1]


def size_for(d, lines, path, width, cap_max, tracking=0):
    """One shared size: widest line fits `width`, tallest cap <= cap_max."""
    size = min(fit_width(s, path, width, tracking) for s in lines)
    while size > 10 and max(cap_h(d, s, path, size) for s in lines) > cap_max:
        size -= 2
    return size


def line(d, s, path, cx, top, size, fill, tracking=0, label=""):
    """Draw s centred on cx with cap-top at `top`. Returns bottom y."""
    f = font(path, size)
    bb = cap(d, s, f)
    w = text_w(f, s, tracking)
    x = cx - w // 2
    y = top - bb[1]
    if tracking:
        run = x
        for ch in s:
            d.text((run, y), ch, font=f, fill=fill)
            run += f.getlength(ch) + tracking
    else:
        d.text((x, y), s, font=f, fill=fill)
    h = bb[3] - bb[1]
    BOXES.append((label.strip() or s[:18], x, top, x + w, top + h))
    if label:
        print(f"  {label:18} {s[:28]!r:32} cap={h/DPI:.2f}in  read≈{h/DPI*10:.0f}ft")
    return top + h


canvas = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(canvas)
CX = W // 2
SAFE_W = W - 2 * SAFE                        # 23.0 in of usable text width

print(f"18x24 LANDSCAPE for Walgreens  trim {TRIM_W_IN:g}x{TRIM_H_IN:g}in, "
      f"bleed {BLEED_IN}in, text safe {SAFE_IN}in\n")

# ---------------- 1. WHAT IT IS -------------------------------------------
s = size_for(d, ["PRESSURE WASHING"], F_COND, SAFE_W, inch(4.0))
head_bot = line(d, "PRESSURE WASHING", F_COND, CX, inch(0.55), s, PAPER,
                label="1 headline")
s = size_for(d, ["& EXTERIOR CLEANING"], F_BOLD, SAFE_W, inch(0.50), inch(0.075))
sub_bot = line(d, "& EXTERIOR CLEANING", F_BOLD, CX, head_bot + inch(0.26), s, BLUE,
               tracking=inch(0.075), label="  subtitle")
rule_y = sub_bot + inch(0.28)
d.rectangle([CX - inch(3.2), rule_y, CX + inch(3.2), rule_y + inch(0.07)], fill=BLUE)

# ---------------- 2. GUARANTEE (left) + QR (right) ------------------------
# Left: two promises, stacked. Right: the QR.
# The Walk-Through Promise leads -- it is settled the same day, while you are
# still set up. Stays-Clean supports it underneath. Both stay under the
# headline and phone in size, so the sign still reads WHAT -> CALL first.
BAND_TOP, BAND_BOT = inch(3.95), inch(10.55)
band_mid = (BAND_TOP + BAND_BOT) // 2

qr = qrcode.QRCode(error_correction=ERROR_CORRECT_Q, box_size=40, border=0)
qr.add_data(QR_URL); qr.make(fit=True)
qr_side, qr_pad = inch(6.00), inch(0.28)
plate = qr_side + 2 * qr_pad
plate_r = W - SAFE
plate_l = plate_r - plate
plate_t = band_mid - plate // 2
d.rounded_rectangle([plate_l, plate_t, plate_r, plate_t + plate],
                    radius=inch(0.18), fill=PAPER)
canvas.paste(qr.make_image(fill_color="black", back_color="white").convert("RGB")
               .resize((qr_side, qr_side), Image.NEAREST),
             (plate_l + qr_pad, plate_t + qr_pad))
BOXES.append(("QR plate", plate_l, plate_t, plate_r, plate_t + plate))

from fontTools.ttLib import TTFont as _TT
_apos = "\u2019" if 0x2019 in _TT(F_BOLD).getBestCmap() else "'"
# Lead-in names the walk-through explicitly, so the promise below reads as
# what happens at the end of the job rather than a vague claim.
LEAD  = "FINAL WALK-THROUGH WITH YOU"
l_trk, l_gap = inch(0.05), inch(0.26)
WALK  = [f"IF YOU DON{_apos}T LIKE IT,", "I RE-CLEAN IT."]
STAYS = ["STAYS CLEAN 6 MONTHS", "GUARANTEED"]

col_l, col_r = SAFE, plate_l - inch(0.60)
col_cx = (col_l + col_r) // 2
col_w  = col_r - col_l

l_size = size_for(d, [LEAD], F_BOLD, col_w, inch(0.55), l_trk)
l_cap  = cap_h(d, LEAD, F_BOLD, l_size)
w_size = size_for(d, WALK,  F_BOLD, col_w, inch(1.20))
s_size = size_for(d, STAYS, F_BOLD, col_w, inch(0.62))
w_caps = [cap_h(d, t, F_BOLD, w_size) for t in WALK]
s_caps = [cap_h(d, t, F_BOLD, s_size) for t in STAYS]
w_lead, s_lead, gap, rule_h = inch(0.28), inch(0.20), inch(0.34), inch(0.07)
group_h = (l_cap + l_gap + sum(w_caps) + w_lead + gap + rule_h + gap
           + sum(s_caps) + s_lead)

gy = band_mid - group_h // 2
gy = line(d, LEAD, F_BOLD, col_cx, gy, l_size, BLUE, tracking=l_trk,
          label="  walk-through lead") + l_gap
for i, t in enumerate(WALK):
    gy = line(d, t, F_BOLD, col_cx, gy, w_size, PAPER,
              label="  walk-through" if i == 0 else "") + (w_lead if i == 0 else 0)
gy += gap
d.rectangle([col_cx - inch(1.6), gy, col_cx + inch(1.6), gy + rule_h], fill=BLUE)
gy += rule_h + gap
for i, t in enumerate(STAYS):
    gy = line(d, t, F_BOLD, col_cx, gy, s_size, PAPER,
              label="  stays-clean" if i == 0 else "") + (s_lead if i == 0 else 0)

# ---------------- 3. THE ACTION -------------------------------------------
FOOT_TOP = inch(16.10)
p_size = size_for(d, ["(256) 677-5992"], F_COND, SAFE_W, inch(4.0))
p_h = cap_h(d, "(256) 677-5992", F_COND, p_size)
p_top = BAND_BOT + (FOOT_TOP - BAND_BOT - p_h) // 2
line(d, "(256) 677-5992", F_COND, CX, p_top, p_size, BLUE, label="2 phone")

# ---------------- 4. FOOTER -----------------------------------------------
d.rectangle([0, FOOT_TOP, W, H], fill=BLUE)
SERVICES = ["DRIVEWAYS · SIDEWALKS · WALKWAYS · PATIOS · PORCHES",
            "HOUSE WASHING · ROOF WASHING · FENCES · WINDOWS"]
sv = size_for(d, SERVICES, F_BOLD, int(SAFE_W * 0.72), inch(0.36))
sy = inch(16.30)
for i, t in enumerate(SERVICES):
    sy = line(d, t, F_BOLD, CX, sy, sv, INK,
              label="  services" if i == 0 else "") + inch(0.14)
AREA = "HUNTSVILLE, AL  ·  CALL OR TEXT FOR A FREE ESTIMATE"
hs = size_for(d, [AREA], F_BOLD, SAFE_W, inch(0.17), inch(0.022))
line(d, AREA, F_BOLD, CX, sy - inch(0.02), hs, INK,
     tracking=inch(0.022), label="  area line")

# ---------------- safe-zone check -----------------------------------------
print()
worst = None
for label, l, t, r, b in BOXES:
    m = min(l, t, W - r, H - b)
    if worst is None or m < worst[1]:
        worst = (label, m)
    if m < SAFE:
        print(f"  !! {label!r} is {m/DPI:.2f}in from trim (< {SAFE_IN}in)")
print(f"  tightest element: {worst[0]!r} at {worst[1]/DPI:.2f}in from trim "
      f"-> {'OK' if worst[1] >= SAFE else 'VIOLATION'}")

# ---------------- bleed: replicate edge pixels outward --------------------
# Everything touching the trim edge is flat background (ink, footer blue),
# so extending the edge rows/columns is exactly right.
full = Image.fromarray(np.pad(np.asarray(canvas),
                              ((BLEED, BLEED), (BLEED, BLEED), (0, 0)), mode="edge"))

# ---------------- exports -------------------------------------------------
try:
    from PIL import ImageCms
    srgb = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
except Exception:
    srgb = None

OUT = "yard-sign-18x24-walgreens.jpg"
for q in (95, 92, 88):
    buf = io.BytesIO()
    full.save(buf, "JPEG", quality=q, subsampling=0, dpi=(DPI, DPI),
              **({"icc_profile": srgb} if srgb else {}))
    if buf.tell() <= 10 * 1024 * 1024:
        break
with open(OUT, "wb") as fh:
    fh.write(buf.getvalue())

canvas.resize((1800, 1350), Image.LANCZOS).save("yard-sign-18x24-PREVIEW.jpg", quality=92)

gw = 1819
g = full.resize((gw, round(full.size[1] * gw / full.size[0])), Image.LANCZOS)
gd = ImageDraw.Draw(g)
k = gw / full.size[0]
bx = lambda v: int(round(v * k))
gd.rectangle([bx(BLEED), bx(BLEED), bx(BLEED + W), bx(BLEED + H)],
             outline=(255, 64, 64), width=3)
gd.rectangle([bx(BLEED + SAFE), bx(BLEED + SAFE), bx(BLEED + W - SAFE), bx(BLEED + H - SAFE)],
             outline=(255, 190, 60), width=2)
g.save("yard-sign-18x24-GUIDES.jpg", quality=92)

mp = full.size[0] * full.size[1] / 1e6
print(f"\n  upload file  {OUT}")
print(f"  pixels       {full.size[0]} x {full.size[1]} = {mp:.1f} MP  (Walgreens limit 100)")
print(f"  physical     {full.size[0]/DPI:.3f} x {full.size[1]/DPI:.3f} in incl. bleed")
print(f"  file size    {len(buf.getvalue())/1024/1024:.2f} MB  (JPEG q{q}, 4:4:4, "
      f"{'sRGB ICC embedded' if srgb else 'no ICC'})")
print(f"  QR           {qr.modules_count} modules at {qr_side/DPI:.2f}in "
      f"({qr_side/qr.modules_count/DPI*25.4:.2f}mm/module)")
