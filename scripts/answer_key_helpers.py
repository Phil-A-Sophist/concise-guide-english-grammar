#!/usr/bin/env python3
"""
Shared helper functions for generating answer key and overhead .docx files.
All chapter answer key scripts should import from this module.
"""

from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def set_paragraph_spacing(paragraph, space_before=0, space_after=0):
    """Set paragraph spacing in points."""
    pPr = paragraph._p.get_or_add_pPr()
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:before'), str(int(space_before * 20)))
    spacing.set(qn('w:after'), str(int(space_after * 20)))
    pPr.append(spacing)


def add_spacer_row(doc):
    """Add a blank spacer paragraph in Times New Roman 20 (no text, for instructor notes)."""
    p = doc.add_paragraph()
    run = p.add_run()
    run.font.name = 'Times New Roman'
    run.font.size = Pt(20)
    pPr = p._p.get_or_add_pPr()
    rPr = OxmlElement('w:rPr')
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), 'Times New Roman')
    rFonts.set(qn('w:hAnsi'), 'Times New Roman')
    rPr.append(rFonts)
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), '40')  # 20pt = 40 half-points
    rPr.append(sz)
    pPr.append(rPr)
    set_paragraph_spacing(p, space_before=0, space_after=0)
    return p


def add_exercise(doc, number, sentence, font_size, font_name=None):
    """Add an exercise header with sentence."""
    p = doc.add_paragraph()
    run = p.add_run(f'Exercise {number}. ')
    run.bold = True
    run.font.size = Pt(font_size)
    if font_name:
        run.font.name = font_name
    if sentence:
        run = p.add_run(sentence)
        run.italic = True
        run.font.size = Pt(font_size)
        if font_name:
            run.font.name = font_name
    set_paragraph_spacing(p, space_before=6, space_after=3)
    return p


def add_answer_line(doc, label, answer, font_size, indent=0.35, font_name=None):
    """Add a label: answer line."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(indent)
    run = p.add_run(f'{label} ')
    run.bold = True
    run.font.size = Pt(font_size)
    if font_name:
        run.font.name = font_name
    run = p.add_run(answer)
    run.italic = True
    run.font.size = Pt(font_size)
    if font_name:
        run.font.name = font_name
    set_paragraph_spacing(p, space_before=0, space_after=2)
    return p


def add_plain_line(doc, text, font_size, indent=0.35, bold_prefix=None, font_name=None):
    """Add a plain text line with optional bold prefix."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(indent)
    if bold_prefix:
        run = p.add_run(bold_prefix)
        run.bold = True
        run.font.size = Pt(font_size)
        if font_name:
            run.font.name = font_name
    run = p.add_run(text)
    run.font.size = Pt(font_size)
    if font_name:
        run.font.name = font_name
    set_paragraph_spacing(p, space_before=0, space_after=2)
    return p


def add_sub_sentence(doc, sub, sentence, font_size, font_name=None):
    """Add a sub-item like a), b), c) with sentence."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run(f'{sub} ')
    run.bold = True
    run.font.size = Pt(font_size)
    if font_name:
        run.font.name = font_name
    if sentence:
        run = p.add_run(sentence)
        run.italic = True
        run.font.size = Pt(font_size)
        if font_name:
            run.font.name = font_name
    set_paragraph_spacing(p, space_before=3, space_after=2)
    return p


def compute_spans(labels):
    """Convert flat label list to (label, span_count, start_index) tuples.

    Non-empty labels start a new span; consecutive empty strings extend it.
    """
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
    """Convert answer labels to blank labels preserving span structure for pre-merging.

    Non-empty labels become a space (visually blank but truthy for compute_spans),
    empty strings stay empty to continue the previous span.
    """
    return ["" if label == "" else " " for label in labels]


def add_labeling_table(doc, words, pos_labels=None, phrase_labels=None,
                       role_labels=None, font_size=10):
    """Add a sentence labeling table with merged cells for Role and Phrase rows.

    When labels are provided for Role/Phrase rows, cells are merged to show
    how words group into phrases and roles. When labels are None (student
    version), cells are left unmerged so students can write in each cell.
    Pass blank_labels(answer_labels) for pre-merged blank cells.
    """
    from docx.enum.table import WD_TABLE_ALIGNMENT

    num_cols = len(words) + 1  # +1 for row headers
    table = doc.add_table(rows=4, cols=num_cols)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.LEFT

    row_headers = ["Role", "Phrase", "Word", "POS"]
    row_data = [role_labels, phrase_labels, words, pos_labels]

    for i, (header, data) in enumerate(zip(row_headers, row_data)):
        # Row header cell
        cell = table.rows[i].cells[0]
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(header)
        run.bold = True
        run.font.size = Pt(font_size)
        # Shade header cell
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shading = OxmlElement('w:shd')
        shading.set(qn('w:fill'), 'E8E8E8')
        shading.set(qn('w:val'), 'clear')
        tcPr.append(shading)

        if i <= 1 and data:
            # Role or Phrase row with data — merge cells to show groupings
            spans = compute_spans(data)
            for label, span, start_idx in spans:
                col_start = start_idx + 1  # +1 for row header column
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
                run = p.add_run(label.strip())
                run.font.size = Pt(font_size)
        else:
            # Normal unmerged row (Word, POS, or blank student rows)
            for j, val in enumerate(data if data else [""] * len(words)):
                cell = table.rows[i].cells[j + 1]
                cell.text = ""
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                if i == 2:  # Word row always filled
                    run = p.add_run(val)
                    run.font.size = Pt(font_size)
                elif data:
                    run = p.add_run(val)
                    run.font.size = Pt(font_size)
                # else leave blank for student version

    return table


def add_diagram_image(doc, diagram_dir, image_name, width_inches=5.5):
    """Add a diagram PNG image to the document."""
    img_path = diagram_dir / f"{image_name}.png"
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


def add_bracket_line(doc, bracket, font_size, indent=0.35, font_name=None):
    """Add a bracket notation line in monospace."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(indent)
    run = p.add_run(bracket)
    run.font.name = 'Consolas'
    run.font.size = Pt(font_size - 1)
    set_paragraph_spacing(p, space_before=0, space_after=2)
    return p


def generate_pretext_labeling_xml(words, filled=False, roles=None, phrases=None, pos_labels=None):
    """Generate PreTeXt XML for a 4-row labeling table.

    Args:
        words: list of words in the sentence
        filled: if True, include answer values (for completed examples);
                if False, leave Role/Phrase/POS rows blank (student version)
        roles: list of role labels (same length as words, '' for span continuation)
        phrases: list of phrase labels
        pos_labels: list of POS labels

    Returns:
        String of PreTeXt XML for a <tabular> element.
    """
    num_cols = len(words) + 1  # +1 for row header
    lines = []
    lines.append('      <tabular top="minor" left="minor">')
    for _ in range(num_cols):
        halign = 'left' if _ == 0 else 'center'
        lines.append(f'        <col halign="{halign}" right="minor"/>')

    # Row 1: Role
    lines.append('        <row bottom="minor">')
    lines.append('          <cell>Role</cell>')
    for i in range(len(words)):
        val = roles[i] if (filled and roles) else ''
        lines.append(f'          <cell>{val}</cell>')
    lines.append('        </row>')

    # Row 2: Phrase
    lines.append('        <row bottom="minor">')
    lines.append('          <cell>Phrase</cell>')
    for i in range(len(words)):
        val = phrases[i] if (filled and phrases) else ''
        lines.append(f'          <cell>{val}</cell>')
    lines.append('        </row>')

    # Row 3: Word (always filled)
    lines.append('        <row bottom="minor">')
    lines.append('          <cell>Word</cell>')
    for w in words:
        lines.append(f'          <cell><foreign>{w}</foreign></cell>')
    lines.append('        </row>')

    # Row 4: POS
    lines.append('        <row bottom="minor">')
    lines.append('          <cell>POS</cell>')
    for i in range(len(words)):
        val = pos_labels[i] if (filled and pos_labels) else ''
        lines.append(f'          <cell>{val}</cell>')
    lines.append('        </row>')

    lines.append('      </tabular>')
    return '\n'.join(lines)


def generate_pretext_exercise_block(exercise_data, filled=False):
    """Generate a complete PreTeXt exercise block with labeling table.

    Args:
        exercise_data: dict with keys: num, sentence, words, roles, phrases,
                       pos, bracket (optional), image_source (optional)
        filled: if True, show answers (for completed examples)

    Returns:
        String of PreTeXt XML for the exercise.
    """
    ex = exercise_data
    lines = []
    lines.append(f'      <p><em>Exercise {ex["num"]}.</em> <foreign>{ex["sentence"]}</foreign></p>')
    lines.append('')
    lines.append(generate_pretext_labeling_xml(
        ex['words'], filled=filled,
        roles=ex.get('roles'), phrases=ex.get('phrases'), pos_labels=ex.get('pos')
    ))
    lines.append('')
    lines.append('      <ul>')
    lines.append('        <li><p>Bracket notation: _____</p></li>')
    lines.append('        <li><p>Diagram:</p></li>')
    lines.append('      </ul>')
    return '\n'.join(lines)


def overhead_page_break(doc):
    """Add a page break for overhead mode (each question starts on a new page)."""
    doc.add_page_break()


def get_font_config(overhead=False, font_size=12):
    """Return font configuration dict for answer key or overhead."""
    if overhead:
        return {
            'body_font': 'Arial Narrow',
            'body_size': 18,
            'heading1_size': 22,
            'heading2_size': 20,
            'heading3_size': 16,
            'bracket_size': 15,
            'diagram_width': 9.0,
        }
    else:
        return {
            'body_font': 'Garamond',
            'body_size': font_size,
            'heading1_size': 16,
            'heading2_size': 14,
            'heading3_size': 12,
            'bracket_size': font_size - 1,
            'diagram_width': 9.0,
        }


def setup_document(doc, overhead=False):
    """Configure document styles for answer key or overhead."""
    cfg = get_font_config(overhead)

    # Set landscape orientation
    section = doc.sections[0]
    section.orientation = 1  # WD_ORIENT.LANDSCAPE
    section.page_width = Inches(11)
    section.page_height = Inches(8.5)

    style = doc.styles['Normal']
    style.font.name = cfg['body_font']
    style.font.size = Pt(cfg['body_size'])

    for i in range(1, 4):
        heading_style = doc.styles[f'Heading {i}']
        heading_style.font.name = 'Open Sans' if not overhead else 'Arial Narrow'
        heading_style.font.bold = True

    return cfg


def add_title_page(doc, chapter_title, cfg, overhead=False):
    """Add the title page for an answer key."""
    title = doc.add_heading(chapter_title, level=1)
    title.runs[0].font.size = Pt(cfg['heading1_size'])
    set_paragraph_spacing(title, space_before=0, space_after=6)

    subtitle = doc.add_heading('Answer Key', level=2)
    subtitle.runs[0].font.size = Pt(cfg['heading2_size'])
    set_paragraph_spacing(subtitle, space_before=0, space_after=12)

    if overhead:
        add_spacer_row(doc)


def add_part_heading(doc, part_title, cfg, overhead=False):
    """Add a part heading with page break."""
    doc.add_page_break()
    part = doc.add_heading(part_title, level=3)
    part.runs[0].font.size = Pt(cfg['heading3_size'])
    return part


def exercise_separator(doc, overhead=False):
    """Add appropriate separator between exercises.
    For overhead: page break so each question starts on a new page.
    For answer key: just a spacer for readability."""
    if overhead:
        doc.add_page_break()
