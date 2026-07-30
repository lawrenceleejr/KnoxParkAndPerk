# design/

- **[LOGGING.md](LOGGING.md)** — the data/logging system design: the Google
  Sheet schema, the Apps Script, serials & checksums, backups, and the
  venue-roster source of truth.

The current visual identity lives in **[../BRAND.md](../BRAND.md)**, and all
brand artwork is generated from **[../tools/build_collateral.py](../tools/build_collateral.py)**
(and the sibling `build_cards`, `build_coasters`, `build_signage`, `build_staff`,
`build_sponsor`, `build_stamp` generators). The source glyph is
[`../assets/mark.svg`](../assets/mark.svg).

> **Retired:** the earlier logo *exploration* (`build_proposals.py`,
> `PROPOSALS.md`, and `proposals/*.svg`) was removed — it pitched alternatives
> to an identity two logos ago and couldn't run (it hard-coded a former repo's
> paths). Its one still-useful idea, a physical stamp, is now a real,
> current-mark die: [`../tools/build_stamp.py`](../tools/build_stamp.py) (see
> [../PRINTING.md](../PRINTING.md)).
