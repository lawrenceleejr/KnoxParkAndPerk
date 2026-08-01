"""Sticker generator — small promo stickers for laptops, water bottles, and
notebooks, carrying the mark and the website. Same brand system as the cards,
coasters, and signage, so the whole kit reads as one program.

Builds, into print/stickers/ (gitignored), an SVG and a true-size print-ready
PDF for each:
  sticker-round-navy    3 in round badge, night navy — for dark laptops/cases.
  sticker-round-paper   3 in round badge, warm paper — for light surfaces.
  sticker-die           die-cut mark (the pin silhouette) with the website on a
                        small paper chip — cut to the outline.
  sticker-bar           3.5 x 1.25 in rounded bar, for a laptop lid.

Every sticker carries knoxpickmeup.org. All type is converted to outlines, so
any sticker shop can run the files as-is.

Usage:
  pip install fonttools brotli uharfbuzz segno cairosvg
  python3 tools/build_stickers.py
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_collateral import (  # noqa: E402
    PAPER, NIGHT, NIGHT2, INK, INK2, ORANGE_INK, GOLD, RULE,
    SITE_LABEL, text, arc_text, svg, mark, mark_w, write_pdf,
    fraunces, fraunces_it, inter6,
)

UPI = 200                 # sticker units per inch (round = 600 units = 3 in)
SITE_UP = SITE_LABEL.upper()   # KNOXPICKMEUP.ORG


# ------------------------------------------------------------------ round badge
def round_sticker(dark):
    """A 3-inch round badge: the mark in the center, KNOX PICK-ME-UP arced over
    the top, the website arced across the bottom, tagline beneath the mark."""
    S, cx = 600, 300
    if dark:
        bg, ring, shield, cup = NIGHT, GOLD, PAPER, NIGHT
        wm, url, tag = GOLD, PAPER, GOLD
    else:
        bg, ring, shield, cup = PAPER, NIGHT, NIGHT, PAPER
        wm, url, tag = ORANGE_INK, INK, INK2

    b = [f'<circle cx="{cx}" cy="{cx}" r="290" fill="{bg}" stroke="{ring}" stroke-width="7"/>',
         f'<circle cx="{cx}" cy="{cx}" r="256" fill="none" stroke="{ring}" '
         f'stroke-width="1.5" opacity="0.45"/>']
    # arced wordmark (top) and website (bottom), centered on the same radius
    b.append(arc_text(inter6, 'KNOX PICK-ME-UP', 25, cx, cx, 272, wm, tracking=0.30, mode='top'))
    b.append(arc_text(inter6, SITE_UP, 20, cx, cx, 272, url, tracking=0.24, mode='bottom'))
    # small dots at 3 and 9 o'clock separating the two arcs
    for sx in (cx - 272, cx + 272):
        b.append(f'<circle cx="{sx}" cy="{cx}" r="4.5" fill="{ring}"/>')
    # the mark, sitting a touch above center to leave room for the tagline
    h = 188
    b.append(mark(cx - mark_w(h) / 2, 150, h, shield=shield, cup=cup))
    b.append(text(fraunces_it, 'Ride from last call to first cup.', 21, cx, 402,
                  tag, anchor='middle')[0])
    return svg(S, S, ''.join(b),
               f'Knox Pick-Me-Up round sticker — {SITE_LABEL}')


# --------------------------------------------------------------- die-cut mark
def die_sticker():
    """The mark itself as a die-cut sticker (cut to the pin outline), with the
    website on a small paper chip tucked under it. A white keyline around both
    shapes is the cut path."""
    W, H = 360, 470
    cx = W / 2
    keyline = '#ffffff'
    b = []
    # die-cut keyline: a fat white outline of the mark + chip reads as the cut
    h = 300
    mx = cx - mark_w(h) / 2
    # white halo behind the mark (slightly larger mark drawn in white)
    hh = h + 15
    b.append(mark(cx - mark_w(hh) / 2, 8, hh, shield=keyline, cup=keyline))
    b.append(mark(mx, 20, h, shield=NIGHT, cup=PAPER))
    # website chip — sized to the text so it never clips
    url_path, url_w = text(inter6, SITE_UP, 17, 0, 0, GOLD, tracking=0.10)
    chip_h, chip_y = 58, 356
    chip_w = url_w + 56
    b.append(f'<rect x="{cx - chip_w/2 - 6}" y="{chip_y - 6}" width="{chip_w + 12}" '
             f'height="{chip_h + 12}" rx="{chip_h/2 + 6}" fill="{keyline}"/>')
    b.append(f'<rect x="{cx - chip_w/2}" y="{chip_y}" width="{chip_w}" height="{chip_h}" '
             f'rx="{chip_h/2}" fill="{NIGHT}"/>')
    b.append(text(inter6, SITE_UP, 17, cx, chip_y + chip_h / 2 + 6, GOLD,
                  tracking=0.10, anchor='middle')[0])
    return svg(W, H, ''.join(b),
               f'Knox Pick-Me-Up die-cut sticker — {SITE_LABEL}')


# ------------------------------------------------------------------- lid bar
def bar_sticker():
    """A 3.5 x 1.25 in rounded bar for a laptop lid: mark on the left, wordmark,
    tagline, and website stacked on the right."""
    W, H = 700, 250
    b = [f'<rect x="4" y="4" width="{W-8}" height="{H-8}" rx="34" fill="{NIGHT}"/>',
         f'<rect x="16" y="16" width="{W-32}" height="{H-32}" rx="24" fill="none" '
         f'stroke="{GOLD}" stroke-width="1.5" opacity="0.5"/>']
    h = 150
    b.append(mark(52, (H - h) / 2, h, shield=PAPER, cup=NIGHT))
    tx = 210
    b.append(text(fraunces, 'Knox Pick-Me-Up', 40, tx, 108, PAPER)[0])
    b.append(text(fraunces_it, 'Ride from last call to first cup.', 19, tx, 146, GOLD)[0])
    b.append(text(inter6, SITE_UP, 15, tx + 2, 182, GOLD, tracking=0.18)[0])
    return svg(W, H, ''.join(b),
               f'Knox Pick-Me-Up lid sticker — {SITE_LABEL}')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', default=os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'print', 'stickers'))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    pieces = {
        'sticker-round-navy.svg': round_sticker(dark=True),
        'sticker-round-paper.svg': round_sticker(dark=False),
        'sticker-die.svg': die_sticker(),
        'sticker-bar.svg': bar_sticker(),
    }
    for name, body in pieces.items():
        svg_f = os.path.join(args.out, name)
        open(svg_f, 'w').write(body)
        write_pdf(body, svg_f[:-4] + '.pdf', UPI)   # true-size print-ready PDF
        print(f'{name:24s} -> {svg_f}  (+ .pdf)')
    print('Print as die-cut or kiss-cut vinyl stickers at ~3 in (round) or '
          '3.5 in wide (bar). Print-ready PDFs sit beside each SVG; all type is '
          'outlined, so no fonts are needed at the shop.')


if __name__ == '__main__':
    main()
