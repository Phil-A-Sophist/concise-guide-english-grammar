#!/usr/bin/env python3
"""Generate new Ch09 homework table PNGs (student mode, blank roles) and tree diagrams."""
import json, time, base64
from pathlib import Path
from playwright.sync_api import sync_playwright

ASSETS = Path(__file__).parent.parent / 'assets' / 'diagrams' / 'new'
HW_DIAG = Path(__file__).parent.parent / 'Homework' / 'diagrams' / 'ch09'
URL = 'http://localhost:8080/index.html'

HW = [
    {
        'bracket': '[S [NP [NP [DET The] [N teacher]] [CONJ and] [NP [DET the] [N principal]]] [VP [V met] [PP [PREP after] [NP [N school]]]]]',
        'table_file': 'ch09_hw_student_010',
        'tree_file': 'ch09_hw_ex10_teacher_principal',
    },
    {
        'bracket': '[S [IC [NP [DET The] [N train]] [VP [V arrived] [ADVP [ADV late]]]] [CONJ but] [IC [NP [DET the] [N passengers]] [VP [V remained] [AdjP [ADJ calm]]]]]',
        'table_file': 'ch09_hw_student_011',
        'tree_file': 'ch09_hw_ex11_train_passengers',
    },
    {
        'bracket': '[S [DC [SUB Although] [NP [DET the] [N library]] [VP [V was] [AdjP [ADJ quiet]]]] [IC [NP [PRON she]] [VP [AUX could] [ADV not] [V concentrate]]]]',
        'table_file': 'ch09_hw_student_012',
        'tree_file': 'ch09_hw_ex12_library_concentrate',
    },
]

def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    HW_DIAG.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1400, 'height': 900})
        page.goto(URL)
        page.wait_for_selector('#bracket-input', state='visible')

        for entry in HW:
            # Generate student-mode table PNG
            view_btn = page.locator('#view-toggle')
            if view_btn.inner_text() == 'Tree View':
                view_btn.click()
                page.wait_for_timeout(100)
            page.fill('#bracket-input', '')
            page.fill('#bracket-input', entry['bracket'])
            page.wait_for_timeout(600)
            view_btn = page.locator('#view-toggle')
            if view_btn.inner_text() == 'Table View':
                view_btn.click()
                page.wait_for_timeout(400)
            page.wait_for_selector('.labeling-table', state='visible')
            page.wait_for_timeout(200)
            # Clear roles and hide placeholders
            page.evaluate('''() => {
                const table = document.querySelector('.labeling-table');
                if (!table) return;
                table.querySelectorAll('td.role').forEach(c => {
                    c.textContent = '';
                    c.contentEditable = 'false';
                });
                const s = document.createElement('style');
                s.textContent = 'td.role[contenteditable="false"]::before{content:none!important}';
                document.head.appendChild(s);
            }''')
            page.wait_for_timeout(100)
            table = page.locator('.labeling-table')
            table.screenshot(path=str(ASSETS / f'{entry["table_file"]}.png'), type='png')
            print(f'  Table: {entry["table_file"]}.png')

            # Generate tree diagram PNG
            page.goto(URL)
            page.wait_for_selector('#bracket-input', state='visible')
            time.sleep(0.3)
            view_btn = page.locator('#view-toggle')
            if view_btn.inner_text() == 'Tree View':
                view_btn.click()
                page.wait_for_timeout(100)
            page.fill('#bracket-input', entry['bracket'])
            time.sleep(0.8)
            page.click('#zoom-fit')
            time.sleep(0.3)
            data_url = page.evaluate('async () => await window.canvasManager.exportPNG(4)')
            if data_url and data_url.startswith('data:image/png;base64,'):
                png = base64.b64decode(data_url.split(',', 1)[1])
                out = HW_DIAG / f'{entry["tree_file"]}.png'
                with open(out, 'wb') as f:
                    f.write(png)
                print(f'  Tree: {entry["tree_file"]}.png ({len(png):,} bytes)')

        browser.close()
    print('\nDone.')

if __name__ == '__main__':
    main()
