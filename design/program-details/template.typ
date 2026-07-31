// =============================================================================
// Knox Pick-Me-Up — Program Details · design template
// -----------------------------------------------------------------------------
// This file holds the LOOK of the briefing book: colors, fonts, the page
// frame, and every reusable component (stat bands, the loop strip, give/get
// cards, the card mock, part dividers, the cover). You usually don't need to
// touch it — write and edit the words in `program-details.typ`.
//
// If you do want to restyle: the palette and type are right below, and each
// component is a small #let function further down.
// =============================================================================

// ---- palette (from BRAND.md) ------------------------------------------------
#let paper      = rgb("#FAF5EB")
#let paperdeep  = rgb("#F2E9D8")
#let ink        = rgb("#241A10")
#let umber      = rgb("#6F5F4C")
#let navy       = rgb("#101A30")
#let navydeep   = rgb("#0A101F")
#let sunrise    = rgb("#FF8200")   // the accent — used sparingly
#let sunriseink = rgb("#B04E00")   // orange for text on paper (accessible)
#let gold       = rgb("#EDA953")   // accent text on dark grounds
#let hairline   = rgb("#DDCFB4")
#let silver     = rgb("#C6CEDC")   // muted text on navy
#let bodybrown  = rgb("#3A2F22")

// ---- type -------------------------------------------------------------------
#let serif  = "Fraunces"
#let sans   = "Inter"
#let figify = "Cormorant"          // big statistics, old-style figures

// helper: an old-style figure in Cormorant (the big numerals)
#let fig(size, body, fill: sunrise) = text(
  font: figify, weight: 700, size: size, fill: fill, number-type: "old-style",
)[#body]

// ---- document setup (applied by `#show: conf` in the content file) ----------
#let conf(body) = {
  set page(
    paper: "us-letter",
    margin: (top: 0.82in, bottom: 0.66in, x: 0.8in),
    footer: context {
      set text(font: sans, size: 6.6pt, fill: rgb("#B3A990"), tracking: 0.9pt)
      grid(
        columns: (1fr, auto), align: (left + horizon, right + horizon),
        upper[Knox Pick-Me-Up  ·  Program Details],
        text(font: figify, weight: 700, size: 10pt, fill: umber, number-type: "old-style")[
          #counter(page).display()
        ],
      )
    },
  )
  set text(font: sans, size: 10.3pt, fill: ink, hyphenate: false)
  set par(leading: 0.72em, spacing: 0.72em, justify: false)
  set block(spacing: 0.9em)
  show link: set text(fill: sunriseink)
  body
}

// convert "---" / "--" typed in string arguments (section titles & subtitles)
// into real em / en dashes — Typst only does this automatically inside markup.
#let fixd(s) = s.replace("---", "—").replace("--", "–")

// ---- anchors & the table of contents ---------------------------------------
// place an invisible, queryable marker so the TOC can find a section's page
#let anchor(name) = [#metadata(none)#label(name)]

#let pageof(name) = context {
  let e = query(label(name))
  if e.len() == 0 [—] else [#counter(page).at(e.first().location()).first()]
}

#let eyebrow(body, fill: sunriseink) = text(
  font: sans, weight: 600, size: 7.6pt, fill: fill, tracking: 1.6pt,
)[#upper(body)]

#let rule = line(length: 100%, stroke: 0.5pt + hairline)

// a superscript citation marker, e.g. #refn[5] — keyed to Appendix F
#let refn(n) = super(text(size: 6.6pt, weight: 600, fill: sunriseink)[#n])

// ---- section openers --------------------------------------------------------
// a numbered section (num may be "" for unnumbered openers like the summary)
#let sect(num, kicker, title, dek, lbl) = {
  pagebreak()
  anchor(lbl)
  grid(
    columns: (if num == "" { 0pt } else { 0.72in }, 1fr),
    column-gutter: if num == "" { 0pt } else { 20pt },
    if num == "" [] else { fig(58pt, num) },
    {
      eyebrow(kicker)
      v(9pt, weak: true)
      text(font: serif, weight: 600, size: 29pt)[#fixd(title)]
      v(5pt, weak: true)
      text(font: serif, style: "italic", size: 13.5pt, fill: umber)[#fixd(dek)]
    },
  )
  v(11pt)
  rule
  v(9pt)
}

// an appendix opener (letter in place of the number)
#let appsect(letter, title, dek, lbl) = {
  pagebreak()
  anchor(lbl)
  grid(
    columns: (0.72in, 1fr), column-gutter: 20pt,
    fig(52pt, letter),
    {
      eyebrow[Appendix #letter]
      v(9pt, weak: true)
      text(font: serif, weight: 600, size: 27pt)[#fixd(title)]
      v(5pt, weak: true)
      text(font: serif, style: "italic", size: 13pt, fill: umber)[#fixd(dek)]
    },
  )
  v(11pt)
  rule
  v(9pt)
}

#let subhead(body) = { v(6pt); text(font: serif, weight: 600, size: 12pt)[#body]; v(2pt) }
#let lead(body) = text(size: 11.6pt, fill: bodybrown)[#body]
#let note(body) = text(size: 8.7pt, fill: umber)[#body]

// two-column running text
#let twocol(body) = columns(2, gutter: 24pt, body)

// ---- night bands ------------------------------------------------------------
#let band(body, deep: false, light: false) = block(
  width: 100%, radius: 2pt, inset: (x: 0.4in, y: 0.34in), breakable: false,
  fill: if deep { navydeep } else if light { paperdeep } else { navy },
)[
  #set text(fill: if light { ink } else { paper })
  #body
]

// stat trio inside a night band. items: ((number-content, label), ...)
#let statband(title, items) = band[
  #eyebrow(title, fill: gold)
  #v(10pt)
  #grid(
    columns: items.map(_ => 1fr), column-gutter: 22pt,
    ..items.map(it => {
      fig(46pt, it.at(0))
      v(-4pt)
      text(size: 8.4pt, fill: silver)[#it.at(1)]
    }),
  )
]

// ---- the loop strip (horizontal, numbered, with arrows) ---------------------
// items: ((num, label), ...) ; dark:true when placed on a navy band
#let loop(items, dark: false) = {
  let cols = ()
  let cells = ()
  for (i, it) in items.enumerate() {
    cols.push(1fr)
    cells.push(align(center + horizon)[
      #fig(22pt, it.at(0))
      #v(4pt, weak: true)
      #text(size: 8pt, weight: 500, fill: if dark { silver } else { ink })[#it.at(1)]
    ])
    if i < items.len() - 1 {
      cols.push(12pt)
      cells.push(align(center + horizon)[
        #text(size: 13pt, fill: if dark { silver.transparentize(50%) } else { hairline })[→]
      ])
    }
  }
  grid(columns: cols, align: center + horizon, ..cells)
}

// ---- vertical numbered steps ------------------------------------------------
// items: ((title, body), ...) — numbered 1..n automatically
#let steps(items) = {
  for (i, it) in items.enumerate() {
    if i > 0 { rule }
    v(4pt)
    grid(
      columns: (0.5in, 1fr), column-gutter: 14pt,
      align(right)[#fig(26pt, str(i + 1))],
      {
        text(font: serif, weight: 600, size: 11.2pt)[#it.at(0)]
        linebreak()
        text(size: 9.7pt, fill: bodybrown)[#it.at(1)]
      },
    )
    v(4pt)
  }
}

// ---- give / get cards -------------------------------------------------------
#let ggcol(title, items, filled: false) = block(
  width: 100%, radius: 2pt, inset: 14pt, breakable: false,
  fill: if filled { paperdeep } else { none },
  stroke: if filled { none } else { 0.75pt + hairline },
)[
  #eyebrow(title)
  #v(6pt)
  #set text(size: 9.6pt)
  #for it in items {
    grid(columns: (10pt, 1fr), text(fill: sunriseink)[•], it)
    v(5pt, weak: true)
  }
]

#let giveget(gt, gi, tt, ti) = {
  v(6pt)
  grid(
    columns: (1fr, 1fr), column-gutter: 24pt,
    ggcol(gt, gi, filled: false),
    ggcol(tt, ti, filled: true),
  )
  v(6pt)
}

// ---- callout & pull quote ---------------------------------------------------
#let callout(q, body) = {
  v(6pt)
  block(
    width: 100%, inset: (left: 16pt), breakable: false,
    stroke: (left: 2pt + sunrise),
  )[
    #text(font: serif, style: "italic", size: 12.5pt)[#q]
    #v(4pt)
    #note(body)
  ]
  v(6pt)
}

// ---- the card mock ----------------------------------------------------------
#let mockcard() = block(width: 3.05in, radius: 6pt, clip: true, stroke: 0.75pt + hairline)[
  #block(fill: navy, width: 100%, inset: (x: 15pt, top: 14pt, bottom: 13pt))[
    #set text(fill: paper)
    #text(size: 6.6pt, fill: gold, tracking: 1.1pt)[#upper[Knox Pick-Me-Up · Thank you for the safe ride home]]
    #v(7pt)
    #text(font: serif, weight: 600, size: 15pt)[One free \ large coffee #text(style: "italic", fill: gold)[— on us.]]
  ]
  #block(fill: paper, width: 100%, inset: (x: 15pt, top: 12pt, bottom: 13pt))[
    #grid(
      columns: (1fr, auto), align: (left + bottom, right + bottom),
      text(size: 6.4pt, fill: umber, tracking: 0.9pt)[#upper[Date issued]],
      fig(12pt, [—  /  —  /  ——], fill: ink),
    )
    #v(5pt); #rule; #v(5pt)
    #text(size: 6.4pt, fill: umber, tracking: 0.9pt)[#upper[Valid one day · Hair of the KAT: free bus fare]]
    #v(7pt)
    #text(font: sans, size: 7pt, fill: umber, tracking: 0.4pt)[KPMU-2026-00004217T]
  ]
]

// caption beside the card
#let cardrow(caption) = grid(
  columns: (3.05in, 1fr), column-gutter: 22pt, align: horizon,
  mockcard(),
  text(size: 9.6pt, fill: bodybrown)[#caption],
)

// ---- part divider (navy plate + its own mini contents) ----------------------
// items: ((num, title), ...)
#let partdivider(pnum, title, dek, items) = {
  pagebreak()
  block(width: 100%, fill: navy, radius: 2pt, inset: (x: 0.5in, top: 0.5in, bottom: 0.46in))[
    #set text(fill: paper)
    #fig(15pt, pnum, fill: gold)
    #v(10pt)
    #text(font: serif, weight: 600, size: 26pt)[#title]
    #v(9pt)
    #text(font: serif, style: "italic", size: 12.5pt, fill: silver)[#fixd(dek)]
    #v(18pt)
    #line(length: 100%, stroke: 0.5pt + silver.transparentize(70%))
    #v(12pt)
    #set text(size: 9pt, fill: rgb("#AEB6C6"))
    #for it in items {
      grid(
        columns: (0.32in, auto), column-gutter: 4pt,
        text(font: serif, weight: 600, fill: paper)[#it.at(0)],
        text(font: serif, weight: 600, fill: paper)[#it.at(1)],
      )
      v(6pt, weak: true)
    }
  ]
}

// ---- references list --------------------------------------------------------
// items: ((title, body, url), ...)
#let reflist(items) = for (i, it) in items.enumerate() {
  if i > 0 { rule }
  v(5pt)
  grid(
    columns: (0.3in, 1fr), column-gutter: 8pt,
    fig(12pt, str(i + 1), fill: sunriseink),
    {
      text(size: 9.2pt)[*#fixd(it.at(0)).* #it.at(1)]
      if it.at(2) != "" {
        linebreak()
        text(size: 8pt, fill: umber)[#it.at(2)]
      }
    },
  )
  v(5pt)
}

// ---- cover & back cover -----------------------------------------------------
#let cover() = page(fill: navy, margin: 0pt, footer: none, header: none)[
  #set text(fill: paper)
  // gold keyline
  #place(top + left, dx: 0.42in, dy: 0.42in,
    rect(width: 100% - 0.84in, height: 100% - 0.84in, stroke: 1.25pt + gold.transparentize(45%)))
  #block(width: 100%, height: 100%, inset: (x: 1.14in, y: 1.12in))[
    #grid(
      rows: (auto, 1fr, auto),
      {
        image("mark-dark.svg", width: 1.42in)
        v(30pt)
        text(font: serif, weight: 600, size: 41pt)[Knox \ Pick-Me-Up]
        v(14pt)
        text(font: serif, style: "italic", size: 16pt, fill: gold)[Ride from last call to first cup.]
      },
      [],
      {
        line(length: 1.1in, stroke: 0.75pt + gold.transparentize(60%))
        v(10pt)
        text(font: sans, weight: 600, size: 9pt, tracking: 2pt)[#upper[Program Details]]
        v(9pt)
        text(font: serif, size: 13pt, fill: rgb("#C6CEDC"))[
          A downtown Knoxville road-safety partnership — rewarding the safe ride home with tomorrow's coffee.
        ]
        v(26pt)
        text(size: 9pt, fill: rgb("#9AA4B6"))[
          Prepared for #box(width: 2.5in, line(length: 100%, stroke: 0.5pt + rgb("#C6CEDC").transparentize(55%)))
        ]
        v(22pt)
        text(size: 8.2pt, fill: rgb("#8892A4"), tracking: 1pt)[
          #upper[Knoxville, Tennessee  ·  hello\@knoxpickmeup.org  ·  knoxpickmeup.org]
        ]
      },
    )
  ]
]

#let backcover() = page(fill: navydeep, margin: 0pt, footer: none, header: none)[
  #set text(fill: paper)
  #align(center + horizon)[
    #image("mark-dark.svg", width: 1.15in)
    #v(18pt)
    #text(font: serif, weight: 600, size: 22pt)[Knox Pick-Me-Up]
    #v(8pt)
    #text(font: serif, style: "italic", size: 13pt, fill: gold)[Ride from last call to first cup.]
    #v(34pt)
    #text(size: 9pt, fill: rgb("#8892A4"), tracking: 1.4pt)[
      #upper[hello\@knoxpickmeup.org \ knoxpickmeup.org \ Knoxville, Tennessee]
    ]
  ]
]

// ---- table of contents helpers ----------------------------------------------
#let tocgroup(t) = { v(14pt); eyebrow(t); v(6pt) }
#let tocrow(labeltext, name) = {
  grid(
    columns: (auto, 1fr, auto), column-gutter: 6pt, align: (left + horizon, center + horizon, right + horizon),
    text(size: 10.2pt)[#labeltext],
    box(width: 100%, inset: (bottom: 2pt))[#text(fill: hairline)[#repeat(gap: 3pt)[.]]],
    text(font: figify, weight: 700, size: 11pt, fill: umber, number-type: "old-style")[#pageof(name)],
  )
  v(3pt)
}

// a simple branded table: uppercase header with a heavy underline, hairline
// between rows. header: (col, ...) ; rows: ((cell, ...), ...) ; cols: sizes
#let ktable(cols, header, rows) = {
  set text(size: 9.5pt)
  table(
    columns: cols,
    inset: (right: 16pt, top: 7pt, bottom: 7pt),
    align: left + top,
    stroke: (x, y) => (bottom: if y == 0 { 1.25pt + ink } else { 0.5pt + hairline }),
    ..header.map(h => text(font: sans, weight: 600, size: 7.6pt, fill: umber, tracking: 1pt)[#upper[#h]]),
    ..rows.flatten(),
  )
}
