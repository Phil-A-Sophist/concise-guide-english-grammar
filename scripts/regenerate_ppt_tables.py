#!/usr/bin/env python3
"""Regenerate PPT table PNGs with complete role assignments.

For each sentence:
1. Enter bracket in SyntaxTreeHybrid
2. Switch to Table View
3. Read the table DOM to understand structure
4. Fill ALL role cells using intelligent assignment based on phrase/POS context
5. Screenshot

Uses the same HTTP server + Playwright pattern as other generators.
"""

import json
import sys
import os
import time
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
TABLE_DIR = PROJECT_ROOT / "data" / "static" / "ppt-diagrams" / "tables"
STH_DIR = Path("C:/Users/irphy/Documents/SyntaxTreeHybrid")
PORT = 8085

TABLE_DIR.mkdir(parents=True, exist_ok=True)

# Complete role assignments for all 23 sentences.
# Keys: sentence_id -> list of (role_row_index, cell_index_within_row, role_label)
# These are authored by reading the rendered table structure.
# We'll use a JS-based approach that reads phrase labels and assigns roles automatically.

ROLE_FILL_JS = '''
(manualOverrides) => {
    const table = document.querySelector('.labeling-table');
    if (!table) return 'no table found';

    const rows = Array.from(table.querySelectorAll('tr'));

    // Collect row types and data
    const rowData = [];
    for (const row of rows) {
        const header = row.querySelector('th');
        const headerText = header ? header.textContent.trim() : '';
        const cells = Array.from(row.querySelectorAll('td'));
        rowData.push({ headerText, cells, row });
    }

    // Find Role rows and their paired Phrase/Clause rows
    const rolePhraseRows = [];
    for (let i = 0; i < rowData.length; i++) {
        if (rowData[i].headerText.startsWith('Role')) {
            const phraseRow = (i + 1 < rowData.length) ? rowData[i + 1] : null;
            rolePhraseRows.push({
                roleRow: rowData[i],
                phraseRow: phraseRow,
                level: rolePhraseRows.length,
            });
        }
    }

    // Find the Word row to get actual words
    let wordCells = [];
    for (const rd of rowData) {
        if (rd.headerText === 'Word') {
            wordCells = rd.cells.map(c => c.textContent.trim());
        }
    }

    // Find POS row
    let posCells = [];
    for (const rd of rowData) {
        if (rd.headerText === 'POS') {
            posCells = rd.cells.map(c => c.textContent.trim());
        }
    }

    // Build a column map: for each role cell, what column span does it cover?
    function getCellSpans(cells) {
        const spans = [];
        let col = 0;
        for (const cell of cells) {
            const colspan = cell.colSpan || 1;
            spans.push({ cell, startCol: col, endCol: col + colspan - 1, text: cell.textContent.trim() });
            col += colspan;
        }
        return spans;
    }

    // Linking verbs for SC detection
    const linkingVerbs = new Set([
        'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
        'seems', 'seem', 'seemed', 'becomes', 'become', 'became',
        'appears', 'appear', 'appeared', 'feels', 'feel', 'felt',
        'looks', 'look', 'looked', 'sounds', 'sound', 'sounded',
        'tastes', 'taste', 'tasted', 'smells', 'smell', 'smelled',
        'remains', 'remain', 'remained'
    ]);

    // Complex transitive verbs (S+V+DO+OC)
    const complexTransVerbs = new Set([
        'considered', 'consider', 'declared', 'declare', 'named', 'name',
        'elected', 'elect', 'appointed', 'appoint', 'called', 'call',
        'made', 'make', 'found', 'find'
    ]);

    // Get the main verb from a VP span
    function getMainVerb(startCol, endCol) {
        for (let c = startCol; c <= endCol; c++) {
            if (c < posCells.length && posCells[c] === 'V') {
                return wordCells[c] ? wordCells[c].toLowerCase() : '';
            }
        }
        return '';
    }

    // Check if VP is copular
    function isCopularVP(startCol, endCol) {
        const verb = getMainVerb(startCol, endCol);
        return linkingVerbs.has(verb);
    }

    function isComplexTrans(startCol, endCol) {
        const verb = getMainVerb(startCol, endCol);
        return complexTransVerbs.has(verb);
    }

    let filled = 0;

    // Process each level
    for (const { roleRow, phraseRow, level } of rolePhraseRows) {
        if (!phraseRow) continue;

        const roleSpans = getCellSpans(roleRow.cells);
        const phraseSpans = getCellSpans(phraseRow.cells);

        // For each role cell, find the matching phrase cell
        for (const roleSpan of roleSpans) {
            const cell = roleSpan.cell;
            if (cell.contentEditable !== 'true') continue;
            if (cell.textContent.trim() && cell.textContent.trim() !== '...') continue;

            // Find matching phrase span
            let phraseType = '';
            for (const ps of phraseSpans) {
                if (ps.startCol === roleSpan.startCol) {
                    phraseType = ps.text;
                    break;
                }
            }

            if (!phraseType) continue;

            // Determine role based on level and phrase type
            let role = '';

            if (level === 0) {
                // Top level: S children
                if (phraseType === 'NP') {
                    // Check if this NP is before or after the VP
                    let hasVPBefore = false;
                    for (const ps of phraseSpans) {
                        if (ps.text === 'VP' && ps.startCol < roleSpan.startCol) {
                            hasVPBefore = true;
                        }
                    }
                    if (hasVPBefore) {
                        role = 'Subject'; // post-VP NP in inverted order
                    } else {
                        role = 'Subject';
                    }
                } else if (phraseType === 'VP') {
                    role = 'Predicate';
                } else if (phraseType === 'S') {
                    // Embedded S at top level = nominal (subject or predicate)
                    // Check position relative to VP
                    let vpFound = false;
                    for (const ps of phraseSpans) {
                        if (ps.text === 'VP' && ps.startCol > roleSpan.startCol) {
                            vpFound = true;
                        }
                    }
                    if (vpFound || roleSpan.startCol === 0) {
                        role = 'Subject';
                    }
                } else if (phraseType === 'IC') {
                    role = 'Main';
                } else if (phraseType === 'DC') {
                    role = 'Adverbial';
                }
            } else {
                // Deeper levels: context-dependent
                // Find parent context by looking at the level above
                let parentPhrase = '';
                if (level > 0 && rolePhraseRows[level - 1]) {
                    const parentPhraseSpans = getCellSpans(rolePhraseRows[level - 1].phraseRow.cells);
                    for (const pps of parentPhraseSpans) {
                        if (pps.startCol <= roleSpan.startCol && pps.endCol >= roleSpan.endCol) {
                            parentPhrase = pps.text;
                            break;
                        }
                    }
                }

                if (parentPhrase === 'NP' || parentPhrase === '') {
                    // Inside NP
                    if (phraseType === 'ADJP' || phraseType === 'VP' || phraseType === 'S') {
                        role = 'Adjectival';
                    } else if (phraseType === 'PP') {
                        role = 'Adjectival';
                    } else if (phraseType === 'NP') {
                        role = 'Adjectival'; // nested NP modifier
                    }
                } else if (parentPhrase === 'VP') {
                    // Inside VP
                    if (phraseType === 'NP') {
                        // Count how many NP siblings are in this VP level
                        const vpParent = phraseSpans.find(ps =>
                            ps.text === 'VP' && ps.startCol <= roleSpan.startCol && ps.endCol >= roleSpan.endCol
                        );
                        // Find all NP siblings at this level within the VP
                        const npSiblings = roleSpans.filter(rs => {
                            const matchPhrase = phraseSpans.find(ps => ps.startCol === rs.startCol);
                            return matchPhrase && matchPhrase.text === 'NP';
                        });

                        const vpStart = vpParent ? vpParent.startCol : 0;
                        const vpEnd = vpParent ? vpParent.endCol : 999;
                        const vpNPs = npSiblings.filter(rs => rs.startCol >= vpStart && rs.endCol <= vpEnd);

                        if (isCopularVP(vpStart, vpEnd)) {
                            role = 'Subject Complement';
                        } else if (isComplexTrans(vpStart, vpEnd) && vpNPs.length >= 2) {
                            // First NP = DO, second = OC
                            const idx = vpNPs.indexOf(vpNPs.find(n => n.startCol === roleSpan.startCol));
                            role = idx === 0 ? 'Direct Object' : 'Object Complement';
                        } else if (vpNPs.length >= 2 && !isComplexTrans(vpStart, vpEnd)) {
                            const idx = vpNPs.indexOf(vpNPs.find(n => n.startCol === roleSpan.startCol));
                            role = idx === 0 ? 'Indirect Object' : 'Direct Object';
                        } else {
                            role = 'Direct Object';
                        }
                    } else if (phraseType === 'ADJP') {
                        // Check if there's an NP before it (OC) or copular (SC)
                        const vpParent = phraseSpans.find(ps =>
                            ps.text === 'VP' && ps.startCol <= roleSpan.startCol && ps.endCol >= roleSpan.endCol
                        );
                        const vpStart = vpParent ? vpParent.startCol : 0;
                        const vpEnd = vpParent ? vpParent.endCol : 999;

                        if (isCopularVP(vpStart, vpEnd)) {
                            role = 'Subject Complement';
                        } else {
                            // Check if preceded by NP (OC pattern)
                            let npBefore = false;
                            for (const ps of phraseSpans) {
                                if (ps.text === 'NP' && ps.endCol < roleSpan.startCol && ps.startCol >= vpStart) {
                                    npBefore = true;
                                }
                            }
                            role = npBefore ? 'Object Complement' : 'Subject Complement';
                        }
                    } else if (phraseType === 'PP') {
                        role = 'Adverbial';
                    } else if (phraseType === 'ADVP') {
                        role = 'Adverbial';
                    } else if (phraseType === 'VP') {
                        role = 'Direct Object'; // infinitive/gerund as DO
                    } else if (phraseType === 'S') {
                        role = 'Direct Object'; // complement clause as DO
                    }
                } else if (parentPhrase === 'PP') {
                    if (phraseType === 'NP') {
                        role = 'Obj Prep';
                    }
                } else if (parentPhrase === 'S') {
                    // Inside embedded clause
                    if (phraseType === 'NP') {
                        // Check position: before VP = Subject, after V = object
                        let vpAfter = false;
                        for (const ps of phraseSpans) {
                            if (ps.text === 'VP' && ps.startCol > roleSpan.startCol) {
                                vpAfter = true;
                            }
                        }
                        role = vpAfter ? 'Subject' : 'Direct Object';
                    } else if (phraseType === 'VP') {
                        role = 'Predicate';
                    }
                }
            }

            // Apply manual overrides if present
            const overrideKey = level + '_' + roleSpan.startCol;
            if (manualOverrides && manualOverrides[overrideKey]) {
                role = manualOverrides[overrideKey];
            }

            if (role) {
                cell.textContent = role;
                filled++;
            }
        }
    }

    return 'Filled ' + filled + ' role cells';
}
'''

# Manual overrides for cases the auto-filler gets wrong
# Format: { sentence_id: { "level_startCol": "role" } }
MANUAL_OVERRIDES = {
    "adv_01": {
        "1_5": "Adverbial",  # participial VP "escaping..." = adverbial, not DO
    },
    "adv_02": {
        "0_0": "Adverbial",  # infinitive VP at start = adverbial, not subject
        "0_3": "Subject",    # Bob = subject
        "0_4": "Predicate",  # bought = predicate
        "1_1": "Direct Object",  # "his plant" = DO of infinitive, not IO
    },
    "adv_03": {
        "0_0": "Adverbial",  # "One morning" = adverbial NP
        "0_3": "Subject",    # "I" = subject
        "0_4": "Predicate",  # "ate" = predicate
    },
    "nom_01": {
        "0_0": "Subject",    # gerund VP "Applying to jobs" = subject
    },
    "nom_05": {
        "0_0": "Subject",    # complement clause "How I feel" = subject
    },
    "adj_11_preview": {
        "0_0": "Subject",    # complement clause "Who will win" = subject
    },
    "adj_12_preview": {
        "1_2": "Direct Object",  # complement clause "my family is cursed" = DO
        "3_4": "Predicate",      # "is cursed" = predicate inside embedded clause
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


def generate_table(page, url, sid, bracket, overrides):
    """Generate a single table PNG with complete roles."""
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

    # Fill roles
    result = page.evaluate(ROLE_FILL_JS, overrides or {})
    print(f"    {result}")
    page.wait_for_timeout(200)

    # Screenshot
    table = page.locator('.labeling-table')
    out_path = TABLE_DIR / f"{sid}.png"
    table.screenshot(path=str(out_path), type='png')
    return out_path


def main():
    with open(DATA_FILE) as f:
        data = json.load(f)

    sentences = data["sentences"]
    total = len(sentences)

    print("=" * 60)
    print(f"PPT Table Regenerator: {total} tables with complete roles")
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
            bracket = s["bracket"]
            overrides = MANUAL_OVERRIDES.get(sid, {})

            print(f"\n[{i+1}/{total}] {sid}: {s['sentence'][:60]}...")

            try:
                out = generate_table(page, url, sid, bracket, overrides)
                print(f"    Saved: {out.name}")
                results.append((sid, True))
            except Exception as e:
                print(f"    ERROR: {e}")
                results.append((sid, False))

            time.sleep(0.3)

        browser.close()

    httpd.shutdown()

    passed = sum(1 for _, ok in results if ok)
    failed = [n for n, ok in results if not ok]
    print(f"\nDone: {passed}/{total} succeeded")
    if failed:
        print(f"FAILED: {', '.join(failed)}")


if __name__ == "__main__":
    main()
