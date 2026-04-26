#!/usr/bin/env python3
"""
One-shot migration: build canonical per-item JSON files in data/trees/ch14/
from the existing scattered sources.

Sources merged:
  1. data/static/table-roles/ch14_tables.json  (brackets + roles per item)
  2. scripts/generate_ch14_answer_key.py        (DIAGRAM_EXERCISES — exercise_num, diagram filename)
  3. scripts/generate_ch14_tree_diagrams.py     (DIAGRAMS — textbook content diagrams)
  4. scripts/generate_hw_diagrams_batch.py      (HW_DIAGRAMS — homework diagrams)

Per-item JSON conforms to the schema in data/trees/README.md.

Usage:
    python scripts/migrate_ch14_to_canonical.py [--dry-run]
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TABLES_JSON = ROOT / 'data' / 'static' / 'table-roles' / 'ch14_tables.json'
ANSWER_KEY_SCRIPT = ROOT / 'scripts' / 'generate_ch14_answer_key.py'
CONTENT_DIAGRAMS_SCRIPT = ROOT / 'scripts' / 'generate_ch14_tree_diagrams.py'
HW_DIAGRAMS_SCRIPT = ROOT / 'scripts' / 'generate_hw_diagrams_batch.py'
OUTPUT_DIR = ROOT / 'data' / 'trees' / 'ch14'

# Add scripts/ to path so we can import answer_key_helpers for bracket parsing
sys.path.insert(0, str(ROOT / 'scripts'))
from answer_key_helpers import parse_bracket_to_multilevel  # noqa: E402


def normalize(bracket):
    """Whitespace-normalized bracket for matching."""
    return ' '.join(bracket.split())


def derive_sentence(bracket):
    """Derive surface sentence string from bracket terminals."""
    data = parse_bracket_to_multilevel(bracket)
    words = data['words']
    if not words:
        return ''
    sentence = ' '.join(words)
    # Capitalize first word; ensure terminal punctuation
    if sentence:
        sentence = sentence[0].upper() + sentence[1:]
    if not sentence.endswith(('.', '?', '!')):
        sentence += '.'
    return sentence


def extract_diagram_exercises():
    """Parse DIAGRAM_EXERCISES list from generate_ch14_answer_key.py via exec.

    Returns a list of dicts as defined in that script.
    """
    src = ANSWER_KEY_SCRIPT.read_text(encoding='utf-8')
    # Find DIAGRAM_EXERCISES = [...] block
    match = re.search(r'DIAGRAM_EXERCISES\s*=\s*(\[.*?\n\])\n\n',
                      src, re.DOTALL)
    if not match:
        raise RuntimeError("Could not locate DIAGRAM_EXERCISES in generate_ch14_answer_key.py")
    block_src = match.group(1)
    return eval(block_src, {'__builtins__': {}}, {})


def extract_content_diagrams():
    """Parse DIAGRAMS dict from generate_ch14_tree_diagrams.py.

    Returns dict mapping name -> bracket.
    """
    src = CONTENT_DIAGRAMS_SCRIPT.read_text(encoding='utf-8')
    match = re.search(r'^DIAGRAMS\s*=\s*(\{.*?^\})', src, re.DOTALL | re.MULTILINE)
    if not match:
        raise RuntimeError("Could not locate DIAGRAMS in generate_ch14_tree_diagrams.py")
    return eval(match.group(1), {'__builtins__': {}}, {})


def extract_hw_diagrams():
    """Parse CHAPTERS['ch14'] from generate_hw_diagrams_batch.py.

    Returns dict mapping diagram filename -> bracket.
    """
    src = HW_DIAGRAMS_SCRIPT.read_text(encoding='utf-8')
    match = re.search(r'^CHAPTERS\s*=\s*(\{.*?^\})', src, re.DOTALL | re.MULTILINE)
    if not match:
        raise RuntimeError("Could not locate CHAPTERS in generate_hw_diagrams_batch.py")
    all_hw = eval(match.group(1), {'__builtins__': {}}, {})
    return all_hw.get('ch14', {})


def find_diagram_for_bracket(bracket, diagram_dict):
    """Find diagram filename whose bracket matches (normalized)."""
    target = normalize(bracket)
    for name, br in diagram_dict.items():
        if normalize(br) == target:
            return name
    return None


def derive_purpose(filename):
    """ch14_hw_NNN -> homework, ch14_table_NNN -> textbook_example."""
    if '_hw_' in filename:
        return 'homework'
    if '_table_' in filename:
        return 'textbook_example'
    return 'textbook_example'


def derive_outputs(purpose, has_diagram, has_table_png, has_pretext_inline):
    outs = []
    if purpose == 'homework':
        outs.extend(['answer_key_docx', 'student_docx', 'overhead_docx'])
        if has_pretext_inline:
            outs.append('pretext_inline')
    elif purpose == 'textbook_example':
        # Textbook examples appear in the chapter HTML; their data isn't normally
        # rendered into the homework Word doc.
        pass
    if has_diagram:
        outs.append('diagram_png')
    if has_table_png:
        outs.append('table_png')
    return outs


def build_canonical_entry(table_entry, diag_exercises_by_bracket,
                           content_diagrams, hw_diagrams):
    """Convert one ch14_tables.json entry into a canonical dict."""
    filename = table_entry['filename']  # e.g., 'ch14_table_001' or 'ch14_hw_001'
    bracket = table_entry['bracket']
    purpose = derive_purpose(filename)
    sentence = derive_sentence(bracket)

    # Diagram lookup
    diagram_filename = None
    exercise_num = None
    bracket_drift = None
    if purpose == 'homework':
        # Try exact match first
        match = diag_exercises_by_bracket.get(normalize(bracket))
        if match:
            diagram_filename = match['diagram']
            exercise_num = match['num']
        else:
            # Fuzzy match: same words list, different POS labels => drift
            target_words = parse_bracket_to_multilevel(bracket)['words']
            for ak_norm_bracket, ak_entry in diag_exercises_by_bracket.items():
                ak_words = parse_bracket_to_multilevel(ak_entry['bracket'])['words']
                if ak_words == target_words:
                    bracket_drift = {
                        'json_bracket': bracket,
                        'answer_key_bracket': ak_entry['bracket'],
                    }
                    # Prefer answer-key bracket (drives rendered diagram)
                    bracket = ak_entry['bracket']
                    diagram_filename = ak_entry['diagram']
                    exercise_num = ak_entry['num']
                    break
            if not diagram_filename:
                # Final fallback
                diagram_filename = find_diagram_for_bracket(bracket, hw_diagrams)
    else:
        diagram_filename = find_diagram_for_bracket(bracket, content_diagrams)
        if not diagram_filename:
            # Try fuzzy match on terminals for content tables too
            target_words = parse_bracket_to_multilevel(bracket)['words']
            for diag_name, diag_bracket in content_diagrams.items():
                if parse_bracket_to_multilevel(diag_bracket)['words'] == target_words:
                    if normalize(diag_bracket) != normalize(bracket):
                        bracket_drift = {
                            'json_bracket': bracket,
                            'diagram_bracket': diag_bracket,
                        }
                        bracket = diag_bracket
                    diagram_filename = diag_name
                    break

    has_diagram = diagram_filename is not None
    has_table_png = True  # All ch14_tables.json entries get a labeling-table PNG
    has_pretext_inline = (purpose == 'homework')  # HW exercises are inline in .ptx

    # Use canonical sentence if the parsed-from-bracket version is sensible;
    # otherwise fall back to a normalized form.
    section = table_entry.get('section')

    entry = {
        'id': filename,
        'chapter': 14,
        'purpose': purpose,
        'section': section,
        'exercise_num': exercise_num,
        'sentence': sentence,
        'bracket': bracket,
        'roles': table_entry.get('roles', {}),
        'diagram_filename': diagram_filename,
        'table_filename': filename,
        'outputs': derive_outputs(purpose, has_diagram, has_table_png, has_pretext_inline),
        'overrides': None,
    }

    # Preserve image_before reference (for textbook tables that show a prior
    # chapter's diagram before the labeling table)
    if table_entry.get('image_before'):
        entry['precursor_image'] = table_entry['image_before']

    return entry, bracket_drift


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true',
                        help='Print summary without writing files')
    args = parser.parse_args()

    print(f"Loading {TABLES_JSON}...")
    tables_data = json.loads(TABLES_JSON.read_text(encoding='utf-8'))
    table_entries = tables_data['sentences']
    print(f"  {len(table_entries)} table entries")

    print(f"Extracting DIAGRAM_EXERCISES from {ANSWER_KEY_SCRIPT.name}...")
    diag_exercises = extract_diagram_exercises()
    diag_by_bracket = {normalize(d['bracket']): d for d in diag_exercises}
    print(f"  {len(diag_exercises)} homework exercises")

    print(f"Extracting content diagrams from {CONTENT_DIAGRAMS_SCRIPT.name}...")
    content_diagrams = extract_content_diagrams()
    print(f"  {len(content_diagrams)} content diagrams")

    print(f"Extracting HW diagrams from {HW_DIAGRAMS_SCRIPT.name}...")
    hw_diagrams = extract_hw_diagrams()
    print(f"  {len(hw_diagrams)} homework diagrams")

    print()
    print(f"Migrating to {OUTPUT_DIR}...")
    if not args.dry_run:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    written = 0
    homework_count = 0
    textbook_count = 0
    diagram_paired = 0
    drifts = []
    for entry_in in table_entries:
        canonical, drift = build_canonical_entry(
            entry_in, diag_by_bracket, content_diagrams, hw_diagrams
        )
        out_path = OUTPUT_DIR / f"{canonical['id']}.json"
        if not args.dry_run:
            out_path.write_text(
                json.dumps(canonical, indent=2, ensure_ascii=False) + '\n',
                encoding='utf-8'
            )
        written += 1
        if canonical['purpose'] == 'homework':
            homework_count += 1
        else:
            textbook_count += 1
        if canonical['diagram_filename']:
            diagram_paired += 1
        if drift:
            drifts.append((canonical['id'], drift))
        marker = '[DRY]' if args.dry_run else '[OK] '
        drift_marker = ' [DRIFT]' if drift else ''
        print(f"  {marker} {canonical['id']}.json  "
              f"(purpose={canonical['purpose']}, "
              f"diagram={canonical['diagram_filename'] or '-'})"
              f"{drift_marker}")

    print()
    print(f"Summary: {written} files | "
          f"{textbook_count} textbook | "
          f"{homework_count} homework | "
          f"{diagram_paired} with diagram filename")

    if drifts:
        print()
        print(f"=== DRIFT DETECTED ({len(drifts)} items) ===")
        print("Used the rendered-diagram bracket as authoritative.")
        for item_id, d in drifts:
            print(f"\n{item_id}:")
            for k, v in d.items():
                print(f"  {k}: {v}")


if __name__ == '__main__':
    main()
