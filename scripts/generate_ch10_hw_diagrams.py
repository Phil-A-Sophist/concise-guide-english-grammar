"""
Generate diagram PNGs for the Chapter 10 Homework Answer Key.
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

PORT = 8083
SYNTAX_TREE_DIR = Path(r"C:\Users\irphy\Documents\SyntaxTreeHybrid")
OUTPUT_DIR = Path(r"C:\Users\irphy\Documents\concise-guide-english-grammar\Homework\diagrams\ch10")
EXPORT_MULTIPLIER = 5

DIAGRAMS = {
    # Exercise 16: "The students are studying for the exam." (present progressive)
    "ch10_hw_ex16_students_studying":
        "[S [NP [DET The] [N students]] [VP [AUX are] [V studying] [PP [PREP for] [NP [DET the] [N exam]]]]]",

    # Exercise 17: "He had finished the assignment before class." (past perfect)
    "ch10_hw_ex17_had_finished":
        "[S [NP [PRON He]] [VP [AUX had] [V finished] [NP [DET the] [N assignment]] [PP [PREP before] [NP [N class]]]]]",

    # Exercise 18: "Does the professor teach on Fridays?" (do-support question)
    "ch10_hw_ex18_does_teach":
        "[S [AUX Does] [NP [DET the] [N professor]] [VP [V teach] [PP [PREP on] [NP [N Fridays]]]]]",

    # Exercise 19: "The report was written by the committee." (passive)
    "ch10_hw_ex19_was_written":
        "[S [NP [DET The] [N report]] [VP [AUX was] [V written] [PP [PREP by] [NP [DET the] [N committee]]]]]",

    # Exercise 20: "They have been waiting at the station for an hour." (perfect progressive)
    "ch10_hw_ex20_have_been_waiting":
        "[S [NP [PRON They]] [VP [AUX have] [AUX been] [V waiting] [PP [PREP at] [NP [DET the] [N station]]] [PP [PREP for] [NP [DET an] [N hour]]]]]",
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
    log("Generating Chapter 10 Homework Diagrams")
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
