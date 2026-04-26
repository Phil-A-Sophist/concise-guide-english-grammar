#!/usr/bin/env python3
"""Regenerate ALL labeling table PNGs across Ch05-15 via SyntaxTreeHybrid + Playwright.

Content tables: roles filled via DOM textContent injection from JSON role files.
Homework student tables: Role, Phrase, and POS rows all cleared (only Word row + headers).

Requires: SyntaxTreeHybrid directory available (starts its own HTTP server).
Uses auto-assign fallback for any roles not in JSON.

Usage:
    python scripts/regenerate_all_table_pngs.py [--chapters 5 6 7] [--port 8080]
"""

import argparse
import json
import sys
import time
import threading
import http.server
import socketserver
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = REPO_ROOT / 'assets' / 'diagrams' / 'new'
JSON_DIR = REPO_ROOT / 'data' / 'static' / 'table-roles'
SYNTAXTREE_DIR = Path('C:/Users/irphy/Documents/SyntaxTreeHybrid')

# Add scripts/ to path for auto-assign fallback
sys.path.insert(0, str(REPO_ROOT / 'scripts'))


def start_server(port):
    """Start a simple HTTP server for SyntaxTreeHybrid in a background thread."""
    os.chdir(str(SYNTAXTREE_DIR))
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *args: None  # suppress logs
    httpd = socketserver.TCPServer(("", port), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    print(f"[SERVER] SyntaxTreeHybrid on http://localhost:{port}")
    return httpd


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


def clear_student_table(page):
    """Clear Role, Phrase, and POS rows for student-mode blank table.
    Only Word row and row headers remain visible."""
    page.evaluate('''
        () => {
            const table = document.querySelector('.labeling-table');
            if (!table) return;

            // Clear role cells
            table.querySelectorAll('td.role').forEach(cell => {
                cell.textContent = '';
                cell.contentEditable = 'false';
            });

            // Clear phrase/clause cells
            table.querySelectorAll('td.phrase, td.clause').forEach(cell => {
                cell.textContent = '';
                cell.contentEditable = 'false';
            });

            // Clear POS cells
            table.querySelectorAll('td.pos').forEach(cell => {
                cell.textContent = '';
                cell.contentEditable = 'false';
            });

            // Hide all ::before placeholders on non-editable cells
            const style = document.createElement('style');
            style.textContent = `
                td.role[contenteditable="false"]::before { content: none !important; }
                td.phrase[contenteditable="false"]::before { content: none !important; }
                td.clause[contenteditable="false"]::before { content: none !important; }
                td.pos[contenteditable="false"]::before { content: none !important; }
            `;
            document.head.appendChild(style);
        }
    ''')
    page.wait_for_timeout(100)


def generate_table_png(page, url, bracket, roles, filename, output_dir, mode='content'):
    """Generate a single table PNG.

    mode='content': fill roles from roles dict (answer key style)
    mode='student': clear all rows except Word (blank for students)
    """
    # Navigate fresh to avoid state leaks
    page.goto(url)
    page.wait_for_selector('#bracket-input', state='visible')
    page.wait_for_timeout(300)

    # Ensure we start in Tree View so bracket input triggers proper parse
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

    if mode == 'student':
        clear_student_table(page)
    elif roles:
        fill_roles_via_dom(page, roles)

    # Screenshot the table
    table = page.locator('.labeling-table')
    out_path = output_dir / f'{filename}.png'
    table.screenshot(path=str(out_path), type='png')
    return out_path


def auto_assign_roles(bracket):
    """Auto-assign roles from bracket notation as fallback."""
    try:
        from assign_table_roles import parse_bracket, assign_roles_to_tree
        tree = parse_bracket(bracket)
        if tree is None:
            return {}
        return assign_roles_to_tree(tree)
    except Exception as e:
        print(f"    WARNING: Auto-assign failed: {e}")
        return {}


def process_chapter(page, url, chapter_num, output_dir):
    """Process all table entries for a single chapter."""
    jp = JSON_DIR / f'ch{chapter_num:02d}_tables.json'
    if not jp.exists():
        print(f"  SKIP: No JSON file for Ch{chapter_num:02d}")
        return 0, 0

    data = json.loads(jp.read_text(encoding='utf-8'))
    entries = data['sentences']

    content_count = 0
    student_count = 0

    for entry in entries:
        filename = entry.get('filename')
        bracket = entry.get('bracket', '')
        roles = entry.get('roles', {})
        skip = entry.get('skip', False)

        if not filename or not bracket or skip:
            continue

        is_homework = 'hw' in filename

        if is_homework:
            # Generate student-mode blank table
            student_filename = filename.replace('_hw_', '_hw_student_')
            generate_table_png(page, url, bracket, {}, student_filename,
                             output_dir, mode='student')
            print(f"    {student_filename}.png (student)")
            student_count += 1
        else:
            # Content table — fill roles, use auto-assign for gaps
            if not roles:
                roles = auto_assign_roles(bracket)
                if roles:
                    print(f"    WARNING: Auto-assigned ALL roles for {filename}")
            else:
                # Merge auto-assign for partial gaps
                auto = auto_assign_roles(bracket)
                if auto:
                    for level_key, level_roles in auto.items():
                        if level_key not in roles:
                            roles[level_key] = level_roles
                        else:
                            for col_key, role_label in level_roles.items():
                                if col_key not in roles[level_key]:
                                    roles[level_key][col_key] = role_label

            generate_table_png(page, url, bracket, roles, filename,
                             output_dir, mode='content')
            print(f"    {filename}.png (content)")
            content_count += 1

    return content_count, student_count


def main():
    parser = argparse.ArgumentParser(description='Regenerate all table PNGs')
    parser.add_argument('--chapters', nargs='+', type=int, default=list(range(5, 16)),
                        help='Chapter numbers to process (default: 5-15)')
    parser.add_argument('--port', type=int, default=8080,
                        help='Port for SyntaxTreeHybrid server (default: 8080)')
    args = parser.parse_args()

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    # Start server
    httpd = start_server(args.port)
    url = f'http://localhost:{args.port}/index.html'
    time.sleep(1)

    total_content = 0
    total_student = 0

    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 1400, 'height': 900})

            for ch in args.chapters:
                print(f"\n=== Chapter {ch:02d} ===")
                c, s = process_chapter(page, url, ch, ASSETS_DIR)
                total_content += c
                total_student += s

            browser.close()

    finally:
        httpd.shutdown()

    print(f"\n=== COMPLETE ===")
    print(f"Content PNGs: {total_content}")
    print(f"Student PNGs: {total_student}")
    print(f"Total: {total_content + total_student}")


if __name__ == '__main__':
    main()
