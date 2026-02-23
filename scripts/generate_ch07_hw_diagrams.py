"""
Generate diagram PNGs for the Chapter 7 Homework Answer Key.
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
OUTPUT_DIR = Path(r"C:\Users\irphy\Documents\concise-guide-english-grammar\Homework\diagrams\ch07")
EXPORT_MULTIPLIER = 5

DIAGRAMS = {
    # Exercise 10: "The dog barked loudly."
    "ch07_hw_ex10_dog_barked":
        "[S [NP [DET The] [N dog]] [VP [V barked] [ADVP [ADV loudly]]]]",

    # Exercise 11: "The talented student from Ohio won the award."
    "ch07_hw_ex11_student_won":
        "[S [NP [DET The] [ADJP [ADJ talented]] [N student] [PP [PREP from] [NP [N Ohio]]]] [VP [V won] [NP [DET the] [N award]]]]",

    # Exercise 12: "She carefully read the interesting book."
    "ch07_hw_ex12_she_read":
        "[S [NP [PRON She]] [VP [ADVP [ADV carefully]] [V read] [NP [DET the] [ADJP [ADJ interesting]] [N book]]]]",

    # Exercise 13 — Meaning 1 (VP attachment): "I shot an elephant in my pajamas."
    "ch07_hw_ex13_elephant_vp":
        "[S [NP [PRON I]] [VP [V shot] [NP [DET an] [N elephant]] [PP [PREP in] [NP [DET my] [N pajamas]]]]]",

    # Exercise 13 — Meaning 2 (NP attachment): "I shot an elephant in my pajamas."
    "ch07_hw_ex13_elephant_np":
        "[S [NP [PRON I]] [VP [V shot] [NP [DET an] [N elephant] [PP [PREP in] [NP [DET my] [N pajamas]]]]]]",

    # Exercise 14 — Garden-path (incorrect) reading: "The horse raced past the barn fell."
    "ch07_hw_ex14_garden_path":
        "[S [NP [DET The] [N horse]] [VP [V raced] [PP [PREP past] [NP [DET the] [N barn]]]]]",

    # Exercise 14 — Correct reading: "The horse raced past the barn fell."
    "ch07_hw_ex14_correct":
        "[S [NP [DET The] [N horse] [VP [V raced] [PP [PREP past] [NP [DET the] [N barn]]]]] [VP [V fell]]]",
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
    log("Generating Chapter 7 Homework Answer Key Diagrams")
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
