#!/usr/bin/env python3
"""
Validate canonical tree files in data/trees/.

Checks:
  1. Schema: required fields present and well-typed.
  2. Bracket parseable: parse_bracket_to_multilevel() accepts the bracket.
  3. Words match: terminal sequence in bracket matches sentence words.
  4. Role coverage: every level/start_col present in the parsed multilevel
     table has a role label, unless overridden or the item is student-only.
  5. Open-class wrapping: every leaf POS in {N, V, ADJ, ADV, PREP} is wrapped
     in its matching phrase {NP, VP, ADJP, ADVP, PP}, with documented exceptions.
  6. Diagram filename uniqueness across all canonical files.
  7. Override schema: any 'overrides' field includes reason + approved_by +
     fix_underlying_when.

Exit codes:
  0 — all checks pass (warnings allowed)
  1 — at least one error
  2 — script error (validator broken)

Usage:
    python scripts/validate_canonical.py [--chapter 14] [--strict] [--quiet]
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TREES_DIR = ROOT / 'data' / 'trees'

sys.path.insert(0, str(ROOT / 'scripts'))
from answer_key_helpers import parse_bracket_to_multilevel  # noqa: E402


# Open-class POS tags that require phrase wrappers
OPEN_CLASS_POS = {'N', 'V', 'ADJ', 'ADV', 'PREP'}
POS_TO_PHRASE = {'N': 'NP', 'V': 'VP', 'ADJ': 'ADJP', 'ADV': 'ADVP', 'PREP': 'PP'}

# All known POS tags (closed + open). Used to identify terminals.
ALL_POS_TAGS = {
    'N', 'NOUN', 'V', 'VERB', 'ADJ', 'ADV', 'DET', 'PRON', 'PREP',
    'MOD', 'AUX', 'REL', 'COMP', 'CONJ', 'SUB', 'PART', 'MODAL', 'CC',
}

# Phrase / clause labels that may legitimately host bare open-class POS as
# direct children. NOM is the textbook's nominal label and conventionally
# hosts gerund V or nominal-head N directly. Update when conventions change.
PHRASE_EXCEPTIONS = {
    'NOM': {'V', 'N', 'PART'},   # gerund V, nominal N, infinitive PART
}


REQUIRED_FIELDS = {
    'id': str,
    'chapter': (int, type(None)),
    'purpose': str,
    'sentence': str,
    'bracket': str,
    'roles': dict,
    'outputs': list,
}

ALLOWED_PURPOSES = {'textbook_example', 'homework', 'exam', 'studyguide'}
ALLOWED_OUTPUTS = {
    'answer_key_docx', 'student_docx', 'overhead_docx',
    'diagram_png', 'table_png', 'pretext_inline',
}
OVERRIDE_REQUIRED_FIELDS = {'rule', 'reason', 'approved_by', 'fix_underlying_when'}


def parse_bracket_tree(bracket):
    """Parse bracket into nested-list tree. Same logic as parse_bracket_to_multilevel.

    Returns root list, or None on failure.
    """
    tokens = []
    i = 0
    while i < len(bracket):
        if bracket[i] in '[]':
            tokens.append(bracket[i])
            i += 1
        elif bracket[i].isspace():
            i += 1
        else:
            j = i
            while j < len(bracket) and bracket[j] not in '[] ':
                j += 1
            tokens.append(bracket[i:j])
            i = j

    stack = []
    current = None
    for tok in tokens:
        if tok == '[':
            node = []
            if current is not None:
                stack.append(current)
            current = node
        elif tok == ']':
            completed = current
            if stack:
                current = stack.pop()
                current.append(completed)
            else:
                current = completed
        else:
            if current is not None:
                current.append(tok)
    return current


def walk_tree(node, parent_label=None):
    """Yield (label, children, parent_label) for every internal node."""
    if not isinstance(node, list) or len(node) == 0:
        return
    label = node[0] if isinstance(node[0], str) else None
    if label is None:
        return
    children = node[1:]
    yield (label, children, parent_label)
    for child in children:
        yield from walk_tree(child, label)


def is_pos_node(node):
    return (isinstance(node, list) and len(node) == 2
            and isinstance(node[0], str) and node[0] in ALL_POS_TAGS
            and isinstance(node[1], str))


# ---------- check functions ----------

def check_schema(entry, errors):
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in entry:
            errors.append(f"missing required field '{field}'")
            continue
        if not isinstance(entry[field], expected_type):
            errors.append(f"field '{field}' has wrong type "
                          f"(got {type(entry[field]).__name__})")
    if 'purpose' in entry and entry['purpose'] not in ALLOWED_PURPOSES:
        errors.append(f"purpose '{entry['purpose']}' not in {sorted(ALLOWED_PURPOSES)}")
    if 'outputs' in entry:
        for out in entry['outputs']:
            if out not in ALLOWED_OUTPUTS:
                errors.append(f"output '{out}' not in {sorted(ALLOWED_OUTPUTS)}")


def check_bracket_parseable(entry, errors):
    bracket = entry.get('bracket', '')
    try:
        data = parse_bracket_to_multilevel(bracket)
    except Exception as e:
        errors.append(f"bracket unparseable: {e}")
        return None
    if not data.get('words'):
        errors.append("bracket parsed but contains no terminal words")
        return None
    return data


def check_words_match(entry, parsed, errors):
    if parsed is None:
        return
    sentence = entry.get('sentence', '')
    bracket_words = parsed['words']
    # Filter elided words ('_' alone, which becomes ' ' after underscore swap)
    visible_bracket = [w for w in bracket_words if w.replace('_', ' ').strip()]
    sent_normalized = sentence.rstrip('.?!').strip()
    sent_words = sent_normalized.split()
    if len(sent_words) != len(visible_bracket):
        errors.append(
            f"sentence has {len(sent_words)} words but bracket has "
            f"{len(visible_bracket)} visible terminals "
            f"(plus {len(bracket_words) - len(visible_bracket)} elided)")
        return
    for i, (sw, bw) in enumerate(zip(sent_words, visible_bracket)):
        bw_normalized = bw.replace('_', ' ')
        if i == 0:
            if sw.lower() != bw_normalized.lower():
                errors.append(
                    f"word {i}: sentence='{sw}' vs bracket='{bw_normalized}'")
        elif sw != bw_normalized:
            errors.append(
                f"word {i}: sentence='{sw}' vs bracket='{bw_normalized}'")


def check_role_coverage(entry, parsed, errors, warnings):
    """Role coverage is a warning by default; --strict promotes to error.

    The current convention labels only 'interesting' roles, leaving deeper
    phrases unlabeled. As ch14 cleanup proceeds, missing roles should be
    filled in or explicitly marked with allow_missing_role override.
    """
    if parsed is None:
        return
    outputs = entry.get('outputs', [])
    answer_outputs = {'answer_key_docx', 'overhead_docx', 'table_png'}
    if not (set(outputs) & answer_outputs):
        return

    overrides = entry.get('overrides') or {}
    suppress_keys = set()
    if overrides.get('rule') == 'allow_missing_role':
        targets = overrides.get('targets', [])
        for t in targets:
            suppress_keys.add(f"{t.get('level')}:{t.get('start_col')}")

    roles = entry.get('roles') or {}
    levels = parsed.get('levels', [])
    for level_idx, level_entries in enumerate(levels):
        level_roles = roles.get(str(level_idx), {})
        for ent in level_entries:
            start_col = ent['start_col']
            key = f"{level_idx}:{start_col}"
            if str(start_col) not in level_roles or not level_roles[str(start_col)]:
                if key in suppress_keys:
                    continue
                warnings.append(
                    f"missing role at level {level_idx}, "
                    f"start_col {start_col} (phrase {ent['label']})")


def check_open_class_wrapping(entry, errors, warnings):
    bracket = entry.get('bracket', '')
    tree = parse_bracket_tree(bracket)
    if tree is None:
        return

    overrides = entry.get('overrides') or {}
    allow_unwrapped = overrides.get('rule') == 'allow_unwrapped_pos'

    # Walk: for each POS leaf, check parent label
    def walk(node, parent_label):
        if not isinstance(node, list) or len(node) == 0:
            return
        label = node[0] if isinstance(node[0], str) else None
        if label is None:
            return
        if is_pos_node(node):
            if label in OPEN_CLASS_POS:
                expected = POS_TO_PHRASE[label]
                if parent_label != expected:
                    # Check exception list
                    exception = PHRASE_EXCEPTIONS.get(parent_label, set())
                    if label in exception:
                        return  # Documented exception
                    msg = (f"open-class {label} '{node[1]}' has parent "
                           f"'{parent_label}' (expected '{expected}')")
                    if allow_unwrapped:
                        return
                    warnings.append(msg)
            return
        for child in node[1:]:
            walk(child, label)

    walk(tree, parent_label=None)


def check_overrides_schema(entry, errors):
    overrides = entry.get('overrides')
    if overrides is None:
        return
    if not isinstance(overrides, dict):
        errors.append("'overrides' must be null or an object")
        return
    missing = OVERRIDE_REQUIRED_FIELDS - set(overrides.keys())
    if missing:
        errors.append(f"override missing required field(s): {sorted(missing)}")


# ---------- main ----------

def validate_file(path):
    """Returns (errors, warnings, entry)."""
    errors = []
    warnings = []
    try:
        entry = json.loads(path.read_text(encoding='utf-8'))
    except Exception as e:
        return [f"could not parse JSON: {e}"], [], None

    check_schema(entry, errors)
    if errors:
        return errors, warnings, entry

    parsed = check_bracket_parseable(entry, errors)
    check_words_match(entry, parsed, errors)
    check_role_coverage(entry, parsed, errors, warnings)
    check_open_class_wrapping(entry, errors, warnings)
    check_overrides_schema(entry, errors)
    return errors, warnings, entry


def check_diagram_uniqueness(entries):
    """Cross-file check: no two entries share a diagram_filename."""
    errors = []
    seen = {}
    for path, entry in entries:
        diag = entry.get('diagram_filename')
        if not diag:
            continue
        if diag in seen:
            errors.append(
                f"diagram_filename '{diag}' used by both "
                f"{seen[diag].name} and {path.name}")
        else:
            seen[diag] = path
    return errors


def collect_active_overrides(entries):
    return [(p, e['overrides']) for p, e in entries
            if e.get('overrides')]


def write_overrides_log(entries):
    """Regenerate data/living/overrides_log.md from current canonical state."""
    actives = collect_active_overrides(entries)
    log_path = ROOT / 'data' / 'living' / 'overrides_log.md'
    log_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        '# Active Canonical Overrides',
        '',
        '**Auto-generated by `scripts/validate_canonical.py` on every run.**',
        'Do not edit by hand. To remove an override, edit the canonical JSON file '
        'and rerun the validator.',
        '',
    ]
    if not actives:
        lines.append('_No active overrides._')
    else:
        lines.append(f'{len(actives)} active override(s):')
        lines.append('')
        for path, ov in actives:
            rel = path.relative_to(ROOT)
            lines.append(f'## `{rel}`')
            lines.append('')
            lines.append(f"- **rule:** `{ov.get('rule', '?')}`")
            lines.append(f"- **reason:** {ov.get('reason', '?')}")
            lines.append(f"- **approved by:** {ov.get('approved_by', '?')}")
            lines.append(f"- **fix when:** {ov.get('fix_underlying_when', '?')}")
            lines.append('')
    log_path.write_text('\n'.join(lines), encoding='utf-8')
    return log_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chapter', type=int, default=None,
                        help='Validate only ch{N}/ subdirectory')
    parser.add_argument('--strict', action='store_true',
                        help='Treat warnings as errors')
    parser.add_argument('--quiet', action='store_true',
                        help='Suppress per-file output; only show errors/warnings')
    args = parser.parse_args()

    if args.chapter is not None:
        scan_dirs = [TREES_DIR / f'ch{args.chapter:02d}']
    else:
        scan_dirs = [d for d in TREES_DIR.iterdir() if d.is_dir()]

    paths = []
    for d in scan_dirs:
        if not d.exists():
            continue
        paths.extend(sorted(d.rglob('*.json')))

    if not paths:
        print(f"No canonical files found.")
        return 0

    print(f"Validating {len(paths)} file(s)...")

    total_errors = 0
    total_warnings = 0
    entries = []
    for path in paths:
        errors, warnings, entry = validate_file(path)
        entries.append((path, entry or {}))
        if errors or warnings:
            print(f"\n{path.relative_to(ROOT)}:")
            for e in errors:
                print(f"  ERROR: {e}")
            for w in warnings:
                print(f"  WARN:  {w}")
        elif not args.quiet:
            print(f"  OK   {path.relative_to(ROOT)}")
        total_errors += len(errors)
        total_warnings += len(warnings)

    # Cross-file checks
    cross_errors = check_diagram_uniqueness(entries)
    for e in cross_errors:
        print(f"\nCROSS-FILE ERROR: {e}")
    total_errors += len(cross_errors)

    # Overrides summary + log file
    actives = collect_active_overrides(entries)
    log_path = write_overrides_log(entries)
    print()
    print(f"=== Summary ===")
    print(f"  Files:    {len(paths)}")
    print(f"  Errors:   {total_errors}")
    print(f"  Warnings: {total_warnings}")
    print(f"  Active overrides: {len(actives)}")
    print(f"  Overrides log:    {log_path.relative_to(ROOT)}")
    if actives:
        print()
        print("=== Active Overrides ===")
        for path, ov in actives:
            print(f"  {path.name}: rule='{ov.get('rule')}', "
                  f"reason='{ov.get('reason')}'")

    if total_errors > 0:
        return 1
    if args.strict and total_warnings > 0:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
