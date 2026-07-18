# Knox Pick-Me-Up — Card Logging System

How cards get tracked from print run → bar → coffee shop → dashboard, with
**no server to maintain, no on-call, and $0/month**. Designed for a
volunteer-run program: every moving part is either a static file on GitHub
Pages or a Google-hosted freebie that keeps running if everyone goes on
vacation.

---

## 1. The moving parts

```
print run                bar                    coffee shop                you
─────────                ───                    ───────────                ───
tools/build_cards.py     pack cover QR          register QR opens          Google Sheet
makes per-serial cards   opens pre-filled       redeem.html?shop=slug      (the database)
+ pack cover sheets  →   Google Form:       →   barista scans the      →       │
each card QR encodes     "serials X–Y → [bar    card's QR with the             ▼
site URL with serial     dropdown]" — 10 sec    phone camera → serial      Looker Studio
                                                logged automatically       dashboard
```

**The one clever trick — the card QR is dual-use.** Every card's QR encodes
`https://…/?c=KPU-2026-00004217#partners` — a plain link to the public site:

- A **patron** who scans it just lands on the participating-businesses
  section of the website. No login walls, nothing weird.
- The **shop scanner page** (`redeem.html`) doesn't *follow* the URL — it
  *reads* it with the camera and extracts the `KPU-…` serial with a regex.

Same printed code, two behaviors, zero extra infrastructure.

**Venue attribution needs nobody to type a venue name, ever:**

- **Coffee shop** = which register QR opened the scanner
  (`redeem.html?shop=wild-love`). Print one QR per shop, tape it by the till.
- **Bar** = the serial range. Packs of 50 are checked out per bar via the
  pack form, so `serial → bar` is a range lookup in the Sheet.

## 2. Components in detail

### A. The database: one Google Sheet
Owned by a program Google account (make one — `knoxpickmeup@gmail.com` — so
this survives any individual volunteer). Three tabs:

| Tab | Columns | Filled by |
|---|---|---|
| `Redemptions` | timestamp · serial · shop · status · **bar** · **pack serial** | Apps Script (below) |
| `Packs` | timestamp · **pack serial** · first card serial · last card serial · bar · **voided** | the pack Google Form (voided: you, by hand) |
| `Venues` | slug · display name · type (bar/shop) · joined date | you, by hand, rarely |

**Pack serials** are 10 digits (`KPU-YYYY-##########`) — two more than the
8-digit card serials, so a pack can never be mistaken for a card anywhere in
the data. The bar attribution is **stored on each redemption row at scan
time**: the Apps Script looks the card's serial up in `Packs` (which range
contains it) and writes the issuing bar and pack serial alongside the shop.
No formulas required for the join; keep a duplicate flag
(`=COUNTIF(B:B,B2)>1`) as a belt-and-suspenders check.

**Kill switch:** to invalidate an entire pack (lost, stolen, misprinted,
or a bar leaves the program), type anything in its `voided` cell —
e.g. `LOST 7/20`. From that moment every card in the pack **fails to scan**
at every register: the barista sees "not valid," and the attempt is still
logged with status `void` so the integrity dashboard shows where voided
cards are turning up. Clearing the cell restores the pack.

### B. The redemption endpoint: a bound Apps Script web app
This is the piece that makes scanning *automatic* (a bare Google Form can't
answer "was this card already used?"). It's ~30 lines pasted **once** into
the Sheet (Extensions → Apps Script), deployed as a web app
(Execute as: **me**, Access: **anyone**). Google hosts, runs, and patches
it — this is configuration, not a server you babysit.

```javascript
const SHEET = 'Redemptions';   // timestamp | serial | shop | status | bar | pack serial
const PACKS = 'Packs';         // timestamp | pack serial | first | last | bar | voided

// serial -> { bar, pack, voided } via the Packs tab (which range contains it)
function lookupBar(serial) {
  const rows = SpreadsheetApp.getActive().getSheetByName(PACKS).getDataRange().getValues();
  const year = serial.slice(4, 8), n = Number(serial.slice(9));
  for (let i = 1; i < rows.length; i++) {
    const [, pack, first, last] = rows[i].map(String);
    if (first.slice(4, 8) === year &&
        n >= Number(first.slice(9)) && n <= Number(last.slice(9))) {
      return { bar: String(rows[i][4] || ''), pack: pack,
               voided: String(rows[i][5] || '').trim() !== '' };
    }
  }
  // pack never checked out — visible in the dashboard
  return { bar: '', pack: '', voided: false };
}

function doGet(e) {
  const p = e.parameter;
  let out = { status: 'error' };
  if (p.action === 'redeem' && /^KPU-\d{4}-\d{8}$/i.test(p.serial || '')) {
    const serial = p.serial.toUpperCase();
    const shop = String(p.shop || 'unknown').slice(0, 40);
    const lock = LockService.getScriptLock();
    lock.waitLock(5000);                       // serialize concurrent scans
    try {
      const sh = SpreadsheetApp.getActive().getSheetByName(SHEET);
      const src = lookupBar(serial);
      if (src.voided) {
        // pack was invalidated — refuse, but keep the attempt for the audit trail
        sh.appendRow([new Date(), serial, shop, 'void', src.bar, src.pack]);
        out = { status: 'void' };
      } else {
        // columns B..D: serial | shop | status — only 'ok' rows count as redeemed
        const rows = sh.getRange(2, 2, Math.max(sh.getLastRow() - 1, 1), 3).getValues();
        const hit = rows.find(r => r[0] === serial && r[2] === 'ok');
        if (hit) {
          // refused, but logged so the dashboard can count duplicate attempts
          sh.appendRow([new Date(), serial, shop, 'dup', src.bar, src.pack]);
          out = { status: 'duplicate', firstShop: hit[1] };
        } else {
          sh.appendRow([new Date(), serial, shop, 'ok', src.bar, src.pack]);
          out = { status: 'ok', bar: src.bar };
        }
      }
    } finally {
      lock.releaseLock();
    }
  }
  if (p.action === 'stats') {
    // public by design: venue names, timestamps, statuses, and counts only —
    // card serials and anything else stay out of the payload
    const ss = SpreadsheetApp.getActive();
    const red = ss.getSheetByName(SHEET).getDataRange().getValues().slice(1)
      .map(r => [new Date(r[0]).toISOString(), String(r[2]), String(r[3]), String(r[4] || '')]);
    const packs = ss.getSheetByName(PACKS).getDataRange().getValues().slice(1)
      .map(r => [new Date(r[0]).toISOString(), String(r[1]), String(r[4] || ''), String(r[5] || '')]);
    out = { redemptions: red, packs: packs };
  }
  return ContentService.createTextOutput(JSON.stringify(out))
    .setMimeType(ContentService.MimeType.JSON);
}
```

`redeem.html` calls it with a GET and shows the barista **"Good to go"** or
**"Card already redeemed at ‹shop›"** in real time.

### C. The scanner: `redeem.html` (this repo, GitHub Pages)
Already built. Brand-styled, self-contained static page:
- opens from a per-shop QR (`redeem.html?shop=slug`), shows which shop it's
  logging for;
- tap-to-start camera; native `BarcodeDetector` where available, vendored
  [jsQR](../assets/vendor/jsQR.js) (Apache-2.0) everywhere else — works on
  iPhone Safari and old Androids alike;
- manual-entry box for damaged codes;
- **offline-tolerant**: no signal → the scan queues in `localStorage`, the
  barista is told to hand over the coffee, and the queue auto-flushes when
  the connection returns;
- per-device duplicate warning even before the network round-trip;
- **demo mode**: with `SCRIPT_URL` unset it logs to the screen only — safe
  to try right now.

### D. Pack check-out: a plain Google Form
One question that matters: **Bar** (dropdown). The pack serial and card
serial range arrive pre-filled by the pack cover sheet's QR. Whoever delivers packs scans,
taps the bar, submits. The cover sheet also has a written-log fallback line.

### E. Card + pack printing: `tools/build_cards.py` (this repo)
`python3 tools/build_cards.py --year 2026 --start 1 --count 500` emits
per-serial card SVGs and one cover sheet per 50 into `print/` (gitignored),
ready for any print shop (SVG→PDF one-liner included in the script output).
Unique QR per card is what makes scan-to-log possible.

### F. The admin dashboard: `dashboard.html` (this repo, GitHub Pages)
A brand-styled, self-contained dashboard on the same static site, fed live
from the Sheet through the Apps Script's `stats` action. It shows a KPI row
(issued, redeemed, redemption rate, last 7 days, duplicate attempts,
voided-pack attempts), redemptions per day/week, ranked **to-shop** and
**from-bar** charts, a bar → shop flow matrix, and the latest activity —
with 7/30/90-day/all-time range chips and a 5-minute auto-refresh.

**Access: shareable by link, on purpose.** The page isn't linked from the
public site and carries `noindex`, so the URL travels by word of mouth —
but anyone you hand it to (the City, KPD, a reporter, a prospective
partner) can open it and watch the numbers live. That works because the
payload is venue names, timestamps, statuses, and counts only — card
serials and patron data never leave the Sheet. With `SCRIPT_URL` unset the
page renders generated demo data, so you can try it right now.

### G. Dashboards for partners: Looker Studio (free)
Connect it to the Sheet once; it stays live. Suggested pages:
- **Program**: cards issued vs redeemed, redemption rate, trend by week.
- **By venue**: redemptions per shop, issuance per bar (via the range
  lookup), busiest nights.
- **Integrity**: duplicate attempts, `void` scans (voided-pack cards
  turning up, and where), unknown-shop scans, packs issued but never
  redeeming (a pack that never redeems = probably sitting in a storeroom,
  not fraud).

Share as view-only links with the City, KPD, KAT, and partners; embed on the
site later if wanted. Nothing to host.

## 3. Setup runbook (one afternoon, in order)

1. Create the program Google account; create the Sheet with the three tabs.
2. Create the **pack form** (fields: pack serial, first card serial, last
   card serial, bar dropdown), link it to the Sheet's `Packs` tab, and grab
   a pre-filled URL (⋮ → *Get pre-filled link*) to learn the three
   `entry.NNNN` IDs.
3. Paste the Apps Script above into the Sheet, deploy as web app, copy the
   `/exec` URL.
4. In this repo: set `SCRIPT_URL` and the `SHOPS` map in `redeem.html`;
   set `SCRIPT_URL` in `dashboard.html`; set `PACK_FORM_URL` in
   `tools/build_cards.py`. Commit, merge — Pages redeploys.
5. Generate per-shop register QRs (any QR tool, or segno one-liner) pointing
   at `https://…/redeem.html?shop=<slug>`; print and laminate.
6. Run `tools/build_cards.py`, send `print/` to the print shop.
7. Build the Looker Studio dashboard on the Sheet; share view links.
8. Dry-run with one friendly bar + one shop before the real pilot.

## 4. What this costs and what can break

**Cost:** $0. GitHub Pages, Google Forms/Sheets/Apps Script, and Looker
Studio are all free at this scale (Apps Script's free quota is ~20k
requests/day; a wildly successful pilot is a few hundred redemptions a
week).

| Failure | What happens | Why it's fine |
|---|---|---|
| Shop has no signal | Scan queues on the phone, flushes later | Coffee still handed over; data arrives late, not never |
| Apps Script down / quota hit | Same queue path | Google outages are rare and short; nobody pages you |
| Barista can't scan | Manual entry box; worst case, write it down | The card itself is still stamped and dated |
| Someone spams the endpoint | Junk rows in a sheet | Serials are checkable against issued ranges; worst real-world case is one free coffee — controls stay proportionate (PROGRAM.md §2) |
| Volunteer leaves | Credentials live in the program account | Hand the Google account + repo admin to the next person |

**Privacy:** the system stores *no patron data at all* — serial, shop, and
timestamp only. That's worth saying out loud to the City and in the FAQ.

## 5. Why not the alternatives

- **A real backend (Cloudflare Workers / Supabase / Firebase):** better
  validation and auth, but now there are deploys, tokens, and breakage that
  page *you*. Wrong trade for a volunteer program whose worst-case loss is
  a coffee. Revisit only if the program outgrows Sheets (>50k rows/year).
- **Plain Google Form for redemptions (no Apps Script):** zero code, but
  can't answer "already redeemed" at the counter and needs a manual serial
  type-in per cup. The Apps Script is 30 lines and removes both problems.
- **Airtable/Notion forms:** nicer UI, but free-tier row caps and a
  commercial dependency for a civic program.
- **No logging (paper only):** always the fallback, but then there are no
  numbers for the City/KPD — and §7 of PROGRAM.md promises metrics.
