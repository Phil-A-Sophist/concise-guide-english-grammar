"""
Generate diagram PNGs for the Bonus Assignment Answer Key.
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
OUTPUT_DIR = Path(r"C:\Users\irphy\Documents\concise-guide-english-grammar\Homework\Exams\diagrams")
EXPORT_MULTIPLIER = 5

# 10 bonus assignment sentences (all intransitive, ~8 words each)
DIAGRAMS = {
    # Q1: "The tall student slept quietly in the library."
    "bonus_q01_student_slept": "[S [NP [DET The] [ADJP [ADJ tall]] [N student]] [VP [V slept] [ADVP [ADV quietly]] [PP [PREP in] [NP [DET the] [N library]]]]]",

    # Q2: "The young children played happily in the yard."
    "bonus_q02_children_played": "[S [NP [DET The] [ADJP [ADJ young]] [N children]] [VP [V played] [ADVP [ADV happily]] [PP [PREP in] [NP [DET the] [N yard]]]]]",

    # Q3: "She ran very quickly through the dark forest."
    "bonus_q03_she_ran": "[S [NP [PRO She]] [VP [V ran] [ADVP [ADV very] [ADV quickly]] [PP [PREP through] [NP [DET the] [ADJP [ADJ dark]] [N forest]]]]]",

    # Q4: "The old dog rested near the warm fireplace."
    "bonus_q04_dog_rested": "[S [NP [DET The] [ADJP [ADJ old]] [N dog]] [VP [V rested] [PP [PREP near] [NP [DET the] [ADJP [ADJ warm]] [N fireplace]]]]]",

    # Q5: "The bright stars shone above the quiet town."
    "bonus_q05_stars_shone": "[S [NP [DET The] [ADJP [ADJ bright]] [N stars]] [VP [V shone] [PP [PREP above] [NP [DET the] [ADJP [ADJ quiet]] [N town]]]]]",

    # Q6: "They walked very slowly along the narrow path."
    "bonus_q06_they_walked": "[S [NP [PRO They]] [VP [V walked] [ADVP [ADV very] [ADV slowly]] [PP [PREP along] [NP [DET the] [ADJP [ADJ narrow]] [N path]]]]]",

    # Q7: "The nervous professor spoke clearly at the podium."
    "bonus_q07_professor_spoke": "[S [NP [DET The] [ADJP [ADJ nervous]] [N professor]] [VP [V spoke] [ADVP [ADV clearly]] [PP [PREP at] [NP [DET the] [N podium]]]]]",

    # Q8: "Small birds sang loudly near the old oak."
    "bonus_q08_birds_sang": "[S [NP [ADJP [ADJ Small]] [N birds]] [VP [V sang] [ADVP [ADV loudly]] [PP [PREP near] [NP [DET the] [ADJP [ADJ old]] [N oak]]]]]",

    # Q9: "He waited very patiently outside the large building."
    "bonus_q09_he_waited": "[S [NP [PRO He]] [VP [V waited] [ADVP [ADV very] [ADV patiently]] [PP [PREP outside] [NP [DET the] [ADJP [ADJ large]] [N building]]]]]",

    # Q10: "The tired runner collapsed suddenly at the barrier."
    "bonus_q10_runner_collapsed": "[S [NP [DET The] [ADJP [ADJ tired]] [N runner]] [VP [V collapsed] [ADVP [ADV suddenly]] [PP [PREP at] [NP [DET the] [N barrier]]]]]",
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
    log("Generating Bonus Assignment Diagrams")
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
