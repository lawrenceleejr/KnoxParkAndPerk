"""Render assets/og-image.png (the social-share raster) from the SVG that
tools/build_collateral.py emits. Split out because most scrapers (Slack,
iMessage, Twitter/X, Facebook) won't render an SVG og:image, so we ship a PNG
— but the design still lives in the brand system, not by hand.

Usage:
  pip install cairosvg
  python3 tools/build_collateral.py   # writes assets/og-image.svg
  python3 tools/build_og_png.py       # -> assets/og-image.png (1200x630)
"""
import os
import cairosvg

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = f'{REPO}/assets/og-image.svg'
OUT = f'{REPO}/assets/og-image.png'

if not os.path.exists(SRC):
    raise SystemExit(f'{SRC} not found — run tools/build_collateral.py first')
cairosvg.svg2png(url=SRC, write_to=OUT, output_width=1200, output_height=630)
print(f'og-image.png -> {OUT}  (1200x630)')
