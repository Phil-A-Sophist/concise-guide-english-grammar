#!/usr/bin/env python3
"""
Extract bracket notations from PreTeXt chapter source files.

For each chapter (ch-05 through ch-14), finds all bracket notations
and associated <image> tags, outputting per-chapter JSON files
ready for role labeling and table PNG export.

Usage:
    python scripts/extract_brackets.py [--output-dir DIR]
"""

import argparse
import json
import re
from pathlib import Path


# Match image source attributes
IMAGE_RE = re.compile(r'<image\s+source="([^"]+)"')

# Root clause labels that start a bracket notation
ROOT_LABELS = {'S', 'IC', 'DC', 'RC', 'CC'}


def find_balanced_brackets(text, start):
    """Find a balanced bracket expression starting at position start.
    Returns the end position (exclusive) or -1 if unbalanced."""
    if text[start] != '[':
        return -1
    depth = 0
    i = start
    while i < len(text):
        if text[i] == '[':
            depth += 1
        elif text[i] == ']':
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return -1


def extract_brackets_from_line(line):
    """Extract all complete bracket notations from a line of text."""
    results = []
    i = 0
    while i < len(line):
        if line[i] == '[':
            # Check if this starts with a root label
            rest = line[i+1:].lstrip()
            label = rest.split()[0] if rest.split() else ''
            if label in ROOT_LABELS:
                end = find_balanced_brackets(line, i)
                if end > 0:
                    bracket = line[i:end]
                    # Must contain at least one nested bracket (not just [S])
                    if '[' in bracket[1:]:
                        results.append(bracket)
                    i = end
                    continue
        i += 1
    return results

# Chapters with tree diagrams
CHAPTERS = list(range(5, 15))  # Ch5 through Ch14


def extract_from_chapter(ptx_path):
    """Extract bracket notations and image references from a chapter file.

    Returns list of dicts with:
        bracket: the bracket notation string
        filename: suggested output filename
        image_before: the image source path that precedes this bracket (if any)
        section: approximate section context
        line_num: line number in source
        roles: empty dict (to be filled in manually)
    """
    text = ptx_path.read_text(encoding='utf-8')
    lines = text.split('\n')
    chapter_num = int(re.search(r'ch-(\d+)', ptx_path.stem).group(1))

    entries = []
    entry_idx = 0

    # Find all bracket notations with their line numbers
    for i, line in enumerate(lines):
        brackets = extract_brackets_from_line(line)
        for bracket in brackets:
            # Clean up whitespace
            bracket = re.sub(r'\s+', ' ', bracket).strip()

            # Find the nearest preceding <image> tag
            image_before = None
            for j in range(i - 1, max(i - 20, -1), -1):
                img_match = IMAGE_RE.search(lines[j])
                if img_match:
                    image_before = img_match.group(1)
                    break

            # Find section context
            section_title = None
            for j in range(i - 1, -1, -1):
                title_match = re.search(r'<title>([^<]+)</title>', lines[j])
                if title_match:
                    section_title = title_match.group(1)
                    break

            entry_idx += 1
            entries.append({
                'bracket': bracket,
                'filename': f'ch{chapter_num:02d}_table_{entry_idx:03d}',
                'image_before': image_before,
                'section': section_title,
                'line_num': i + 1,
                'roles': {},
            })

    return entries


def main():
    parser = argparse.ArgumentParser(description='Extract bracket notations from PreTeXt')
    parser.add_argument('--output-dir', '-o', default='data/static/table-roles',
                        help='Output directory for per-chapter JSON files')
    parser.add_argument('--source-dir', '-s', default='pretext/source',
                        help='PreTeXt source directory')
    args = parser.parse_args()

    source_dir = Path(args.source_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    total = 0
    for ch_num in CHAPTERS:
        ptx_path = source_dir / f'ch-{ch_num:02d}.ptx'
        if not ptx_path.exists():
            print(f'  Ch{ch_num:02d}: file not found, skipping')
            continue

        entries = extract_from_chapter(ptx_path)
        total += len(entries)

        out_path = output_dir / f'ch{ch_num:02d}_tables.json'
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump({'sentences': entries}, f, indent=2, ensure_ascii=False)

        print(f'  Ch{ch_num:02d}: {len(entries)} bracket notations -> {out_path.name}')

    print(f'\nTotal: {total} bracket notations across {len(CHAPTERS)} chapters')


if __name__ == '__main__':
    main()
