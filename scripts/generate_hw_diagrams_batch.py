"""
Generate homework diagram PNGs for Chapters 5, 6, 8, 9, 12, 13, 14, 15.
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
BASE_OUTPUT_DIR = Path(r"C:\Users\irphy\Documents\concise-guide-english-grammar\Homework\diagrams")
EXPORT_MULTIPLIER = 5

# All chapters and their diagrams
CHAPTERS = {
    'ch05': {
        'ch05_hw_ex15_girl_runs':
            '[S [NP [DET The] [ADJP [ADJ tall]] [N girl]] [VP [V runs] [ADVP [ADV quickly]]]]',
        'ch05_hw_ex16_rain_fell':
            '[S [NP [ADJP [ADJ Heavy]] [N rain]] [VP [V fell] [ADVP [ADV suddenly]]]]',
        'ch05_hw_ex17_artist_painted':
            '[S [NP [DET The] [ADJP [ADJ young]] [N artist]] [VP [V painted] [ADVP [ADV beautifully]]]]',
        'ch05_hw_ex18_birds_sing':
            '[S [NP [ADJP [ADJ Small]] [N birds]] [VP [V sing] [ADVP [ADV loudly]]]]',
        'ch05_hw_ex19_student_solved':
            '[S [NP [DET The] [ADJP [ADJ clever]] [N student]] [VP [V solved] [NP [DET the] [ADJP [ADJ difficult]] [N problem]] [ADVP [ADV easily]]]]',
    },
    'ch06': {
        'ch06_hw_ex11_she_walked':
            '[S [NP [PRON She]] [VP [V walked] [PP [PREP to] [NP [DET the] [N store]]]]]',
        'ch06_hw_ex12_they_gave':
            '[S [NP [PRON They]] [VP [V gave] [NP [PRON it]] [PP [PREP to] [NP [PRON her]]]]]',
        'ch06_hw_ex13_book_belongs':
            '[S [NP [DET The] [N book] [PP [PREP on] [NP [DET the] [N shelf]]]] [VP [V belongs] [PP [PREP to] [NP [PRON him]]]]]',
        'ch06_hw_ex14_everyone_listened':
            '[S [NP [PRON Everyone] [PP [PREP in] [NP [DET the] [N room]]]] [VP [V listened] [ADVP [ADV carefully]]]]',
        'ch06_hw_ex15_sister_drove':
            '[S [NP [DET My] [N sister] [CONJ and] [PRON I]] [VP [V drove] [PP [PREP to] [NP [DET the] [N park]]]]]',
    },
    'ch08': {
        'ch08_hw_ex11a_birds_sing':
            '[S [NP [N Birds]] [VP [V sing]]]',
        'ch08_hw_ex11b_solution_simple':
            '[S [NP [DET The] [N solution]] [VP [V was] [ADJP [ADJ simple]]]]',
        'ch08_hw_ex11c_music_sounded':
            '[S [NP [DET The] [N music]] [VP [V sounded] [ADJP [ADJ beautiful]]]]',
        'ch08_hw_ex11d_student_finished':
            '[S [NP [DET The] [N student]] [VP [V finished] [NP [DET the] [N report]]]]',
        'ch08_hw_ex11e_professor_gave':
            '[S [NP [DET The] [N professor]] [VP [V gave] [NP [DET the] [N class]] [NP [DET a] [N deadline]]]]',
        'ch08_hw_ex11f_board_declared':
            '[S [NP [DET The] [N board]] [VP [V declared] [NP [DET the] [N plan]] [ADJP [ADJ inadequate]]]]',
    },
    'ch09': {
        'ch09_hw_ex11a_marcus_traveled':
            '[S [NP [N Marcus] [CONJ and] [N Elena]] [VP [V traveled]]]',
        'ch09_hw_ex11b_dog_barked':
            '[S [NP [DET The] [N dog]] [VP [V barked] [CONJ and] [VP [V chased] [NP [DET the] [N squirrel]]]]]',
        'ch09_hw_ex11c_writes_composes':
            '[S [IC [NP [PRON She]] [VP [V writes] [NP [N poetry]]]] [CC [CONJ and]] [IC [NP [PRON he]] [VP [V composes] [NP [N music]]]]]',
        'ch09_hw_ex11d_when_rained':
            '[S [DC [SUB When] [NP [PRON it]] [VP [V rained]]] [IC [NP [PRON we]] [VP [V stayed] [ADVP [ADV inside]]]]]',
    },
    'ch12': {
        'ch12_hw_ex14_practiced_afternoon':
            '[S [NP [DET The] [N team]] [VP [V practiced] [NP [DET every] [N afternoon]]]]',
        'ch12_hw_ex15_paused_check':
            '[S [NP [PRON She]] [VP [V paused] [VP [V to_check] [NP [DET her] [N notes]]]]]',
        'ch12_hw_ex16_running_caught':
            '[S [VP [V Running] [ADVP [ADV quickly]]] [NP [PRON he]] [VP [V caught] [NP [DET the] [N bus]]]]',
        'ch12_hw_ex17_unfortunately':
            '[S [ADVP [ADV Unfortunately]] [NP [DET the] [N game]] [VP [AUX was] [V cancelled]]]',
        'ch12_hw_ex18_left_early':
            '[S [IC [NP [PRON She]] [VP [V left] [ADVP [ADV early]]]] [DC [SUB because] [NP [DET the] [N roads]] [VP [V were] [ADJP [ADJ icy]]]]]',
    },
    'ch13': {
        'ch13_hw_ex16_student_award':
            '[S [NP [DET The] [N student] [RC [REL who] [VP [V won] [NP [DET the] [N award]]]]] [VP [V celebrated]]]',
        'ch13_hw_ex17_selected_team':
            '[S [NP [DET The] [N students] [VP [V selected] [PP [PREP for] [NP [DET the] [N team]]]]] [VP [V celebrated]]]',
        'ch13_hw_ex18_plan_win':
            '[S [NP [DET The] [N team]] [VP [V has] [NP [DET a] [N plan] [VP [V to_win] [NP [DET the] [N tournament]]]]]]',
        'ch13_hw_ex19_running_water':
            '[S [NP [VP [V Running]] [N water]] [VP [V flowed] [PP [PREP through] [NP [DET the] [N pipe]]]]]',
        'ch13_hw_ex20_woman_coat':
            '[S [NP [DET The] [N woman] [VP [V wearing] [NP [DET the] [ADJP [ADJ red]] [N coat]]]] [VP [V smiled]]]',
    },
    # 'ch14' loaded from canonical data/trees/ch14/ — see _load_canonical_ch14() below
    'ch15': {
        'ch15_hw_ex16_storm_ended':
            '[S [IC [NP [DET The] [N storm]] [VP [V ended]]] [CC [CONJ and]] [IC [NP [DET the] [N sun]] [VP [V came] [ADVP [ADV out]]]]]',
        'ch15_hw_ex17_although_tired':
            '[S [DC [COMP Although] [NP [PRON she]] [VP [V was] [ADJP [ADJ tired]]]] [IC [NP [PRON she]] [VP [V finished] [NP [DET the] [N report]]]]]',
        'ch15_hw_ex18_however':
            '[S [NP [DET The] [N professor]] [ADVP [ADV however]] [VP [V disagreed] [ADVP [ADV completely]]]]',
        'ch15_hw_ex19_sister_boston':
            '[S [NP [DET My] [N sister] [RC [REL who] [VP [V lives] [PP [PREP in] [NP [N Boston]]]]]] [VP [V visits] [ADVP [ADV often]]]]',
        'ch15_hw_ex20_after_lecture':
            '[S [PP [PREP After] [NP [DET the] [N lecture]]] [NP [N students]] [VP [V asked] [NP [DET many] [N questions]]]]',
    },
}


def _load_canonical_ch14():
    """Load ch14 homework diagrams from canonical data/trees/ch14/."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from answer_key_helpers import load_canonical_trees
    out = {}
    for entry in load_canonical_trees(14, purpose='homework'):
        name = entry.get('diagram_filename')
        if not name:
            continue
        if 'diagram_png' not in entry.get('outputs', []):
            continue
        out[name] = entry['bracket']
    return out


# Inject canonical ch14 entries
CHAPTERS['ch14'] = _load_canonical_ch14()


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
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--chapter', type=int, default=None,
                        help='Limit to a single chapter, e.g., --chapter 14')
    cli_args = parser.parse_args()

    chapters = dict(CHAPTERS)
    if cli_args.chapter is not None:
        key = f'ch{cli_args.chapter:02d}'
        chapters = {key: chapters.get(key, {})}
        if not chapters[key]:
            log(f"No diagrams for {key}")
            return

    total = sum(len(d) for d in chapters.values())
    log("=" * 60)
    log(f"Generating Homework Diagrams: {len(chapters)} chapter(s), {total} diagrams")
    log("=" * 60)

    log("Starting HTTP server...")
    server = threading.Thread(target=start_server, daemon=True)
    server.start()
    time.sleep(1)

    results = []
    count = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1400, "height": 900})

        for ch_name, diagrams in chapters.items():
            output_dir = BASE_OUTPUT_DIR / ch_name
            output_dir.mkdir(parents=True, exist_ok=True)
            log(f"\n--- {ch_name.upper()} ({len(diagrams)} diagrams) -> {output_dir} ---")

            for name, bracket in diagrams.items():
                count += 1
                log(f"\n[{count}/{total}] {name}")
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
                        output_path = output_dir / f"{name}.png"
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
    failed = [n for n, ok in results if not ok]
    log(f"\nDone: {passed}/{len(results)} succeeded")
    if failed:
        log(f"FAILED: {', '.join(failed)}")


if __name__ == "__main__":
    main()
