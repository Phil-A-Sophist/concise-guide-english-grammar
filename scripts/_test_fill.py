"""Quick test: fill roles into SyntaxTreeHybrid table and dump results."""
import time, threading, http.server, socketserver, os, json
from pathlib import Path
from playwright.sync_api import sync_playwright

PORT = 8084
STH = Path('C:/Users/irphy/Documents/SyntaxTreeHybrid')

def start_server():
    os.chdir(str(STH))
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *a: None
    with socketserver.TCPServer(('', PORT), handler) as h:
        h.serve_forever()

threading.Thread(target=start_server, daemon=True).start()
time.sleep(1)

bracket = '[S [NP [PRON He]] [VP [V works] [PP [PREP in] [NP [DET the] [N city]]]]]'
roles = {"0": {"0": "Subject", "1": "Predicate"}, "1": {"2": "Adverbial"}, "2": {"3": "Obj Prep"}}

FILL_JS = """(rolesDict) => {
    const table = document.querySelector('.labeling-table');
    if (!table) return 'no table';
    const rows = table.querySelectorAll('tr');
    let roleIndex = 0;
    let log = [];
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
                log.push('roleIndex=' + roleIndex + ' pos=' + pos + ' role=' + (role || 'NONE') + ' editable=true');
                if (role) { cell.textContent = role; }
            } else {
                log.push('roleIndex=' + roleIndex + ' pos=' + pos + ' SKIPPED editable=' + cell.contentEditable);
            }
            pos += (cell.colSpan || 1);
        });
        roleIndex++;
    });
    return log.join('|');
}"""

DUMP_JS = """() => {
    const table = document.querySelector('.labeling-table');
    const rows = table.querySelectorAll('tr');
    let out = [];
    rows.forEach(row => {
        const th = row.querySelector('th');
        if (!th) return;
        const cells = Array.from(row.querySelectorAll('td'));
        let pos = 0;
        let info = [];
        for (const c of cells) {
            info.push(pos + ':' + JSON.stringify(c.textContent.trim()) + '(' + c.contentEditable + ',cs=' + c.colSpan + ')');
            pos += (c.colSpan || 1);
        }
        out.push(th.textContent.trim() + ' => ' + info.join(' | '));
    });
    return out;
}"""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page(viewport={'width': 1400, 'height': 900})
    url = f'http://localhost:{PORT}/index.html'
    page.goto(url)
    page.wait_for_selector('#bracket-input', state='visible')
    time.sleep(0.3)

    view_btn = page.locator('#view-toggle')
    if view_btn.inner_text() == 'Tree View':
        view_btn.click()
        time.sleep(0.1)

    page.fill('#bracket-input', bracket)
    time.sleep(0.6)

    view_btn = page.locator('#view-toggle')
    if view_btn.inner_text() == 'Table View':
        view_btn.click()
        time.sleep(0.4)

    page.wait_for_selector('.labeling-table', state='visible')
    time.sleep(0.2)

    # Fill and log
    log = page.evaluate(FILL_JS, roles)
    print("=== FILL LOG ===")
    for entry in log.split('|'):
        print(' ', entry)

    time.sleep(0.3)

    # Dump final state
    print("\n=== TABLE STATE ===")
    rows = page.evaluate(DUMP_JS)
    for row in rows:
        print(' ', row)

    # Screenshot
    table = page.locator('.labeling-table')
    table.screenshot(path='test_fill.png', type='png')
    print('\nSaved test_fill.png')
    browser.close()
