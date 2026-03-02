#!/usr/bin/env python3
"""
Generate Morphology Bonus Assignment .docx files (student version and answer key).
No diagrams — students divide 20 words into morphemes and label each free or bound.
"""

from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SCRIPT_DIR = Path(__file__).parent


# =============================================================================
# HELPERS
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


def set_col_width(table, col_idx, width_inches):
    """Set a column width via XML (python-docx doesn't expose this directly)."""
    for row in table.rows:
        cell = row.cells[col_idx]
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        tcW = OxmlElement('w:tcW')
        tcW.set(qn('w:w'), str(int(width_inches * 1440)))
        tcW.set(qn('w:type'), 'dxa')
        tcPr.append(tcW)


# =============================================================================
# WORD DATA
# Each entry: word, breakdown (list of morphemes), labels (list of free/bound)
# breakdown uses - prefix for prefixes, suffix for suffixes, bare for free roots
# =============================================================================

WORDS = [
    {
        "word": "playful",
        "morphemes": ["play", "-ful"],
        "labels":    ["free", "bound"],
        "note": "",
    },
    {
        "word": "darkness",
        "morphemes": ["dark", "-ness"],
        "labels":    ["free", "bound"],
        "note": "",
    },
    {
        "word": "quickly",
        "morphemes": ["quick", "-ly"],
        "labels":    ["free", "bound"],
        "note": "",
    },
    {
        "word": "kindness",
        "morphemes": ["kind", "-ness"],
        "labels":    ["free", "bound"],
        "note": "",
    },
    {
        "word": "bookcase",
        "morphemes": ["book", "case"],
        "labels":    ["free", "free"],
        "note": "compound noun",
    },
    {
        "word": "truthful",
        "morphemes": ["truth", "-ful"],
        "labels":    ["free", "bound"],
        "note": "",
    },
    {
        "word": "powerless",
        "morphemes": ["power", "-less"],
        "labels":    ["free", "bound"],
        "note": "",
    },
    {
        "word": "misunderstand",
        "morphemes": ["mis-", "understand"],
        "labels":    ["bound", "free"],
        "note": "understand is a single morpheme in modern English",
    },
    {
        "word": "rebuilding",
        "morphemes": ["re-", "build", "-ing"],
        "labels":    ["bound", "free", "bound"],
        "note": "",
    },
    {
        "word": "teachers",
        "morphemes": ["teach", "-er", "-s"],
        "labels":    ["free", "bound", "bound"],
        "note": "",
    },
    {
        "word": "carefully",
        "morphemes": ["care", "-ful", "-ly"],
        "labels":    ["free", "bound", "bound"],
        "note": "",
    },
    {
        "word": "unfriendly",
        "morphemes": ["un-", "friend", "-ly"],
        "labels":    ["bound", "free", "bound"],
        "note": "",
    },
    {
        "word": "notebooks",
        "morphemes": ["note", "book", "-s"],
        "labels":    ["free", "free", "bound"],
        "note": "compound noun + plural",
    },
    {
        "word": "unlockable",
        "morphemes": ["un-", "lock", "-able"],
        "labels":    ["bound", "free", "bound"],
        "note": "",
    },
    {
        "word": "songwriter",
        "morphemes": ["song", "write", "-er"],
        "labels":    ["free", "free", "bound"],
        "note": "compound base + derivational suffix",
    },
    {
        "word": "replayable",
        "morphemes": ["re-", "play", "-able"],
        "labels":    ["bound", "free", "bound"],
        "note": "",
    },
    {
        "word": "unhappiness",
        "morphemes": ["un-", "happy", "-ness"],
        "labels":    ["bound", "free", "bound"],
        "note": "",
    },
    {
        "word": "unpredictable",
        "morphemes": ["un-", "predict", "-able"],
        "labels":    ["bound", "free", "bound"],
        "note": "",
    },
    {
        "word": "disrespectful",
        "morphemes": ["dis-", "respect", "-ful"],
        "labels":    ["bound", "free", "bound"],
        "note": "",
    },
    {
        "word": "disagreements",
        "morphemes": ["dis-", "agree", "-ment", "-s"],
        "labels":    ["bound", "free", "bound", "bound"],
        "note": "",
    },
]


# =============================================================================
# DOCUMENT BUILDER
# =============================================================================

def create_document(is_answer_key=False):
    doc = Document()

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
    title_text = "ENGL 3110 \u2014 Morphology Bonus Assignment \u2014 Spring 2026"
    if is_answer_key:
        title_text += " \u2014 ANSWER KEY"

    title = doc.add_heading(title_text, level=1)
    for run in title.runs:
        run.font.size = Pt(16)
    set_paragraph_spacing(title, space_before=0, space_after=4)

    p = doc.add_paragraph()
    add_run(p, "Total Points: 20  \u2022  1 point per word", bold=True, font_size=11)
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
    add_run(p, "For each word in the table below, complete two columns:", font_size=11)

    for item in [
        ("1. ", "Morpheme Breakdown: ", "Divide the word into its individual morphemes. Use + to separate them. Mark prefixes with a leading hyphen (un-) and suffixes with a trailing hyphen (-ness)."),
        ("2. ", "Free or Bound: ", "Label each morpheme as either free (can stand alone as a word) or bound (must attach to another morpheme). List labels in the same order as your breakdown."),
    ]:
        p = doc.add_paragraph()
        add_run(p, item[0], bold=True, font_size=11)
        add_run(p, item[1], bold=True, font_size=11)
        add_run(p, item[2], font_size=11)

    p = doc.add_paragraph()
    add_run(p, "Example: ", bold=True, font_size=10)
    set_paragraph_spacing(p, space_before=4, space_after=2)

    # Example table
    ex_table = doc.add_table(rows=2, cols=3)
    ex_table.style = 'Table Grid'
    ex_table.alignment = WD_TABLE_ALIGNMENT.LEFT

    headers = ["Word", "Morpheme Breakdown", "Free or Bound?"]
    for j, h in enumerate(headers):
        cell = ex_table.rows[0].cells[j]
        cell.text = ""
        p2 = cell.paragraphs[0]
        add_run(p2, h, bold=True, font_size=10)
        set_cell_shading(cell, "E8E8E8")

    ex_data = ["unhelpful", "un- + help + -ful", "bound, free, bound"]
    for j, val in enumerate(ex_data):
        cell = ex_table.rows[1].cells[j]
        cell.text = ""
        p2 = cell.paragraphs[0]
        add_run(p2, val, font_size=10, italic=(j == 0))

    p = doc.add_paragraph()
    set_paragraph_spacing(p, space_before=4, space_after=4)

    if is_answer_key:
        p = doc.add_paragraph()
        add_run(p, "Note: ", bold=True, font_size=10)
        add_run(p, "Italicized text in the Notes column explains any non-obvious analyses.", italic=True, font_size=10)
        set_paragraph_spacing(p, space_before=0, space_after=6)

    # -------------------------------------------------------------------------
    # MAIN TABLE
    # -------------------------------------------------------------------------
    num_cols = 5 if is_answer_key else 4
    num_rows = len(WORDS) + 1  # +1 for header row

    table = doc.add_table(rows=num_rows, cols=num_cols)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.LEFT

    # Header row
    col_headers = ["#", "Word", "Morpheme Breakdown", "Free or Bound?", "Notes"]
    for j, h in enumerate(col_headers[:num_cols]):
        cell = table.rows[0].cells[j]
        cell.text = ""
        p2 = cell.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER if j == 0 else WD_ALIGN_PARAGRAPH.LEFT
        add_run(p2, h, bold=True, font_size=10)
        set_cell_shading(cell, "E8E8E8")

    # Data rows
    for i, entry in enumerate(WORDS):
        row = table.rows[i + 1]

        # Column 0: number
        cell = row.cells[0]
        cell.text = ""
        p2 = cell.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_run(p2, str(i + 1), font_size=10)

        # Column 1: word
        cell = row.cells[1]
        cell.text = ""
        p2 = cell.paragraphs[0]
        add_run(p2, entry["word"], font_size=10, bold=True)

        # Column 2: morpheme breakdown
        cell = row.cells[2]
        cell.text = ""
        p2 = cell.paragraphs[0]
        if is_answer_key:
            breakdown = " + ".join(entry["morphemes"])
            add_run(p2, breakdown, font_size=10)

        # Column 3: labels
        cell = row.cells[3]
        cell.text = ""
        p2 = cell.paragraphs[0]
        if is_answer_key:
            label_str = ", ".join(entry["labels"])
            add_run(p2, label_str, font_size=10)

        # Column 4 (answer key only): notes
        if is_answer_key:
            cell = row.cells[4]
            cell.text = ""
            p2 = cell.paragraphs[0]
            if entry["note"]:
                add_run(p2, entry["note"], font_size=9, italic=True)

    # Shade alternating rows lightly for readability
    for i in range(len(WORDS)):
        if (i + 1) % 2 == 0:
            for j in range(num_cols):
                set_cell_shading(table.rows[i + 1].cells[j], "F5F5F5")

    # -------------------------------------------------------------------------
    # SCORING NOTE (student version only)
    # -------------------------------------------------------------------------
    if not is_answer_key:
        p = doc.add_paragraph()
        set_paragraph_spacing(p, space_before=8, space_after=2)
        add_run(p, "Scoring: ", bold=True, font_size=10)
        add_run(p, "1 point per word. Full credit requires correctly identifying ALL morphemes and labeling each one.", font_size=10)

    return doc


def main():
    print("=" * 60)
    print("Generating Morphology Bonus Assignment .docx files")
    print("=" * 60)

    student_path = SCRIPT_DIR / "ENGL 3110 - S26 - Morphology Bonus Assignment.docx"
    print(f"\nGenerating student version: {student_path.name}")
    doc = create_document(is_answer_key=False)
    doc.save(str(student_path))
    print(f"  Saved: {student_path}")

    key_path = SCRIPT_DIR / "ENGL 3110 - S26 - Morphology Bonus Assignment - Answer Key.docx"
    print(f"\nGenerating answer key: {key_path.name}")
    doc = create_document(is_answer_key=True)
    doc.save(str(key_path))
    print(f"  Saved: {key_path}")

    print("\nDone!")


if __name__ == "__main__":
    main()
