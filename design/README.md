# design/

- **[LOGGING.md](LOGGING.md)** — the data/logging system design: the Google
  Sheet schema, the Apps Script, serials & checksums, backups, and the
  venue-roster source of truth.

- **[program-details.html](program-details.html)** — the **Program Details**
  partner briefing book: a portrait, print-ready document that walks every
  partner (bars, coffee shops, City/KPD, KAT, the Downtown Parking Authority,
  sponsors) through how the program works, why each side wins, how it pays for
  itself, the harm-reduction case (with real citations), and appendices on the
  technical architecture, serialization, privacy, printing, finances,
  references, brand, and how to fork the program for another community. It is
  self-contained (fonts and the mark are embedded) — open it in a browser and
  print, or regenerate the PDF with the two tools below.
  - **[../tools/build_program_details.py](../tools/build_program_details.py)**
    assembles the HTML from `PROGRAM.md`'s content and the brand assets.
  - **[../tools/render_program_details.py](../tools/render_program_details.py)**
    renders the PDF and fills the table of contents with real page numbers
    (needs Chromium + `websocket-client` + `pymupdf`).

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
