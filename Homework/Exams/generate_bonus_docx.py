#!/usr/bin/env python3
"""
Generate Bonus Assignment .docx files (student version and answer key).
Run generate_bonus_diagrams.py first to create the PNG files.
"""

from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SCRIPT_DIR = Path(__file__).parent
DIAGRAM_DIR = SCRIPT_DIR / "diagrams"


# =============================================================================
# HELPERS (same pattern as exam scripts)
# =============================================================================

def set_paragraph_spacing(paragraph, space_before=0, space_after=0):
    pPr = paragraph._p.get_or_add_pPr()
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:before'), str(int(space_before * 20)))
    spacing.set(qn('w:after'), str(int(space_after * 20)))
    pPr.append(spacing)


def set_cell_shading(cell, color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), color)
    shading.set(qn('w:val'), 'clear')
    tcPr.append(shading)


def add_run(paragraph, text, bold=False, italic=False, font_size=None, font_name=None, color=None):
    run = paragraph.add_run(text)
    if bold:
        run.bold = True
    if italic:
        run.italic = True
    if font_size:
        run.font.size = Pt(font_size)
    if font_name:
        run.font.name = font_name
    if color:
        run.font.color.rgb = RGBColor(*color)
    return run


def add_section_header(doc, text, level=2, font_size=14):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.size = Pt(font_size)
    return h


def compute_spans(labels):
    """Convert flat label list to (label, span_count, start_index) tuples."""
    spans = []
    i = 0
    while i < len(labels):
        label = labels[i]
        if label:
            span = 1
            while i + span < len(labels) and labels[i + span] == "":
                span += 1
            spans.append((label, span, i))
            i += span
        else:
            i += 1
    return spans


def blank_labels(labels):
    """Convert answer labels to blank labels preserving span structure."""
    return ["" if label == "" else " " for label in labels]


def add_labeling_table(doc, words, pos_labels=None, phrase_labels=None, role_labels=None, font_size=10):
    """Add a 4-row sentence labeling table (Role, Phrase, Word, POS)."""
    num_cols = len(words) + 1
    table = doc.add_table(rows=4, cols=num_cols)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.LEFT

    row_headers = ["Role", "Phrase", "Word", "POS"]
    row_data = [role_labels, phrase_labels, words, pos_labels]

    for i, (header, data) in enumerate(zip(row_headers, row_data)):
        cell = table.rows[i].cells[0]
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        add_run(p, header, bold=True, font_size=font_size)
        set_cell_shading(cell, "E8E8E8")

        if i <= 1 and data:
            spans = compute_spans(data)
            for label, span, start_idx in spans:
                col_start = start_idx + 1
                col_end = col_start + span - 1
                if span > 1:
                    table.rows[i].cells[col_start].merge(table.rows[i].cells[col_end])
                merged_cell = table.rows[i].cells[col_start]
                for paragraph in merged_cell.paragraphs:
                    for run in paragraph.runs:
                        run.text = ""
                p = merged_cell.paragraphs[0]
                p.text = ""
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                add_run(p, label, font_size=font_size)
        else:
            for j, val in enumerate(data if data else [""] * len(words)):
                cell = table.rows[i].cells[j + 1]
                cell.text = ""
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                if i == 2:
                    add_run(p, val, font_size=font_size)
                elif data:
                    add_run(p, val, font_size=font_size)

    return table


def add_diagram_image(doc, image_name, width_inches=5.0):
    img_path = DIAGRAM_DIR / f"{image_name}.png"
    if img_path.exists():
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.add_picture(str(img_path), width=Inches(width_inches))
        set_paragraph_spacing(p, space_before=4, space_after=4)
        return p
    else:
        p = doc.add_paragraph(f"[Diagram not found: {image_name}.png]")
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        return p


def add_diagram_box(doc):
    """Add a bordered blank area for students to paste their diagram."""
    p = doc.add_paragraph()
    add_run(p, "Diagram: ", bold=True, font_size=10)
    add_run(p, "Use SyntaxTreeHybrid to create your tree diagram. Paste or attach your PNG image below.", font_size=10, italic=True)
    set_paragraph_spacing(p, space_before=4, space_after=2)

    # Blank space (4 empty paragraphs)
    for _ in range(4):
        spacer = doc.add_paragraph()
        set_paragraph_spacing(spacer, space_before=0, space_after=0)

    return p


# =============================================================================
# SENTENCE DATA
# =============================================================================

SENTENCES = [
    {
        "num": 1,
        "sentence": "The tall student slept quietly in the library.",
        "words": ["The", "tall", "student", "slept", "quietly", "in", "the", "library"],
        "pos":     ["DET", "ADJ", "N",       "V",      "ADV",     "PREP", "DET", "N"],
        "phrases": ["NP",  "",    "",         "VP",     "ADVP",    "PP",   "",    ""],
        "roles":   ["Subject", "", "", "Predicate", "", "", "", ""],
        "bracket": "[S [NP [DET The] [ADJP [ADJ tall]] [N student]] [VP [V slept] [ADVP [ADV quietly]] [PP [PREP in] [NP [DET the] [N library]]]]]",
        "diagram": "bonus_q01_student_slept",
        "width": 5.0,
    },
    {
        "num": 2,
        "sentence": "The young children played happily in the yard.",
        "words": ["The", "young", "children", "played", "happily", "in", "the", "yard"],
        "pos":     ["DET", "ADJ",   "N",        "V",      "ADV",     "PREP", "DET", "N"],
        "phrases": ["NP",  "",      "",          "VP",     "ADVP",    "PP",   "",    ""],
        "roles":   ["Subject", "", "", "Predicate", "", "", "", ""],
        "bracket": "[S [NP [DET The] [ADJP [ADJ young]] [N children]] [VP [V played] [ADVP [ADV happily]] [PP [PREP in] [NP [DET the] [N yard]]]]]",
        "diagram": "bonus_q02_children_played",
        "width": 5.0,
    },
    {
        "num": 3,
        "sentence": "She ran very quickly through the dark forest.",
        "words": ["She", "ran", "very",  "quickly", "through", "the", "dark", "forest"],
        "pos":     ["PRO", "V",  "ADV",  "ADV",     "PREP",    "DET", "ADJ",  "N"],
        "phrases": ["NP",  "VP", "ADVP", "",        "PP",      "",    "",     ""],
        "roles":   ["Subject", "Predicate", "", "", "", "", "", ""],
        "bracket": "[S [NP [PRO She]] [VP [V ran] [ADVP [ADV very] [ADV quickly]] [PP [PREP through] [NP [DET the] [ADJP [ADJ dark]] [N forest]]]]]",
        "diagram": "bonus_q03_she_ran",
        "width": 5.5,
    },
    {
        "num": 4,
        "sentence": "The old dog rested near the warm fireplace.",
        "words": ["The", "old", "dog", "rested", "near", "the", "warm",  "fireplace"],
        "pos":     ["DET", "ADJ", "N",  "V",      "PREP", "DET", "ADJ",  "N"],
        "phrases": ["NP",  "",    "",   "VP",     "PP",   "",    "",     ""],
        "roles":   ["Subject", "", "", "Predicate", "", "", "", ""],
        "bracket": "[S [NP [DET The] [ADJP [ADJ old]] [N dog]] [VP [V rested] [PP [PREP near] [NP [DET the] [ADJP [ADJ warm]] [N fireplace]]]]]",
        "diagram": "bonus_q04_dog_rested",
        "width": 5.0,
    },
    {
        "num": 5,
        "sentence": "The bright stars shone above the quiet town.",
        "words": ["The", "bright", "stars", "shone", "above", "the", "quiet", "town"],
        "pos":     ["DET", "ADJ",   "N",     "V",     "PREP",  "DET", "ADJ",   "N"],
        "phrases": ["NP",  "",      "",      "VP",    "PP",    "",    "",      ""],
        "roles":   ["Subject", "", "", "Predicate", "", "", "", ""],
        "bracket": "[S [NP [DET The] [ADJP [ADJ bright]] [N stars]] [VP [V shone] [PP [PREP above] [NP [DET the] [ADJP [ADJ quiet]] [N town]]]]]",
        "diagram": "bonus_q05_stars_shone",
        "width": 5.0,
    },
    {
        "num": 6,
        "sentence": "They walked very slowly along the narrow path.",
        "words": ["They", "walked", "very",  "slowly", "along", "the", "narrow", "path"],
        "pos":     ["PRO",  "V",     "ADV",  "ADV",    "PREP",  "DET", "ADJ",    "N"],
        "phrases": ["NP",   "VP",    "ADVP", "",       "PP",    "",    "",       ""],
        "roles":   ["Subject", "Predicate", "", "", "", "", "", ""],
        "bracket": "[S [NP [PRO They]] [VP [V walked] [ADVP [ADV very] [ADV slowly]] [PP [PREP along] [NP [DET the] [ADJP [ADJ narrow]] [N path]]]]]",
        "diagram": "bonus_q06_they_walked",
        "width": 5.5,
    },
    {
        "num": 7,
        "sentence": "The nervous professor spoke clearly at the podium.",
        "words": ["The", "nervous",  "professor", "spoke", "clearly", "at",   "the", "podium"],
        "pos":     ["DET", "ADJ",    "N",          "V",     "ADV",    "PREP", "DET", "N"],
        "phrases": ["NP",  "",       "",            "VP",    "ADVP",   "PP",   "",    ""],
        "roles":   ["Subject", "", "", "Predicate", "", "", "", ""],
        "bracket": "[S [NP [DET The] [ADJP [ADJ nervous]] [N professor]] [VP [V spoke] [ADVP [ADV clearly]] [PP [PREP at] [NP [DET the] [N podium]]]]]",
        "diagram": "bonus_q07_professor_spoke",
        "width": 5.0,
    },
    {
        "num": 8,
        "sentence": "Small birds sang loudly near the old oak.",
        "words": ["Small", "birds", "sang", "loudly", "near", "the", "old", "oak"],
        "pos":     ["ADJ",   "N",    "V",    "ADV",    "PREP", "DET", "ADJ", "N"],
        "phrases": ["NP",    "",     "VP",   "ADVP",   "PP",   "",    "",    ""],
        "roles":   ["Subject", "", "Predicate", "", "", "", "", ""],
        "bracket": "[S [NP [ADJP [ADJ Small]] [N birds]] [VP [V sang] [ADVP [ADV loudly]] [PP [PREP near] [NP [DET the] [ADJP [ADJ old]] [N oak]]]]]",
        "diagram": "bonus_q08_birds_sang",
        "width": 5.0,
    },
    {
        "num": 9,
        "sentence": "He waited very patiently outside the large building.",
        "words": ["He",  "waited", "very",  "patiently", "outside", "the", "large", "building"],
        "pos":     ["PRO", "V",    "ADV",  "ADV",       "PREP",    "DET", "ADJ",   "N"],
        "phrases": ["NP",  "VP",   "ADVP", "",          "PP",      "",    "",      ""],
        "roles":   ["Subject", "Predicate", "", "", "", "", "", ""],
        "bracket": "[S [NP [PRO He]] [VP [V waited] [ADVP [ADV very] [ADV patiently]] [PP [PREP outside] [NP [DET the] [ADJP [ADJ large]] [N building]]]]]",
        "diagram": "bonus_q09_he_waited",
        "width": 5.5,
    },
    {
        "num": 10,
        "sentence": "The tired runner collapsed suddenly at the barrier.",
        "words": ["The", "tired", "runner", "collapsed", "suddenly", "at",   "the", "barrier"],
        "pos":     ["DET", "ADJ",  "N",      "V",         "ADV",     "PREP", "DET", "N"],
        "phrases": ["NP",  "",     "",       "VP",        "ADVP",    "PP",   "",    ""],
        "roles":   ["Subject", "", "", "Predicate", "", "", "", ""],
        "bracket": "[S [NP [DET The] [ADJP [ADJ tired]] [N runner]] [VP [V collapsed] [ADVP [ADV suddenly]] [PP [PREP at] [NP [DET the] [N barrier]]]]]",
        "diagram": "bonus_q10_runner_collapsed",
        "width": 5.0,
    },
]


# =============================================================================
# DOCUMENT BUILDER
# =============================================================================

def build_abbrev_table(doc):
    """Add the standard abbreviation key table."""
    p = doc.add_paragraph()
    add_run(p, "Abbreviation Key", bold=True, font_size=11)
    set_paragraph_spacing(p, space_before=6, space_after=2)

    abbrev_table = doc.add_table(rows=8, cols=3)
    abbrev_table.style = 'Table Grid'

    headers = ["Parts of Speech", "Phrase Types", "Roles"]
    abbrev_data = [
        ["Noun = N",          "Noun Phrase = NP",          "Subject = Subj"],
        ["Verb = V",          "Verb Phrase = VP",          "Predicate = Pred"],
        ["Adjective = ADJ",   "Adjective Phrase = ADJP",   ""],
        ["Adverb = ADV",      "Adverb Phrase = ADVP",      ""],
        ["Pronoun = PRO",     "Prepositional Phrase = PP",  ""],
        ["Determiner = DET",  "Sentence = S",              ""],
        ["Preposition = PREP","",                           ""],
    ]

    for j, h in enumerate(headers):
        cell = abbrev_table.rows[0].cells[j]
        cell.text = ""
        p = cell.paragraphs[0]
        add_run(p, h, bold=True, font_size=9)
        set_cell_shading(cell, "E8E8E8")

    for i, row_vals in enumerate(abbrev_data):
        for j, val in enumerate(row_vals):
            cell = abbrev_table.rows[i + 1].cells[j]
            cell.text = ""
            p = cell.paragraphs[0]
            add_run(p, val, font_size=9)


def build_notes(doc):
    """Add the standard notes block."""
    p = doc.add_paragraph()
    add_run(p, "Notes:", bold=True, font_size=10)
    notes = [
        "In the Phrase row, label the main verb as VP. The VP label in the table applies to just the main verb itself.",
        "In the Role row, label the subject noun phrase as Subject and the main verb as Predicate. Leave other cells empty.",
        "Always include a Phrase-level label for every noun, verb, adjective, adverb, and preposition.",
        "Determiners (DET) group under the NP — they do not get their own Phrase label.",
    ]
    for note in notes:
        bp = doc.add_paragraph(style='List Bullet')
        bp.text = ""
        add_run(bp, note, font_size=10)


def create_document(is_answer_key=False):
    doc = Document()

    # Default font
    style = doc.styles['Normal']
    style.font.name = 'Garamond'
    style.font.size = Pt(11)
    style.paragraph_format.space_after = Pt(4)

    for i in range(1, 4):
        h_style = doc.styles[f'Heading {i}']
        h_style.font.name = 'Open Sans'
        h_style.font.bold = True

    # -------------------------------------------------------------------------
    # HEADER
    # -------------------------------------------------------------------------
    title_text = "ENGL 3110 \u2014 Bonus Assignment \u2014 Spring 2026"
    if is_answer_key:
        title_text += " \u2014 ANSWER KEY"

    title = doc.add_heading(title_text, level=1)
    for run in title.runs:
        run.font.size = Pt(16)
    set_paragraph_spacing(title, space_before=0, space_after=4)

    p = doc.add_paragraph()
    add_run(p, "Total Points: 20  \u2022  2 points per sentence", bold=True, font_size=11)
    set_paragraph_spacing(p, space_before=0, space_after=4)

    if not is_answer_key:
        p = doc.add_paragraph()
        add_run(p, "STUDENT NAME: ", bold=True, font_size=11)
        add_run(p, "_" * 55, font_size=11)
        set_paragraph_spacing(p, space_before=0, space_after=6)

    # -------------------------------------------------------------------------
    # INSTRUCTIONS
    # -------------------------------------------------------------------------
    add_section_header(doc, "Instructions", level=2, font_size=13)

    p = doc.add_paragraph()
    add_run(p, "For each sentence below, complete two tasks:", font_size=11)

    for item in [
        ("1. ", "Complete the labeling table ", "by filling in the Role, Phrase, and Part of Speech (POS) rows."),
        ("2. ", "Create a syntax tree diagram ", "using SyntaxTreeHybrid. In the student version, paste or attach your diagram in the space provided. In the answer key, the completed diagram is shown."),
    ]:
        p = doc.add_paragraph()
        add_run(p, item[0], bold=True, font_size=11)
        add_run(p, item[1], bold=True, font_size=11)
        add_run(p, item[2], font_size=11)

    p = doc.add_paragraph()
    add_run(p, "Scoring (per sentence): ", bold=True, font_size=10)
    add_run(p, "1 point for a correct labeling table  \u2022  1 point for a correct diagram", font_size=10)
    set_paragraph_spacing(p, space_before=2, space_after=6)

    build_abbrev_table(doc)

    p = doc.add_paragraph()
    set_paragraph_spacing(p, space_before=4, space_after=0)
    build_notes(doc)

    # -------------------------------------------------------------------------
    # SENTENCES
    # -------------------------------------------------------------------------
    for q in SENTENCES:
        doc.add_page_break()

        p = doc.add_paragraph()
        add_run(p, f"Sentence {q['num']}: ", bold=True, font_size=12)
        add_run(p, f"(2 pts) ", font_size=11)
        add_run(p, q["sentence"], italic=True, font_size=11)
        set_paragraph_spacing(p, space_before=6, space_after=4)

        # Labeling table
        if is_answer_key:
            add_labeling_table(
                doc, q["words"],
                pos_labels=q["pos"],
                phrase_labels=q["phrases"],
                role_labels=q["roles"],
                font_size=10,
            )
        else:
            add_labeling_table(
                doc, q["words"],
                phrase_labels=blank_labels(q["phrases"]),
                role_labels=blank_labels(q["roles"]),
                font_size=10,
            )

        # Bracket notation
        p = doc.add_paragraph()
        if is_answer_key:
            add_run(p, "Bracket notation: ", bold=True, font_size=10)
            add_run(p, q["bracket"], font_size=9, font_name="Consolas")
        else:
            add_run(p, "Bracket notation: ", bold=True, font_size=10)
            add_run(p, "_" * 70, font_size=10)
        set_paragraph_spacing(p, space_before=4, space_after=2)

        # Diagram
        if is_answer_key:
            add_diagram_image(doc, q["diagram"], width_inches=q["width"])
        else:
            add_diagram_box(doc)

    return doc


def main():
    print("=" * 60)
    print("Generating Bonus Assignment .docx files")
    print("=" * 60)

    student_path = SCRIPT_DIR / "ENGL 3110 - S26 - Bonus Assignment.docx"
    print(f"\nGenerating student version: {student_path.name}")
    doc = create_document(is_answer_key=False)
    doc.save(str(student_path))
    print(f"  Saved: {student_path}")

    key_path = SCRIPT_DIR / "ENGL 3110 - S26 - Bonus Assignment - Answer Key.docx"
    print(f"\nGenerating answer key: {key_path.name}")
    doc = create_document(is_answer_key=True)
    doc.save(str(key_path))
    print(f"  Saved: {key_path}")

    print("\nDone!")


if __name__ == "__main__":
    main()
