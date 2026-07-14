# Knox Park & Perk — Program Design

**Tagline:** *Make it home safe. Tomorrow's coffee's on us.*

A public-private partnership between the City of Knoxville, the Knoxville Police
Department, downtown bars, and downtown coffee shops. Patrons who drove downtown
and choose a rideshare home at the end of the night receive a **$5 Morning Perk
voucher**, redeemable at a participating coffee shop when they return the next
morning to retrieve their car.

---

## 1. The Problem & The Insight

People drive downtown, drink more than planned, and then face a choice: pay for
a ride home *and* a ride back tomorrow (plus the hassle), or just drive. The
parked car is the single biggest driver of impaired driving decisions.

**The insight:** don't fight the car — use it. The car guarantees the patron
returns downtown in the morning. Reward the safe choice at the exact moment it's
made (last call, at the bar) and cash it in at the exact moment it pays off
(the morning retrieval trip). Downtown gets the customer twice.

## 2. How It Works (Mechanics)

1. **Patron** drives downtown, parks, and goes out.
2. At the end of the night, patron **books a rideshare/taxi home** instead of driving.
3. Patron **shows the confirmed ride screen** to a bartender at a participating bar.
4. Bartender **date-stamps and hands over one Morning Perk voucher** ($5).
5. Patron returns in the morning, **redeems the voucher** at a participating
   coffee shop, and drives home sober.

### Voucher rules
- $5 face value; no cash value; overage paid by customer, underage not refunded.
- One voucher per person per night.
- Valid **36 hours** from date stamp (covers the morning-after window; prevents hoarding).
- Serialized (`KPP-YYYY-######`), date-stamped, and marked with the issuing bar's initials.

### Fraud & abuse controls
- **Serialization:** every voucher has a unique number; books of 50 are checked
  out to bars, so issuance is traceable per venue per week.
- **Two-touch validation:** bar stamp at issue, coffee shop log at redemption.
  Mismatched or duplicate serials are flagged in monthly reconciliation.
- **Short expiry** kills secondary-market and stockpiling value.
- **Low stakes by design:** the worst case of a gamed voucher is $5 of coffee.
  Controls are proportionate — the program must stay a 10-second interaction at
  the bar, or bartenders won't do it on a busy Saturday.
- **Bartender discretion is a feature:** staff already judge sobriety and IDs;
  they can decline a voucher without confrontation ("we're out tonight").

### Overnight parking
The program's promise collapses if the patron gets towed. The city partnership
includes **overnight amnesty in city-owned garages** (e.g., no ticketing/towing
for vehicles retrieved by noon), with signage in participating garages. Private
lot operators are recruited as sponsors with the same terms.

## 3. Branding

| Element | Spec |
|---|---|
| Name | **Knox Park & Perk** ("Park" = your car; "Perk" = the coffee, and the perk) |
| Tagline | *Make it home safe. Tomorrow's coffee's on us.* |
| Story arc | Night → Ride → Sunrise → Coffee (🌙 → 🚗 → ☕) |
| Palette | Midnight navy `#141d33`, cream `#fff7ec`, espresso `#3a2a1d`, sunrise orange `#ff8200` (a nod to Knoxville's favorite color), gold `#ffb95e` |
| Voice | Warm, wry, zero lecture. Never "don't drink and drive"; always "good call — coffee's on us." |
| Physical kit | Coasters ("Booked your ride? Show your bartender."), restroom mirror clings, table tents, window decals ("Perk Partner"), bartender stamp, voucher books |

Coasters are the hero medium: they sit under the drink at exactly the decision
moment, and bars go through thousands of them anyway — the program replaces a
cost with free branded stock.

## 4. Partner Value & Engagement Playbook

### Downtown bars — *the distribution network*
**Pitch:** "Free coasters and signage, a safer close to your night, reduced
dram-shop-adjacent risk, and your name on a city-backed safety program. The ask
is a 10-second stamp-and-hand at last call."
- Cost to join: $0. Program supplies all materials and voucher books.
- Engagement: start with 5–8 anchor venues in the Old City and Market Square
  whose owners talk to each other; founding-partner status (logo on vouchers,
  press) creates FOMO for the second wave.
- Staff onboarding: one laminated card behind the bar; 5-minute pre-shift brief;
  small monthly staff perk (e.g., coffee for the crew) to keep buy-in.

### Coffee shops — *the redemption network*
**Pitch:** "Guaranteed reimbursed morning traffic from the late-night crowd —
customers you don't currently get — plus your logo in every bar downtown."
- Reimbursed **full $5 face value monthly**; average tickets exceed $5, so
  redemptions are net-revenue-positive plus a new-customer channel.
- Redemption workflow: take voucher, ring as program tender, log serial (paper
  log or shared form), drop vouchers in the monthly reconciliation envelope.
- Recruit shops within a short walk of major garages first (Gay Street, Market
  Square, Old City).

### City of Knoxville — *funding & parking policy*
**Pitch:** "A positive-incentive complement to enforcement. One prevented DUI
crash saves more than a year of program vouchers. Plus measurable downtown
morning foot traffic."
- Asks: seed funding from safety/downtown-vitality budgets, overnight garage
  amnesty, inclusion in city communications.
- Offer: full transparency — quarterly issuance/redemption data by venue.

### Knoxville Police Department — *credibility & reach*
**Pitch:** "You get a carrot to pair with the stick. Every voucher is a
documented decision not to drive impaired."
- Asks: public endorsement, program mention at DUI-awareness moments (football
  Saturdays, New Year's), no enforcement role inside bars (keeps bar staff and
  patrons comfortable).
- KPD is a *supporter*, not an operator — the program must never feel like
  surveillance or a sobriety checkpoint.

### Sponsors — *scaling the fund*
Natural fits: rideshare companies (Uber/Lyft — the program literally drives
bookings), auto insurers, hospital systems / UT Medical Center (trauma
prevention), parking operators, downtown property owners, breweries'
community funds, UT athletics-adjacent brands for game-day surges.

### Outreach sequence
1. **City + KPD first** (credibility unlocks everything else) — one-pager + this site.
2. **3 anchor coffee shops** (redemption must exist before issuance).
3. **5–8 anchor bars** for the pilot footprint.
4. **Press launch** with city/KPD, tied to a high-risk weekend.
5. **Second wave** recruitment using pilot data.

## 5. Pilot Budget (6 months, illustrative)

| Item | Estimate |
|---|---|
| Vouchers redeemed: ~400/mo × $5 × 6 mo | $12,000 |
| Printing: coasters, vouchers, signage, stamps | $4,000 |
| Part-time coordinator (reconciliation, restock, partner care) | $9,000 |
| Launch marketing & press event | $3,000 |
| Contingency (~15%) | $4,000 |
| **Total pilot** | **~$32,000** |

Key ratio: every dollar spent is split roughly 40% direct patron benefit /
60% infrastructure at pilot scale; infrastructure share falls steeply as the
program scales. Note redemption ≠ issuance: industry gift-voucher redemption
rates suggest budgeting for 50–70% redemption of issued vouchers.

## 6. Metrics & Success Criteria

- **Primary:** vouchers issued and redeemed (by venue, by night of week).
- **Secondary:** late-night DUI arrests / single-vehicle incidents in the
  downtown zone (with KPD, acknowledging small-sample noise in a pilot).
- **Economic:** average redemption ticket size vs. $5; repeat-customer reports
  from coffee shops; overnight garage stays on program nights.
- **Qualitative:** bartender friction reports, patron surveys via QR on voucher.
- **Pilot success gates:** ≥60% of anchor bars actively issuing by month 2;
  ≥50% redemption rate; zero material fraud incidents; partner renewal intent.

## 7. Timeline

| Phase | Window | Milestones |
|---|---|---|
| Design & city buy-in | Months 0–2 | City/KPD MOU, parking amnesty policy, fund established |
| Partner recruitment | Months 2–3 | 3 coffee shops + 6 bars signed, materials printed |
| Pilot launch | Month 4 | Press event on a high-visibility weekend |
| Pilot run | Months 4–9 | Monthly reconciliation, mid-pilot tune-up |
| Evaluate & scale | Month 10+ | Public report, second-wave recruitment, sponsor expansion |

## 8. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Bartenders skip it on busy nights | 10-second workflow, staff perks, coasters do the marketing passively |
| Cars towed despite promise | City amnesty formalized *before* launch; garage signage; hotline on voucher |
| Perception of promoting drinking | Framing is strictly "safe ride home"; KPD/city endorsement; no alcohol-brand sponsors on patron-facing materials |
| Fraud (fake ride screens, duplicates) | $5 cap, serials, expiry, bartender discretion; accept small leakage as marketing cost |
| Coffee shops float too much cash | Monthly (or biweekly at first) reimbursement; cap per-shop monthly exposure at pilot |
| Program conflated with enforcement | KPD as endorser only; no data on individuals is ever collected — vouchers are anonymous |

---

*Contact: hello@knoxparkandperk.org · Knoxville, TN*
