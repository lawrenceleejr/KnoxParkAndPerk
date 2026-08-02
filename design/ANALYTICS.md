# Knox Pick-Me-Up — Website analytics & attribution

The site runs **Cloudflare Web Analytics** — cookieless, no consent banner,
nothing that identifies a person (that's the promise on
[`/privacy/`](../privacy/index.html)). This guide covers what it shows, and the
one trick that turns it into channel attribution: tagging the links and QR codes
you control.

## What you get for free (no tagging)

Open the Cloudflare dashboard → **Web Analytics → knoxpickmeup.org**:

- **Visits & page views** over time
- **Top pages / Paths** — where people land and what they read
- **Referrers** — the site that sent them. Instagram, Facebook, Google, a news
  article: these show up automatically, no setup.
- **Countries / regions** — Knoxville-area vs. out-of-town
- **Device, OS, browser**
- **Core Web Vitals** — real-world load speed

## What it does NOT show (and why nothing privacy-first does)

No age, gender, or interests. That data only exists by tracking people across the
whole web (Google Signals / ad networks), which needs cookies, a consent banner,
and would break the privacy page. Even in Google Analytics those panels come back
mostly empty at this scale. Your real audience signal is the **redemption data**
(which shops, which nights, how many) — not web stats.

## The one trick: tag what you control with `?src=`

Cloudflare's **Referrers** report catches inbound *links*. It can't tell a printed
**QR code** apart — every coaster, poster, and table tent just lands as "Direct."
To separate them, put a channel tag in the URL:

```
https://knoxpickmeup.org/?src=coaster#findus
```

The tag rides in the query string (**before** the `#` — a query after the
fragment isn't a real parameter and won't be tracked), and each distinct tag
shows up as its own row in Cloudflare's **Paths** report. Filter/search for
`src=` to see them.

### Canonical source names

Keep these consistent — a typo makes a separate row:

| Channel | `?src=` value |
|---|---|
| Coasters | `coaster` |
| Signage (tents / posters / window) | `sign` |
| Instagram bio link | `instagram` |
| Facebook | `facebook` |
| Email / newsletter | `email` |
| Press / news article | `press` |
| Slide deck or flyer | `deck` |

All lowercase, one word.

## Digital links — paste these directly

- Instagram bio: `https://knoxpickmeup.org/?src=instagram`
- Facebook: `https://knoxpickmeup.org/?src=facebook`
- Email signature: `https://knoxpickmeup.org/?src=email`
- Press kit: `https://knoxpickmeup.org/?src=press`

## Print QR codes — regenerate with `--src`

The marketing generators tag their QR automatically (defaults shown); override
per run:

```sh
python3 tools/build_coasters.py --src coaster
python3 tools/build_signage.py  --src sign
```

`--src ''` disables tagging. The tag is placed correctly before the `#findus`
fragment. The **card** QR is a redemption link (`/redeem/?shop=…`) and is
intentionally *never* tagged — it isn't a marketing channel.

## Reading it

Cloudflare → **Web Analytics → knoxpickmeup.org**:

- **Referrers** → social, search, and news, automatically.
- **Paths / Top pages** → search `src=` → your tagged coasters, signage, and
  links, each its own row. Compare counts to see what actually drives traffic.

## When to graduate

If you outgrow Cloudflare — you want first-class campaign reports, goals/funnels,
or per-city geography — **Plausible** or **Matomo** are the privacy-first step up
(still cookieless, still no age/gender). True age/gender/interests means Google
Analytics + cookies + a consent banner + walking back the privacy promise; only
worth it if a funder specifically demands it, and even then expect sparse data.
