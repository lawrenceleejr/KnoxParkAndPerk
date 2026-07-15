# Knox Park & Perk — Visual Identity

*Make it home safe. Tomorrow's coffee's on us.*

This is the brand guide for Knox Park & Perk. Everything here is built on one
idea: **the journey from a dark night out to a bright morning coffee.** Night
navy resolves into sunrise orange; a coffee cup rises like the sun; the
ampersand ties "Park **&** Perk" together.

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
| Primary lockup (light bg) | [`assets/logo.svg`](assets/logo.svg) | Default. On cream/white and light photos. |
| Lockup (dark bg) | [`assets/logo-dark.svg`](assets/logo-dark.svg) | On navy/espresso/dark photos. Cream wordmark. |
| Emblem / badge | [`assets/logo-mark.svg`](assets/logo-mark.svg) | Standalone icon where the full name is elsewhere; stamps, seals, large watermark. |
| Ampersand mark | [`assets/ampersand.svg`](assets/ampersand.svg) | The signature glyph on its own (see §3). |
| App icon / favicon | [`assets/favicon.svg`](assets/favicon.svg) | Browser tab, social avatar, app tile. |

**The emblem** is a coffee cup at sunrise inside a badge whose sky runs from
night at the top to sunrise at the bottom — "you made it to morning." It is
ringed with **KNOX PARK & PERK** and **MAKE IT HOME SAFE**.

**Clear space:** keep at least the height of the emblem's ring stroke — roughly
the cap-height of the wordmark — clear on all sides. Don't crowd it.

**Minimum size:** lockup no smaller than 180 px / 1.6 in wide; emblem and app
icon no smaller than 24 px. Below ~32 px prefer the **ampersand mark** or
**favicon**, which are built to stay legible when tiny.

**Don't:** recolor the wordmark outside the palette · stretch or skew ·
add drop shadows/outlines · rebuild the lockup with different fonts ·
place the light lockup on a busy/dark background (use `logo-dark.svg`).

---

## 3. The ampersand — our signature mark

Park **&** Perk lives and dies on that ampersand, so we made it the brand's
monogram. [`assets/ampersand.svg`](assets/ampersand.svg) is a custom, calligraphic
ampersand drawn as a single flowing stroke in the sunrise gradient. It reads
cleanly from hero-size down to a 16 px favicon.

Use it for: the **favicon / app icon** (set in a navy rounded square, see
`favicon.svg`), social avatars, a large watermark or section divider, a "loading"
or bullet glyph, merch (coaster backs, pins, cup sleeves).

Keep it in brand colors — sunrise gradient, solid cream, solid navy, or solid
sunrise. Don't outline it, add effects, or set it at an angle.

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

A warm serif for personality, a clean geometric sans for everything functional.

| Role | Typeface | Weights | Used for |
|---|---|---|---|
| Display | **Fraunces** (serif) | 500 / 600 / 800, incl. *italic* | Wordmark, headings (h1–h3), taglines. Its italic ampersand echoes our mark. |
| Text & UI | **Poppins** (sans) | 400 / 500 / 600 / 700 / 800 | Body copy, nav, buttons, labels, kickers, the "Knoxville, Tennessee" line. |

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

[`assets/favicon.svg`](assets/favicon.svg) — the ampersand in the sunrise
gradient on a Night-Deep rounded square with a gold edge. Wired into the site as:

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
  logo.svg          Primary lockup (light backgrounds)
  logo-dark.svg     Lockup for dark backgrounds
  logo-mark.svg     Emblem / badge
  ampersand.svg     Signature ampersand glyph
  favicon.svg       App icon / favicon (ampersand in a rounded square)
  card.svg          The Morning Perk Card artwork
  coaster.svg       The bar coaster artwork
  palette.svg       Color swatch sheet
```

*Contact: hello@knoxparkandperk.org · Knoxville, TN*
