# Program Details — the partner briefing book

This folder is the editable source for the **Knox Pick-Me-Up — Program Details**
document (the bound partner briefing book). It's written in
[Typst](https://typst.app), which keeps the words in plain, readable text while
the design is applied automatically.

```
program-details.typ   ← the WORDS. Edit this. (all the copy lives here)
template.typ          ← the LOOK. Colors, fonts, and the reusable components
                        (stat bands, give/get cards, the card mock, dividers).
                        You rarely need to touch it.
fonts/                ← the brand fonts (Fraunces, Inter, Cormorant) as .ttf
mark-dark.svg         ← the mark recolored for the navy cover
mark-paper.svg        ← the mark recolored for light pages
```

## Editing the copy — no software to install

1. Go to **[typst.app](https://typst.app)** and sign in (free).
2. Create a project and **upload this whole `program-details/` folder**.
3. Open `program-details.typ`. You get a live preview on the right, and
   Google-Docs-style sharing so collaborators can edit too.
4. Edit the text. Press the download button for a PDF.

Typst reads almost like Markdown:

| You type | You get |
|---|---|
| `*bold*` | **bold** |
| `_italic_` | _italic_ |
| `---` | — (em dash) |
| `"quotes"` | curly “quotes” automatically |
| `\$5` | a literal `$5`  *(a bare `$` starts a math formula, so escape it)* |

Each section begins with `#sect("2", "Part I · The Opportunity", "The insight",
"subtitle…", "s_insight")` — change the number, kicker, title, or subtitle
freely. **The table of contents and every page number update themselves** — you
never hand-number anything, and cross-references like `page #pageof("s_park")`
follow the content automatically.

To add a section, copy an existing `#sect(...)` block, give it a new label (the
last argument, e.g. `"s_new"`), write the body, and add one matching
`#tocrow("N  Title", "s_new")` line up in the Contents. That's it.

## Editing on the command line (optional)

Install the `typst` CLI (a single binary, `brew install typst` or from
[github.com/typst/typst](https://github.com/typst/typst)), then:

```sh
# from this folder:
typst watch  --font-path fonts program-details.typ    # live preview while editing
typst compile --font-path fonts program-details.typ \
      ../Knox-Pick-Me-Up-Program-Details.pdf          # write the final PDF
```

## Build targets (screen vs. print)

The same source builds a screen PDF and print-ready files, selected with
`--input target=…`:

```sh
# on-screen / web (default): 8.5x11, no bleed, no blank pages, clickable links
typst compile --font-path fonts program-details.typ \
      ../Knox-Pick-Me-Up-Program-Details.pdf

# Lulu perfect-bound INTERIOR: 8.75x11.25 (0.125" bleed), right-hand starts,
# even page count, NO cover pages (Lulu prints the cover separately)
typst compile --font-path fonts --input target=interior program-details.typ \
      ../Knox-Pick-Me-Up-Program-Details-lulu-interior.pdf

# Front + back cover art alone, full-bleed, for Lulu's cover creator
typst compile --font-path fonts --input target=covers covers.typ \
      ../Knox-Pick-Me-Up-Program-Details-lulu-cover.pdf

# full book with cover inline + bleed (e.g. for coil binding as one file)
typst compile --font-path fonts --input target=print program-details.typ out.pdf
```

What the targets change:

- **screen** — the reading/web version. No bleed, and none of the blank filler
  pages (they'd just be blanks to scroll past); the contents and citation URLs
  are live links.
- **print / interior / covers** — add 0.125" bleed and the book imposition:
  the cover, contents, and every Part open on a right-hand (recto) page, blank
  filler pages are inserted where needed, and the count is padded even. Those
  blanks carry no running footer (it's hidden on any page lacking the invisible
  `<pm>` content marker). `interior` drops the cover pages for Lulu's
  perfect-bound flow; `covers` renders just the front and back cover art.

For Lulu: create the project with the **interior** PDF, choose your paper, and
either use Lulu's cover creator with the **cover** art or ask for a wraparound
cover built to Lulu's exact spine width (it depends on the final page count and
paper, so it's built last). If a binding needs a multiple-of-four page count,
add or remove a trailing blank.

## Notes

- The fonts here are the same faces as the rest of the brand
  (`assets/fonts/`). The brand ships Fraunces as a *variable* font pinned to
  weight 900, which Typst can't re-weight on its own, so `fonts/` holds three
  static cuts instantiated from it — `fraunces-regular` (weight 400),
  `fraunces-semibold` (600), and `fraunces-italic` — plus Inter and Cormorant.
  If the brand fonts ever change, re-instantiate those cuts into `fonts/`.
- The `.svg` art (the card, coasters, window decal, table tent, posters, pack
  cover, staff sheets, sponsor one-sheet) are copies of the generated collateral
  in [`../../print/`](../../print) and [`../../assets/`](../../assets), kept here
  so the folder is self-contained for typst.app. If a piece is regenerated,
  re-copy it in.
- Keep the numbers honest: the local injury/fatality figures and the pilot
  budget come from [`../../PROGRAM.md`](../../PROGRAM.md) — update them here if
  they change there.
