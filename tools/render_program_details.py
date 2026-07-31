# -*- coding: utf-8 -*-
"""Render design/program-details.html to a print-ready PDF with real page
numbers in the table of contents.

    python3 tools/render_program_details.py [out.pdf]

Two passes: render once, find the page each section landed on (searching the
PDF text for a unique phrase per section), rewrite the TOC placeholders with
those page numbers, then render the final PDF. Page numbering and the running
footer come from native CSS @page counters; the cover and back cover are
full-bleed with no footer.

Requirements: a Chromium/Chrome binary, plus `websocket-client` and `pymupdf`
(pip install websocket-client pymupdf). The build step itself has no
dependencies. Chrome is located via $CHROME, then $PLAYWRIGHT_BROWSERS_PATH,
then common system paths.
"""
import base64, glob, json, os, re, socket, subprocess, sys, time, urllib.request
import pathlib

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
HTML = ROOT / "design" / "program-details.html"
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "design" / "Knox-Pick-Me-Up-Program-Details.pdf"
PASS1 = ROOT / "design" / ".program-details-pass1.pdf"

# unique ASCII phrase found only on each section's page (its opener subtitle,
# or a distinctive line) — used to resolve TOC page numbers after pass 1.
SNIP = {
    "execsummary": "reads only this page",
    "s_problem": "moment of decision at last call",
    "s_insight": "Reward the safe choice when it",
    "s_idea": "One loop that closes itself",
    "s_journey": "the patron was going to take anyway",
    "s_card": "a free ride to come get it",
    "s_trust": "the worst case is one free coffee",
    "s_parking": "has to feel free and safe",
    "s_bars": "date-and-hand at last call",
    "s_shops": "and you control the exposure",
    "s_city": "a carrot to pair with the stick",
    "s_kat": "an accepted ride, and a free-ride partner",
    "s_park": "the people who most need to hear it",
    "s_sponsors": "Your name on the safe ride home",
    "s_ask": "sized to the partner",
    "s_fund": "who carries it",
    "s_pilot": "then evaluate honestly and scale",
    "s_metrics": "a privacy stance we can state out loud",
    "s_risks": "Every obvious objection, met before it",
    "s_faq": "Starting with the hard one",
    "s_invite": "a page in this book with your name on it",
    "a_tech": "no server to maintain",
    "a_serial": "One secret in the whole system",
    "a_privacy": "four independent backup layers",
    "a_print": "generated to spec from the toolkit",
    "a_finance": "not a per-coffee payout",
    "a_refs": "the supportive and the skeptical",
    "a_brand": "one confident stroke of Tennessee orange",
    "a_fork": "another city stands up its own",
}


def find_chrome():
    if os.environ.get("CHROME") and pathlib.Path(os.environ["CHROME"]).exists():
        return os.environ["CHROME"]
    pw = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
    for pat in (f"{pw}/chromium-*/chrome-linux/chrome", f"{pw}/chromium-*/chrome-linux/headless_shell"):
        hits = sorted(glob.glob(pat))
        if hits:
            return hits[-1]
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        from shutil import which
        p = which(name)
        if p:
            return p
    raise SystemExit("No Chrome/Chromium found. Set $CHROME to the binary path.")


def render(src_html_path, dst_pdf_path):
    import websocket  # websocket-client

    chrome = find_chrome()
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    proc = subprocess.Popen(
        [chrome, "--headless=new", f"--remote-debugging-port={port}", "--remote-allow-origins=*",
         "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
         "--no-default-browser-check", f"--user-data-dir=/tmp/kpmu-pdf-{port}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        ws_url = None
        for _ in range(120):
            try:
                ws_url = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version"))["webSocketDebuggerUrl"]
                break
            except Exception:
                time.sleep(0.1)
        if not ws_url:
            raise RuntimeError("DevTools did not come up")
        ws = websocket.create_connection(ws_url, max_size=None)
        counter = {"i": 0}

        def send(method, params=None, sess=None):
            counter["i"] += 1; mid = counter["i"]
            msg = {"id": mid, "method": method, "params": params or {}}
            if sess:
                msg["sessionId"] = sess
            ws.send(json.dumps(msg))
            while True:
                r = json.loads(ws.recv())
                if r.get("id") == mid and r.get("sessionId") == sess:
                    if "error" in r:
                        raise RuntimeError(r["error"])
                    return r.get("result", {})

        tid = send("Target.createTarget", {"url": "about:blank"})["targetId"]
        sess = send("Target.attachToTarget", {"targetId": tid, "flatten": True})["sessionId"]
        send("Page.enable", sess=sess)
        frame = send("Page.getFrameTree", sess=sess)["frameTree"]["frame"]["id"]
        send("Page.setDocumentContent", {"frameId": frame, "html": pathlib.Path(src_html_path).read_text()}, sess=sess)
        time.sleep(2.0)  # let embedded fonts and layout settle
        res = send("Page.printToPDF", {
            "printBackground": True, "paperWidth": 8.5, "paperHeight": 11,
            "preferCSSPageSize": True,  # native @page size + margins + footer counters
        }, sess=sess)
        pathlib.Path(dst_pdf_path).write_bytes(base64.b64decode(res["data"]))
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()


def main():
    import fitz  # pymupdf

    # 1. build the HTML (with {P:key} placeholders)
    subprocess.run([sys.executable, str(HERE / "build_program_details.py"), str(HTML)], check=True)

    # 2. pass 1
    render(HTML, PASS1)

    # 3. locate each section's page (skip cover=0 and TOC=1)
    doc = fitz.open(PASS1)
    pages = {}
    for key, snip in SNIP.items():
        pg = None
        for i in range(2, doc.page_count):
            if doc[i].search_for(snip):
                pg = i + 1
                break
        pages[key] = pg
    missing = [k for k, v in pages.items() if v is None]
    print(f"located {len(SNIP) - len(missing)}/{len(SNIP)} sections; {doc.page_count} pages")
    if missing:
        print("WARNING missing:", missing)

    # 4. fill the TOC placeholders (and any in-body cross references)
    html = HTML.read_text()
    html = re.sub(r"\{P:([a-z_]+)\}", lambda m: str(pages.get(m.group(1)) or "—"), html)
    HTML.write_text(html)

    # 5. final pass
    render(HTML, OUT)
    try:
        PASS1.unlink()
    except OSError:
        pass
    print("wrote", OUT, OUT.stat().st_size, "bytes,", fitz.open(OUT).page_count, "pages")


if __name__ == "__main__":
    main()
