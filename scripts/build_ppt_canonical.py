#!/usr/bin/env python3
"""Build canonical JSON files for the 23 PPT sentences in data/trees/ppt/.

Roles authored against the actual rendered editable-cell layout (dumped via
dump_ppt_table_layout.py). Every editable cell receives a role label.

Schema mirrors data/trees/ch14/*.json (canonical SSOT). The PPT renderer loads
from here instead of from hardcoded ROLE_ASSIGNMENTS.
"""
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PPT_DATA = PROJECT_ROOT / "data" / "static" / "ppt_diagram_data.json"
OUT_DIR = PROJECT_ROOT / "data" / "trees" / "ppt"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# Roles authored from the editable-cell layout dump (data/static/ppt-table-layouts.json)
ROLES = {
    "adv_01": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"2": "Adverbial", "5": "Adverbial"},
        "2": {"3": "Obj Prep", "6": "Direct Object"},
        "3": {"7": "Adjectival"},
    },
    "adv_02": {
        "0": {"0": "Adverbial", "3": "Subject", "4": "Predicate"},
        "1": {"1": "Direct Object", "5": "Direct Object"},
    },
    "adv_03": {
        "0": {"0": "Adverbial", "5": "Subject", "6": "Predicate"},
        "1": {"2": "Adjectival", "7": "Direct Object"},
        "2": {"3": "Obj Prep"},
    },
    "adv_04_preview": {
        "0": {"0": "Subject", "4": "Predicate"},
        "1": {"2": "Adjectival"},
        "2": {"2": "Subject", "3": "Predicate"},
    },
    "adv_05_preview": {
        "0": {"0": "Subject", "2": "Predicate"},
        "1": {"3": "Adverbial", "5": "Direct Object"},
        "2": {"7": "Adjectival"},
        "3": {"7": "Direct Object", "8": "Subject", "9": "Predicate"},
    },
    "adv_06_preview": {
        "0": {"0": "Subject", "5": "Predicate"},
        "1": {"2": "Adjectival", "5": "Adverbial"},
        "2": {"2": "Subject", "3": "Predicate"},
    },
    "adj_01": {
        "0": {"0": "Subject", "5": "Predicate"},
        "1": {"2": "Adjectival", "6": "Subject Complement"},
        "2": {"3": "Direct Object", "7": "Adjectival", "9": "Adjectival"},
        "3": {"10": "Obj Prep"},
    },
    "adj_02": {
        "0": {"0": "Subject", "3": "Predicate"},
        "1": {"1": "Adjectival", "4": "Adverbial"},
        "2": {"5": "Obj Prep"},
        "3": {"6": "Adjectival"},
    },
    "adj_03": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"2": "Adverbial"},
        "2": {"3": "Obj Prep"},
        "3": {"4": "Adjectival"},
        "4": {"5": "Adverbial"},
        "5": {"6": "Obj Prep"},
    },
    "adj_04": {
        "0": {"0": "Subject", "4": "Predicate"},
        "1": {"1": "Adjectival", "6": "Adverbial"},
        "2": {"1": "Adverbial", "7": "Obj Prep"},
    },
    "adj_05": {
        "0": {"0": "Subject", "6": "Predicate"},
        "1": {"2": "Adjectival", "7": "Direct Object"},
        "2": {"2": "Subject", "3": "Predicate", "8": "Adjectival"},
        "3": {"4": "Direct Object"},
    },
    "adj_06": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"2": "Adverbial"},
        "2": {"3": "Obj Prep"},
        "3": {"5": "Adjectival"},
        "4": {"5": "Relativizer", "6": "Subject", "8": "Predicate"},
        "5": {"9": "Subject Complement"},
    },
    "adj_07": {
        "0": {"0": "Subject", "5": "Predicate"},
        "1": {"2": "Adjectival", "6": "Adverbial"},
        "2": {"2": "Direct Object", "3": "Subject", "4": "Predicate"},
    },
    "adj_08": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"3": "Direct Object"},
        "2": {"5": "Adjectival"},
        "3": {"5": "Relativizer", "6": "Subject", "7": "Predicate"},
        "4": {"9": "Direct Object"},
    },
    "adj_09": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"3": "Direct Object"},
        "2": {"5": "Adjectival"},
        "3": {"6": "Obj Prep"},
        "4": {"8": "Adjectival"},
        "5": {"8": "Subject", "9": "Predicate"},
        "6": {"9": "Adverbial", "11": "Direct Object"},
    },
    "adj_10_preview": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"2": "Direct Object"},
        "2": {"2": "Subject", "3": "Predicate"},
    },
    "adj_11_preview": {
        "0": {"0": "Subject", "3": "Predicate"},
        "1": {"0": "Subject", "1": "Predicate", "4": "Subject Complement"},
    },
    "adj_12_preview": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"2": "Direct Object"},
        "2": {"2": "Subject", "4": "Predicate"},
        "3": {"5": "Subject Complement"},
    },
    "nom_01": {
        "0": {"0": "Subject", "3": "Predicate"},
        "1": {"1": "Adverbial", "4": "Subject Complement"},
        "2": {"2": "Obj Prep"},
    },
    "nom_02": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"2": "Direct Object"},
        "2": {"3": "Direct Object"},
        "3": {"4": "Adjectival"},
    },
    "nom_03": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"3": "Direct Object"},
        "2": {"4": "Subject", "6": "Predicate"},
        "3": {"8": "Subject Complement"},
    },
    "nom_04": {
        "0": {"0": "Subject", "1": "Predicate"},
        "1": {"2": "Direct Object", "7": "Coordinator", "8": "Direct Object"},
        "2": {"3": "Subject", "5": "Predicate", "9": "Subject", "10": "Predicate"},
        "3": {"6": "Subject Complement"},
    },
    "nom_05": {
        "0": {"0": "Subject", "3": "Predicate"},
        "1": {"1": "Subject", "2": "Predicate", "4": "Subject Complement"},
        "2": {"5": "Adjectival"},
        "3": {"6": "Obj Prep"},
    },
}


def main():
    with open(PPT_DATA) as f:
        data = json.load(f)

    written = 0
    for s in data["sentences"]:
        sid = s["id"]
        roles = ROLES.get(sid)
        if not roles:
            print(f"SKIP {sid}: no roles authored")
            continue

        canonical = {
            "id": sid,
            "source": "ppt",
            "sentence": s["sentence"],
            "context": s.get("context", ""),
            "bracket": s["bracket"],
            "roles": roles,
            "slides": s.get("slides", []),
            "table_filename": sid,
            "diagram_filename": sid,
            "outputs": ["table_png", "tree_png"],
            "overrides": None,
        }
        out = OUT_DIR / f"{sid}.json"
        out.write_text(json.dumps(canonical, indent=2))
        written += 1

    print(f"Wrote {written} canonical files to {OUT_DIR}")


if __name__ == "__main__":
    main()
