"""
Generate ~30 new syntax tree diagrams for the Full Diagram List appendix.
Uses SyntaxTreeHybrid + Playwright.
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
OUTPUT_DIR = Path(r"C:\Users\irphy\Documents\concise-guide-english-grammar\assets\diagrams\new")
EXPORT_MULTIPLIER = 5

# ── ALL NEW APPENDIX DIAGRAMS ────────────────────────────────────────────────
# Format: (filename_without_ext, bracket_notation)

DIAGRAMS = [
    # ── NP: Capstone diagram with all modifier slots ─────────────────────
    (
        "app_np_08_all_slots",
        "[NP [DET the] [ADJP [ADJ brilliant]] [ADJP [ADJ young]] [N student] [PP [PREP from] [NP [N Ohio]]] [RC [REL who] [VP [V studies] [NP [N linguistics]]]]]"
    ),

    # ── VP: The "chef cooks dinner" thread ───────────────────────────────
    (
        "app_vp_01_simple_present",
        "[S [NP [DET The] [N chef]] [VP [V cooks] [NP [N dinner]]]]"
    ),
    (
        "app_vp_02_simple_past",
        "[S [NP [DET The] [N chef]] [VP [V cooked] [NP [N dinner]]]]"
    ),
    (
        "app_vp_03_progressive",
        "[S [NP [DET The] [N chef]] [VP [AUX is] [V cooking] [NP [N dinner]]]]"
    ),
    (
        "app_vp_04_past_progressive",
        "[S [NP [DET The] [N chef]] [VP [AUX was] [V cooking] [NP [N dinner]]]]"
    ),
    (
        "app_vp_05_perfect",
        "[S [NP [DET The] [N chef]] [VP [AUX has] [V cooked] [NP [N dinner]]]]"
    ),
    (
        "app_vp_06_past_perfect",
        "[S [NP [DET The] [N chef]] [VP [AUX had] [V cooked] [NP [N dinner]]] [DC [SUB before] [NP [DET the] [N guests]] [VP [V arrived]]]]"
    ),
    (
        "app_vp_07_perfect_progressive",
        "[S [NP [DET The] [N chef]] [VP [AUX has] [AUX been] [V cooking] [NP [N dinner]]]]"
    ),
    (
        "app_vp_08_past_perfect_prog",
        "[S [NP [DET The] [N chef]] [VP [AUX had] [AUX been] [V cooking] [NP [N dinner]]]]"
    ),
    (
        "app_vp_09_passive",
        "[S [NP [N Dinner]] [VP [AUX was] [V cooked] [PP [PREP by] [NP [DET the] [N chef]]]]]"
    ),
    (
        "app_vp_10_passive_agentless",
        "[S [NP [N Dinner]] [VP [AUX was] [V cooked]]]"
    ),
    (
        "app_vp_11_progressive_passive",
        "[S [NP [N Dinner]] [VP [AUX is] [AUX being] [V cooked] [PP [PREP by] [NP [DET the] [N chef]]]]]"
    ),
    (
        "app_vp_12_get_passive",
        "[S [NP [N Dinner]] [VP [V got] [V burned]]]"
    ),
    (
        "app_vp_13_modal_ability",
        "[S [NP [DET The] [N chef]] [VP [MOD can] [V cook] [NP [N dinner]]]]"
    ),
    (
        "app_vp_14_modal_obligation",
        "[S [NP [DET The] [N chef]] [VP [MOD must] [V cook] [NP [N dinner]]]]"
    ),
    (
        "app_vp_15_modal_epistemic",
        "[S [NP [DET The] [N chef]] [VP [MOD must] [AUX be] [V cooking] [NP [N dinner]]]]"
    ),
    (
        "app_vp_16_modal_perfect",
        "[S [NP [DET The] [N chef]] [VP [MOD should] [AUX have] [V cooked] [NP [N dinner]]]]"
    ),
    (
        "app_vp_17_modal_perf_prog",
        "[S [NP [DET The] [N chef]] [VP [MOD should] [AUX have] [AUX been] [V cooking] [NP [N dinner]]]]"
    ),
    (
        "app_vp_18_full_aux_stack",
        "[S [NP [N Dinner]] [VP [MOD should] [AUX have] [AUX been] [AUX being] [V cooked]]]"
    ),
    (
        "app_vp_19_do_question",
        "[S [AUX Does] [NP [DET the] [N chef]] [VP [V cook] [NP [N dinner]]]]"
    ),
    (
        "app_vp_20_do_negation",
        "[S [NP [DET The] [N chef]] [VP [AUX does] [NEG not] [V cook] [NP [N dinner]]]]"
    ),

    # ── AdvP: Modifying an adjective ─────────────────────────────────────
    (
        "app_advp_04_mod_adj",
        "[ADJP [ADVP [ADV extremely]] [ADJ proud]]"
    ),

    # ── Sentence Patterns: Coordinated VPs ───────────────────────────────
    (
        "app_sent_16_coord_vps",
        "[S [NP [DET The] [N dog]] [VP [VP [V barked]] [CONJ and] [VP [V ran]]]]"
    ),

    # ── Compound/Complex: Compound with "but" ────────────────────────────
    (
        "app_cc_04_compound_but",
        "[S [IC [NP [PRON She]] [VP [V studied] [ADVP [ADV hard]]]] [CONJ but] [IC [NP [PRON she]] [VP [V failed] [NP [DET the] [N exam]]]]]"
    ),

    # ── Adverbials: Participial and Multiple ─────────────────────────────
    (
        "app_adverbl_08_participial",
        "[S [VP [V Walking] [ADVP [ADV home]]] [NP [PRON she]] [VP [V noticed] [NP [DET the] [N sunset]]]]"
    ),
    (
        "app_adverbl_10_multiple",
        "[S [NP [PRON She]] [VP [V worked] [ADVP [ADV hard]] [NP [DET all] [N day]] [PP [PREP in] [NP [DET the] [N library]]]]]"
    ),

    # ── Relative Clauses: whom, whose, when ──────────────────────────────
    (
        "app_relcl_03_whom",
        "[NP [DET the] [N student] [RC [REL whom] [NP [PRON I]] [VP [V met]]]]"
    ),
    (
        "app_relcl_04_whose",
        "[NP [DET the] [N student] [RC [REL whose] [NP [N book]] [NP [PRON I]] [VP [V borrowed]]]]"
    ),
    (
        "app_relcl_06_when",
        "[NP [DET the] [N day] [RC [REL when] [NP [PRON she]] [VP [V graduated]]]]"
    ),

    # ── Complement Clauses: Infinitive complement ────────────────────────
    (
        "app_compcl_05_infinitive",
        "[S [NP [PRON She]] [VP [V wants] [VP [PREP to] [V leave]]]]"
    ),

    # ── Structural Ambiguity: Complement vs. Adjunct PP ──────────────────
    (
        "app_ambig_05_adjunct_vp",
        "[S [NP [PRON She]] [VP [V talked] [PP [PREP about] [NP [DET the] [N problem]]] [PP [PREP on] [NP [DET the] [N phone]]]]]"
    ),
    (
        "app_ambig_06_adjunct_np",
        "[S [NP [PRON She]] [VP [V talked] [PP [PREP about] [NP [DET the] [N problem] [PP [PREP on] [NP [DET the] [N phone]]]]]]]"
    ),
]


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


def generate_diagrams(start_from=None):
    log("=" * 70)
    log("Appendix Diagram Generation")
    log("=" * 70)
    log(f"Total diagrams: {len(DIAGRAMS)}")
    log(f"Output: {OUTPUT_DIR}")
    log("")

    diagrams_to_run = []
    skipping = bool(start_from)
    for name, bracket in DIAGRAMS:
        if skipping:
            if name == start_from:
                skipping = False
            else:
                continue
        out_path = OUTPUT_DIR / f"{name}.png"
        if out_path.exists():
            log(f"  [SKIP] {name}.png already exists")
            continue
        diagrams_to_run.append((name, bracket))

    if not diagrams_to_run:
        log("All diagrams already exist. Done.")
        return

    log(f"Diagrams to generate: {len(diagrams_to_run)}")
    log("")

    log("Starting HTTP server...")
    server = threading.Thread(target=start_server, daemon=True)
    server.start()
    time.sleep(1)

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1400, "height": 900})

        for i, (name, bracket) in enumerate(diagrams_to_run):
            log(f"\n[{i+1:02d}/{len(diagrams_to_run)}] {name}")
            log(f"  Bracket: {bracket}")

            page.goto(f"http://localhost:{PORT}/index.html")
            page.wait_for_selector("#diagram-canvas", state="visible")
            time.sleep(0.5)

            bracket_input = page.locator("#bracket-input")
            bracket_input.click()
            bracket_input.fill(bracket)
            time.sleep(1.0)

            status = page.locator("#bracket-status").inner_text()
            success = "error" not in status.lower()

            attempts = 1
            while not success and attempts < 3:
                log(f"  Attempt {attempts} failed ({status}), retrying...")
                attempts += 1
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
                    log(f"  Status: {status}")
                    log(f"  Saved: {name}.png")
                    results.append({"name": name, "success": True})
                except Exception as e:
                    log(f"  Export error: {e}")
                    results.append({"name": name, "success": False, "status": str(e)})
            else:
                log(f"  FAILED: {status}")
                results.append({"name": name, "success": False, "status": status})

            time.sleep(0.3)

        browser.close()

    log("\n" + "=" * 70)
    passed = sum(1 for r in results if r["success"])
    failed = len(results) - passed
    log(f"Done: {passed} succeeded, {failed} failed")
    if failed:
        log("\nFailed:")
        for r in results:
            if not r["success"]:
                log(f"  - {r['name']}: {r.get('status', '?')}")
    log("=" * 70)


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    start_from = sys.argv[1] if len(sys.argv) > 1 else None
    generate_diagrams(start_from)
