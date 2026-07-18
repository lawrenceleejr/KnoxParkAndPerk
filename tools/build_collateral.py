"""Regenerate brand collateral (logo, card, coaster, palette) with outlined type.

Usage: pip install fonttools brotli uharfbuzz && python3 tools/build_collateral.py
"""
import math, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from text2path import Face

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = f'{REPO}/assets/fonts'
fraunces = Face(f'{F}/fraunces-600-normal-9.woff2')
fraunces_it = Face(f'{F}/fraunces-400-italic-3.woff2')
inter6 = Face(f'{F}/inter-600-normal-30.woff2')
inter4 = Face(f'{F}/inter-400-normal-16.woff2')

# tokens
PAPER   = '#faf5eb'
PAPER2  = '#f2e9d8'
INK     = '#241a10'
INK2    = '#6f5f4c'
NIGHT   = '#101a30'
NIGHT2  = '#0a101f'
ORANGE  = '#ff8200'
ORANGE_INK = '#b04e00'
GOLD    = '#eda953'
RULE    = '#ddcfb4'

# ---- mark extraction (from assets/mark.svg) ----
mark_src = open(f'{REPO}/assets/mark.svg').read()
groups = re.findall(r'<g .*?</g>', mark_src, re.S)
dark_g, orange_g = groups[0], groups[1]
MARK_X, MARK_Y, MARK_W, MARK_H = 14.96, 43.85, 556.4, 490.32

def mark(x, y, h, dark=INK, orange=ORANGE):
    s = h / MARK_H
    g_dark = dark_g.replace('fill="currentColor"', f'fill="{dark}"')
    g_or = orange_g.replace('fill="#ff8200"', f'fill="{orange}"')
    return (f'<g transform="translate({x - MARK_X*s:.2f},{y - MARK_Y*s:.2f}) scale({s:.5f})">'
            f'{g_dark}{g_or}</g>')

def mark_w(h):
    return h / MARK_H * MARK_W

def text(face, s, size, x, y, fill, tracking=0.0, anchor='start'):
    d, w = face.shape(s, size, letterspacing=tracking)
    if anchor == 'middle': x -= w/2
    elif anchor == 'end': x -= w
    return f'<path transform="translate({x:.2f},{y:.2f})" fill="{fill}" d="{d}"/>', w

def arc_text(face, s, size, cx, cy, R, fill, tracking=0.12, mode='top', center_deg=0.0):
    """Per-glyph text along a circle. mode top: baseline circle R, reads clockwise across top.
    mode bottom: reads across bottom, glyphs upright (tops toward center)."""
    widths = []
    for ch in s:
        _, w = face.shape(ch, size)
        widths.append(w)
    track = tracking * size
    total = sum(widths) + track * (len(s)-1)
    out = []
    dist = -total/2
    for ch, w in zip(s, widths):
        mid = dist + w/2
        ang = mid / R  # radians along arc
        deg = math.degrees(ang) + center_deg
        if ch != ' ':
            d, _ = face.shape(ch, size)
            if mode == 'top':
                px = cx + R*math.sin(math.radians(deg))
                py = cy - R*math.cos(math.radians(deg))
                rot = deg
            else:
                px = cx + R*math.sin(math.radians(deg))
                py = cy + R*math.cos(math.radians(deg))
                rot = -deg
            out.append(f'<g transform="translate({px:.2f},{py:.2f}) rotate({rot:.2f})">'
                       f'<path transform="translate({-w/2:.2f},0)" fill="{fill}" d="{d}"/></g>')
        dist += w + track
    return ''.join(out)

def svg(vb_w, vb_h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w} {vb_h}" '
            f'role="img" aria-label="{label}">\n{body}\n</svg>\n')

# =====================================================================
# 1. Logo lockups
# =====================================================================
def lockup(ink, accent, sub_ink, dark_bg=None):
    H = 200
    mh = 128
    mx, my = 10, (H-mh)/2 - 4
    tx = mx + mark_w(mh) + 34
    body = []
    if dark_bg:
        pass  # transparent background; consumer places on dark
    body.append(mark(mx, my, mh, dark=ink, orange=ORANGE))
    w1_path, w1 = text(fraunces, 'Knox Pick-Me-Up', 58, tx, 88, ink)
    body.append(w1_path)
    t_path, tw = text(fraunces_it, 'Make it home safe. Tomorrow’s coffee’s on us.', 21, tx+2, 124, accent)
    body.append(t_path)
    l_path, lw = text(inter6, 'DOWNTOWN KNOXVILLE, TENNESSEE', 11, tx+2, 156, sub_ink, tracking=0.22)
    body.append(l_path)
    W = math.ceil(tx + max(w1, tw, lw) + 12)
    return svg(W, H, ''.join(body),
               'Knox Pick-Me-Up — Make it home safe. Tomorrow’s coffee’s on us. Downtown Knoxville, Tennessee')

open(f'{REPO}/assets/logo.svg', 'w').write(lockup(INK, ORANGE_INK, INK2))
open(f'{REPO}/assets/logo-dark.svg', 'w').write(lockup(PAPER, GOLD, '#b9b3a4', dark_bg=True))

# =====================================================================
# 2. Morning Pick-Me-Up card (525 x 300)
# =====================================================================
card_src = open(f'{REPO}/assets/card.svg').read()
qr = re.search(r'<g transform="translate\(404,106\) scale\(2\.49\)">.*?</g>', card_src, re.S).group(0)
qr = qr.replace('stroke="#141d33"', f'stroke="{NIGHT}"')

b = []
b.append(f'<rect x="1" y="1" width="523" height="298" rx="14" fill="{PAPER}" stroke="{RULE}" stroke-width="1.5"/>')
b.append(f'<path d="M15 1.75 H510 a13 13 0 0 1 13.25 13.25 V22 H1.75 V15 A13 13 0 0 1 15 1.75 Z" fill="{ORANGE}"/>')
# header
b.append(mark(26, 40, 40))
b.append(text(fraunces, 'Knox Pick-Me-Up', 23, 82, 68, INK)[0])
b.append(text(inter6, 'MORNING PICK-ME-UP CARD', 9, 499, 64, ORANGE_INK, tracking=0.18, anchor='end')[0])
b.append(f'<line x1="26" y1="92" x2="499" y2="92" stroke="{RULE}" stroke-width="1"/>')
# offer
b.append(text(fraunces, 'Free large coffee', 36, 26, 148, INK)[0])
b.append(text(fraunces_it, 'You made the safe call. The morning’s on us.', 14.5, 27, 174, INK2)[0])
bullets = [
    'One large coffee at participating downtown shops',
    'Free KAT bus rides while this card is valid',
    'One per ride · Not for resale · No cash value',
]
for i, t in enumerate(bullets):
    y = 202 + i*19
    b.append(f'<rect x="27" y="{y-3.5}" width="7" height="1.5" fill="{ORANGE}"/>')
    b.append(text(inter4, t, 11, 42, y, INK2)[0])
# QR
b.append(f'<rect x="398" y="104" width="102" height="102" rx="4" fill="#ffffff" stroke="{RULE}" stroke-width="1"/>')
b.append(f'<g transform="translate(5.4,9)">{qr}</g>')
b.append(text(inter6, 'SCAN FOR PARTICIPATING', 6.8, 449, 222, INK2, tracking=0.16, anchor='middle')[0])
b.append(text(inter6, 'BUSINESSES', 6.8, 449, 233, INK2, tracking=0.16, anchor='middle')[0])
# validity + serial
b.append(f'<line x1="26" y1="252" x2="499" y2="252" stroke="{RULE}" stroke-width="1"/>')
b.append(text(inter6, 'VALID FOR ONE DAY FROM', 9.5, 26, 274, INK, tracking=0.14)[0])
b.append(f'<line x1="190" y1="276" x2="310" y2="276" stroke="{INK2}" stroke-width="1"/>')
b.append(text(inter4, 'Nº KPU-2026-004217', 9.5, 499, 274, INK2, tracking=0.04, anchor='end')[0])
open(f'{REPO}/assets/card.svg', 'w').write(
    svg(525, 300, ''.join(b), 'Knox Pick-Me-Up — Morning Pick-Me-Up Card, good for a free large coffee and free KAT rides'))

# =====================================================================
# 3. Coaster (420 x 420)
# =====================================================================
c = []
cx = cy = 210
c.append(f'<circle cx="{cx}" cy="{cy}" r="204" fill="{PAPER}" stroke="{RULE}" stroke-width="1.5"/>')
c.append(f'<circle cx="{cx}" cy="{cy}" r="192" fill="none" stroke="{INK}" stroke-width="2"/>')
c.append(f'<circle cx="{cx}" cy="{cy}" r="158" fill="none" stroke="{RULE}" stroke-width="1"/>')
c.append(arc_text(inter6, 'KNOX PICK-ME-UP', 15, cx, cy, 175, INK, tracking=0.32, mode='top'))
c.append(arc_text(inter6, 'FREE LARGE COFFEE · FREE KAT RIDE', 12, cx, cy, 172, ORANGE_INK, tracking=0.26, mode='bottom'))
# side dots
for sdeg in (90, 270):
    px = cx + 175*math.sin(math.radians(sdeg))
    py = cy - 175*math.cos(math.radians(sdeg))
    c.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.6" fill="{ORANGE}"/>')
# center
c.append(mark(cx - mark_w(96)/2, 92, 96))
c.append(text(fraunces, 'Booked your ride home?', 27, cx, 250, INK, anchor='middle')[0])
c.append(text(fraunces, 'Show your bartender.', 27, cx, 284, INK, anchor='middle')[0])
c.append(text(fraunces_it, 'Tomorrow’s coffee’s on us.', 18, cx, 318, ORANGE_INK, anchor='middle')[0])
open(f'{REPO}/assets/coaster.svg', 'w').write(
    svg(420, 420, ''.join(c), 'Knox Pick-Me-Up coaster — Booked your ride home? Show your bartender. Tomorrow’s coffee’s on us.'))

# =====================================================================
# 4. Palette (900 x 360)
# =====================================================================
swatches = [
    ('Paper',        PAPER,  INK,  True),
    ('Paper Deep',   PAPER2, INK,  True),
    ('Ink',          INK,    PAPER, False),
    ('Umber',        INK2,   PAPER, False),
    ('Night',        NIGHT,  PAPER, False),
    ('Night Deep',   NIGHT2, PAPER, False),
    ('Sunrise',      ORANGE, NIGHT2, False),
    ('Sunrise Ink',  ORANGE_INK, PAPER, False),
]
p = [f'<rect width="900" height="360" fill="{PAPER}"/>']
p.append(text(inter6, 'KNOX PICK-ME-UP · COLOR', 12, 40, 52, INK, tracking=0.22)[0])
cw, ch, gx, gy = 195, 110, 12, 12
x0, y0 = 40, 80
for i, (name, hexv, on, border) in enumerate(swatches):
    col, row = i % 4, i // 4
    x, y = x0 + col*(cw+gx), y0 + row*(ch+gy)
    stroke = f' stroke="{RULE}" stroke-width="1"' if border else ''
    p.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="3" fill="{hexv}"{stroke}/>')
    p.append(text(inter6, name.upper(), 10, x+14, y+ch-34, on, tracking=0.14)[0])
    p.append(text(inter4, hexv.upper(), 10, x+14, y+ch-16, on)[0])
p.append(text(inter4, 'Type: Fraunces 600 (display) · Inter 400/500/600 (text) · Cormorant 700 old-style figures (statistics)', 11, 40, 336, INK2)[0])
open(f'{REPO}/assets/palette.svg', 'w').write(
    svg(900, 360, ''.join(p), 'Knox Pick-Me-Up color palette and type'))

print('collateral built')
