"""
Generate diagram PNGs for the Exam One Answer Key.
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

# Example diagram + all 5 exam answer key diagrams
DIAGRAMS = {
    # Worked example: "The old man sat quietly."
    "example_old_man_sat": "[S [NP [DET The] [ADJP [ADJ old]] [N man]] [VP [V sat] [ADVP [ADV quietly]]]]",

    # Q26: "The cat slept."
    "q26_cat_slept": "[S [NP [DET The] [N cat]] [VP [V slept]]]",

    # Q27: "The cheerful birds sang beautifully in the garden."
    "q27_birds_sang": "[S [NP [DET The] [ADJP [ADJ cheerful]] [N birds]] [VP [V sang] [ADVP [ADV beautifully]] [PP [PREP in] [NP [DET the] [N garden]]]]]",

    # Q28: "The students from Ohio studied carefully."
    "q28_students_studied": "[S [NP [DET The] [N students] [PP [PREP from] [NP [N Ohio]]]] [VP [V studied] [ADVP [ADV carefully]]]]",

    # Q29: "Several brave firefighters worked tirelessly during the dangerous storm."
    "q29_firefighters_worked": "[S [NP [DET Several] [ADJP [ADJ brave]] [N firefighters]] [VP [V worked] [ADVP [ADV tirelessly]] [PP [PREP during] [NP [DET the] [ADJP [ADJ dangerous]] [N storm]]]]]",

    # Q30: "The tall professor with gray hair spoke very eloquently."
    "q30_professor_spoke": "[S [NP [DET The] [ADJP [ADJ tall]] [N professor] [PP [PREP with] [NP [ADJP [ADJ gray]] [N hair]]]] [VP [V spoke] [ADVP [ADVP [ADV very]] [ADV eloquently]]]]",
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
    log("Generating Exam One Answer Key Diagrams")
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
