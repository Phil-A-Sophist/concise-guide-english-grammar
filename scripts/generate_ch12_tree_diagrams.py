"""
Generate tree diagram PNGs for Ch12 Adverbials content sections.
Uses SyntaxTreeHybrid's native exportPNG() via Playwright.
"""

import os
import sys
import time
import base64
import threading
import http.server
import socketserver
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("ERROR: Playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)

sys.stdout.reconfigure(line_buffering=True)

PORT = 8082
SYNTAX_TREE_DIR = Path(r"C:\Users\irphy\Documents\SyntaxTreeHybrid")
OUTPUT_DIR = Path(r"C:\Users\irphy\Documents\concise-guide-english-grammar\assets\diagrams\new")
EXPORT_MULTIPLIER = 5

DIAGRAMS = {
    # 12.5 NP Adverbials: Last week the students met
    "ch12_126_last_week_met": "[S [NP [ADJP [ADJ Last]] [N week]] [NP [DET the] [N students]] [VP [V met]]]",

    # 12.6 Infinitive: He studied hard to pass the exam
    "ch12_127_studied_to_pass": "[S [NP [PRON He]] [VP [V studied] [ADVP [ADV hard]] [VP [V to] [V pass] [NP [DET the] [N exam]]]]]",

    # 12.6 Infinitive+Adj: She was happy to help
    "ch12_127_happy_to_help": "[S [NP [PRON She]] [VP [V was] [ADJP [ADJ happy] [VP [V to] [V help]]]]]",

    # 12.7 Present participle: Knowing the answer she raised her hand
    "ch12_128_knowing_answer": "[S [VP [V Knowing] [NP [DET the] [N answer]]] [NP [PRON she]] [VP [V raised] [NP [DET her] [N hand]]]]",

    # 12.7 Past participle: Exhausted from the journey he collapsed
    "ch12_128_exhausted_collapsed": "[S [VP [V Exhausted] [PP [PREP from] [NP [DET the] [N journey]]]] [NP [PRON he]] [VP [V collapsed]]]",

    # 12.8 Adverbial clause: When she arrived we started working
    "ch12_129_when_arrived": "[S [DC [SUB When] [NP [PRON she]] [VP [V arrived]]] [IC [NP [PRON we]] [VP [V started] [VP [V working]]]]]",
}


def log(msg):
    print(msg, flush=True)


def start_server():
    os.chdir(str(SYNTAX_TREE_DIR))
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *args: None
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        httpd.serve_forever()


def save_data_url_as_png(data_url, filepath):
    header, encoded = data_url.split(',', 1)
    data = base64.b64decode(encoded)
    with open(filepath, 'wb') as f:
        f.write(data)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    log("=" * 60)
    log("Generating Ch12 Content Tree Diagrams")
    log("=" * 60)
    log(f"Diagrams: {len(DIAGRAMS)}")
    log(f"Output: {OUTPUT_DIR}")

    log("Starting HTTP server...")
    server = threading.Thread(target=start_server, daemon=True)
    server.start()
    time.sleep(1)

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1400, "height": 900})

        for i, (name, bracket) in enumerate(DIAGRAMS.items()):
            log(f"\n[{i+1}/{len(DIAGRAMS)}] {name}")
            log(f"  {bracket}")

            page.goto(f"http://localhost:{PORT}/index.html")
            page.wait_for_selector("#diagram-canvas", state="visible")
            time.sleep(0.5)

            bracket_input = page.locator("#bracket-input")
            bracket_input.click()
            bracket_input.fill(bracket)
            time.sleep(1.0)

            status = page.locator("#bracket-status").inner_text()
            success = "error" not in status.lower()

            if not success:
                bracket_input.fill("")
                time.sleep(0.3)
                bracket_input.fill(bracket)
                time.sleep(1.0)
                status = page.locator("#bracket-status").inner_text()
                success = "error" not in status.lower()

            if success:
                try:
                    data_url = page.evaluate(f"""
                        async () => {{
                            await new Promise(r => setTimeout(r, 200));
                            return await window.canvasManager.exportPNG({EXPORT_MULTIPLIER});
                        }}
                    """)
                    output_path = OUTPUT_DIR / f"{name}.png"
                    save_data_url_as_png(data_url, output_path)
                    log(f"  Saved: {name}.png")
                    results.append((name, True))
                except Exception as e:
                    log(f"  Export error: {e}")
                    results.append((name, False))
            else:
                log(f"  FAILED: {status}")
                results.append((name, False))

            time.sleep(0.3)

        browser.close()

    log("\n" + "=" * 60)
    log("RESULTS")
    log("=" * 60)
    for name, ok in results:
        log(f"  {'OK' if ok else 'FAIL'}: {name}")

    ok_count = sum(1 for _, ok in results if ok)
    log(f"\n{ok_count}/{len(results)} diagrams generated")


if __name__ == '__main__':
    main()
