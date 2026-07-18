"""Proposed new logos + custom visual elements for Knox Pick-Me-Up (design exploration)."""
import math, sys, os
sys.path.insert(0, '/home/user/KnoxParkAndPerk/tools')
from text2path import Face
from build_collateral import (PAPER, PAPER2, INK, INK2, NIGHT, NIGHT2, ORANGE,
                              ORANGE_INK, GOLD, RULE, text, arc_text, svg,
                              fraunces, fraunces_it, inter6, inter4)

OUT = '/home/user/KnoxParkAndPerk/design/proposals'
os.makedirs(OUT, exist_ok=True)

def rays(cx, cy, r0, r1, angles, stroke, w):
    out = []
    for a in angles:
        rad = math.radians(a)
        x0, y0 = cx + r0*math.cos(rad), cy - r0*math.sin(rad)
        x1, y1 = cx + r1*math.cos(rad), cy - r1*math.sin(rad)
        out.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" '
                   f'stroke="{stroke}" stroke-width="{w}" stroke-linecap="round"/>')
    return ''.join(out)

# ---------------------------------------------------------------- 1. First Light
def first_light(fg=INK, accent=ORANGE, bg=None):
    b = []
    if bg: b.append(f'<rect width="240" height="240" fill="{bg}"/>')
    # sun half-disc rising from the coffee surface (rim y=108)
    b.append(f'<path d="M94 106 A26 26 0 0 1 146 106 Z" fill="{accent}"/>')
    b.append(rays(120, 106, 38, 50, [30, 65, 90, 115, 150], accent, 8))
    # cup bowl
    b.append(f'<path d="M62 106 L62 124 A58 58 0 0 0 178 124 L178 106" fill="none" '
             f'stroke="{fg}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>')
    # rim
    b.append(f'<line x1="50" y1="106" x2="190" y2="106" stroke="{fg}" stroke-width="11" stroke-linecap="round"/>')
    # handle
    b.append(f'<path d="M182 122 C206 122 206 152 178 154" fill="none" stroke="{fg}" '
             f'stroke-width="10" stroke-linecap="round"/>')
    # saucer
    b.append(f'<line x1="86" y1="196" x2="154" y2="196" stroke="{fg}" stroke-width="11" stroke-linecap="round"/>')
    return ''.join(b)

open(f'{OUT}/concept-1-first-light.svg', 'w').write(
    svg(240, 240, first_light(), 'Concept 1 — First Light: a sunrise coming up out of the coffee cup'))

# lockup variant
b = [first_light()]
w1, ww = text(fraunces, 'Knox Pick-Me-Up', 56, 264, 118, INK)
b.append(w1)
b.append(text(fraunces_it, 'Ride from last call to first call.', 20, 266, 152, ORANGE_INK)[0])
open(f'{OUT}/concept-1-lockup.svg', 'w').write(
    svg(math.ceil(264+ww+16), 240, ''.join(b), 'Concept 1 lockup — First Light mark with wordmark'))

# ---------------------------------------------------------------- 2. Last Call / First Light stamp
b = []
cx = cy = 150
b.append(f'<circle cx="{cx}" cy="{cy}" r="140" fill="{PAPER}"/>')
b.append(f'<circle cx="{cx}" cy="{cy}" r="136" fill="none" stroke="{INK}" stroke-width="3"/>')
b.append(f'<circle cx="{cx}" cy="{cy}" r="104" fill="none" stroke="{INK}" stroke-width="1.2"/>')
b.append(arc_text(inter6, 'KNOX PICK-ME-UP', 14, cx, cy, 118, INK, tracking=0.3, mode='top'))
b.append(arc_text(inter6, 'LAST CALL · FIRST LIGHT', 11, cx, cy, 116, ORANGE_INK, tracking=0.24, mode='bottom'))
for sdeg in (90, 270):
    px = cx + 118*math.sin(math.radians(sdeg)); py = cy - 118*math.cos(math.radians(sdeg))
    b.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.4" fill="{ORANGE}"/>')
# center: star -> dashed route home -> cup
b.append(f'<path d="M186 74 l3.4 9.4 9.4 3.4 -9.4 3.4 -3.4 9.4 -3.4 -9.4 -9.4 -3.4 9.4 -3.4 Z" fill="{INK}"/>')
b.append(f'<path d="M182 108 C150 130 190 152 150 172" fill="none" stroke="{INK}" '
         f'stroke-width="4.5" stroke-linecap="round" stroke-dasharray="0.1 11"/>')
# small cup at route end
b.append(f'<path d="M118 182 L118 190 A26 26 0 0 0 170 190 L170 182" fill="none" stroke="{INK}" '
         f'stroke-width="6" stroke-linecap="round"/>')
b.append(f'<line x1="112" y1="182" x2="176" y2="182" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
b.append(f'<path d="M172 190 C186 190 186 204 170 205" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
b.append(f'<path d="M132 180 A12 12 0 0 1 156 180 Z" fill="{ORANGE}"/>')
open(f'{OUT}/concept-2-stamp.svg', 'w').write(
    svg(300, 300, ''.join(b), 'Concept 2 — a bartender-stamp seal: a star at last call, a dashed route home, a sunrise cup'))

# ---------------------------------------------------------------- 3. Steam Road
def steam_road(fg=INK, road=PAPER, accent=ORANGE, bg=None):
    b = []
    if bg: b.append(f'<rect width="240" height="240" fill="{bg}"/>')
    # mug
    b.append(f'<rect x="82" y="122" width="80" height="70" rx="10" fill="none" stroke="{fg}" stroke-width="11"/>')
    b.append(f'<path d="M164 136 C190 138 190 172 162 174" fill="none" stroke="{fg}" stroke-width="10" stroke-linecap="round"/>')
    # steam that is a road: thick stroke with dashed centerline
    p = 'M98 112 C156 94 72 62 130 38'
    b.append(f'<path d="{p}" fill="none" stroke="{fg}" stroke-width="22" stroke-linecap="round"/>')
    b.append(f'<path d="{p}" fill="none" stroke="{road}" stroke-width="4.2" stroke-dasharray="11 9" stroke-linecap="butt"/>')
    # destination: rising sun beyond the top of the road
    b.append(f'<path d="M155 42 A15 15 0 0 1 185 42 Z" fill="{accent}"/>')
    b.append(rays(170, 42, 21, 29, [40, 90, 140], accent, 5.5))
    b.append(f'<line x1="148" y1="42" x2="192" y2="42" stroke="{accent}" stroke-width="5.5" stroke-linecap="round"/>')
    return ''.join(b)

open(f'{OUT}/concept-3-steam-road.svg', 'w').write(
    svg(240, 240, steam_road(road=PAPER), 'Concept 3 — Steam Road: the steam off the mug is a dashed highway leading to a sunrise'))

# ---------------------------------------------------------------- 4. Night & Morning token
b = []
cx = cy = 120; R = 96
b.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>')
# night upper half
b.append(f'<path d="M{cx-R+2} {cy} A{R-2} {R-2} 0 0 1 {cx+R-2} {cy} Z" fill="{NIGHT}"/>')
# stars
b.append(f'<path d="M84 72 l2.6 7 7 2.6 -7 2.6 -2.6 7 -2.6 -7 -7 -2.6 7 -2.6 Z" fill="{PAPER}"/>')
b.append(f'<circle cx="152" cy="60" r="2.6" fill="{PAPER}"/>')
b.append(f'<circle cx="126" cy="46" r="1.8" fill="{PAPER}"/>')
# sunrise on the horizon
b.append(f'<path d="M96 120 A24 24 0 0 1 144 120 Z" fill="{ORANGE}"/>')
b.append(rays(120, 120, 33, 43, [35, 90, 145], ORANGE, 6.5))
# horizon line
b.append(f'<line x1="{cx-R+4}" y1="120" x2="{cx+R-4}" y2="120" stroke="{INK}" stroke-width="4"/>')
# cup below (morning side)
b.append(f'<path d="M96 152 L96 158 A24 24 0 0 0 144 158 L144 152" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')
b.append(f'<line x1="90" y1="152" x2="150" y2="152" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')
b.append(f'<path d="M146 158 C160 158 160 172 144 173" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
open(f'{OUT}/concept-4-night-morning.svg', 'w').write(
    svg(240, 240, ''.join(b), 'Concept 4 — Night & Morning token: starry night above the horizon, sunrise and coffee below'))

# ---------------------------------------------------------------- element sheet
E = []
E.append(f'<rect width="960" height="700" fill="{PAPER}"/>')
E.append(text(inter6, 'KNOX PICK-ME-UP · CUSTOM VISUAL ELEMENTS (PROPOSED)', 12, 48, 56, INK, tracking=0.22)[0])

# 1. horizon divider
E.append(text(inter6, 'HORIZON DIVIDER — section break, night to morning', 9, 48, 96, INK2, tracking=0.14)[0])
E.append(f'<line x1="48" y1="126" x2="444" y2="126" stroke="{RULE}" stroke-width="1.5"/>')
E.append(f'<path d="M456 126 A12 12 0 0 1 480 126 Z" fill="{ORANGE}"/>')
E.append(rays(468, 126, 17, 23, [45, 90, 135], ORANGE, 3.5))
E.append(f'<line x1="492" y1="126" x2="912" y2="126" stroke="{RULE}" stroke-width="1.5"/>')

# 2. route divider
E.append(text(inter6, 'ROUTE RULE — the journey home, then back for coffee', 9, 48, 180, INK2, tracking=0.14)[0])
E.append(f'<path d="M56 214 l3 8.2 8.2 3 -8.2 3 -3 8.2 -3 -8.2 -8.2 -3 8.2 -3 Z" fill="{INK}"/>')
E.append(f'<line x1="84" y1="225" x2="852" y2="225" stroke="{INK}" stroke-width="3" stroke-linecap="round" stroke-dasharray="0.1 10"/>')
E.append(f'<path d="M868 214 L868 220 A14 14 0 0 0 896 220 L896 214" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
E.append(f'<line x1="864" y1="214" x2="900" y2="214" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
E.append(f'<path d="M876 210 A6 6 0 0 1 888 210 Z" fill="{ORANGE}"/>')

# 3. icon set
E.append(text(inter6, 'ICON SET — monoline, one weight, for steps and wayfinding', 9, 48, 286, INK2, tracking=0.14)[0])
icons = []
def ic(body):  # 48x48 viewport at given origin
    icons.append(body)
S = 'fill="none" stroke="%s" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"' % INK
# parking garage
p_d, p_w = inter6.shape('P', 26)
ic(f'<path d="M6 20 L24 8 L42 20 L42 42 L6 42 Z" {S}/>'
   f'<path transform="translate({24-p_w/2:.1f},36)" fill="{INK}" d="{p_d}"/>')
# bus
ic(f'<rect x="8" y="7" width="32" height="28" rx="5" {S}/><line x1="8" y1="21" x2="40" y2="21" {S}/>'
   f'<circle cx="16" cy="37.5" r="3" fill="{INK}"/><circle cx="32" cy="37.5" r="3" fill="{INK}"/>'
   f'<line x1="14" y1="14" x2="34" y2="14" {S}/>')
# rideshare phone
ic(f'<rect x="13" y="5" width="22" height="38" rx="4" {S}/>'
   f'<path d="M24 13 a7.5 7.5 0 0 1 7.5 7.5 c0 5.5 -7.5 12 -7.5 12 c0 0 -7.5 -6.5 -7.5 -12 A7.5 7.5 0 0 1 24 13 Z" {S}/>'
   f'<circle cx="24" cy="20.5" r="2.2" fill="{INK}"/>')
# card
ic(f'<rect x="5" y="11" width="38" height="26" rx="3" {S}/><line x1="5" y1="19" x2="43" y2="19" stroke="{ORANGE}" stroke-width="3.2"/>'
   f'<line x1="11" y1="27" x2="27" y2="27" {S}/><line x1="11" y1="32" x2="21" y2="32" {S}/>'
   f'<rect x="32" y="25" width="7" height="7" {S}/>')
# cup
ic(f'<path d="M8 18 L8 24 A16 16 0 0 0 40 24 L40 18 Z" {S}/><line x1="5" y1="18" x2="43" y2="18" {S}/>'
   f'<path d="M40 22 C48 22 48 32 39 33" {S}/>'
   f'<path d="M21 12 C25 9 19 6 23 3" {S.replace(INK, ORANGE)}/>')
# sunrise
ic(f'<line x1="5" y1="34" x2="43" y2="34" {S}/><path d="M14 34 A10 10 0 0 1 34 34" {S.replace(INK, ORANGE)}/>'
   + rays(24, 34, 15, 21, [30, 90, 150], ORANGE, 3.2).replace('/>', '/>'))
labels = ['PARK', 'KAT', 'RIDE', 'CARD', 'COFFEE', 'MORNING']
for i, (body, lab) in enumerate(zip(icons, labels)):
    x = 48 + i*112
    E.append(f'<g transform="translate({x},312)">{body}</g>')
    E.append(text(inter6, lab, 8.5, x+24, 384, INK2, tracking=0.18, anchor='middle')[0])

# 4. coffee-ring stamp
E.append(text(inter6, 'COFFEE-RING STAIN', 9, 48, 444, INK2, tracking=0.14)[0])
E.append(f'<g transform="translate(120,540)" fill="none" stroke="{ORANGE_INK}" opacity="0.85">'
         f'<ellipse cx="0" cy="0" rx="62" ry="58" stroke-width="7" stroke-dasharray="88 14 42 9 120 12" transform="rotate(-14)"/>'
         f'<ellipse cx="3" cy="2" rx="55" ry="52" stroke-width="2" stroke-dasharray="60 34 90 26" transform="rotate(23)"/></g>')
# 5. sunrise scallop pattern
E.append(text(inter6, 'SUNRISE SCALLOP — repeating border for print collateral', 9, 250, 444, INK2, tracking=0.14)[0])
row = []
for i in range(10):
    x = 250 + i*68
    row.append(f'<path d="M{x} 540 A20 20 0 0 1 {x+40} 540 Z" fill="{ORANGE if i%2==0 else NIGHT}"/>')
E.append(f'<line x1="240" y1="540" x2="930" y2="540" stroke="{INK}" stroke-width="2.5"/>' + ''.join(row))
# 6. serial / ticket treatment
E.append(text(inter6, 'SERIAL TREATMENT — every card is numbered, make it a feature', 9, 48, 620, INK2, tracking=0.14)[0])
E.append(f'<rect x="48" y="638" width="240" height="40" rx="3" fill="none" stroke="{INK}" stroke-width="1.5" stroke-dasharray="6 5"/>')
E.append(text(inter6, 'Nº KPMU-2026-00004217', 15, 168, 664, ORANGE_INK, tracking=0.08, anchor='middle')[0])
open(f'{OUT}/elements.svg', 'w').write(svg(960, 700, ''.join(E), 'Proposed custom visual elements for Knox Pick-Me-Up'))
print('proposals built')
