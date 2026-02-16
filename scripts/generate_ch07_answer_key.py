#!/usr/bin/env python3
"""
Generate Chapter 7 Answer Key and Overhead Answer Key .docx files.
"""

import os
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor
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


def add_answer_table(doc, headers, rows, font_size=11):
    """Add a formatted table with merged cells for Role and Phrase rows."""
    num_cols = len(headers)
    table = doc.add_table(rows=1 + len(rows), cols=num_cols)
    table.style = 'Table Grid'

    # Header row (Role row) — merge cells to show groupings
    # First cell is the row label ("Role"), rest are data
    spans = compute_spans(headers)
    for label, span, start_idx in spans:
        if span > 1:
            table.rows[0].cells[start_idx].merge(table.rows[0].cells[start_idx + span - 1])
        cell = table.rows[0].cells[start_idx]
        for paragraph in cell.paragraphs:
            paragraph.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(label)
        run.bold = True
        run.font.size = Pt(font_size)

    # Data rows
    for i, row_data in enumerate(rows):
        row_label = row_data[0] if row_data else ""
        is_mergeable = row_label in ("Phrase",)  # Phrase row gets merged

        if is_mergeable:
            spans = compute_spans(row_data)
            for label, span, start_idx in spans:
                if span > 1:
                    table.rows[i + 1].cells[start_idx].merge(
                        table.rows[i + 1].cells[start_idx + span - 1]
                    )
                cell = table.rows[i + 1].cells[start_idx]
                for paragraph in cell.paragraphs:
                    paragraph.text = ""
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.add_run(label)
                run.font.size = Pt(font_size)
        else:
            for j, cell_text in enumerate(row_data):
                cell = table.rows[i + 1].cells[j]
                cell.text = cell_text
                for paragraph in cell.paragraphs:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for run in paragraph.runs:
                        run.font.size = Pt(font_size)


def create_answer_key(output_path, font_size=12):
    """Create the Chapter 7 Answer Key document."""
    doc = Document()

    # Set up styles
    style = doc.styles['Normal']
    style.font.name = 'Garamond'
    style.font.size = Pt(font_size)

    for i in range(1, 4):
        heading_style = doc.styles[f'Heading {i}']
        heading_style.font.name = 'Open Sans'
        heading_style.font.bold = True

    # Title
    title = doc.add_heading('Chapter 7: Introduction to Sentence Diagramming', level=1)
    title.runs[0].font.size = Pt(16 if font_size == 12 else 22)
    set_paragraph_spacing(title, space_before=0, space_after=6)

    subtitle = doc.add_heading('Answer Key', level=2)
    subtitle.runs[0].font.size = Pt(14 if font_size == 12 else 20)
    set_paragraph_spacing(subtitle, space_before=0, space_after=12)

    # =============================================
    # Part 1: Subject and Predicate Identification
    # =============================================
    part = doc.add_heading('Part 1: Subject and Predicate Identification', level=3)
    part.runs[0].font.size = Pt(12 if font_size == 12 else 18)

    # Exercise 1
    p = doc.add_paragraph()
    run = p.add_run('Exercise 1. ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('The curious students from the advanced chemistry class carefully examined the unusual compound.')
    run.italic = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=6, space_after=3)

    for label, answer in [
        ('Subject NP:', 'The curious students from the advanced chemistry class'),
        ('Head of subject NP:', 'students'),
        ('Predicate VP:', 'carefully examined the unusual compound'),
        ('Head of predicate VP:', 'examined'),
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.35)
        run = p.add_run(f'{label} ')
        run.bold = True
        run.font.size = Pt(font_size)
        run = p.add_run(answer)
        run.italic = True
        run.font.size = Pt(font_size)
        set_paragraph_spacing(p, space_before=0, space_after=2)

    # Exercise 2
    p = doc.add_paragraph()
    run = p.add_run('Exercise 2. ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('My extremely talented older sister from Portland won the national competition.')
    run.italic = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=6, space_after=3)

    for label, answer in [
        ('Subject NP:', 'My extremely talented older sister from Portland'),
        ('Head of subject NP:', 'sister'),
        ('Predicate VP:', 'won the national competition'),
        ('Head of predicate VP:', 'won'),
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.35)
        run = p.add_run(f'{label} ')
        run.bold = True
        run.font.size = Pt(font_size)
        run = p.add_run(answer)
        run.italic = True
        run.font.size = Pt(font_size)
        set_paragraph_spacing(p, space_before=0, space_after=2)

    # Exercise 3
    p = doc.add_paragraph()
    run = p.add_run('Exercise 3. ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('Several angry protesters outside the courthouse demanded immediate action.')
    run.italic = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=6, space_after=3)

    for label, answer in [
        ('Subject NP:', 'Several angry protesters outside the courthouse'),
        ('Head of subject NP:', 'protesters'),
        ('Predicate VP:', 'demanded immediate action'),
        ('Head of predicate VP:', 'demanded'),
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.35)
        run = p.add_run(f'{label} ')
        run.bold = True
        run.font.size = Pt(font_size)
        run = p.add_run(answer)
        run.italic = True
        run.font.size = Pt(font_size)
        set_paragraph_spacing(p, space_before=0, space_after=2)

    # ==============================
    # Part 2: Heads and Modifiers
    # ==============================
    if font_size > 12:
        doc.add_page_break()
    part = doc.add_heading('Part 2: Heads and Modifiers', level=3)
    part.runs[0].font.size = Pt(12 if font_size == 12 else 18)

    # Exercise 4
    p = doc.add_paragraph()
    run = p.add_run('Exercise 4. ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('my grandmother\'s beautiful antique wooden jewelry box')
    run.italic = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=6, space_after=3)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('Head: ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('box')
    run.italic = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=0, space_after=2)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('Modifiers:')
    run.bold = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=0, space_after=2)

    modifiers_4 = [
        "my grandmother's — possessive determiner",
        "beautiful — adjective",
        "antique — adjective",
        "wooden — adjective",
        "jewelry — noun (functioning adjectivally)",
    ]
    for mod in modifiers_4:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent = Inches(0.7)
        run = p.add_run(mod)
        run.font.size = Pt(font_size)
        set_paragraph_spacing(p, space_before=0, space_after=1)

    # Exercise 5
    p = doc.add_paragraph()
    run = p.add_run('Exercise 5. ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('extremely carefully')
    run.italic = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=6, space_after=3)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('Head: ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('carefully')
    run.italic = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=0, space_after=2)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('Modifiers:')
    run.bold = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=0, space_after=2)

    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent = Inches(0.7)
    run = p.add_run('extremely — adverb (degree modifier)')
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=0, space_after=1)

    # Exercise 6
    p = doc.add_paragraph()
    run = p.add_run('Exercise 6. ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('quite proud of her remarkable achievement')
    run.italic = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=6, space_after=3)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('Head: ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('proud')
    run.italic = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=0, space_after=2)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('Modifiers:')
    run.bold = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=0, space_after=2)

    modifiers_6 = [
        "quite — adverb (degree modifier)",
        "of her remarkable achievement — prepositional phrase (complement of 'proud')",
    ]
    for mod in modifiers_6:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent = Inches(0.7)
        run = p.add_run(mod)
        run.font.size = Pt(font_size)
        set_paragraph_spacing(p, space_before=0, space_after=1)

    # ======================================
    # Part 3: Completing Sentence Tables
    # ======================================
    if font_size > 12:
        doc.add_page_break()
    part = doc.add_heading('Part 3: Completing Sentence Tables', level=3)
    part.runs[0].font.size = Pt(12 if font_size == 12 else 18)

    # Exercise 7: Thunder rumbled.
    p = doc.add_paragraph()
    run = p.add_run('Exercise 7. ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('Thunder rumbled.')
    run.italic = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=6, space_after=3)

    add_answer_table(doc,
        ['Role', 'Subject', 'Predicate'],
        [
            ['Phrase', 'NP', 'MVP'],
            ['Word', 'Thunder', 'rumbled'],
            ['POS', 'N', 'V'],
        ],
        font_size=font_size - 1
    )

    # Exercise 8: The old man sat quietly.
    p = doc.add_paragraph()
    run = p.add_run('Exercise 8. ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('The old man sat quietly.')
    run.italic = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=6, space_after=3)

    add_answer_table(doc,
        ['Role', 'Subject', '', '', 'Predicate', ''],
        [
            ['Phrase', 'NP', '', '', 'MVP', 'ADVP'],
            ['Word', 'The', 'old', 'man', 'sat', 'quietly'],
            ['POS', 'DET', 'ADJ', 'N', 'V', 'ADV'],
        ],
        font_size=font_size - 1
    )

    # Exercise 9: The cat chased the mouse.
    p = doc.add_paragraph()
    run = p.add_run('Exercise 9. ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('The cat chased the mouse.')
    run.italic = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=6, space_after=3)

    add_answer_table(doc,
        ['Role', 'Subject', '', 'Predicate', '', ''],
        [
            ['Phrase', 'NP', '', 'MVP', 'NP', ''],
            ['Word', 'The', 'cat', 'chased', 'the', 'mouse'],
            ['POS', 'DET', 'N', 'V', 'DET', 'N'],
        ],
        font_size=font_size - 1
    )

    # ===========================================
    # Part 4: Completing Diagrams and Tables
    # ===========================================
    if font_size > 12:
        doc.add_page_break()
    part = doc.add_heading('Part 4: Completing Diagrams and Tables', level=3)
    part.runs[0].font.size = Pt(12 if font_size == 12 else 18)

    # Exercise 10: The dog barked loudly.
    p = doc.add_paragraph()
    run = p.add_run('Exercise 10. ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('The dog barked loudly.')
    run.italic = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=6, space_after=3)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('Bracket notation: ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('[S [NP [DET The] [N dog]] [VP [V barked] [ADVP [ADV loudly]]]]')
    run.font.name = 'Consolas'
    run.font.size = Pt(font_size - 1)
    set_paragraph_spacing(p, space_before=0, space_after=3)

    add_answer_table(doc,
        ['Role', 'Subject', '', 'Predicate', ''],
        [
            ['Phrase', 'NP', '', 'MVP', 'ADVP'],
            ['Word', 'The', 'dog', 'barked', 'loudly'],
            ['POS', 'DET', 'N', 'V', 'ADV'],
        ],
        font_size=font_size - 1
    )

    # Exercise 11: The talented student from Ohio won the award.
    p = doc.add_paragraph()
    run = p.add_run('Exercise 11. ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('The talented student from Ohio won the award.')
    run.italic = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=6, space_after=3)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('Bracket notation: ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('[S [NP [DET The] [ADJP [ADJ talented]] [N student] [PP [PREP from] [NP [N Ohio]]]] [VP [V won] [NP [DET the] [N award]]]]')
    run.font.name = 'Consolas'
    run.font.size = Pt(font_size - 1)
    set_paragraph_spacing(p, space_before=0, space_after=3)

    add_answer_table(doc,
        ['Role', 'Subject', '', '', '', '', 'Predicate', '', ''],
        [
            ['Phrase', 'NP', '', '', 'PP', '', 'MVP', 'NP', ''],
            ['Word', 'The', 'talented', 'student', 'from', 'Ohio', 'won', 'the', 'award'],
            ['POS', 'DET', 'ADJ', 'N', 'PREP', 'N', 'V', 'DET', 'N'],
        ],
        font_size=font_size - 1
    )

    # Exercise 12: She carefully read the interesting book.
    p = doc.add_paragraph()
    run = p.add_run('Exercise 12. ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('She carefully read the interesting book.')
    run.italic = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=6, space_after=3)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('Bracket notation: ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('[S [NP [PRON She]] [VP [ADVP [ADV carefully]] [V read] [NP [DET the] [ADJP [ADJ interesting]] [N book]]]]')
    run.font.name = 'Consolas'
    run.font.size = Pt(font_size - 1)
    set_paragraph_spacing(p, space_before=0, space_after=3)

    add_answer_table(doc,
        ['Role', 'Subject', 'Predicate', '', '', '', ''],
        [
            ['Phrase', 'NP', 'ADVP', 'MVP', 'NP', '', ''],
            ['Word', 'She', 'carefully', 'read', 'the', 'interesting', 'book'],
            ['POS', 'PRON', 'ADV', 'V', 'DET', 'ADJ', 'N'],
        ],
        font_size=font_size - 1
    )

    # ==========================================
    # Part 5: Structural Ambiguity Analysis
    # ==========================================
    if font_size > 12:
        doc.add_page_break()
    part = doc.add_heading('Part 5: Structural Ambiguity Analysis', level=3)
    part.runs[0].font.size = Pt(12 if font_size == 12 else 18)

    # Exercise 13
    p = doc.add_paragraph()
    run = p.add_run('Exercise 13. ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('I shot an elephant in my pajamas.')
    run.italic = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=6, space_after=3)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('a) Two possible meanings:')
    run.bold = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=3, space_after=2)

    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent = Inches(0.7)
    run = p.add_run('Meaning 1: I was wearing my pajamas when I shot an elephant. (PP "in my pajamas" modifies VP — describes the circumstances of the shooting)')
    run.font.size = Pt(font_size)

    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent = Inches(0.7)
    run = p.add_run('Meaning 2: I shot an elephant that was wearing my pajamas. (PP "in my pajamas" modifies NP "an elephant" — describes which elephant)')
    run.font.size = Pt(font_size)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('b) Bracket notation for each reading:')
    run.bold = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=3, space_after=2)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.7)
    run = p.add_run('Meaning 1 (VP attachment): ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('[S [NP [PRON I]] [VP [V shot] [NP [DET an] [N elephant]] [PP [PREP in] [NP [DET my] [N pajamas]]]]]')
    run.font.name = 'Consolas'
    run.font.size = Pt(font_size - 1)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.7)
    run = p.add_run('Meaning 2 (NP attachment): ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('[S [NP [PRON I]] [VP [V shot] [NP [DET an] [N elephant] [PP [PREP in] [NP [DET my] [N pajamas]]]]]]')
    run.font.name = 'Consolas'
    run.font.size = Pt(font_size - 1)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('c) Model response:')
    run.bold = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=3, space_after=2)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.7)
    run = p.add_run(
        'This sentence is funny because of structural ambiguity involving PP attachment. '
        'The audience initially interprets "in my pajamas" as modifying the VP — '
        'describing the shooter\'s attire, which is a plausible (if eccentric) reading. '
        'Groucho then reveals the absurd alternative: the elephant was wearing his pajamas. '
        'This reading comes from attaching the PP to the NP "an elephant" instead. '
        'The humor arises because both structures are grammatically valid, but one produces '
        'an absurd mental image. The joke exploits the fact that listeners commit to one '
        'structural analysis before realizing the other was intended.'
    )
    run.font.size = Pt(font_size)

    # Exercise 14
    p = doc.add_paragraph()
    run = p.add_run('Exercise 14. ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('The horse raced past the barn fell.')
    run.italic = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=6, space_after=3)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('a) Initial reading:')
    run.bold = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=3, space_after=2)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.7)
    run = p.add_run(
        'Most readers initially parse "The horse" as the subject NP and "raced past the barn" '
        'as the main VP — the horse is running past a barn. When "fell" appears, the sentence '
        'seems to "break" because the reader has already assigned "raced" as the main verb, '
        'and there appears to be no grammatical role for "fell" to play.'
    )
    run.font.size = Pt(font_size)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('b) Correct reading:')
    run.bold = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=3, space_after=2)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.7)
    run = p.add_run(
        'The correct reading is: "The horse [that was] raced past the barn fell." '
        'Here, "raced past the barn" is a reduced relative clause modifying "horse" — '
        'it tells us which horse (the one that was raced past the barn). '
        'The main verb of the sentence is "fell." The full subject NP is '
        '"The horse raced past the barn," and the VP is simply "fell."'
    )
    run.font.size = Pt(font_size)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('c) Model response:')
    run.bold = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=3, space_after=2)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.7)
    run = p.add_run(
        'Garden-path sentences cause confusion because our brains process language incrementally — '
        'we build structural interpretations word by word as we read. When we encounter "The horse raced," '
        'the simplest analysis is that "raced" is the main verb, and we commit to that structure. '
        'When "fell" appears, it forces us to revise: "raced" was actually part of a reduced relative '
        'clause, not the main verb. This revision is cognitively costly, which is why the sentence '
        'feels confusing. Garden-path sentences demonstrate that sentence comprehension is not just '
        'about knowing the words — it requires actively building and sometimes revising hierarchical '
        'structure in real time.'
    )
    run.font.size = Pt(font_size)

    # Exercise 15
    p = doc.add_paragraph()
    run = p.add_run('Exercise 15. ')
    run.bold = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=6, space_after=3)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('Model response:')
    run.bold = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=3, space_after=2)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.7)
    run = p.add_run(
        'Understanding hierarchical sentence structure matters because meaning depends on how words '
        'are grouped, not just on the words themselves. For example, the sentence "I saw the man with '
        'binoculars" is ambiguous: it could mean I used binoculars to see the man, or I saw a man '
        'who had binoculars. A tree diagram reveals these two structures by showing different PP '
        'attachment points. For writing, this awareness helps us construct sentences whose structure '
        'guides readers to the intended meaning, avoiding accidental ambiguity.'
    )
    run.font.size = Pt(font_size)

    doc.save(str(output_path))
    print(f"Created: {output_path}")


def main():
    script_dir = Path(__file__).parent
    homework_dir = script_dir.parent / 'Homework'

    # Create Answer Key (standard size)
    create_answer_key(
        homework_dir / 'Chapter 07 Answer Key.docx',
        font_size=12
    )

    # Create Overhead Answer Key (large font for projection)
    create_answer_key(
        homework_dir / 'Homework 07 Overhead.docx',
        font_size=22
    )


if __name__ == '__main__':
    main()
