"""Stage every visual and print asset into materials/assets/ for the
knoxpickmeup.org/materials showcase page.

The brand marks (assets/*.svg) and the booklet PDFs (design/*.pdf) are already
committed, and the page links to them in place. The print kit (cards, coasters,
signage, stickers, staff sheets, sponsor sheet) is generated into the gitignored
print/ tree, so this script runs those generators and copies a representative,
committable set into materials/assets/ (self-contained SVG + true-size PDF),
plus a raster cover thumbnail for the booklet.

Run it whenever the art changes, then commit materials/assets/:
  pip install fonttools brotli uharfbuzz segno cairosvg pymupdf
  python3 tools/build_materials.py
"""
import os
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, 'materials', 'assets')

# each generator is run so print/ is fresh before we copy from it
GENERATORS = [
    [sys.executable, 'tools/build_collateral.py'],
    [sys.executable, 'tools/build_cards.py', '--year', '2026', '--start', '1', '--count', '1'],
    [sys.executable, 'tools/build_coasters.py'],
    [sys.executable, 'tools/build_signage.py'],
    [sys.executable, 'tools/build_staff.py'],
    [sys.executable, 'tools/build_sponsor.py'],
    [sys.executable, 'tools/build_stickers.py'],
]

# (dest basename, source path relative to REPO without extension) — the .svg and
# .pdf twins are both copied when present.
COPY = [
    ('card-front',       'print/cards/card-KPMU-2026-00000001Q'),
    ('card-back',        'print/cards/card-back'),
    ('pack-cover',       'print/packs/pack-KPMU-2026-P0001'),
    ('coaster-night',    'print/coasters/coaster-night'),
    ('coaster-day',      'print/coasters/coaster-day'),
    ('table-tent',       'print/signage/table-tent'),
    ('window-decal',     'print/signage/window-sticker'),
    ('poster-community', 'print/signage/sign-community'),
    ('poster-restroom',  'print/signage/sign-bathroom'),
    ('sticker-mark',     'print/stickers/sticker-mark'),
    ('sticker-wordmark', 'print/stickers/sticker-wordmark'),
    ('staff-barista',    'print/staff/barista-one-pager'),
    ('staff-onboarding', 'print/staff/bar-onboarding'),
    ('sponsor-one-sheet','print/sponsor/sponsor-one-sheet'),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    for cmd in GENERATORS:
        subprocess.run(cmd, cwd=REPO, check=True, stdout=subprocess.DEVNULL)
        print(f'ran   {cmd[1]}')

    for dest, src in COPY:
        got = []
        for ext in ('.svg', '.pdf'):
            s = os.path.join(REPO, src + ext)
            if os.path.isfile(s):
                shutil.copyfile(s, os.path.join(OUT, dest + ext))
                got.append(ext)
            else:
                print(f'  MISSING {src + ext}')
        print(f'staged {dest:20s} {" ".join(got)}')

    # booklet cover thumbnail — page 1 of the screen PDF (kept current here)
    import fitz
    pdf = os.path.join(REPO, 'design', 'Knox-Pick-Me-Up-Program-Details.pdf')
    fitz.open(pdf)[0].get_pixmap(dpi=150).save(os.path.join(OUT, 'booklet-cover.png'))
    print('rendered booklet-cover.png')
    print(f'\nStaged into {OUT}. Commit materials/ to publish the /materials page.')


if __name__ == '__main__':
    main()
