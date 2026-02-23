#!/usr/bin/env python3
"""
Generate Chapter 15 Answer Key and Overhead Answer Key .docx files.
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
    """Create the Chapter 15 Answer Key document."""
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
    title = doc.add_heading('Chapter 15: Punctuation', level=1)
    title.runs[0].font.size = Pt(heading1_size)
    set_paragraph_spacing(title, space_before=0, space_after=6)

    subtitle = doc.add_heading('Answer Key', level=2)
    subtitle.runs[0].font.size = Pt(heading2_size)
    set_paragraph_spacing(subtitle, space_before=0, space_after=12)

    if overhead:
        add_spacer_row(doc)

    # =============================================
    # Part 1: Comma Usage
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 1: Comma Usage', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    # Exercise 1
    add_exercise(doc, 1, 'When the storm passed we surveyed the damage and began cleanup efforts.', body_size, font_name=body_font)
    add_answer_line(doc, 'Corrected:', 'When the storm passed, we surveyed the damage and began cleanup efforts.', body_size, font_name=body_font)
    add_plain_line(doc, 'Function: comma after introductory adverb clause', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 2
    add_exercise(doc, 2, 'She is talented hardworking and creative.', body_size, font_name=body_font)
    add_answer_line(doc, 'Corrected:', 'She is talented, hardworking, and creative.', body_size, font_name=body_font)
    add_plain_line(doc, 'Function: commas separating items in a series (Oxford comma before "and")', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 3
    add_exercise(doc, 3, 'My brother who lives in Seattle is visiting next week.', body_size, font_name=body_font)
    add_answer_line(doc, 'Corrected:', 'My brother, who lives in Seattle, is visiting next week.', body_size, font_name=body_font)
    add_plain_line(doc,
        'Function: commas setting off nonrestrictive relative clause (assumes the speaker has only one brother; '
        'if the speaker has multiple brothers, no commas would be needed \u2014 the clause would be restrictive)',
        body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 4
    add_exercise(doc, 4, 'The meeting was productive but it ran overtime.', body_size, font_name=body_font)
    add_answer_line(doc, 'Corrected:', 'The meeting was productive, but it ran overtime.', body_size, font_name=body_font)
    add_plain_line(doc, 'Function: comma before coordinating conjunction joining two independent clauses', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 5
    add_exercise(doc, 5, 'The tall distinguished professor gave an inspiring lecture.', body_size, font_name=body_font)
    add_answer_line(doc, 'Corrected:', 'The tall, distinguished professor gave an inspiring lecture.', body_size, font_name=body_font)
    add_plain_line(doc,
        'Function: comma between coordinate adjectives (you can say "tall and distinguished," '
        'so a comma is appropriate)',
        body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 6
    add_exercise(doc, 6, 'The students who completed the assignment received extra credit.', body_size, font_name=body_font)
    add_plain_line(doc,
        'No comma is needed because "who completed the assignment" is a restrictive relative clause \u2014 '
        'it identifies which students received extra credit (only those who completed the assignment, '
        'not all students). Removing the clause would change the meaning.',
        body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # =============================================
    # Part 2: Semicolons and Colons
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 2: Semicolons and Colons', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    punctuation = [
        (7, 'She had one goal ( : / ; ) to finish the project on time.',
         'colon',
         'A colon introduces an explanation or elaboration after a complete sentence.'),
        (8, 'The rain stopped ( : / ; ) we went outside immediately.',
         'semicolon',
         'A semicolon joins two related independent clauses without a conjunction.'),
        (9, 'The committee includes three officers ( : / ; ) Dr. Lee, president; Ms. Park, secretary; and Mr. Kim, treasurer.',
         'colon',
         'A colon introduces the list. Semicolons are already used within the list items to separate names from titles.'),
        (10, 'He was exhausted ( : / ; ) however, he continued working.',
         'semicolon',
         'A semicolon is needed before a conjunctive adverb ("however") joining two independent clauses.'),
    ]

    for num, sentence, choice, reasoning in punctuation:
        add_exercise(doc, num, sentence, body_size, font_name=body_font)
        add_answer_line(doc, 'Choice:', choice, body_size, font_name=body_font)
        add_plain_line(doc, reasoning, body_size, font_name=body_font)
        if overhead:
            add_spacer_row(doc)

    # =============================================
    # Part 3: Apostrophes
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 3: Apostrophes', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    apostrophes = [
        (11, 'Its important to understand its function in the sentence.',
         'It\u2019s important to understand its function in the sentence.',
         'The first "its" should be "it\u2019s" (contraction of "it is"). The second "its" is correct (possessive).'),
        (12, 'The students books were left in the classroom.',
         'The students\u2019 books were left in the classroom.',
         'Plural possessive: "students\u2019" (the books belonging to the students).'),
        (13, 'The Joneses car is parked in the driveway.',
         'The Joneses\u2019 car is parked in the driveway.',
         'Plural possessive of a name ending in -s: "Joneses\u2019" (the car belonging to the Joneses).'),
        (14, 'Theyre going to their house over there.',
         'They\u2019re going to their house over there.',
         '"Theyre" should be "They\u2019re" (contraction of "they are"). "Their" and "there" are correct as used.'),
        (15, 'The womens team won the championship.',
         'The women\u2019s team won the championship.',
         'Irregular plural possessive: "women\u2019s" (the team belonging to the women). '
         'Since "women" doesn\u2019t end in -s, add \u2019s.'),
    ]

    for num, original, corrected, explanation in apostrophes:
        add_exercise(doc, num, original, body_size, font_name=body_font)
        add_answer_line(doc, 'Corrected:', corrected, body_size, font_name=body_font)
        add_plain_line(doc, explanation, body_size, font_name=body_font)
        if overhead:
            add_spacer_row(doc)

    # =============================================
    # Part 4: Comprehensive Punctuation
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 4: Comprehensive Punctuation', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    # Exercise 16
    add_exercise(doc, 16, None, body_size, font_name=body_font)
    add_plain_line(doc,
        'When the meeting ended, the participants left quickly; however, several stayed behind '
        'to discuss the proposal. The main question was this: should they proceed?',
        body_size, font_name=body_font)
    add_plain_line(doc,
        'Comma after introductory clause; semicolon before "however"; comma after "however"; '
        'period after "proposal"; colon before elaboration; question mark for direct question.',
        body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 17
    add_exercise(doc, 17, None, body_size, font_name=body_font)
    add_plain_line(doc,
        'The report, which took three months to complete, contained the following recommendations: '
        'reduce costs, improve efficiency, and increase employee training. However, the board '
        'rejected all three proposals.',
        body_size, font_name=body_font)
    add_plain_line(doc,
        'Commas around nonrestrictive clause; colon before list; commas in series (Oxford comma); '
        'period; comma after "However."',
        body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 18
    add_exercise(doc, 18, None, body_size, font_name=body_font)
    add_plain_line(doc,
        'Dr. Smith, who has been teaching for twenty years, said, "I believe that students '
        'learn best when they\u2019re engaged in meaningful activities."',
        body_size, font_name=body_font)
    add_plain_line(doc,
        'Period after "Dr"; commas around nonrestrictive clause; comma before quotation; '
        'quotation marks around direct speech; apostrophe in "they\u2019re"; period inside quotation marks.',
        body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # =============================================
    # Part 5: Analysis and Application
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 5: Analysis and Application', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    # Exercise 19
    add_exercise(doc, 19, None, body_size, font_name=body_font)
    add_plain_line(doc,
        '(a) "The students who studied passed the exam." \u2014 Restrictive: only those students '
        'who studied passed. Implies some students didn\u2019t study and didn\u2019t pass.',
        body_size, font_name=body_font)
    add_plain_line(doc,
        '(b) "The students, who studied, passed the exam." \u2014 Non-restrictive: all the students '
        'studied, and all of them passed. The clause adds extra information about what the students did.',
        body_size, font_name=body_font)
    add_plain_line(doc,
        'The commas change the meaning from identifying a subset (restrictive) to describing the '
        'whole group (non-restrictive). This is a key example of how punctuation affects meaning.',
        body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 20
    add_exercise(doc, 20, None, body_size, font_name=body_font)
    add_plain_line(doc,
        'Open-ended. Accept any paragraph that correctly identifies at least four punctuation marks '
        'with accurate grammatical explanations for each.',
        body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 21
    add_exercise(doc, 21, None, body_size, font_name=body_font)
    add_plain_line(doc,
        'Open-ended reflection. Accept thoughtful answers that demonstrate awareness of '
        'punctuation rules and self-assessment of challenges.',
        body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    doc.save(str(output_path))
    print(f"Created: {output_path}")


def main():
    script_dir = Path(__file__).parent
    homework_dir = script_dir.parent / 'Homework'

    create_answer_key(
        homework_dir / 'Chapter 15 Answer Key.docx',
        font_size=12
    )

    create_answer_key(
        homework_dir / 'Homework 15 Overhead.docx',
        overhead=True
    )


if __name__ == '__main__':
    main()
