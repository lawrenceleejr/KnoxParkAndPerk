"""Two-sided coaster generator — the night side and the day side of the story.

NIGHT side (faces up under the drink, at the bar): the participating BARS run
around the rim, and the center walks the patron through the decision they're
about to make — leave the car overnight, book a ride home, free coffee when
they come back for it in the morning.

DAY side (the flip): the participating COFFEE SHOPS run around the rim, with
a QR to the program site in the center — where the card gets redeemed.

Venue lists, the QR target, and the center logo are all configurable; with no
flags it builds a sample pair from the demo roster using the brand mark.

Usage:
  pip install fonttools brotli uharfbuzz segno
  python3 tools/build_coasters.py \
      --bars "Preservation Pub, Barley's Taproom, Suttree's" \
      --shops "Remedy Coffee, Wild Love Bakehouse, K Brew" \
      --logo path/to/sponsor-or-partner-logo.svg \
      --qr-url https://lawrenceleejr.github.io/KnoxParkAndPerk/

Outputs print/coasters/coaster-night.svg and coaster-day.svg (gitignored —
print artifacts). All type is converted to outlines, like every other piece
of collateral, so any print shop can run the files as-is. Coaster spec is in
PRINTING.md (pulpboard, 3.5-4 in round, flat color).
"""
import argparse, io, math, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import segno
from build_collateral import (PAPER, INK, INK2, NIGHT, NIGHT2, ORANGE,
                              ORANGE_INK, GOLD, RULE, text, arc_text, svg,
                              mark, mark_w, fraunces, fraunces_it,
                              inter6, inter4)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://lawrenceleejr.github.io/KnoxParkAndPerk/'

# geometry — 420 units = 4 in round coaster (105 units/in)
W = 420
CX = CY = 210
R_EDGE, R_RING, R_INNER, R_NAMES = 204, 192, 158, 175
NIGHT_RULE = '#2a3550'   # hairline on the night field (matches the card back)


def qr_group(data, x, y, size, color=NIGHT):
    q = segno.make(data, error='m', micro=False)
    buf = io.BytesIO()
    q.save(buf, kind='svg', xmldecl=False, svgns=False, border=0)
    d = re.search(r'<path[^>]* d="([^"]+)"', buf.getvalue().decode()).group(1)
    n = q.symbol_size(border=0)[0]
    return (f'<g transform="translate({x},{y}) scale({size / n:.5f})">'
            f'<path stroke="{color}" d="{d}"/></g>')


def embed_svg(path, cx, top_y, h):
    """Inline an arbitrary SVG file scaled to height h, horizontally centered
    on cx with its top at top_y. Needs a viewBox (or width/height) on the
    root element."""
    src = open(path).read()
    m = re.search(r'viewBox="([\d.eE+\- ,]+)"', src)
    if m:
        vx, vy, vw, vh = (float(v) for v in m.group(1).replace(',', ' ').split())
    else:
        mw = re.search(r'<svg[^>]*\swidth="([\d.]+)', src)
        mh = re.search(r'<svg[^>]*\sheight="([\d.]+)', src)
        if not (mw and mh):
            raise SystemExit(f'{path}: the logo SVG needs a viewBox (or width/height)')
        vx, vy, vw, vh = 0.0, 0.0, float(mw.group(1)), float(mh.group(1))
    inner = re.sub(r'^.*?<svg[^>]*>', '', src, count=1, flags=re.S).rsplit('</svg>', 1)[0]
    s = h / vh
    x = cx - vw * s / 2
    return (f'<g transform="translate({x - vx * s:.2f},{top_y - vy * s:.2f}) scale({s:.5f})">'
            f'{inner}</g>')


def logo(cx, top_y, h, logo_path, on_dark):
    """Center logo slot: the supplied SVG if configured, else the brand mark
    in the side's ink (paper silhouette on night, ink on paper)."""
    if logo_path:
        return embed_svg(logo_path, cx, top_y, h)
    return mark(cx - mark_w(h) / 2, top_y, h, dark=(PAPER if on_dark else INK))


def chord(y, pad=16):
    """Usable line width inside the inner ring at baseline y."""
    dy = y - CY
    return 2 * math.sqrt(max(R_INNER * R_INNER - dy * dy, 0)) - pad


def fit(face, s, size, max_w, tracking=0.0, min_size=8):
    """Largest size <= the requested one at which s fits in max_w."""
    while size > min_size and face.shape(s, size, letterspacing=tracking)[1] > max_w:
        size -= 0.25
    return size


NAME_TRACK = 0.18  # letterspacing for rim names (em fraction, matches labels)


def _arc_w(face, s, size):
    ws = [face.shape(ch, size)[1] for ch in s]
    return sum(ws) + NAME_TRACK * size * (len(s) - 1)


def ring_names(names, face, base_size, fill, dot, max_arc_deg=152):
    """Venue names around the rim: first half across the top arc, the rest
    across the bottom (both reading upright), separated by accent dots.
    Auto-shrinks until each group fits its arc."""
    names = [n.upper() for n in names]
    split = math.ceil(len(names) / 2)
    out = []
    for group, mode in ((names[:split], 'top'), (names[split:], 'bottom')):
        if not group:
            continue
        size = base_size
        while True:
            widths = [_arc_w(face, n, size) for n in group]
            gap = size * 2.4                      # arc px between names
            total = sum(widths) + gap * (len(group) - 1)
            if math.degrees(total / R_NAMES) <= max_arc_deg or size <= 8:
                break
            size -= 0.5
        if math.degrees(total / R_NAMES) > max_arc_deg:
            print(f'WARNING: {len(group)} names do not fit the {mode} arc even at '
                  f'{size}px — consider shorter names or fewer venues per coaster')
        deg = -math.degrees(total / R_NAMES) / 2  # group centered on the arc
        for i, (name, w) in enumerate(zip(group, widths)):
            wdeg = math.degrees(w / R_NAMES)
            out.append(arc_text(face, name, size, CX, CY, R_NAMES, fill,
                                tracking=NAME_TRACK, mode=mode,
                                center_deg=deg + wdeg / 2))
            if i < len(group) - 1:               # dot in the middle of the gap
                mid = math.radians(deg + wdeg + math.degrees(gap / R_NAMES) / 2)
                px = CX + R_NAMES * math.sin(mid)
                py = CY - R_NAMES * math.cos(mid) if mode == 'top' else CY + R_NAMES * math.cos(mid)
                out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.4" fill="{dot}"/>')
            deg += wdeg + math.degrees(gap / R_NAMES)
    return ''.join(out)


def night_side(bars, logo_path):
    """The bar side: navy field, bars around the rim, the three steps in the
    center — written for someone already out, deciding what to do about the
    car."""
    b = []
    b.append(f'<circle cx="{CX}" cy="{CY}" r="{R_EDGE}" fill="{NIGHT}" stroke="{NIGHT2}" stroke-width="1.5"/>')
    b.append(f'<circle cx="{CX}" cy="{CY}" r="{R_RING}" fill="none" stroke="{ORANGE}" stroke-width="2"/>')
    b.append(f'<circle cx="{CX}" cy="{CY}" r="{R_INNER}" fill="none" stroke="{NIGHT_RULE}" stroke-width="1"/>')
    b.append(ring_names(bars, inter6, 13, GOLD, ORANGE))
    b.append(logo(CX, 72, 46, logo_path, on_dark=True))
    hsz = fit(fraunces, 'Drove downtown tonight?', 23, chord(148))
    b.append(text(fraunces, 'Drove downtown tonight?', hsz, CX, 152, PAPER, anchor='middle')[0])
    steps = [
        'Leave the car — municipal garages are free overnight.',
        'Book a ride home. Show your bartender.',
        'Free coffee when you’re back in the morning.',
    ]
    # the whole block fits the tightest of its three rows, numeral included
    indent, ssz = 20, 11.5
    row_w = min(chord(186 + i * 28) for i in range(len(steps)))
    ssz = min(fit(inter4, s, ssz, row_w - indent) for s in steps)
    x0 = CX - (max(inter4.shape(s, ssz)[1] for s in steps) + indent) / 2
    for i, s in enumerate(steps):
        y = 186 + i * 28
        b.append(text(fraunces, str(i + 1), 19, x0, y, ORANGE)[0])
        b.append(text(inter4, s, ssz, x0 + indent, y - 2, PAPER)[0])
    b.append(text(fraunces_it, 'Ride from last call to first call.', 14, CX, 292, GOLD, anchor='middle')[0])
    return svg(W, W, ''.join(b),
               'Knox Pick-Me-Up coaster, night side — leave the car overnight, '
               'book a ride home, free coffee in the morning; participating bars around the rim')


def day_side(shops, logo_path, qr_url):
    """The morning side: paper field, coffee shops around the rim, and the
    QR to the program site in the center."""
    b = []
    b.append(f'<circle cx="{CX}" cy="{CY}" r="{R_EDGE}" fill="{PAPER}" stroke="{RULE}" stroke-width="1.5"/>')
    b.append(f'<circle cx="{CX}" cy="{CY}" r="{R_RING}" fill="none" stroke="{INK}" stroke-width="2"/>')
    b.append(f'<circle cx="{CX}" cy="{CY}" r="{R_INNER}" fill="none" stroke="{RULE}" stroke-width="1"/>')
    b.append(ring_names(shops, inter6, 13, INK, ORANGE))
    b.append(logo(CX, 70, 40, logo_path, on_dark=False))
    b.append(text(fraunces, 'Back for your car?', 23, CX, 142, INK, anchor='middle')[0])
    sub = 'That card is a free large coffee — and your KAT fare.'
    b.append(text(fraunces_it, sub, fit(fraunces_it, sub, 12.5, chord(160)), CX, 164, ORANGE_INK, anchor='middle')[0])
    if qr_url:
        b.append(f'<rect x="{CX - 48}" y="182" width="96" height="96" rx="4" fill="#ffffff" stroke="{RULE}" stroke-width="1"/>')
        b.append(qr_group(qr_url, CX - 40, 190, 80))
        # 9 units ≈ 6.5pt at 4in — the floor for print legibility
        b.append(text(inter6, 'SCAN FOR SHOPS, HOURS + THE PROGRAM', 9, CX, 299, INK2, tracking=0.16, anchor='middle')[0])
    else:
        b.append(text(fraunces, 'knoxpickmeup.org', 20, CX, 234, INK, anchor='middle')[0])
        b.append(text(inter6, 'SHOPS, HOURS + THE PROGRAM', 9, CX, 262, INK2, tracking=0.16, anchor='middle')[0])
    b.append(text(inter4, 'knoxpickmeup.org', 10, CX, 317, INK2, anchor='middle')[0])
    return svg(W, W, ''.join(b),
               'Knox Pick-Me-Up coaster, day side — free large coffee with your card; '
               'participating coffee shops around the rim, QR to the program site')


def split_list(s):
    return [v.strip() for v in s.split(',') if v.strip()]


def main():
    ap = argparse.ArgumentParser(description='Build the two-sided Knox Pick-Me-Up coaster.')
    ap.add_argument('--bars', default='Preservation Pub, Barley’s Taproom, Suttree’s, '
                                      'Peter Kern Library, Boyd’s Jig & Reel',
                    help='comma-separated bars for the night-side rim')
    ap.add_argument('--shops', default='Remedy Coffee, Wild Love Bakehouse, K Brew, Honeybee Coffee',
                    help='comma-separated coffee shops for the day-side rim')
    ap.add_argument('--logo', default='',
                    help='path to an SVG to use as the center logo on both sides '
                         '(default: the brand mark, in each side’s ink)')
    ap.add_argument('--qr-url', default=f'{SITE}#partners',
                    help='URL the day-side QR encodes; pass an empty string to '
                         'print the site name instead of a QR')
    ap.add_argument('--out', default=os.path.join(REPO, 'print', 'coasters'),
                    help='output directory')
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    night_f = os.path.join(args.out, 'coaster-night.svg')
    day_f = os.path.join(args.out, 'coaster-day.svg')
    open(night_f, 'w').write(night_side(split_list(args.bars), args.logo))
    open(day_f, 'w').write(day_side(split_list(args.shops), args.logo, args.qr_url))
    print(f'night side (bars, the three steps)      -> {night_f}')
    print(f'day side (shops, QR to the program)     -> {day_f}')
    print('Print as a 4 in round, 2-sided pulpboard coaster — see PRINTING.md.')


if __name__ == '__main__':
    main()
