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

# 10 bonus assignment sentences — more complex structures, PP in every position
DIAGRAMS = {
    # Q1: PP modifying N (subject head); long NP with two pre-nominal ADJs
    # "The tall energetic student near the door arrived late."
    "bonus_q01_student_arrived": "[S [NP [DET The] [ADJP [ADJ tall]] [ADJP [ADJ energetic]] [N student] [PP [PREP near] [NP [DET the] [N door]]]] [VP [V arrived] [ADVP [ADV late]]]]",

    # Q2: PP modifying N (subject head); very long NP (2 ADJs + post-nominal PP with ADJ)
    # "The brilliant young professor from the northern campus spoke clearly."
    "bonus_q02_professor_spoke": "[S [NP [DET The] [ADJP [ADJ brilliant]] [ADJP [ADJ young]] [N professor] [PP [PREP from] [NP [DET the] [ADJP [ADJ northern]] [N campus]]]] [VP [V spoke] [ADVP [ADV clearly]]]]",

    # Q3: PP modifying ADJ (PP inside post-nominal ADJP)
    # "The student afraid of failure studied very diligently."
    "bonus_q03_student_studied": "[S [NP [DET The] [N student] [ADJP [ADJ afraid] [PP [PREP of] [NP [N failure]]]]] [VP [V studied] [ADVP [ADVP [ADV very]] [ADV diligently]]]]",

    # Q4: PP modifying ADV ("far" modified by "from the noisy old city")
    # "They lived quite far from the noisy old city."
    "bonus_q04_they_lived": "[S [NP [PRO They]] [VP [V lived] [ADVP [ADVP [ADV quite]] [ADV far] [PP [PREP from] [NP [DET the] [ADJP [ADJ noisy]] [ADJP [ADJ old]] [N city]]]]]]",

    # Q5: Nested PP — PP modifying N as object of preposition
    # "He waited quietly at the bench near the old fountain."
    "bonus_q05_he_waited": "[S [NP [PRO He]] [VP [V waited] [ADVP [ADV quietly]] [PP [PREP at] [NP [DET the] [N bench] [PP [PREP near] [NP [DET the] [ADJP [ADJ old]] [N fountain]]]]]]]",

    # Q6: Very long VP — V + ADVP + PP + PP (two adverbial PPs)
    # "She sat quite peacefully near the tall fountain in the old courtyard."
    "bonus_q06_she_sat": "[S [NP [PRO She]] [VP [V sat] [ADVP [ADVP [ADV quite]] [ADV peacefully]] [PP [PREP near] [NP [DET the] [ADJP [ADJ tall]] [N fountain]]] [PP [PREP in] [NP [DET the] [ADJP [ADJ old]] [N courtyard]]]]]",

    # Q7: Long NP (DET+ADJ+ADJ+N+PP) AND long VP (V+ADVP+PP)
    # "The tired old dog from the farm slept quietly near the fire."
    "bonus_q07_dog_slept": "[S [NP [DET The] [ADJP [ADJ tired]] [ADJP [ADJ old]] [N dog] [PP [PREP from] [NP [DET the] [N farm]]]] [VP [V slept] [ADVP [ADV quietly]] [PP [PREP near] [NP [DET the] [N fire]]]]]",

    # Q8: PP modifying V; PP object NP contains two ADJs
    # "The nervous boy sat rigidly in the hard narrow chair."
    "bonus_q08_boy_sat": "[S [NP [DET The] [ADJP [ADJ nervous]] [N boy]] [VP [V sat] [ADVP [ADV rigidly]] [PP [PREP in] [NP [DET the] [ADJP [ADJ hard]] [ADJP [ADJ narrow]] [N chair]]]]]",

    # Q9: PP modifying ADV — "deep" modified by "in the dark forest" (second ADVP in VP)
    # "The small birds sang very loudly deep in the dark forest."
    "bonus_q09_birds_sang": "[S [NP [DET The] [ADJP [ADJ small]] [N birds]] [VP [V sang] [ADVP [ADVP [ADV very]] [ADV loudly]] [ADVP [ADV deep] [PP [PREP in] [NP [DET the] [ADJP [ADJ dark]] [N forest]]]]]]",

    # Q10: Very long NP — post-nominal ADJP whose head ADJ has a PP complement (PP → ADJ)
    # "The old woman confident in her skills spoke quite passionately."
    "bonus_q10_woman_spoke": "[S [NP [DET The] [ADJP [ADJ old]] [N woman] [ADJP [ADJ confident] [PP [PREP in] [NP [DET her] [N skills]]]]] [VP [V spoke] [ADVP [ADVP [ADV quite]] [ADV passionately]]]]",
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
