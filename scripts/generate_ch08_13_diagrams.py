"""
Generate 48 inline syntax tree diagrams for chapters 8-13.
8 diagrams per chapter, placed in body sections.
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

PORT = 8081  # Use 8081 to avoid conflict with other servers
SYNTAX_TREE_DIR = Path(r"C:\Users\irphy\Documents\SyntaxTreeHybrid")
OUTPUT_DIR = Path(r"C:\Users\irphy\Documents\concise-guide-english-grammar\assets\diagrams\new")
EXPORT_MULTIPLIER = 5

# ── ALL 48 DIAGRAMS ─────────────────────────────────────────────────────────
# Format: (filename_without_ext, bracket_notation)

DIAGRAMS = [
    # ── CH-08: Basic Sentence Elements and Sentence Patterns ─────────────
    (
        "ch08_s_np_vp",
        "[S [NP [N Dogs]] [VP [V bark]]]"
    ),
    (
        "ch08_subj_pred_example",
        "[S [NP [DET The] [ADJ young] [N artist]] [VP [V arrived]]]"
    ),
    (
        "ch08_argument_put",
        "[S [NP [PRON She]] [VP [V put] [NP [DET the] [N book]] [PP [PREP on] [NP [DET the] [N table]]]]]"
    ),
    (
        "ch08_adverbial_spoke",
        "[S [NP [PRON She]] [VP [V spoke] [ADVP [ADV quietly]] [PP [PREP in] [NP [DET the] [N library]]]]]"
    ),
    (
        "ch08_direct_obj_basic",
        "[S [NP [DET The] [N cat]] [VP [V chased] [NP [DET the] [N mouse]]]]"
    ),
    (
        "ch08_subj_complement_adj",
        "[S [NP [PRON She]] [VP [V seems] [ADJP [ADJ happy]]]]"
    ),
    (
        "ch08_obj_complement_adj",
        "[S [NP [DET The] [N jury]] [VP [V found] [NP [PRON him]] [ADJP [ADJ guilty]]]]"
    ),
    (
        "ch08_valency_intrans",
        "[S [NP [N Birds]] [VP [V sing]]]"
    ),

    # ── CH-09: Compound and Complex Sentences ─────────────────────────────
    (
        "ch09_simple_sentence",
        "[S [NP [DET The] [N students]] [VP [V studied]]]"
    ),
    (
        "ch09_compound_and",
        "[S [IC [NP [PRON She]] [VP [V writes] [NP [N poetry]]]] [CONJ and] [IC [NP [PRON he]] [VP [V composes] [NP [N music]]]]]"
    ),
    (
        "ch09_compound_subj_only",
        "[S [NP [NP [N Marcus]] [CONJ and] [NP [N Elena]]] [VP [V traveled]]]"
    ),
    (
        "ch09_complex_because",
        "[S [IC [NP [PRON She]] [VP [V declined]]] [DC [SUB because] [NP [PRON she]] [VP [AUX had] [NP [ADJ other] [N plans]]]]]"
    ),
    (
        "ch09_complex_when_first",
        "[S [DC [SUB When] [NP [DET the] [N power]] [VP [V flickered]]] [IC [NP [PRON Everyone]] [VP [V looked] [ADVP [ADV up]]]]]"
    ),
    (
        "ch09_relative_clause",
        "[S [NP [DET The] [N candidate] [RC [REL who] [VP [V impressed] [NP [DET the] [N committee]]]]] [VP [V received] [NP [DET the] [N position]]]]"
    ),
    (
        "ch09_noun_clause_obj",
        "[S [NP [PRON I]] [VP [V understand] [NC [COMP that] [NP [PRON you]] [VP [V are] [ADJP [ADJ frustrated]]]]]]"
    ),
    (
        "ch09_noun_clause_subj",
        "[S [NC [COMP That] [NP [PRON she]] [VP [V resigned]]] [VP [V shocked] [NP [DET the] [N board]]]]"
    ),

    # ── CH-10: Verbs Part One — Tense and Aspect ─────────────────────────
    (
        "ch10_be_progressive",
        "[S [NP [PRON She]] [VP [AUX is] [V reading]]]"
    ),
    (
        "ch10_be_passive_aux",
        "[S [NP [DET The] [N book]] [VP [AUX was] [V written] [PP [PREP by] [NP [N Maria]]]]]"
    ),
    (
        "ch10_have_perfect",
        "[S [NP [PRON She]] [VP [AUX has] [V finished] [NP [DET the] [N work]]]]"
    ),
    (
        "ch10_have_perfect_past",
        "[S [NP [PRON They]] [VP [AUX had] [V left]] [DC [SUB before] [NP [PRON I]] [VP [V arrived]]]]"
    ),
    (
        "ch10_do_question",
        "[S [AUX Does] [NP [PRON she]] [VP [V work] [ADVP [ADV here]]]]"
    ),
    (
        "ch10_do_negation",
        "[S [NP [PRON She]] [VP [AUX does] [NEG not] [V work] [ADVP [ADV here]]]]"
    ),
    (
        "ch10_simple_present",
        "[S [NP [PRON She]] [VP [V walks] [PP [PREP to] [NP [N school]]] [NP [DET every] [N day]]]]"
    ),
    (
        "ch10_perfect_progressive_pres",
        "[S [NP [PRON She]] [VP [AUX has] [AUX been] [V waiting]]]"
    ),

    # ── CH-11: Verbs Part Two — Voice and Modals ─────────────────────────
    (
        "ch11_active_sentence",
        "[S [NP [DET The] [N dog]] [VP [V bit] [NP [DET the] [N man]]]]"
    ),
    (
        "ch11_passive_by",
        "[S [NP [DET The] [N man]] [VP [AUX was] [V bitten] [PP [PREP by] [NP [DET the] [N dog]]]]]"
    ),
    (
        "ch11_passive_agentless",
        "[S [NP [DET The] [N window]] [VP [AUX was] [V broken]]]"
    ),
    (
        "ch11_get_passive_body",
        "[S [NP [PRON She]] [VP [V got] [V promoted]]]"
    ),
    (
        "ch11_modal_can_ability",
        "[S [NP [PRON She]] [VP [MOD can] [V swim]]]"
    ),
    (
        "ch11_modal_must_oblig",
        "[S [NP [PRON You]] [VP [MOD must] [V stop] [ADVP [ADV here]]]]"
    ),
    (
        "ch11_modal_must_epist",
        "[S [NP [PRON She]] [VP [MOD must] [V be] [ADJP [ADJ tired]]]]"
    ),
    (
        "ch11_modal_should_perf",
        "[S [NP [PRON You]] [VP [MOD should] [AUX have] [V called]]]"
    ),

    # ── CH-12: Adverbials ─────────────────────────────────────────────────
    (
        "ch12_advp_adverbial",
        "[S [NP [PRON She]] [VP [V ran] [ADVP [ADV quickly]]]]"
    ),
    (
        "ch12_pp_place_adverbial",
        "[S [NP [PRON He]] [VP [V works] [PP [PREP in] [NP [DET the] [N city]]]]]"
    ),
    (
        "ch12_pp_time_adverbial",
        "[S [NP [PRON She]] [VP [V arrived] [PP [PREP at] [NP [N noon]]]]]"
    ),
    (
        "ch12_adv_clause_because",
        "[S [IC [NP [PRON She]] [VP [V left]]] [DC [SUB because] [NP [PRON she]] [VP [V was] [ADJP [ADJ tired]]]]]"
    ),
    (
        "ch12_adv_clause_when",
        "[S [DC [SUB When] [NP [DET the] [N class]] [VP [V ended]]] [IC [NP [N students]] [VP [V left]]]]"
    ),
    (
        "ch12_sentence_adverb_disj",
        "[S [ADVP [ADV Fortunately]] [NP [PRON she]] [VP [V passed]]]"
    ),
    (
        "ch12_multiple_adverbials",
        "[S [NP [PRON She]] [VP [V worked] [ADVP [ADV hard]] [NP [DET all] [N day]]]]"
    ),
    (
        "ch12_inf_purpose_adverb",
        "[S [NP [PRON He]] [VP [V saved] [NP [N money]] [VP [PREP to] [V buy] [NP [DET a] [N car]]]]]"
    ),

    # ── CH-13: Adjectivals ────────────────────────────────────────────────
    (
        "ch13_adj_prenominal",
        "[S [NP [DET The] [ADJ red] [N car]] [VP [V stopped]]]"
    ),
    (
        "ch13_adj_predicative",
        "[S [NP [DET The] [N car]] [VP [V is] [ADJP [ADJ red]]]]"
    ),
    (
        "ch13_pp_adjectival",
        "[S [NP [DET The] [N book] [PP [PREP on] [NP [DET the] [N shelf]]]] [VP [V is] [PRON mine]]]"
    ),
    (
        "ch13_rel_clause_restr",
        "[S [NP [DET The] [N students] [RC [REL who] [VP [V studied]]]] [VP [V passed]]]"
    ),
    (
        "ch13_rel_clause_non_restr",
        "[S [NP [NP [PRON My] [N sister]] [RC [REL who] [VP [V lives] [PP [PREP in] [NP [N Boston]]]]]] [VP [V called]]]"
    ),
    (
        "ch13_pres_part_phrase",
        "[S [NP [DET The] [N woman] [VP [V singing] [PP [PREP on] [NP [N stage]]]]] [VP [V left]]]"
    ),
    (
        "ch13_past_part_phrase",
        "[S [NP [DET The] [N report] [VP [V written] [PP [PREP by] [NP [DET the] [N team]]]]] [VP [V was] [ADJP [ADJ thorough]]]]"
    ),
    (
        "ch13_inf_adjectival",
        "[S [NP [PRON He]] [VP [V has] [NP [NP [N time]] [VP [PREP to] [V spare]]]]]"
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
    log("Ch08-13 Inline Diagram Generation")
    log("=" * 70)
    log(f"Total diagrams: {len(DIAGRAMS)}")
    log(f"Output: {OUTPUT_DIR}")
    log("")

    # Skip already-existing diagrams unless start_from is specified
    diagrams_to_run = []
    for name, bracket in DIAGRAMS:
        out_path = OUTPUT_DIR / f"{name}.png"
        if start_from:
            if name == start_from:
                start_from = None  # start including from here
            else:
                continue
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
