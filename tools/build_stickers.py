"""Sticker generator — promo stickers for laptops, water bottles, and
notebooks, from the same brand system as the cards, coasters, and signage.

Builds, into print/stickers/ (gitignored), an SVG and a true-size print-ready
PDF for each. Both sit on a transparent ground with NO border — the printer
cuts to the outline and adds the white die-cut border and bleed:
  sticker-mark       just the mark, big (~4 in tall). The pin tip stays visible.
  sticker-wordmark   a bold, left-aligned typographic lockup — name, orange
                     rule, tagline, website — that die-cuts to the lettering.

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
    PAPER, NIGHT, ORANGE, ORANGE_INK, INK2, GOLD, SITE_LABEL, text, svg, mark,
    mark_w, write_pdf, fraunces, fraunces_it, inter6,
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
    """A bold, left-aligned typographic lockup on a transparent ground — no
    plate/box, so the sticker die-cuts to the lettering. The name stacked big,
    a chunky orange rule, the tagline, and the website."""
    pad = 8
    x = pad
    b = []
    y = 60
    _, w1 = text(fraunces, 'Knox', 68, x, y, NIGHT)
    b.append(_)
    y += 66
    _, w2 = text(fraunces, 'Pick-Me-Up', 68, x, y, NIGHT)
    b.append(_)
    y += 26
    b.append(f'<rect x="{x + 2}" y="{y}" width="104" height="8" rx="1" fill="{ORANGE}"/>')
    y += 46
    _, w3 = text(fraunces_it, 'Ride from last call to first cup.', 29, x, y, NIGHT)
    b.append(_)
    y += 36
    _, w4 = text(inter6, SITE_UP, 18, x + 2, y, ORANGE_INK, tracking=0.16)
    b.append(_)
    W = round(max(w1, w2, w3, w4) + 2 * pad)
    H = round(y + 12)
    upi = max(1, round(W / 3.4))         # ~3.4 in wide
    return svg(W, H, ''.join(b), f'Knox Pick-Me-Up sticker — {SITE_LABEL}'), upi


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
