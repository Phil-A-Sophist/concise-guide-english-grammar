#!/usr/bin/env python3
"""Generate table and tree diagram PNGs for PPT slides via SyntaxTreeHybrid + Playwright.

Uses the same proven pattern as generate_hw_diagrams_batch.py (trees) and
regenerate_all_table_pngs.py (tables).
"""

import json
import sys
import os
import time
import base64
import threading
import http.server
import socketserver
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("ERROR: pip install playwright && playwright install chromium")
    sys.exit(1)

sys.stdout.reconfigure(line_buffering=True)

PROJECT_ROOT = Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "static" / "ppt_diagram_data.json"
CANONICAL_DIR = PROJECT_ROOT / "data" / "trees" / "ppt"
TABLE_DIR = PROJECT_ROOT / "data" / "static" / "ppt-diagrams" / "tables"
TREE_DIR = PROJECT_ROOT / "data" / "static" / "ppt-diagrams" / "trees"
STH_DIR = Path("C:/Users/irphy/Documents/SyntaxTreeHybrid")

PORT = 8084
EXPORT_MULTIPLIER = 5

TABLE_DIR.mkdir(parents=True, exist_ok=True)
TREE_DIR.mkdir(parents=True, exist_ok=True)

# Role assignments keyed by sentence ID → depth-indexed dict
ROLE_ASSIGNMENTS = {
    "adv_01": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"1": "Adverbial", "3": "Adverbial"},
        "2": {"2": "Obj Prep", "4": "Direct Object"},
    },
    "adv_02": {
        "0": {"0": "Adverbial", "1": "Subject", "2": "Predicate"},
        "1": {"1": "Direct Object", "3": "Direct Object"},
    },
    "adv_03": {
        "0": {"0": "Adverbial", "2": "Subject", "3": "Predicate"},
        "1": {"1": "Adverbial", "4": "Direct Object"},
        "2": {"2": "Obj Prep"},
    },
    "adv_04_preview": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"1": "Adjectival"},
    },
    "adv_05_preview": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"2": "Direct Object"},
        "2": {"3": "Adjectival"},
    },
    "adv_06_preview": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"1": "Adjectival", "2": "Adverbial"},
    },
    "adj_01": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"1": "Adjectival", "3": "Subject Complement"},
        "2": {"2": "Direct Object", "5": "Adverbial"},
        "3": {"6": "Obj Prep"},
    },
    "adj_02": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"0": "Adjectival", "2": "Adverbial"},
        "2": {"3": "Obj Prep"},
    },
    "adj_03": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"1": "Adverbial"},
        "2": {"2": "Obj Prep"},
        "3": {"3": "Adjectival"},
        "4": {"4": "Adverbial"},
        "5": {"5": "Obj Prep"},
    },
    "adj_04": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"0": "Adjectival", "2": "Adverbial"},
        "2": {"3": "Obj Prep"},
    },
    "adj_05": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"1": "Adjectival", "3": "Direct Object"},
        "2": {"3": "Adjectival"},
    },
    "adj_06": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"1": "Adverbial"},
        "2": {"2": "Obj Prep"},
        "3": {"3": "Adjectival"},
    },
    "adj_07": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"1": "Adjectival", "3": "Adverbial"},
    },
    "adj_08": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"2": "Direct Object"},
        "2": {"3": "Adjectival"},
    },
    "adj_09": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"1": "Direct Object"},
        "2": {"2": "Adverbial"},
        "3": {"3": "Obj Prep"},
        "4": {"4": "Adjectival"},
    },
    "adj_10_preview": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"1": "Direct Object"},
    },
    "adj_11_preview": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"1": "Subject Complement"},
    },
    "adj_12_preview": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"1": "Direct Object"},
    },
    "nom_01": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"0": "Adverbial", "2": "Subject Complement"},
        "2": {"1": "Obj Prep"},
    },
    "nom_02": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"1": "Direct Object"},
        "2": {"2": "Direct Object"},
    },
    "nom_03": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"1": "Direct Object"},
    },
    "nom_04": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"1": "Direct Object", "3": "Direct Object"},
    },
    "nom_05": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"2": "Subject Complement"},
        "2": {"3": "Adverbial"},
        "3": {"4": "Obj Prep"},
    },
}


def start_server():
    os.chdir(str(STH_DIR))
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *args: None
    httpd = socketserver.TCPServer(("", PORT), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    print(f"[SERVER] SyntaxTreeHybrid on http://localhost:{PORT}")
    return httpd


def save_data_url_as_png(data_url, filepath):
    header, encoded = data_url.split(',', 1)
    data = base64.b64decode(encoded)
    with open(filepath, 'wb') as f:
        f.write(data)


def fill_roles_via_dom(page, roles_dict):
    """Fill role cells by setting textContent via JS evaluate."""
    page.evaluate('''
        (rolesDict) => {
            const table = document.querySelector('.labeling-table');
            if (!table) return;
            const rows = table.querySelectorAll('tr');
            let roleIndex = 0;
            rows.forEach((row) => {
                const header = row.querySelector('th');
                if (!header || !header.textContent.trim().startsWith('Role')) return;
                const cells = row.querySelectorAll('td');
                let pos = 0;
                cells.forEach((cell) => {
                    if (cell.contentEditable === 'true') {
                        let role = (rolesDict[String(roleIndex)] || {})[String(pos)];
                        if (role) {
                            cell.textContent = role;
                        }
                    }
                    pos += (cell.colSpan || 1);
                });
                roleIndex++;
            });
        }
    ''', roles_dict)
    page.wait_for_timeout(200)


def generate_tree(page, url, bracket, output_path):
    """Generate a tree diagram PNG via exportPNG()."""
    page.goto(url)
    page.wait_for_selector('#bracket-input', state='visible')
    page.wait_for_timeout(300)

    # Make sure we're in Tree View
    view_btn = page.locator('#view-toggle')
    if view_btn.inner_text() == 'Tree View':
        view_btn.click()
        page.wait_for_timeout(100)

    page.fill('#bracket-input', '')
    page.fill('#bracket-input', bracket)
    page.wait_for_timeout(1000)

    status = page.locator('#bracket-status').inner_text()
    if 'error' in status.lower():
        # Retry
        page.fill('#bracket-input', '')
        page.wait_for_timeout(200)
        page.fill('#bracket-input', bracket)
        page.wait_for_timeout(1000)
        status = page.locator('#bracket-status').inner_text()

    if 'error' in status.lower():
        print(f"    BRACKET ERROR: {status}")
        return False

    data_url = page.evaluate(f"""
        async () => {{
            await new Promise(r => setTimeout(r, 200));
            return await window.canvasManager.exportPNG({EXPORT_MULTIPLIER});
        }}
    """)
    save_data_url_as_png(data_url, output_path)
    return True


def generate_table(page, url, bracket, roles, output_path):
    """Generate a labeling table PNG with roles filled."""
    page.goto(url)
    page.wait_for_selector('#bracket-input', state='visible')
    page.wait_for_timeout(300)

    # Start in Tree View
    view_btn = page.locator('#view-toggle')
    if view_btn.inner_text() == 'Tree View':
        view_btn.click()
        page.wait_for_timeout(100)

    page.fill('#bracket-input', '')
    page.fill('#bracket-input', bracket)
    page.wait_for_timeout(600)

    # Switch to Table View
    view_btn = page.locator('#view-toggle')
    if view_btn.inner_text() == 'Table View':
        view_btn.click()
        page.wait_for_timeout(400)

    page.wait_for_selector('.labeling-table', state='visible')
    page.wait_for_timeout(200)

    if roles:
        fill_roles_via_dom(page, roles)

    table = page.locator('.labeling-table')
    table.screenshot(path=str(output_path), type='png')
    return True


def load_canonical():
    """Load all canonical PPT JSONs from data/trees/ppt/ keyed by id.

    Falls back to legacy ROLE_ASSIGNMENTS only if a canonical file is absent
    (with a warning). The canonical schema is the single source of truth for
    bracket + roles; ppt_diagram_data.json provides slide mappings only.
    """
    out = {}
    for f in sorted(CANONICAL_DIR.glob("*.json")):
        out[f.stem] = json.loads(f.read_text())
    return out


def main():
    with open(DATA_FILE) as f:
        data = json.load(f)

    canonical = load_canonical()
    sentences = data["sentences"]
    total = len(sentences)

    print("=" * 60)
    print(f"PPT Diagram Generator: {total} sentences x 2 (table + tree) = {total * 2} PNGs")
    print(f"Canonical entries loaded: {len(canonical)}")
    missing = [s["id"] for s in sentences if s["id"] not in canonical]
    if missing:
        print(f"WARNING: no canonical for: {', '.join(missing)} — will use legacy ROLE_ASSIGNMENTS")
    print("=" * 60)

    httpd = start_server()
    time.sleep(1)

    url = f"http://localhost:{PORT}/index.html"
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1600, "height": 900})

        for i, s in enumerate(sentences):
            sid = s["id"]
            if sid in canonical:
                bracket = canonical[sid]["bracket"]
                roles = canonical[sid]["roles"]
            else:
                bracket = s["bracket"]
                roles = ROLE_ASSIGNMENTS.get(sid, {})

            print(f"\n[{i+1}/{total}] {sid}: {s['sentence'][:60]}...")

            # Generate tree
            tree_path = TREE_DIR / f"{sid}.png"
            ok = generate_tree(page, url, bracket, tree_path)
            if ok:
                print(f"  Tree: OK -> {tree_path.name}")
            else:
                print(f"  Tree: FAILED")
            results.append((f"{sid}_tree", ok))

            time.sleep(0.3)

            # Generate table
            table_path = TABLE_DIR / f"{sid}.png"
            ok = generate_table(page, url, bracket, roles, table_path)
            if ok:
                print(f"  Table: OK -> {table_path.name}")
            else:
                print(f"  Table: FAILED")
            results.append((f"{sid}_table", ok))

            time.sleep(0.3)

        browser.close()

    httpd.shutdown()

    passed = sum(1 for _, ok in results if ok)
    failed = [n for n, ok in results if not ok]
    print(f"\nDone: {passed}/{len(results)} succeeded")
    if failed:
        print(f"FAILED: {', '.join(failed)}")


if __name__ == "__main__":
    main()
