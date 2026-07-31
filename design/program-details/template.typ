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
  set par(leading: 0.72em, spacing: 0.82em, justify: false)
  set block(spacing: 1.0em)
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
// a numbered section. num may be "" for an unnumbered opener; kicker/dek may be
// "" to omit them. brk:false lets the section flow onto the current page (used
// for the short Part I sections) instead of forcing a page break.
#let sect(num, kicker, title, dek, lbl, brk: true) = {
  if brk { pagebreak() } else { v(20pt) }
  anchor(lbl)
  grid(
    columns: (if num == "" { 0pt } else { 0.72in }, 1fr),
    column-gutter: if num == "" { 0pt } else { 20pt },
    if num == "" [] else { fig(58pt, num) },
    {
      if kicker != "" { eyebrow(kicker); v(10pt, weak: true) }
      text(font: serif, weight: 600, size: 29pt)[#fixd(title)]
      if dek != "" {
        v(11pt, weak: true)
        text(font: serif, style: "italic", size: 13.5pt, fill: umber)[#fixd(dek)]
      }
    },
  )
  v(14pt)
  rule
  v(13pt)
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
      v(10pt, weak: true)
      text(font: serif, weight: 600, size: 27pt)[#fixd(title)]
      v(11pt, weak: true)
      text(font: serif, style: "italic", size: 13pt, fill: umber)[#fixd(dek)]
    },
  )
  v(14pt)
  rule
  v(13pt)
}

#let subhead(body) = { v(15pt); text(font: serif, weight: 600, size: 12.5pt)[#body]; v(5pt) }
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

// ---- the loop strip: numbered nodes joined by a connecting line -------------
// items: ((num, label), ...) ; dark:true when placed on a navy band
#let loop(items, dark: false) = {
  let n = items.len()
  let ring = if dark { gold } else { sunrise }
  let conn = if dark { silver.transparentize(55%) } else { hairline }
  let lab = if dark { silver } else { bodybrown }

  // a numbered node
  let node(num) = box(
    width: 30pt, height: 30pt, radius: 50%, stroke: 1pt + ring,
    fill: if dark { none } else { paper },
  )[#align(center + horizon)[#fig(17pt, num, fill: ring)]]

  // build interleaved columns: node, connector, node, connector, ... node
  let cols = ()
  let nodes = ()
  let labels = ()
  for (i, it) in items.enumerate() {
    cols.push(1fr)
    nodes.push(align(center)[#node(it.at(0))])
    labels.push(align(center + top)[
      #text(size: 8pt, weight: 500, fill: lab)[#it.at(1)]
    ])
    if i < n - 1 {
      cols.push(20pt)
      nodes.push(align(horizon)[#line(length: 100%, stroke: conn)])
      labels.push([])
    }
  }
  grid(columns: cols, row-gutter: 9pt, ..nodes, ..labels)
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
// The two columns are cells of one grid, so the row auto-sizes to the taller
// side and BOTH cell fills/strokes span that full height — equal boxes for free.
#let ggcell(title, items) = {
  eyebrow(title)
  v(9pt)
  set text(size: 9.6pt)
  for (i, it) in items.enumerate() {
    if i > 0 { v(7pt, weak: true) }
    grid(columns: (12pt, 1fr), text(fill: sunriseink)[•], it)
  }
}

#let giveget(gt, gi, tt, ti) = {
  v(10pt)
  grid(
    columns: (1fr, 1fr), column-gutter: 20pt, inset: 15pt,
    fill: (c, r) => if c == 1 { paperdeep } else { none },
    stroke: (c, r) => if c == 0 { 0.75pt + hairline } else { none },
    ggcell(gt, gi),
    ggcell(tt, ti),
  )
  v(10pt)
}

// ---- callout & pull quote ---------------------------------------------------
#let callout(q, body) = {
  v(12pt)
  block(
    width: 100%, inset: (left: 18pt, y: 4pt), breakable: false,
    stroke: (left: 2pt + sunrise),
  )[
    #text(font: serif, style: "italic", size: 12.5pt)[#q]
    #v(5pt)
    #note(body)
  ]
  v(12pt)
}

// ---- the real card artwork (front), with a caption beside it ----------------
// `card.svg` is a copy of assets/card.svg (the actual generated card front)
#let cardrow(caption) = grid(
  columns: (3.5in, 1fr), column-gutter: 22pt, align: horizon,
  box(radius: 6pt, clip: true, stroke: 0.75pt + hairline)[#image("card.svg", width: 100%)],
  text(size: 10pt, fill: bodybrown)[#caption],
)

// a row of collateral thumbnails with a shared caption below
// pieces: ((path, width), ...)
#let collateral(pieces, caption) = {
  v(10pt)
  grid(
    columns: pieces.map(p => p.at(1)), column-gutter: 20pt, align: bottom,
    ..pieces.map(p => box(radius: 4pt, clip: true, stroke: 0.75pt + hairline)[
      #image(p.at(0), width: 100%)
    ]),
  )
  v(7pt)
  note(caption)
}

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
    #v(14pt)
    #for (i, it) in items.enumerate() {
      if i > 0 { v(9pt, weak: true) }
      grid(
        columns: (0.34in, auto), column-gutter: 6pt, align: (left + horizon, left + horizon),
        fig(13pt, it.at(0), fill: gold),
        text(font: serif, weight: 400, size: 11.5pt, fill: paper)[#it.at(1)],
      )
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
#let tocgroup(t) = { v(15pt); eyebrow(t); v(8pt) }
// num aligned in its own column so "1" and "10" line up; whole row links to
// the section anchor and jumps there when clicked.
#let tocrow(num, title, name) = {
  link(label(name))[
    #grid(
      columns: (1.7em, auto, 1fr, auto), column-gutter: 8pt,
      align: (right + horizon, left + horizon, center + horizon, right + horizon),
      text(size: 10.2pt, fill: umber)[#num],
      text(size: 10.2pt, fill: ink)[#title],
      box(width: 100%, inset: (bottom: 2pt))[#text(fill: hairline)[#repeat(gap: 3pt)[.]]],
      text(font: figify, weight: 700, size: 11pt, fill: umber, number-type: "old-style")[#pageof(name)],
    )
  ]
  v(5pt)
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
