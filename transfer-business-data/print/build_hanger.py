from PIL import Image, ImageDraw, ImageFont

# Real vendor template: 3.6252 x 8.6252in @ 300dpi (includes bleed)
W, H = 1088, 2588
BLACK = (12, 13, 15)
NEAR_BLACK = (20, 21, 24)
WHITE = (246, 246, 244)
ACCENT = (47, 168, 232)
GRAY = (154, 154, 150)
DARKTEXT = (42, 42, 40)
CX = W // 2

# Vendor die-line safe zone, measured from pt-93ab03e90db54a5e9af6e402686043d6.ai:
# magenta safe rect = x[54,1032] y[835,2531] at 300dpi. The die-cut hole sits
# above y~835 — that whole top band must stay empty on both front and back.
SAFE_TOP = 852
SAFE_BOTTOM = 2508
LMARGIN = 114
SAFE_W = W - LMARGIN * 2  # 860

def pt(p): return round(p * 300 / 72)

FONT_PATHS = {
    "bold": "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "black": "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    "reg": "/System/Library/Fonts/Supplemental/Arial.ttf",
    "it": "/System/Library/Fonts/Supplemental/Arial Italic.ttf",
}
def font(weight, size_pt):
    return ImageFont.truetype(FONT_PATHS[weight], pt(size_pt))

def text_w(draw, text, fnt, spacing=0):
    if spacing:
        return sum(draw.textlength(ch, font=fnt) + spacing for ch in text) - spacing
    return draw.textlength(text, font=fnt)

def center_text(draw, cx, y, text, fnt, fill, spacing=0):
    if spacing:
        w = text_w(draw, text, fnt, spacing)
        x = cx - w / 2
        for ch in text:
            draw.text((x, y), ch, font=fnt, fill=fill)
            x += draw.textlength(ch, font=fnt) + spacing
    else:
        w = draw.textlength(text, font=fnt)
        draw.text((cx - w / 2, y), text, font=fnt, fill=fill)

def fit_size(draw, text, weight, start_pt, max_w, spacing=0, min_pt=8):
    size = start_pt
    while size > min_pt:
        f = font(weight, size)
        if text_w(draw, text, f, spacing) <= max_w:
            return f, size
        size -= 0.5
    return font(weight, min_pt), min_pt

def draw_fit_line(draw, cx, y, text, weight, start_pt, max_w, fill, spacing=0):
    f, size = fit_size(draw, text, weight, start_pt, max_w, spacing)
    center_text(draw, cx, y, text, f, fill, spacing)
    return pt(size)

def wrap_lines(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=fnt) <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def draw_paragraph(draw, cx, y, text, weight, size_pt, max_w, fill, line_gap=8):
    f = font(weight, size_pt)
    lines = wrap_lines(draw, text, f, max_w)
    lh = pt(size_pt) + line_gap
    for ln in lines:
        center_text(draw, cx, y, ln, f, fill)
        y += lh
    return y

def cover_crop(im, target_w, target_h, focus=0.35):
    src_ratio = im.width / im.height
    tgt_ratio = target_w / target_h
    if src_ratio > tgt_ratio:
        new_h = im.height
        new_w = int(new_h * tgt_ratio)
        left = (im.width - new_w) // 2
        im = im.crop((left, 0, left + new_w, new_h))
    else:
        new_w = im.width
        new_h = int(new_w / tgt_ratio)
        top = int((im.height - new_h) * focus)
        im = im.crop((0, top, new_w, top + new_h))
    return im.resize((target_w, target_h), Image.LANCZOS)

PHONE = "(256) 588-9948"
