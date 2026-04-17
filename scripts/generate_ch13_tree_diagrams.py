"""
Generate tree diagram PNGs for Ch13 Adjectivals content sections.
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
    # 13.2 #4 / 13.11.2 A: Restrictive relative clause
    "ch13_rel_clause_restr": "[S [NP [DET The] [N students] [RC [NP [REL who]] [VP [V studied]]]] [VP [V passed]]]",

    # 13.2 #6 / 13.11.2 E: Infinitive adjectival
    "ch13_inf_adjectival": "[S [NP [PRON He]] [VP [V has] [NP [NP [N time]] [VP [V to spare]]]]]",

    # 13.11.2 B: Non-restrictive relative clause
    "ch13_rel_clause_non_restr": "[S [NP [NP [PRON My] [N sister]] [RC [NP [REL who]] [VP [V lives] [PP [PREP in] [NP [N Boston]]]]]] [VP [V called]]]",

    # 13.2 #2 / 13.6 / 13.11: Noun adjunct
    "ch13_noun_adjunct": "[S [NP [DET The] [N history] [N professor]] [VP [V lectured]]]",

    # 13.5: Degree-modified AdjP
    "ch13_adjp_degree": "[S [NP [DET The] [ADJP [ADV extremely] [ADJ tall]] [N building]] [VP [V collapsed]]]",

    # 13.6: Noun adjunct (detail section)
    "ch13_noun_adjunct_detail": "[S [NP [DET The] [N government] [N report]] [VP [V arrived]]]",

    # 13.7: PP adjectival (new sentence)
    "ch13_pp_adj_detail": "[S [NP [DET The] [N woman] [PP [PREP in] [NP [DET the] [N office]]]] [VP [V called]]]",

    # 13.8: Relative clause (detail section)
    "ch13_rel_clause_detail": "[S [NP [DET The] [N student] [RC [NP [REL who]] [VP [V won] [NP [DET the] [N award]]]]] [VP [V celebrated]]]",

    # 13.9: Participial phrase (detail section)
    "ch13_part_phrase_detail": "[S [NP [DET The] [N woman] [VP [V wearing] [NP [DET the] [ADJP [ADJ red]] [N coat]]]] [VP [V smiled]]]",

    # 13.10: Infinitive adjectival (new sentence)
    "ch13_inf_adj_detail": "[S [NP [DET The] [N team]] [VP [V has] [NP [NP [DET a] [N plan]] [VP [V to follow]]]]]",

    # 13.4: Restrictive/Non-restrictive
    "ch13_restr_nonrestr": "[S [NP [DET The] [N players] [RC [NP [REL who]] [VP [V practiced]]]] [VP [V won] [NP [DET the] [N game]]]]",
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
    log("Generating Ch13 Content Tree Diagrams")
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
