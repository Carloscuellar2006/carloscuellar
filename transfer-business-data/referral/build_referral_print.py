#!/usr/bin/env python3
"""Big Spring Cleaning Exteriors & Pressure Washing — referral print pieces.

  1. referral-sheet.pdf   8.5 x 11 in, 2 pages (leave-behind)
  2. referral-card.pdf    3.5 x 2 in trim + 0.125 bleed, 2 pages (front/back)

Style: gradient panels with layered water flow, rounded cards, icon tiles and
numbered steps — the structure of the trifold the client referenced, in Big
Spring's own identity. The rocket is a Huntsville nod, used once, small.

Pages are composed in RGBA (so card shadows composite properly) and flattened
to RGB on save.
"""
import math, os
from PIL import Image, ImageDraw, ImageFont
import qrcode
from qrcode.constants import ERROR_CORRECT_Q, ERROR_CORRECT_M

DPI = 300

NAVY   = (11, 46, 71)
DEEP   = (20, 88, 133)
BLUE   = (47, 168, 232)
SKY    = (126, 205, 245)
INK    = (12, 13, 15)
PAPER  = (255, 255, 255)
SHELL  = (240, 246, 250)
BODY   = (74, 85, 96)
MUTED  = (128, 141, 152)
RULE   = (222, 232, 239)
GREEN  = (24, 150, 100)
GREENB = (232, 248, 241)
BLUEB  = (232, 245, 253)

FB = "fonts/Archivo-Black.ttf"
FS = "fonts/Archivo-Bold.ttf"
IR = "fonts/Inter-Regular.ttf"
IM = "fonts/Inter-Medium.ttf"
IS = "fonts/Inter-SemiBold.ttf"

PHONE      = "(256) 677-5992"
BRAND_L1   = "BIG SPRING CLEANING EXTERIORS"
BRAND_L2   = "& PRESSURE WASHING"
# Both say "referral" so scans are attributable. /referral-card needs 37
# modules vs 33, so the card QR is printed larger to stay above ~0.6mm.
QR_SHEET   = "https://bigspringpressurewashing.com/referral"
QR_CARD    = "https://bigspringpressurewashing.com/referral-card"

LOGO_WHITE = ["logo/logo-mark-white-1024.png",
              "/Users/carloscuellar1/Desktop/pressure-washing-site/logo/logo-mark-white-1024.png"]
LOGO_BLUE  = ["logo/logo-mark-1024.png",
              "/Users/carloscuellar1/Desktop/pressure-washing-site/logo/logo-mark-1024.png"]
_warned = []


def inch(v): return int(round(v * DPI))
def F(p, s): return ImageFont.truetype(p, max(1, int(round(s))))
def cap(d, s, f): return d.textbbox((0, 0), s, font=f)


def draw(d, s, path, size, x, y, fill=INK, anchor="la", tracking=0):
    f = F(path, size)
    bb = cap(d, s, f)
    if tracking:
        w = sum(f.getlength(c) for c in s) + tracking * (len(s) - 1)
        if anchor[0] == "m": x -= w / 2
        elif anchor[0] == "r": x -= w
        cx = x
        for ch in s:
            d.text((cx, y - bb[1]), ch, font=f, fill=fill)
            cx += f.getlength(ch) + tracking
    else:
        ax = {"l": x, "m": x - f.getlength(s) / 2, "r": x - f.getlength(s)}[anchor[0]]
        d.text((ax, y - bb[1]), s, font=f, fill=fill)
    return y + (bb[3] - bb[1])


def wrap(d, s, path, size, max_w):
    f = F(path, size)
    lines, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if f.getlength(t) <= max_w: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines


def para(d, s, path, size, x, y, max_w, fill=BODY, leading=1.55, anchor="la"):
    f = F(path, size)
    for ln in wrap(d, s, path, size, max_w):
        ax = x if anchor == "la" else x - f.getlength(ln) / 2
        d.text((ax, y), ln, font=f, fill=fill)
        y += int(size * leading)
    return y


def qr_img(url, px, ec=ERROR_CORRECT_Q):
    q = qrcode.QRCode(error_correction=ec, box_size=30, border=0)
    q.add_data(url); q.make(fit=True)
    return (q.make_image(fill_color="black", back_color="white")
             .convert("RGB").resize((px, px), Image.NEAREST), q.modules_count)


def load_logo(px, white=False):
    for p in (LOGO_WHITE if white else LOGO_BLUE):
        if not os.path.exists(p): continue
        try:
            im = Image.open(p); im.load(); im = im.convert("RGBA")
        except Exception: continue
        sc = min(px / im.size[0], px / im.size[1])
        return im.resize((max(1, int(im.size[0]*sc)), max(1, int(im.size[1]*sc))),
                         Image.LANCZOS)
    if "miss" not in _warned:
        print("  !! logo not found — searched", LOGO_WHITE + LOGO_BLUE)
        _warned.append("miss")
    return None


# ---------------------------------------------------------------- styling --
def vgrad(im, box, c0, c1):
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    g = Image.new("RGB", (1, h))
    gd = ImageDraw.Draw(g)
    for i in range(h):
        t = i / max(1, h - 1)
        gd.point((0, i), fill=tuple(int(c0[k] + (c1[k] - c0[k]) * t) for k in range(3)))
    im.paste(g.resize((x1 - x0, h), Image.BILINEAR).convert("RGBA"), (x0, y0))


def waves(im, box, bands):
    """Layered sine bands — the water flow."""
    x0, y0, x1, y1 = box
    W, H = x1 - x0, y1 - y0
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    step = max(1, W // 260)
    for yf, amp, freq, col, alpha in bands:
        base = H * yf
        pts = [(x, base + amp * math.sin(freq * x / W * 2 * math.pi))
               for x in range(0, W + 1, step)]
        ld.polygon(pts + [(W, H + 4), (0, H + 4)], fill=col + (alpha,))
    im.alpha_composite(layer, (x0, y0))


def rcard(im, box, radius, fill, shadow=True, outline=None, ow=0):
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle(
            [box[0] + inch(0.025), box[1] + inch(0.045),
             box[2] + inch(0.025), box[3] + inch(0.045)],
            radius=radius, fill=(14, 42, 64, 30))
        im.alpha_composite(sh)
    ImageDraw.Draw(im).rounded_rectangle(box, radius=radius, fill=fill,
                                         outline=outline, width=ow)


def rocket(d, cx, cy, h, color, flame=None):
    """Small rocket glyph — Huntsville nod."""
    w = h * 0.42
    d.polygon([(cx, cy - h/2), (cx + w/2, cy - h*0.06), (cx + w/2, cy + h*0.30),
               (cx - w/2, cy + h*0.30), (cx - w/2, cy - h*0.06)], fill=color)
    d.ellipse([cx - w*0.19, cy - h*0.20, cx + w*0.19, cy + h*0.05], fill=PAPER)
    d.polygon([(cx - w/2, cy + h*0.04), (cx - w*1.00, cy + h*0.34),
               (cx - w/2, cy + h*0.30)], fill=color)
    d.polygon([(cx + w/2, cy + h*0.04), (cx + w*1.00, cy + h*0.34),
               (cx + w/2, cy + h*0.30)], fill=color)
    if flame:
        d.polygon([(cx - w*0.24, cy + h*0.30), (cx + w*0.24, cy + h*0.30),
                   (cx, cy + h*0.60)], fill=flame)


# --------------------------------------------------------- service glyphs --
def g_house(d, x, y, s, c):
    d.polygon([(x+s*.5, y+s*.16), (x+s*.86, y+s*.46), (x+s*.14, y+s*.46)], fill=c)
    d.rectangle([x+s*.26, y+s*.46, x+s*.74, y+s*.84], fill=c)

def g_roof(d, x, y, s, c):
    d.polygon([(x+s*.5, y+s*.20), (x+s*.90, y+s*.54), (x+s*.10, y+s*.54)], fill=c)
    d.rectangle([x+s*.12, y+s*.62, x+s*.88, y+s*.74], fill=c)

def g_drive(d, x, y, s, c):
    d.polygon([(x+s*.36, y+s*.16), (x+s*.64, y+s*.16),
               (x+s*.86, y+s*.84), (x+s*.14, y+s*.84)], fill=c)

def g_walk(d, x, y, s, c):
    for i in range(3):
        yy = y + s*(.20 + i*.24)
        d.rounded_rectangle([x+s*.18, yy, x+s*.82, yy+s*.14], radius=int(s*.05), fill=c)

def g_patio(d, x, y, s, c):
    for r in range(2):
        for col in range(2):
            d.rounded_rectangle([x+s*(.16+col*.36), y+s*(.16+r*.36),
                                 x+s*(.46+col*.36), y+s*(.46+r*.36)],
                                radius=int(s*.05), fill=c)

def g_window(d, x, y, s, c):
    w = max(2, int(s*.09))
    d.rounded_rectangle([x+s*.16, y+s*.16, x+s*.84, y+s*.84], radius=int(s*.08),
                        outline=c, width=w)
    d.line([(x+s*.5, y+s*.16), (x+s*.5, y+s*.84)], fill=c, width=w)
    d.line([(x+s*.16, y+s*.5), (x+s*.84, y+s*.5)], fill=c, width=w)

def g_gutter(d, x, y, s, c):
    d.polygon([(x+s*.12, y+s*.28), (x+s*.88, y+s*.28), (x+s*.88, y+s*.44),
               (x+s*.30, y+s*.44), (x+s*.30, y+s*.84), (x+s*.12, y+s*.84)], fill=c)

def g_fence(d, x, y, s, c):
    for i in range(4):
        xx = x + s*(.14 + i*.20)
        d.rounded_rectangle([xx, y+s*.18, xx+s*.10, y+s*.86], radius=int(s*.04), fill=c)
    d.rectangle([x+s*.10, y+s*.40, x+s*.90, y+s*.50], fill=c)

def g_lights(d, x, y, s, c):
    d.arc([x+s*.06, y+s*.08, x+s*.94, y+s*.70], start=200, end=340,
          fill=c, width=max(2, int(s*.08)))
    for fx, fy in ((.22, .46), (.5, .56), (.78, .46)):
        d.ellipse([x+s*(fx-.09), y+s*fy, x+s*(fx+.09), y+s*(fy+.20)], fill=c)


def chip(im, s_px, x, y, glyph, bg=BLUEB, fg=DEEP):
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x, y, x + s_px, y + s_px], radius=int(s_px * 0.26), fill=bg)
    glyph(d, x, y, s_px, fg)


def footer(im, W, H, M):
    vgrad(im, (0, H - inch(0.50), W, H), DEEP, NAVY)
    d = ImageDraw.Draw(im)
    rocket(d, M + inch(0.17), H - inch(0.25), inch(0.30), SKY, flame=BLUE)
    draw(d, f"HUNTSVILLE AND SURROUNDING AREAS   ·   {PHONE}", FS, inch(0.098),
         M + inch(0.44), H - inch(0.295), fill=PAPER, tracking=inch(0.012))


# ============================================================ SHEET PAGE 1 ==
def sheet_page1():
    W, H = inch(8.5), inch(11)
    im = Image.new("RGBA", (W, H), PAPER + (255,))
    M, CW = inch(0.58), W - inch(1.16)

    HDR = inch(3.05)
    vgrad(im, (0, 0, W, HDR), NAVY, DEEP)
    waves(im, (0, 0, W, HDR), [(0.62, inch(0.20), 1.4, SKY, 46),
                               (0.74, inch(0.16), 2.1, BLUE, 62),
                               (0.87, inch(0.13), 1.1, BLUE, 96)])
    d = ImageDraw.Draw(im)

    lg = load_logo(inch(0.84), white=True)
    if lg: im.alpha_composite(lg, (M, inch(0.38)))
    draw(d, BRAND_L1, FS, inch(0.105), M + inch(0.76), inch(0.50),
         fill=PAPER, tracking=inch(0.017))
    draw(d, BRAND_L2, FS, inch(0.105), M + inch(0.76), inch(0.695),
         fill=SKY, tracking=inch(0.017))

    draw(d, "Thanks for choosing", FB, inch(0.40), M, inch(1.32), fill=PAPER)
    draw(d, "Big Spring.", FB, inch(0.40), M, inch(1.86), fill=SKY)
    para(d, "Everything we clean, how often it needs doing, and how to get $25 off "
            "your next service.", IR, inch(0.145), M, inch(2.44), CW - inch(2.1),
         fill=(196, 222, 240))

    y = inch(3.42)
    draw(d, "EVERYTHING WE DO", FB, inch(0.175), M, y, fill=INK, tracking=inch(0.026))
    d.rounded_rectangle([M, y + inch(0.32), M + inch(0.72), y + inch(0.365)],
                        radius=inch(0.02), fill=BLUE)

    COLS = [
        ("EXTERIOR WASHING", [
            (g_house, "House Washing", "Soft wash that kills algae at the root."),
            (g_roof,  "Roof Washing",  "Black streaks and moss, safely removed."),
            (g_fence, "Fence & Deck",  "Weathered wood and vinyl, back to color."),
        ]),
        ("FLATWORK", [
            (g_drive, "Driveways",       "Red clay, oil, rust and traffic film."),
            (g_walk,  "Walkways",        "The path up to your front door."),
            (g_patio, "Patios & Porches","Pavers, concrete, steps and railings."),
        ]),
        ("ADD-ONS", [
            (g_window, "Window Cleaning", "Inside and out, screens included."),
            (g_gutter, "Gutter Cleaning", "Cleared before it stains the siding."),
            (g_lights, "Holiday Lights",  "Installed October, taken down after."),
        ]),
    ]
    col_w = (CW - inch(0.42)) // 3
    top = y + inch(0.66)
    for ci, (title, items) in enumerate(COLS):
        cx = M + ci * (col_w + inch(0.21))
        draw(d, title, FB, inch(0.102), cx, top, fill=DEEP, tracking=inch(0.017))
        cy = top + inch(0.30)
        for glyph, name, desc in items:
            chip(im, inch(0.42), cx, cy, glyph)
            d = ImageDraw.Draw(im)
            draw(d, name, IS, inch(0.132), cx + inch(0.55), cy + inch(0.02), fill=INK)
            para(d, desc, IR, inch(0.102), cx + inch(0.55), cy + inch(0.19),
                 col_w - inch(0.55))
            cy += inch(0.74)

    y = inch(6.86)
    rcard(im, [M, y, W - M, y + inch(2.10)], inch(0.14), SHELL + (255,), shadow=False)
    d = ImageDraw.Draw(im)
    draw(d, "HOW OFTEN IT NEEDS DOING", FB, inch(0.122), M + inch(0.32),
         y + inch(0.26), fill=INK, tracking=inch(0.022))
    FREQ = [("House wash", "every 1–2 years"), ("Roof wash", "every 2–3 years"),
            ("Driveway & flatwork", "every 1–2 years"), ("Windows", "2–4 times a year"),
            ("Gutters", "twice a year")]
    yy = y + inch(0.60)
    for i, (k, v) in enumerate(FREQ):
        ry = yy + i * inch(0.28)
        draw(d, k, IM, inch(0.126), M + inch(0.32), ry, fill=BODY)
        draw(d, v, IS, inch(0.126), W - M - inch(0.32), ry, fill=INK, anchor="ra")
        if i < len(FREQ) - 1:
            d.rectangle([M + inch(0.32), ry + inch(0.202),
                         W - M - inch(0.32), ry + inch(0.209)], fill=RULE)

    gy = inch(9.44)
    rcard(im, [M, gy, W - M, gy + inch(0.70)], inch(0.12), NAVY + (255,), shadow=False)
    d = ImageDraw.Draw(im)
    draw(d, "STAYS CLEAN 6 MONTHS, GUARANTEED", FB, inch(0.185), W // 2,
         gy + inch(0.18), fill=PAPER, anchor="ma")
    draw(d, "If algae or mildew comes back inside six months, we re-clean it free.",
         IR, inch(0.108), W // 2, gy + inch(0.44), fill=(150, 186, 214), anchor="ma")

    footer(im, W, H, M)
    return im


# ============================================================ SHEET PAGE 2 ==
def sheet_page2():
    W, H = inch(8.5), inch(11)
    im = Image.new("RGBA", (W, H), PAPER + (255,))
    M, CW = inch(0.58), W - inch(1.16)

    HDR = inch(3.50)
    vgrad(im, (0, 0, W, HDR), NAVY, DEEP)
    waves(im, (0, 0, W, HDR), [(0.66, inch(0.22), 1.2, SKY, 44),
                               (0.78, inch(0.17), 1.9, BLUE, 60),
                               (0.90, inch(0.13), 2.6, BLUE, 94)])
    d = ImageDraw.Draw(im)
    draw(d, "REFERRAL PROGRAM", FS, inch(0.108), W // 2, inch(0.46),
         fill=SKY, anchor="ma", tracking=inch(0.030))
    draw(d, "Give $25. Get $25.", FB, inch(0.50), W // 2, inch(0.88),
         fill=PAPER, anchor="ma")
    para(d, "Know a neighbor whose driveway could use the same treatment? "
            "Send them our way and you both come out ahead.",
         IR, inch(0.148), W // 2, inch(1.64), inch(5.2),
         fill=(196, 222, 240), anchor="ma")

    y = inch(2.44)
    hw = (CW - inch(0.20)) // 2
    for i, (bg, lab, labc, amt, note) in enumerate([
        (GREENB, "THEY GET", GREEN, "$25 off", "their first service with us"),
        (BLUEB,  "YOU GET",  DEEP,  "$25 off", "your next service — no limit"),
    ]):
        x = M + i * (hw + inch(0.20))
        rcard(im, [x, y, x + hw, y + inch(1.46)], inch(0.13), bg + (255,))
        d = ImageDraw.Draw(im)
        draw(d, lab, FB, inch(0.102), x + inch(0.26), y + inch(0.24),
             fill=labc, tracking=inch(0.020))
        draw(d, amt, FB, inch(0.32), x + inch(0.26), y + inch(0.50), fill=INK)
        para(d, note, IR, inch(0.116), x + inch(0.26), y + inch(1.00), hw - inch(0.52))

    # ---- cleaning spend converts to Christmas-light credit ----
    d = ImageDraw.Draw(im)
    by = inch(4.06)
    rcard(im, [M, by, W - M, by + inch(0.80)], inch(0.11), (255, 250, 240, 255),
          shadow=False, outline=(236, 207, 149), ow=inch(0.012))
    d = ImageDraw.Draw(im)
    g_lights(d, M + inch(0.20), by + inch(0.17), inch(0.38), (196, 132, 32))
    draw(d, "Your cleaning pays for your Christmas lights.", FB, inch(0.135),
         M + inch(0.72), by + inch(0.15), fill=(111, 74, 12))
    para(d, "Every dollar you spend on cleaning comes off your light install, dollar for "
            "dollar. Spend $500 and that's $500 off your lights.",
         IR, inch(0.108), M + inch(0.72), by + inch(0.36), W - M - inch(0.96),
         fill=(138, 101, 38))
    draw(d, "MAX CREDIT $500 PER HOUSEHOLD  ·  INSTALLS OCTOBER–DECEMBER", FS,
         inch(0.082), M + inch(0.72), by + inch(0.63), fill=(166, 132, 72),
         tracking=inch(0.010))

    y = inch(5.10)
    draw(d, "HOW IT WORKS", FB, inch(0.175), M, y, fill=INK, tracking=inch(0.026))
    d.rounded_rectangle([M, y + inch(0.32), M + inch(0.72), y + inch(0.365)],
                        radius=inch(0.02), fill=BLUE)
    STEPS = [
        ("Hand over a card, or send them online",
         "Give a neighbor one of your referral cards with your name on the back, "
         "or submit their details on our referral page."),
        ("They book — $25 comes off their first job",
         "Applied automatically when we invoice them. No code to remember, and "
         "we won't hound them."),
        ("You get $25 off your next service",
         "Credited the day their job is finished. No cap — send five neighbors "
         "and that's $125 off."),
    ]
    yy = y + inch(0.62)
    for i, (t, desc) in enumerate(STEPS):
        r = inch(0.20)
        d.ellipse([M, yy, M + r * 2, yy + r * 2], fill=BLUE)
        f = F(FB, inch(0.19))
        bb = cap(d, str(i + 1), f)
        d.text((M + r - f.getlength(str(i + 1)) / 2, yy + r - (bb[3] + bb[1]) / 2),
               str(i + 1), font=f, fill=PAPER)
        tx = M + inch(0.58)
        draw(d, t, IS, inch(0.152), tx, yy + inch(0.03), fill=INK)
        para(d, desc, IR, inch(0.120), tx, yy + inch(0.26), CW - inch(0.58))
        yy += inch(0.80)

    qy = inch(8.34)
    rcard(im, [M, qy, W - M, qy + inch(1.54)], inch(0.14), NAVY + (255,), shadow=False)
    q, mods = qr_img(QR_SHEET, inch(1.14))
    plate = Image.new("RGBA", (inch(1.28), inch(1.28)), PAPER + (255,))
    plate.paste(q, (inch(0.07), inch(0.07)))
    im.alpha_composite(plate, (M + inch(0.22), qy + inch(0.13)))
    d = ImageDraw.Draw(im)
    tx = M + inch(1.68)
    draw(d, "REFER SOMEONE IN 30 SECONDS", FB, inch(0.122), tx, qy + inch(0.26),
         fill=SKY, tracking=inch(0.020))
    para(d, "Scan the code, or just call or text and say who you're sending.",
         IR, inch(0.116), tx, qy + inch(0.52), W - M - tx - inch(0.22),
         fill=(184, 212, 232))
    draw(d, PHONE, FB, inch(0.225), tx, qy + inch(0.96), fill=PAPER)

    para(d, "Referral credit applies once the referred job is completed and paid. Credit has no "
            "cash value and can't be applied to an invoice already settled. One $25 credit per "
            "referred household. Your credit doesn't expire. Christmas light credit: cleaning "
            "spend is credited dollar for dollar toward a light installation, up to $500 per "
            "household, on installs booked October–December. No cash value. Referral credits "
            "and cleaning-spend credit cannot exceed $500 combined.",
         IR, inch(0.088), M, inch(9.98), CW, fill=MUTED, leading=1.48)

    footer(im, W, H, M)
    return im, mods


# ================================================================== CARDS ===
BLEED, TW, TH = 0.125, 3.5, 2.0
CWp, CHp = inch(TW + 2 * BLEED), inch(TH + 2 * BLEED)


def card_front():
    im = Image.new("RGBA", (CWp, CHp), NAVY + (255,))
    vgrad(im, (0, 0, CWp, CHp), NAVY, DEEP)
    waves(im, (0, 0, CWp, CHp), [(0.56, inch(0.10), 1.3, SKY, 40),
                                 (0.70, inch(0.08), 2.0, BLUE, 56),
                                 (0.85, inch(0.06), 1.1, BLUE, 88)])
    d = ImageDraw.Draw(im)
    lg = load_logo(inch(0.44), white=True)
    if lg: im.alpha_composite(lg, (int(CWp/2 - lg.size[0]/2), inch(0.28)))
    draw(d, BRAND_L1, FS, inch(0.066), CWp // 2, inch(0.78), fill=PAPER,
         anchor="ma", tracking=inch(0.017))
    draw(d, BRAND_L2, FS, inch(0.066), CWp // 2, inch(0.885), fill=SKY,
         anchor="ma", tracking=inch(0.017))
    draw(d, "$25 OFF", FB, inch(0.50), CWp // 2, inch(1.08), fill=PAPER, anchor="ma")
    draw(d, "YOUR FIRST CLEAN", FB, inch(0.122), CWp // 2, inch(1.74),
         fill=SKY, anchor="ma", tracking=inch(0.030))
    return im


def card_back():
    im = Image.new("RGBA", (CWp, CHp), PAPER + (255,))
    vgrad(im, (0, 0, CWp, inch(0.60)), NAVY, DEEP)
    waves(im, (0, 0, CWp, inch(0.60)), [(0.70, inch(0.05), 1.6, BLUE, 78)])
    d = ImageDraw.Draw(im)
    draw(d, "HOW IT WORKS", FB, inch(0.096), inch(0.32), inch(0.25),
         fill=PAPER, tracking=inch(0.024))
    rocket(d, CWp - inch(0.34), inch(0.30), inch(0.25), SKY, flame=BLUE)

    # At error-correction Q this URL needs 37 modules = 0.60mm each, right on
    # the print floor and flaky in testing. Level M gets it to 33 modules =
    # 0.68mm, which scans far more reliably on a card. Quiet zone must also be
    # >= 4 modules (~0.11in) or readers fail to lock on.
    q, mods = qr_img(QR_CARD, inch(0.88), ec=ERROR_CORRECT_M)
    qx, qy = CWp - inch(1.14), inch(0.70)
    d.rounded_rectangle([qx - inch(0.11), qy - inch(0.11),
                         qx + inch(0.99), qy + inch(0.99)],
                        radius=inch(0.06), fill=PAPER + (255,))
    im.paste(q, (qx, qy))

    tx, y = inch(0.32), inch(0.80)
    for i, s in enumerate(["Call or text us with this card",
                           "Book any exterior cleaning",
                           "$25 comes off your invoice"]):
        r = inch(0.070)
        d.ellipse([tx, y, tx + r * 2, y + r * 2], fill=BLUE)
        f = F(FB, inch(0.080))
        bb = cap(d, str(i + 1), f)
        d.text((tx + r - f.getlength(str(i + 1)) / 2, y + r - (bb[3] + bb[1]) / 2),
               str(i + 1), font=f, fill=PAPER)
        draw(d, s, IM, inch(0.092), tx + inch(0.21), y + inch(0.010), fill=INK)
        y += inch(0.202)

    ly = inch(1.66)
    draw(d, "REFERRED BY", FS, inch(0.066), tx, ly, fill=MUTED, tracking=inch(0.018))
    d.rectangle([tx + inch(0.72), ly + inch(0.080),
                 CWp - inch(1.34), ly + inch(0.090)], fill=RULE)
    draw(d, PHONE, FB, inch(0.126), tx, ly + inch(0.182), fill=DEEP)
    return im, mods


# =================================================================== build ==
p1 = sheet_page1().convert("RGB")
_p2, sm = sheet_page2()
p2 = _p2.convert("RGB")
p1.save("referral-sheet-p1.png", dpi=(DPI, DPI))
p2.save("referral-sheet-p2.png", dpi=(DPI, DPI))
p1.save("referral-sheet.pdf", "PDF", resolution=float(DPI), save_all=True,
        append_images=[p2])

cf = card_front().convert("RGB")
_cb, cm = card_back()
cb = _cb.convert("RGB")
cf.save("referral-card-front.png", dpi=(DPI, DPI))
cb.save("referral-card-back.png", dpi=(DPI, DPI))
cf.save("referral-card.pdf", "PDF", resolution=float(DPI), save_all=True,
        append_images=[cb])

for im, n in ((p1, "referral-sheet-p1"), (p2, "referral-sheet-p2")):
    im.resize((850, 1100), Image.LANCZOS).save(f"{n}-PREVIEW.jpg", quality=92)
for im, n in ((cf, "referral-card-front"), (cb, "referral-card-back")):
    small = im.resize((1125, 675), Image.LANCZOS)
    small.save(f"{n}-PREVIEW.jpg", quality=94)
    g = small.copy(); gd = ImageDraw.Draw(g); s = 1125 / 3.75
    gd.rectangle([0.125*s, 0.125*s, 3.625*s, 2.125*s], outline=(255, 64, 64), width=3)
    gd.rectangle([0.25*s, 0.25*s, 3.5*s, 2.0*s], outline=(255, 190, 60), width=2)
    g.save(f"{n}-TRIM.jpg", quality=94)

print(f"SHEET  8.50 x 11.00 in, 2 pages  ({p1.size[0]}x{p1.size[1]}px @ {DPI}dpi)")
print(f"CARD   {TW} x {TH} in trim + {BLEED} bleed  ({CWp}x{CHp}px)")
print(f"QR     sheet {sm} modules @1.14in ({1.14/sm*25.4:.2f}mm) · "
      f"card {cm} modules @0.88in ({0.88/cm*25.4:.2f}mm, level M)")
