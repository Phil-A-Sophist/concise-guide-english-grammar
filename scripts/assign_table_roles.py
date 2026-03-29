#!/usr/bin/env python3
"""
Assign functional roles to bracket notation entries in table-roles JSON files.

Parses bracket notation into tree structures and assigns roles based on
structural position. Indices are word positions (0-based across the whole
sentence), matching the labeling table column layout.

Usage:
    python scripts/assign_table_roles.py [--input-dir DIR] [--validate-ch7] [--dry-run]
"""

import argparse
import json
import sys
from pathlib import Path


# --- Tree parser ---

class TreeNode:
    __slots__ = ('label', 'word', 'children', 'parent', 'depth',
                 'word_start', 'word_end')

    def __init__(self, label, word=None):
        self.label = label
        self.word = word
        self.children = []
        self.parent = None
        self.depth = 0
        self.word_start = -1
        self.word_end = -1

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        return child

    def is_terminal(self):
        return self.word is not None and len(self.children) == 0


def parse_bracket(text):
    text = text.strip()
    pos = 0

    def parse_node():
        nonlocal pos
        if pos >= len(text) or text[pos] != '[':
            return None
        pos += 1
        while pos < len(text) and text[pos] == ' ':
            pos += 1
        label_start = pos
        while pos < len(text) and text[pos] not in ' []':
            pos += 1
        label = text[label_start:pos]
        node = TreeNode(label)
        while pos < len(text) and text[pos] == ' ':
            pos += 1
        if pos < len(text) and text[pos] == '[':
            while pos < len(text) and text[pos] == '[':
                child = parse_node()
                if child:
                    node.add_child(child)
                while pos < len(text) and text[pos] == ' ':
                    pos += 1
        elif pos < len(text) and text[pos] != ']':
            word_start = pos
            while pos < len(text) and text[pos] != ']':
                pos += 1
            node.word = text[word_start:pos].strip()
        if pos < len(text) and text[pos] == ']':
            pos += 1
        return node

    return parse_node()


def assign_word_positions(node, counter=None):
    if counter is None:
        counter = [0]
    if node.is_terminal():
        node.word_start = counter[0]
        node.word_end = counter[0]
        counter[0] += 1
    else:
        for child in node.children:
            assign_word_positions(child, counter)
        if node.children:
            node.word_start = node.children[0].word_start
            node.word_end = node.children[-1].word_end


def assign_depths(node, depth=0):
    node.depth = depth
    for child in node.children:
        assign_depths(child, depth + 1)


# --- Role assignment ---

LINKING_VERBS = {
    'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
    'seems', 'seem', 'seemed',
    'becomes', 'become', 'became',
    'appears', 'appear', 'appeared',
    'feels', 'feel', 'felt',
    'looks', 'look', 'looked',
    'sounds', 'sound', 'sounded',
    'tastes', 'taste', 'tasted',
    'smells', 'smell', 'smelled',
    'remains', 'remain', 'remained',
    'stays', 'stay', 'stayed',
    'grows', 'grow', 'grew',
    'turns', 'turn', 'turned',
    'gets', 'get', 'got',
    'proves', 'prove', 'proved',
}

COMPLEX_TRANS_VERBS = {
    'elected', 'elect', 'named', 'name', 'appointed', 'appoint',
    'called', 'call', 'made', 'make', 'considered', 'consider',
    'declared', 'declare', 'crowned', 'crown', 'found', 'find',
}

TEMPORAL_NOUNS = {
    'day', 'days', 'night', 'nights', 'morning', 'mornings',
    'afternoon', 'afternoons', 'evening', 'evenings',
    'week', 'weeks', 'month', 'months', 'year', 'years',
    'hour', 'hours', 'minute', 'minutes', 'second', 'seconds',
    'moment', 'moments', 'time', 'times',
    'summer', 'winter', 'spring', 'fall', 'autumn',
    'today', 'tomorrow', 'yesterday',
}


def get_main_verb(vp_node):
    for child in vp_node.children:
        if child.label == 'V' and child.word:
            return child.word.lower()
        if child.label == 'VP':
            v = get_main_verb(child)
            if v:
                return v
    return None


def is_copular_vp(vp_node):
    verb = get_main_verb(vp_node)
    return verb in LINKING_VERBS if verb else False


def is_temporal_np(np_node):
    """Check if NP is a temporal expression (adverbial function)."""
    for child in np_node.children:
        if child.label == 'N' and child.word and child.word.lower() in TEMPORAL_NOUNS:
            return True
    return False


def count_arg_nps(vp_node):
    """Count non-temporal NP children of VP (argument NPs only)."""
    return sum(1 for c in vp_node.children
               if c.label == 'NP' and not is_temporal_np(c))


def has_adjp_after_np(vp_node):
    seen_np = False
    for child in vp_node.children:
        if child.label == 'NP' and not is_temporal_np(child):
            seen_np = True
        elif child.label == 'ADJP' and seen_np:
            return True
    return False


def assign_roles_to_tree(tree):
    """
    Walk the tree and assign roles. Returns dict of:
      { level_str: { word_position_str: role_label } }
    """
    if tree is None:
        return {}

    assign_word_positions(tree)
    assign_depths(tree)
    roles = {}

    def add_role(depth, node, role):
        roles.setdefault(str(depth), {})[str(node.word_start)] = role

    def process_np_modifiers(np_node, depth):
        for child in np_node.children:
            if child.label in ('DET', 'N', 'PRON', 'CONJ'):
                continue
            if child.label in ('ADJP', 'ADJ', 'PP', 'RC', 'VP'):
                add_role(depth, child, 'Adjectival')
                if child.label == 'PP':
                    process_pp_np(child, depth + 1)
                elif child.label == 'VP':
                    process_vp_inside_np(child, depth + 1)
                elif child.label == 'RC':
                    process_rc(child, depth + 1)
            elif child.label == 'NP':
                process_np_modifiers(child, depth + 1)

    def process_pp_np(pp_node, depth):
        for child in pp_node.children:
            if child.label == 'NP':
                process_np_modifiers(child, depth)

    def process_vp_inside_np(vp_node, depth):
        for child in vp_node.children:
            if child.label == 'PP':
                process_pp_np(child, depth)
            elif child.label == 'NP':
                process_np_modifiers(child, depth)

    def process_rc(rc_node, depth):
        for child in rc_node.children:
            if child.label == 'VP':
                process_vp(child, depth, is_in_rc=True)

    def process_vp(vp_node, depth, is_in_rc=False):
        copular = is_copular_vp(vp_node)
        arg_np_count = count_arg_nps(vp_node)
        has_oc_adjp = has_adjp_after_np(vp_node)
        verb = get_main_verb(vp_node)
        is_complex_trans = (verb in COMPLEX_TRANS_VERBS) if verb else False

        arg_np_seen = 0
        for child in vp_node.children:
            if child.label in ('V', 'AUX', 'MOD', 'NEG', 'CONJ', 'PART',
                               'SUB', 'REL'):
                continue

            if child.label == 'NP':
                if is_temporal_np(child):
                    add_role(depth, child, 'Adverbial')
                    process_np_modifiers(child, depth + 1)
                    continue

                arg_np_seen += 1
                if copular:
                    add_role(depth, child, 'Subject Complement')
                elif has_oc_adjp and arg_np_seen == 1:
                    add_role(depth, child, 'Direct Object')
                elif is_complex_trans and arg_np_count >= 2:
                    if arg_np_seen == 1:
                        add_role(depth, child, 'Direct Object')
                    else:
                        add_role(depth, child, 'Object Complement')
                elif arg_np_count >= 2 and not is_complex_trans:
                    if arg_np_seen == 1:
                        add_role(depth, child, 'Indirect Object')
                    else:
                        add_role(depth, child, 'Direct Object')
                else:
                    add_role(depth, child, 'Direct Object')
                process_np_modifiers(child, depth + 1)

            elif child.label == 'ADJP':
                if copular:
                    add_role(depth, child, 'Subject Complement')
                elif arg_np_seen > 0:
                    add_role(depth, child, 'Object Complement')
                else:
                    add_role(depth, child, 'Subject Complement')
                for adjp_child in child.children:
                    if adjp_child.label == 'PP':
                        process_pp_np(adjp_child, depth + 1)

            elif child.label == 'ADVP':
                add_role(depth, child, 'Adverbial')

            elif child.label == 'PP':
                add_role(depth, child, 'Adverbial')
                process_pp_np(child, depth + 1)

            elif child.label == 'VP':
                is_conjoined = any(c.label == 'CONJ' for c in vp_node.children)
                if is_conjoined:
                    process_vp(child, depth, is_in_rc=is_in_rc)
                else:
                    add_role(depth, child, 'Adverbial')

            elif child.label == 'CC':
                add_role(depth, child, 'Direct Object')

            elif child.label == 'DC':
                add_role(depth, child, 'Adverbial')

            elif child.label == 'PRON':
                if copular:
                    add_role(depth, child, 'Subject Complement')

    def process_ic_dc_internals(clause_node, depth):
        for child in clause_node.children:
            if child.label == 'NP':
                add_role(depth, child, 'Subject')
                process_np_modifiers(child, depth + 1)
            elif child.label == 'VP':
                add_role(depth, child, 'Predicate')
                process_vp(child, depth + 1)
            elif child.label == 'PP':
                add_role(depth, child, 'Adverbial')
                process_pp_np(child, depth + 1)
            elif child.label == 'ADVP':
                add_role(depth, child, 'Adverbial')

    def process_s_level(s_node, base_depth):
        """Assign roles to direct children of any S-like node.
        Handles all child types: NP, VP, PP, ADVP, IC, DC, CC, S, CONJ, AUX."""
        for child in s_node.children:
            if child.label == 'NP':
                add_role(base_depth, child, 'Subject')
                process_np_modifiers(child, base_depth + 1)
            elif child.label == 'VP':
                add_role(base_depth, child, 'Predicate')
                process_vp(child, base_depth + 1)
            elif child.label == 'PP':
                add_role(base_depth, child, 'Adverbial')
                process_pp_np(child, base_depth + 1)
            elif child.label == 'ADVP':
                add_role(base_depth, child, 'Adverbial')
            elif child.label == 'DC':
                add_role(base_depth, child, 'Adverbial')
                process_ic_dc_internals(child, base_depth + 1)
            elif child.label == 'IC':
                add_role(base_depth, child, 'Main')
                process_ic_dc_internals(child, base_depth + 1)
            elif child.label == 'CC':
                if child == s_node.children[0]:
                    add_role(base_depth, child, 'Subject')
                else:
                    add_role(base_depth, child, 'Direct Object')
            elif child.label == 'S':
                # Coordinated S — recurse without labeling the S itself
                process_s_level(child, base_depth)
            elif child.label in ('CONJ', 'AUX'):
                pass

    # --- Main dispatch: always use unified process_s_level ---
    if tree.label == 'S':
        process_s_level(tree, 0)

    return roles


def assign_roles_for_entry(entry):
    if entry.get('skip'):
        return {}
    tree = parse_bracket(entry['bracket'])
    if tree is None:
        print(f"  WARNING: Could not parse: {entry['bracket'][:60]}...")
        return {}
    return assign_roles_to_tree(tree)


# --- Validation ---

def validate_against_ch7(ch7_path):
    with open(ch7_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    mismatches = []
    for entry in data['sentences']:
        if entry.get('skip') or not entry['roles']:
            continue
        computed = assign_roles_for_entry(entry)
        if computed != entry['roles']:
            mismatches.append({
                'filename': entry['filename'],
                'bracket': entry['bracket'][:80],
                'expected': entry['roles'],
                'computed': computed,
            })
    return mismatches


# --- Main ---

def main():
    parser = argparse.ArgumentParser(description='Assign roles to bracket notation entries')
    parser.add_argument('--input-dir', '-i', default='data/static/table-roles',
                        help='Directory containing chXX_tables.json files')
    parser.add_argument('--validate-ch7', action='store_true',
                        help='Validate against manually authored Ch7 roles')
    parser.add_argument('--dry-run', action='store_true',
                        help='Print roles without writing files')
    parser.add_argument('--chapters', '-c', nargs='*', type=int,
                        help='Specific chapters to process (default: all)')
    args = parser.parse_args()

    input_dir = Path(args.input_dir)

    if args.validate_ch7:
        ch7_path = input_dir / 'ch07_tables.json'
        if not ch7_path.exists():
            print("ERROR: ch07_tables.json not found")
            sys.exit(1)
        mismatches = validate_against_ch7(ch7_path)
        if mismatches:
            print(f"VALIDATION FAILED: {len(mismatches)} mismatch(es)")
            for m in mismatches:
                print(f"\n  {m['filename']}: {m['bracket']}")
                print(f"    Expected: {m['expected']}")
                print(f"    Computed: {m['computed']}")
            sys.exit(1)
        else:
            print("VALIDATION PASSED: All Ch7 entries match")
            return

    chapters = args.chapters or [5, 6, 8, 9, 10, 11, 12, 13, 14]
    total_assigned = 0
    total_skipped = 0

    for ch_num in chapters:
        json_path = input_dir / f'ch{ch_num:02d}_tables.json'
        if not json_path.exists():
            print(f"  Ch{ch_num:02d}: not found, skipping")
            continue

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assigned = 0
        skipped = 0
        for entry in data['sentences']:
            if entry.get('skip'):
                skipped += 1
                continue
            new_roles = assign_roles_for_entry(entry)
            if new_roles:
                entry['roles'] = new_roles
                assigned += 1
            else:
                skipped += 1

        total_assigned += assigned
        total_skipped += skipped

        if args.dry_run:
            print(f"\n  Ch{ch_num:02d}: {assigned} assigned, {skipped} skipped")
            for entry in data['sentences']:
                if entry.get('skip') or not entry['roles']:
                    continue
                print(f"    {entry['filename']}: {entry['roles']}")
        else:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"  Ch{ch_num:02d}: {assigned} assigned, {skipped} skipped -> {json_path.name}")

    print(f"\nTotal: {total_assigned} assigned, {total_skipped} skipped")


if __name__ == '__main__':
    main()
