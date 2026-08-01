# design/

- **[LOGGING.md](LOGGING.md)** — the data/logging system design: the Google
  Sheet schema, the Apps Script, serials & checksums, backups, and the
  venue-roster source of truth.

- **[program-details/](program-details/)** — the **Program Details** partner
  briefing book: a portrait, print-ready document that walks every partner
  (bars, coffee shops, City/KPD, KAT, the Downtown Parking Authority, sponsors)
  through how the program works, why each side wins, how it pays for itself, the
  harm-reduction case (with real citations), and appendices on the technical
  architecture, serialization, privacy, printing, finances, references, brand,
  and how to fork the program for another community. It's authored in
  **[Typst](https://typst.app)** so anyone can edit it — the copy lives in
  [`program-details/program-details.typ`](program-details/program-details.typ)
  in plain, Markdown-like text and the design lives in `template.typ`. Edit it
  in the browser at [typst.app](https://typst.app) (upload the folder, live
  preview, export a PDF) or with the `typst` CLI. See
  [`program-details/README.md`](program-details/README.md) for the how-to.
- **[Knox-Pick-Me-Up-Program-Details.pdf](Knox-Pick-Me-Up-Program-Details.pdf)**
  — the on-screen / web version (clickable contents and citations, no bleed).
- **[Knox-Pick-Me-Up-Program-Details-lulu-interior.pdf](Knox-Pick-Me-Up-Program-Details-lulu-interior.pdf)**
  and **[…-lulu-cover.pdf](Knox-Pick-Me-Up-Program-Details-lulu-cover.pdf)** —
  print-ready files for [Lulu](https://lulu.com): the perfect-bound interior
  (0.125" bleed, right-hand starts, even page count) and the front/back cover
  art. See [`program-details/README.md`](program-details/README.md#build-targets-screen-vs-print).

The current visual identity lives in **[../BRAND.md](../BRAND.md)**, and all
brand artwork is generated from **[../tools/build_collateral.py](../tools/build_collateral.py)**
(and the sibling `build_cards`, `build_coasters`, `build_signage`, `build_staff`,
`build_sponsor` generators). The source glyph is
[`../assets/mark.svg`](../assets/mark.svg).

> **Retired:** the earlier logo *exploration* (`build_proposals.py`,
> `PROPOSALS.md`, and `proposals/*.svg`) was removed — it pitched alternatives
> to an identity two logos ago and couldn't run (it hard-coded a former repo's
> paths). One concept was a physical stamp; the program has since dropped the
> stamp — the bartender **writes the date on the card by hand** (see
> [../PRINTING.md](../PRINTING.md)).
