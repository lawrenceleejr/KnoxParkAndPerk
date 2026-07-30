"""Regenerate brand collateral (logo, card, coaster, palette) with outlined type.

Usage: pip install fonttools brotli uharfbuzz segno cairosvg && python3 tools/build_collateral.py
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
NIGHT_RULE = '#2a3550'   # hairline on night fields (card back + night coaster)

# canonical site + QR target — imported by every generator so the URL lives
# in exactly one place. Printed QRs land on the shop map (#findus), never the
# partner-recruitment section.
SITE = 'https://knoxpickmeup.org/'
SITE_LABEL = 'knoxpickmeup.org'
FINDUS = SITE + '#findus'

# ---- mark extraction (from assets/mark.svg) ----
# The mark is a badge: a navy (#101a30) shield with a white (#ffffff) coffee
# cup drawn on top. Two tokens carry the whole thing — recolor the shield and
# the cup independently so it reads on any background (navy shield + paper cup
# on light; paper shield + navy cup on dark).
mark_src = open(f'{REPO}/assets/mark.svg').read()
MARK_BODY = re.search(r'<svg[^>]*>(.*)</svg>', mark_src, re.S).group(1).strip()
MARK_X, MARK_Y, MARK_W, MARK_H = 0, 0, 171.89, 189.79

def mark(x, y, h, shield=NIGHT, cup=PAPER):
    s = h / MARK_H
    body = MARK_BODY.replace('#101a30', shield).replace('#ffffff', cup)
    return (f'<g transform="translate({x - MARK_X*s:.2f},{y - MARK_Y*s:.2f}) scale({s:.5f})">'
            f'{body}</g>')

def mark_w(h):
    return h / MARK_H * MARK_W

def text(face, s, size, x, y, fill, tracking=0.0, anchor='start'):
    d, w = face.shape(s, size, letterspacing=tracking)
    if anchor == 'middle': x -= w/2
    elif anchor == 'end': x -= w
    return f'<path transform="translate({x:.2f},{y:.2f})" fill="{fill}" d="{d}"/>', w

def arc_text(face, s, size, cx, cy, R, fill, tracking=0.12, mode='top', center_deg=0.0, cap=0.72):
    """Per-glyph text along a circle, vertically CENTERED on radius R (so the
    band it occupies is symmetric about R, top and bottom arcs matching).
    mode top: reads clockwise across the top; mode bottom: across the bottom,
    glyphs upright (tops toward center). `cap` is the cap-height/size ratio
    used to center the glyphs — glyphs are drawn baseline-at-origin, so a
    downward shift of cap*size/2 puts their optical center on R."""
    voff = cap * size / 2
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
                       f'<path transform="translate({-w/2:.2f},{voff:.2f})" fill="{fill}" d="{d}"/></g>')
        dist += w + track
    return ''.join(out)

def svg(vb_w, vb_h, body, label):
    label = label.replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quot;')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w} {vb_h}" '
            f'role="img" aria-label="{label}">\n{body}\n</svg>\n')


def write_pdf(svg_str, path, upi):
    """Write a print-ready, true-size vector PDF from an SVG string.
    `upi` is the artwork's user-units-per-inch, so the PDF prints at the right
    physical size (all type is already outlined, so the file is self-contained
    and needs no fonts at the shop). Requires `pip install cairosvg`."""
    import cairosvg
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg_str)
    w, h = float(m.group(1)), float(m.group(2))
    sized = svg_str.replace('<svg ', f'<svg width="{w / upi:.4f}in" height="{h / upi:.4f}in" ', 1)
    cairosvg.svg2pdf(bytestring=sized.encode('utf-8'), write_to=path)


def embed_svg(path, h):
    """Inline an arbitrary SVG (a sponsor/partner logo) scaled to height `h`,
    positioned with its top-left at (0,0). Returns (fragment, width) — wrap the
    fragment in your own translate() to place it. Needs a viewBox or width/height
    on the root."""
    src = open(path).read()
    m = re.search(r'viewBox="([\d.eE+\- ,]+)"', src)
    if m:
        vx, vy, vw, vh = (float(v) for v in m.group(1).replace(',', ' ').split())
    else:
        mw = re.search(r'<svg[^>]*\swidth="([\d.]+)', src)
        mh = re.search(r'<svg[^>]*\sheight="([\d.]+)', src)
        if not (mw and mh):
            raise SystemExit(f'{path}: logo SVG needs a viewBox (or width/height)')
        vx, vy, vw, vh = 0.0, 0.0, float(mw.group(1)), float(mh.group(1))
    inner = re.sub(r'^.*?<svg[^>]*>', '', src, count=1, flags=re.S).rsplit('</svg>', 1)[0]
    s = h / vh
    frag = f'<g transform="translate({-vx*s:.2f},{-vy*s:.2f}) scale({s:.5f})">{inner}</g>'
    return frag, vw * s


def place(frag, x, y):
    """Wrap an embed_svg fragment in a translate to (x, y)."""
    return f'<g transform="translate({x:.2f},{y:.2f})">{frag}</g>'


def sponsor_row(cx, y_mid, path, label, label_fill, h=15):
    """A centered 'LABEL [logo-on-white-chip]' row — the sponsor slot used on
    the card back and the coaster. The white chip keeps any logo legible on
    navy or paper; the program mark is never touched."""
    frag, w = embed_svg(path, h)
    pad = 5
    boxw, boxh = w + pad * 2, h + pad * 2
    lbl_path, lbl_w = text(inter6, label, 7, 0, 0, label_fill, tracking=0.14)
    gap = 9
    total = lbl_w + gap + boxw
    x0 = cx - total / 2
    out = [text(inter6, label, 7, x0, y_mid + 2.5, label_fill, tracking=0.14)[0]]
    bx, by = x0 + lbl_w + gap, y_mid - boxh / 2
    out.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{boxw:.1f}" height="{boxh:.1f}" '
               f'rx="3" fill="#ffffff" stroke="{RULE}" stroke-width="0.8"/>')
    out.append(place(frag, bx + pad, by + pad))
    return ''.join(out)

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
    # navy shield + paper cup on light backgrounds; flip both so the badge
    # reads on dark (paper shield + navy cup)
    body.append(mark(mx, my, mh,
                     shield=(PAPER if dark_bg else NIGHT),
                     cup=(NIGHT if dark_bg else PAPER)))
    w1_path, w1 = text(fraunces, 'Knox Pick-Me-Up', 58, tx, 88, ink)
    body.append(w1_path)
    t_path, tw = text(fraunces_it, 'Ride from last call to first cup.', 21, tx+2, 124, accent)
    body.append(t_path)
    l_path, lw = text(inter6, 'DOWNTOWN KNOXVILLE, TENNESSEE', 11, tx+2, 156, sub_ink, tracking=0.22)
    body.append(l_path)
    W = math.ceil(tx + max(w1, tw, lw) + 12)
    return svg(W, H, ''.join(body),
               'Knox Pick-Me-Up — Ride from last call to first cup. Downtown Knoxville, Tennessee')

def build_lockups():
    open(f'{REPO}/assets/logo.svg', 'w').write(lockup(INK, ORANGE_INK, INK2))
    open(f'{REPO}/assets/logo-dark.svg', 'w').write(lockup(PAPER, GOLD, '#b9b3a4', dark_bg=True))

# =====================================================================
# 2. Morning Pick-Me-Up card (525 x 300)
# =====================================================================
# The spec card shows a real, working QR: like every printed card, it encodes
# the public site URL with this sample's serial embedded.
import io, segno
from serials import DEMO_KEY, derive_ck_key, serial_letter

SAMPLE_SERIAL = 'KPMU-2026-00004217' + serial_letter('KPMU-2026-00004217',
                                                     derive_ck_key(DEMO_KEY))

def qr_svg(data, x, y, size, color=NIGHT, error='m'):
    q = segno.make(data, error=error, micro=False)
    buf = io.BytesIO()
    q.save(buf, kind='svg', xmldecl=False, svgns=False, border=0)
    d = re.search(r'<path[^>]* d="([^"]+)"', buf.getvalue().decode()).group(1)
    n = q.symbol_size(border=0)[0]
    return (f'<g transform="translate({x},{y}) scale({size / n:.5f})">'
            f'<path stroke="{color}" d="{d}"/></g>')

def qr_modules(data, error='m'):
    """Modules per side for `data` — lets callers size the mandatory 4-module
    quiet zone from the actual QR version rather than a guess."""
    return segno.make(data, error=error, micro=False).symbol_size(border=0)[0]

def quiet_pad(data, size, error='m', modules=4):
    """User-unit width of a `modules`-wide quiet zone for a QR drawn at `size`."""
    return modules * size / qr_modules(data, error)

def build_card_sample():
    # assets/card.svg is reference art, not a separate design: it is the exact
    # production card face (build_cards.card_svg) rendered with a demo-key
    # sample serial, so it can never drift from what the print run emits.
    from build_cards import card_svg
    open(f'{REPO}/assets/card.svg', 'w').write(card_svg(SAMPLE_SERIAL))

# =====================================================================
# 3. Coaster (420 x 420)
# =====================================================================
def build_coaster_sample():
    # assets/coaster.svg is a distinct one-sided brand swatch, NOT the
    # two-sided print coaster — that lives in tools/build_coasters.py. This
    # single face just shows the mark + rim + a decision line for the brand
    # sheet; don't treat it as a print master.
    c = []
    cx = cy = 210
    c.append(f'<circle cx="{cx}" cy="{cy}" r="204" fill="{PAPER}" stroke="{RULE}" stroke-width="1.5"/>')
    c.append(f'<circle cx="{cx}" cy="{cy}" r="192" fill="none" stroke="{INK}" stroke-width="2"/>')
    c.append(f'<circle cx="{cx}" cy="{cy}" r="158" fill="none" stroke="{RULE}" stroke-width="1"/>')
    c.append(arc_text(inter6, 'KNOX PICK-ME-UP', 15, cx, cy, 175, INK, tracking=0.32, mode='top'))
    c.append(arc_text(inter6, 'FREE LARGE COFFEE · HAIR OF THE KAT', 12, cx, cy, 172, ORANGE_INK, tracking=0.26, mode='bottom'))
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
def build_palette():
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

# =====================================================================
# 5. Favicon (64 x 64) and emblem badge (240 x 240)
# =====================================================================
# Both seal the mark in a night badge, so the navy shield is recolored to
# paper (with a navy cup) — the badge carries the identity at any tab size.
def badge_pin(side, h):
    x = (side - mark_w(h)) / 2
    y = (side - h) / 2
    return mark(x, y, h, shield=PAPER, cup=NIGHT)

def build_favicon():
    fav = ('<defs><linearGradient id="fav-bg" x1="0" y1="0" x2="0" y2="1">'
           f'<stop offset="0%" stop-color="{NIGHT}"/><stop offset="100%" stop-color="{NIGHT2}"/></linearGradient></defs>'
           f'<rect x="1.5" y="1.5" width="61" height="61" rx="15" fill="url(#fav-bg)" stroke="{GOLD}" stroke-width="2.5"/>'
           + badge_pin(64, 46))
    open(f'{REPO}/assets/favicon.svg', 'w').write(svg(64, 64, fav, 'Knox Pick-Me-Up favicon'))

def build_emblem():
    emblem = ('<defs><linearGradient id="badge-m" x1="0" y1="0" x2="0" y2="1">'
              f'<stop offset="0%" stop-color="{NIGHT}"/><stop offset="100%" stop-color="{NIGHT2}"/></linearGradient></defs>'
              f'<circle cx="120" cy="120" r="112" fill="url(#badge-m)" stroke="{GOLD}" stroke-width="5"/>'
              f'<circle cx="120" cy="120" r="96" fill="none" stroke="{GOLD}" stroke-width="1" opacity=".4"/>'
              + badge_pin(240, 168))
    open(f'{REPO}/assets/logo-mark.svg', 'w').write(svg(240, 240, emblem, 'Knox Pick-Me-Up emblem'))

# =====================================================================
# 6. Social share card (1200 x 630) — the og:image for link previews
# =====================================================================
# Emitted as SVG here (deterministic, no extra deps for the regenerate
# workflow); the raster assets/og-image.png that scrapers actually read is
# rendered from this SVG with cairosvg — see tools/build_og_png.py.
def build_og():
    W, H, cx = 1200, 630, 600
    b = [('<defs><linearGradient id="og-bg" x1="0" y1="0" x2="0" y2="1">'
          f'<stop offset="0%" stop-color="{NIGHT}"/><stop offset="100%" stop-color="{NIGHT2}"/></linearGradient></defs>'),
         f'<rect width="{W}" height="{H}" fill="url(#og-bg)"/>',
         f'<rect x="26" y="26" width="{W-52}" height="{H-52}" fill="none" stroke="{GOLD}" stroke-width="2" opacity="0.5"/>',
         f'<rect x="26" y="26" width="{W-52}" height="10" fill="{ORANGE}"/>']
    # the badge mark — paper shield, navy cup, so it reads on the night field
    b.append(mark(cx - mark_w(150) / 2, 84, 150, shield=PAPER, cup=NIGHT))
    b.append(text(fraunces, 'Knox Pick-Me-Up', 78, cx, 330, PAPER, anchor='middle')[0])
    b.append(text(fraunces_it, 'Ride from last call to first cup.', 32, cx, 384, GOLD, anchor='middle')[0])
    b.append(f'<line x1="{cx-150}" y1="432" x2="{cx+150}" y2="432" stroke="{GOLD}" stroke-width="1" opacity="0.5"/>')
    b.append(text(inter6, 'FREE COFFEE FOR A SAFE RIDE HOME', 23, cx, 486, PAPER, tracking=0.16, anchor='middle')[0])
    b.append(text(inter6, 'DOWNTOWN KNOXVILLE · KNOXPICKMEUP.ORG', 15, cx, 556, '#b9b3a4', tracking=0.2, anchor='middle')[0])
    open(f'{REPO}/assets/og-image.svg', 'w').write(
        svg(W, H, ''.join(b), 'Knox Pick-Me-Up — free coffee for a safe ride home, downtown Knoxville'))

def build_all():
    build_lockups()
    build_card_sample()
    build_coaster_sample()
    build_palette()
    build_favicon()
    build_emblem()
    build_og()
    print('collateral built')


if __name__ == '__main__':
    build_all()
