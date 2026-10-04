#!/usr/bin/env python3
"""Big Spring Pressure Washing — 20 x 30 in job-site services sign.

Changes from the 20x28 version:
  - page is 20 x 30 in
  - "SCAN FOR A / FREE QUOTE" removed
  - QR enlarged to fill the reclaimed space
"""
from PIL import Image, ImageDraw, ImageFont
import qrcode
from qrcode.constants import ERROR_CORRECT_Q

DPI = 300
W_IN, H_IN = 20.0, 30.0
W, H = int(W_IN * DPI), int(H_IN * DPI)

INK   = (12, 13, 15)
PAPER = (246, 246, 244)
BLUE  = (47, 168, 232)
GRAY  = (150, 154, 158)

F_BLACK = "fonts/Archivo-Black.ttf"
F_XBOLD = "fonts/Archivo-ExtraBold.ttf"
F_BOLD  = "fonts/Archivo-Bold.ttf"
F_SEMI  = "fonts/Archivo-SemiBold.ttf"

QR_URL = "https://bigspringpressurewashing.com/quote?utm_source=yard-sign&utm_medium=print&utm_campaign=job-site"

def inch(v):
    return int(round(v * DPI))

def font(path, size):
    return ImageFont.truetype(path, size)

def text_wh(d, s, f, tracking=0):
    if tracking and len(s) > 1:
        w = sum(d.textbbox((0, 0), ch, font=f)[2] - d.textbbox((0, 0), ch, font=f)[0] for ch in s)
        w += tracking * (len(s) - 1)
        # width via advance is more reliable for tracked text
        w = int(sum(f.getlength(ch) for ch in s) + tracking * (len(s) - 1))
    else:
        w = int(f.getlength(s))
    bb = d.textbbox((0, 0), s, font=f)
    return w, bb[3] - bb[1]

def fit_width(d, s, path, target_w, lo=10, hi=3000, tracking=0):
    """Largest font size whose rendered width <= target_w."""
    best = lo
    while lo <= hi:
        mid = (lo + hi) // 2
        f = font(path, mid)
        w, _ = text_wh(d, s, f, tracking)
        if w <= target_w:
            best = mid; lo = mid + 1
        else:
            hi = mid - 1
    return best

def cap_box(d, s, f):
    """Bounding box of the inked glyphs, for true optical placement."""
    return d.textbbox((0, 0), s, font=f)

def draw_centered(d, s, path, cx, top, cap_h=None, target_w=None, fill=PAPER,
                  tracking=0, size=None):
    """Draw s centered on cx. Either cap_h (target cap height in px) or
    target_w (max width in px) sets the size. Returns (size, bottom_y)."""
    if size is None:
        if target_w is not None:
            size = fit_width(d, s, path, target_w, tracking=tracking)
            if cap_h is not None:
                # don't exceed the height budget either
                s2 = size
                while s2 > 10:
                    f = font(path, s2)
                    bb = cap_box(d, s, f)
                    if bb[3] - bb[1] <= cap_h:
                        break
                    s2 -= 2
                size = s2
        else:
            size = 10
            while size < 3000:
                f = font(path, size + 2)
                bb = cap_box(d, s, f)
                if bb[3] - bb[1] > cap_h:
                    break
                size += 2
    f = font(path, size)
    bb = cap_box(d, s, f)
    w = int(f.getlength(s)) if not tracking else int(sum(f.getlength(c) for c in s) + tracking * (len(s) - 1))
    x = cx - w // 2
    y = top - bb[1]
    if tracking:
        cx_run = x
        for ch in s:
            d.text((cx_run, y), ch, font=f, fill=fill)
            cx_run += f.getlength(ch) + tracking
    else:
        d.text((x, y), s, font=f, fill=fill)
    return size, top + (bb[3] - bb[1])

def checkbox(d, x, y, side, radius_frac=0.16):
    r = int(side * radius_frac)
    d.rounded_rectangle([x, y, x + side, y + side], radius=r, fill=BLUE)
    # white check
    lw = max(3, int(side * 0.14))
    p1 = (x + side * 0.24, y + side * 0.52)
    p2 = (x + side * 0.43, y + side * 0.71)
    p3 = (x + side * 0.76, y + side * 0.29)
    d.line([p1, p2], fill=PAPER, width=lw)
    d.line([p2, p3], fill=PAPER, width=lw)


canvas = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(canvas)

MARGIN = inch(0.55)
CX = W // 2
CONTENT_W = W - 2 * MARGIN

# ---------------- top bar ----------------
d.rectangle([0, 0, W, inch(0.70)], fill=BLUE)
draw_centered(d, "PRESSURE WASHING IN PROGRESS", F_BOLD, CX, inch(0.255),
              cap_h=inch(0.19), fill=INK, tracking=inch(0.022))

# ---------------- headline ----------------
# Two blocks: white = what the business does, blue = the full guarantee
# sentence. Every line inside a block shares one font size so the block
# reads as a single object rather than a stack of independent lines.
def stack_block(lines, path, y, width, fill, leading, gap_after):
    """Draw `lines` centered, all at one size chosen so the widest fits
    `width`. Returns the y below the block."""
    size = min(fit_width(d, s, path, width) for s in lines)
    f = font(path, size)
    for i, s in enumerate(lines):
        bb = cap_box(d, s, f)
        w = int(f.getlength(s))
        d.text((CX - w // 2, y - bb[1]), s, font=f, fill=fill)
        h = bb[3] - bb[1]
        print(f"    {s!r:24} size={size:4d}  cap={h/DPI:.2f}in  top={y/DPI:.2f}in")
        y += h + (leading if i < len(lines) - 1 else 0)
    return y + gap_after

print("headline:")
y = inch(0.88)
y = stack_block(["EXTERIOR CLEANING", "PRESSURE WASHING"],
                F_BLACK, y, CONTENT_W, PAPER,
                leading=inch(0.10), gap_after=inch(0.34))
y = stack_block(["STAYS CLEAN 6 MONTHS", "OR I RE-CLEAN IT FREE"],
                F_BLACK, y, CONTENT_W, BLUE,
                leading=inch(0.10), gap_after=0)
print(f"    headline block ends at {y/DPI:.2f}in")
HEADLINE_BOT = y

# ---------------- section header ----------------
hdr_top = HEADLINE_BOT + inch(0.42)
_, hdr_bot = draw_centered(d, "WHAT WE TREAT", F_BOLD, CX, hdr_top,
                           cap_h=inch(0.36), fill=BLUE, tracking=inch(0.035))
rule_y = hdr_bot + inch(0.16)
d.rectangle([CX - inch(1.5), rule_y, CX + inch(1.5), rule_y + inch(0.035)], fill=BLUE)

# ---------------- checklist ----------------
LEFT  = ["RED CLAY STAINS", "OIL & RUST STAINS", "DIRTY DRIVEWAYS", "WALKWAYS", "SIDEWALKS"]
RIGHT = ["ROOF ALGAE", "SIDING & MILDEW", "PATIOS & PAVERS", "FENCES", "WINDOWS"]

list_top = rule_y + inch(0.50)
row_h    = inch(1.20)
col_w    = inch(9.0)
col_x    = [MARGIN, MARGIN + inch(9.55)]
box_side = inch(0.62)
gap      = inch(0.26)

# one size for every label so the two columns read as one object
label_w = col_w - box_side - gap
sizes = []
for s in LEFT + RIGHT:
    sizes.append(fit_width(d, s, F_BLACK, label_w))
lab_size = min(sizes)
lab_font = font(F_BLACK, lab_size)

for ci, col in enumerate([LEFT, RIGHT]):
    for ri, label in enumerate(col):
        cy = list_top + ri * row_h
        bb = cap_box(d, label, lab_font)
        cap_h = bb[3] - bb[1]
        by = cy + (cap_h - box_side) // 2
        checkbox(d, col_x[ci], by, box_side)
        d.text((col_x[ci] + box_side + gap, cy - bb[1]), label, font=lab_font, fill=PAPER)

list_bot = list_top + 4*row_h + (cap_box(d,"SIDEWALKS",lab_font)[3]-cap_box(d,"SIDEWALKS",lab_font)[1])
print(f"checklist {list_top/DPI:.2f} -> {list_bot/DPI:.2f}in   price band starts 13.45in "
      f"(clearance {(inch(13.45)-list_bot)/DPI:.2f}in)")

# ---------------- price band ----------------
band_top, band_bot = inch(13.45), inch(14.75)
d.rectangle([MARGIN - inch(0.18), band_top, W - MARGIN + inch(0.18), band_bot], fill=BLUE)
draw_centered(d, "DRIVEWAYS FROM $249", F_BLACK, CX, band_top + inch(0.22),
              cap_h=inch(0.62), fill=INK)
draw_centered(d, "WALKWAY & PORCH INCLUDED FREE", F_BOLD, CX, band_top + inch(1.00),
              cap_h=inch(0.23), fill=INK, tracking=inch(0.012))

# ---------------- phone ----------------
draw_centered(d, "CALL OR TEXT", F_BOLD, CX, inch(15.15), cap_h=inch(0.30),
              fill=GRAY, tracking=inch(0.030))
_, phone_bot = draw_centered(d, "(256) 677-5992", F_BLACK, CX, inch(15.75),
                             target_w=int(CONTENT_W * 0.88), fill=BLUE)
print(f"phone bottom {phone_bot/DPI:.2f}in  ->  panel top 18.00in "
      f"(clearance {(inch(18.00)-phone_bot)/DPI:.2f}in)")

# ---------------- QR panel (enlarged; no "SCAN FOR A FREE QUOTE") ----------------
# Panel wraps the QR instead of spanning the full width — with the
# "SCAN FOR A / FREE QUOTE" text gone, a full-width panel would leave
# ~4.4 in of dead white on each side.
panel_top, panel_bot = inch(17.95), inch(29.05)
pad = inch(0.50)
qr_side = (panel_bot - panel_top) - 2 * pad
panel_w = qr_side + 2 * pad
panel_x = CX - panel_w // 2
d.rounded_rectangle([panel_x, panel_top, panel_x + panel_w, panel_bot],
                    radius=inch(0.20), fill=PAPER)

qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_Q, box_size=40, border=0)
qr.add_data(QR_URL)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
qr_img = qr_img.resize((qr_side, qr_side), Image.NEAREST)

qx = CX - qr_side // 2
qy = panel_top + pad
canvas.paste(qr_img, (qx, qy))

# ---------------- bottom bar ----------------
d.rectangle([0, inch(29.30), W, H], fill=BLUE)
draw_centered(d, "HUNTSVILLE AND SURROUNDING AREAS", F_BOLD, CX, inch(29.55),
              cap_h=inch(0.19), fill=INK, tracking=inch(0.022))

canvas.save("yard-sign-services-20x30.png", dpi=(DPI, DPI))
canvas.save("yard-sign-services-20x30.pdf", "PDF", resolution=float(DPI))
canvas.resize((1200, 1800), Image.LANCZOS).save("yard-sign-services-20x30-PREVIEW.jpg",
                                                quality=92)

print(f"canvas         : {W} x {H} px  ({W/DPI} x {H/DPI} in @ {DPI} DPI)")
print(f"QR modules     : {qr.modules_count}")
print(f"QR printed size: {qr_side/DPI:.2f} in  (was 8.00 in)")
print(f"QR panel      : {panel_w/DPI:.2f} x {(panel_bot-panel_top)/DPI:.2f} in")
print(f"QR module size : {qr_side/qr.modules_count/DPI*25.4:.2f} mm")
print(f"label cap size : {lab_size} px")
