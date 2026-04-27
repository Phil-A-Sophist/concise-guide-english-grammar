#!/usr/bin/env python3
"""
Regenerate PreTeXt include files for ch14 homework labeling tables from canonical.

Reads canonical homework entries from data/trees/ch14/ and writes one PreTeXt
fragment per entry to pretext/source/generated/ch14/{id}.ptx.

ch-14.ptx must reference these via xi:include — see _ch14_pretext_inline_used.

Usage:
    python scripts/regenerate_ch14_pretext.py [--dry-run]
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEN_DIR = ROOT / 'pretext' / 'source' / 'generated' / 'ch14'

sys.path.insert(0, str(ROOT / 'scripts'))
from answer_key_helpers import (  # noqa: E402
    load_canonical_trees, parse_bracket_to_multilevel,
    generate_pretext_labeling_xml,
)


def make_include(entry):
    """Build a PreTeXt fragment (a <tabular> block) for one canonical entry.

    Returns the XML string ready to be written to an include file.
    """
    parsed = parse_bracket_to_multilevel(entry['bracket'])
    words = parsed['words']
    # Filter elided words (e.g., '_' for missing complementizers)
    visible_words = [w for w in words if w.replace('_', ' ').strip()]

    # Use existing helper, filled=False for student-blank table
    body = generate_pretext_labeling_xml(visible_words, filled=False)

    # Reduce indentation by 4 spaces — body indents to fit a deeper context;
    # at the include-file root we want minimal indentation.
    body = '\n'.join(line[4:] if line.startswith('    ') else line
                     for line in body.splitlines())

    header = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<!-- AUTO-GENERATED from data/trees/ch14/{entry["id"]}.json '
        '- do not edit; regenerate via scripts/regenerate_ch14_pretext.py -->\n'
    )
    return header + body + '\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    entries = load_canonical_trees(14, purpose='homework')
    targets = [e for e in entries
               if 'pretext_inline' in (e.get('outputs') or [])]

    if not args.dry_run:
        GEN_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Regenerating {len(targets)} ch14 PreTeXt include(s) in {GEN_DIR}")
    for entry in targets:
        out_path = GEN_DIR / f"{entry['id']}.ptx"
        xml = make_include(entry)
        if args.dry_run:
            print(f"  [DRY] {out_path.relative_to(ROOT)}")
            print('  ' + xml.replace('\n', '\n  '))
        else:
            out_path.write_text(xml, encoding='utf-8')
            print(f"  [OK]  {out_path.relative_to(ROOT)}")


if __name__ == '__main__':
    main()
