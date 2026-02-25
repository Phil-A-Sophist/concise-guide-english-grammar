"""
Generate SyntaxTreeHybrid PNG diagrams for Rhet Gram Ch 1 answer key.
Uses Playwright to drive the local SyntaxTreeHybrid app.

Run this BEFORE generate_rhet_gram_ch1_answer_key.py.
Output: Homework/diagrams/ch01_rg/*.png
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

PORT       = 8082
SYNTAX_TREE_DIR = Path(r"C:\Users\irphy\Documents\SyntaxTreeHybrid")
OUTPUT_DIR = Path(r"C:\Users\irphy\Documents\concise-guide-english-grammar\Homework\diagrams\ch01_rg")
EXPORT_MULTIPLIER = 5

DIAGRAMS = {
    # Exercise 3.2: "Cupcakes are a popular alternative to birthday cakes."
    "ch01_rg_ex32_cupcakes":
        "[S [NP [N Cupcakes]] [VP [V are] [NP [DET a] [ADJP [ADJ popular]] [N alternative] [PP [PREP to] [NP [N birthday] [N cakes]]]]]]",

    # Practice One: "Bears seldomly attack without a very good reason."
    "ch01_rg_p1_bears":
        "[S [NP [N Bears]] [VP [ADV seldomly] [V attack] [PP [PREP without] [NP [DET a] [ADJP [ADV very] [ADJ good]] [N reason]]]]]",

    # Practice Two: "Stephen usually sits alone at home."
    "ch01_rg_p2_stephen":
        "[S [NP [N Stephen]] [VP [ADV usually] [V sits] [ADV alone] [PP [PREP at] [NP [N home]]]]]",

    # Practice Three: "My younger brother works for the city."
    "ch01_rg_p3_brother":
        "[S [NP [DET My] [ADJP [ADJ younger]] [N brother]] [VP [V works] [PP [PREP for] [NP [DET the] [N city]]]]]",

    # Practice Four: "The painfully long discussion continued incessantly until noon."
    "ch01_rg_p4_discussion":
        "[S [NP [DET The] [ADJP [ADV painfully] [ADJ long]] [N discussion]] [VP [V continued] [ADV incessantly] [PP [PREP until] [NP [N noon]]]]]",

    # Example Five: "All my dearest friends from highschool suddenly left."
    "ch01_rg_p5_friends":
        "[S [NP [DET All] [DET my] [ADJP [ADJ dearest]] [N friends] [PP [PREP from] [NP [N highschool]]]] [VP [ADV suddenly] [V left]]]",
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
    log("Generating Rhet Gram Ch 1 Diagrams via SyntaxTreeHybrid")
    log("=" * 60)
    log(f"Diagrams: {len(DIAGRAMS)}")
    log(f"Output:   {OUTPUT_DIR}")

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

    passed = sum(1 for _, ok in results if ok)
    log(f"\nDone: {passed}/{len(results)} succeeded")
    if passed == len(results):
        log("All diagrams generated. Run generate_rhet_gram_ch1_answer_key.py next.")


if __name__ == "__main__":
    main()
