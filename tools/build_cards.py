"""Batch-generate print-ready Morning Pick-Me-Up cards and pack cover sheets.

Each card gets a unique serial and a unique QR. The QR encodes a URL on the
public site with the serial embedded (?c=KPU-...#partners):
  - a PATRON who scans it lands on the participating-businesses section;
  - a SHOP scanning it from redeem.html has the serial read straight off it.

Each pack of PACK_SIZE cards gets a cover sheet whose QR opens the pack
check-out Google Form pre-filled with the pack's serial range, so whoever
hands the pack to a bar just scans it and picks the bar from a dropdown.

Usage:
  pip install fonttools brotli uharfbuzz segno
  python3 tools/build_cards.py --year 2026 --start 1 --count 100
Outputs to print/cards/ and print/packs/ (gitignored — print artifacts).
See design/LOGGING.md for the full system.
"""
import argparse, io, math, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import segno
from build_collateral import (PAPER, INK, INK2, NIGHT, ORANGE, ORANGE_INK, RULE,
                              text, svg, mark, fraunces, fraunces_it, inter6, inter4)

# ================= CONFIG =================
SITE = 'https://lawrenceleejr.github.io/KnoxParkAndPerk/'
# Pack check-out Google Form (see design/LOGGING.md step 2). Template gets
# .format(first=..., last=...). Leave empty until the form exists.
PACK_FORM_URL = ''
# e.g. ('https://docs.google.com/forms/d/e/FORM_ID/viewform?usp=pp_url'
#       '&entry.1111111={first}&entry.2222222={last}')
PACK_SIZE = 50
# ==========================================

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def qr_path(data, error='m'):
    """Return (svg_path_d, modules_per_side) for a QR encoding `data`."""
    q = segno.make(data, error=error, micro=False)
    buf = io.BytesIO()
    q.save(buf, kind='svg', xmldecl=False, svgns=False, border=0)
    m = re.search(r'<path[^>]* d="([^"]+)"', buf.getvalue().decode())
    n = q.symbol_size(border=0)[0]
    return m.group(1), n


def qr_group(data, x, y, size, color=NIGHT):
    d, n = qr_path(data)
    s = size / n
    return (f'<g transform="translate({x},{y}) scale({s:.5f})">'
            f'<path stroke="{color}" d="{d}"/></g>')


def card_svg(serial):
    url = f'{SITE}?c={serial}#partners'
    b = []
    b.append(f'<rect x="1" y="1" width="523" height="298" rx="14" fill="{PAPER}" stroke="{RULE}" stroke-width="1.5"/>')
    b.append(f'<path d="M15 1.75 H510 a13 13 0 0 1 13.25 13.25 V22 H1.75 V15 A13 13 0 0 1 15 1.75 Z" fill="{ORANGE}"/>')
    b.append(mark(26, 40, 40))
    b.append(text(fraunces, 'Knox Pick-Me-Up', 23, 82, 68, INK)[0])
    b.append(text(inter6, 'MORNING PICK-ME-UP CARD', 9, 499, 64, ORANGE_INK, tracking=0.18, anchor='end')[0])
    b.append(f'<line x1="26" y1="92" x2="499" y2="92" stroke="{RULE}" stroke-width="1"/>')
    b.append(text(fraunces, 'Free large coffee', 36, 26, 148, INK)[0])
    b.append(text(fraunces_it, 'You made the safe call. Your second brew’s on us.', 14.5, 27, 174, INK2)[0])
    rows = [
        [('One large coffee at participating downtown shops', inter4, INK2)],
        [('Hair of the KAT', inter6, ORANGE_INK),
         (' — your KAT bus fare while this card is valid', inter4, INK2)],
        [('One per ride · Not for resale · No cash value', inter4, INK2)],
    ]
    for i, segs in enumerate(rows):
        y = 202 + i * 19
        b.append(f'<rect x="27" y="{y-3.5}" width="7" height="1.5" fill="{ORANGE}"/>')
        x = 42
        for seg, face, col in segs:
            pth, w = text(face, seg, 11, x, y, col)
            b.append(pth)
            x += w
    b.append(f'<rect x="398" y="104" width="102" height="102" rx="4" fill="#ffffff" stroke="{RULE}" stroke-width="1"/>')
    b.append(qr_group(url, 408, 114, 82))
    b.append(text(inter6, 'SCAN FOR PARTICIPATING', 6.8, 449, 222, INK2, tracking=0.16, anchor='middle')[0])
    b.append(text(inter6, 'BUSINESSES', 6.8, 449, 233, INK2, tracking=0.16, anchor='middle')[0])
    b.append(f'<line x1="26" y1="252" x2="499" y2="252" stroke="{RULE}" stroke-width="1"/>')
    b.append(text(inter6, 'VALID FOR ONE DAY FROM', 9.5, 26, 274, INK, tracking=0.14)[0])
    b.append(f'<line x1="190" y1="276" x2="310" y2="276" stroke="{INK2}" stroke-width="1"/>')
    b.append(text(inter4, f'Nº {serial}', 9.5, 499, 274, INK2, tracking=0.04, anchor='end')[0])
    return svg(525, 300, ''.join(b),
               f'Knox Pick-Me-Up — Morning Pick-Me-Up Card {serial}')


def pack_svg(pack_no, first, last):
    b = []
    b.append(f'<rect width="525" height="700" fill="{PAPER}" stroke="{RULE}" stroke-width="1.5"/>')
    b.append(f'<rect width="525" height="16" fill="{ORANGE}"/>')
    b.append(mark(40, 52, 56))
    b.append(text(fraunces, 'Knox Pick-Me-Up', 30, 118, 92, INK)[0])
    b.append(text(inter6, f'CARD PACK Nº {pack_no:03d} · {PACK_SIZE} CARDS', 11, 40, 142, ORANGE_INK, tracking=0.16)[0])
    b.append(f'<line x1="40" y1="162" x2="485" y2="162" stroke="{RULE}" stroke-width="1"/>')
    b.append(text(inter6, 'SERIALS', 9, 40, 194, INK2, tracking=0.18)[0])
    b.append(text(fraunces, f'{first}', 26, 40, 228, INK)[0])
    b.append(text(fraunces, f'through  {last}', 26, 40, 262, INK)[0])
    b.append(f'<line x1="40" y1="292" x2="485" y2="292" stroke="{RULE}" stroke-width="1"/>')
    b.append(text(inter6, 'CHECKING THIS PACK OUT TO A BAR?', 11, 40, 326, INK, tracking=0.14)[0])
    if PACK_FORM_URL:
        url = PACK_FORM_URL.format(first=first, last=last)
        b.append(qr_group(url, 40, 348, 170))
        b.append(text(inter4, 'Scan, pick the bar from the list, submit. Ten seconds.', 12, 232, 380, INK2)[0])
        b.append(text(inter4, 'That ties every card in this pack to the bar for the', 12, 232, 400, INK2)[0])
        b.append(text(inter4, 'monthly numbers — no other paperwork.', 12, 232, 420, INK2)[0])
    else:
        b.append(text(inter4, 'Pack check-out form not configured yet — set PACK_FORM_URL in', 12, 40, 356, INK2)[0])
        b.append(text(inter4, 'tools/build_cards.py (see design/LOGGING.md) and rebuild.', 12, 40, 376, INK2)[0])
    b.append(f'<line x1="40" y1="560" x2="485" y2="560" stroke="{RULE}" stroke-width="1"/>')
    b.append(text(inter6, 'BAR', 9, 40, 592, INK2, tracking=0.18)[0])
    b.append(f'<line x1="80" y1="592" x2="300" y2="592" stroke="{INK2}" stroke-width="1"/>')
    b.append(text(inter6, 'DATE', 9, 330, 592, INK2, tracking=0.18)[0])
    b.append(f'<line x1="378" y1="592" x2="485" y2="592" stroke="{INK2}" stroke-width="1"/>')
    b.append(text(inter4, 'Backup for the QR: write it down and text a photo to the program.', 10.5, 40, 630, INK2)[0])
    return svg(525, 700, ''.join(b),
               f'Knox Pick-Me-Up card pack {pack_no:03d}, serials {first} to {last}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--year', type=int, default=2026)
    ap.add_argument('--start', type=int, default=1, help='first serial number')
    ap.add_argument('--count', type=int, default=PACK_SIZE, help='how many cards')
    args = ap.parse_args()

    cards_dir = os.path.join(REPO, 'print', 'cards')
    packs_dir = os.path.join(REPO, 'print', 'packs')
    os.makedirs(cards_dir, exist_ok=True)
    os.makedirs(packs_dir, exist_ok=True)

    serials = [f'KPU-{args.year}-{n:06d}' for n in range(args.start, args.start + args.count)]
    for s in serials:
        open(os.path.join(cards_dir, f'card-{s}.svg'), 'w').write(card_svg(s))

    for i in range(0, len(serials), PACK_SIZE):
        chunk = serials[i:i + PACK_SIZE]
        pack_no = (args.start + i - 1) // PACK_SIZE + 1
        open(os.path.join(packs_dir, f'pack-{pack_no:03d}.svg'), 'w').write(
            pack_svg(pack_no, chunk[0], chunk[-1]))

    print(f'{len(serials)} cards -> {cards_dir}')
    print(f'{math.ceil(len(serials)/PACK_SIZE)} pack sheets -> {packs_dir}')
    print('Hand the SVGs to any print shop, or convert: '
          'pip install cairosvg && python3 -c "import cairosvg,glob;'
          '[cairosvg.svg2pdf(url=f,write_to=f.replace(\'.svg\',\'.pdf\')) '
          'for f in glob.glob(\'print/**/*.svg\',recursive=True)]"')


if __name__ == '__main__':
    main()
