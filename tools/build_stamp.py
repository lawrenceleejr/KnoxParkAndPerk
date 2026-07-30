"""Bartender date-stamp die — the physical validity control.

At hand-out the bartender stamps today's date in the card's DATE ISSUED box;
that stamp is what starts the one-day window (PROGRAM.md, PRINTING.md). This
generates the round rubber-stamp DIE for the current badge mark, sized for a
standard 30 mm round self-inking dater (e.g. Trodat Printy 46030): a fixed top
plate (mark + KNOX PICK-ME-UP) and bottom plate (VALID ONE DAY), with the
center band left clear for the dater's own date wheel.

This replaces the retired design/proposals/concept-2-stamp.svg, which was drawn
for an identity two logos ago.

Units are 0.1 mm (300 u = 30 mm); the PDF exports true-size at 254 u/in.

Usage:
  pip install fonttools brotli uharfbuzz segno cairosvg
  python3 tools/build_stamp.py
"""
import argparse, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_collateral import (NIGHT, text, arc_text, svg, mark, mark_w,
                              write_pdf, inter6)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = 300              # 300 units = 30 mm die
UPI = 254            # 0.1 mm per unit -> 254 units per inch (true-size PDF)
CX = CY = 150
INKC = NIGHT         # one-color die; prints in whatever pad ink the shop uses


def stamp_die():
    b = [f'<circle cx="{CX}" cy="{CY}" r="143" fill="none" stroke="{INKC}" stroke-width="2.5"/>',
         f'<circle cx="{CX}" cy="{CY}" r="132" fill="none" stroke="{INKC}" stroke-width="1"/>']
    # top plate: arced wordmark at the very top, the mark (navy shield, knockout
    # cup) stacked below it — both clear of the date band
    b.append(arc_text(inter6, 'KNOX PICK-ME-UP', 14, CX, CY, 118, INKC, tracking=0.14, mode='top'))
    b.append(mark(CX - mark_w(34) / 2, 74, 34, shield=INKC, cup='#ffffff'))
    # center date band — left CLEAR for the dater's date wheel; hairlines bracket it
    b.append(f'<line x1="40" y1="128" x2="260" y2="128" stroke="{INKC}" stroke-width="1"/>')
    b.append(f'<line x1="40" y1="172" x2="260" y2="172" stroke="{INKC}" stroke-width="1"/>')
    # bottom plate
    b.append(arc_text(inter6, 'VALID ONE DAY', 13, CX, CY, 116, INKC, tracking=0.16, mode='bottom'))
    b.append(text(inter6, 'DATE ISSUED', 8, CX, 205, INKC, tracking=0.24, anchor='middle')[0])
    return svg(S, S, ''.join(b),
               'Knox Pick-Me-Up bartender date-stamp die — 30 mm round, mark + wordmark, '
               'centre band clear for the dater date wheel')


def main():
    ap = argparse.ArgumentParser(description='Build the Knox Pick-Me-Up bartender date-stamp die.')
    ap.add_argument('--out', default=os.path.join(REPO, 'print', 'stamp'), help='output directory')
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    body = stamp_die()
    svg_f = os.path.join(args.out, 'stamp-die.svg')
    open(svg_f, 'w').write(body)
    write_pdf(body, svg_f[:-4] + '.pdf', UPI)
    print(f'stamp-die.svg -> {svg_f}  (+ .pdf, true-size 30 mm round)')
    print('Spec: 30 mm round self-inking dater (e.g. Trodat Printy 46030). One '
          'colour; centre band stays clear for the date wheel. Line weights are '
          'the die minimum (~0.25 mm) — a stamp vendor can run the PDF as the '
          'custom text-plate art. See PRINTING.md.')


if __name__ == '__main__':
    main()
