"""Sticker generator — a die-cut laptop / promo sticker carrying the mark and
the website. Same brand system as the cards, coasters, and signage, so the
whole kit reads as one program.

Builds, into print/stickers/ (gitignored), an SVG and a true-size print-ready
PDF:
  sticker-laptop   die-cut mark (the pin silhouette) with the website on a
                   small chip below — cut to the outline. ~2.4 x 3.1 in.

All type is converted to outlines, so any sticker shop can run the file as-is.

Usage:
  pip install fonttools brotli uharfbuzz segno cairosvg
  python3 tools/build_stickers.py
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_collateral import (  # noqa: E402
    PAPER, NIGHT, GOLD, SITE_LABEL, text, svg, mark, mark_w, write_pdf, inter6,
)

UPI = 150                       # sticker units per inch (360 wide ≈ 2.4 in)
SITE_UP = SITE_LABEL.upper()    # KNOXPICKMEUP.ORG


def laptop_sticker():
    """The mark as a die-cut sticker (cut to the pin outline), with the website
    on a small navy chip tucked under it. A white keyline around both shapes is
    the cut path."""
    W, H = 360, 470
    cx = W / 2
    keyline = '#ffffff'
    b = []
    # the mark, with a white halo behind it (a slightly larger mark in white)
    h = 300
    b.append(mark(cx - mark_w(h + 15) / 2, 8, h + 15, shield=keyline, cup=keyline))
    b.append(mark(cx - mark_w(h) / 2, 20, h, shield=NIGHT, cup=PAPER))
    # website chip — sized to the text so it never clips
    _, url_w = text(inter6, SITE_UP, 17, 0, 0, GOLD, tracking=0.10)
    chip_h, chip_y = 58, 356
    chip_w = url_w + 56
    b.append(f'<rect x="{cx - chip_w/2 - 6}" y="{chip_y - 6}" width="{chip_w + 12}" '
             f'height="{chip_h + 12}" rx="{chip_h/2 + 6}" fill="{keyline}"/>')
    b.append(f'<rect x="{cx - chip_w/2}" y="{chip_y}" width="{chip_w}" height="{chip_h}" '
             f'rx="{chip_h/2}" fill="{NIGHT}"/>')
    b.append(text(inter6, SITE_UP, 17, cx, chip_y + chip_h / 2 + 6, GOLD,
                  tracking=0.10, anchor='middle')[0])
    return svg(W, H, ''.join(b),
               f'Knox Pick-Me-Up die-cut laptop sticker — {SITE_LABEL}')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', default=os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'print', 'stickers'))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    name = 'sticker-laptop.svg'
    body = laptop_sticker()
    svg_f = os.path.join(args.out, name)
    open(svg_f, 'w').write(body)
    write_pdf(body, svg_f[:-4] + '.pdf', UPI)   # true-size print-ready PDF
    print(f'{name:20s} -> {svg_f}  (+ .pdf)')
    print('Print as a die-cut (or kiss-cut) vinyl sticker, ~2.4 x 3.1 in. The '
          'PDF is true-size with type outlined, so no fonts are needed at the shop.')


if __name__ == '__main__':
    main()
