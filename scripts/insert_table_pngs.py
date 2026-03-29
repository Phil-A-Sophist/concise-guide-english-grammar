#!/usr/bin/env python3
"""
Insert multi-level labeling table PNG references into PreTeXt source files.

For each entry in a chapter's table-roles JSON:
1. Finds the bracket notation line in the .ptx file (matching on bracket text)
2. Locates the nearest preceding <image> tag (the tree diagram)
3. Inserts a new <image> tag for the table PNG above the tree diagram

Usage:
    python scripts/insert_table_pngs.py [--chapters 05 06 07 ...]
    python scripts/insert_table_pngs.py --all
    python scripts/insert_table_pngs.py --dry-run --all
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_DIR = ROOT / 'data' / 'static' / 'table-roles'
PTX_DIR = ROOT / 'pretext' / 'source'


def count_words(bracket):
    """Count terminal words in a bracket notation."""
    # Words are tokens not starting with [ or ] and not all-caps labels
    tokens = bracket.replace('[', ' ').replace(']', ' ').split()
    words = [t for t in tokens if not t.isupper() and not t.startswith('[')]
    return len(words)


def pick_width(word_count):
    """Choose image width percentage based on word count."""
    if word_count <= 3:
        return '50%'
    elif word_count <= 5:
        return '65%'
    elif word_count <= 7:
        return '80%'
    else:
        return '95%'


def extract_sentence(bracket):
    """Extract the plain sentence from bracket notation for alt text."""
    tokens = bracket.replace('[', ' ').replace(']', ' ').split()
    words = [t for t in tokens if not t.isupper()]
    return ' '.join(words)


def find_bracket_line(lines, bracket_text, hint_line=None):
    """Find the line index containing this bracket notation in a <c> tag.

    When multiple matches exist (same sentence in different sections),
    uses hint_line (from JSON line_num) to pick the closest match.
    """
    normalized = ' '.join(bracket_text.split())
    matches = []
    for i, line in enumerate(lines):
        if '<c>' in line and '</c>' in line:
            m = re.search(r'<c>(.*?)</c>', line)
            if m:
                line_bracket = ' '.join(m.group(1).split())
                if line_bracket == normalized:
                    matches.append(i)
    if not matches:
        return None
    if len(matches) == 1 or hint_line is None:
        return matches[0]
    # Pick the match closest to the hint line number (0-indexed)
    hint_idx = hint_line - 1
    return min(matches, key=lambda x: abs(x - hint_idx))


def find_preceding_image(lines, bracket_idx):
    """Find the nearest <image source=...> line above the bracket line."""
    for i in range(bracket_idx - 1, max(bracket_idx - 20, -1), -1):
        if '<image source=' in lines[i]:
            return i
    return None


def build_image_tag(filename, bracket, indent):
    """Build the PreTeXt <image> block for a table PNG."""
    sentence = extract_sentence(bracket)
    wc = count_words(bracket)
    width = pick_width(wc)
    desc = f'Multi-level labeling table for "{sentence}"'
    return [
        f'{indent}<image source="diagrams/new/{filename}.png" width="{width}">\n',
        f'{indent}  <description>{desc}</description>\n',
        f'{indent}</image>\n',
    ]


def process_chapter(ch_num, dry_run=False):
    """Insert table PNG references for one chapter."""
    json_path = JSON_DIR / f'ch{ch_num}_tables.json'
    ptx_path = PTX_DIR / f'ch-{ch_num}.ptx'

    if not json_path.exists():
        print(f'  SKIP: {json_path.name} not found')
        return 0
    if not ptx_path.exists():
        print(f'  SKIP: {ptx_path.name} not found')
        return 0

    data = json.loads(json_path.read_text(encoding='utf-8'))
    lines = ptx_path.read_text(encoding='utf-8').splitlines(keepends=True)

    inserted = 0
    # Process in reverse order so line numbers stay valid
    entries = []
    for entry in data['sentences']:
        if entry.get('skip'):
            continue
        bracket = entry['bracket']
        filename = entry['filename']

        line_num = entry.get('line_num')

        # Check if already inserted
        already = any(f'diagrams/new/{filename}.png' in line for line in lines)
        if already:
            print(f'  ALREADY: {filename}')
            continue

        bracket_idx = find_bracket_line(lines, bracket, hint_line=line_num)
        if bracket_idx is None:
            print(f'  WARNING: bracket not found for {filename}')
            continue

        image_idx = find_preceding_image(lines, bracket_idx)
        if image_idx is not None:
            insert_at = image_idx  # Insert table above tree diagram
        else:
            insert_at = bracket_idx  # No tree image; insert above bracket

        # Detect indent from the image or bracket line
        ref_line = lines[insert_at]
        indent = re.match(r'^(\s*)', ref_line).group(1)

        entries.append((insert_at, filename, bracket, indent))

    # Sort by position descending so insertions don't shift later indices
    entries.sort(key=lambda x: x[0], reverse=True)

    for insert_at, filename, bracket, indent in entries:
        new_lines = build_image_tag(filename, bracket, indent)
        if dry_run:
            print(f'  DRY-RUN: {filename} -> line {insert_at + 1}')
            inserted += 1
        else:
            lines[insert_at:insert_at] = new_lines
            inserted += 1
            print(f'  INSERT: {filename} -> line {insert_at + 1}')

    if not dry_run and inserted > 0:
        ptx_path.write_text(''.join(lines), encoding='utf-8')
        print(f'  Wrote {ptx_path.name} ({inserted} tables inserted)')

    return inserted


def main():
    parser = argparse.ArgumentParser(description='Insert table PNG refs into PreTeXt')
    parser.add_argument('--chapters', nargs='+', default=[],
                        help='Chapter numbers (e.g., 05 06 07)')
    parser.add_argument('--all', action='store_true',
                        help='Process all chapters with JSON files')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be inserted without modifying files')
    args = parser.parse_args()

    if args.all:
        chapters = sorted(p.stem.replace('_tables', '').replace('ch', '')
                          for p in JSON_DIR.glob('ch*_tables.json'))
    elif args.chapters:
        chapters = args.chapters
    else:
        parser.print_help()
        sys.exit(1)

    total = 0
    for ch in chapters:
        print(f'Ch{ch}:')
        total += process_chapter(ch, dry_run=args.dry_run)

    action = 'would insert' if args.dry_run else 'inserted'
    print(f'\nDone. {total} table images {action} across {len(chapters)} chapters.')


if __name__ == '__main__':
    main()
