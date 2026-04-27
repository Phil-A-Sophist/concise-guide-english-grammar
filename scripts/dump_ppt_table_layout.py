#!/usr/bin/env python3
"""Dump the actual rendered Role-row layout for each PPT sentence bracket.

Output: data/static/ppt-table-layouts.json
{
  "<sid>": {
    "bracket": "...",
    "words": ["The", "very", ...],
    "pos": ["DET", "ADV", ...],
    "role_rows": [
      {"level": 0, "cells": [{"start": 0, "span": 4, "phrase": "NP"}, ...]},
      ...
    ]
  }
}

Renders each bracket in SyntaxTreeHybrid Table View, then walks the DOM:
- Reads Word and POS rows for terminal columns
- For each Role row, captures contentEditable cell start columns + their colSpan
- Reads the immediately following Phrase row to attach phrase type per role cell

This output is the input for canonical role authoring.
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

sys.stdout.reconfigure(line_buffering=True)

PROJECT_ROOT = Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "static" / "ppt_diagram_data.json"
OUT_FILE = PROJECT_ROOT / "data" / "static" / "ppt-table-layouts.json"
STH_DIR = Path("C:/Users/irphy/Documents/SyntaxTreeHybrid")
PORT = 8086


DUMP_JS = '''
() => {
    const table = document.querySelector('.labeling-table');
    if (!table) return null;
    const rows = Array.from(table.querySelectorAll('tr'));

    function spans(cells) {
        const out = [];
        let col = 0;
        for (const cell of cells) {
            const cs = cell.colSpan || 1;
            out.push({
                start: col,
                span: cs,
                text: cell.textContent.trim(),
                editable: cell.contentEditable === 'true',
            });
            col += cs;
        }
        return out;
    }

    let words = [];
    let pos = [];
    const phraseRows = [];
    const roleRows = [];
    let lastWasRole = false;
    let pendingRoleIdx = -1;

    for (const row of rows) {
        const th = row.querySelector('th');
        const headerText = th ? th.textContent.trim() : '';
        const cells = Array.from(row.querySelectorAll('td'));
        const data = spans(cells);

        if (headerText === 'Word') {
            words = data.map(d => d.text);
        } else if (headerText === 'POS') {
            pos = data.map(d => d.text);
        } else if (headerText.startsWith('Role')) {
            roleRows.push({ level: roleRows.length, cells: data });
            pendingRoleIdx = roleRows.length - 1;
        } else if ((headerText === 'Phrase' || headerText === 'Clause') && pendingRoleIdx >= 0) {
            phraseRows.push({ forRole: pendingRoleIdx, cells: data });
            pendingRoleIdx = -1;
        }
    }

    // Attach phrase types to each role cell by matching start column
    for (const pr of phraseRows) {
        const role = roleRows[pr.forRole];
        for (const rc of role.cells) {
            const match = pr.cells.find(c => c.start === rc.start);
            rc.phrase = match ? match.text : '';
        }
    }

    return { words, pos, role_rows: roleRows };
}
'''


def start_server():
    os.chdir(str(STH_DIR))
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *args: None
    httpd = socketserver.TCPServer(("", PORT), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    print(f"[SERVER] SyntaxTreeHybrid on http://localhost:{PORT}")
    return httpd


def dump_one(page, url, sid, bracket):
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

    layout = page.evaluate(DUMP_JS)
    return layout


def main():
    with open(DATA_FILE) as f:
        data = json.load(f)

    sentences = data["sentences"]
    print(f"Dumping layouts for {len(sentences)} sentences")

    httpd = start_server()
    time.sleep(1)
    url = f"http://localhost:{PORT}/index.html"

    out = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 900})

        for i, s in enumerate(sentences):
            sid = s["id"]
            bracket = s["bracket"]
            print(f"[{i+1}/{len(sentences)}] {sid}")
            try:
                layout = dump_one(page, url, sid, bracket)
                if layout:
                    out[sid] = {"bracket": bracket, **layout}
                else:
                    print(f"  WARN: empty layout")
            except Exception as e:
                print(f"  ERROR: {e}")

        browser.close()
    httpd.shutdown()

    OUT_FILE.write_text(json.dumps(out, indent=2))
    print(f"\nWrote {OUT_FILE}")


if __name__ == "__main__":
    main()
