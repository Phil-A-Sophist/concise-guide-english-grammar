#!/usr/bin/env python3
"""Spot-check verification: render a sentence's table with canonical roles applied,
then read back and print every Role row's filled cells. Exits non-zero if any
editable cell is left blank.
"""
import json
import sys
import os
import time
import threading
import http.server
import socketserver
from pathlib import Path

from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).parent.parent
CANONICAL_DIR = PROJECT_ROOT / "data" / "trees" / "ppt"
STH_DIR = Path("C:/Users/irphy/Documents/SyntaxTreeHybrid")
PORT = 8087

CHECK = sys.argv[1:] or ["adj_04", "adj_05", "adj_06", "adj_10_preview", "adj_11_preview", "adj_12_preview"]

FILL_AND_READ_JS = '''
(rolesDict) => {
    const table = document.querySelector('.labeling-table');
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
                if (role) cell.textContent = role;
            }
            pos += (cell.colSpan || 1);
        });
        roleIndex++;
    });
    // Read back
    const out = [];
    let lvl = 0;
    rows.forEach((row) => {
        const header = row.querySelector('th');
        if (!header || !header.textContent.trim().startsWith('Role')) return;
        const cells = row.querySelectorAll('td');
        let pos = 0;
        const lvlOut = { level: lvl, cells: [] };
        cells.forEach((cell) => {
            if (cell.contentEditable === 'true') {
                lvlOut.cells.push({ start: pos, span: cell.colSpan || 1, text: cell.textContent.trim() });
            }
            pos += (cell.colSpan || 1);
        });
        out.push(lvlOut);
        lvl++;
    });
    return out;
}
'''


def start_server():
    os.chdir(str(STH_DIR))
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *a: None
    httpd = socketserver.TCPServer(("", PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def main():
    httpd = start_server()
    time.sleep(1)
    url = f"http://localhost:{PORT}/index.html"

    blanks_found = False
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 900})

        for sid in CHECK:
            canonical = json.loads((CANONICAL_DIR / f"{sid}.json").read_text())
            bracket = canonical["bracket"]
            roles = canonical["roles"]

            page.goto(url)
            page.wait_for_selector('#bracket-input', state='visible')
            page.wait_for_timeout(300)
            view_btn = page.locator('#view-toggle')
            if view_btn.inner_text() == 'Tree View':
                view_btn.click()
                page.wait_for_timeout(100)
            page.fill('#bracket-input', '')
            page.fill('#bracket-input', bracket)
            page.wait_for_timeout(600)
            view_btn = page.locator('#view-toggle')
            if view_btn.inner_text() == 'Table View':
                view_btn.click()
                page.wait_for_timeout(400)
            page.wait_for_selector('.labeling-table', state='visible')
            page.wait_for_timeout(200)

            result = page.evaluate(FILL_AND_READ_JS, roles)
            print(f"=== {sid} ===")
            for r in result:
                cells_str = ", ".join(f"col{c['start']}({c['span']})={c['text']!r}" for c in r['cells'])
                print(f"  L{r['level']}: {cells_str}")
                for c in r['cells']:
                    if not c['text']:
                        print(f"    !! BLANK at L{r['level']} col {c['start']}")
                        blanks_found = True

        browser.close()
    httpd.shutdown()
    sys.exit(1 if blanks_found else 0)


if __name__ == "__main__":
    main()
