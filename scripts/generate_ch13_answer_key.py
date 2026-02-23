#!/usr/bin/env python3
"""
Generate Chapter 13 Answer Key and Overhead Answer Key .docx files.
"""

from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches
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


def create_answer_key(output_path, font_size=12, overhead=False):
    """Create the Chapter 13 Answer Key document."""
    if overhead:
        body_font = 'Arial Narrow'
        body_size = 18
        heading1_size = 22
        heading2_size = 20
        heading3_size = 16
        table_size = 16
        bracket_size = 15
    else:
        body_font = 'Garamond'
        body_size = font_size
        heading1_size = 16
        heading2_size = 14
        heading3_size = 12
        table_size = font_size - 1
        bracket_size = font_size - 1

    doc = Document()

    style = doc.styles['Normal']
    style.font.name = body_font
    style.font.size = Pt(body_size)

    for i in range(1, 4):
        heading_style = doc.styles[f'Heading {i}']
        heading_style.font.name = 'Open Sans' if not overhead else 'Arial Narrow'
        heading_style.font.bold = True

    # Title
    title = doc.add_heading('Chapter 13: Adjectivals', level=1)
    title.runs[0].font.size = Pt(heading1_size)
    set_paragraph_spacing(title, space_before=0, space_after=6)

    subtitle = doc.add_heading('Answer Key', level=2)
    subtitle.runs[0].font.size = Pt(heading2_size)
    set_paragraph_spacing(subtitle, space_before=0, space_after=12)

    if overhead:
        add_spacer_row(doc)

    # =============================================
    # Part 1: Identification and Classification
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 1: Identification and Classification', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    # Exercise 1
    add_exercise(doc, 1, 'The book on the top shelf belongs to my professor.', body_size, font_name=body_font)
    add_answer_line(doc, 'Form:', 'prepositional phrase', body_size, font_name=body_font)
    add_plain_line(doc, 'Modifies "book" \u2014 tells which book', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 2
    add_exercise(doc, 2, 'The woman who won the award gave an inspiring speech.', body_size, font_name=body_font)
    add_answer_line(doc, 'Form:', 'relative clause', body_size, font_name=body_font)
    add_plain_line(doc, 'Modifies "woman" \u2014 identifies which woman', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 3
    add_exercise(doc, 3, 'The broken window needs to be repaired immediately.', body_size, font_name=body_font)
    add_answer_line(doc, 'Form:', 'past participle (single-word adjectival)', body_size, font_name=body_font)
    add_plain_line(doc, 'Modifies "window" \u2014 describes the window\u2019s state', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 4
    add_exercise(doc, 4, 'I need something to eat before the meeting.', body_size, font_name=body_font)
    add_answer_line(doc, 'Form:', 'infinitive phrase', body_size, font_name=body_font)
    add_plain_line(doc, 'Modifies "something" \u2014 specifies what kind of something', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 5
    add_exercise(doc, 5, 'The government report was released yesterday.', body_size, font_name=body_font)
    add_answer_line(doc, 'Form:', 'noun (used as adjectival)', body_size, font_name=body_font)
    add_plain_line(doc, 'Modifies "report" \u2014 classifies the type of report', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 6
    add_exercise(doc, 6, 'The students waiting in line seemed impatient.', body_size, font_name=body_font)
    add_answer_line(doc, 'Form:', 'present participial phrase', body_size, font_name=body_font)
    add_plain_line(doc, 'Modifies "students" \u2014 identifies which students', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 7
    add_exercise(doc, 7, 'We found a very comfortable chair at the antique store.', body_size, font_name=body_font)
    add_answer_line(doc, 'Form:', 'adjective phrase', body_size, font_name=body_font)
    add_plain_line(doc, 'Modifies "chair" \u2014 describes the chair', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # =============================================
    # Part 2: Restrictive vs. Non-Restrictive
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 2: Restrictive vs. Non-Restrictive', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    classifications = [
        (8, 'The students who completed the extra assignment received bonus points.',
         'Restrictive (R)',
         'No commas set off the clause. It identifies which students received bonus points \u2014 '
         'only those who completed the extra assignment, not all students.'),
        (9, 'The Eiffel Tower, which was built in 1889, attracts millions of visitors.',
         'Non-restrictive (NR)',
         'Commas set off the clause. The Eiffel Tower is already uniquely identified; '
         'the clause adds supplementary information about when it was built.'),
        (10, 'The car that I bought last year already needs repairs.',
         'Restrictive (R)',
         'No commas; "that" is used (typical of restrictive clauses). '
         'The clause identifies which car \u2014 specifically the one bought last year.'),
        (11, 'My neighbor\u2019s dog, a golden retriever, barks every morning.',
         'Non-restrictive (NR)',
         'Commas set off the appositive. The dog is already identified as "my neighbor\u2019s dog"; '
         '"a golden retriever" adds extra descriptive information.'),
    ]

    for num, sentence, classification, explanation in classifications:
        add_exercise(doc, num, sentence, body_size, font_name=body_font)
        add_answer_line(doc, 'Type:', classification, body_size, font_name=body_font)
        add_plain_line(doc, explanation, body_size, font_name=body_font)
        if overhead:
            add_spacer_row(doc)

    # =============================================
    # Part 3: Sentence Combining
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 3: Sentence Combining', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    p = doc.add_paragraph()
    run = p.add_run('Exercises 12\u201315 are open-ended. Accept any grammatically correct combination using the requested structure.')
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=6)

    combinations = [
        (12, 'Relative clause: This is the book. I told you about it.',
         '"This is the book that I told you about."'),
        (13, 'Relative clause: The scientist won a Nobel Prize. Her research changed medicine.',
         '"The scientist whose research changed medicine won a Nobel Prize."'),
        (14, 'Participial phrase: The students were exhausted from the exam. They went home early.',
         '"Exhausted from the exam, the students went home early."'),
        (15, 'Participial phrase: The letter was written in 1945. The letter was found in the attic.',
         '"Written in 1945, the letter was found in the attic." '
         'OR "The letter, written in 1945, was found in the attic."'),
    ]

    for num, prompt, sample in combinations:
        add_exercise(doc, num, None, body_size, font_name=body_font)
        add_plain_line(doc, prompt, body_size, bold_prefix='Prompt: ', font_name=body_font)
        add_plain_line(doc, f'Sample: {sample}', body_size, font_name=body_font)
        if overhead:
            add_spacer_row(doc)

    # =============================================
    # Part 4: Sentence Writing
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 4: Sentence Writing', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    p = doc.add_paragraph()
    run = p.add_run('Exercises 16\u201320 are open-ended. Accept any grammatically correct sentence that demonstrates the requested structure.')
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=6)

    writing = [
        (16, 'Restrictive relative clause with "that"',
         '"The book that I read last summer changed my perspective on history."'),
        (17, 'Present participial phrase modifying the subject',
         '"Running late for the meeting, Sarah grabbed her keys and rushed out the door."'),
        (18, 'Past participial phrase modifying a noun',
         '"The report, written by the committee, outlined several recommendations."'),
        (19, 'Infinitive phrase functioning as an adjectival',
         '"She needs a place to study for her exams."'),
        (20, 'Multiple pre-modifying adjectives (at least three)',
         '"They bought a beautiful large antique wooden dresser at the estate sale."'),
    ]

    for num, structure, sample in writing:
        add_exercise(doc, num, None, body_size, font_name=body_font)
        add_plain_line(doc, f'{structure}:', body_size, bold_prefix='Structure: ', font_name=body_font)
        add_plain_line(doc, f'Sample: {sample}', body_size, font_name=body_font)
        if overhead:
            add_spacer_row(doc)

    # =============================================
    # Part 5: Error Correction and Analysis
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 5: Error Correction and Analysis', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    # Exercise 21: Dangling Participle Correction
    add_exercise(doc, 21, None, body_size, font_name=body_font)
    add_plain_line(doc, 'Correct each dangling participle:', body_size, font_name=body_font)

    danglers = [
        ('a)', 'Walking through the park, the flowers were beautiful.',
         '"Walking through the park, I thought the flowers were beautiful." '
         'OR "As I walked through the park, the flowers were beautiful."',
         'The original implies the flowers were walking.'),
        ('b)', 'Having finished the report, the computer was shut down.',
         '"Having finished the report, she shut down the computer."',
         'The original implies the computer finished the report.'),
        ('c)', 'Exhausted from the journey, the bed looked inviting.',
         '"Exhausted from the journey, I thought the bed looked inviting."',
         'The original implies the bed was exhausted.'),
    ]

    for label, original, corrected, explanation in danglers:
        add_plain_line(doc, f'{label} {original}', body_size, indent=0.35, font_name=body_font)
        add_plain_line(doc, f'Corrected: {corrected}', body_size, indent=0.7, font_name=body_font)
        add_plain_line(doc, f'Explanation: {explanation}', body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # Exercise 22: Meaning Analysis
    add_exercise(doc, 22, None, body_size, font_name=body_font)
    add_plain_line(doc,
        'a) "My brother who lives in Chicago is a doctor."',
        body_size, font_name=body_font)
    add_plain_line(doc,
        'Restrictive: implies the speaker has more than one brother. The clause '
        'identifies which brother \u2014 the one in Chicago (as opposed to brothers elsewhere).',
        body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc,
        'b) "My brother, who lives in Chicago, is a doctor."',
        body_size, font_name=body_font)
    add_plain_line(doc,
        'Non-restrictive: implies the speaker has only one brother. The clause '
        'adds supplementary information about where he lives; it doesn\u2019t serve '
        'to distinguish him from other brothers.',
        body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # Exercise 23: Multiple Adjectivals
    add_exercise(doc, 23, None, body_size, font_name=body_font)
    add_plain_line(doc,
        'The talented young American jazz musician from New Orleans who won the competition',
        body_size, font_name=body_font)

    add_plain_line(doc, 'a) Adjectivals identified:', body_size, font_name=body_font)

    adjectivals = [
        ('"talented"', 'adjective (pre-modifier, opinion)'),
        ('"young"', 'adjective (pre-modifier, age)'),
        ('"American"', 'adjective (pre-modifier, origin)'),
        ('"jazz"', 'noun as adjectival (pre-modifier, purpose/type)'),
        ('"from New Orleans"', 'prepositional phrase (post-modifier)'),
        ('"who won the competition"', 'relative clause (post-modifier)'),
    ]

    for word, form in adjectivals:
        add_plain_line(doc, f'{word} \u2014 {form}', body_size, indent=0.7, font_name=body_font)

    add_plain_line(doc,
        'b) Pre-modifiers follow this typical order: determiner \u2192 opinion \u2192 size \u2192 '
        'age \u2192 shape \u2192 color \u2192 origin \u2192 material \u2192 purpose \u2192 NOUN. '
        'In this example: opinion (talented) \u2192 age (young) \u2192 origin (American) \u2192 '
        'type (jazz) \u2192 NOUN (musician).',
        body_size, font_name=body_font)

    add_plain_line(doc,
        'c) Post-modifiers follow the noun because they are longer, more complex structures '
        '(phrases and clauses) that would be unwieldy before the noun. English places shorter, '
        'simpler modifiers before the noun and longer, more complex ones after it. '
        'PPs and relative clauses are too heavy for pre-nominal position.',
        body_size, font_name=body_font)

    doc.save(str(output_path))
    print(f"Created: {output_path}")


def main():
    script_dir = Path(__file__).parent
    homework_dir = script_dir.parent / 'Homework'

    create_answer_key(
        homework_dir / 'Chapter 13 Answer Key.docx',
        font_size=12
    )

    create_answer_key(
        homework_dir / 'Homework 13 Overhead.docx',
        overhead=True
    )


if __name__ == '__main__':
    main()
