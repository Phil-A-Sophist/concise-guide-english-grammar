#!/usr/bin/env python3
"""Audit 1:1 pairing of labeling tables and tree diagrams in completed examples.

Scans PreTeXt source files for completed examples (content sections and homework
"Example (completed)" blocks) and verifies each has BOTH a labeling table AND a
tree diagram image.

Does NOT flag homework exercises — students draw their own diagrams.

Usage:
    python scripts/audit_table_diagram_pairs.py
"""

import re
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent / 'pretext' / 'source'
ASSETS_DIR = Path(__file__).resolve().parent.parent / 'assets' / 'diagrams' / 'new'


def scan_chapter(ptx_path):
    """Scan a chapter file for completed-example table/diagram pairing issues."""
    text = ptx_path.read_text(encoding='utf-8')
    lines = text.split('\n')
    ch_match = re.search(r'ch-(\d+)', ptx_path.name)
    if not ch_match:
        return []
    ch_num = int(ch_match.group(1))
    findings = []

    # Strategy: find all image references, classify as table or diagram,
    # then check context for pairing.

    # Collect all images with their line numbers and context
    images = []
    for i, line in enumerate(lines):
        m = re.search(r'source="([^"]+)"', line)
        if m and 'diagrams/' in m.group(1):
            src = m.group(1)
            filename = src.split('/')[-1]
            is_table = '_table_' in filename or '_hw_student' in filename or '_hw_' in filename
            images.append({
                'line': i + 1,
                'src': src,
                'filename': filename,
                'is_table': is_table,
                'is_student': '_hw_student' in filename,
            })

    # Also find <tabular> elements
    tabulars = []
    for i, line in enumerate(lines):
        if '<tabular' in line:
            # Check if it's a labeling table (has Role/Phrase/POS/Word cells nearby)
            context = '\n'.join(lines[i:min(i+20, len(lines))])
            if re.search(r'<cell>Role</cell>', context) or re.search(r'<cell>Word</cell>', context):
                tabulars.append({'line': i + 1, 'is_table': True})

    # Identify "completed example" regions
    # Pattern 1: <paragraphs><title>Example (completed)</title> in homework
    # Pattern 2: content sections with table+diagram pairs (not in homework exercises)

    # Find homework section boundaries
    homework_start = None
    for i, line in enumerate(lines):
        if 'homework' in line.lower() and 'xml:id' in line:
            homework_start = i
            break

    # Find "Example (completed)" blocks
    example_blocks = []
    for i, line in enumerate(lines):
        if 'Example (completed)' in line or 'Example:' in line:
            example_blocks.append(i + 1)

    # For content sections (before homework): every table PNG should have
    # a nearby diagram, and vice versa
    content_tables = []
    content_diagrams = []
    for img in images:
        if homework_start and img['line'] > homework_start:
            continue  # in homework section
        if img['is_table']:
            content_tables.append(img)
        else:
            content_diagrams.append(img)

    # Check content table-diagram pairing (within 15 lines of each other)
    for table in content_tables:
        has_diagram = False
        for diag in content_diagrams:
            if abs(table['line'] - diag['line']) <= 15:
                has_diagram = True
                break
        if not has_diagram:
            findings.append(
                f"  Ch{ch_num:02d} line {table['line']}: CONTENT TABLE "
                f"'{table['filename']}' has NO nearby tree diagram"
            )

    for diag in content_diagrams:
        has_table = False
        for table in content_tables:
            if abs(diag['line'] - table['line']) <= 15:
                has_table = True
                break
        # Also check for nearby <tabular> elements
        for tab in tabulars:
            if homework_start and tab['line'] > homework_start:
                continue
            if abs(diag['line'] - tab['line']) <= 15:
                has_table = True
                break
        if not has_table:
            findings.append(
                f"  Ch{ch_num:02d} line {diag['line']}: CONTENT DIAGRAM "
                f"'{diag['filename']}' has NO nearby labeling table"
            )

    # Check homework completed examples
    for ex_line in example_blocks:
        if homework_start and ex_line < homework_start:
            continue  # content example, handled above

        # Look within 20 lines for both a table and a diagram
        has_table = False
        has_diagram = False

        for img in images:
            if abs(img['line'] - ex_line) <= 20:
                if img['is_table']:
                    has_table = True
                else:
                    has_diagram = True

        for tab in tabulars:
            if abs(tab['line'] - ex_line) <= 20:
                has_table = True

        if not has_table:
            findings.append(
                f"  Ch{ch_num:02d} line {ex_line}: HOMEWORK EXAMPLE "
                f"has NO labeling table"
            )
        if not has_diagram:
            findings.append(
                f"  Ch{ch_num:02d} line {ex_line}: HOMEWORK EXAMPLE "
                f"has NO tree diagram"
            )

    # Check for missing PNG files
    for img in images:
        png_path = ASSETS_DIR / img['filename']
        if not png_path.exists():
            findings.append(
                f"  Ch{ch_num:02d} line {img['line']}: MISSING FILE "
                f"'{img['filename']}'"
            )

    return findings


def main():
    print("=== Table-Diagram Pairing Audit ===\n")

    all_findings = []
    for ch_num in range(5, 16):
        ptx = SRC_DIR / f'ch-{ch_num:02d}.ptx'
        if not ptx.exists():
            continue
        findings = scan_chapter(ptx)
        if findings:
            print(f"Ch{ch_num:02d}: {len(findings)} issue(s)")
            for f in findings:
                print(f)
            all_findings.extend(findings)

    print(f"\n=== Summary ===")
    print(f"Total issues: {len(all_findings)}")
    if all_findings:
        print("AUDIT FAILED")
        return 1
    else:
        print("ALL EXAMPLES PROPERLY PAIRED")
        return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
