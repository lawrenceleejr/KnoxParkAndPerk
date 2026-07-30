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
makes per-serial cards   opens the scanner's    redeem/?shop=slug      (the database)
+ pack cover sheets  →   admin check-out:   →   barista scans the      →       │
each card QR encodes     pick the bar, scan     card's QR with the             ▼
site URL with serial     the pack — 10 sec      phone camera → serial      built-in /dashboard/
                                                logged automatically       (Looker optional)
```

**The one clever trick — the card QR is dual-use.** Every card's QR encodes
`https://…/?c=KPMU-2026-00004217T#findus` — a plain link to the public site:

- A **patron** who scans it just lands on the shop map — the list of places
  that redeem the card. No login walls, nothing weird.
- The **shop scanner page** (`redeem/index.html`) doesn't *follow* the URL — it
  *reads* it with the camera and extracts the `KPMU-…` serial with a regex.

Same printed code, two behaviors, zero extra infrastructure.

**Venue attribution needs nobody to type a venue name, ever:**

- **Coffee shop** = which register QR opened the scanner
  (`redeem/?shop=wild-love`). Print one QR per shop, tape it by the till.
- **Bar** = the serial range. Packs of 50 are checked out per bar in the
  scanner's admin mode (scan the pack QR, pick the bar), so `serial → bar` is
  a range lookup in the Sheet.

## 2. Components in detail

### A. The database: one Google Sheet
Owned by a program Google account (make one — `knoxpickmeup@gmail.com` — so
this survives any individual volunteer). **How it gets written:** the
`Redemptions` tab is appended to by the **Apps Script web app** (below) every
time a barista scans — no form involved; the `Packs` tab is written by the
scanner's **admin pack check-out** (`checkout` action below); the
`Venues` tab and the `voided` column are edited **by hand**, rarely. Nothing
else ever writes to the file. Three tabs:

| Tab | Columns | Filled by |
|---|---|---|
| `Redemptions` | timestamp · serial · shop · status · **bar** · **pack serial** | Apps Script (below) |
| `Packs` | timestamp · **pack serial** · first card serial · last card serial · bar · **voided** | the admin `checkout` action (voided: you, by hand) |
| `Venues` | slug · display name · type (bar/shop) · joined date · **deactivated** · **monthly cap** (shops, optional) | admin check-out (new bars) + you, by hand |

**Pack serials** carry a leading **P** (`KPMU-YYYY-P####`) so a pack can never
be mistaken for a card (`KPMU-YYYY-########X`) anywhere in the data or by eye. The bar attribution is **stored on each redemption row at scan
time**: the Apps Script looks the card's serial up in `Packs` (which range
contains it) and writes the issuing bar and pack serial alongside the shop.
No formulas required for the join; keep a duplicate flag
(`=COUNTIF(B:B,B2)>1`) as a belt-and-suspenders check.

**Serial checksum — the anti-guessing letter.** Every card serial ends in
one letter (`KPMU-2026-00004217T`) that can't be computed without a secret,
so serials can't be minted by counting up from a card in hand. **There is
exactly one secret in the whole system** — `PROGRAM_KEY` — and the checksum
uses a key *derived* from it: `CK_KEY = hex(HMAC-SHA256(PROGRAM_KEY,
"serial-v1"))`, then `letter = HMAC-SHA256(CK_KEY, serial)` — over the whole
`KPMU-YYYY-########` body, not just the digits — mapped to a
24-letter alphabet (no I/O, which read as 1/0). The derivation is one-way,
which is what lets the derived key ride in each shop's **register QR**
(`redeem/?shop=slug&k=<derived>`): the scanner verifies every scanned
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
    // Honor the scan's own timestamp for offline-queued scans, so a batch
    // that reconnects hours later isn't all dated to flush time (which would
    // corrupt the dashboard's time-of-day heatmap). Trust it only if it
    // parses, isn't in the future, and isn't older than 2 days; else now.
    const when = (function () {
      const t = Date.parse(p.at || '');
      const now = Date.now();
      return (t && t <= now + 60000 && t >= now - 2 * 86400000) ? new Date(t) : new Date();
    })();
    const lock = LockService.getScriptLock();
    lock.waitLock(5000);                       // serialize concurrent scans
    try {
      const sh = SpreadsheetApp.getActive().getSheetByName(SHEET);
      if (checkLetter(serial.slice(0, -1)) !== serial.slice(-1)) {
        // fails the keyed checksum — mistyped or made up; log it and refuse
        sh.appendRow([when, serial, shop, 'bad', '', '']);
        out = { status: 'invalid' };
        return ContentService.createTextOutput(JSON.stringify(out))
          .setMimeType(ContentService.MimeType.JSON);
      }
      const src = lookupBar(serial);
      if (src.voided) {
        // pack was invalidated — refuse, but keep the attempt for the audit trail
        sh.appendRow([when, serial, shop, 'void', src.bar, src.pack]);
        out = { status: 'void' };
      } else {
        // columns B..D: serial | shop | status — only 'ok' rows count as redeemed
        const rows = sh.getRange(2, 2, Math.max(sh.getLastRow() - 1, 1), 3).getValues();
        const hit = rows.find(r => r[0] === serial && r[2] === 'ok');
        if (hit) {
          // refused, but logged so the dashboard can count duplicate attempts
          sh.appendRow([when, serial, shop, 'dup', src.bar, src.pack]);
          out = { status: 'duplicate', firstShop: hit[1] };
        } else {
          sh.appendRow([when, serial, shop, 'ok', src.bar, src.pack]);
          out = { status: 'ok', bar: src.bar };
        }
      }
    } finally {
      lock.releaseLock();
    }
  }
  if (p.action === 'checkout' && /^KPMU-\d{4}-P\d+$/i.test(p.pack || '')) {
    // Admin pack check-out (redeem/?admin): tie a printed pack to the bar
    // taking it. Gated by the DERIVED check key (the same k printed on
    // register QRs) so a drive-by request can't write Packs/Venues rows —
    // the admin phone arms itself by opening any register QR once. This is
    // a tripwire, not a vault: anyone holding a register QR has k, but they
    // could also just scan cards. Insert-only — a pack already in the sheet
    // is REFUSED (never duplicated or silently reassigned); to move a pack,
    // edit the Packs tab by hand.
    if ((p.k || '') !== CK_KEY) {
      return ContentService.createTextOutput(JSON.stringify({ status: 'denied' }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    const pack = p.pack.toUpperCase();
    const first = String(p.first || '').toUpperCase();
    const last = String(p.last || '').toUpperCase();
    const bar = String(p.bar || '').slice(0, 60);
    const lock = LockService.getScriptLock();
    lock.waitLock(5000);
    try {
      const sh = SpreadsheetApp.getActive().getSheetByName(PACKS);
      const rows = sh.getDataRange().getValues();
      let existing = null;
      for (let i = 1; i < rows.length; i++) if (String(rows[i][1]) === pack) { existing = rows[i]; break; }
      if (existing) {
        // already checked out — refuse, and report which bar has it
        out = { status: 'exists', pack: pack, bar: String(existing[4] || '') };
      } else {
        sh.appendRow([new Date(), pack, first, last, bar, '']);
        // make sure a newly-typed bar shows up as a venue for the dashboard
        const vs = SpreadsheetApp.getActive().getSheetByName('Venues');
        if (vs && bar) {
          const known = vs.getDataRange().getValues().slice(1)
            .some(r => String(r[1]).trim().toLowerCase() === bar.toLowerCase());
          if (!known) vs.appendRow([bar.toLowerCase().replace(/[^a-z0-9]+/g, '-'), bar, 'bar', new Date(), '', '']);
        }
        out = { status: 'ok', pack: pack, bar: bar };
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
    '\n\nDashboard: <your GitHub Pages URL>/dashboard/';
  MailApp.sendEmail(Session.getEffectiveUser().getEmail(),
    'Pick-Me-Up weekly: ' + n('ok') + ' coffees' + (attn.length ? ' — ' + attn.length + ' item(s) need attention' : ''),
    body);
}
```

`redeem/index.html` calls it with a GET and shows the barista **"Good to go"** or
**"Card already redeemed at ‹shop›"** in real time.

### C. The scanner: `redeem/index.html` (this repo, GitHub Pages)
Already built. Brand-styled, self-contained static page:
- opens from a per-shop QR (`redeem/?shop=slug`), shows which shop it's
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

### D. Pack check-out: the scanner's admin mode
Open `redeem/?admin=1` (or scan a pack's cover-sheet QR, which is a
`redeem/?pack=…&first=…&last=…` link, or tap the scanner's header five
times). Pick the bar from the list — **add a new one inline** if it isn't
there yet — then scan the pack's QR (or paste the code). That posts the
`checkout` action, which appends a `Packs` row (pack serial, card range, bar)
and adds any new bar to `Venues`. Check-out is **insert-only**: a pack already
in the sheet is refused (the scanner shows "already checked out to <bar>"), so
a double-scan can't duplicate or silently reassign it — to move a pack, edit
the `Packs` tab by hand. The cover sheet also has a written-log fallback line.
No Google Form needed.

Check-outs are **gated by the derived check key** — the same `k` every
register QR carries — so a random internet request can't write `Packs`/
`Venues` rows. The admin phone arms itself the first time it opens any
register QR (the key is remembered on the device); an unarmed device gets a
clear "open a register QR once" message instead of a silent failure.

### E. Card + pack printing: `tools/build_cards.py` (this repo)
`python3 tools/build_cards.py --year 2026 --start 1 --count 500` emits
per-serial card SVGs — each with a true-size print-ready PDF beside it — and
one cover sheet per 50 into `print/` (gitignored), ready for any print shop.
Unique QR per card is what makes scan-to-log possible.

### F. The admin dashboard: `dashboard/index.html` (this repo, GitHub Pages)
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
  is the only writer (redemptions and pack check-outs both go through it) —
  nobody else needs edit access, ever. Give the City/partners the dashboard
  link, not the sheet.
- Protect the `Redemptions` tab (right-click tab → Protect sheet → only the
  owner). The script still writes; stray humans can't.
- The one column humans touch on purpose (`Packs.voided`) stays editable.

**Restore runbook** (worst case — the sheet is ruined):
1. Try **File → Version history** first; restoring a version fixes 95% of
   accidents in one click.
2. Else open the newest copy in the **KPMU Backups** Drive folder, rename it,
   and repoint nothing — instead copy its tabs back into the original file
   (the Apps Script and its triggers are bound to the original's ID; keeping
   that file alive is simpler than re-deploying).
3. Else pull `data/backup/*.csv` from this repo (or any older version via
   `git log -- data/backup`) and File → Import → each CSV into its tab.
4. If the whole Google account is lost: create a new Sheet from the CSVs,
   re-paste the Apps Script, re-deploy, and update `SCRIPT_URL` in
   `redeem/index.html`/`dashboard/index.html` and the two GitHub secrets. That is the
   entire blast radius — under an hour.

**Failure alerting for free:** after setup, a failed nightly backup fails
the GitHub Action, and GitHub emails the repo owner. No pager, no service.

### I. Businesses joining or leaving

**Where the roster lives (keep these in step).** There is no single shared
data file, so a venue change touches a fixed, short list of places:

| Roster | File / location | Holds | Notes |
|---|---|---|---|
| Live data | Sheet → `Venues` tab | shops **and** bars | source of truth for the dashboard (display name, cap, deactivation) |
| Public map | `index.html` → `SHOPS` / `BARS` arrays | shops + bars | name + lat/lon pins |
| Map fallback | `index.html` → `.fallback` list | shops + bars | the no-JS / no-tiles list; must mirror the arrays above |
| Scanner seed | `redeem/index.html` → `SHOPS` (shop register) and `BARS` (check-out dropdown seed) | shops + bars | seeds only — bars can also be typed inline in admin mode |

(The roster in `dashboard/index.html` is illustrative **demo data** behind the
"demo data" badge, not a roster to maintain.)

The system is designed so the roster can churn without touching any data:

**A coffee shop joins:** add one line to the `SHOPS` map in `redeem/index.html`
(slug → display name) and one to the `SHOPS` roster in `index.html`'s map
(name + lat/lon pin), merge, print their register QR, and add them to the
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

**A bar joins:** just check a pack out to it in admin mode — type the new
bar's name inline and the `checkout` action adds it to `Venues` for you.
(Optionally seed it in the `BARS` roster in `redeem/index.html` so it's in
the dropdown without typing, and in `index.html`'s map for the name + pin.)
Attribution flows from the pack records — nothing else to update.

**A bar leaves (deactivation):** mark it `deactivated` on the `Venues` tab
(the dashboard greys it out with a note, keeping its history) and void its
unredeemed packs (the kill-switch column) so outstanding cards stop
scanning. All historical attribution is stored on the redemption rows at
scan time, so past data never shifts. Note: the bar's `Venues` display name
must exactly match the name used at check-out — that's how the dashboard
links them.

## 3. Setup runbook (one afternoon, in order)

1. Create the program Google account; create the Sheet with the three tabs
   (`Redemptions`, `Packs`, `Venues`).
2. Paste the Apps Script above into the Sheet; set `PROGRAM_KEY` — the one
   secret in the whole system (save it somewhere safe: print runs, register
   QRs, and backups all use it); deploy as web app, copy the `/exec` URL.
3. In this repo: set `SCRIPT_URL` and the `SHOPS` map in `redeem/index.html`
   (and optionally seed the `BARS` roster); set `SCRIPT_URL` in
   `dashboard/index.html`. Commit, merge — Pages redeploys.
4. Generate per-shop register QRs pointing at
   `https://…/redeem/?shop=<slug>&k=<derived>`, where `<derived>` is the check
   key from `tools/ckkey.py` (so the scanner can verify serials offline);
   print and laminate.
5. Run `tools/build_cards.py --key "$KPMU_PROGRAM_KEY"` (the same secret —
   **without it the cards are signed with the public demo key and won't
   validate**), then send `print/` to the print shop. See PRINTING.md.
6. The built-in dashboard is already live at `/dashboard/` from step 3 — share
   that link with partners. (Optionally also build a Looker Studio view on the
   Sheet if a partner wants their own charts.)
7. Backups: add the daily `nightlySnapshot` trigger in the Apps Script; in
   this repo's Settings → Secrets → Actions add `BACKUP_URL` (the `/exec`
   URL) and `PROGRAM_KEY` (the same one secret), then run the "Nightly data
   backup" workflow once by hand to confirm a `data/backup/` commit appears.
   While you're in the trigger screen, add the weekly `weeklyDigest` trigger
   (Monday 7–8 AM) so the coordinator gets the week-in-review email.
8. Dry-run with one friendly bar + one shop before the real pilot.

## 4. What this costs and what can break

**Cost:** $0. GitHub Pages, Google Sheets/Apps Script, and Looker
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
