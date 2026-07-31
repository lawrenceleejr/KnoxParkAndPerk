// =============================================================================
// Knox Pick-Me-Up — Program Details
// =============================================================================
// THIS is the file to edit. It holds all the words. The design lives in
// `template.typ`; you rarely need to open it.
//
// How to edit:
//   • Prose is plain text. *bold* is bold, _italic_ is italic, --- is an
//     em dash, and straight "quotes" become curly automatically.
//   • Write a dollar sign as \$  (a bare $ starts a math formula in Typst).
//   • Each section starts with  #sect(...)  — change the title, subtitle, or
//     body freely. The table of contents and all page numbers update by
//     themselves; you never hand-number anything.
//   • #sect(..., brk: false) lets a short section share a page with the one
//     before it instead of starting a new page.
//
// How to preview / export a PDF:
//   • Easiest, no install: upload this folder to https://typst.app — it edits
//     in the browser with a live preview and exports the PDF. (Great for
//     collaborators.)
//   • Command line:  typst compile --font-path fonts program-details.typ
// =============================================================================

#import "template.typ": *
#show: conf

// -----------------------------------------------------------------------------
#cover()

// ---- Contents ---------------------------------------------------------------
#eyebrow[Contents]
#v(4pt)
#text(font: serif, weight: 600, size: 24pt)[Program Details]
#v(6pt)

#tocgroup("The one-page idea")
#tocrow("", "Executive summary", "execsummary")

#tocgroup("Part I · The Opportunity")
#tocrow("1", "The problem", "s_problem")
#tocrow("2", "The insight", "s_insight")
#tocrow("3", "The idea, in one line", "s_idea")

#tocgroup("Part II · How It Works")
#tocrow("4", "The patron journey", "s_journey")
#tocrow("5", "The Morning Pick-Me-Up Card", "s_card")
#tocrow("6", "Trust by design", "s_trust")
#tocrow("7", "The car stays put", "s_parking")

#tocgroup("Part III · Why It Works for Everyone")
#tocrow("8", "Downtown bars", "s_bars")
#tocrow("9", "Coffee shops", "s_shops")
#tocrow("10", "City of Knoxville & KPD", "s_city")
#tocrow("11", "Knoxville Area Transit (KAT)", "s_kat")
#tocrow("12", "Downtown Parking Authority", "s_park")
#tocrow("13", "Sponsors", "s_sponsors")

#tocgroup("Part IV · Making It Real")
#tocrow("14", "What we ask of you", "s_ask")
#tocrow("15", "Built to sustain itself", "s_fund")
#tocrow("16", "The pilot", "s_pilot")
#tocrow("17", "How we'll know it's working", "s_metrics")
#tocrow("18", "Risks, and how we've handled them", "s_risks")
#tocrow("19", "Frequently asked questions", "s_faq")

#tocgroup("Summary")
#tocrow("", "The invitation", "s_invite")

#tocgroup("Appendices")
#tocrow("A", "Technical architecture", "a_tech")
#tocrow("B", "The card & anti-forgery serialization", "a_serial")
#tocrow("C", "Data, privacy, & backups", "a_privacy")
#tocrow("D", "The print kit & production", "a_print")
#tocrow("E", "Financial detail", "a_finance")
#tocrow("F", "Evidence & references", "a_refs")
#tocrow("G", "Brand at a glance", "a_brand")
#tocrow("H", "Forking this for your community", "a_fork")

// ---- Executive summary ------------------------------------------------------
#sect("", "", "Executive summary", "", "execsummary")

#block(width: 6.05in)[#lead[
  Impaired driving keeps hurting people on Knoxville's roads --- in the region,
  crashes involving an impaired driver seriously injure about *67 people and
  kill 27 every year*, and *one in three* Knox County crash deaths involves an
  impaired driver.#refn[13] The single biggest reason people talk themselves
  into driving home is the car they parked downtown.
]]

#block(width: 6.05in)[
  *Knox Pick-Me-Up doesn't fight the car --- it uses it.* A patron who drove
  downtown and chooses a safe ride home --- a rideshare, a taxi, or a KAT bus
  --- shows that ride to a bartender and gets a *Morning Pick-Me-Up Card*: good
  for a _free large coffee_ at a participating shop when they come back the
  next morning for their car, and a free KAT ride to get there. The card is
  framed as a _thank-you_ for keeping our roads safe --- not a coupon, and
  never a lecture.
]

#band[
  #eyebrow("The loop, in one line", fill: gold)
  #v(12pt)
  #loop((
    ([1], [Drive downtown, park]),
    ([2], [Take a safe ride home]),
    ([3], [Show the ride, get the card]),
    ([4], [Free KAT ride back]),
    ([5], [Free coffee, drive home sober]),
  ), dark: true)
]

#subhead[Why it works for everyone]
#block(width: 6.05in)[
  Bars get free branded coasters, a safer close, and their name on a city-backed
  safety program for a 10-second hand-off. Coffee shops get morning traffic from
  a late-night crowd they rarely see. The City and KPD get a positive-incentive
  complement to enforcement. KAT gets first-time riders. The Downtown Parking
  Authority gets its free-nights-and-weekends message in front of the exact
  people who need it. Sponsors get their name on the safe ride home, in every
  bar downtown.
]

#subhead[The ask, and the cost]
#block(width: 6.05in)[
  The coffee is carried by the shops as customer acquisition --- the way they'd
  fund any promotion --- and KAT rides are KAT's in-kind contribution, so the
  program's only real cash need is a modest set of pilot fixed costs (printing,
  a part-time coordinator, and launch) on the order of *\~\$18,000* for six
  months. The marginal cost of one more safe ride home is essentially zero. One
  prevented crash pays for the entire pilot many times over.#refn[1]
]

// =============================================================================
// PART I
// =============================================================================
#partdivider("Part I", "The Opportunity",
  "The problem worth solving, the insight that makes this different, and the whole idea in a single line.",
  (([1], [The problem]), ([2], [The insight]), ([3], [The idea, in one line])))

#sect("1", "Part I · The Opportunity", "The problem",
  "Impaired driving on Knoxville's roads, and the moment of decision at last call.", "s_problem")

#twocol[
  People drive downtown, drink more than they planned, and then face a choice:
  pay for a ride home _and_ a ride back tomorrow --- plus the hassle of
  retrieving the car --- or just drive. Told that way, the parked car does most
  of the arguing for driving.

  #colbreak()
  The human cost of the choice going wrong is not abstract in Knoxville. It
  falls on families, on emergency rooms, and on the people in the other car.
  Enforcement and education both matter, but neither changes the incentives a
  person actually weighs at 1 a.m. with a car half a block away.
]

#v(4pt)
#statband("The toll, every year", (
  ([67], [people seriously injured in area crashes involving an impaired driver#refn[13]]),
  ([27], [people killed in those crashes, each year#refn[13]]),
  ([1#h(3pt)#text(size: 24pt)[in]#h(3pt)3], [Knox County crash deaths involves an impaired driver#refn[13]]),
))

#v(6pt)
#block(width: 6.05in)[#note[
  Sources: Knoxville Regional Transportation Planning Organization (annual
  injuries and fatalities in area impaired-driving crashes); Knox County Health
  Department (share of deadly crashes involving an impaired driver).
]]

#sect("2", "Part I · The Opportunity", "The insight",
  "Don't fight the parked car --- use it. Reward the safe choice when it's made, and cash it in when it pays off.", "s_insight")

#block(width: 6.05in)[#lead[
  The car that makes people want to drive is also a guarantee: it means the
  patron _will_ be back downtown in the morning. That's the opening.
]]

#twocol[
  Knox Pick-Me-Up rewards the safe choice at the exact moment it's made --- last
  call, at the bar --- and lets the patron cash it in at the exact moment the
  choice pays off: the morning trip back for the car. Downtown gets the visitor
  twice, and one more impaired driver stays off the road.

  #colbreak()
  The framing carries the whole program. The card is a *thank-you*, not a coupon
  --- Knoxville recognizing the most valuable thing a patron did all night,
  which was getting home without driving. Warm and non-preachy, it makes a free
  coffee feel like recognition rather than a payout.
]

#callout([
  "Good call --- coffee's on us."
], [
  The voice, everywhere: warm, wry, zero lecture. Never "don't drink and
  drive"; always a thank-you for the safe ride home.
])

#sect("3", "Part I · The Opportunity", "The idea, in one line",
  "Last call → ride home → morning → coffee. One loop that closes itself.", "s_idea")

#band[
  #loop((
    ([1], [Drove downtown, parked the car]),
    ([2], [Took a safe ride home instead]),
    ([3], [Showed the ride, got a dated card]),
    ([4], [Free KAT ride back downtown]),
    ([5], [Free coffee, then drove home sober]),
  ), dark: true)
]

#block(width: 6.05in)[#lead[
  Every step is something the patron already wanted to do, made a little easier
  or a little more rewarding. The card is the thread that ties the safe choice
  at night to the payoff in the morning --- and because the reward waits until
  the next day, it can only be claimed by someone who genuinely left the car and
  came back for it.
]]

#block(width: 6.05in)[
  The rest of this document is simply that loop, told from each partner's point
  of view --- how it works at the bar, at the counter, and on the bus; why every
  partner comes out ahead; and how it pays for itself.
]

// =============================================================================
// PART II
// =============================================================================
#partdivider("Part II", "How It Works",
  "The patron's six steps, the card itself, the trust that keeps it honest, and the parked car that makes it all possible.",
  (([4], [The patron journey]), ([5], [The Morning Pick-Me-Up Card]), ([6], [Trust by design]), ([7], [The car stays put])))

#sect("4", "Part II · How It Works", "The patron journey",
  "Six steps, most of which the patron was going to take anyway.", "s_journey")

#steps((
  ([Out for the night], [Patron drives downtown, parks, and goes out.]),
  ([Chooses a safe ride home], [At the end of the night, they take a booked rideshare or taxi, or a KAT bus --- instead of driving.]),
  ([Shows proof of the ride], [They show a bartender a confirmed rideshare screen or an activated transit ticket --- a 10-second glance.]),
  ([Gets a Morning Pick-Me-Up Card], [The bartender writes today's date on the card and hands it over --- one card per ride.]),
  ([Rides KAT free back to the car], [While valid, the card doubles as a free KAT pass --- "Hair of the KAT" --- including the morning trip back downtown.]),
  ([Claims the coffee, drives home sober], [At a participating shop the next morning, they redeem a free large coffee, retrieve the car, and drive home clear-headed.]),
))

#callout([
  The reward waits until morning --- on purpose.
], [
  Because the coffee can only be claimed the next day, at the car, the card
  structurally can't reward anything except actually leaving the car overnight
  and coming back for it.
])

#sect("5", "Part II · How It Works", "The Morning Pick-Me-Up Card",
  "A wallet-sized thank-you: one free large coffee, and a free ride to come get it.", "s_card")

#cardrow[
  This is the card itself. It's good for one free large coffee, and --- while
  it's valid --- free KAT fare for the ride back to the car. The bartender
  writes the date by hand at hand-out, and a unique serial and QR make every
  card traceable and one-time.
]

#subhead[Card rules, in plain terms]
#list(
  [*One card per ride* --- the ride is the ticket. A group sharing one Uber gets one card; two rides, two cards. Cards are handed out while supplies last, so a bar that's out for the night can simply say so.],
  [*Valid one day from issue.* The bartender writes the date by hand at hand-out; that written date is both the record and the start of the one-day window --- long enough for the morning-after trip, short enough to prevent hoarding.],
  [*"Hair of the KAT."* A valid card is free KAT fare during its window --- show it to board any bus, including the ride back to the car.],
  [*Designated-driver exception, bartender's call.* A sober driver taking everyone home is the exact behavior the program rewards; a bartender may hand them a card at their discretion. A tool for staff, not a patron entitlement.],
)

#sect("6", "Part II · How It Works", "Trust by design",
  "Two touches keep it honest --- and the worst case is one free coffee.", "s_trust")

#giveget(
  "Touch one · at the bar",
  ([The bartender dates the card at the moment of proof.],
   [Books of 50 are checked out to each bar, so every serial traces to a venue and a week.]),
  "Touch two · at the shop",
  ([The barista scans the card's QR at redemption --- logged automatically, no typing.],
   [Duplicate or mismatched serials are flagged instantly; a lost pack is voided with one cell.]),
)

#twocol[
  *Serialized, and un-inventable.* Every card carries a unique number ending in
  a keyed checksum letter, so serials can't be minted by counting up from a card
  in hand. A made-up serial fails at the register and is logged as an attempt.

  *Short expiry* kills any secondary-market or stockpiling value --- a card is
  worth a coffee for one day and nothing after.

  #colbreak()
  *Pack kill switch.* A lost, stolen, or misprinted pack is voided in one step;
  from that moment every card in it fails to scan everywhere, and attempts are
  logged with where they turned up.

  *Proportionate by design.* The worst case of a gamed card is a single free
  coffee, so the controls stay light enough to keep the bar interaction to ten
  seconds. Bartender discretion is a feature, not a loophole.
]

#v(4pt)
#block(width: 6.05in)[#note[
  The full logging architecture --- a static site plus a Google Sheet, \$0/month,
  no server to babysit --- is in Appendix A, and the serialization scheme in
  Appendix B.
]]

#sect("7", "Part II · How It Works", "The car stays put",
  "Leaving the car overnight has to feel free and safe --- and in Knoxville, it already is.", "s_parking")

#block(width: 6.05in)[#lead[
  The program doesn't have to negotiate a parking policy. Downtown's public
  parking --- municipal garages and surface lots alike --- is already *free
  after 6 p.m. on weeknights and all weekend.*
]]

#twocol[
  What's missing isn't free parking --- it's the _knowledge_ of it at the
  decision moment. So the program advertises the free-parking reality loudly, on
  coasters, cards, and signage, so patrons stop treating "but my car" as a
  reason to drive.

  #colbreak()
  This is exactly where the *Downtown Parking Authority* comes in as a partner
  (page #pageof("s_park")): the program amplifies their free-nights-and-weekends
  message to the precise audience that needs it, and they give patrons a
  worry-free place to leave the car. Messaging is coordinated with the City so
  posted hours and any move-out times are stated accurately; where a public
  facility isn't nearby, private lot operators are recruited as sponsors.
]

// =============================================================================
// PART III
// =============================================================================
#partdivider("Part III", "Why It Works for Everyone",
  "One page per partner --- what they give, and what they get. Turn to the page for whoever's across the table.",
  (([8], [Downtown bars]), ([9], [Coffee shops]), ([10], [City of Knoxville & KPD]),
   ([11], [KAT]), ([12], [Downtown Parking Authority]), ([13], [Sponsors])))

#sect("8", "Part III · The distribution network", "Downtown bars",
  "The card starts in your hand. The ask is a 10-second date-and-hand at last call.", "s_bars")

#block(width: 6.05in)[#lead[
  Free coasters and signage, a safer close to your night, and your name on a
  city-backed road-safety program --- for handing a dated card to someone who
  books a ride home.
]]

#block(width: 6.05in)[
  The math is simple: the same parked car that tempts a patron to drive is the
  reason they'll be back tomorrow, so sending them home safe tonight doesn't cost
  you the visit --- it guarantees it. And the coasters that carry the message are
  stock you already put under every drink, now doing the marketing for you.
]

#giveget(
  "What we ask of you",
  ([A 10-second hand-off: glance at the ride, write the date, hand over one card.],
   [Keep a book of cards behind the bar and a laminated reference by the register.],
   [A quick pre-shift mention so staff know the drill.]),
  "What you get",
  ([Free branded coasters that replace stock you already buy --- and do the marketing passively.],
   [A safer, calmer close to the night and reduced dram-shop-adjacent risk.],
   [Early-partner billing: your name on cards and in the press launch.],
   [\$0 to join at pilot --- the program supplies every material and card book.]),
)

#collateral(
  (("coaster-night.svg", 1.5in), ("table-tent.svg", 0.72in)),
  [The free collateral you'll get --- the night coaster for the bar top and the
  folded table tent --- carries the program mark and message and does the
  talking for you. See the full identity in Appendix G (page #pageof("a_brand"))
  and the complete print kit in Appendix D (page #pageof("a_print")).],
)

#sect("9", "Part III · The redemption network", "Coffee shops",
  "Morning traffic from a crowd you don't currently see --- and your name on Pick-Me-Up materials all over town.", "s_shops")

#block(width: 6.05in)[#lead[
  A late-night crowd, in your shop the next morning --- and free advertising for
  your shop on cards, coasters, and signage across downtown.
]]

#giveget(
  "What we ask of you",
  ([Honor the card for one free large coffee, and scan its QR at the register.],
   [Provide the coffee as your own customer-acquisition cost, the way you'd fund any promotion.],
   [Help co-design the funding model --- real co-ownership, not a terms sheet.]),
  "What you get",
  ([First-time morning visits from customers you rarely reach --- and the regulars a good first cup creates.],
   [Your shop's name on the cards, coasters, and signage carried by every partner downtown --- free advertising you don't have to make.],
   [Monthly data back: redemptions and average-ticket uplift, so the value is visible.]),
)

#block(width: 6.05in)[#note[
  Why the math works: the card brings in a crowd you don't see in the morning, a
  large coffee is a small pour against a morning ticket that usually runs
  higher, and a good first visit makes a regular. Recruit shops within a short
  walk of the major garages first --- Gay Street, Market Square, and the Old
  City.
]]

#sect("10", "Part III · Credibility & safer streets", "City of Knoxville & KPD",
  "A positive-incentive complement to enforcement.", "s_city")

#block(width: 6.05in)[#lead[
  One prevented impaired-driving crash costs the city far more than this
  program's entire pilot.#refn[1] The asks are mostly promotion, not an
  open-ended budget line.
]]

#giveget(
  "What we ask of you",
  ([*City:* co-promote the already-free evening and weekend municipal parking, and include the program in city communications.],
   [*City:* an optional one-time seed for launch costs --- treated strictly as seed.],
   [*KPD:* a public endorsement and a program mention at high-risk moments --- football Saturdays, New Year's, and holiday weekends.],
   [*KPD:* no enforcement role inside bars; endorser, not operator.]),
  "What you get",
  ([A measurable, positive complement to enforcement and education --- part of the multi-component approach the evidence actually supports.#refn[3]],
   [Full transparency: quarterly issuance and redemption data by venue.],
   [A program that is never surveillance --- cards are anonymous, and no personal data is ever collected.],
   [Goodwill: Knoxville visibly thanking people for keeping the roads safe.]),
)

#block(width: 6.05in)[#note[
  KPD is a supporter, not an operator. The program must never feel like a
  checkpoint; every card is simply a documented decision not to drive home
  impaired.
]]

#sect("11", "Part III · The ride home & back", "Knoxville Area Transit",
  "\"Hair of the KAT\": an accepted ride, and a free-ride partner.", "s_kat")

#block(width: 6.05in)[#lead[
  Riders already taking the bus home safely should qualify too --- and a valid
  card should let anyone ride KAT free while it lasts, including the morning trip
  back to the car.
]]

#giveget(
  "What we ask of you",
  ([Recognize an activated KAT ticket as valid ride proof at the bar.],
   [Accept a valid Pick-Me-Up Card as free fare during its one-day window.],
   [Help communicate late-night and weekend routes and hours to patrons and bar staff.]),
  "What you get",
  ([KAT in front of the exact crowd that needs a late ride --- and first-time riders who stick.],
   [Off-peak, morning-trip ridership the card sends straight to you.],
   [Exposure naturally capped: the card is valid one day only, so cost is contained.],
   [Clean, anonymous ridership data (a driver count or farebox code).]),
)

#block(width: 6.05in)[#note[
  The free rides are KAT's in-kind contribution to a shared road-safety goal ---
  new riders and goodwill in exchange, not a program payout. And the audience is
  receptive: majorities of millennials and Gen-Z say they want to support and
  invest in public transit,#refn[14] so a free first ride is a natural on-ramp to
  a lasting rider.
]]

#sect("12", "Part III · A worry-free place for the car", "Downtown Parking Authority",
  "We carry your free-nights-and-weekends message to the people who most need to hear it.", "s_park")

#block(width: 6.05in)[#lead[
  Downtown parking is already free on nights and weekends --- the problem is that
  patrons don't know it at the moment they're deciding whether to drive. We put
  that message on the coaster under their drink.
]]

#giveget(
  "What we ask of you",
  ([Confirm the free evening and weekend hours (and any exceptions) so we state them accurately.],
   [Let the program amplify your free-parking communications on coasters, cards, and signage.],
   [Coordinate on any move-out times or special-event pricing so patrons aren't surprised.]),
  "What you get",
  ([Your core message --- free parking nights and weekends --- in front of the precise audience deciding whether to leave the car.],
   [More overnight use of municipal garages and lots on program nights.],
   [A partner actively reassuring drivers that leaving the car is easy, free, and safe.],
   [Alignment with a city-backed road-safety initiative.]),
)

#block(width: 6.05in)[#note[
  Leaving the car overnight has to feel free and safe or the whole program falls
  apart --- which makes the Parking Authority's message not a nice-to-have but
  load-bearing. Where a public facility isn't nearby, private lot operators can
  join as sponsors.
]]

#sect("13", "Part III · The accelerant", "Sponsors",
  "Your name on the safe ride home --- in every bar downtown.", "s_sponsors")

#block(width: 6.05in)[#lead[
  Annual presented-by placement on coasters and cards already in every bar
  downtown --- unusually good placement per dollar --- funding a program whose
  entire purpose aligns with your interests.
]]

#giveget(
  "What we ask of you",
  ([An annual sponsorship that covers fixed costs the per-coffee models don't --- printing and a coordinator.],
   [A logo file to the spec in the outreach one-sheet.],
   [For patron-facing materials: no alcohol brands.]),
  "What you get",
  ([Your logo in a "printing donated by" slot on coasters and cards --- without touching the program mark.],
   [Association with a positive, city-backed and KPD-backed road-safety story.],
   [A natural fit for rideshare companies, auto insurers, trauma systems, parking operators, and downtown property owners.],
   [A ready-made outreach one-sheet: what it funds, where the logo rides, and the spec.]),
)

#block(width: 6.05in)[#note[
  The placement is already built into the toolkit --- a single flag drops a
  sponsor logo into the donated-printing slot on cards and both coaster sides.
  Details in Appendix D and Appendix E.
]]

// =============================================================================
// PART IV
// =============================================================================
#partdivider("Part IV", "Making It Real",
  "The ask, the funding, the pilot, the metrics, the risks --- and the hard questions, answered honestly.",
  (([14], [What we ask of you]), ([15], [Built to sustain itself]), ([16], [The pilot]),
   ([17], [How we'll know it's working]), ([18], [Risks & mitigations]), ([19], [Frequently asked questions])))

#sect("14", "Part IV · Making It Real", "What we ask of you",
  "Every ask is small, specific, and sized to the partner.", "s_ask")

#ktable(
  (5.5em, 1fr),
  ("Partner", "The ask"),
  (
    ([*Downtown bars*], [A 10-second date-and-hand at last call; keep card books and a reference behind the bar.]),
    ([*Coffee shops*], [Honor the card for one large coffee and scan it; provide the coffee as customer acquisition; help pick the funding model.]),
    ([*City of Knoxville*], [Co-promote free evening and weekend parking; include the program in city comms; an optional one-time launch seed.]),
    ([*KPD*], [Public endorsement and a mention at high-risk moments; no enforcement role in bars.]),
    ([*KAT*], [Accept transit tickets as ride proof; accept a valid card as free fare; help communicate late-night service.]),
    ([*Parking Authority*], [Confirm free-parking hours; let the program amplify that message; coordinate on exceptions.]),
    ([*Sponsors*], [Annual support for fixed costs; a logo file; no alcohol brands on patron-facing materials.]),
  ),
)

#subhead[The order we recruit in]
#enum(
  [*City and KPD first* --- credibility unlocks everything else.],
  [*Three anchor coffee shops* --- redemption must exist before issuance; they co-design the funding model.],
  [*Five to eight anchor bars* for the pilot footprint.],
  [*KAT* to confirm ride proof, the free-ride benefit, and service messaging.],
  [*Parking Authority* to lock the free-parking message.],
  [*Sponsors*, once the partner map makes the placement value concrete.],
  [*Press launch* with the City and KPD, tied to a high-risk weekend --- then a data-driven second wave.],
)

#sect("15", "Part IV · Making It Real", "Built to sustain itself",
  "The perk is always free to the patron who took the safe ride. Here's who carries it.", "s_fund")

#block(width: 6.05in)[#lead[
  The funding model is deliberately open --- it gets locked with partners as they
  come on board --- but one constraint is fixed. Candidate streams, roughly in
  order of long-run durability:
]]

#ktable(
  (9.5em, 1fr),
  ("Stream", "How it works"),
  (
    ([*A · Merchant-funded* #linebreak() #note[the self-sustaining core]], [Shops provide the coffee as their own customer-acquisition cost. Zero external money; scales automatically with participation. The large coffee is a small pour against a higher morning ticket.]),
    ([*B · Community round-up* #linebreak() #note[parked for the pilot]], [An optional \$1 line on bar tabs --- tonight's crowd stands tomorrow's coffee. Kept as a switch-on-later option; deliberately absent from pilot materials.]),
    ([*C · Sponsorship tiers* #linebreak() #note[the accelerant]], [Annual presented-by packages cover fixed costs the per-coffee models don't. Logos ride on coasters and cards already in every bar.]),
    ([*D · Bar partner dues* #linebreak() #note[optional, later]], [A modest membership once foot-traffic value is proven. Held in reserve --- free entry is what makes the network dense at pilot.]),
    ([*E · Grants & city seed* #linebreak() #note[launch only]], [One-time money for the pilot's fixed costs. Seed only.]),
  ),
)

#band(light: true)[
  #eyebrow("Recommended architecture")
  #v(8pt)
  Model *A* as the base (the coffee costs the program nothing in cash), *C* to
  cover fixed costs, and *E* to launch, with *B* held as the community flywheel
  and *D* in reserve. KAT rides are KAT's in-kind contribution. Under this
  structure, the marginal cost of one more safe ride home is approximately zero
  --- which is what makes it durable.
]

#block(width: 6.05in)[#note[
  Illustrative pilot fixed costs and coupon economics are in Appendix E.
]]

#sect("16", "Part IV · Making It Real", "The pilot",
  "One footprint, one season, then evaluate honestly and scale.", "s_pilot")

#ktable(
  (8.4em, 6.2em, 1fr),
  ("Phase", "Window", "Milestones"),
  (
    ([*Design & city buy-in*], [Months 0--2], [City and KPD memorandum of understanding; free-parking co-promotion agreement with the Parking Authority.]),
    ([*Partner recruitment*], [Months 2--3], [Three coffee shops, six bars, and KAT signed; funding architecture locked with partners; materials printed.]),
    ([*Pilot launch*], [Month 4], [Press event on a high-visibility weekend.]),
    ([*Pilot run*], [Months 4--9], [Monthly reconciliation; a mid-pilot tune-up.]),
    ([*Evaluate & scale*], [Month 10+], [Public report; second-wave recruitment; sponsor expansion.]),
  ),
)

#callout([
  Success gates for the pilot
], [
  ≥60% of anchor bars actively issuing by month 2 · ≥50% redemption rate ·
  average redemption ticket comfortably above the coffee's cost · zero material
  fraud incidents · partner renewal intent.
])

#sect("17", "Part IV · Making It Real", "How we'll know it's working",
  "Real numbers --- and a privacy stance we can state out loud.", "s_metrics")

#twocol[
  *Primary.* Cards issued and redeemed, by venue and by night of week --- the
  pulse of the program.

  *Road safety.* Late-night impaired-driving crashes, arrests, and
  single-vehicle incidents in the downtown zone, tracked with KPD ---
  acknowledging small-sample noise in a pilot. This is the outcome the program
  exists to move.

  #colbreak()
  *Economic.* Average redemption ticket versus the cost of a large coffee (the
  number that proves Model A); repeat-customer reports; overnight garage stays on
  program nights.

  *Qualitative.* Bartender friction reports and short patron surveys via a QR on
  the card.
]

#band[
  #eyebrow("The privacy stance", fill: gold)
  #v(8pt)
  The system stores *no patron data at all* --- a serial, a shop, and a
  timestamp, nothing more. There are no accounts, no names, and no tracking.
  Cards are anonymous by design, which is exactly what lets KPD endorse the
  program without it ever feeling like surveillance. That's worth saying out loud
  to the City, and it's in the FAQ.
]

#sect("18", "Part IV · Making It Real", "Risks, and how we've handled them",
  "Every obvious objection, met before it's raised.", "s_risks")

#ktable(
  (11em, 1fr),
  ("Risk", "Mitigation"),
  (
    ([*Bartenders skip it on busy nights*], [A 10-second workflow, staff perks, and coasters that do the marketing passively.]),
    ([*Patron fears a ticket or tow for leaving the car*], [Lead with free evening and weekend municipal parking; confirm hours with the City and Parking Authority; print them on signage; program contact on the card.]),
    ([*Perception of promoting drinking*], [Framing is strictly the safe ride home and safer roads; City and KPD endorsement; no alcohol-brand sponsors on patron-facing materials. Full answer in the FAQ.]),
    ([*Fraud (fake ride screens, duplicates)*], [One-free-coffee cap, one-per-ride rule, serials, expiry, and bartender discretion; small leakage accepted as a marketing cost.]),
    ([*Redemption concentrates on a few shops*], [Recruit shops near every major garage and publish the redemption spread so imbalances surface early.]),
    ([*Shops lose faith in the coupon math*], [Share ticket-uplift data monthly; community and sponsor funds can backstop the coffee if Model A underperforms.]),
    ([*Program conflated with enforcement*], [KPD as endorser only; cards anonymous --- no data on individuals is ever collected.]),
  ),
)

// ---- FAQ --------------------------------------------------------------------
#let faq(q, a) = { v(11pt); text(font: serif, weight: 600, size: 12.4pt)[#q]; v(4pt); block(width: 6.35in)[#text(size: 9.9pt, fill: bodybrown)[#a]] }

#sect("19", "Part IV · Making It Real", "Frequently asked questions",
  "Starting with the hard one.", "s_faq")

#faq([Isn't this rewarding people for a night of irresponsible drinking?], [
  It's a fair thing to raise, and the honest answer is a *harm-reduction*
  one.#refn[9] People are going to go out and drink downtown whether or not this
  program exists. Given that, the only question that changes outcomes is: when
  someone has had too much, how do we make the safe choice the easy one?
  Pick-Me-Up doesn't subsidize the drinking --- the reward is explicitly tied to
  _not driving_, it's claimed the _next morning_, and it's capped at a coffee. It
  buys down the single largest friction that pushes people to drive impaired: the
  parked car. And the evidence base is real. A synthesis of roughly 125 studies
  found that well-implemented alternative-transportation programs _can_ reduce
  impaired driving, and identified the design attributes that predict success ---
  low cost, high awareness, convenience, and rides both to and from
  venues#refn[5] --- attributes this program is deliberately built around. We're
  also honest that the direct evidence for reward programs is *mixed*: the
  responsible reading, which we adopt, is that a reward like this should be _one
  component of a broader effort_ --- enforcement, education, transit, and
  responsible service --- and should be evaluated, not sold as a silver bullet.#refn[3]
])

#faq([Doesn't a free ride home just lead people to drink more?], [
  That specific risk is documented, and we take it seriously: a
  subsidized-rideshare study in Columbus found real crash reductions but also a
  self-reported _increase_ in drinking that partly offset the benefit.#refn[8]
  It's exactly why our reward is small, delayed to the next morning, and tied to
  the safe ride rather than to the bar tab --- a coffee you collect tomorrow at
  your car is a poor incentive to have one more drink tonight. It's also why we
  commit to measuring outcomes honestly rather than assuming them.
])

#faq([Is this public money buying people coffee?], [
  No. The coffee is carried by participating shops as their own
  customer-acquisition cost, backstopped by sponsors --- not a public payout ---
  and KAT rides are KAT's in-kind contribution. The program's only real cash need
  is a modest set of fixed costs (printing, a part-time coordinator, and launch).
  Any public seed is one-time and optional. Against that, alcohol-impaired
  crashes were estimated to cost *\$58 billion* in economic costs and *\$296
  billion* in comprehensive societal harm nationally in a single year#refn[1] ---
  so even a modest local reduction dwarfs the cost of coffee and bus fare.
])

#faq([Why not just tell people not to drink and drive?], [
  Because messaging alone has a weak track record. The Community Preventive
  Services Task Force found _insufficient evidence_ that promoting designated
  drivers on its own reduces impaired driving,#refn[4] while it _recommends_
  multi-component programs with community mobilization on strong evidence.#refn[3]
  A positive incentive delivered at the decision moment is the piece enforcement
  and slogans miss --- it complements them rather than replacing them.
])

#faq([Are you collecting data on people who've been drinking? Is this surveillance?], [
  No, and that's deliberate. The system stores no patron data at all --- only a
  card serial, a shop, and a timestamp. There are no names, no accounts, and no
  tracking. Cards are anonymous, and KPD is an endorser, not an operator: there
  is no enforcement role in bars and nothing that resembles a checkpoint. The
  anonymity is what makes the endorsement possible.
])

#faq([What stops someone from gaming it?], [
  Layered, proportionate controls: one card per booked ride, a keyed serial that
  can't be invented, a one-day expiry that kills resale value, per-shop caps, a
  pack kill-switch, and two-touch validation (dated at the bar, scanned at the
  shop). And the stakes are low by design --- the worst case of a gamed card is a
  single free coffee, so we keep the controls light enough that the bar
  interaction stays ten seconds. Details in Appendix B.
])

#faq([Isn't leaving the car downtown a hassle --- or a ticket risk?], [
  Downtown's municipal garages and lots are already free after 6 p.m. on
  weeknights and all weekend, so leaving the car overnight is free and allowed.
  The program partners with the Downtown Parking Authority to make sure those
  hours are stated accurately and communicated at the decision moment --- and the
  card carries a program contact for questions.
])

#block(width: 6.35in)[#note[
  Every figure and claim above is sourced in *Appendix F · Evidence &
  references* (page #pageof("a_refs")).
]]

// =============================================================================
// SUMMARY / CLOSING
// =============================================================================
#pagebreak()
#anchor("s_invite")
#band(deep: true)[
  #eyebrow("The invitation", fill: gold)
  #v(12pt)
  #text(font: serif, weight: 600, size: 26pt, fill: paper)[Let's make the safe \ choice the easy one.]
  #v(14pt)
  #block(width: 5.2in)[#text(size: 11.5pt, fill: silver)[
    Knox Pick-Me-Up asks each partner for something small and gives each one
    something real --- and together it keeps one more impaired driver off
    Knoxville's roads on the nights that matter most. The loop is designed, the
    toolkit is built, and the cost to start is a single sponsor conversation.
  ]]
  #v(8pt)
  #block(width: 5.2in)[#text(size: 11.5pt, fill: silver)[
    If you're a bar, a coffee shop, the City, KPD, KAT, the Parking Authority, or
    a sponsor --- there's a page in this book with your name on it. We'd love to
    talk about it.
  ]]
  #v(26pt)
  #line(length: 100%, stroke: 0.5pt + silver.transparentize(70%))
  #v(16pt)
  #eyebrow("Get in touch", fill: gold)
  #v(8pt)
  #text(font: serif, size: 12pt, fill: paper)[hello\@knoxpickmeup.org  ·  knoxpickmeup.org]
  #v(4pt)
  #text(size: 9pt, fill: silver)[Knoxville, Tennessee]
]

// =============================================================================
// APPENDICES
// =============================================================================
#appsect("A", "Technical architecture",
  "A turnkey system with no server to maintain, no on-call, and \$0/month.", "a_tech")

#block(width: 6.05in)[#lead[
  The whole tracking system runs on a static website plus a Google Sheet. Every
  moving part is either a static file on GitHub Pages or a Google-hosted freebie
  that keeps running if every volunteer goes on vacation.
]]

#v(6pt)
#band[
  #loop((
    ([1], [Print run makes serialized cards]),
    ([2], [Bar — pack checked out by QR]),
    ([3], [Coffee shop scans card QR]),
    ([4], [Google Sheet — the database]),
    ([5], [Live dashboard on the same site]),
  ), dark: true)
]

#subhead[The one clever trick]
#block(width: 6.05in)[
  Every card's QR encodes a plain link to the public site with the serial
  attached. A *patron* who scans it just lands on the shop map. The *shop's
  scanner page* doesn't follow the link --- it reads the serial off the camera
  with a regex. Same printed code, two behaviors, and zero extra infrastructure.
]

#subhead[The components]
#list(
  [*The database --- one Google Sheet* owned by a program account, with three tabs (Redemptions, Packs, Venues). Nothing else to host.],
  [*The redemption endpoint --- a \~30-line Apps Script web app* bound to the Sheet. It answers "was this card already used?" at the counter, in real time; Google hosts, runs, and patches it.],
  [*The scanner* (#raw("redeem/")) --- a self-contained static page opened from a per-shop QR. Tap-to-scan with the phone camera, a manual-entry fallback, and *offline tolerance*: no signal means the scan queues and auto-flushes when the connection returns.],
  [*Pack check-out --- the scanner's admin mode.* Scan a pack's cover QR, pick the bar --- that's the entire "which bar issued this" step, and it's insert-only so a double-scan can't reassign a pack.],
  [*The dashboard* (#raw("dashboard/")) --- a live, brand-styled page fed from the Sheet: issued and redeemed KPIs, a day×hour heatmap, to-shop and from-bar charts, and integrity tiles. Shareable by link --- the City, KPD, or a reporter can watch the numbers live, because the payload is venue names, timestamps, and counts only.],
)

#block(width: 6.05in)[#note[
  Attribution needs nobody to type a venue name, ever: the coffee shop is
  identified by which register QR opened the scanner, and the issuing bar by the
  serial's pack range. Cost at pilot scale: \$0.
]]

#appsect("B", "The card & anti-forgery serialization",
  "One secret in the whole system --- and serials that can't be minted by counting.", "a_serial")

#block(width: 6.05in)[
  Every card serial looks like *KPMU-2026-00004217T*: a year, an eight-digit
  number, and one *keyed checksum letter*. That letter is computed from a secret,
  so nobody can invent a valid serial by counting up from a card in hand --- a
  made-up serial passes only 1 time in 24, and every failure is logged.
]

#subhead[Exactly one secret]
#block(width: 6.05in)[
  The whole system has a single secret, PROGRAM_KEY. The checksum uses a key
  _derived_ from it (a one-way HMAC), and it's the derived key --- not the secret
  --- that rides in each shop's register QR. That's what lets the scanner verify
  serials locally and instantly, even offline, while someone who photographs a
  register QR still can't forge cards, touch backups, or learn the program key.
]

#subhead[Packs, and the kill switch]
#list(
  [*Packs of 50* carry their own serial with a leading P, so a pack can never be mistaken for a card. Checking a pack out to a bar ties every serial in it to that venue.],
  [*Kill switch:* to invalidate a lost, stolen, or misprinted pack, type anything in its voided cell. From that moment every card in it fails to scan at every register, and attempts are logged with where they surfaced. Clearing the cell restores it.],
  [*Two-touch:* dated by hand at the bar, scanned at the shop --- duplicates and mismatches flag automatically.],
)

#callout([
  Low stakes by design.
], [
  The worst realistic case of a gamed card is one free coffee, so the controls
  stay proportionate --- enough to deter, light enough to keep the bar hand-off
  to ten seconds.
])

#appsect("C", "Data, privacy, & backups",
  "No patron data exists to lose --- and four independent backup layers for what does.", "a_privacy")

#subhead[What's collected --- and what isn't]
#block(width: 6.05in)[
  The system stores a card *serial*, a *shop*, and a *timestamp*. There are no
  names, no accounts, no payment data, and no location tracking --- there is no
  patron identity anywhere in the system to collect, leak, or subpoena. The only
  card serials that ever leave the Sheet are those of _refused_ scans (already
  redeemed, voided, or invalid), which grant nothing and power duplicate
  forensics.
]

#subhead[Backups & disaster recovery]
#ktable(
  (7em, 1fr),
  ("Layer", "Protects against"),
  (
    ([*1 · Sheet version history*], [A bad edit or deleted column --- built into Google Sheets, automatic.]),
    ([*2 · Nightly Drive snapshot*], [A mangled or deleted tab --- 30 dated copies kept by a daily trigger.]),
    ([*3 · Nightly off-Google backup*], [Google account loss --- a GitHub Action commits CSVs of every tab; git history is the archive.]),
    ([*4 · Print artifacts*], [Everything digital at once --- pack sheets and cards carry hand-written date and bar lines.]),
  ),
)

#block(width: 6.05in)[#note[
  Hardening: the Sheet is shared with no editors --- the Apps Script is the only
  writer --- and partners get the dashboard link, never the Sheet. Worst-case
  full restore from the CSVs is under an hour. A failed nightly backup emails the
  owner; no pager, no service.
]]

#appsect("D", "The print kit & production",
  "Everything a print shop needs --- and it's all generated to spec from the toolkit.", "a_print")

#block(width: 6.05in)[
  The physical kit _is_ the program: the cards are the redeemable item, the packs
  are the fraud control, and the coasters are the advertising. Every generator
  writes a true-size, print-ready PDF with all type converted to outlines --- hand
  the files straight to a shop.
]

#ktable(
  (7em, 1fr),
  ("Piece", "Notes"),
  (
    ([*Card books*], [50 cards per book, a unique QR and serial per card. In printer terms, a raffle-ticket book with variable data --- commoditized and cheap.]),
    ([*Pack cover sheets*], [One per book, carrying the pack serial and a check-out QR.]),
    ([*Coasters (two-sided)*], [The advertising medium --- they sit under the drink at the decision moment. Bars burn through them anyway, so the program replaces a cost with free branded stock.]),
    ([*Signage*], [Table tents, a window decal, and restroom and community posters.]),
    ([*Staff & register*], [A laminated barista one-pager and bar-onboarding sheet; one register QR per shop.]),
  ),
)

#block(width: 6.05in)[#note[
  Ballpark: short-run card books land around \$0.08--0.20 per card, so a
  1,000-card pilot is roughly \$100--250 --- one sponsor conversation, with a
  natural sponsor in a local print shop credited on the card backs. The key spec:
  *uncoated stock*, because the bartender writes the date in ballpoint. A GitHub
  Action builds the whole kit in the browser and hands back a zip of PDFs --- no
  terminal needed.
]]

#appsect("E", "Financial detail",
  "The cash budget is fixed costs --- not a per-coffee payout.", "a_finance")

#subhead[Illustrative pilot fixed costs · 6 months]
#ktable(
  (1fr, 6em),
  ("Item", "Estimate"),
  (
    ([Printing: coasters, cards, and signage], [#align(right)[\$4,000]]),
    ([Part-time coordinator (reconciliation, restock, partner care)], [#align(right)[\$9,000]]),
    ([Launch marketing and press event], [#align(right)[\$3,000]]),
    ([Contingency], [#align(right)[\$2,000]]),
    ([*Total fixed*], [#align(right)[*\~\$18,000*]]),
  ),
)

#block(width: 6.05in)[
  The coffee itself is carried by participating shops (Model A) and backstopped by
  sponsorship if a shop needs it; KAT rides are KAT's in-kind contribution. So the
  program's cash budget is essentially the fixed costs above, not a per-perk
  payout --- and the marginal cost of one more safe ride home is approximately
  zero.
]

#subhead[Coupon economics (Model A), and why shops say yes]
#block(width: 6.05in)[
  The card brings in a late-night crowd shops rarely see in the morning; a large
  coffee is a small pour against a morning ticket that usually runs higher; and a
  good first visit creates a regular. The dashboard shows each shop its own
  average-ticket uplift, so the value is visible, not assumed.
]

#block(width: 6.05in)[#note[
  Sponsorship tiers cover the fixed costs above; logos ride on coasters and cards
  already in every bar downtown --- unusually good placement per dollar.
]]

#appsect("F", "Evidence & references",
  "The sources behind every figure and claim --- the supportive and the skeptical.", "a_refs")

#block(width: 6.05in)[#note[
  The evidence for reward programs is genuinely mixed, and we cite it that way:
  the supportive syntheses, the skeptical cost-effectiveness work, and the
  behavioral-design and harm-reduction foundations, alongside the local Knoxville
  figures.
]]
#v(6pt)

#reflist((
  ("The Economic and Societal Impact of Motor Vehicle Crashes, 2019",
   [NHTSA, Report DOT HS 813 403 (2022). Alcohol-impaired crashes: \~\$58B economic and \~\$296B comprehensive societal cost in 2019.],
   "crashstats.nhtsa.dot.gov/Api/Public/ViewPublication/813403.pdf"),
  ("Impaired Driving Facts",
   [U.S. Centers for Disease Control and Prevention. Ongoing toll and cost figures for alcohol-impaired driving.],
   "cdc.gov/impaired-driving/facts/index.html"),
  ("Alcohol-Impaired Driving: Multicomponent Interventions with Community Mobilization",
   [The Community Guide / Community Preventive Services Task Force --- recommends, strong evidence. Why a reward should sit inside a multi-part strategy.],
   "thecommunityguide.org (motor-vehicle-injury / alcohol-impaired driving)"),
  ("Effectiveness of designated driver programs for reducing alcohol-impaired driving: a systematic review",
   [Ditter et al., American Journal of Preventive Medicine (2005). CPSTF found insufficient evidence that DD promotion alone works.],
   "pubmed.ncbi.nlm.nih.gov/15894161/"),
  ("The effectiveness of alternative transportation programs in reducing impaired driving: a literature review and synthesis",
   [Journal of Safety Research (2020). Reviews \~125 studies; identifies the design attributes that predict success.],
   "pubmed.ncbi.nlm.nih.gov/33334469/"),
  ("Safe Ride Programs: Alternatives to Impaired Driving",
   [Traffic Injury Research Foundation (TIRF) literature review. Practitioner-oriented synthesis.],
   "tirf.ca/projects/safe-ride-programs-alternatives-impaired-driving/"),
  ("Countermeasures That Work --- Alternative Transportation",
   [NHTSA. The standard U.S. reference rating what's proven vs. promising.],
   "nhtsa.gov/book/countermeasures-that-work"),
  ("Efficacy and cost-effectiveness of subsidized ridesharing as a drunk-driving intervention",
   [Accident Analysis & Prevention (2020), Columbus, OH. Crash reductions, but modest and expensive savings and a self-reported increase in drinking --- the direct caution behind a small, safe-ride-tied perk.],
   "pubmed.ncbi.nlm.nih.gov/32866769/"),
  ("Harm Reduction as an Alcohol-Prevention Strategy",
   [Alcohol Research: Current Reviews (NIAAA), 2018.],
   "ncbi.nlm.nih.gov/pmc/articles/PMC6876518/"),
  ("What Is Harm Reduction?",
   [Johns Hopkins Bloomberg School of Public Health (2022). Plain-language primer on the philosophy.],
   "publichealth.jhu.edu/2022/what-is-harm-reduction"),
  ("Harm reduction approaches to alcohol use: health promotion, prevention, and treatment",
   [Addictive Behaviors (2002). Foundational framing of pragmatic, non-abstinence approaches.],
   "sciencedirect.com/science/article/abs/pii/S0306460302002940"),
  ("Nudge: Improving Decisions About Health, Wealth, and Happiness",
   [Thaler & Sunstein (2008). The case for removing friction and rewarding the desired choice at the exact moment it's made.],
   ""),
  ("Local data",
   [Knoxville Regional Transportation Planning Organization (annual injuries and fatalities in area impaired-driving crashes); Knox County Health Department (share of deadly crashes involving an impaired driver).],
   ""),
  ("Millennials & Mobility / rider attitudes toward public transit",
   [American Public Transportation Association (APTA), \"Millennials & Mobility\" and follow-on ridership research: younger adults report strong support for investing in and using public transit.],
   "apta.com (research: millennials and mobility)"),
))

#appsect("G", "Brand at a glance",
  "Warm paper, espresso ink, night navy, and one confident stroke of Tennessee orange.", "a_brand")

#grid(
  columns: (1.3in, 1fr), column-gutter: 22pt, align: horizon,
  image("mark-paper.svg", width: 1.3in),
  text(size: 9.6pt, fill: bodybrown)[
    *The mark.* A *wine-glass silhouette* cradling a steaming coffee cup --- the
    night out and the morning after, sealed in one glyph. Kept to a two-color
    navy and paper pair; never outlined, tilted, or effected.
  ],
)

#subhead[Palette]
#ktable(
  (7em, 6em, 1fr),
  ("Color", "Hex", "Role"),
  (
    ([*Paper*], [#raw("#FAF5EB")], [Primary light background; text on dark]),
    ([*Ink*], [#raw("#241A10")], [Display type and body headings]),
    ([*Night*], [#raw("#101A30")], [Primary dark band]),
    ([*Sunrise*], [#raw("#FF8200")], [The accent --- used sparingly: figures, the mark, one rule]),
    ([*Gold*], [#raw("#EDA953")], [Accent text on dark backgrounds]),
  ),
)

#subhead[Type & voice]
#block(width: 6.05in)[
  *Fraunces* (serif) for display, *Inter* (sans) for text, and *Cormorant* with
  old-style figures for statistics --- all free and self-hosted. The voice is
  warm, wry, and never preachy: never "don't drink and drive," always a
  thank-you for the safe ride home. One accent color, used rarely, so that when
  orange appears it means something.
]

#pagebreak()
#text(font: serif, weight: 600, size: 15pt)[The brand, applied]
#v(3pt)
#block(width: 6.05in)[#note[
  Every patron-facing and back-of-house piece is generated to spec from one mark
  source, so the identity stays consistent everywhere it lands. The full,
  print-ready kit lives in Appendix D (page #pageof("a_print")).
]]
#v(12pt)

#eyebrow[The card]
#v(8pt)
#grow((
  ("card.svg", "Front — the redeemable coffee + KAT fare", 3.0in),
  ("card-back.svg", "Back — how it works and the partnership line", 3.0in),
))

#v(20pt)
#eyebrow[Coasters & window]
#v(8pt)
#grow((
  ("coaster-night.svg", "Coaster, night side — at the bar", 2.0in),
  ("coaster-day.svg", "Coaster, day side — at the shop", 2.0in),
  ("window-sticker.svg", "Window decal — the storefront", 2.0in),
))

#pagebreak()
#eyebrow[Table & wall]
#v(8pt)
#grow((
  ("table-tent.svg", "Table tent — both faces fold up", 1.0in),
  ("sign-bathroom.svg", "Restroom poster", 1.93in),
  ("sign-community.svg", "Community poster", 1.93in),
))

#v(20pt)
#eyebrow[Behind the counter]
#v(8pt)
#grow((
  ("pack.svg", "Pack cover sheet", 1.5in),
  ("barista-one-pager.svg", "Barista reference", 1.55in),
  ("bar-onboarding.svg", "Bar onboarding", 1.55in),
  ("sponsor-one-sheet.svg", "Sponsor one-sheet", 1.55in),
))

#appsect("H", "Forking this for your community",
  "Knox Pick-Me-Up is an open playbook --- here's how another city stands up its own.", "a_fork")

#block(width: 6.05in)[#lead[
  Nothing about this is Knoxville-specific except the name and the partners. The
  whole thing --- the site, the scanner, the dashboard, the print generators, and
  this document --- is a toolkit another community can adapt in an afternoon of
  setup and a few weeks of partner conversations.
]]

#steps((
  ([Rebrand], [Swap the name, mark, tagline, and the one accent color for your city's. The identity is parametric --- the generators regenerate every asset from one mark source.]),
  ([Swap the partners], [Replace the venue rosters and your transit agency's equivalent of "Hair of the KAT." Confirm your downtown's free-parking hours with your parking authority.]),
  ([Stand up the backend], [Create a program Google account and Sheet, paste the \~30-line Apps Script, set your one secret, and deploy. One afternoon, following the setup runbook.]),
  ([Print & run a pilot], [Generate the card books and coasters to spec, recruit a handful of anchor bars and shops, launch on a high-risk weekend, and evaluate honestly.]),
))

#subhead[Localize the evidence]
#block(width: 6.05in)[
  Replace the local figures (page #pageof("s_problem")) with your region's
  impaired-driving injury and fatality numbers from your transportation planning
  organization and health department. The national and peer-reviewed sources in
  Appendix F travel unchanged --- and so does the honest framing: run the reward
  as one component of a broader effort, and publish what you find.
]

#callout([
  The design constraint that must survive any fork:
], [
  the perk is always free to the patron who took the safe ride, it's claimed the
  next morning at the car, and it's capped small. Keep those three, and the
  harm-reduction logic --- and the fraud math --- still hold.
])

// -----------------------------------------------------------------------------
#backcover()
