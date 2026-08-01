"""Sticker generator — a die-cut laptop / promo sticker carrying the mark and
the website. Same brand system as the cards, coasters, and signage, so the
whole kit reads as one program.

Builds, into print/stickers/ (gitignored), an SVG and a true-size print-ready
PDF:
  sticker-laptop   the mark with the website fused onto the pin as one shape,
                   on a transparent ground — ~2.4 x 2.9 in. No border: the
                   printer adds the die-cut white border and bleed.

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

UPI = 120                       # sticker units per inch (~2.4 x 2.9 in overall)
SITE_UP = SITE_LABEL.upper()    # KNOXPICKMEUP.ORG


def laptop_sticker():
    """The mark with the website on a small navy pill fused to the pin's point,
    so the whole thing is ONE cohesive die-cut silhouette. No keyline / border —
    the printer adds the white die-cut border and bleed."""
    h = 300                              # the pin
    pin_top = 6
    pin_w = mark_w(h)
    _, url_w = text(inter6, SITE_UP, 15, 0, 0, GOLD, tracking=0.08)
    pill_w = url_w + 42
    pill_h = 46
    W = round(max(pin_w, pill_w) + 16)   # crop tight to the artwork
    cx = W / 2
    point_y = pin_top + h                # tip of the pin
    pill_y = point_y - 16                # fuse the pill onto the tip
    H = round(pill_y + pill_h + 8)
    b = [f'<rect x="{cx - pill_w/2}" y="{pill_y}" width="{pill_w}" height="{pill_h}" '
         f'rx="{pill_h/2}" fill="{NIGHT}"/>',
         mark(cx - pin_w / 2, pin_top, h, shield=NIGHT, cup=PAPER),
         text(inter6, SITE_UP, 15, cx, pill_y + pill_h / 2 + 5, GOLD,
              tracking=0.08, anchor='middle')[0]]
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
    print('Print as a die-cut (or kiss-cut) vinyl sticker, ~2.4 x 2.9 in, on a '
          'transparent ground — the shop adds the white die-cut border and bleed. '
          'Type is outlined, so no fonts are needed at the shop.')


if __name__ == '__main__':
    main()
