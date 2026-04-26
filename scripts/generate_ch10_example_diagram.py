"""
Generate the example diagram PNG for Chapter 10 Homework Part 4.
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

PORT = 8084
SYNTAX_TREE_DIR = Path(r"C:\Users\irphy\Documents\SyntaxTreeHybrid")
OUTPUT_DIR = Path(r"C:\Users\irphy\Documents\concise-guide-english-grammar\assets\diagrams\new")
EXPORT_MULTIPLIER = 5

DIAGRAMS = {
    "ch10_hw_example":
        "[S [NP [PRON She]] [VP [AUX has] [AUX been] [V reading] [NP [DET the] [N book]]]]",
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

    log("Generating Ch10 homework example diagram...")

    server = threading.Thread(target=start_server, daemon=True)
    server.start()
    time.sleep(1)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1400, "height": 900})

        for name, bracket in DIAGRAMS.items():
            log(f"  {name}: {bracket}")
            page.goto(f"http://localhost:{PORT}/index.html")
            page.wait_for_selector("#diagram-canvas", state="visible")
            time.sleep(0.5)

            bracket_input = page.locator("#bracket-input")
            bracket_input.click()
            bracket_input.fill(bracket)
            time.sleep(1.0)

            status = page.locator("#bracket-status").inner_text()
            if "error" not in status.lower():
                data_url = page.evaluate(f"""
                    async () => {{
                        await new Promise(r => setTimeout(r, 200));
                        return await window.canvasManager.exportPNG({EXPORT_MULTIPLIER});
                    }}
                """)
                output_path = OUTPUT_DIR / f"{name}.png"
                save_data_url_as_png(data_url, output_path)
                log(f"  Saved: {output_path}")
            else:
                log(f"  FAILED: {status}")

        browser.close()

    log("Done.")


if __name__ == "__main__":
    main()
