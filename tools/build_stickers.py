"""Sticker generator — promo stickers for laptops, water bottles, and
notebooks, from the same brand system as the cards, coasters, and signage.

Builds, into print/stickers/ (gitignored), an SVG and a true-size print-ready
PDF for each. Both sit on a transparent ground with NO border — the printer
cuts to the outline and adds the white die-cut border and bleed:
  sticker-mark       just the mark, big (~4 in tall). The pin tip stays visible.
  sticker-wordmark   the name, tagline, and website set on a navy rounded plate
                     (~3.6 x 1.5 in).

All type is converted to outlines, so any sticker shop can run the files as-is.

Usage:
  pip install fonttools brotli uharfbuzz segno cairosvg
  python3 tools/build_stickers.py
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_collateral import (  # noqa: E402
    PAPER, NIGHT, GOLD, SITE_LABEL, text, svg, mark, mark_w, write_pdf,
    fraunces, fraunces_it, inter6,
)

SITE_UP = SITE_LABEL.upper()    # KNOXPICKMEUP.ORG


def mark_sticker():
    """Just the mark, large, on a transparent ground — the whole pin (tip and
    all) is the die-cut shape. ~4 in tall at 105 units/in."""
    h = 400
    pad = 10
    W = round(mark_w(h) + 2 * pad)
    H = round(h + 2 * pad)
    body = mark(pad, pad, h, shield=NIGHT, cup=PAPER)
    return svg(W, H, body, f'Knox Pick-Me-Up mark sticker — die-cut'), 105


def wordmark_sticker():
    """The name, tagline, and website on a navy rounded plate — a clean
    typographic sticker. ~3.6 x 1.5 in at 200 units/in."""
    W, H, cx = 720, 300, 360
    b = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="42" fill="{NIGHT}"/>',
         text(fraunces, 'Knox Pick-Me-Up', 54, cx, 120, PAPER, anchor='middle')[0],
         text(fraunces_it, 'Ride from last call to first cup.', 26, cx, 170, GOLD,
              anchor='middle')[0],
         f'<line x1="{cx-72}" y1="202" x2="{cx+72}" y2="202" stroke="{GOLD}" '
         f'stroke-width="1.5" opacity="0.55"/>',
         text(inter6, SITE_UP, 18, cx, 240, GOLD, tracking=0.20, anchor='middle')[0]]
    return svg(W, H, ''.join(b), f'Knox Pick-Me-Up sticker — {SITE_LABEL}'), 200


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', default=os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'print', 'stickers'))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    pieces = {
        'sticker-mark.svg': mark_sticker(),
        'sticker-wordmark.svg': wordmark_sticker(),
    }
    for name, (body, upi) in pieces.items():
        svg_f = os.path.join(args.out, name)
        open(svg_f, 'w').write(body)
        write_pdf(body, svg_f[:-4] + '.pdf', upi)   # true-size print-ready PDF
        print(f'{name:22s} -> {svg_f}  (+ .pdf)')
    print('Print as die-cut (or kiss-cut) vinyl on a transparent ground — the '
          'shop cuts to the outline and adds the white border + bleed. Type is '
          'outlined, so no fonts are needed at the shop.')


if __name__ == '__main__':
    main()
