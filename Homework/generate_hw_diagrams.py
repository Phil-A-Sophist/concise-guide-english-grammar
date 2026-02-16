"""
Generate diagram PNGs for the SyntaxTreeHybrid Practice Assignment and Answer Key.
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

PORT = 8081
SYNTAX_TREE_DIR = Path(r"C:\Users\irphy\Documents\SyntaxTreeHybrid")
OUTPUT_DIR = Path(r"C:\Users\irphy\Documents\concise-guide-english-grammar\Homework\diagrams")
EXPORT_MULTIPLIER = 5

# All diagrams needed for the homework assignment and answer key
DIAGRAMS = {
    # Instructions example
    "example_dogs_bark": "[S [NP [N Dogs]] [VP [V bark]]]",

    # Exercise 1-4 sample sentences (New Orleans themed)
    "ex1_musicians_play": "[S [NP [N Musicians]] [VP [V play]]]",
    "ex2_streetcars_move": "[S [NP [DET The] [N streetcars]] [VP [V move] [ADVP [ADV slowly]]]]",
    "ex3_gumbo_simmers": "[S [NP [ADJP [ADJ Delicious]] [N gumbo]] [VP [V simmers] [PP [PREP in] [NP [N kitchens]]]]]",
    "ex4_crowds_dance": "[S [NP [ADJP [ADVP [ADV Incredibly]] [ADJ lively]] [N crowds]] [VP [V dance] [ADVP [ADVP [ADV quite]] [ADV energetically]]]]",

    # Exercise 5 answer key
    "ex5a_scientists": "[S [NP [DET Some] [ADJP [ADVP [ADV very]] [ADJ smart]] [N scientists]] [VP [V fail] [ADVP [ADVP [ADV quite]] [ADV frequently]]]]",
    "ex5b_fool": "[S [NP [DET The] [N fool] [PP [PREP on] [NP [DET the] [N hill]]]] [VP [V speaks] [ADVP [ADVP [ADV so]] [ADV eloquently]]]]",
    "ex5c_products": "[S [NP [ADJP [ADJ Terrible]] [N products]] [VP [ADVP [ADV often]] [V linger] [PP [PREP on] [NP [DET the] [N shelf]]]]]",
    "ex5d_teenagers": "[S [NP [ADJP [ADVP [ADV Extremely]] [ADJ nervous]] [N teenagers]] [VP [V sweat] [ADVP [ADV profusely]] [PP [PREP on] [NP [DET many] [ADJP [ADJ first]] [N dates]]]]]",
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
    log("Generating Homework Diagrams")
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
