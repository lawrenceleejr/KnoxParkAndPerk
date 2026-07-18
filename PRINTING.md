# Knox Pick-Me-Up — Printing Guide

Everything needed to take this repo's artwork to a print shop: what to
order, exact specs to quote, how to generate the files, and what to check
before a run. The physical kit is the program — the cards are the
redeemable item, the packs are the fraud control, the coasters are the ad.

---

## 1. What gets printed

| Piece | Artwork | Quantity logic |
|---|---|---|
| **Card books** (the main event) | `tools/build_cards.py` → `print/cards/` (unique front per card + one static back) | 50 cards/book; 20 books per 1,000 cards |
| **Pack cover sheets** | same script → `print/packs/` (one per book, with pack serial + check-out QR) | 1 per book |
| **Register QRs** (one per coffee shop) | generate per shop, see §5 | 1–2 per shop, laminated |
| **Coasters** | [`assets/coaster.svg`](assets/coaster.svg) | thousands — bars burn through them; they're the advertising |
| Later: table tents, mirror clings, window decals | from `assets/` lockups | per venue |

## 2. The card books — what to ask a printer for

In printer language this is a **raffle-ticket book with variable data**:
perforated tear-off cards, sequential serials, bound in books — one of the
most commoditized products in printing. The only "special" ask is that the
variable data includes a **unique QR per card** (called *variable-data
printing*, VDP), which any digital-press shop can do.

**Copy-paste RFQ:**

> Tear-off card books, 50 cards per book plus a printed cover (artwork
> supplied). Card size 3.5″ × 2″ (quote with and without a 0.75″ bound
> stub). Stock: **14pt uncoated cover** — cards must accept a rubber stamp
> and ballpoint pen, so no gloss or UV coating. Ink 4/4: **front carries
> variable data** (unique QR + serial per card, sequential across books;
> print-ready files supplied, one file per card), **back is static** (one
> file, same on every card). Micro-perforation between stub and card (or
> above the binding edge if no stub). Bound by padding or staple at the
> top edge with a chipboard backer; per-book cover sheet supplied.
> Quantity: 1,000 cards / 20 books — please also quote 2,500 and 5,000.

Why each line matters:
- **Uncoated stock** is non-negotiable: the bartender's date stamp is the
  validity control, and glossy stock rejects stamps.
- **Front variable / back static** is what keeps two-sided cheap — VDP is
  priced per variable *side*, and our back
  (`print/cards/card-back.svg`) is deliberately identical on every card.
- **The stub option** is the raffle-book upgrade worth asking about: a
  small bound stub repeats the serial and stays in the book when the card
  is torn out, giving every bar an automatic paper log of what it issued.
  If a printer quotes it cheaply, take it (and ask for the stub artwork —
  the generator can be extended to produce it).
- **Sequential across books** — give the printer the serial order and let
  them collate so book 1 is serials 1–50, book 2 is 51–100, etc. The pack
  cover sheets are generated to match exactly that split.

**Ballpark:** short-run digital VDP books land around **$0.08–0.20 per
card**, so a 1,000-card pilot is roughly **$100–250** — one sponsor
conversation. There's a natural sponsor: a local print shop, credited on
the card backs ("printing donated by ___").

## 3. Who to send it to

- **A local Knoxville commercial printer** — best option, and on-theme as
  a program sponsor. Franchise shops (Minuteman Press, Allegra, etc.)
  handle perforated VDP books routinely. Ask for *"perforated tear-off
  books with variable data."*
- **Online, VDP-capable:** Smartpress (accepts supplied variable-data
  files, does custom perforation and padding); raffle-ticket specialists
  (TicketPrinting.com, Admit One) if they'll take per-card QR art.
- **Coasters:** any custom-coaster house (pulpboard, 3.5–4″ round,
  1–2 color is fine — the artwork is already flat color).
- **Avoid** pure-template services (Vistaprint-style): generally no
  per-card QR + perforation + books.

## 4. Generating the print files

```sh
pip install fonttools brotli uharfbuzz segno
python3 tools/build_cards.py --year 2026 --start 1 --count 1000
```

That writes to `print/` (gitignored):
- `print/cards/card-KPU-2026-00000001.svg` … — one file per card (front)
- `print/cards/card-back.svg` — the static back, once
- `print/packs/pack-KPU-2026-0000000001.svg` … — one cover sheet per 50

Everything is SVG with **all type converted to outlines** — no font
substitution surprises at the shop. Most shops prefer PDF; convert with:

```sh
pip install cairosvg
python3 -c "import cairosvg,glob
for f in glob.glob('print/**/*.svg', recursive=True):
    cairosvg.svg2pdf(url=f, write_to=f.replace('.svg', '.pdf'))"
```

**Bleed:** the current artwork is exact trim size (3.5″ × 2″ at 150/in
units). The front's orange band and the navy back run to the trim edge,
so the shop will ask for **1/8″ bleed**. Ask for their template/specs
first, then extend `tools/build_cards.py` to their bleed + crop-mark spec
before the final run (the layout is parametric — this is a small change,
not a redesign).

**Before generating, check the CONFIG block** at the top of
`tools/build_cards.py`: `PACK_FORM_URL` must be set (see
[`design/LOGGING.md`](design/LOGGING.md)) or the pack cover sheets print a
"form not configured" placeholder instead of the check-out QR.

## 5. Register QRs (one per coffee shop)

Each shop's counter QR opens the scanner pre-set to that shop:

```sh
python3 -c "import segno; segno.make(
  'https://lawrenceleejr.github.io/KnoxParkAndPerk/redeem.html?shop=SLUG',
  error='q').save('register-SLUG.png', scale=12, border=2)"
```

Use the slugs from the `SHOPS` map in [`redeem.html`](redeem.html). Print
at ~3″, mount on card stock, laminate. Error level `q` keeps them
scannable when the lamination glares or the corner gets coffee on it.

## 6. Pre-flight checklist (every run)

1. **Serial continuity** — `--start` must be the next unused number
   (check the highest serial in the `Packs` tab or `data/backup/packs.csv`;
   never reprint a live range).
2. **`PACK_FORM_URL` configured** so pack sheets carry the check-out QR.
3. **Proof one card end to end**: print `card-…0001` on a desk printer,
   scan its QR with a phone — it must open the public site — then scan it
   from `redeem.html?shop=demo-cafe` and see the serial extracted.
4. **Stamp test** on the shop's actual stock sample: rubber date stamp +
   ballpoint, smudge check after 10 seconds.
5. **QR size sanity**: the card QR prints at about 0.55″ — fine for
   phone cameras, but don't let a shop shrink the card below 3.5″ × 2″.
6. Order **books = cards ÷ 50**, and physically match pack cover sheets
   to books by serial range when they arrive.

---

*Specs live here; the logging system the QRs feed is in
[`design/LOGGING.md`](design/LOGGING.md); brand rules are in
[`BRAND.md`](BRAND.md).*
