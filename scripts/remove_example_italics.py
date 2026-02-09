#!/usr/bin/env python3
"""
Remove italics from language examples in PreTeXt source files.

This script removes <em> tags from common patterns where italics are used
for language examples rather than emphasis:
1. Table cells: <cell><em>word</em></cell> → <cell>word</cell>
2. List items (whole): <li><p><em>word</em></p></li> → <li><p>word</p></li>
3. List items (start): <li><p><em>word</em> ... → <li><p>word ...

Chapters 1-3 are skipped as per user request.
"""

import re
from pathlib import Path

SOURCE_DIR = Path(__file__).parent.parent / "pretext" / "source"

# Chapters to process (skip 1-3)
CHAPTERS = [f"ch-{i:02d}.ptx" for i in range(4, 22)]


def remove_em_in_cells(content: str) -> tuple[str, int]:
    """Remove <em> tags from table cells that contain only emphasized text."""
    pattern = r'<cell><em>([^<]+)</em></cell>'
    replacement = r'<cell>\1</cell>'
    new_content, count = re.subn(pattern, replacement, content)
    return new_content, count


def remove_em_in_list_items_whole(content: str) -> tuple[str, int]:
    """Remove <em> from list items that are entirely emphasized."""
    pattern = r'<li><p><em>([^<]+)</em></p></li>'
    replacement = r'<li><p>\1</p></li>'
    new_content, count = re.subn(pattern, replacement, content)
    return new_content, count


def remove_em_at_list_item_start(content: str) -> tuple[str, int]:
    """Remove <em> from the beginning of list items (word followed by space/dash)."""
    # Match <li><p><em>word</em> followed by space, dash, or other punctuation
    pattern = r'<li><p><em>([^<]+)</em>(\s*[-–—:,])'
    replacement = r'<li><p>\1\2'
    new_content, count = re.subn(pattern, replacement, content)
    return new_content, count


def process_file(filepath: Path) -> dict:
    """Process a single file and return counts of changes."""
    content = filepath.read_text(encoding='utf-8')
    original = content

    counts = {
        'cells': 0,
        'list_whole': 0,
        'list_start': 0,
    }

    content, counts['cells'] = remove_em_in_cells(content)
    content, counts['list_whole'] = remove_em_in_list_items_whole(content)
    content, counts['list_start'] = remove_em_at_list_item_start(content)

    if content != original:
        filepath.write_text(content, encoding='utf-8')

    return counts


def main():
    total_counts = {'cells': 0, 'list_whole': 0, 'list_start': 0}

    print("Removing italics from language examples...")
    print("=" * 50)

    for chapter in CHAPTERS:
        filepath = SOURCE_DIR / chapter
        if not filepath.exists():
            print(f"  {chapter}: not found, skipping")
            continue

        counts = process_file(filepath)
        total = sum(counts.values())

        if total > 0:
            print(f"  {chapter}: {total} changes")
            print(f"    - table cells: {counts['cells']}")
            print(f"    - list items (whole): {counts['list_whole']}")
            print(f"    - list items (start): {counts['list_start']}")
        else:
            print(f"  {chapter}: no changes")

        for key in total_counts:
            total_counts[key] += counts[key]

    print("=" * 50)
    print(f"Total changes: {sum(total_counts.values())}")
    print(f"  - table cells: {total_counts['cells']}")
    print(f"  - list items (whole): {total_counts['list_whole']}")
    print(f"  - list items (start): {total_counts['list_start']}")


if __name__ == "__main__":
    main()
