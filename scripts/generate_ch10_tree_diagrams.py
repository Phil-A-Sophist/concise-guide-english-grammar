"""
Generate tree diagram PNGs for Ch10 Section 10.11 (Diagramming Verb Phrases).
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
    # Simple: "She walks."
    "ch10_tree_simple": "[S [NP [PRON She]] [VP [V walks]]]",

    # Progressive: "She is walking."
    "ch10_tree_progressive": "[S [NP [PRON She]] [VP [AUX is] [V walking]]]",

    # Perfect: "She has walked."
    "ch10_tree_perfect": "[S [NP [PRON She]] [VP [AUX has] [V walked]]]",

    # Perfect progressive: "She has been walking."
    "ch10_tree_perf_prog": "[S [NP [PRON She]] [VP [AUX has] [AUX been] [V walking]]]",

    # Full progressive: "The children are playing a game in the backyard."
    "ch10_tree_full_prog": "[S [NP [DET The] [N children]] [VP [AUX are] [V playing] [NP [DET a] [N game]] [PP [PREP in] [NP [DET the] [N backyard]]]]]",

    # Full perfect: "The professor has assigned three chapters for next week."
    "ch10_tree_full_perfect": "[S [NP [DET The] [N professor]] [VP [AUX has] [V assigned] [NP [ADJ three] [N chapters]] [PP [PREP for] [NP [ADJ next] [N week]]]]]",

    # Full perfect progressive: "The students had been studying grammar in the library all afternoon."
    "ch10_tree_full_perf_prog": "[S [NP [DET The] [N students]] [VP [AUX had] [AUX been] [V studying] [NP [N grammar]] [PP [PREP in] [NP [DET the] [N library]]] [NP [DET all] [N afternoon]]]]",

    # Do-support question: "Does she walk?"
    "ch10_tree_do_question": "[S [AUX Does] [NP [PRON she]] [VP [V walk]]]",

    # Do-support negation: "She does not walk."
    "ch10_tree_do_negation": "[S [NP [PRON She]] [VP [AUX does] [ADV not] [V walk]]]",
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
    log("Generating Ch10 Section 10.11 Tree Diagrams")
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

    passed = sum(1 for _, ok in results if ok)
    log(f"\nDone: {passed}/{len(results)} succeeded")


if __name__ == "__main__":
    main()
