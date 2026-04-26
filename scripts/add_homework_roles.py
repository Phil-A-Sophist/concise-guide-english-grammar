#!/usr/bin/env python3
"""
Add homework exercise brackets (with auto-assigned roles) to table-roles JSON files.

The JSON files in data/static/table-roles/ were populated from textbook (PreTeXt)
examples, but the homework answer key scripts have their own unique bracket notations.
This script extracts those brackets, computes roles via assign_table_roles.py's
deterministic logic, and appends them to the JSON files.

Usage:
    python scripts/add_homework_roles.py [--dry-run]
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Import the role assignment logic
sys.path.insert(0, str(Path(__file__).parent))
from assign_table_roles import parse_bracket, assign_word_positions, assign_depths, assign_roles_to_tree


SCRIPTS_DIR = Path(__file__).parent
JSON_DIR = SCRIPTS_DIR.parent / 'data' / 'static' / 'table-roles'


def extract_brackets_from_script(script_path):
    """Extract all bracket notation strings from an answer key script."""
    text = script_path.read_text(encoding='utf-8')
    # Match 'bracket': '...' patterns (single-quoted bracket values)
    matches = re.findall(r"'bracket':\s*'([^']+)'", text)
    return matches


def compute_roles(bracket):
    """Compute roles for a bracket notation using assign_table_roles logic."""
    tree = parse_bracket(bracket)
    if tree is None:
        return {}
    assign_word_positions(tree)
    assign_depths(tree)
    return assign_roles_to_tree(tree)


def normalize(bracket):
    """Normalize whitespace in a bracket string for comparison."""
    return ' '.join(bracket.split())


def main():
    parser = argparse.ArgumentParser(description='Add homework brackets to table-roles JSON')
    parser.add_argument('--dry-run', action='store_true', help='Print changes without writing')
    args = parser.parse_args()

    chapters = list(range(5, 16))  # Ch05 through Ch15
    total_added = 0
    total_skipped = 0

    for ch_num in chapters:
        script_path = SCRIPTS_DIR / f'generate_ch{ch_num:02d}_answer_key.py'
        json_path = JSON_DIR / f'ch{ch_num:02d}_tables.json'

        if not script_path.exists():
            print(f"  Ch{ch_num:02d}: script not found, skipping")
            continue
        if not json_path.exists():
            print(f"  Ch{ch_num:02d}: JSON not found, skipping")
            continue

        # Load existing JSON
        data = json.loads(json_path.read_text(encoding='utf-8'))
        existing_brackets = {normalize(e['bracket']) for e in data['sentences']}

        # Extract homework brackets
        hw_brackets = extract_brackets_from_script(script_path)
        added = 0
        skipped = 0

        for bracket in hw_brackets:
            norm = normalize(bracket)
            if norm in existing_brackets:
                skipped += 1
                continue

            roles = compute_roles(bracket)
            entry = {
                'bracket': bracket,
                'filename': f'ch{ch_num:02d}_hw_{added + 1:03d}',
                'image_before': None,
                'section': 'Homework Part 4',
                'line_num': None,
                'roles': roles,
            }

            if args.dry_run:
                print(f"  Ch{ch_num:02d} ADD: {bracket[:70]}...")
                print(f"         roles: {roles}")
            else:
                data['sentences'].append(entry)

            existing_brackets.add(norm)
            added += 1

        if not args.dry_run and added > 0:
            json_path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + '\n',
                encoding='utf-8'
            )

        total_added += added
        total_skipped += skipped
        status = "DRY RUN" if args.dry_run else "written"
        print(f"  Ch{ch_num:02d}: {added} added, {skipped} already present ({status})")

    print(f"\nTotal: {total_added} added, {total_skipped} already present")


if __name__ == '__main__':
    main()
