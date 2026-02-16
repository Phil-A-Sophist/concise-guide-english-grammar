"""
Generate diagram PNGs for the Exam One Study Guide Answer Key.
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
OUTPUT_DIR = Path(r"C:\Users\irphy\Documents\concise-guide-english-grammar\Homework\Exams\diagrams")
EXPORT_MULTIPLIER = 5

# Study guide diagrams (reuse the example from the exam + 5 new sentences)
DIAGRAMS = {
    # Q14: "The dog barked."
    "sg_q14_dog_barked": "[S [NP [DET The] [N dog]] [VP [V barked]]]",

    # Q15: "The happy children played quietly in the park."
    "sg_q15_children_played": "[S [NP [DET The] [ADJP [ADJ happy]] [N children]] [VP [V played] [ADVP [ADV quietly]] [PP [PREP in] [NP [DET the] [N park]]]]]",

    # Q16: "The teacher from Texas arrived early."
    "sg_q16_teacher_arrived": "[S [NP [DET The] [N teacher] [PP [PREP from] [NP [N Texas]]]] [VP [V arrived] [ADVP [ADV early]]]]",

    # Q17: "Many talented musicians performed brilliantly during the annual festival."
    "sg_q17_musicians_performed": "[S [NP [DET Many] [ADJP [ADJ talented]] [N musicians]] [VP [V performed] [ADVP [ADV brilliantly]] [PP [PREP during] [NP [DET the] [ADJP [ADJ annual]] [N festival]]]]]",

    # Q18: "The young artist with curly hair painted quite skillfully."
    "sg_q18_artist_painted": "[S [NP [DET The] [ADJP [ADJ young]] [N artist] [PP [PREP with] [NP [ADJP [ADJ curly]] [N hair]]]] [VP [V painted] [ADVP [ADVP [ADV quite]] [ADV skillfully]]]]",
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
    log("Generating Exam One Study Guide Diagrams")
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
