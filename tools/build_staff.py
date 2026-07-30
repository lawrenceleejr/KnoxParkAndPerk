"""Staff-facing print materials — the letter-size reference sheets that live
behind the bar and go in a venue's onboarding folder. Same brand system as the
cards, coasters, and signage; generic (no per-venue info), all type outlined.

Builds, into print/staff/ (gitignored), an SVG and a true-size print-ready PDF
for each:
  barista-one-pager   What the scanner shows and what to do — the five/six scan
                      outcomes with their exact on-screen wording, plus manual
                      entry, the flashlight, and offline behavior. Laminate it
                      and keep it by the register.
  bar-onboarding      For a bar joining the program: what you're agreeing to,
                      when to hand a card, the date-writing step, pack basics, and
                      who to contact.

The outcome wording here is copied verbatim from redeem/index.html's setStatus
calls — if the scanner's phrasing changes, update this sheet to match.

Usage:
  pip install fonttools brotli uharfbuzz segno cairosvg
  python3 tools/build_staff.py
"""
import argparse, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_collateral import (PAPER, PAPER2, INK, INK2, NIGHT, ORANGE, ORANGE_INK,
                              GOLD, RULE, SITE_LABEL, text, svg, mark, mark_w,
                              write_pdf, fraunces, fraunces_it, inter6, inter4)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPI = 100                    # letter = 850 x 1100 at 100 user-units/inch
W, H = 850, 1100
MARGIN = 64
CONTACT = 'hello@knoxpickmeup.org'

OK, WARN, BAD = '#2e7d32', '#b04e00', '#b3261e'

# The six states the scanner can show a barista, verbatim from redeem/index.html.
# give=True → hand over the coffee; give=False → no coffee. The glyph is drawn
# as an SVG path (below), not a font character — the outlined font subsets don't
# carry ✓/✕.
OUTCOMES = [
    (OK,   'ok',   'Good to go — coffee’s on us',   True,
     'The card is valid and first-used here. Hand over the large coffee.'),
    (WARN, 'down', 'No signal — saved on this phone', True,
     'You’re offline. The scan is saved and sends itself when signal returns. Still hand over the coffee.'),
    (WARN, 'bang', 'Already scanned on this phone',  False,
     'This exact card was already logged on this phone. One coffee per card — no coffee.'),
    (BAD,  'x',    'Card already redeemed',          False,
     'The card was already used (here or at another shop). No coffee.'),
    (BAD,  'x',    'Card not valid',                 False,
     'The card’s pack was voided (lost or withdrawn). Don’t accept it — no coffee.'),
    (BAD,  'x',    'Serial doesn’t check out',       False,
     'Mistyped, or not a real Knox Pick-Me-Up card. No coffee.'),
]


def fit(face, s, size, max_w, min_size=14):
    while size > min_size and face.shape(s, size)[1] > max_w:
        size -= 1
    return size


def chip(cx, cy, r, kind, color):
    """Colored status disc with a stroked white glyph (no font dependency)."""
    o = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>']
    st = 'stroke="#ffffff" stroke-width="3.2" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    if kind == 'ok':
        o.append(f'<path d="M{cx-8} {cy} L{cx-2} {cy+7} L{cx+9} {cy-8}" {st}/>')
    elif kind == 'x':
        o.append(f'<path d="M{cx-7} {cy-7} L{cx+7} {cy+7} M{cx-7} {cy+7} L{cx+7} {cy-7}" {st}/>')
    elif kind == 'bang':
        o.append(f'<path d="M{cx} {cy-9} L{cx} {cy+2}" {st}/>')
        o.append(f'<circle cx="{cx}" cy="{cy+8}" r="1.9" fill="#ffffff"/>')
    elif kind == 'down':
        o.append(f'<path d="M{cx} {cy-9} L{cx} {cy+5} M{cx-5} {cy} L{cx} {cy+5} L{cx+5} {cy}" {st}/>')
        o.append(f'<path d="M{cx-6} {cy+9} L{cx+6} {cy+9}" {st}/>')
    return ''.join(o)


def wrap(face, s, size, max_w):
    words, lines, cur = s.split(' '), [], ''
    for w in words:
        trial = (cur + ' ' + w).strip()
        if face.shape(trial, size)[1] <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def frame(eyebrow, title):
    """Common letter scaffold: border, orange top bar, mark, wordmark, eyebrow,
    big title. Returns (svg_parts, y) with y just below the title."""
    b = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
         f'<rect x="24" y="24" width="{W-48}" height="{H-48}" fill="none" stroke="{RULE}" stroke-width="2"/>',
         f'<rect x="24" y="24" width="{W-48}" height="10" fill="{ORANGE}"/>']
    b.append(mark(MARGIN, 60, 74))
    b.append(text(fraunces, 'Knox Pick-Me-Up', 30, MARGIN + mark_w(74) + 20, 96, INK)[0])
    b.append(text(inter6, eyebrow, 12, MARGIN + mark_w(74) + 22, 120, ORANGE_INK, tracking=0.2)[0])
    b.append(f'<line x1="{MARGIN}" y1="154" x2="{W-MARGIN}" y2="154" stroke="{RULE}" stroke-width="1.5"/>')
    b.append(text(fraunces, title, fit(fraunces, title, 40, W - 2 * MARGIN), MARGIN, 214, INK)[0])
    return b, 250


def section_label(b, y, s):
    b.append(text(inter6, s, 13, MARGIN, y, ORANGE_INK, tracking=0.16)[0])
    return y + 26


def para(b, y, s, size=14.5, face=None, fill=INK2, lh=1.34, indent=0):
    face = face or inter4
    for line in wrap(face, s, size, W - 2 * MARGIN - indent):
        b.append(text(face, line, size, MARGIN + indent, y, fill)[0])
        y += size * lh
    return y


# ============================================================ barista one-pager
def barista_one_pager():
    b, y = frame('BARISTA QUICK REFERENCE', 'Scan a card. The screen tells you what to do.')
    y = para(b, y + 6,
             'Open the scanner from your register QR, point the phone camera at the QR on the '
             'card (or type the serial below it). Watch the colored banner:', 15)
    y += 18

    # outcome rows: chip on the left, title + verdict pill on the top line,
    # description wrapped beneath — nothing overlaps regardless of title length
    row_h = 92
    x0 = MARGIN
    tw = W - 2 * MARGIN
    tx = x0 + 62               # text column, right of the chip
    for color, kind, title, give, desc in OUTCOMES:
        b.append(f'<rect x="{x0}" y="{y}" width="{tw}" height="{row_h - 14}" rx="8" '
                 f'fill="{PAPER2 if give else PAPER}" stroke="{color}" stroke-width="1.5"/>')
        b.append(chip(x0 + 32, y + 39, 19, kind, color))
        b.append(text(fraunces, title, 20, tx, y + 30, INK)[0])
        verdict = 'HAND OVER THE COFFEE' if give else 'NO COFFEE'
        b.append(text(inter6, verdict, 11, x0 + tw - 18, y + 29, color, tracking=0.12, anchor='end')[0])
        dy = y + 52
        for line in wrap(inter4, desc, 13, tw - (tx - x0) - 24):
            b.append(text(inter4, line, 13, tx, dy, INK2)[0])
            dy += 13 * 1.3
        y += row_h

    y += 8
    y = section_label(b, y, 'IF THE CODE WON’T SCAN')
    y = para(b, y, 'Type the serial (KPMU-2026-…) into the “Manual entry” box and tap Log it. '
                   'Dim room? Tap the ⚡ flashlight button on the camera view.', 14)
    y += 16
    y = section_label(b, y, 'NO INTERNET?')
    y = para(b, y, 'Keep scanning — every scan is saved on the phone and sends itself the moment '
                   'signal returns. The note under the banner shows how many are waiting.', 14)

    b.append(f'<line x1="{MARGIN}" y1="{H-96}" x2="{W-MARGIN}" y2="{H-96}" stroke="{RULE}" stroke-width="1"/>')
    b.append(text(inter6, f'{SITE_LABEL}  ·  {CONTACT}', 12, MARGIN, H - 66, INK2, tracking=0.08)[0])
    b.append(text(fraunces_it, 'One coffee per card. When in doubt, the banner color is the answer: green/amber = yes, red = no.',
                  13, MARGIN, H - 44, ORANGE_INK)[0])
    return svg(W, H, ''.join(b), 'Knox Pick-Me-Up — barista quick reference: what the scanner shows and what to do')


# ============================================================ bar onboarding
def bar_onboarding():
    b, y = frame('FOR PARTICIPATING BARS', 'Welcome aboard. Here’s the whole job.')
    y = para(b, y + 6,
             'Knox Pick-Me-Up gives a patron who lines up a safe ride home a card for a free '
             'coffee — and a free KAT ride — the next morning. As a bar, your part is small:', 15)
    y += 16

    y = section_label(b, y, 'WHAT YOU’RE AGREEING TO')
    for s in [
        'Hand a card to a patron who shows you a booked ride home (rideshare booked, or an active KAT ticket).',
        'One card per booked ride, while your pack lasts. The card is the thank-you — no cost to you.',
        'Keep the cards behind the bar; they’re serialized and dated by hand, so treat them like the vouchers they are.',
    ]:
        b.append(f'<circle cx="{MARGIN+4}" cy="{y-4}" r="2.6" fill="{ORANGE}"/>')
        y = para(b, y, s, 14, indent=20) + 8
    y += 8

    y = section_label(b, y, 'HANDING OUT A CARD')
    for i, s in enumerate([
        'Confirm the ride: a booked rideshare on their phone, or an activated KAT ticket.',
        'Write today’s date in the DATE ISSUED box — that starts the one-day clock.',
        'Hand it over. That’s it — the patron scans and redeems it themselves tomorrow.',
    ]):
        b.append(text(fraunces, str(i + 1), 22, MARGIN, y + 4, ORANGE)[0])
        y = para(b, y, s, 14, indent=34) + 10
    y += 6

    y = section_label(b, y, 'YOUR PACK')
    y = para(b, y, 'Cards come in packs of 50. When a pack is dropped off, someone scans its cover-sheet '
                   'QR and assigns the pack to your bar — that’s how the program counts your contribution, '
                   'with no other paperwork. Running low? Ask for the next pack.', 14)

    b.append(f'<line x1="{MARGIN}" y1="{H-104}" x2="{W-MARGIN}" y2="{H-104}" stroke="{RULE}" stroke-width="1"/>')
    y = section_label(b, H - 74, 'QUESTIONS?')
    b.append(text(inter4, f'{CONTACT}  ·  {SITE_LABEL}  ·  A road-safety partnership with the City of Knoxville, KPD, and KAT.',
                  13, MARGIN, H - 48, INK2)[0])
    return svg(W, H, ''.join(b), 'Knox Pick-Me-Up — bar onboarding: what you agree to, handing out a card, packs, and contact')


def main():
    ap = argparse.ArgumentParser(description='Build Knox Pick-Me-Up staff sheets (barista + bar onboarding).')
    ap.add_argument('--out', default=os.path.join(REPO, 'print', 'staff'), help='output directory')
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    pieces = {
        'barista-one-pager.svg': barista_one_pager(),
        'bar-onboarding.svg': bar_onboarding(),
    }
    for name, body in pieces.items():
        svg_f = os.path.join(args.out, name)
        open(svg_f, 'w').write(body)
        write_pdf(body, svg_f[:-4] + '.pdf', UPI)
        print(f'{name:22s} -> {svg_f}  (+ .pdf)')
    print('Print at 8.5 x 11; laminate the barista sheet for the register. '
          'Generic (no per-venue info); all type is outlined.')


if __name__ == '__main__':
    main()
