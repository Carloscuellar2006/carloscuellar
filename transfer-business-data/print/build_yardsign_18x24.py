#!/usr/bin/env python3
"""Big Spring Pressure Washing — 18 x 24 in LANDSCAPE yard sign (H-stake, Coroplast).

Hormozi brief: before/after proof, one big number, guarantee, QR.

Photos: set BEFORE_IMG / AFTER_IMG to readable file paths. If either is
missing or unreadable, a clearly-marked placeholder is drawn instead so the
layout can be reviewed before the images land.
"""
from PIL import Image, ImageDraw, ImageFont
import qrcode, os
from qrcode.constants import ERROR_CORRECT_Q

DPI = 300
W_IN, H_IN = 24.0, 18.0          # landscape
W, H = int(W_IN * DPI), int(H_IN * DPI)

INK   = (12, 13, 15)
PAPER = (246, 246, 244)
BLUE  = (47, 168, 232)
GRAY  = (150, 154, 158)
FRAME = (58, 62, 68)

F_BLACK = "fonts/Archivo-Black.ttf"
F_COND  = "fonts/Archivo-Black-w70.ttf"   # condensed: same width, ~38% taller caps
F_BOLD  = "fonts/Archivo-Bold.ttf"

QR_URL = ("https://bigspringpressurewashing.com/quote"
          "?utm_source=yard-sign-18x24&utm_medium=print&utm_campaign=job-site")

BEFORE_IMG = None    # <- set to the chosen "before" file
AFTER_IMG  = None    # <- set to the chosen "after"  file

def inch(v): return int(round(v * DPI))
def font(p, s): return ImageFont.truetype(p, s)

def fit_width(d, s, path, target_w, tracking=0):
    lo, hi, best = 10, 4000, 10
    while lo <= hi:
        mid = (lo + hi) // 2
        f = font(path, mid)
        w = int(sum(f.getlength(c) for c in s) + tracking * (len(s) - 1)) if tracking \
            else int(f.getlength(s))
        if w <= target_w: best, lo = mid, mid + 1
        else: hi = mid - 1
    return best

def cap(d, s, f): return d.textbbox((0, 0), s, font=f)

def line(d, s, path, cx, top, width=None, cap_h=None, fill=PAPER, tracking=0,
         label="", size=None):
    """Draw s centred on cx with cap-top at `top`. Returns bottom y.
    Pass `size` to set the point size directly (used when several lines
    must share one size)."""
    if size is not None:
        pass
    elif width is not None:
        size = fit_width(d, s, path, width, tracking)
        if cap_h:
            while size > 10:
                bb = cap(d, s, font(path, size))
                if bb[3] - bb[1] <= cap_h: break
                size -= 2
    else:
        size = 10
        while size < 4000:
            bb = cap(d, s, font(path, size + 2))
            if bb[3] - bb[1] > cap_h: break
            size += 2
    f = font(path, size)
    bb = cap(d, s, f)
    w = int(sum(f.getlength(c) for c in s) + tracking * (len(s) - 1)) if tracking \
        else int(f.getlength(s))
    x, y = cx - w // 2, top - bb[1]
    if tracking:
        for ch in s:
            d.text((x, y), ch, font=f, fill=fill); x += f.getlength(ch) + tracking
    else:
        d.text((x, y), s, font=f, fill=fill)
    h = bb[3] - bb[1]
    if label:
        print(f"  {label:22} {s[:26]!r:30} cap={h/DPI:.2f}in  "
              f"read≈{h/DPI*10:.0f}ft  top={top/DPI:.2f}in")
    return top + h

def load_photo(path, box_w, box_h):
    """Return an image cropped to fill box, or None if unusable."""
    if not path or not os.path.exists(path):
        return None
    try:
        im = Image.open(path); im.load()
        im = im.convert("RGB")
    except Exception as e:
        print(f"  !! could not read {path}: {e}")
        return None
    sw, sh = im.size
    scale = max(box_w / sw, box_h / sh)
    im = im.resize((max(1, int(sw * scale)), max(1, int(sh * scale))), Image.LANCZOS)
    left, top = (im.size[0] - box_w) // 2, (im.size[1] - box_h) // 2
    return im.crop((left, top, left + box_w, top + box_h))

def placeholder(canvas, x, y, w, h, word):
    """Marked-up empty frame. Hatching is drawn on its own tile and pasted so
    it cannot bleed past the box edges."""
    tile = Image.new("RGB", (w, h), (30, 33, 38))
    td = ImageDraw.Draw(tile)
    step = inch(0.55)
    for k in range(-(h // step) - 1, (w + h) // step + 2):
        td.line([(k * step, 0), (k * step + h, h)], fill=(40, 44, 50), width=inch(0.03))
    canvas.paste(tile, (x, y))
    d = ImageDraw.Draw(canvas)
    d.rectangle([x, y, x + w, y + h], outline=FRAME, width=inch(0.05))
    line(d, word, F_BLACK, x + w // 2, y + h // 2 - inch(0.90),
         width=int(w * 0.50), fill=(120, 126, 134))
    line(d, "DROP PHOTO IN", F_BOLD, x + w // 2, y + h // 2 + inch(0.62),
         width=int(w * 0.38), fill=(86, 92, 100), tracking=inch(0.03))


canvas = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(canvas)

M   = inch(0.70)                 # side margin
CX  = W // 2
CW  = W - 2 * M                  # content width 22.6in

print(f"18x24 LANDSCAPE  ({W_IN} x {H_IN} in, {W}x{H}px @ {DPI}dpi)\n")

# ---------------- 1. WHAT IT IS  (biggest statement on the sign) ----------
HEAD_M = inch(0.42)
head_bot = line(d, "PRESSURE WASHING", F_COND, CX, inch(0.45),
                width=W - 2 * HEAD_M, fill=PAPER, label="1 WHAT IT IS")
sub_bot = line(d, "& EXTERIOR CLEANING", F_BOLD, CX, head_bot + inch(0.26),
               cap_h=inch(0.50), fill=BLUE, tracking=inch(0.075),
               label="  subtitle")
d.rectangle([CX - inch(3.2), sub_bot + inch(0.28),
             CX + inch(3.2), sub_bot + inch(0.35)], fill=BLUE)

# ---------------- 2. PROOF ------------------------------------------------
# No price on this sign, so proof is the main content and takes the space
# the price block used to occupy.
# The QR sits in its own right-hand column beside the photos. That buys two
# things: the photos come down in size, and the phone below gets the FULL
# width instead of sharing a row with the QR.
qr_side = inch(5.80)                       # was 4.50in
qr_x    = W - M - qr_side

band_top, band_bot = inch(3.60), inch(9.35)
band_h  = band_bot - band_top
photos_w = qr_x - M - inch(0.62)
half_w  = (photos_w - inch(0.20)) // 2

for i, (img_path, word) in enumerate([(BEFORE_IMG, "BEFORE"), (AFTER_IMG, "AFTER")]):
    px = M + i * (half_w + inch(0.20))
    photo = load_photo(img_path, half_w, band_h)
    if photo:
        canvas.paste(photo, (px, band_top))
    else:
        placeholder(canvas, px, band_top, half_w, band_h, word)
    chip_w, chip_h = inch(2.35), inch(0.62)
    d.rectangle([px, band_top, px + chip_w, band_top + chip_h], fill=BLUE)
    line(d, word, F_BOLD, px + chip_w // 2, band_top + inch(0.20),
         cap_h=inch(0.26), fill=INK, tracking=inch(0.020))

# ---------------- 3+4. DE-RISK AND ACTION ---------------------------------
# Guarantee and phone share the left column; the QR owns the right column,
# so the two never contend for the same horizontal space.
qr = qrcode.QRCode(error_correction=ERROR_CORRECT_Q, box_size=40, border=0)
qr.add_data(QR_URL); qr.make(fit=True)
qr_pad = inch(0.28)
qr_y   = band_top + (band_h - qr_side) // 2         # centred on the photo row
d.rounded_rectangle([qr_x - qr_pad, qr_y - qr_pad,
                     qr_x + qr_side + qr_pad, qr_y + qr_side + qr_pad],
                    radius=inch(0.18), fill=PAPER)
canvas.paste(qr.make_image(fill_color="black", back_color="white")
               .convert("RGB").resize((qr_side, qr_side), Image.NEAREST), (qr_x, qr_y))

# Guarantee and phone now own the full sign width — nothing shares their row.
g_bot = line(d, "STAYS CLEAN 6 MONTHS, GUARANTEED", F_BOLD, CX, inch(10.00),
             width=int(CW * 0.94), cap_h=inch(0.86), fill=PAPER, label="  guarantee")
# The phone is width-limited, not height-limited: at full width its cap comes
# out around 2.6in and no vertical room can make it larger. So give it the
# widest measure the sign allows, then centre it in the gap that remains.
PHONE_M   = inch(0.42)                       # tighter than the 0.70 body margin
phone_w   = W - 2 * PHONE_M
FOOT_TOP  = inch(16.20)

probe = fit_width(d, "(256) 677-5992", F_COND, phone_w)
pb    = cap(d, "(256) 677-5992", font(F_COND, probe))
p_h   = pb[3] - pb[1]
p_top = g_bot + (FOOT_TOP - g_bot - p_h) // 2      # centred in the black block

p_bot = line(d, "(256) 677-5992", F_COND, CX, p_top,
             width=phone_w, cap_h=inch(4.00), fill=BLUE, label="2 THE ACTION")

print(f"  phone measure {phone_w/DPI:.2f}in wide (body margin {M/DPI:.2f} -> {PHONE_M/DPI:.2f})")
print(f"  black block {g_bot/DPI:.2f}-{FOOT_TOP/DPI:.2f}in; phone centred, "
      f"{(p_top-g_bot)/DPI:.2f}in above / {(FOOT_TOP-p_bot)/DPI:.2f}in below")
print(f"\n  photo band {band_h/DPI:.2f}in tall, each photo "
      f"{half_w/DPI:.2f} x {band_h/DPI:.2f}in  (aspect {half_w/band_h:.2f})")
print(f"  QR {qr_side/DPI:.2f}in, panel {(qr_y-qr_pad)/DPI:.2f}-{(qr_y+qr_side+qr_pad)/DPI:.2f}in")
print(f"  phone bottom {p_bot/DPI:.2f}in")

# ---------------- 5. EVERYTHING ELSE WE DO  (footer) ----------------------
d.rectangle([0, FOOT_TOP, W, H], fill=BLUE)

SERVICES = ["DRIVEWAYS · SIDEWALKS · WALKWAYS · PATIOS · PORCHES",
            "HOUSE WASHING · ROOF WASHING · FENCES · WINDOWS"]
svc_size = min(fit_width(d, s, F_BOLD, int(CW * 0.72)) for s in SERVICES)
sy = inch(16.40)
for s in SERVICES:
    sy = line(d, s, F_BOLD, CX, sy, size=svc_size, fill=INK,
              label="  services") + inch(0.15)

line(d, "HUNTSVILLE, AL  ·  CALL OR TEXT FOR A FREE ESTIMATE", F_BOLD, CX,
     inch(17.62), cap_h=inch(0.17), fill=INK, tracking=inch(0.022))

canvas.save("yard-sign-18x24.png", dpi=(DPI, DPI))
canvas.save("yard-sign-18x24.pdf", "PDF", resolution=float(DPI))
canvas.resize((1800, 1350), Image.LANCZOS).save("yard-sign-18x24-PREVIEW.jpg", quality=92)

have = bool(BEFORE_IMG and AFTER_IMG)
print(f"\nQR {qr.modules_count} modules at {qr_side/DPI:.2f}in "
      f"({qr_side/qr.modules_count/DPI*25.4:.2f}mm/module)")
print(f"photos: {'embedded' if have else 'PLACEHOLDER — not final'}")
