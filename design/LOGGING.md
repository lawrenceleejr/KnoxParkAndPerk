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
`https://…/?c=KPMU-2026-00004217#partners` — a plain link to the public site:

- A **patron** who scans it just lands on the participating-businesses
  section of the website. No login walls, nothing weird.
- The **shop scanner page** (`redeem.html`) doesn't *follow* the URL — it
  *reads* it with the camera and extracts the `KPMU-…` serial with a regex.

Same printed code, two behaviors, zero extra infrastructure.

**Venue attribution needs nobody to type a venue name, ever:**

- **Coffee shop** = which register QR opened the scanner
  (`redeem.html?shop=wild-love`). Print one QR per shop, tape it by the till.
- **Bar** = the serial range. Packs of 50 are checked out per bar via the
  pack form, so `serial → bar` is a range lookup in the Sheet.

## 2. Components in detail

### A. The database: one Google Sheet
Owned by a program Google account (make one — `knoxpickmeup@gmail.com` — so
this survives any individual volunteer). **How it gets written:** the
`Redemptions` tab is appended to by the **Apps Script web app** (below) every
time a barista scans — no form involved; the `Packs` tab is filled by the
**pack check-out Google Form** (a normal form-linked-to-sheet setup); the
`Venues` tab and the `voided` column are edited **by hand**, rarely. Nothing
else ever writes to the file. Three tabs:

| Tab | Columns | Filled by |
|---|---|---|
| `Redemptions` | timestamp · serial · shop · status · **bar** · **pack serial** | Apps Script (below) |
| `Packs` | timestamp · **pack serial** · first card serial · last card serial · bar · **voided** | the pack Google Form (voided: you, by hand) |
| `Venues` | slug · display name · type (bar/shop) · joined date · **deactivated** · **monthly cap** (shops, optional) | you, by hand, rarely |

**Pack serials** are 10 digits (`KPMU-YYYY-##########`) — two more than the
8-digit card serials, so a pack can never be mistaken for a card anywhere in
the data. The bar attribution is **stored on each redemption row at scan
time**: the Apps Script looks the card's serial up in `Packs` (which range
contains it) and writes the issuing bar and pack serial alongside the shop.
No formulas required for the join; keep a duplicate flag
(`=COUNTIF(B:B,B2)>1`) as a belt-and-suspenders check.

**Serial checksum — the anti-guessing letter.** Every card serial ends in
one letter (`KPMU-2026-00004217T`) that can't be computed without a secret,
so serials can't be minted by counting up from a card in hand. **There is
exactly one secret in the whole system** — `PROGRAM_KEY` — and the checksum
uses a key *derived* from it: `CK_KEY = hex(HMAC-SHA256(PROGRAM_KEY,
"serial-v1"))`, then `letter = HMAC-SHA256(CK_KEY, digits)` mapped to a
24-letter alphabet (no I/O, which read as 1/0). The derivation is one-way,
which is what lets the derived key ride in each shop's **register QR**
(`redeem.html?shop=slug&k=<derived>`): the scanner verifies every scanned
serial locally and instantly — including offline and in demo mode — while
someone who photographs a register QR still can't touch the backup action
or learn the program key. The server re-checks regardless. A made-up serial
passes 1 time in 24, every failure is logged (status `bad`) and surfaced on
the dashboard, and the printed register QRs are the only place the derived
key lives outside Google — never this repo. Get the derived key for QR
printing with `python3 tools/ckkey.py 'YOUR-PROGRAM-KEY'`.

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
// THE one program secret: gates the backup action, and every serial's
// checksum derives from it. Same value goes to GitHub secret PROGRAM_KEY
// and to tools/build_cards.py --key at print time. Nothing else to remember.
const PROGRAM_KEY = 'CHOOSE-ONE-LONG-RANDOM-STRING';

// serial checksum uses a DERIVED key (safe to embed in register QRs so the
// scanner can verify serials locally — deriving is one-way, so a leaked
// register QR cannot unlock the backup action)
const CK_ALPHABET = 'ABCDEFGHJKLMNPQRSTUVWXYZ';     // 24 letters, no I/O
function toHex(bytes) {
  return bytes.map(b => (((b % 256) + 256) % 256).toString(16).padStart(2, '0')).join('');
}
const CK_KEY = toHex(Utilities.computeHmacSha256Signature('serial-v1', PROGRAM_KEY));
function checkLetter(base) {
  const raw = Utilities.computeHmacSha256Signature(base, CK_KEY);
  return CK_ALPHABET[((raw[0] % 256) + 256) % 256 % 24];
}

// serial -> { bar, pack, voided } via the Packs tab (which range contains it)
function lookupBar(serial) {
  const rows = SpreadsheetApp.getActive().getSheetByName(PACKS).getDataRange().getValues();
  // digits only — serials end in a checksum letter, so slice a fixed width
  const year = serial.slice(5, 9), n = Number(serial.slice(10, 18));
  for (let i = 1; i < rows.length; i++) {
    const [, pack, first, last] = rows[i].map(String);
    if (first.slice(5, 9) === year &&
        n >= Number(first.slice(10, 18)) && n <= Number(last.slice(10, 18))) {
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
  if (p.action === 'redeem' && /^KPMU-\d{4}-\d{8}[A-Z]$/i.test(p.serial || '')) {
    const serial = p.serial.toUpperCase();
    const shop = String(p.shop || 'unknown').slice(0, 40);
    const lock = LockService.getScriptLock();
    lock.waitLock(5000);                       // serialize concurrent scans
    try {
      const sh = SpreadsheetApp.getActive().getSheetByName(SHEET);
      if (checkLetter(serial.slice(0, -1)) !== serial.slice(-1)) {
        // fails the keyed checksum — mistyped or made up; log it and refuse
        sh.appendRow([new Date(), serial, shop, 'bad', '', '']);
        out = { status: 'invalid' };
        return ContentService.createTextOutput(JSON.stringify(out))
          .setMimeType(ContentService.MimeType.JSON);
      }
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
    // public by design: venue names, timestamps, statuses, and counts only.
    // REDEEMED card serials stay out of the payload; refused scans (dup/void/
    // bad) DO include theirs — those serials are already burned or invalid,
    // so exposing them grants nothing, and they power duplicate forensics.
    const ss = SpreadsheetApp.getActive();
    const red = ss.getSheetByName(SHEET).getDataRange().getValues().slice(1)
      .map(r => [new Date(r[0]).toISOString(), String(r[2]), String(r[3]), String(r[4] || ''), String(r[5] || ''),
                 String(r[3]) === 'ok' ? '' : String(r[1] || '')]);
    // first/last card serials let the dashboard size each pack (25s vs 50s)
    const packs = ss.getSheetByName(PACKS).getDataRange().getValues().slice(1)
      .map(r => [new Date(r[0]).toISOString(), String(r[1]), String(r[4] || ''), String(r[5] || ''),
                 String(r[2] || ''), String(r[3] || '')]);
    const vsheet = ss.getSheetByName('Venues');
    const venues = !vsheet ? [] : vsheet.getDataRange().getValues().slice(1)
      .map(r => [String(r[0] || ''), String(r[1] || ''), String(r[2] || ''), String(r[4] || ''), String(r[5] || '')]);
    out = { redemptions: red, packs: packs, venues: venues };
  }
  if (p.action === 'backup') {
    // full dump (serials included) for the nightly GitHub backup — gated by
    // the program key, which lives here and in a GitHub secret, never in the repo
    if (p.key !== PROGRAM_KEY) {
      out = { status: 'denied' };
    } else {
      const ss = SpreadsheetApp.getActive();
      out = {};
      for (const name of ['Redemptions', 'Packs', 'Venues']) {
        const sheet = ss.getSheetByName(name);
        if (sheet) out[name] = sheet.getDataRange().getValues();
      }
    }
  }
  return ContentService.createTextOutput(JSON.stringify(out))
    .setMimeType(ContentService.MimeType.JSON);
}

// Nightly whole-file snapshot inside Google Drive (backup layer 2).
// After pasting, run it once to authorize, then add a time-driven trigger:
// Apps Script editor → Triggers → Add → nightlySnapshot, time-driven, daily 3–4 AM.
function nightlySnapshot() {
  const KEEP = 30;
  const src = DriveApp.getFileById(SpreadsheetApp.getActive().getId());
  const folders = DriveApp.getFoldersByName('KPMU Backups');
  const folder = folders.hasNext() ? folders.next() : DriveApp.createFolder('KPMU Backups');
  src.makeCopy('KPMU data ' + Utilities.formatDate(new Date(), 'America/New_York', 'yyyy-MM-dd'), folder);
  const copies = [];
  const it = folder.getFiles();
  while (it.hasNext()) copies.push(it.next());
  copies.sort((a, b) => b.getDateCreated() - a.getDateCreated())
        .slice(KEEP).forEach(f => f.setTrashed(true));
}

// Weekly coordinator digest: Monday-morning email with last week's numbers
// plus anything needing attention (resupply, dormant packs) — the dashboard
// comes to you instead of you remembering to open it. After pasting, add a
// time-driven trigger: weeklyDigest, week timer, every Monday, 7–8 AM.
function weeklyDigest() {
  const ss = SpreadsheetApp.getActive();
  const reds = ss.getSheetByName(SHEET).getDataRange().getValues().slice(1);
  const packs = ss.getSheetByName(PACKS).getDataRange().getValues().slice(1);
  const now = Date.now(), inWeek = r => now - new Date(r[0]).getTime() <= 7 * 86400000;
  const n = s => reds.filter(r => inWeek(r) && String(r[3]) === s).length;
  // pack size from its card-serial range (defaults to 50)
  const size = p => { const a = Number(String(p[2]).slice(10, 18)), b = Number(String(p[3]).slice(10, 18));
                      return a && b && b >= a ? b - a + 1 : 50; };
  const okByPack = {};
  reds.forEach(r => { if (String(r[3]) === 'ok' && r[5]) okByPack[String(r[5])] = (okByPack[String(r[5])] || 0) + 1; });
  const latest = {};   // bar -> newest non-voided pack row
  packs.forEach(p => { const bar = String(p[4] || '');
    if (bar && !String(p[5] || '').trim() &&
        (!latest[bar] || String(p[1]) > String(latest[bar][1]))) latest[bar] = p; });
  const attn = [];
  for (const bar in latest) {   // provably >50% through the last pack
    const p = latest[bar], used = okByPack[String(p[1])] || 0;
    if (used > size(p) / 2)
      attn.push('RESUPPLY ' + bar + ' — ' + used + ' of ' + size(p) + ' cards from their last pack already redeemed');
  }
  packs.forEach(p => {          // checked out 3+ weeks ago, never redeemed from
    const age = (now - new Date(p[0]).getTime()) / 86400000;
    if (age >= 21 && !String(p[5] || '').trim() && !okByPack[String(p[1])])
      attn.push('DORMANT pack ' + String(p[1]) + ' at ' + String(p[4]) + ' — checked out ' +
                Math.round(age) + ' days ago, no redemptions yet');
  });
  const body = 'Knox Pick-Me-Up — week in review\n\n' +
    'Coffees redeemed: ' + n('ok') + '\nDuplicates refused: ' + n('dup') +
    '\nVoided-pack attempts: ' + n('void') + '\nBad serials: ' + n('bad') +
    '\nPacks checked out: ' + packs.filter(inWeek).length + '\n\n' +
    (attn.length ? 'Needs attention:\n- ' + attn.join('\n- ') : 'Nothing needs attention.') +
    '\n\nDashboard: <your GitHub Pages URL>/dashboard.html';
  MailApp.sendEmail(Session.getEffectiveUser().getEmail(),
    'Pick-Me-Up weekly: ' + n('ok') + ' coffees' + (attn.length ? ' — ' + attn.length + ' item(s) need attention' : ''),
    body);
}
```

`redeem.html` calls it with a GET and shows the barista **"Good to go"** or
**"Card already redeemed at ‹shop›"** in real time.

### C. The scanner: `redeem.html` (this repo, GitHub Pages)
Already built. Brand-styled, self-contained static page:
- opens from a per-shop QR (`redeem.html?shop=slug`), shows which shop it's
  logging for;
- tap-to-start camera with live detection feedback (polygon over the code,
  serial chip, outcome-colored reticle, scan line, torch toggle) and a stop
  button; native `BarcodeDetector` where available, vendored
  [jsQR](../assets/vendor/jsQR.min.js) (Apache-2.0, minified) everywhere
  else — **lazy-loaded only at camera start on browsers that need it**, so
  the page itself is a ~20 KB instant load;
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
(issued, redeemed, redemption rate, last 7 days), redemptions per day/week,
a day-of-week × hour heatmap of when coffees get claimed, ranked
**to-shop** and **from-bar** charts, a bar → shop flow matrix, and the
latest activity — with 7/30/90-day/all-time range chips and a 5-minute
auto-refresh. An **Admin info** toggle adds the coordinator's view:
integrity tiles and spike plots (duplicates, voided-pack attempts, bad
serials), a **resupply warning** when a bar is provably more than halfway
through its last pack, a **dormant-pack warning** for packs three-plus
weeks old with no redemptions, **days of cards left** per bar (stock ÷
trailing burn rate), **redemption rate by bar**, **monthly cap tracking**
per shop, and **duplicate forensics** that separates a copied card
circulating between shops from a harmless register double-scan.

**Access: shareable by link, on purpose.** The page isn't linked from the
public site and carries `noindex`, so the URL travels by word of mouth —
but anyone you hand it to (the City, KPD, a reporter, a prospective
partner) can open it and watch the numbers live. That works because the
payload is venue names, timestamps, statuses, and counts only — patron
data never exists, and the only card serials that leave the Sheet are
those of *refused* scans (already redeemed, voided, or invalid), which
grant nothing and power the duplicate forensics. With `SCRIPT_URL` unset
the page renders generated demo data, so you can try it right now.

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

### H. Backups & disaster recovery

"What if someone breaks the sheet?" is handled in four independent layers,
none of which you have to remember to run:

| Layer | What it protects against | Where it lives | Effort |
|---|---|---|---|
| 1. **Sheet version history** | a bad edit, a deleted column, a broken formula | built into Google Sheets (File → Version history → See version history) | zero — automatic |
| 2. **Nightly Drive snapshot** | a mangled or deleted *tab*, script accidents | `nightlySnapshot()` in the same Apps Script + one daily trigger; keeps 30 dated copies in a "KPMU Backups" Drive folder | one-time trigger setup |
| 3. **Nightly off-Google backup** | Google account lockout, Drive loss, "I just don't trust Google" | [`.github/workflows/backup.yml`](../.github/workflows/backup.yml) pulls every tab via the key-gated `backup` action and commits CSVs to `data/backup/` in this repo — **git history is the archive**, so every past day is recoverable | two repo secrets |
| 4. **Print artifacts** | everything digital at once | pack cover sheets have a hand-written bar/date line; cards are physically stamped | already in the workflow |

**Hardening the sheet against "someone breaks something":**
- Share the Sheet with **no editors**. The Apps Script runs as the owner and
  the pack form writes through Google's own plumbing — nobody else needs
  edit access, ever. Give the City/partners the dashboard link, not the sheet.
- Protect the `Redemptions` tab (right-click tab → Protect sheet → only the
  owner). The script still writes; stray humans can't.
- The one column humans touch on purpose (`Packs.voided`) stays editable.

**Restore runbook** (worst case — the sheet is ruined):
1. Try **File → Version history** first; restoring a version fixes 95% of
   accidents in one click.
2. Else open the newest copy in the **KPMU Backups** Drive folder, rename it,
   and repoint nothing — instead copy its tabs back into the original file
   (the Apps Script and form are bound to the original's ID; keeping that
   file alive is simpler than re-deploying).
3. Else pull `data/backup/*.csv` from this repo (or any older version via
   `git log -- data/backup`) and File → Import → each CSV into its tab.
4. If the whole Google account is lost: create a new Sheet from the CSVs,
   re-paste the Apps Script, re-deploy, and update `SCRIPT_URL` in
   `redeem.html`/`dashboard.html` and the two GitHub secrets. That is the
   entire blast radius — under an hour.

**Failure alerting for free:** after setup, a failed nightly backup fails
the GitHub Action, and GitHub emails the repo owner. No pager, no service.

### I. Businesses joining or leaving

The system is designed so the roster can churn without touching any data:

**A coffee shop joins:** add one line to the `SHOPS` map in `redeem.html`
(slug → display name), merge, print their register QR, and add them to the
`Venues` tab — including their agreed monthly redemption cap in the cap
column, if they set one (the dashboard tracks month-to-date against it). Their name appears in the dashboard automatically with their
first scan — every chart and the flow matrix build their axes from the
data, uncapped, and the matrix scrolls as the roster grows.

**A coffee shop leaves (deactivation):** put anything in its `deactivated`
cell on the `Venues` tab (e.g. `left 9/15`) — the dashboard immediately
shows it **greyed out with a "deactivated" note** wherever it appears,
while its history stays visible (correct — those coffees happened). Then
remove its `SHOPS` line and take back the register QR. A scan from a stale
register QR still logs, labeled as an unknown shop code, so nothing is
silently lost while the change propagates. Clearing the cell reactivates
it. Don't delete the Venues row — the row is what keeps the display name
and the grey-out working for historical data.

**A bar joins:** add it to the pack form's Bar dropdown (a one-minute
Google Forms edit) and the `Venues` tab, then check packs out to it as
usual. Attribution flows from the pack records — nothing else to update.

**A bar leaves (deactivation):** mark it `deactivated` on the `Venues` tab
(the dashboard greys it out with a note, keeping its history), void its
unredeemed packs (the kill-switch column) so outstanding cards stop
scanning, and remove it from the form dropdown. All historical attribution
is stored on the redemption rows at scan time, so past data never shifts.
Note: the bar's `Venues` display name must exactly match the name used in
the pack form dropdown — that's how the dashboard links them.

## 3. Setup runbook (one afternoon, in order)

1. Create the program Google account; create the Sheet with the three tabs.
2. Create the **pack form** (fields: pack serial, first card serial, last
   card serial, bar dropdown), link it to the Sheet's `Packs` tab, and grab
   a pre-filled URL (⋮ → *Get pre-filled link*) to learn the three
   `entry.NNNN` IDs.
3. Paste the Apps Script above into the Sheet; set `PROGRAM_KEY` — the one
   secret in the whole system (save it somewhere safe: print runs, register
   QRs, and backups all use it); deploy as web app, copy the `/exec` URL.
4. In this repo: set `SCRIPT_URL` and the `SHOPS` map in `redeem.html`;
   set `SCRIPT_URL` in `dashboard.html`; set `PACK_FORM_URL` in
   `tools/build_cards.py`. Commit, merge — Pages redeploys.
5. Generate per-shop register QRs (any QR tool, or segno one-liner) pointing
   at `https://…/redeem.html?shop=<slug>`; print and laminate.
6. Run `tools/build_cards.py`, send `print/` to the print shop.
7. Build the Looker Studio dashboard on the Sheet; share view links.
8. Backups: add the daily `nightlySnapshot` trigger in the Apps Script; in
   this repo's Settings → Secrets → Actions add `BACKUP_URL` (the `/exec`
   URL) and `PROGRAM_KEY` (the same one secret), then run the "Nightly data
   backup" workflow once by hand to confirm a `data/backup/` commit appears.
   While you're in the trigger screen, add the weekly `weeklyDigest` trigger
   (Monday 7–8 AM) so the coordinator gets the week-in-review email.
9. Dry-run with one friendly bar + one shop before the real pilot.

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
