#!/usr/bin/env python3
"""Regenerate ALL Ch09 table PNGs by typing roles directly into SyntaxTreeHybrid cells.
Also generates the new compound VP tree diagram.
Requires: SyntaxTreeHybrid running on localhost:8080
"""
import json
import time
import base64
from pathlib import Path
from playwright.sync_api import sync_playwright

ASSETS_DIR = Path(__file__).parent.parent / 'assets' / 'diagrams' / 'new'
JSON_PATH = Path(__file__).parent.parent / 'data' / 'static' / 'table-roles' / 'ch09_tables.json'
PORT = 8080
URL = f'http://localhost:{PORT}/index.html'


def fill_roles_via_dom(page, roles_dict):
    """Fill role cells by setting textContent via JS evaluate.
    Searches ALL depth levels for each cell's word position to handle
    depth indexing mismatches between JSON and SyntaxTreeHybrid DOM.
    roles_dict: {"0": {"0": "Main", "2": "Adverbial"}, "1": {...}, ...}
    """
    page.evaluate('''
        (rolesDict) => {
            const table = document.querySelector('.labeling-table');
            if (!table) return;
            // Build a flat map: position -> role (first match across depths)
            // But respect depth ordering: try to match by role row index first
            const rows = table.querySelectorAll('tr');
            let roleIndex = 0;
            rows.forEach((row) => {
                const header = row.querySelector('th');
                if (!header || !header.textContent.trim().startsWith('Role')) return;
                const cells = row.querySelectorAll('td');
                let pos = 0;
                cells.forEach((cell) => {
                    if (cell.contentEditable === 'true') {
                        // First try matching depth to roleIndex
                        let role = (rolesDict[String(roleIndex)] || {})[String(pos)];
                        // If no match, search only DEEPER depths (prevent shallow roles leaking down)
                        if (!role) {
                            for (let d = roleIndex + 1; d < 10; d++) {
                                if (rolesDict[String(d)] && rolesDict[String(d)][String(pos)]) {
                                    role = rolesDict[String(d)][String(pos)];
                                    break;
                                }
                            }
                        }
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


def click_and_type_roles(page, roles_dict):
    """Fallback: click each role cell and type via keyboard."""
    role_info = page.evaluate('''
        () => {
            const table = document.querySelector('.labeling-table');
            if (!table) return [];
            const rows = Array.from(table.querySelectorAll('tr'));
            let result = [];
            let roleIndex = 0;
            for (const row of rows) {
                const header = row.querySelector('th');
                if (!header || !header.textContent.trim().startsWith('Role')) continue;
                const cells = Array.from(row.querySelectorAll('td'));
                let pos = 0;
                for (let ci = 0; ci < cells.length; ci++) {
                    const cell = cells[ci];
                    const cs = cell.colSpan || 1;
                    if (cell.contentEditable === 'true') {
                        // Get bounding box for clicking
                        const rect = cell.getBoundingClientRect();
                        result.push({
                            depth: roleIndex,
                            startPos: pos,
                            x: rect.x + rect.width / 2,
                            y: rect.y + rect.height / 2
                        });
                    }
                    pos += cs;
                }
                roleIndex++;
            }
            return result;
        }
    ''')

    for cell_info in role_info:
        depth = str(cell_info['depth'])
        pos = str(cell_info['startPos'])
        if depth in roles_dict and pos in roles_dict[depth]:
            role_text = roles_dict[depth][pos]
            page.mouse.click(cell_info['x'], cell_info['y'])
            page.wait_for_timeout(50)
            page.keyboard.type(role_text)
            page.wait_for_timeout(50)

    page.wait_for_timeout(200)


def generate_table(page, bracket, roles, filename, output_dir, use_click=True):
    """Generate a table PNG via SyntaxTreeHybrid."""
    # Switch to Tree View first so bracket input triggers sync
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

    # Fill roles via DOM (reliable) — click approach has coordinate issues with merged cells
    if roles:
        fill_roles_via_dom(page, roles)
    else:
        # Clear auto-generated role content AND hide ::before placeholder for blank homework tables
        page.evaluate('''
            () => {
                const table = document.querySelector('.labeling-table');
                if (!table) return;
                table.querySelectorAll('td.role').forEach(cell => {
                    cell.textContent = '';
                    cell.contentEditable = 'false';
                });
                // Inject style to hide ::before placeholder on non-editable role cells
                const style = document.createElement('style');
                style.textContent = 'td.role[contenteditable="false"]::before { content: none !important; }';
                document.head.appendChild(style);
            }
        ''')
        page.wait_for_timeout(100)

    # Screenshot
    table = page.locator('.labeling-table')
    out_path = output_dir / f'{filename}.png'
    table.screenshot(path=str(out_path), type='png')
    print(f'  {filename}.png')


def generate_tree(page, bracket, filename, output_dir):
    """Generate a tree diagram PNG."""
    page.goto(URL)
    page.wait_for_selector('#bracket-input', state='visible')
    time.sleep(0.3)

    # Make sure we're in tree view
    view_btn = page.locator('#view-toggle')
    if view_btn.inner_text() == 'Tree View':
        view_btn.click()
        page.wait_for_timeout(100)

    page.fill('#bracket-input', bracket)
    time.sleep(0.8)

    page.click('#zoom-fit')
    time.sleep(0.3)

    data_url = page.evaluate("""
        async () => { return await window.canvasManager.exportPNG(4); }
    """)

    if data_url and data_url.startswith('data:image/png;base64,'):
        base64_data = data_url.split(',', 1)[1]
        png_data = base64.b64decode(base64_data)
        out_path = output_dir / f'{filename}.png'
        with open(out_path, 'wb') as f:
            f.write(png_data)
        print(f'  {filename}.png ({len(png_data):,} bytes)')
    else:
        print(f'  ERROR: No PNG data for {filename}')


def main():
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    # Load roles from JSON
    data = json.loads(JSON_PATH.read_text(encoding='utf-8'))
    entries = {s['filename']: s for s in data['sentences']}

    # Textbook tables (with roles)
    textbook_tables = [
        'ch09_table_001', 'ch09_table_002', 'ch09_table_003',
        'ch09_table_004', 'ch09_table_005', 'ch09_table_006',
        'ch09_table_007', 'ch09_table_008', 'ch09_table_009',
        'ch09_table_010', 'ch09_table_011', 'ch09_table_012',
    ]

    # Homework tables (NO roles - blank)
    homework_tables = [
        'ch09_hw_001', 'ch09_hw_002', 'ch09_hw_003', 'ch09_hw_004',
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1400, 'height': 900})
        page.goto(URL)
        page.wait_for_selector('#bracket-input', state='visible')

        print('Generating textbook table PNGs (with roles)...')
        for name in textbook_tables:
            entry = entries[name]
            generate_table(page, entry['bracket'], entry['roles'],
                           name, ASSETS_DIR, use_click=True)

        print('\nGenerating homework table PNGs (blank roles)...')
        for name in homework_tables:
            entry = entries[name]
            # Use filename ch09_hw_student_NNN for the PreTeXt homework
            student_name = name.replace('ch09_hw_', 'ch09_hw_student_')
            generate_table(page, entry['bracket'], {},
                           student_name, ASSETS_DIR, use_click=False)

        print('\nGenerating tree diagrams...')
        # New compound VP tree
        generate_tree(page,
            '[S [NP [DET The] [N dog]] [VP [VP [V barked]] [CONJ and] [VP [V chased] [NP [DET the] [N squirrel]]]]]',
            'ch09_compound_vp', ASSETS_DIR)
        # Regenerate compound simple tree (in case it needs update)
        generate_tree(page,
            '[S [IC [NP [PRON It]] [VP [V rained]]] [CONJ and] [IC [NP [PRON we]] [VP [V stayed] [ADVP [ADV inside]]]]]',
            'ch09_compound_simple', ASSETS_DIR)

        browser.close()

    print('\nDone. All Ch09 PNGs regenerated.')


if __name__ == '__main__':
    main()
