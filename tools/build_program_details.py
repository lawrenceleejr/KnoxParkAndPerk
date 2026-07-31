# -*- coding: utf-8 -*-
"""Assemble the Knox Pick-Me-Up — Program Details briefing book as one
self-contained HTML file (fonts and the mark are embedded, so it opens and
prints identically anywhere, with no external dependencies).

    python3 tools/build_program_details.py [out.html]

The generated HTML carries {P:key} placeholders in its table of contents; the
companion renderer (tools/render_program_details.py) fills those with real
page numbers while producing the PDF. Opened directly in a browser the file is
fully readable and printable — only the TOC page numbers wait on the renderer.
"""
import base64, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
ASSETS = ROOT / "assets"

# --- fonts: embed the self-hosted woff2 as base64 so the file is portable ----
_FONT_FACES = [
    ("Fraunces", "normal", 400, "fraunces-400-normal-6.woff2"),
    ("Fraunces", "italic", 400, "fraunces-400-italic-3.woff2"),
    ("Fraunces", "normal", 600, "fraunces-600-normal-9.woff2"),
    ("Inter", "normal", 400, "inter-400-normal-16.woff2"),
    ("Inter", "normal", 500, "inter-500-normal-23.woff2"),
    ("Inter", "normal", 600, "inter-600-normal-30.woff2"),
    ("Cormorant", "normal", 700, "cormorant-700.woff2"),
]
def _embed_fonts():
    out = []
    for fam, style, weight, fn in _FONT_FACES:
        b64 = base64.b64encode((ASSETS / "fonts" / fn).read_bytes()).decode()
        out.append(
            f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{weight};"
            f"font-display:swap;src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
        )
    return "\n".join(out)
FONTS = _embed_fonts()

# --- the mark: recolour the two-token source for dark and light grounds -------
_MARK_SRC = (ASSETS / "mark.svg").read_text()
MARK_DARK = _MARK_SRC.replace("#101a30", "#FAF5EB").replace("#ffffff", "#101A30")
MARK_PAPER = _MARK_SRC.replace("#ffffff", "#FAF5EB")

# ---------------------------------------------------------------- CSS
CSS = r"""
""" + FONTS + r"""
:root{
  --paper:#FAF5EB; --paper-deep:#F2E9D8; --ink:#241A10; --umber:#6F5F4C;
  --night:#101A30; --night-deep:#0A101F; --sunrise:#FF8200; --sunrise-ink:#B04E00;
  --gold:#EDA953; --hairline:#DDCFB4;
  --serif:'Fraunces',Georgia,serif; --sans:'Inter','Helvetica Neue',Arial,sans-serif;
  --fig:'Cormorant',Garamond,serif;
}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;}
body{font-family:var(--sans);color:var(--ink);font-size:10.3pt;line-height:1.6;
  -webkit-print-color-adjust:exact;print-color-adjust:exact;}
@page{ size:letter; margin:0.82in 0.8in 0.66in;
  @bottom-left{ content:"KNOX PICK-ME-UP \00B7  PROGRAM DETAILS"; font-family:'Inter',sans-serif;
    font-size:6.6pt; color:#B3A990; letter-spacing:0.14em; }
  @bottom-right{ content:counter(page); font-family:'Cormorant',serif; font-weight:700;
    font-variant-numeric:oldstyle-nums; font-size:10pt; color:#6F5F4C; }
}
@page:first{ margin:0; @bottom-left{content:none;} @bottom-right{content:none;} }
@page cover{ margin:0; @bottom-left{content:none;} @bottom-right{content:none;} }

/* ---- primitives ---- */
h1,h2,h3,h4{font-family:var(--serif);font-weight:600;color:var(--ink);margin:0;
  line-height:1.12;-webkit-font-smoothing:antialiased;}
p{margin:0 0 0.62em 0;}
a{color:var(--sunrise-ink);text-decoration:none;}
strong{font-weight:600;color:var(--ink);}
em{font-style:italic;}
.serif{font-family:var(--serif);}
.measure{max-width:6.05in;}

/* section opener */
.section{page-break-before:always;}
.eyebrow{font-family:var(--sans);font-weight:600;font-size:7.6pt;letter-spacing:0.2em;
  text-transform:uppercase;color:var(--sunrise-ink);margin:0 0 0.9em 0;}
.opener{display:flex;align-items:flex-start;gap:0.34in;margin-bottom:0.26in;}
.opener .num{font-family:var(--fig);font-weight:700;font-variant-numeric:oldstyle-nums;
  font-size:58pt;line-height:0.8;color:var(--sunrise);flex:0 0 auto;}
.opener .htext{flex:1;}
.opener h1{font-size:29pt;letter-spacing:-0.01em;}
.opener .dek{font-family:var(--serif);font-style:italic;font-weight:400;font-size:13.5pt;
  color:var(--umber);margin-top:0.32em;line-height:1.34;}
.rule{border:0;border-top:1px solid var(--hairline);margin:0.16in 0 0.24in;}
h2.sub{font-size:15.5pt;margin:0.32in 0 0.12in;letter-spacing:-0.01em;}
h3.sub{font-size:11.8pt;margin:0.22in 0 0.06in;}
.lead{font-size:11.6pt;line-height:1.62;color:#3a2f22;}

/* two-column body */
.cols{column-count:2;column-gap:0.42in;}
.cols p{margin-bottom:0.7em;}

/* night band */
.band{background:var(--night);color:var(--paper);border-radius:2px;
  padding:0.34in 0.4in;margin:0.26in 0;break-inside:avoid;}
.band.deep{background:var(--night-deep);}
.band h2,.band h3,.band h1{color:var(--paper);}
.band .eyebrow{color:var(--gold);}
.band a{color:var(--gold);}
.band .umber{color:#AEB6C6;}

/* stat trio */
.stats{display:flex;gap:0.3in;}
.stats .stat{flex:1;}
.stat .n{font-family:var(--fig);font-weight:700;font-variant-numeric:oldstyle-nums;
  font-size:46pt;line-height:0.9;color:var(--sunrise);}
.stat .n.sm{font-size:34pt;}
.stat .l{font-size:8.4pt;line-height:1.45;color:#C3CAD8;margin-top:0.5em;
  letter-spacing:0.01em;}
.band.light-stats{background:var(--paper-deep);color:var(--ink);}
.band.light-stats .l{color:var(--umber);}

/* numbered steps (vertical) */
.steps{margin:0.1in 0 0;}
.step{display:flex;gap:0.24in;padding:0.11in 0;border-top:1px solid var(--hairline);break-inside:avoid;}
.step:first-child{border-top:0;}
.step .sn{font-family:var(--fig);font-weight:700;font-variant-numeric:oldstyle-nums;
  font-size:26pt;line-height:0.9;color:var(--sunrise);flex:0 0 0.5in;text-align:right;}
.step .sb{flex:1;padding-top:0.04in;}
.step .sb b{font-family:var(--serif);font-weight:600;font-size:11.2pt;display:block;margin-bottom:0.12em;}
.step .sb span{font-size:9.7pt;color:#4a3f30;}

/* loop strip (horizontal) */
.loop{display:flex;gap:0;margin:0.12in 0 0.1in;break-inside:avoid;}
.loop .lp{flex:1;text-align:center;position:relative;padding:0 0.06in;}
.loop .lp .c{font-family:var(--fig);font-weight:700;font-variant-numeric:oldstyle-nums;
  font-size:22pt;color:var(--sunrise);line-height:1;}
.loop .lp .t{font-size:8.1pt;line-height:1.3;color:var(--ink);margin-top:0.4em;font-weight:500;}
.loop .lp:not(:last-child):after{content:"\2192";position:absolute;right:-0.02in;top:0.02in;
  color:var(--hairline);font-size:14pt;}
.band .loop .lp .t{color:#D8DEE8;}
.band .loop .lp:not(:last-child):after{color:rgba(214,222,232,0.45);}

/* definition / give-get grid */
.gg{display:flex;gap:0.34in;margin:0.2in 0;break-inside:avoid;}
.gg .c{flex:1;background:var(--paper-deep);border-radius:2px;padding:0.24in 0.26in;}
.gg .c.give{background:transparent;border:1px solid var(--hairline);}
.gg .c h4{font-size:8pt;letter-spacing:0.16em;text-transform:uppercase;color:var(--sunrise-ink);
  font-family:var(--sans);font-weight:600;margin-bottom:0.5em;}
.gg .c ul{margin:0;padding-left:1.05em;}
.gg .c li{font-size:9.6pt;margin-bottom:0.42em;line-height:1.45;}

/* tables */
table{width:100%;border-collapse:collapse;margin:0.16in 0;font-size:9.5pt;}
th{text-align:left;font-family:var(--sans);font-weight:600;font-size:7.6pt;letter-spacing:0.1em;
  text-transform:uppercase;color:var(--umber);border-bottom:1.5px solid var(--ink);
  padding:0.06in 0.14in 0.06in 0;vertical-align:bottom;}
td{padding:0.09in 0.14in 0.09in 0;border-bottom:1px solid var(--hairline);vertical-align:top;
  line-height:1.42;}
td:last-child,th:last-child{padding-right:0;}
tr{break-inside:avoid;}
td strong{font-family:var(--serif);font-weight:600;}
.tnum{font-family:var(--fig);font-weight:700;font-variant-numeric:oldstyle-nums;
  font-size:12pt;color:var(--sunrise-ink);white-space:nowrap;}

/* callout */
.callout{border-left:2px solid var(--sunrise);padding:0.02in 0 0.02in 0.22in;margin:0.2in 0;
  break-inside:avoid;}
.callout .q{font-family:var(--serif);font-style:italic;font-size:12.5pt;color:var(--ink);
  line-height:1.34;margin-bottom:0.4em;}
.pull{font-family:var(--serif);font-size:15pt;line-height:1.34;color:var(--ink);
  margin:0.22in 0;font-weight:600;letter-spacing:-0.01em;}

/* lists */
ul.clean{margin:0.08in 0 0.14in;padding-left:1.05em;}
ul.clean li{margin-bottom:0.4em;line-height:1.5;}
ol.clean{margin:0.08in 0 0.14in;padding-left:1.25em;}
ol.clean li{margin-bottom:0.42em;line-height:1.5;}

/* faq */
.faq{break-inside:avoid;margin:0 0 0.24in;}
.faq .qq{font-family:var(--serif);font-weight:600;font-size:12.4pt;color:var(--ink);
  margin-bottom:0.14em;line-height:1.24;}
.faq .aa{font-size:9.9pt;color:#372c1e;line-height:1.56;}
sup.ref{font-family:var(--sans);font-size:6.6pt;color:var(--sunrise-ink);font-weight:600;
  vertical-align:super;line-height:0;padding:0 0.02em;}

/* references */
.refs{counter-reset:r;font-size:9.2pt;}
.refs .r{display:flex;gap:0.16in;padding:0.09in 0;border-top:1px solid var(--hairline);break-inside:avoid;}
.refs .r:first-child{border-top:0;}
.refs .r .rn{font-family:var(--fig);font-weight:700;font-variant-numeric:oldstyle-nums;
  font-size:12pt;color:var(--sunrise-ink);flex:0 0 0.3in;}
.refs .r .rb{flex:1;line-height:1.44;}
.refs .r .rb .u{color:var(--umber);font-size:8pt;word-break:break-all;}

/* card mock */
.cardmock{display:flex;gap:0.3in;margin:0.2in 0;break-inside:avoid;align-items:stretch;}
.mockcard{width:3.05in;flex:0 0 auto;border-radius:6px;overflow:hidden;border:1px solid var(--hairline);}
.mockcard .top{background:var(--night);color:var(--paper);padding:0.2in 0.22in 0.18in;}
.mockcard .top .k{font-size:6.6pt;letter-spacing:0.18em;text-transform:uppercase;color:var(--gold);}
.mockcard .top .offer{font-family:var(--serif);font-size:15pt;font-weight:600;line-height:1.1;margin-top:0.1in;}
.mockcard .top .offer em{color:var(--gold);font-style:italic;}
.mockcard .bot{background:var(--paper);padding:0.16in 0.22in 0.18in;}
.mockcard .row{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1px solid var(--hairline);
  padding-bottom:0.5em;margin-bottom:0.5em;}
.mockcard .row .lab{font-size:6.4pt;letter-spacing:0.14em;text-transform:uppercase;color:var(--umber);}
.mockcard .row .val{font-family:var(--fig);font-weight:700;font-size:12pt;color:var(--ink);}
.mockcard .ser{font-family:'Inter';font-size:7pt;letter-spacing:0.06em;color:var(--umber);}
.cardmock .caption{flex:1;font-size:9.6pt;color:#3a2f22;align-self:center;}
.cardmock .caption b{font-family:var(--serif);}

/* small helper */
.note{font-size:8.7pt;color:var(--umber);line-height:1.5;}
.kicker{font-family:var(--sans);font-weight:600;font-size:7.6pt;letter-spacing:0.2em;
  text-transform:uppercase;color:var(--sunrise-ink);}
.spacer{height:0.14in;}

/* ===== cover ===== */
.cover{page:cover;background:var(--night);color:var(--paper);width:8.5in;height:11in;
  position:relative;overflow:hidden;page-break-after:always;}
.cover .kl{position:absolute;inset:0.42in;border:1.5px solid rgba(237,169,83,0.55);}
.cover .inner{position:absolute;inset:0.42in;padding:0.7in 0.72in;display:flex;flex-direction:column;}
.cover .mark{width:1.42in;height:auto;margin-bottom:0.42in;}
.cover .mark svg{width:100%;height:auto;display:block;}
.cover .wm{font-family:var(--serif);font-weight:600;font-size:41pt;letter-spacing:-0.015em;
  line-height:1.0;color:var(--paper);}
.cover .tag{font-family:var(--serif);font-style:italic;font-weight:400;font-size:16pt;
  color:var(--gold);margin-top:0.2in;}
.cover .fill{flex:1;}
.cover .subrule{border-top:1px solid rgba(237,169,83,0.4);width:1.1in;margin:0 0 0.28in;}
.cover .sub{font-family:var(--sans);font-weight:600;font-size:9pt;letter-spacing:0.24em;
  text-transform:uppercase;color:var(--paper);}
.cover .desc{font-family:var(--serif);font-size:13pt;color:#C6CEDC;margin-top:0.12in;line-height:1.4;max-width:4.4in;}
.cover .prep{margin-top:0.4in;font-size:9pt;color:#9aa4b6;line-height:1.9;letter-spacing:0.02em;}
.cover .prep .line{display:inline-block;border-bottom:1px solid rgba(198,206,220,0.4);width:2.5in;}
.cover .foot{margin-top:0.32in;font-size:8.2pt;letter-spacing:0.14em;color:#8892a4;text-transform:uppercase;}

/* ===== part divider (navy plate within frame) ===== */
.part{page-break-before:always;}
.plate{background:var(--night);color:var(--paper);border-radius:2px;padding:0.5in 0.5in 0.46in;
  break-inside:avoid;margin-bottom:0.28in;position:relative;}
.plate .pnum{font-family:var(--fig);font-weight:700;font-variant-numeric:oldstyle-nums;
  font-size:15pt;color:var(--gold);letter-spacing:0.06em;}
.plate h1{color:var(--paper);font-size:26pt;margin:0.14in 0 0.12in;letter-spacing:-0.01em;}
.plate .pd{font-family:var(--serif);font-style:italic;font-size:12.5pt;color:#C6CEDC;line-height:1.4;max-width:5in;}
.plate .toc{margin-top:0.28in;border-top:1px solid rgba(198,206,220,0.28);padding-top:0.18in;
  font-size:9pt;color:#AEB6C6;line-height:1.85;}
.plate .toc b{color:var(--paper);font-family:var(--serif);font-weight:600;}

/* ===== closing CTA ===== */
.closing{page-break-before:always;}

/* ===== TOC ===== */
.toc-page{page-break-before:always;}
.toc-h{font-family:var(--serif);font-weight:600;font-size:24pt;margin-bottom:0.06in;}
.toc-list{margin-top:0.24in;}
.toc-grp{font-family:var(--sans);font-weight:600;font-size:7.8pt;letter-spacing:0.2em;
  text-transform:uppercase;color:var(--sunrise-ink);margin:0.24in 0 0.1in;}
.toc-grp:first-child{margin-top:0;}
.toc-row{display:flex;align-items:baseline;gap:0.1in;padding:0.055in 0;font-size:10.2pt;}
.toc-row .tt{white-space:nowrap;}
.toc-row .tt.b{font-family:var(--serif);font-weight:600;}
.toc-row .dots{flex:1;border-bottom:1px dotted var(--hairline);transform:translateY(-0.03in);}
.toc-row .pg{font-family:var(--fig);font-weight:700;font-variant-numeric:oldstyle-nums;
  font-size:11pt;color:var(--umber);}
.toc-row .sub{color:var(--umber);}

/* back cover */
.back{page:cover;background:var(--night-deep);color:var(--paper);width:8.5in;height:11in;
  position:relative;page-break-before:always;overflow:hidden;}
.back .c{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;
  justify-content:center;text-align:center;padding:1in;}
.back .mark{width:1.15in;margin-bottom:0.34in;}
.back .mark svg{width:100%;display:block;}
.back .wm{font-family:var(--serif);font-weight:600;font-size:22pt;color:var(--paper);}
.back .tag{font-family:var(--serif);font-style:italic;font-size:13pt;color:var(--gold);margin-top:0.14in;}
.back .ct{margin-top:0.5in;font-size:9pt;letter-spacing:0.14em;text-transform:uppercase;color:#8892a4;line-height:2;}
"""

# ---------------------------------------------------------------- helpers
def opener(eyebrow, num, title, dek):
    return f"""
<div class="opener">
  <div class="num">{num}</div>
  <div class="htext">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{title}</h1>
    <div class="dek">{dek}</div>
  </div>
</div>
<hr class="rule">"""

def ref(n):
    return f'<sup class="ref">{n}</sup>'

# ---------------------------------------------------------------- content
def cover():
    return f"""
<div class="cover">
  <div class="kl"></div>
  <div class="inner">
    <div class="mark">{MARK_DARK}</div>
    <div class="wm">Knox<br>Pick-Me-Up</div>
    <div class="tag">Ride from last call to first cup.</div>
    <div class="fill"></div>
    <div class="subrule"></div>
    <div class="sub">Program Details</div>
    <div class="desc">A downtown Knoxville road-safety partnership &mdash; rewarding the safe ride home with tomorrow&rsquo;s coffee.</div>
    <div class="prep">Prepared for&nbsp;&nbsp;<span class="line"></span></div>
    <div class="foot">Knoxville, Tennessee &nbsp;&middot;&nbsp; hello@knoxpickmeup.org &nbsp;&middot;&nbsp; knoxpickmeup.org</div>
  </div>
</div>"""

# TOC uses placeholders {P:key} filled after first render
def toc():
    rows = [
        ("grp","The one-page idea"),
        ("row","Executive summary","execsummary",False),
        ("grp","Part I · The Opportunity"),
        ("row","1  The problem","s_problem",False),
        ("row","2  The insight","s_insight",False),
        ("row","3  The idea, in one line","s_idea",False),
        ("grp","Part II · How It Works"),
        ("row","4  The patron journey","s_journey",False),
        ("row","5  The Morning Pick-Me-Up Card","s_card",False),
        ("row","6  Trust by design","s_trust",False),
        ("row","7  The car stays put","s_parking",False),
        ("grp","Part III · Why It Works for Everyone"),
        ("row","8  Downtown bars","s_bars",False),
        ("row","9  Coffee shops","s_shops",False),
        ("row","10  City of Knoxville & KPD","s_city",False),
        ("row","11  Knoxville Area Transit (KAT)","s_kat",False),
        ("row","12  Downtown Parking Authority","s_park",False),
        ("row","13  Sponsors","s_sponsors",False),
        ("grp","Part IV · Making It Real"),
        ("row","14  What we ask of you","s_ask",False),
        ("row","15  Built to sustain itself","s_fund",False),
        ("row","16  The pilot","s_pilot",False),
        ("row","17  How we’ll know it’s working","s_metrics",False),
        ("row","18  Risks, and how we’ve handled them","s_risks",False),
        ("row","19  Frequently asked questions","s_faq",False),
        ("grp","Closing"),
        ("row","The invitation","s_invite",False),
        ("grp","Appendices"),
        ("row","A  Technical architecture","a_tech",False),
        ("row","B  The card & anti-forgery serialization","a_serial",False),
        ("row","C  Data, privacy & backups","a_privacy",False),
        ("row","D  The print kit & production","a_print",False),
        ("row","E  Financial detail","a_finance",False),
        ("row","F  Evidence & references","a_refs",False),
        ("row","G  Brand at a glance","a_brand",False),
        ("row","H  Forking this for your community","a_fork",False),
    ]
    html = ['<div class="toc-page"><div class="eyebrow">Contents</div><div class="toc-h">Program Details</div>',
            '<div class="lead measure">Written so you can open it flat on the table and turn to the one page a partner needs &mdash; every Part III partner page and the FAQ stands on its own.</div>',
            '<div class="toc-list">']
    for item in rows:
        if item[0]=="grp":
            html.append(f'<div class="toc-grp">{item[1]}</div>')
        else:
            _,label,key,bold = item
            b = " b" if bold else ""
            html.append(f'<div class="toc-row"><span class="tt{b}">{label}</span>'
                        f'<span class="dots"></span><span class="pg">{{P:{key}}}</span></div>')
    html.append('</div></div>')
    return "\n".join(html)

def execsummary():
    return f"""
<div class="section"><a id="execsummary"></a>
{opener("The one-page idea","","Executive summary","If someone reads only this page.")}
<p class="lead measure">Impaired driving keeps hurting people on Knoxville&rsquo;s roads &mdash; in the region, crashes involving an impaired driver seriously injure about <strong>67 people and kill 27 every year</strong>, and <strong>one in three</strong> Knox County crash deaths involves an impaired driver.{ref(13)} The single biggest reason people talk themselves into driving home is the car they parked downtown.</p>

<p class="measure"><strong>Knox Pick-Me-Up doesn&rsquo;t fight the car &mdash; it uses it.</strong> A patron who drove downtown and chooses a safe ride home &mdash; a rideshare, a taxi, or a KAT bus &mdash; shows that ride to a bartender and gets a <strong>Morning Pick-Me-Up Card</strong>: good for a <em>free large coffee</em> at a participating shop when they come back the next morning for their car, and a free KAT ride to get there. The card is framed as a <em>thank-you</em> for keeping our roads safe &mdash; not a coupon, and never a lecture.</p>

<div class="band">
  <div class="eyebrow">The loop, in one line</div>
  <div class="loop">
    <div class="lp"><div class="c">1</div><div class="t">Drive downtown, park</div></div>
    <div class="lp"><div class="c">2</div><div class="t">Take a safe ride home</div></div>
    <div class="lp"><div class="c">3</div><div class="t">Show the ride &rarr; get the card</div></div>
    <div class="lp"><div class="c">4</div><div class="t">Free KAT ride back</div></div>
    <div class="lp"><div class="c">5</div><div class="t">Free coffee, drive home sober</div></div>
  </div>
</div>

<h3 class="sub">Why it works for everyone</h3>
<p class="measure">Bars get free branded coasters, a safer close, and their name on a city-backed safety program for a 10-second hand-off. Coffee shops get morning traffic from a late-night crowd they rarely see. The City and KPD get a positive-incentive complement to enforcement. KAT gets first-time riders. The Downtown Parking Authority gets its free-nights-and-weekends message in front of the exact people who need it. Sponsors get their name on the safe ride home, in every bar downtown.</p>

<h3 class="sub">The ask, and the cost</h3>
<p class="measure">The coffee is carried by the shops as customer acquisition &mdash; the way they&rsquo;d fund any promotion &mdash; and KAT rides are KAT&rsquo;s in-kind contribution, so the program&rsquo;s only real cash need is a modest set of pilot fixed costs (printing, a part-time coordinator, launch) on the order of <strong>~$18,000</strong> for six months. The marginal cost of one more safe ride home is essentially zero. One prevented crash pays for the entire pilot many times over.{ref(1)}</p>
</div>"""

def part_divider(pnum, title, dek, toc_lines):
    tl = "<br>".join(toc_lines)
    return f"""
<div class="part">
  <div class="plate">
    <div class="pnum">{pnum}</div>
    <h1>{title}</h1>
    <div class="pd">{dek}</div>
    <div class="toc">{tl}</div>
  </div>
</div>"""

def part1():
    out = [part_divider("Part I","The Opportunity",
        "The problem worth solving, the insight that makes this different, and the whole idea in a single line.",
        ["<b>1</b>&ensp;The problem","<b>2</b>&ensp;The insight","<b>3</b>&ensp;The idea, in one line"])]
    # 1 problem
    out.append(f"""
<div class="section"><a id="s_problem"></a>
{opener("Part I · The Opportunity","1","The problem","Impaired driving on Knoxville’s roads, and the moment of decision at last call.")}
<div class="cols">
<p>People drive downtown, drink more than they planned, and then face a choice: pay for a ride home <em>and</em> a ride back tomorrow &mdash; plus the hassle of retrieving the car &mdash; or just drive. Told that way, the parked car does most of the arguing for driving.</p>
<p>The human cost of the choice going wrong is not abstract in Knoxville. It falls on families, on emergency rooms, and on the people in the other car. Enforcement and education both matter, but neither changes the incentives a person actually weighs at 1&nbsp;a.m. with a car half a block away.</p>
</div>
<div class="band">
  <div class="eyebrow">The toll, every year</div>
  <div class="stats">
    <div class="stat"><div class="n">67</div><div class="l">people seriously injured in area crashes involving an impaired driver{ref(13)}</div></div>
    <div class="stat"><div class="n">27</div><div class="l">people killed in those crashes, each year{ref(13)}</div></div>
    <div class="stat"><div class="n">1<span style="font-size:24pt">&nbsp;in&nbsp;</span>3</div><div class="l">Knox County crash deaths involves an impaired driver{ref(13)}</div></div>
  </div>
</div>
<p class="measure note">Sources: Knoxville Regional Transportation Planning Organization (annual injuries and fatalities in area impaired-driving crashes); Knox County Health Department (share of deadly crashes involving an impaired driver).</p>
</div>""")
    # 2 insight
    out.append(f"""
<div class="section"><a id="s_insight"></a>
{opener("Part I · The Opportunity","2","The insight","Don’t fight the parked car &mdash; use it. Reward the safe choice when it’s made, and cash it in when it pays off.")}
<p class="lead measure">The car that makes people want to drive is also a guarantee: it means the patron <em>will</em> be back downtown in the morning. That&rsquo;s the opening.</p>
<div class="cols">
<p>Knox Pick-Me-Up rewards the safe choice at the exact moment it&rsquo;s made &mdash; last call, at the bar &mdash; and lets the patron cash it in at the exact moment the choice pays off: the morning trip back for the car. Downtown gets the visitor twice, and one more impaired driver stays off the road.</p>
<p>The framing carries the whole program. The card is a <strong>thank-you</strong>, not a coupon &mdash; Knoxville recognizing the most valuable thing a patron did all night, which was getting home without driving. Warm and non-preachy, it makes a free coffee feel like recognition rather than a payout, and it sets up community-funded models where tonight&rsquo;s crowd can stand the coffee for tomorrow&rsquo;s safe riders.</p>
</div>
<div class="callout">
  <div class="q">&ldquo;Good call &mdash; coffee&rsquo;s on us.&rdquo;</div>
  <div class="note">The voice, everywhere: warm, wry, zero lecture. Never &ldquo;don&rsquo;t drink and drive&rdquo;; always a thank-you for the safe ride home.</div>
</div>
</div>""")
    # 3 idea
    out.append(f"""
<div class="section"><a id="s_idea"></a>
{opener("Part I · The Opportunity","3","The idea, in one line","Last call → ride home → morning → coffee. One loop that closes itself.")}
<div class="band">
  <div class="loop">
    <div class="lp"><div class="c">1</div><div class="t">Drove downtown,<br>parked the car</div></div>
    <div class="lp"><div class="c">2</div><div class="t">Took a safe ride<br>home instead</div></div>
    <div class="lp"><div class="c">3</div><div class="t">Showed the ride,<br>got a dated card</div></div>
    <div class="lp"><div class="c">4</div><div class="t">Free KAT ride<br>back downtown</div></div>
    <div class="lp"><div class="c">5</div><div class="t">Free coffee,<br>then drove home sober</div></div>
  </div>
</div>
<p class="lead measure">Every step is something the patron already wanted to do, made a little easier or a little more rewarding. The card is the thread that ties the safe choice at night to the payoff in the morning &mdash; and because the reward waits until the next day, it can only be claimed by someone who genuinely left the car and came back for it.</p>
<p class="measure">The rest of this document is simply that loop, told from each partner&rsquo;s point of view &mdash; how it works at the bar, at the counter, and on the bus; why every partner comes out ahead; and how it pays for itself.</p>
</div>""")
    return "\n".join(out)

def part2():
    out = [part_divider("Part II","How It Works",
        "The patron&rsquo;s six steps, the card itself, the trust that keeps it honest, and the parked car that makes it all possible.",
        ["<b>4</b>&ensp;The patron journey","<b>5</b>&ensp;The Morning Pick-Me-Up Card","<b>6</b>&ensp;Trust by design","<b>7</b>&ensp;The car stays put"])]
    # 4 journey
    out.append(f"""
<div class="section"><a id="s_journey"></a>
{opener("Part II · How It Works","4","The patron journey","Six steps, most of which the patron was going to take anyway.")}
<div class="steps">
  <div class="step"><div class="sn">1</div><div class="sb"><b>Out for the night</b><span>Patron drives downtown, parks, and goes out.</span></div></div>
  <div class="step"><div class="sn">2</div><div class="sb"><b>Chooses a safe ride home</b><span>At the end of the night, they take a booked rideshare or taxi, or a KAT bus &mdash; instead of driving.</span></div></div>
  <div class="step"><div class="sn">3</div><div class="sb"><b>Shows proof of the ride</b><span>They show a bartender a confirmed rideshare screen or an activated transit ticket &mdash; a 10-second glance.</span></div></div>
  <div class="step"><div class="sn">4</div><div class="sb"><b>Gets a Morning Pick-Me-Up Card</b><span>The bartender writes today&rsquo;s date on the card and hands it over &mdash; one card per ride.</span></div></div>
  <div class="step"><div class="sn">5</div><div class="sb"><b>Rides KAT free back to the car</b><span>While valid, the card doubles as a free KAT pass &mdash; &ldquo;Hair of the KAT&rdquo; &mdash; including the morning trip back downtown.</span></div></div>
  <div class="step"><div class="sn">6</div><div class="sb"><b>Claims the coffee, drives home sober</b><span>At a participating shop the next morning, they redeem a free large coffee, retrieve the car, and drive home clear-headed.</span></div></div>
</div>
<div class="callout">
  <div class="q">The reward waits until morning &mdash; on purpose.</div>
  <div class="note">Because the coffee can only be claimed the next day, at the car, the card structurally can&rsquo;t reward anything except actually leaving the car overnight and coming back for it.</div>
</div>
</div>""")
    # 5 card
    out.append(f"""
<div class="section"><a id="s_card"></a>
{opener("Part II · How It Works","5","The Morning Pick-Me-Up Card","A wallet-sized thank-you: one free large coffee, and a free ride to come get it.")}
<div class="cardmock">
  <div class="mockcard">
    <div class="top">
      <div class="k">Knox Pick-Me-Up &middot; Thank you for the safe ride home</div>
      <div class="offer">One free<br>large coffee <em>&mdash; on us.</em></div>
    </div>
    <div class="bot">
      <div class="row"><div><div class="lab">Date issued</div></div><div class="val">&mdash;&nbsp;/&nbsp;&mdash;&nbsp;/&nbsp;&mdash;&mdash;</div></div>
      <div class="row" style="border-bottom:0;margin-bottom:0.2em;"><div class="lab">Valid one day &middot; Hair&nbsp;of&nbsp;the&nbsp;KAT: free bus fare</div></div>
      <div class="ser">KPMU-2026-00004217T</div>
    </div>
  </div>
  <div class="caption"><b>The perks.</b> One free large coffee (no cash value; any add-ons are on the customer). While valid, the card is also free KAT fare &mdash; the free ride back downtown to the car. A serial and unique QR make each card traceable and one-time.</div>
</div>
<h3 class="sub">Card rules, in plain terms</h3>
<ul class="clean">
  <li><strong>One card per ride</strong> &mdash; the ride is the ticket. A group sharing one Uber gets one card; two rides, two cards. Cards are handed out while supplies last, so a bar that&rsquo;s out for the night can simply say so.</li>
  <li><strong>Valid one day from issue.</strong> The bartender writes the date by hand at hand-out; that written date is both the record and the start of the one-day window &mdash; long enough for the morning-after trip, short enough to prevent hoarding.</li>
  <li><strong>&ldquo;Hair of the KAT.&rdquo;</strong> A valid card is free KAT fare during its window &mdash; show it to board any bus, including the ride back to the car.</li>
  <li><strong>Designated-driver exception, bartender&rsquo;s call.</strong> A sober driver taking everyone home is the exact behavior the program rewards; a bartender may hand them a card at their discretion. A tool for staff, not a patron entitlement.</li>
</ul>
</div>""")
    # 6 trust
    out.append(f"""
<div class="section"><a id="s_trust"></a>
{opener("Part II · How It Works","6","Trust by design","Two touches keep it honest &mdash; and the worst case is one free coffee.")}
<div class="gg">
  <div class="c give"><h4>Touch one &middot; at the bar</h4><ul>
    <li>The bartender dates the card at the moment of proof.</li>
    <li>Books of 50 are checked out to each bar, so every serial traces to a venue and a week.</li>
  </ul></div>
  <div class="c"><h4>Touch two &middot; at the shop</h4><ul>
    <li>The barista scans the card&rsquo;s QR at redemption &mdash; logged automatically, no typing.</li>
    <li>Duplicate or mismatched serials are flagged instantly; a lost pack is voided with one cell.</li>
  </ul></div>
</div>
<div class="cols">
<p><strong>Serialized, and un-inventable.</strong> Every card carries a unique number ending in a keyed checksum letter, so serials can&rsquo;t be minted by counting up from a card in hand. A made-up serial fails at the register and is logged as an attempt.</p>
<p><strong>Short expiry</strong> kills any secondary-market or stockpiling value &mdash; a card is worth a coffee for one day and nothing after.</p>
<p><strong>Pack kill switch.</strong> A lost, stolen, or misprinted pack is voided in one step; from that moment every card in it fails to scan everywhere, and attempts are logged with where they turned up.</p>
<p><strong>Proportionate by design.</strong> The worst case of a gamed card is a single free coffee, so the controls stay light enough to keep the bar interaction to ten seconds. Bartender discretion is a feature, not a loophole: staff already judge sobriety and IDs, and can decline without confrontation.</p>
</div>
<p class="note measure">The full logging architecture &mdash; a static site plus a Google Sheet, $0/month, no server to babysit &mdash; is in Appendix A, and the serialization scheme in Appendix B.</p>
</div>""")
    # 7 parking
    out.append(f"""
<div class="section"><a id="s_parking"></a>
{opener("Part II · How It Works","7","The car stays put","Leaving the car overnight has to feel free and safe &mdash; and in Knoxville, it already is.")}
<p class="lead measure">The program doesn&rsquo;t have to negotiate a parking policy. Downtown&rsquo;s public parking &mdash; municipal garages and surface lots alike &mdash; is already <strong>free after 6&nbsp;p.m. on weeknights and all weekend.</strong></p>
<div class="cols">
<p>What&rsquo;s missing isn&rsquo;t free parking &mdash; it&rsquo;s the <em>knowledge</em> of it at the decision moment. So the program advertises the free-parking reality loudly, on coasters, cards, and signage, so patrons stop treating &ldquo;but my car&rdquo; as a reason to drive.</p>
<p>This is exactly where the <strong>Downtown Parking Authority</strong> comes in as a partner (page&nbsp;{{P:s_park}}): the program amplifies their free-nights-and-weekends message to the precise audience that needs it, and they give patrons a worry-free place to leave the car. Messaging is coordinated with the City so posted hours and any move-out times are stated accurately; where a public facility isn&rsquo;t nearby, private lot operators are recruited as sponsors.</p>
</div>
</div>""")
    return "\n".join(out)

def gg_block(give_title, give, get_title, get):
    gl = "".join(f"<li>{x}</li>" for x in give)
    gr = "".join(f"<li>{x}</li>" for x in get)
    return f"""<div class="gg">
  <div class="c give"><h4>{give_title}</h4><ul>{gl}</ul></div>
  <div class="c"><h4>{get_title}</h4><ul>{gr}</ul></div>
</div>"""

def part3():
    out = [part_divider("Part III","Why It Works for Everyone",
        "One page per partner &mdash; what they give, and what they get. Turn to the page for whoever&rsquo;s across the table.",
        ["<b>8</b>&ensp;Downtown bars","<b>9</b>&ensp;Coffee shops","<b>10</b>&ensp;City of Knoxville & KPD","<b>11</b>&ensp;KAT","<b>12</b>&ensp;Downtown Parking Authority","<b>13</b>&ensp;Sponsors"])]

    out.append(f"""
<div class="section"><a id="s_bars"></a>
{opener("Part III · The distribution network","8","Downtown bars","The card starts in your hand. The ask is a 10-second date-and-hand at last call.")}
<p class="lead measure">&ldquo;Free coasters and signage, a safer close to your night, and your name on a city-backed road-safety program &mdash; for handing a dated card to someone who books a ride home.&rdquo;</p>
{gg_block("What we ask of you",
  ["A 10-second hand-off: glance at the ride, write the date, hand over one card.",
   "Keep a book of cards behind the bar and a laminated reference by the register.",
   "A quick pre-shift mention so staff know the drill."],
  "What you get",
  ["Free branded coasters that replace stock you already buy &mdash; and do the marketing passively.",
   "A safer, calmer close to the night and reduced dram-shop-adjacent risk.",
   "Early-partner billing: your logo on cards and in the press launch.",
   "$0 to join at pilot &mdash; the program supplies every material and card book."])}
<p class="note measure">Where to start: 5&ndash;8 anchor venues in the Old City and Market Square whose owners talk to each other. Early billing creates real FOMO for the second wave. A small monthly staff perk &mdash; coffee for the crew &mdash; keeps buy-in high.</p>
</div>""")

    out.append(f"""
<div class="section"><a id="s_shops"></a>
{opener("Part III · The redemption network","9","Coffee shops","Morning traffic from a crowd you don’t currently see &mdash; and you control the exposure.")}
<p class="lead measure">&ldquo;The late-night crowd, in your shop the next morning &mdash; plus your logo in every bar downtown. Cap your exposure while we prove the ticket math together.&rdquo;</p>
{gg_block("What we ask of you",
  ["Honor the card for one free large coffee, and scan its QR at the register.",
   "Provide the coffee as your own customer-acquisition cost, the way you&rsquo;d fund any promotion.",
   "Help co-design the funding model &mdash; real co-ownership, not a terms sheet."],
  "What you get",
  ["First-time morning visits from customers you rarely reach &mdash; and the regulars a good first cup creates.",
   "Your logo in every participating bar downtown.",
   "A monthly redemption cap you control while the model proves out.",
   "Monthly data back: redemptions and average-ticket uplift, so the value is visible."])}
<p class="note measure">Why the math works: the card brings in a crowd you don&rsquo;t see in the morning, a large coffee is a small pour against a morning ticket that usually runs higher, and a good first visit makes a regular. Recruit shops within a short walk of the major garages first &mdash; Gay Street, Market Square, the Old City.</p>
</div>""")

    out.append(f"""
<div class="section"><a id="s_city"></a>
{opener("Part III · Credibility & safer streets","10","City of Knoxville & KPD","A positive-incentive complement to enforcement &mdash; a carrot to pair with the stick.")}
<p class="lead measure">&ldquo;One prevented impaired-driving crash costs the city far more than this program&rsquo;s entire pilot.{ref(1)} The asks are mostly promotion, not an open-ended budget line.&rdquo;</p>
{gg_block("What we ask of you",
  ["<b>City:</b> co-promote the already-free evening and weekend municipal parking, and include the program in city communications.",
   "<b>City:</b> optional one-time seed for launch costs &mdash; treated strictly as seed, never the operating model.",
   "<b>KPD:</b> a public endorsement and a program mention at high-risk moments &mdash; football Saturdays, New Year&rsquo;s, holiday weekends.",
   "<b>KPD:</b> no enforcement role inside bars; endorser, not operator."],
  "What you get",
  ["A measurable, positive complement to enforcement and education &mdash; part of the multi-component approach the evidence actually supports.{}".format(ref(3)),
   "Full transparency: quarterly issuance and redemption data by venue.",
   "A program that is never surveillance &mdash; cards are anonymous, and no personal data is ever collected.",
   "Goodwill: Knoxville visibly thanking people for keeping the roads safe."])}
<p class="note measure">KPD is a supporter, not an operator. The program must never feel like a checkpoint; every card is simply a documented decision not to drive home impaired.</p>
</div>""")

    out.append(f"""
<div class="section"><a id="s_kat"></a>
{opener("Part III · The ride home & back","11","Knoxville Area Transit","&ldquo;Hair of the KAT&rdquo;: an accepted ride, and a free-ride partner.")}
<p class="lead measure">&ldquo;Riders already taking the bus home safely should qualify too &mdash; and a valid card should let anyone ride KAT free while it lasts, including the morning trip back to the car.&rdquo;</p>
{gg_block("What we ask of you",
  ["Recognize an activated KAT ticket as valid ride proof at the bar.",
   "Accept a valid Pick-Me-Up Card as free fare during its one-day window.",
   "Help communicate late-night and weekend routes and hours to patrons and bar staff."],
  "What you get",
  ["KAT in front of the exact crowd that needs a late ride &mdash; and first-time riders who stick.",
   "Off-peak, morning-trip ridership the card sends straight to you.",
   "Exposure naturally capped: the card is valid one day only, so cost is contained.",
   "Clean, anonymous ridership data (a driver count or farebox code)."])}
<p class="note measure">Structure: the free rides are KAT&rsquo;s in-kind contribution to a shared road-safety goal &mdash; new riders and goodwill in exchange, not a program payout. Sponsorship can support KAT&rsquo;s marketing of the program if useful. There is no longer a free downtown trolley, so this free-ride benefit is something the program provides &mdash; it doesn&rsquo;t lean on a pre-existing service.</p>
</div>""")

    out.append(f"""
<div class="section"><a id="s_park"></a>
{opener("Part III · A worry-free place for the car","12","Downtown Parking Authority","We carry your free-nights-and-weekends message to the people who most need to hear it.")}
<p class="lead measure">&ldquo;Downtown parking is already free on nights and weekends &mdash; the problem is that patrons don&rsquo;t know it at the moment they&rsquo;re deciding whether to drive. We put that message on the coaster under their drink.&rdquo;</p>
{gg_block("What we ask of you",
  ["Confirm the free evening and weekend hours (and any exceptions) so we state them accurately.",
   "Let the program amplify your free-parking communications on coasters, cards, and signage.",
   "Coordinate on any move-out times or special-event pricing so patrons aren&rsquo;t surprised."],
  "What you get",
  ["Your core message &mdash; free parking nights and weekends &mdash; in front of the precise audience deciding whether to leave the car.",
   "More overnight use of municipal garages and lots on program nights.",
   "A partner actively reassuring drivers that leaving the car is easy, free, and safe.",
   "Alignment with a city-backed road-safety initiative."])}
<p class="note measure">Leaving the car overnight has to feel free and safe or the whole program falls apart &mdash; which makes the Parking Authority&rsquo;s message not a nice-to-have but load-bearing. Where a public facility isn&rsquo;t nearby, private lot operators can join as sponsors.</p>
</div>""")

    out.append(f"""
<div class="section"><a id="s_sponsors"></a>
{opener("Part III · The accelerant","13","Sponsors","Your name on the safe ride home &mdash; in every bar downtown.")}
<p class="lead measure">&ldquo;Annual &lsquo;presented by&rsquo; placement on coasters and cards already in every bar downtown &mdash; unusually good placement per dollar &mdash; funding a program whose entire purpose aligns with your interests.&rdquo;</p>
{gg_block("What we ask of you",
  ["An annual sponsorship that covers fixed costs the per-coffee models don&rsquo;t &mdash; printing and a coordinator.",
   "A logo file to the spec in the outreach one-sheet.",
   "For patron-facing materials: no alcohol brands."],
  "What you get",
  ["Your logo in a &ldquo;printing donated by&rdquo; slot on coasters and cards &mdash; without touching the program mark.",
   "Association with a positive, city- and KPD-backed road-safety story.",
   "Natural fit for rideshare companies, auto insurers, trauma systems, parking operators, and downtown property owners.",
   "A ready-made outreach one-sheet: what it funds, where the logo rides, the spec."])}
<p class="note measure">The placement is already built into the toolkit &mdash; a single flag drops a sponsor logo into the donated-printing slot on cards and both coaster sides. Details in Appendix D and Appendix E.</p>
</div>""")
    return "\n".join(out)

def part4():
    out = [part_divider("Part IV","Making It Real",
        "The ask, the funding, the pilot, the metrics, the risks &mdash; and the hard questions, answered honestly.",
        ["<b>14</b>&ensp;What we ask of you","<b>15</b>&ensp;Built to sustain itself","<b>16</b>&ensp;The pilot","<b>17</b>&ensp;How we&rsquo;ll know it&rsquo;s working","<b>18</b>&ensp;Risks & mitigations","<b>19</b>&ensp;Frequently asked questions"])]

    out.append(f"""
<div class="section"><a id="s_ask"></a>
{opener("Part IV · Making It Real","14","What we ask of you","Every ask is small, specific, and sized to the partner.")}
<table>
<thead><tr><th style="width:1.7in">Partner</th><th>The ask</th></tr></thead>
<tbody>
<tr><td><strong>Downtown bars</strong></td><td>A 10-second date-and-hand at last call; keep card books and a reference behind the bar.</td></tr>
<tr><td><strong>Coffee shops</strong></td><td>Honor the card for one large coffee and scan it; provide the coffee as customer acquisition; help pick the funding model.</td></tr>
<tr><td><strong>City of Knoxville</strong></td><td>Co-promote free evening/weekend parking; include the program in city comms; optional one-time launch seed.</td></tr>
<tr><td><strong>KPD</strong></td><td>Public endorsement and a mention at high-risk moments; no enforcement role in bars.</td></tr>
<tr><td><strong>KAT</strong></td><td>Accept transit tickets as ride proof; accept a valid card as free fare; help communicate late-night service.</td></tr>
<tr><td><strong>Parking Authority</strong></td><td>Confirm free-parking hours; let the program amplify that message; coordinate on exceptions.</td></tr>
<tr><td><strong>Sponsors</strong></td><td>Annual support for fixed costs; a logo file; no alcohol brands on patron-facing materials.</td></tr>
</tbody>
</table>
<h3 class="sub">The order we recruit in</h3>
<ol class="clean">
  <li><strong>City + KPD first</strong> &mdash; credibility unlocks everything else.</li>
  <li><strong>Three anchor coffee shops</strong> &mdash; redemption must exist before issuance; they co-design the funding model.</li>
  <li><strong>Five to eight anchor bars</strong> for the pilot footprint.</li>
  <li><strong>KAT</strong> to confirm ride proof, the free-ride benefit, and service messaging.</li>
  <li><strong>Parking Authority</strong> to lock the free-parking message.</li>
  <li><strong>Sponsors</strong>, once the partner map makes the placement value concrete.</li>
  <li><strong>Press launch</strong> with the City and KPD, tied to a high-risk weekend &mdash; then a data-driven second wave.</li>
</ol>
</div>""")

    out.append(f"""
<div class="section"><a id="s_fund"></a>
{opener("Part IV · Making It Real","15","Built to sustain itself","The perk is always free to the patron who took the safe ride. Here&rsquo;s who carries it.")}
<p class="lead measure">The funding model is deliberately open &mdash; it gets locked with partners as they come on board &mdash; but one constraint is fixed. Candidate streams, roughly in order of long-run durability:</p>
<table>
<thead><tr><th style="width:1.9in">Stream</th><th>How it works</th></tr></thead>
<tbody>
<tr><td><strong>A &middot; Merchant-funded</strong><br><span class="note">the self-sustaining core</span></td><td>Shops provide the coffee as their own customer-acquisition cost. Zero external money; scales automatically with participation. The large coffee is a small pour against a higher morning ticket.</td></tr>
<tr><td><strong>B &middot; Community round-up</strong><br><span class="note">parked for the pilot</span></td><td>An optional $1 line on bar tabs &mdash; tonight&rsquo;s crowd stands tomorrow&rsquo;s coffee. Kept as a switch-on-later option; deliberately absent from pilot materials.</td></tr>
<tr><td><strong>C &middot; Sponsorship tiers</strong><br><span class="note">the accelerant</span></td><td>Annual &ldquo;presented by&rdquo; packages cover fixed costs the per-coffee models don&rsquo;t. Logos ride on coasters and cards already in every bar.</td></tr>
<tr><td><strong>D &middot; Bar partner dues</strong><br><span class="note">optional, later</span></td><td>A modest membership once foot-traffic value is proven. Held in reserve &mdash; free entry is what makes the network dense at pilot.</td></tr>
<tr><td><strong>E &middot; Grants & city seed</strong><br><span class="note">launch only</span></td><td>One-time money for the pilot&rsquo;s fixed costs. Seed, never the operating model.</td></tr>
</tbody>
</table>
<div class="band light-stats">
  <div class="eyebrow" style="color:var(--sunrise-ink)">Recommended architecture</div>
  <p style="margin:0;color:#3a2f22;font-size:10pt;">Model <strong>A</strong> as the base (the coffee costs the program nothing in cash), <strong>C</strong> to cover fixed costs, <strong>E</strong> to launch, with <strong>B</strong> held as the community flywheel and <strong>D</strong> in reserve. KAT rides are KAT&rsquo;s in-kind contribution. Under this structure, the marginal cost of one more safe ride home is approximately zero &mdash; which is what makes it durable.</p>
</div>
<p class="note measure">Illustrative pilot fixed costs and coupon economics are in Appendix E.</p>
</div>""")

    out.append(f"""
<div class="section"><a id="s_pilot"></a>
{opener("Part IV · Making It Real","16","The pilot","One footprint, one season, then evaluate honestly and scale.")}
<table>
<thead><tr><th style="width:1.7in">Phase</th><th style="width:1.1in">Window</th><th>Milestones</th></tr></thead>
<tbody>
<tr><td><strong>Design & city buy-in</strong></td><td class="tnum">Months 0&ndash;2</td><td>City / KPD memorandum of understanding; free-parking co-promotion agreement with the Parking Authority.</td></tr>
<tr><td><strong>Partner recruitment</strong></td><td class="tnum">Months 2&ndash;3</td><td>Three coffee shops, six bars, and KAT signed; funding architecture locked with partners; materials printed.</td></tr>
<tr><td><strong>Pilot launch</strong></td><td class="tnum">Month 4</td><td>Press event on a high-visibility weekend.</td></tr>
<tr><td><strong>Pilot run</strong></td><td class="tnum">Months 4&ndash;9</td><td>Monthly reconciliation; a mid-pilot tune-up.</td></tr>
<tr><td><strong>Evaluate & scale</strong></td><td class="tnum">Month 10+</td><td>Public report; second-wave recruitment; sponsor expansion.</td></tr>
</tbody>
</table>
<div class="callout">
  <div class="q">Success gates for the pilot</div>
  <div class="note">&ge;60% of anchor bars actively issuing by month&nbsp;2 &middot; &ge;50% redemption rate &middot; average redemption ticket comfortably above the coffee&rsquo;s cost &middot; zero material fraud incidents &middot; partner renewal intent.</div>
</div>
</div>""")

    out.append(f"""
<div class="section"><a id="s_metrics"></a>
{opener("Part IV · Making It Real","17","How we’ll know it’s working","Real numbers &mdash; and a privacy stance we can state out loud.")}
<div class="cols">
<p><strong>Primary.</strong> Cards issued and redeemed, by venue and by night of week &mdash; the pulse of the program.</p>
<p><strong>Road safety.</strong> Late-night impaired-driving crashes, arrests, and single-vehicle incidents in the downtown zone, tracked with KPD &mdash; acknowledging small-sample noise in a pilot. This is the outcome the program exists to move.</p>
<p><strong>Economic.</strong> Average redemption ticket versus the cost of a large coffee (the number that proves Model A); repeat-customer reports; overnight garage stays on program nights.</p>
<p><strong>Qualitative.</strong> Bartender friction reports and short patron surveys via a QR on the card.</p>
</div>
<div class="band">
  <div class="eyebrow">The privacy stance</div>
  <p style="margin:0;color:var(--paper);font-size:10.2pt;">The system stores <strong style="color:var(--paper)">no patron data at all</strong> &mdash; a serial, a shop, and a timestamp, nothing more. There are no accounts, no names, no tracking. Cards are anonymous by design, which is exactly what lets KPD endorse the program without it ever feeling like surveillance. That&rsquo;s worth saying out loud to the City, and it&rsquo;s in the FAQ.</p>
</div>
</div>""")

    out.append(f"""
<div class="section"><a id="s_risks"></a>
{opener("Part IV · Making It Real","18","Risks, and how we’ve handled them","Every obvious objection, met before it&rsquo;s raised.")}
<table>
<thead><tr><th style="width:2.5in">Risk</th><th>Mitigation</th></tr></thead>
<tbody>
<tr><td><strong>Bartenders skip it on busy nights</strong></td><td>A 10-second workflow, staff perks, and coasters that do the marketing passively.</td></tr>
<tr><td><strong>Patron fears a ticket or tow for leaving the car</strong></td><td>Lead with free evening/weekend municipal parking; confirm hours with the City and Parking Authority; print them on signage; program contact on the card.</td></tr>
<tr><td><strong>Perception of promoting drinking</strong></td><td>Framing is strictly the safe ride home and safer roads; City/KPD endorsement; no alcohol-brand sponsors on patron-facing materials. Full answer in the FAQ.</td></tr>
<tr><td><strong>Fraud (fake ride screens, duplicates)</strong></td><td>One-free-coffee cap, one-per-ride rule, serials, expiry, bartender discretion; small leakage accepted as a marketing cost.</td></tr>
<tr><td><strong>Redemption concentrates on a few shops</strong></td><td>Per-shop monthly caps at pilot; recruit shops near every major garage; publish the redemption spread.</td></tr>
<tr><td><strong>Shops lose faith in the coupon math</strong></td><td>Share ticket-uplift data monthly; community/sponsor funds can backstop the coffee if Model A underperforms.</td></tr>
<tr><td><strong>Program conflated with enforcement</strong></td><td>KPD as endorser only; cards anonymous &mdash; no data on individuals is ever collected.</td></tr>
</tbody>
</table>
</div>""")

    # FAQ
    out.append(f"""
<div class="section"><a id="s_faq"></a>
{opener("Part IV · Making It Real","19","Frequently asked questions","Starting with the hard one.")}

<div class="faq">
  <div class="qq">Isn&rsquo;t this rewarding people for a night of irresponsible drinking?</div>
  <div class="aa">It&rsquo;s a fair thing to raise, and the honest answer is a <strong>harm-reduction</strong> one.{ref(9)} People are going to go out and drink downtown whether or not this program exists. Given that, the only question that changes outcomes is: when someone has had too much, how do we make the safe choice the easy one? Pick-Me-Up doesn&rsquo;t subsidize the drinking &mdash; the reward is explicitly tied to <em>not driving</em>, it&rsquo;s claimed the <em>next morning</em>, and it&rsquo;s capped at a coffee. It buys down the single largest friction that pushes people to drive impaired: the parked car. And the evidence base is real. A synthesis of roughly 125 studies found that well-implemented alternative-transportation programs <em>can</em> reduce impaired driving, and identified the design attributes that predict success &mdash; low cost, high awareness, convenience, and rides both to and from venues{ref(5)} &mdash; attributes this program is deliberately built around. We&rsquo;re also honest that the direct evidence for reward programs is <strong>mixed</strong>: the responsible reading, which we adopt, is that a reward like this should be <em>one component of a broader effort</em> &mdash; enforcement, education, transit, responsible service &mdash; and should be evaluated, not sold as a silver bullet.{ref(3)}</div>
</div>

<div class="faq">
  <div class="qq">Doesn&rsquo;t a free ride home just lead people to drink more?</div>
  <div class="aa">That specific risk is documented, and we take it seriously: a subsidized-rideshare study in Columbus found real crash reductions but also a self-reported <em>increase</em> in drinking that partly offset the benefit.{ref(8)} It&rsquo;s exactly why our reward is small, delayed to the next morning, and tied to the safe ride rather than to the bar tab &mdash; a coffee you collect tomorrow at your car is a poor incentive to have one more drink tonight. It&rsquo;s also why we commit to measuring outcomes honestly rather than assuming them.</div>
</div>

<div class="faq">
  <div class="qq">Is this public money buying people coffee?</div>
  <div class="aa">No. The coffee is carried by participating shops as their own customer-acquisition cost, backstopped by sponsors &mdash; not a public payout &mdash; and KAT rides are KAT&rsquo;s in-kind contribution. The program&rsquo;s only real cash need is a modest set of fixed costs (printing, a part-time coordinator, launch). Any public seed is one-time and optional. Against that, alcohol-impaired crashes were estimated to cost <strong>$58&nbsp;billion</strong> in economic costs and <strong>$296&nbsp;billion</strong> in comprehensive societal harm nationally in a single year{ref(1)} &mdash; so even a modest local reduction dwarfs the cost of coffee and bus fare.</div>
</div>

<div class="faq">
  <div class="qq">Why not just tell people not to drink and drive?</div>
  <div class="aa">Because messaging alone has a weak track record. The Community Preventive Services Task Force found <em>insufficient evidence</em> that promoting designated drivers on its own reduces impaired driving,{ref(4)} while it <em>recommends</em> multi-component programs with community mobilization on strong evidence.{ref(3)} A positive incentive delivered at the decision moment is the piece enforcement and slogans miss &mdash; it complements them rather than replacing them.</div>
</div>

<div class="faq">
  <div class="qq">Are you collecting data on people who&rsquo;ve been drinking? Is this surveillance?</div>
  <div class="aa">No, and that&rsquo;s deliberate. The system stores no patron data at all &mdash; only a card serial, a shop, and a timestamp. There are no names, no accounts, no tracking. Cards are anonymous, and KPD is an endorser, not an operator: there is no enforcement role in bars and nothing that resembles a checkpoint. The anonymity is what makes the endorsement possible.</div>
</div>

<div class="faq">
  <div class="qq">What stops someone from gaming it?</div>
  <div class="aa">Layered, proportionate controls: one card per booked ride, a keyed serial that can&rsquo;t be invented, a one-day expiry that kills resale value, per-shop caps, a pack kill-switch, and two-touch validation (dated at the bar, scanned at the shop). And the stakes are low by design &mdash; the worst case of a gamed card is a single free coffee, so we keep the controls light enough that the bar interaction stays ten seconds. Details in Appendix B.</div>
</div>

<div class="faq">
  <div class="qq">Isn&rsquo;t leaving the car downtown a hassle &mdash; or a ticket risk?</div>
  <div class="aa">Downtown&rsquo;s municipal garages and lots are already free after 6&nbsp;p.m. on weeknights and all weekend, so leaving the car overnight is free and allowed. The program partners with the Downtown Parking Authority to make sure those hours are stated accurately and communicated at the decision moment &mdash; and the card carries a program contact for questions.</div>
</div>

<p class="note measure">Every figure and claim above is sourced in <strong>Appendix F &middot; Evidence &amp; references</strong> (page&nbsp;{{P:a_refs}}).</p>
</div>""")
    return "\n".join(out)

def closing():
    return f"""
<div class="closing">
<div class="band deep" style="margin-top:0;padding:0.6in 0.55in;">
  <div class="eyebrow">The invitation</div>
  <h1 style="color:var(--paper);font-size:26pt;letter-spacing:-0.01em;margin-bottom:0.18in;">Let&rsquo;s make the safe<br>choice the easy one.</h1>
  <p class="umber" style="font-size:11.5pt;max-width:5.2in;line-height:1.6;">Knox Pick-Me-Up asks each partner for something small and gives each one something real &mdash; and together it keeps one more impaired driver off Knoxville&rsquo;s roads on the nights that matter most. The loop is designed, the toolkit is built, and the cost to start is a single sponsor conversation.</p>
  <p class="umber" style="font-size:11.5pt;max-width:5.2in;line-height:1.6;">If you&rsquo;re a bar, a coffee shop, the City, KPD, KAT, the Parking Authority, or a sponsor &mdash; there&rsquo;s a page in this book with your name on it. We&rsquo;d love to talk about it.</p>
  <div style="margin-top:0.4in;border-top:1px solid rgba(198,206,220,0.28);padding-top:0.22in;">
    <span class="kicker" style="color:var(--gold)">Get in touch</span>
    <p style="color:var(--paper);font-size:12pt;margin:0.1in 0 0;font-family:var(--serif);">hello@knoxpickmeup.org &nbsp;&middot;&nbsp; knoxpickmeup.org</p>
    <p class="umber" style="font-size:9pt;margin-top:0.06in;">Knoxville, Tennessee</p>
  </div>
</div>
</div>"""

# ---------------- appendices ----------------
def app_open(letter, title, dek):
    return f"""<div class="section">
{opener("Appendix "+letter, letter, title, dek)}"""

def appendices():
    out = []
    # A tech
    out.append(f"""<a id="a_tech"></a>{app_open("A","Technical architecture","A turnkey system with no server to maintain, no on-call, and $0/month.")}
<p class="lead measure">The whole tracking system runs on a static website plus a Google Sheet. Every moving part is either a static file on GitHub Pages or a Google-hosted freebie that keeps running if every volunteer goes on vacation.</p>
<div class="loop" style="margin-bottom:0.2in">
  <div class="lp"><div class="c">1</div><div class="t">Print run<br>makes serialized cards</div></div>
  <div class="lp"><div class="c">2</div><div class="t">Bar<br>pack checked out by QR</div></div>
  <div class="lp"><div class="c">3</div><div class="t">Coffee shop<br>scans card QR</div></div>
  <div class="lp"><div class="c">4</div><div class="t">Google Sheet<br>the database</div></div>
  <div class="lp"><div class="c">5</div><div class="t">Live dashboard<br>on the same site</div></div>
</div>
<h3 class="sub">The one clever trick</h3>
<p class="measure">Every card&rsquo;s QR encodes a plain link to the public site with the serial attached. A <strong>patron</strong> who scans it just lands on the shop map. The <strong>shop&rsquo;s scanner page</strong> doesn&rsquo;t follow the link &mdash; it reads the serial off the camera with a regex. Same printed code, two behaviors, zero extra infrastructure.</p>
<h3 class="sub">The components</h3>
<ul class="clean">
  <li><strong>The database &mdash; one Google Sheet</strong> owned by a program account, with three tabs (<span class="note">Redemptions, Packs, Venues</span>). Nothing else to host.</li>
  <li><strong>The redemption endpoint &mdash; a ~30-line Apps Script web app</strong> bound to the Sheet. It answers &ldquo;was this card already used?&rdquo; at the counter, in real time; Google hosts, runs, and patches it.</li>
  <li><strong>The scanner &mdash; <span class="note">redeem/</span></strong>, a self-contained static page opened from a per-shop QR. Tap-to-scan with the phone camera, a manual-entry fallback, and <strong>offline tolerance</strong>: no signal means the scan queues and auto-flushes when the connection returns.</li>
  <li><strong>Pack check-out &mdash; the scanner&rsquo;s admin mode.</strong> Scan a pack&rsquo;s cover QR, pick the bar &mdash; that&rsquo;s the entire &ldquo;which bar issued this&rdquo; step, and it&rsquo;s insert-only so a double-scan can&rsquo;t reassign a pack.</li>
  <li><strong>The dashboard &mdash; <span class="note">dashboard/</span></strong>, a live, brand-styled page fed from the Sheet: issued/redeemed KPIs, a day&times;hour heatmap, to-shop and from-bar charts, and integrity tiles. Shareable by link &mdash; the City, KPD, or a reporter can watch the numbers live, because the payload is venue names, timestamps, and counts only.</li>
</ul>
<p class="note measure">Attribution needs nobody to type a venue name, ever: the coffee shop is identified by which register QR opened the scanner, and the issuing bar by the serial&rsquo;s pack range. Cost at pilot scale: $0.</p>
</div>""")

    # B serial
    out.append(f"""<a id="a_serial"></a>{app_open("B","The card & anti-forgery serialization","One secret in the whole system &mdash; and serials that can&rsquo;t be minted by counting.")}
<p class="measure">Every card serial looks like <strong>KPMU-2026-00004217T</strong>: a year, an eight-digit number, and one <strong>keyed checksum letter</strong>. That letter is computed from a secret, so nobody can invent a valid serial by counting up from a card in hand &mdash; a made-up serial passes only 1 time in 24, and every failure is logged.</p>
<h3 class="sub">Exactly one secret</h3>
<p class="measure">The whole system has a single secret, <span class="note">PROGRAM_KEY</span>. The checksum uses a key <em>derived</em> from it (a one-way HMAC), and it&rsquo;s the derived key &mdash; not the secret &mdash; that rides in each shop&rsquo;s register QR. That&rsquo;s what lets the scanner verify serials locally and instantly, even offline, while someone who photographs a register QR still can&rsquo;t forge cards, touch backups, or learn the program key.</p>
<h3 class="sub">Packs, and the kill switch</h3>
<ul class="clean">
  <li><strong>Packs of 50</strong> carry their own serial with a leading <span class="note">P</span>, so a pack can never be mistaken for a card. Checking a pack out to a bar ties every serial in it to that venue.</li>
  <li><strong>Kill switch:</strong> to invalidate a lost, stolen, or misprinted pack, type anything in its <span class="note">voided</span> cell. From that moment every card in it fails to scan at every register, and attempts are logged with where they surfaced. Clearing the cell restores it.</li>
  <li><strong>Two-touch:</strong> dated by hand at the bar, scanned at the shop &mdash; duplicates and mismatches flag automatically.</li>
</ul>
<div class="callout"><div class="q">Low stakes by design.</div><div class="note">The worst realistic case of a gamed card is one free coffee, so the controls stay proportionate &mdash; enough to deter, light enough to keep the bar hand-off to ten seconds.</div></div>
</div>""")

    # C privacy
    out.append(f"""<a id="a_privacy"></a>{app_open("C","Data, privacy & backups","No patron data exists to lose &mdash; and four independent backup layers for what does.")}
<h3 class="sub">What&rsquo;s collected &mdash; and what isn&rsquo;t</h3>
<p class="measure">The system stores a card <strong>serial</strong>, a <strong>shop</strong>, and a <strong>timestamp</strong>. There are no names, no accounts, no payment data, no location tracking &mdash; there is no patron identity anywhere in the system to collect, leak, or subpoena. The only card serials that ever leave the Sheet are those of <em>refused</em> scans (already redeemed, voided, or invalid), which grant nothing and power duplicate forensics.</p>
<h3 class="sub">Backups &amp; disaster recovery</h3>
<table>
<thead><tr><th style="width:1.9in">Layer</th><th>Protects against</th></tr></thead>
<tbody>
<tr><td><strong>1 &middot; Sheet version history</strong></td><td>A bad edit or deleted column &mdash; built into Google Sheets, automatic.</td></tr>
<tr><td><strong>2 &middot; Nightly Drive snapshot</strong></td><td>A mangled or deleted tab &mdash; 30 dated copies kept by a daily trigger.</td></tr>
<tr><td><strong>3 &middot; Nightly off-Google backup</strong></td><td>Google account loss &mdash; a GitHub Action commits CSVs of every tab; git history is the archive.</td></tr>
<tr><td><strong>4 &middot; Print artifacts</strong></td><td>Everything digital at once &mdash; pack sheets and cards carry hand-written date/bar lines.</td></tr>
</tbody>
</table>
<p class="note measure">Hardening: the Sheet is shared with no editors &mdash; the Apps Script is the only writer &mdash; and partners get the dashboard link, never the Sheet. Worst-case full restore from the CSVs is under an hour. A failed nightly backup emails the owner; no pager, no service.</p>
</div>""")

    # D print
    out.append(f"""<a id="a_print"></a>{app_open("D","The print kit & production","Everything a print shop needs &mdash; and it&rsquo;s all generated to spec from the toolkit.")}
<p class="measure">The physical kit <em>is</em> the program: the cards are the redeemable item, the packs are the fraud control, the coasters are the advertising. Every generator writes a true-size, print-ready PDF with all type converted to outlines &mdash; hand the files straight to a shop.</p>
<table>
<thead><tr><th style="width:1.9in">Piece</th><th>Notes</th></tr></thead>
<tbody>
<tr><td><strong>Card books</strong></td><td>50 cards per book, a unique QR + serial per card. In printer terms, a raffle-ticket book with variable data &mdash; commoditized and cheap.</td></tr>
<tr><td><strong>Pack cover sheets</strong></td><td>One per book, carrying the pack serial and a check-out QR.</td></tr>
<tr><td><strong>Coasters (two-sided)</strong></td><td>The advertising medium &mdash; they sit under the drink at the decision moment. Bars burn through them anyway, so the program replaces a cost with free branded stock.</td></tr>
<tr><td><strong>Signage</strong></td><td>Table tents, a window decal, and restroom/community posters.</td></tr>
<tr><td><strong>Staff & register</strong></td><td>A laminated barista one-pager and bar-onboarding sheet; one register QR per shop.</td></tr>
</tbody>
</table>
<p class="note measure">Ballpark: short-run card books land around $0.08&ndash;0.20 per card, so a 1,000-card pilot is roughly $100&ndash;250 &mdash; one sponsor conversation, with a natural sponsor in a local print shop credited on the card backs. The key spec: <strong>uncoated stock</strong>, because the bartender writes the date in ballpoint. A GitHub Action builds the whole kit in the browser and hands back a zip of PDFs &mdash; no terminal needed.</p>
</div>""")

    # E finance
    out.append(f"""<a id="a_finance"></a>{app_open("E","Financial detail","The cash budget is fixed costs &mdash; not a per-coffee payout.")}
<h3 class="sub">Illustrative pilot fixed costs &middot; 6 months</h3>
<table>
<thead><tr><th>Item</th><th style="text-align:right;width:1.3in">Estimate</th></tr></thead>
<tbody>
<tr><td>Printing: coasters, cards, signage</td><td class="tnum" style="text-align:right">$4,000</td></tr>
<tr><td>Part-time coordinator (reconciliation, restock, partner care)</td><td class="tnum" style="text-align:right">$9,000</td></tr>
<tr><td>Launch marketing & press event</td><td class="tnum" style="text-align:right">$3,000</td></tr>
<tr><td>Contingency</td><td class="tnum" style="text-align:right">$2,000</td></tr>
<tr><td><strong>Total fixed</strong></td><td class="tnum" style="text-align:right"><strong>~$18,000</strong></td></tr>
</tbody>
</table>
<p class="measure">The coffee itself is carried by participating shops (Model A) and backstopped by sponsorship if a shop needs it; KAT rides are KAT&rsquo;s in-kind contribution. So the program&rsquo;s cash budget is essentially the fixed costs above, not a per-perk payout &mdash; and the marginal cost of one more safe ride home is approximately zero.</p>
<h3 class="sub">Coupon economics (Model A), and why shops say yes</h3>
<p class="measure">The card brings in a late-night crowd shops rarely see in the morning; a large coffee is a small pour against a morning ticket that usually runs higher; and a good first visit creates a regular. Shops can cap monthly redemptions while the model proves out, and the dashboard shows each shop its own average-ticket uplift so the value is visible, not assumed.</p>
<p class="note measure">Sponsorship tiers cover the fixed costs above; logos ride on coasters and cards already in every bar downtown &mdash; unusually good placement per dollar.</p>
</div>""")

    # F references
    refs = [
      ("The Economic and Societal Impact of Motor Vehicle Crashes, 2019", "NHTSA, Report DOT HS 813 403 (2022). Alcohol-impaired crashes: ~$58B economic and ~$296B comprehensive societal cost in 2019.", "crashstats.nhtsa.dot.gov/Api/Public/ViewPublication/813403.pdf"),
      ("Impaired Driving Facts", "U.S. Centers for Disease Control and Prevention. Ongoing toll and cost figures for alcohol-impaired driving.", "cdc.gov/impaired-driving/facts/index.html"),
      ("Alcohol-Impaired Driving: Multicomponent Interventions with Community Mobilization", "The Community Guide / Community Preventive Services Task Force &mdash; recommends, strong evidence. Why a reward should sit inside a multi-part strategy.", "thecommunityguide.org (motor-vehicle-injury / alcohol-impaired driving)"),
      ("Effectiveness of designated driver programs for reducing alcohol-impaired driving: a systematic review", "Ditter et al., American Journal of Preventive Medicine (2005). CPSTF found insufficient evidence that DD promotion alone works.", "pubmed.ncbi.nlm.nih.gov/15894161/"),
      ("The effectiveness of alternative transportation programs in reducing impaired driving: a literature review and synthesis", "Journal of Safety Research (2020). Reviews ~125 studies; identifies the design attributes that predict success.", "pubmed.ncbi.nlm.nih.gov/33334469/"),
      ("Safe Ride Programs: Alternatives to Impaired Driving", "Traffic Injury Research Foundation (TIRF) literature review. Practitioner-oriented synthesis.", "tirf.ca/projects/safe-ride-programs-alternatives-impaired-driving/"),
      ("Countermeasures That Work &mdash; Alternative Transportation", "NHTSA. The standard U.S. reference rating what&rsquo;s proven vs. promising.", "nhtsa.gov/book/countermeasures-that-work"),
      ("Efficacy and cost-effectiveness of subsidized ridesharing as a drunk-driving intervention", "Accident Analysis & Prevention (2020), Columbus, OH. Crash reductions, but modest/expensive savings and a self-reported increase in drinking &mdash; the direct caution behind a small, safe-ride-tied perk.", "pubmed.ncbi.nlm.nih.gov/32866769/"),
      ("Harm Reduction as an Alcohol-Prevention Strategy", "Alcohol Research: Current Reviews (NIAAA), 2018.", "ncbi.nlm.nih.gov/pmc/articles/PMC6876518/"),
      ("What Is Harm Reduction?", "Johns Hopkins Bloomberg School of Public Health (2022). Plain-language primer on the philosophy.", "publichealth.jhu.edu/2022/what-is-harm-reduction"),
      ("Harm reduction approaches to alcohol use: health promotion, prevention, and treatment", "Addictive Behaviors (2002). Foundational framing of pragmatic, non-abstinence approaches.", "sciencedirect.com/science/article/abs/pii/S0306460302002940"),
      ("Nudge: Improving Decisions About Health, Wealth, and Happiness", "Thaler & Sunstein (2008). The case for removing friction and rewarding the desired choice at the exact moment it&rsquo;s made.", ""),
      ("Local data", "Knoxville Regional Transportation Planning Organization (annual injuries and fatalities in area impaired-driving crashes); Knox County Health Department (share of deadly crashes involving an impaired driver).", ""),
    ]
    ritems = []
    for i,(t,d,u) in enumerate(refs, start=1):
        uline = f'<div class="u">{u}</div>' if u else ''
        ritems.append(f'<div class="r"><div class="rn">{i}</div><div class="rb"><strong>{t}.</strong> {d}{uline}</div></div>')
    out.append(f"""<a id="a_refs"></a>{app_open("F","Evidence & references","The sources behind every figure and claim &mdash; the supportive and the skeptical.")}
<p class="note measure">The evidence for reward programs is genuinely mixed, and we cite it that way: the supportive syntheses, the skeptical cost-effectiveness work, and the behavioral-design and harm-reduction foundations, alongside the local Knoxville figures.</p>
<div class="refs">
{''.join(ritems)}
</div>
</div>""")

    # G brand
    out.append(f"""<a id="a_brand"></a>{app_open("G","Brand at a glance","Warm paper, espresso ink, night navy, and one confident stroke of Tennessee orange.")}
<div class="cardmock" style="align-items:center">
  <div style="flex:0 0 1.3in;"><div style="width:1.3in">{MARK_PAPER}</div></div>
  <div class="caption"><b>The mark.</b> A rounded badge cradling a steaming coffee cup &mdash; the morning after the safe ride home, sealed in one glyph. Kept to a two-color navy/paper pair; never outlined, tilted, or effected.</div>
</div>
<h3 class="sub">Palette</h3>
<table>
<thead><tr><th>Color</th><th>Hex</th><th>Role</th></tr></thead>
<tbody>
<tr><td><strong>Paper</strong></td><td class="note">#FAF5EB</td><td>Primary light background; text on dark</td></tr>
<tr><td><strong>Ink</strong></td><td class="note">#241A10</td><td>Display type, body headings</td></tr>
<tr><td><strong>Night</strong></td><td class="note">#101A30</td><td>Primary dark band</td></tr>
<tr><td><strong>Sunrise</strong></td><td class="note">#FF8200</td><td>The accent &mdash; used sparingly: figures, the mark, one rule</td></tr>
<tr><td><strong>Gold</strong></td><td class="note">#EDA953</td><td>Accent text on dark backgrounds</td></tr>
</tbody>
</table>
<h3 class="sub">Type &amp; voice</h3>
<p class="measure"><strong>Fraunces</strong> (serif) for display, <strong>Inter</strong> (sans) for text, <strong>Cormorant</strong> with old-style figures for statistics &mdash; all free and self-hosted. The voice is warm, wry, and never preachy: never &ldquo;don&rsquo;t drink and drive,&rdquo; always &ldquo;good call &mdash; coffee&rsquo;s on us.&rdquo; One accent color, used rarely, so that when orange appears it means something.</p>
</div>""")

    # H fork
    out.append(f"""<a id="a_fork"></a>{app_open("H","Forking this for your community","Knox Pick-Me-Up is an open playbook &mdash; here&rsquo;s how another city stands up its own.")}
<p class="lead measure">Nothing about this is Knoxville-specific except the name and the partners. The whole thing &mdash; the site, the scanner, the dashboard, the print generators, and this document &mdash; is a toolkit another community can adapt in an afternoon of setup and a few weeks of partner conversations.</p>
<div class="steps">
  <div class="step"><div class="sn">1</div><div class="sb"><b>Rebrand</b><span>Swap the name, mark, tagline, and the one accent color for your city&rsquo;s. The identity is parametric &mdash; the generators regenerate every asset from one mark source.</span></div></div>
  <div class="step"><div class="sn">2</div><div class="sb"><b>Swap the partners</b><span>Replace the venue rosters and your transit agency&rsquo;s equivalent of &ldquo;Hair of the KAT.&rdquo; Confirm your downtown&rsquo;s free-parking hours with your parking authority.</span></div></div>
  <div class="step"><div class="sn">3</div><div class="sb"><b>Stand up the backend</b><span>Create a program Google account and Sheet, paste the ~30-line Apps Script, set your one secret, and deploy. One afternoon, following the setup runbook.</span></div></div>
  <div class="step"><div class="sn">4</div><div class="sb"><b>Print &amp; run a pilot</b><span>Generate the card books and coasters to spec, recruit a handful of anchor bars and shops, launch on a high-risk weekend, and evaluate honestly.</span></div></div>
</div>
<h3 class="sub">Localize the evidence</h3>
<p class="measure">Replace the local figures (page&nbsp;{{P:s_problem}}) with your region&rsquo;s impaired-driving injury and fatality numbers from your transportation planning organization and health department. The national and peer-reviewed sources in Appendix F travel unchanged &mdash; and so does the honest framing: run the reward as one component of a broader effort, and publish what you find.</p>
<div class="callout"><div class="q">The design constraint that must survive any fork:</div><div class="note">the perk is always free to the patron who took the safe ride, it&rsquo;s claimed the next morning at the car, and it&rsquo;s capped small. Keep those three, and the harm-reduction logic &mdash; and the fraud math &mdash; still hold.</div></div>
</div>""")
    return "\n".join(out)

def back():
    return f"""
<div class="back"><div class="c">
  <div class="mark">{MARK_DARK}</div>
  <div class="wm">Knox Pick-Me-Up</div>
  <div class="tag">Ride from last call to first cup.</div>
  <div class="ct">hello@knoxpickmeup.org<br>knoxpickmeup.org<br>Knoxville, Tennessee</div>
</div></div>"""

# ---------------------------------------------------------------- assemble
def build():
    body = "".join([
        cover(), toc(), execsummary(),
        part1(), part2(), part3(), part4(),
        closing(),
        appendices(),
        back(),
    ])
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Knox Pick-Me-Up — Program Details</title>
<style>{CSS}</style></head><body>{body}</body></html>"""
    out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "design" / "program-details.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print("wrote", out, len(html), "bytes")
    return out

if __name__ == "__main__":
    build()
