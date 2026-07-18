# Knox Pick-Me-Up

*Ride from last call to first call.*

**🌐 Live site: <https://lawrenceleejr.github.io/KnoxParkAndPerk/>**

A proposed public-private road-safety partnership for downtown Knoxville:
patrons who drove downtown and take a safe ride home at the end of the night —
a rideshare, taxi, or public transit — show proof of the ride to their
bartender and receive a **Morning Pick-Me-Up Card**, good for a **free large coffee**
at a participating downtown shop when they return the next morning to pick up
their car. While valid (one day), the card also doubles as a free KAT transit
pass — including the ride back downtown to the car.

Partners: City of Knoxville · Knoxville Police Department · Knoxville Area
Transit (KAT) · downtown bars · downtown coffee shops.

## The pages

Three pages, one static site — each aimed at a different audience:

| Page | Audience | What it does |
|---|---|---|
| [`index.html`](https://lawrenceleejr.github.io/KnoxParkAndPerk/) | **Public** — patrons, partners, press | The program site: how it works, why it matters, the card, partner pitch, FAQ. Every card's QR lands patrons here, on the participating-businesses section. Linked everywhere. |
| [`redeem.html`](https://lawrenceleejr.github.io/KnoxParkAndPerk/redeem.html) | **Business** — coffee-shop baristas | The card scanner. Opened from the shop's register QR (`?shop=slug`, with a dropdown fallback), it scans a card's QR with the phone camera, shows live detection feedback, and logs the redemption — with duplicate/voided-card rejection, offline queueing, manual entry, and a stop button. Runs in labeled demo mode until the backend is configured. |
| [`dashboard.html`](https://lawrenceleejr.github.io/KnoxParkAndPerk/dashboard.html) | **Admin** — you, and anyone you hand the link | Live program numbers from the Sheet: issued/redeemed/rate tiles, integrity counters, redemptions over time, to-shop and from-bar rankings, the bar→shop flow matrix, latest activity. Unlinked and unindexed but freely shareable — it exposes venue names, timestamps, and counts only, never patron data or serials. |

Also business-facing but not a page: each **card pack's cover sheet** carries
a QR that opens the pack check-out Google Form (pre-filled serials, pick the
bar from a dropdown).

## Contents

- **[`index.html`](index.html) · [`redeem.html`](redeem.html) ·
  [`dashboard.html`](dashboard.html)** — the three pages above; fully
  self-contained static files, no build step.
- **[`PROGRAM.md`](PROGRAM.md)** — full program design: mechanics, card spec,
  fraud controls, branding guide, partner engagement playbook, pilot budget,
  metrics, timeline, and risk register.
- **[`design/LOGGING.md`](design/LOGGING.md)** — the card-tracking system:
  QR scan-to-log redemptions (`redeem.html`), pack check-out, Google Sheets
  backend, Looker Studio dashboards — no servers, $0, volunteer-proof.
- **[`PRINTING.md`](PRINTING.md)** — the printing guide: card-book specs and
  a copy-paste RFQ, vendor guidance, file generation, register QRs, and the
  pre-flight checklist for every print run.
- **[`BRAND.md`](BRAND.md)** — the visual identity guide: logo suite, the
  signature mark, color palette, typography, favicon, layout language, and usage.
- **[`assets/`](assets)** — brand assets as scalable SVG (print- and web-ready;
  all type converted to outlines, no font dependencies):
  - [`logo.svg`](assets/logo.svg) — primary lockup (light backgrounds)
  - [`logo-dark.svg`](assets/logo-dark.svg) — lockup for dark backgrounds
  - [`mark.svg`](assets/mark.svg) — the signature mark (cup + steering wheel)
  - [`logo-mark.svg`](assets/logo-mark.svg) — the mark sealed in a badge (emblem)
  - [`favicon.svg`](assets/favicon.svg) — app icon / favicon
  - [`palette.svg`](assets/palette.svg) — color swatch sheet
  - [`card.svg`](assets/card.svg) — the Morning Pick-Me-Up Card (business-card size)
  - [`coaster.svg`](assets/coaster.svg) — the bar coaster (round)

## How the data flows

One Google Sheet is the entire database. Who writes what:

| Data | Written by | Human involved? |
|---|---|---|
| `Redemptions` (each coffee handed over) | the **Apps Script web app**, when a barista scans a card on [`redeem.html`](redeem.html) | barista points a phone camera; no typing |
| `Packs` (which bar got which serials) | the **pack check-out Google Form**, opened by the QR on each pack's cover sheet | deliverer picks the bar from a dropdown |
| `Venues`, `Packs.voided` (kill switch) | **you, by hand** | rarely |

Nothing else ever writes to the Sheet. Full architecture, the Apps Script
code, and failure-mode analysis: [`design/LOGGING.md`](design/LOGGING.md).

## Set up the program (one afternoon)

Everything below is free and requires no server. Steps 1–3 happen in Google,
4–6 in this repo, 7–8 back in Google/GitHub.

1. **Create the program Google account** (e.g. `knoxpickmeup@gmail.com`) so
   nothing is tied to one volunteer. Do all Google steps signed in as it.
2. **Create the Sheet** with three tabs and header rows:
   - `Redemptions`: `timestamp | serial | shop | status | bar | pack serial`
   - `Packs`: `timestamp | pack serial | first | last | bar | voided`
   - `Venues`: `slug | name | type | joined | deactivated`
   Share it with **no one** (partners get the dashboard, not the sheet), and
   right-click the `Redemptions` tab → *Protect sheet* → only you.
3. **Create the pack check-out Form** (Google Forms): short-answer fields
   *Pack serial*, *First card serial*, *Last card serial*, and a *Bar*
   dropdown. Link responses to the Sheet's `Packs` tab. Then ⋮ → *Get
   pre-filled link*, fill dummy values, and note the three `entry.NNNNN`
   numbers in the generated URL.
4. **Paste the Apps Script** from [`design/LOGGING.md`](design/LOGGING.md)
   into the Sheet (Extensions → Apps Script). Set `BACKUP_KEY` to a long
   random string. Deploy → New deployment → Web app, *Execute as: me*,
   *Access: anyone*. Copy the `/exec` URL. Run `nightlySnapshot` once to
   authorize it, then add a daily time-driven trigger for it (Triggers → Add).
5. **Configure this repo** (marked `CONFIG` blocks at the top of each file):
   - [`redeem.html`](redeem.html): `SCRIPT_URL` = the `/exec` URL; fill the
     `SHOPS` map (slug → display name).
   - [`dashboard.html`](dashboard.html): the same `SCRIPT_URL`.
   - [`tools/build_cards.py`](tools/build_cards.py): `PACK_FORM_URL` using
     the three `entry.NNNNN` IDs from step 3.
   Commit and merge to `main` — Pages redeploys automatically.
6. **Print things** — follow [`PRINTING.md`](PRINTING.md): generate the
   card books and pack cover sheets with `tools/build_cards.py`, make one
   register QR per coffee shop, and use the RFQ + pre-flight checklist
   there when ordering.
7. **Dashboards** — the built-in one is live immediately at
   [`dashboard.html`](dashboard.html) (unlinked and unindexed; share the URL
   freely). Optionally build a Looker Studio view on the Sheet for partners
   who want to slice data themselves.
8. **Turn on backups** — repo Settings → Secrets and variables → Actions →
   add `BACKUP_URL` (the `/exec` URL) and `BACKUP_KEY` (same string as in
   the script). Run the *Nightly data backup* workflow once by hand
   (Actions tab → Run workflow) and confirm a commit touching
   `data/backup/*.csv` appears.
9. **Dry-run** with one friendly bar and one shop before the pilot:
   check a pack out, scan a card at a register, watch it land on the
   dashboard.

## Backups — "what if someone breaks the sheet?"

Four independent layers, detailed in
[`design/LOGGING.md`](design/LOGGING.md#h-backups--disaster-recovery):

1. **Sheet version history** (built into Google) — one-click restore for bad
   edits; covers 95% of accidents.
2. **Nightly Drive snapshots** — the Apps Script copies the whole file into
   a "KPU Backups" folder daily, keeping 30 dated copies.
3. **Nightly off-Google backup** — a GitHub Action pulls every tab and
   commits CSVs to [`data/backup/`](data/backup) in this repo; **git history
   is the archive**, so any past day is recoverable even if the entire
   Google account is lost. If the backup breaks, the Action fails and
   GitHub emails you — that's the whole monitoring system.
4. **Paper** — pack cover sheets carry a hand-written bar/date line, and
   every card is physically stamped.

Losing the whole Google account costs under an hour: rebuild the Sheet from
the repo's CSVs, re-paste the script, update `SCRIPT_URL` in two files.

## Publishing the site

GitHub Pages is configured to deploy from the `main` branch (Settings → Pages),
so every push to `main` republishes
<https://lawrenceleejr.github.io/KnoxParkAndPerk/> automatically. No build
tooling required.
