# Knox Park & Perk — Visual Identity

*Make it home safe. Tomorrow's coffee's on us.*

This is the brand guide for Knox Park & Perk. Everything here is built on one
idea: **the journey from a dark night out to a bright morning coffee.** Night
navy resolves into sunrise orange. The signature **mark** — a coffee cup whose
inside is a steering wheel, steam rising — says the whole program in one glyph
("park the car, coffee's on us") and doubles as the connective **"and"** in
"Park [mark] Perk."

All assets live in [`assets/`](assets) as scalable SVG (resolution-independent,
print- and web-ready).

---

## 1. Brand at a glance

| | |
|---|---|
| **Name** | Knox Park & Perk |
| **Tagline** | *Make it home safe. Tomorrow's coffee's on us.* |
| **Essence** | Road safety made warm and rewarding — not preachy |
| **Story arc** | Last call → Ride home → Morning → Coffee |
| **Voice** | Warm, wry, plainspoken. Never "don't drink and drive"; always "good call — coffee's on us." |

---

## 2. Logo suite

| Asset | File | Use |
|---|---|---|
| Primary lockup (light bg) | [`assets/logo.svg`](assets/logo.svg) | Default. "KNOX PARK [mark] PERK" on cream/white and light photos. |
| Lockup (dark bg) | [`assets/logo-dark.svg`](assets/logo-dark.svg) | On navy/espresso/dark photos. Cream wordmark. |
| The mark | [`assets/mark.svg`](assets/mark.svg) | The signature glyph on its own — the connective "and," a bullet, a watermark. Uses `currentColor` so it takes the surrounding text color; steam & coffee stay orange. |
| Emblem / badge | [`assets/logo-mark.svg`](assets/logo-mark.svg) | The mark sealed in a navy badge, for stamps, avatars, spot use. |
| App icon / favicon | [`assets/favicon.svg`](assets/favicon.svg) | Browser tab, social avatar, app tile. |

**The mark** is a coffee cup whose interior is a three-spoke steering wheel,
with steam rising and coffee pooled at the bottom — "park the car, the morning's
on us." It is the heart of the identity: it sits **between the two words as the
connective "and"** ("KNOX PARK [mark] PERK"), and stands alone as the icon.

**Clear space:** keep at least one cup-width of clear space around the lockup.
Don't crowd it.

**Minimum size:** lockup no smaller than 180 px / 1.6 in wide; the mark/app icon
no smaller than 20 px. The mark is drawn to stay legible when small.

**Don't:** recolor the wordmark outside the palette · stretch or skew ·
add drop shadows/outlines · rebuild the lockup with different fonts ·
place the light lockup on a busy/dark background (use `logo-dark.svg`) ·
recolor the steam/coffee away from sunrise orange.

---

## 3. The mark — our connective "and"

Park **and** Perk are joined by the mark itself: in the wordmark it literally
takes the place of the ampersand, so the logo reads "KNOX PARK [cup] PERK." The
cup-and-steering-wheel does double duty — it *is* the program (drive safe,
coffee's on us) and it *is* the conjunction.

[`assets/mark.svg`](assets/mark.svg) is drawn with the silhouette in
`currentColor` (so it inherits the text color — cream on dark, espresso on
light) and the steam and coffee locked to sunrise orange. Inline it (SVG
`<use>`) so `currentColor` works; when embedded via `<img>` set the color
explicitly.

Use it for: the connective "and" in the wordmark, the **favicon / app icon**,
social avatars, a large watermark or section divider, a bullet glyph, and merch.

Keep the silhouette in a single brand color (cream, navy, or espresso) with the
steam/coffee in sunrise orange. Don't outline it, add effects, or tilt it.

---

## 4. Color palette

Full swatch sheet: [`assets/palette.svg`](assets/palette.svg)

| Name | Hex | RGB | Role |
|---|---|---|---|
| Night Deep | `#0C1224` | 12, 18, 36 | Primary dark bg; app-icon field |
| Midnight Navy | `#141D33` | 20, 29, 51 | Nav, dark sections, emblem sky top |
| Espresso | `#3A2A1D` | 58, 42, 29 | Body text on cream |
| Espresso Light | `#6B543F` | 107, 84, 63 | Secondary text, captions |
| Cream | `#FFF7EC` | 255, 247, 236 | Primary light bg; text on dark |
| Gold | `#FFB95E` | 255, 185, 94 | Accents, taglines on dark, ring/borders |
| Sunrise | `#FF8200` | 255, 130, 0 | Primary accent, buttons, the ampersand |
| Sunrise Deep | `#D96A00` | 217, 106, 0 | Accent text on cream, gradient end, hovers |

**The signature gradient (night → sunrise)** — used in the emblem sky, hero
background, and app icon:
`#0C1224` → `#1B2749` → `#6B3A12` → `#FF8200` (top to bottom).
**Sun gradient:** `#FFF2CF` → `#FFB95E` → `#FF8200`.

**Contrast & accessibility**
- Body text: **Espresso `#3A2A1D` on Cream**, or **Cream on Night** — both high-contrast.
- Sunrise and Gold are **accent** colors: use for fills, large/bold display text,
  icons, and borders — not for small body copy on cream (too low-contrast).
  For orange *text* on cream, use **Sunrise Deep `#D96A00`** and keep it large/bold.
- On dark backgrounds, **Gold `#FFB95E`** is the safe accent-text color.

---

## 5. Typography

The wordmark is set in a heavy geometric sans so its stroke weight matches the
mark; a warm serif adds personality in the taglines and section headings.

| Role | Typeface | Weights | Used for |
|---|---|---|---|
| Wordmark | **Poppins ExtraBold** (sans) | 800 | "KNOX PARK [mark] PERK." Chosen because its even, geometric strokes match the weight of the mark. Tight tracking (~-0.02em). |
| Headings | **Fraunces** (serif) | 600 / 800, incl. *italic* | Section headings (h2–h3) and the italic taglines — editorial warmth. |
| Text & UI | **Poppins** (sans) | 400 / 500 / 600 / 700 | Body copy, nav, buttons, labels, kickers, the "Knoxville, Tennessee" line. |

Both are free (Google Fonts / SIL OFL). Web embed:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,800;1,9..144,500;1,9..144,600&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

```css
:root {
  --f-display: 'Fraunces', Georgia, 'Times New Roman', serif;
  --f-sans: 'Poppins', 'Helvetica Neue', Arial, sans-serif;
}
```

**Fallbacks** (email, print, or where the webfont can't load): Georgia for
display, Helvetica/Arial for sans. Kickers and labels are set in
uppercase Poppins with generous letter-spacing (~0.18em).

---

## 6. Favicon & app icon

[`assets/favicon.svg`](assets/favicon.svg) — the mark (cream cup, orange steam
& coffee) on a Night-Deep rounded square with a gold edge. Wired into the site as:

```html
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="apple-touch-icon" href="assets/favicon.svg">
```

For platforms that need raster icons (older browsers, app stores), export the
SVG to PNG at 16, 32, 180, 192, and 512 px.

---

## 7. Motifs

- **Coffee cup at sunrise** — the hero symbol; a cup with the dawn on its surface.
- **Night sky with stars** — dark sections; small twinkling dots, never busy.
- **Sunrise-and-navy skyline stripe** — a thin repeating bar as a section divider.
- **Rays** — short radiating strokes for a rising sun; keep them simple and even.

---

## 8. File index

```
assets/
  logo.svg          Primary lockup — "KNOX PARK [mark] PERK" (light bg)
  logo-dark.svg     Lockup for dark backgrounds
  mark.svg          The signature mark (cup + steering wheel); the connective "and"
  logo-mark.svg     The mark sealed in a navy badge (emblem)
  favicon.svg       App icon / favicon (the mark in a rounded square)
  card.svg          The Morning Perk Card artwork
  coaster.svg       The bar coaster artwork
  palette.svg       Color swatch sheet
  ampersand.svg     Alternate calligraphic ampersand glyph (secondary)
```

*Contact: hello@knoxparkandperk.org · Knoxville, TN*
