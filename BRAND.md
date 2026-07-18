# Knox Pick-Me-Up — Visual Identity

*Make it home safe. Tomorrow's coffee's on us.*

This is the brand guide for Knox Pick-Me-Up. The identity is built on one idea:
**the journey from a dark night out to a bright morning coffee** — told with
restraint. Warm paper, espresso ink, deep night navy, and one confident stroke
of Tennessee orange. The signature **mark** — a coffee cup whose inside is a
steering wheel, steam rising — says the whole program in a single glyph:
*park the car, coffee's on us.*

All assets live in [`assets/`](assets) as scalable SVG. Every piece of type in
the collateral is converted to outlines, so the files render identically
everywhere — web, print, email — with no font dependencies.

---

## 1. Brand at a glance

| | |
|---|---|
| **Name** | Knox Pick-Me-Up |
| **Tagline** | *Make it home safe. Tomorrow's coffee's on us.* |
| **Essence** | Road safety made warm and rewarding — not preachy |
| **Story arc** | Last call → Ride home → Morning → Coffee |
| **Voice** | Warm, wry, plainspoken. Never "don't drink and drive"; always "good call — coffee's on us." |
| **Design posture** | Editorial and civic: generous whitespace, hairline rules, one accent color used sparingly. No gradients, no drop shadows, no decoration that doesn't carry meaning. |

---

## 2. Logo suite

| Asset | File | Use |
|---|---|---|
| Primary lockup (light bg) | [`assets/logo.svg`](assets/logo.svg) | Default. Mark + "Knox Pick-Me-Up" wordmark, tagline, and place line on paper/white. |
| Lockup (dark bg) | [`assets/logo-dark.svg`](assets/logo-dark.svg) | On night navy or dark photography. Paper wordmark, gold tagline. |
| The mark | [`assets/mark.svg`](assets/mark.svg) | The signature glyph on its own. Uses `currentColor` for the silhouette so it takes the surrounding text color; steam & coffee stay orange. |
| Emblem / badge | [`assets/logo-mark.svg`](assets/logo-mark.svg) | The mark sealed in a night circle, for stamps, avatars, spot use. |
| App icon / favicon | [`assets/favicon.svg`](assets/favicon.svg) | Browser tab, social avatar, app tile. |

**The wordmark** is set in Fraunces SemiBold, title case — *Knox Pick-Me-Up* —
never all-caps. The mark sits to the left of the wordmark at cap height ×2,
optically aligned to the first line.

**Clear space:** keep at least one cup-width of clear space around the lockup.

**Minimum size:** lockup no smaller than 200 px / 1.75 in wide; the mark/app
icon no smaller than 20 px.

**Don't:** set the wordmark in another typeface or in all-caps · stretch or
skew · add drop shadows, outlines, or gradients · recolor the steam/coffee away
from sunrise orange · place the light lockup on a dark background (use
`logo-dark.svg`).

---

## 3. The mark

A coffee cup whose interior is a three-spoke steering wheel, with steam rising
and coffee pooled at the bottom — "park the car, the morning's on us."

[`assets/mark.svg`](assets/mark.svg) is drawn with the silhouette in
`currentColor` (so it inherits the text color — ink on paper, paper on night)
and the steam and coffee locked to sunrise orange `#FF8200`. Inline it (SVG
`<use>`) so `currentColor` works; when embedded via `<img>` the color must be
set in the file.

Use it for: the lockup, the favicon / app icon, social avatars, a large
hero graphic, and merch. Keep the silhouette in a single brand color (ink,
paper, or night) with the steam/coffee in sunrise orange. Don't outline it,
add effects, or tilt it.

---

## 4. Color palette

Full swatch sheet: [`assets/palette.svg`](assets/palette.svg)

| Name | Hex | RGB | Role |
|---|---|---|---|
| Paper | `#FAF5EB` | 250, 245, 235 | Primary light background; text on dark |
| Paper Deep | `#F2E9D8` | 242, 233, 216 | Alternate light band |
| Ink | `#241A10` | 36, 26, 16 | Display type, body headings, buttons |
| Umber | `#6F5F4C` | 111, 95, 76 | Secondary text, captions |
| Night | `#101A30` | 16, 26, 48 | Primary dark band |
| Night Deep | `#0A101F` | 10, 16, 31 | Deepest dark band (CTA), app-icon field |
| Sunrise | `#FF8200` | 255, 130, 0 | The accent: mark steam/coffee, big figures, rules, primary buttons on dark |
| Sunrise Ink | `#B04E00` | 176, 78, 0 | Orange for *text* on paper (accessible), link underlines, labels |
| Gold | `#EDA953` | 237, 169, 83 | Accent text on dark backgrounds |
| Hairline | `#DDCFB4` | 221, 207, 180 | Rules and borders on paper |

**One accent, used sparingly.** Sunrise orange carries the brand precisely
because it appears rarely: the mark's steam, the big statistics, hairline
accents, and one button per view. If everything is orange, nothing is.

**Contrast & accessibility**
- Body text: **Ink on Paper** or **Paper on Night** — both high-contrast.
- Sunrise `#FF8200` is for large display use only (figures, the mark). For
  orange *text* at reading sizes on paper, use **Sunrise Ink `#B04E00`**.
- On dark backgrounds, **Gold `#EDA953`** is the safe accent-text color.
- No gradients anywhere in the identity.

---

## 5. Typography

A classic editorial pairing: a characterful serif for display, a neutral sans
for text, and old-style figures reserved for statistics.

| Role | Typeface | Weights | Used for |
|---|---|---|---|
| Display | **Fraunces** (serif) | 600, + 400 *italic* | The wordmark, headlines, FAQ questions, card offer lines. Title case or sentence case — never all-caps. Italic 400 for taglines. |
| Text & UI | **Inter** (sans) | 400 / 500 / 600 | Body copy, lists, captions. Small labels: Inter 600, uppercase, letter-spaced (+0.14–0.22em) — the only all-caps in the system. |
| Figures | **Cormorant** (serif) | 700 | Large statistics only, with old-style (text) figures — `font-variant-numeric: oldstyle-nums` — so the 3s and 7s descend below the baseline. |

All are free (Google Fonts / SIL OFL) and **self-hosted** in
[`assets/fonts/`](assets/fonts) — the site does not depend on a font CDN:

```html
<link rel="stylesheet" href="assets/fonts/fonts.css">
```

```css
:root {
  --f-serif: 'Fraunces', Georgia, serif;
  --f-sans: 'Inter', 'Helvetica Neue', Arial, sans-serif;
  --f-figures: 'Cormorant', Garamond, serif;
}
```

**Scale:** one modular scale (ratio 1.25) drives all sizes. Body ≥ 16 px,
line-height ≈ 1.6, measure 45–75 characters. Hierarchy comes from size,
weight, and space — never color alone.

---

## 6. Favicon & app icon

[`assets/favicon.svg`](assets/favicon.svg) — the mark (paper cup, orange steam
& coffee) on a Night rounded square. Wired into the site as:

```html
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="apple-touch-icon" href="assets/favicon.svg">
```

For platforms that need raster icons, export the SVG to PNG at 16, 32, 180,
192, and 512 px.

---

## 7. Layout language

- **Hairline rules** (`#DDCFB4` on paper, `rgba(250,245,235,.18)` on night)
  structure the page — not boxes, cards, or shadows.
- **Asymmetric editorial grid:** a narrow left column carries the section
  label and heading; content sits right.
- **Numbered steps** use large old-style Cormorant figures in sunrise orange.
- **Night bands** are used twice per page at most (statistics, final CTA).
- **No motion** beyond functional state changes (hover color, details
  open/close). Nothing pulses, twinkles, or floats.

---

## 8. File index

```
assets/
  logo.svg          Primary lockup (light bg) — type outlined, no font deps
  logo-dark.svg     Lockup for dark backgrounds
  mark.svg          The signature mark (cup + steering wheel)
  logo-mark.svg     The mark sealed in a night circle (emblem)
  favicon.svg       App icon / favicon (the mark in a rounded square)
  card.svg          The Morning Pick-Me-Up Card artwork
  coaster.svg       The bar coaster artwork
  palette.svg       Color swatch sheet
  fonts/            Self-hosted woff2 (Fraunces, Inter, Cormorant) + fonts.css
```

*Contact: hello@knoxpickmeup.org · Knoxville, TN*
