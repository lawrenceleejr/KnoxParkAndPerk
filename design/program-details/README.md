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
