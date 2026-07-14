# Knox Park & Perk — Program Design

**Tagline:** *Make it home safe. Tomorrow's coffee's on us.*

A public-private partnership between the City of Knoxville, the Knoxville Police
Department, Knoxville Area Transit (KAT), downtown bars, and downtown coffee
shops. Patrons who drove downtown and choose a safe ride home at the end of the
night — a rideshare, a taxi, or public transit — receive a **$5 Morning Perk
voucher**, framed as a *tip for making the safe, responsible choice*, redeemable
at a participating coffee shop when they return the next morning to retrieve
their car.

---

## 1. The Problem & The Insight

People drive downtown, drink more than planned, and then face a choice: pay for
a ride home *and* a ride back tomorrow (plus the hassle), or just drive. The
parked car is the single biggest driver of impaired driving decisions.

**The insight:** don't fight the car — use it. The car guarantees the patron
returns downtown in the morning. Reward the safe choice at the exact moment it's
made (last call, at the bar) and cash it in at the exact moment it pays off
(the morning retrieval trip). Downtown gets the customer twice.

**The framing:** the voucher is a **tip**. Patrons tip service staff all night;
Park & Perk is downtown tipping the patron back for the most valuable service of
the evening — getting home without driving. "Tip" keeps the tone warm and
non-preachy, makes the $5 feel like recognition rather than a coupon, and sets
up patron-side funding mechanics ("Perk It Forward," below) where tonight's
crowd tips tomorrow's safe riders.

## 2. How It Works (Mechanics)

1. **Patron** drives downtown, parks, and goes out.
2. At the end of the night, patron **takes a safe ride home** instead of driving —
   a booked rideshare/taxi, or a KAT bus or trolley.
3. Patron **shows proof of the ride** to a bartender at a participating bar: a
   confirmed rideshare screen or an activated transit ticket.
4. Bartender **date-stamps and hands over one Morning Perk voucher** ($5) per
   ride.
5. Patron returns in the morning, **redeems the voucher** at a participating
   coffee shop, and drives home sober.

### Voucher rules
- $5 face value; no cash value; overage paid by customer, underage not refunded.
- **One voucher per ride** — the ride is the ticket. Accepted proof: a confirmed
  rideshare/taxi, or an activated KAT bus or trolley ticket. A group sharing one
  Uber gets one card (the booker's). Two rides, two cards.
- Valid **two days** from date stamp (covers the morning-after window; prevents hoarding).
- Serialized (`KPP-YYYY-######`), date-stamped, and marked with the issuing bar's initials.

### Fraud & abuse controls
- **Serialization:** every voucher has a unique number; books of 50 are checked
  out to bars, so issuance is traceable per venue per week.
- **One-per-ride rule** is self-limiting: a voucher requires a distinct booked
  ride shown at the bar, and the bartender stamps at the moment of proof.
- **Two-touch validation:** bar stamp at issue, coffee shop log at redemption.
  Mismatched or duplicate serials are flagged in monthly reconciliation.
- **Short expiry** kills secondary-market and stockpiling value.
- **Low stakes by design:** the worst case of a gamed voucher is $5 of coffee.
  Controls are proportionate — the program must stay a 10-second interaction at
  the bar, or bartenders won't do it on a busy Saturday.
- **Bartender discretion is a feature:** staff already judge sobriety and IDs;
  they can decline a voucher without confrontation ("we're out tonight").

### Overnight parking
Leaving the car overnight has to feel free and safe, or the program falls apart.
Fortunately Knoxville already provides this: **parking in the City's municipal
garages is free on evenings and weekends.** The program doesn't need to
negotiate a parking policy — it just needs to *advertise* the free-parking
reality loudly (on coasters, cards, and signage) so patrons stop treating "but
my car" as a reason to drive. Coordinate messaging with the City so posted
garage hours and any move-out times are stated accurately; recruit private lot
operators as sponsors where a garage isn't nearby.

## 3. Branding

| Element | Spec |
|---|---|
| Name | **Knox Park & Perk** ("Park" = your car; "Perk" = the coffee, and the perk) |
| Tagline | *Make it home safe. Tomorrow's coffee's on us.* |
| Core frame | The voucher is a **tip** for making the safe, responsible choice — recognition, not a coupon |
| Story arc | Night → Ride → Sunrise → Coffee (🌙 → 🚗 → ☕) |
| Palette | Midnight navy `#141d33`, cream `#fff7ec`, espresso `#3a2a1d`, sunrise orange `#ff8200` (a nod to Knoxville's favorite color), gold `#ffb95e` |
| Voice | Warm, wry, zero lecture. Never "don't drink and drive"; always "good call — coffee's on us." Promise "free coffee downtown," never oversell ($5 is a coffee, not breakfast). |
| Physical kit | Coasters ("Booked your ride? Show your bartender."), restroom mirror clings, table tents, window decals ("Perk Partner"), bartender stamp, voucher books |

Coasters are the hero medium: they sit under the drink at exactly the decision
moment, and bars go through thousands of them anyway — the program replaces a
cost with free branded stock.

## 4. Monetization & Sustainability

The funding model is deliberately open — it will be locked with partners as
they come on board. The design constraint is fixed: **the perk is always free to the
patron who took the safe ride.** Candidate revenue streams, roughly in order of
long-run sustainability:

### A. Merchant-funded ("coupon economics") — the self-sustaining core
Coffee shops honor the $5 card as their own customer-acquisition cost, the way
they'd fund any promotion. The math that makes it rational: the card brings in
a late-night demographic they rarely see before noon, average morning tickets
exceed $5, and a good first visit creates a repeat customer. Shops can cap
monthly redemptions while the model proves out.
*Pro:* zero external money needed; scales automatically with participation.
*Con:* asks the smallest businesses to carry the direct cost; needs early
ticket-size data to keep shops convinced.

### B. Perk It Forward (patron round-up) — the tip loop
An optional $1 line on bar tabs: tonight's patrons "tip" tomorrow's safe
riders. This is the purest expression of the brand — the community literally
tips people for getting home safe — and even modest uptake at busy venues
funds a large share of vouchers.
*Pro:* on-brand, visible, feels like Knoxville looking after Knoxville.
*Con:* revenue varies with uptake; needs simple POS handling and transparent
accounting (publish the pot monthly).

### C. Sponsorship tiers — the accelerant
Annual "presented by" packages for brands whose economics align with fewer
impaired drivers and more rides: rideshare companies (the program drives
bookings), auto insurers, hospital/trauma systems, parking operators, downtown
property owners. Sponsor logos ride on coasters and vouchers already in every
bar downtown — unusually good placement per dollar.
*Pro:* covers fixed costs (printing, coordinator) that per-voucher models don't.
*Con:* renewal risk; keep alcohol brands off patron-facing materials.

### D. Bar partner dues — optional, later
A modest monthly membership once the program has proven foot-traffic and
goodwill value. Not recommended for the pilot: bars joining free is what makes
the network dense enough to matter.

### E. Grants & city seed — launch only
One-time money (highway-safety grants, downtown-vitality funds, community
foundations) for the pilot's fixed costs. Treated strictly as seed, never as
the operating model.

**Recommended architecture:** A as the base (vouchers cost the program nothing
in cash), B as the community flywheel and story, C to cover fixed costs, E to
get off the ground. D held in reserve. Under this structure the marginal cost
of one more safe ride home is approximately zero to the program — which is
what makes it durable.

### Pilot fixed costs (6 months, illustrative)

| Item | Estimate |
|---|---|
| Printing: coasters, vouchers, signage, stamps | $4,000 |
| Part-time coordinator (reconciliation, restock, partner care) | $9,000 |
| Launch marketing & press event | $3,000 |
| Contingency | $2,000 |
| **Total fixed** | **~$18,000** (voucher face value carried per model A/B above) |

## 5. Partner Value & Engagement Playbook

### Downtown bars — *the distribution network*
**Pitch:** "Free coasters and signage, a safer close to your night, reduced
dram-shop-adjacent risk, and your name on a city-backed safety program. The ask
is a 10-second stamp-and-hand at last call."
- Cost to join: $0 at pilot. Program supplies all materials and voucher books.
- Engagement: start with 5–8 anchor venues in the Old City and Market Square
  whose owners talk to each other; early-partner billing (logo on vouchers,
  press) creates FOMO for the second wave.
- Staff onboarding: one laminated card behind the bar; 5-minute pre-shift brief;
  small monthly staff perk (e.g., coffee for the crew) to keep buy-in.
- Perk It Forward: venues that opt in add the $1 round-up line and get
  "Community Tipper" billing.

### Coffee shops — *the redemption network*
**Pitch:** "Morning traffic from the late-night crowd — customers you don't
currently get — plus your logo in every bar downtown. You control your exposure
with a monthly cap while we prove the ticket math together."
- Redemption workflow: take voucher, log serial, done. Monthly data shared back
  (redemptions, average ticket uplift) so the value is visible.
- Recruit shops within a short walk of major garages first (Gay Street, Market
  Square, Old City).
- Coffee shops help pick the funding architecture (Section 4) — real
  co-ownership, not a terms sheet.

### City of Knoxville — *credibility & promotion*
**Pitch:** "A positive-incentive complement to enforcement. One prevented DUI
crash costs the city more than this program's entire pilot. The asks are mostly
promotion, not an open-ended budget line."
- Asks: co-promote the already-free evening/weekend municipal garage parking,
  inclusion in city communications, optional one-time seed for launch costs.
- Offer: full transparency — quarterly issuance/redemption data by venue.

### Knoxville Police Department — *credibility & reach*
**Pitch:** "You get a carrot to pair with the stick. Every voucher is a
documented decision not to drive impaired."
- Asks: public endorsement, program mention at DUI-awareness moments (football
  Saturdays, New Year's), no enforcement role inside bars.
- KPD is a *supporter*, not an operator — the program must never feel like
  surveillance or a sobriety checkpoint. Vouchers are anonymous; no personal
  data is ever collected.

### Knoxville Area Transit (KAT) — *an accepted ride & a service partner*
**Pitch:** "Riders already using the bus or the free downtown trolley to get
home safely should qualify for the perk too. Being an accepted proof puts KAT
in front of the exact crowd that needs a late ride, and drives off-peak
ridership."
- Asks: recognize an activated KAT bus/trolley ticket as valid proof; help
  communicate late-night and weekend routes/hours to patrons and bar staff.
- Offer: co-branding on materials; a reason for the bar crowd to try transit.
- Longer term: coordinate service/marketing around the highest-risk nights so
  a bus home is a genuinely easy option, not just an eligible one.

### Outreach sequence
1. **City + KPD first** (credibility unlocks everything else) — one-pager + this site.
2. **3 anchor coffee shops** (redemption must exist before issuance; they
   co-design the funding model).
3. **5–8 anchor bars** for the pilot footprint.
4. **KAT** to confirm transit tickets as accepted proof and align late-night service messaging.
5. **Sponsors** once the partner map makes the placement value concrete.
6. **Press launch** with city/KPD, tied to a high-risk weekend.
7. **Second wave** recruitment using pilot data.

## 6. Metrics & Success Criteria

- **Primary:** vouchers issued and redeemed (by venue, by night of week).
- **Secondary:** late-night DUI arrests / single-vehicle incidents in the
  downtown zone (with KPD, acknowledging small-sample noise in a pilot).
- **Economic:** average redemption ticket size vs. $5 face value (the number
  that proves model A); repeat-customer reports from coffee shops; Perk It
  Forward uptake rate; overnight garage stays on program nights.
- **Qualitative:** bartender friction reports, patron surveys via QR on voucher.
- **Pilot success gates:** ≥60% of anchor bars actively issuing by month 2;
  ≥50% redemption rate; average redemption ticket ≥2× face value; zero material
  fraud incidents; partner renewal intent.

## 7. Timeline

| Phase | Window | Milestones |
|---|---|---|
| Design & city buy-in | Months 0–2 | City/KPD MOU, free-parking co-promotion agreement |
| Partner recruitment | Months 2–3 | 3 coffee shops + 6 bars + KAT signed; funding architecture locked with partners; materials printed |
| Pilot launch | Month 4 | Press event on a high-visibility weekend |
| Pilot run | Months 4–9 | Monthly reconciliation, mid-pilot tune-up |
| Evaluate & scale | Month 10+ | Public report, second-wave recruitment, sponsor expansion |

## 8. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Bartenders skip it on busy nights | 10-second workflow, staff perks, coasters do the marketing passively |
| Patron fears a ticket or tow for leaving the car | Lead with the fact that municipal garages are free evenings/weekends; confirm garage hours with the City; print them on signage; hotline on voucher |
| Perception of promoting drinking | Framing is strictly "safe ride home"; KPD/city endorsement; no alcohol-brand sponsors on patron-facing materials |
| Fraud (fake ride screens, duplicates) | $5 cap, one-per-booked-ride, serials, expiry, bartender discretion; accept small leakage as marketing cost |
| Redemption load concentrates on a few coffee shops | Per-shop monthly caps at pilot; recruit shops near every major garage; publish redemption spread |
| Coffee shops lose faith in the coupon math | Share ticket-uplift data monthly; Perk It Forward / sponsor funds can backstop face value if model A underperforms |
| Program conflated with enforcement | KPD as endorser only; vouchers anonymous — no data on individuals is ever collected |

---

*Contact: hello@knoxparkandperk.org · Knoxville, TN*
