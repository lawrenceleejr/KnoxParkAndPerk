"""Sponsor one-sheet — the outreach leave-behind for a business that wants to
underwrite the coffees and put its name on the safe ride home (PROGRAM.md
funding Model C). Letter-size, print-ready, generic; same brand system.

Builds print/sponsor/sponsor-one-sheet.svg (+ .pdf). It explains what a
sponsorship funds, where the logo rides (card backs + coasters, already in
every participating bar), the logo spec for those slots, and who to contact.

Usage:
  pip install fonttools brotli uharfbuzz segno cairosvg
  python3 tools/build_sponsor.py
"""
import argparse, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_collateral import (PAPER, INK, INK2, ORANGE, ORANGE_INK, GOLD, RULE,
                              SITE_LABEL, text, svg, write_pdf, inter4, inter6, fraunces_it)
from build_staff import frame, section_label, para, W, H, MARGIN, CONTACT


def sponsor_one_sheet():
    b, y = frame('SPONSORSHIP', 'Put your name on the safe ride home.')
    y = para(b, y + 6,
             'Knox Pick-Me-Up thanks people who line up a safe ride home downtown with a free '
             'coffee the next morning. A sponsorship underwrites those coffees — and rides on the '
             'materials already in every participating bar and coffee shop.', 15)
    y += 16

    y = section_label(b, y, 'WHAT A SPONSORSHIP FUNDS')
    y = para(b, y, 'The free large coffee and free KAT ride each card gives a patron who chose not '
                   'to drive. Every dollar goes to the offer, not overhead — the whole system runs '
                   'on free tools (see the program facts at knoxpickmeup.org).', 14)
    y += 14

    y = section_label(b, y, 'WHERE YOUR LOGO RIDES')
    for s in [
        'Card backs — a “printing donated by” slot on every Morning Pick-Me-Up card handed out at the bar.',
        'Coasters — the same slot on the two-sided coasters that sit on tables in every participating venue.',
        'The program mark always stays; your logo shares the piece, it never replaces it.',
    ]:
        b.append(f'<circle cx="{MARGIN+4}" cy="{y-4}" r="2.6" fill="{ORANGE}"/>')
        y = para(b, y, s, 14, indent=20) + 8
    y += 8

    y = section_label(b, y, 'LOGO SPEC')
    y = para(b, y, 'Send a vector SVG with a viewBox (or width/height). A single-color or high-contrast '
                   'logo reads best — it prints small and sits on a white chip so it stays legible on '
                   'the navy card back and the paper coaster alike. No alcohol-brand logos on these '
                   'patron-facing pieces (a program rule).', 14)
    y += 14

    y = section_label(b, y, 'TIERS & PLACEMENT')
    y = para(b, y, 'Placement runs by print wave (a wave is tens of thousands of coasters and cards). '
                   'Tiers scale with how many venues and waves your logo appears in — ask for the '
                   'current rate card; we’ll match a tier to your budget and print schedule.', 14)

    b.append(f'<line x1="{MARGIN}" y1="{H-104}" x2="{W-MARGIN}" y2="{H-104}" stroke="{RULE}" stroke-width="1"/>')
    section_label(b, H - 74, 'GET IN TOUCH')
    b.append(text(inter4, f'{CONTACT}  ·  {SITE_LABEL}  ·  A road-safety partnership with the City of Knoxville, KPD, and KAT.',
                  13, MARGIN, H - 48, INK2)[0])
    return svg(W, H, ''.join(b),
               'Knox Pick-Me-Up sponsorship one-sheet — what a sponsorship funds, where the logo rides, spec, and contact')


def main():
    ap = argparse.ArgumentParser(description='Build the Knox Pick-Me-Up sponsor one-sheet.')
    ap.add_argument('--out', default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'print', 'sponsor'),
                    help='output directory')
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    body = sponsor_one_sheet()
    svg_f = os.path.join(args.out, 'sponsor-one-sheet.svg')
    open(svg_f, 'w').write(body)
    write_pdf(body, svg_f[:-4] + '.pdf', 100)   # letter at 100 u/in
    print(f'sponsor-one-sheet.svg -> {svg_f}  (+ .pdf)')


if __name__ == '__main__':
    main()
