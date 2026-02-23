#!/usr/bin/env python3
"""
Generate Chapter 14 Answer Key and Overhead Answer Key .docx files.
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
    """Create the Chapter 14 Answer Key document."""
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
    title = doc.add_heading('Chapter 14: Nominals', level=1)
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
    add_exercise(doc, 1, 'I don\u2019t know whether she received my message.', body_size, font_name=body_font)
    add_answer_line(doc, 'Form:', 'wh-clause (whether-clause)', body_size, font_name=body_font)
    add_answer_line(doc, 'Function:', 'direct object (of "know")', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 2
    add_exercise(doc, 2, 'The problem is that we lack sufficient funding.', body_size, font_name=body_font)
    add_answer_line(doc, 'Form:', 'that-clause', body_size, font_name=body_font)
    add_answer_line(doc, 'Function:', 'subject complement', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 3
    add_exercise(doc, 3, 'To learn a new language requires dedication and practice.', body_size, font_name=body_font)
    add_answer_line(doc, 'Form:', 'infinitive phrase', body_size, font_name=body_font)
    add_answer_line(doc, 'Function:', 'subject', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 4
    add_exercise(doc, 4, 'What the scientist discovered changed the field of biology.', body_size, font_name=body_font)
    add_answer_line(doc, 'Form:', 'wh-clause', body_size, font_name=body_font)
    add_answer_line(doc, 'Function:', 'subject', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 5
    add_exercise(doc, 5, 'She enjoys reading mystery novels on rainy afternoons.', body_size, font_name=body_font)
    add_answer_line(doc, 'Form:', 'gerund phrase', body_size, font_name=body_font)
    add_answer_line(doc, 'Function:', 'direct object (of "enjoys")', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 6
    add_exercise(doc, 6, 'He asked who would be attending the conference.', body_size, font_name=body_font)
    add_answer_line(doc, 'Form:', 'wh-clause', body_size, font_name=body_font)
    add_answer_line(doc, 'Function:', 'direct object (of "asked")', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 7
    add_exercise(doc, 7, 'Her greatest fear is making a mistake in public.', body_size, font_name=body_font)
    add_answer_line(doc, 'Form:', 'gerund phrase', body_size, font_name=body_font)
    add_answer_line(doc, 'Function:', 'subject complement', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # =============================================
    # Part 2: Functional Analysis
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 2: Functional Analysis', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    functions = [
        (8, 'That the project failed disappointed everyone.',
         'subject',
         'The that-clause is the subject of "disappointed."'),
        (9, 'The committee discussed how they would proceed.',
         'direct object',
         'The wh-clause is the direct object of "discussed."'),
        (10, 'She\u2019s interested in learning more about linguistics.',
         'object of preposition',
         'The gerund phrase is the object of the preposition "in."'),
        (11, 'The main issue is whether we should continue.',
         'subject complement',
         'The wh-clause follows the linking verb "is" and renames "the main issue."'),
        (12, 'I appreciate your helping us with the move.',
         'direct object',
         'The gerund phrase (with possessive) is the direct object of "appreciate."'),
    ]

    for num, sentence, function, explanation in functions:
        add_exercise(doc, num, sentence, body_size, font_name=body_font)
        add_answer_line(doc, 'Function:', function, body_size, font_name=body_font)
        add_plain_line(doc, explanation, body_size, font_name=body_font)
        if overhead:
            add_spacer_row(doc)

    # =============================================
    # Part 3: Sentence Completion
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 3: Sentence Completion', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    p = doc.add_paragraph()
    run = p.add_run('Exercises 13\u201317 are open-ended. Accept any grammatically correct nominal of the requested type.')
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=6)

    completions = [
        (13, 'Gerund phrase as subject: __________ can be challenging for new employees.',
         '"Learning new software can be challenging for new employees."'),
        (14, 'Wh-clause as direct object: The detective investigated __________.',
         '"The detective investigated who had access to the building."'),
        (15, 'Infinitive phrase as subject complement: Her goal this year is __________.',
         '"Her goal this year is to complete her dissertation."'),
        (16, 'That-clause as subject: __________ surprised everyone at the meeting.',
         '"That the CEO resigned surprised everyone at the meeting."'),
        (17, 'Gerund phrase as object of preposition: She succeeded by __________.',
         '"She succeeded by studying consistently throughout the semester."'),
    ]

    for num, prompt, sample in completions:
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
    run = p.add_run('Exercises 18\u201322 are open-ended. Accept any grammatically correct sentence that demonstrates the requested structure.')
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=6)

    writing = [
        (18, 'Wh-clause as direct object',
         '"I wonder what she meant by that remark."'),
        (19, 'Gerund phrase as object of preposition',
         '"He improved his skills by practicing every day."'),
        (20, 'Infinitive phrase as subject complement',
         '"The best strategy is to start early and plan ahead."'),
        (21, 'That-clause as subject complement',
         '"The truth is that we underestimated the difficulty."'),
        (22, 'Extraposed subject (It + that-clause or infinitive)',
         '"It is important to consider all perspectives before deciding." '
         'OR "It surprised me that she already knew."'),
    ]

    for num, structure, sample in writing:
        add_exercise(doc, num, None, body_size, font_name=body_font)
        add_plain_line(doc, f'{structure}:', body_size, bold_prefix='Structure: ', font_name=body_font)
        add_plain_line(doc, f'Sample: {sample}', body_size, font_name=body_font)
        if overhead:
            add_spacer_row(doc)

    # =============================================
    # Part 5: Analysis and Application
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 5: Analysis and Application', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    # Exercise 23
    add_exercise(doc, 23, None, body_size, font_name=body_font)
    add_plain_line(doc, 'a) "She stopped smoking." vs. b) "She stopped to smoke."', body_size, font_name=body_font)

    add_plain_line(doc,
        'Grammatical difference: In (a), "smoking" is a gerund \u2014 it functions as '
        'the direct object of "stopped." In (b), "to smoke" is an infinitive phrase \u2014 '
        'it functions as an adverbial of purpose.',
        body_size, font_name=body_font)
    add_plain_line(doc,
        'Meaning difference: (a) means she quit the habit of smoking. '
        '(b) means she paused what she was doing in order to have a smoke.',
        body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 24
    add_exercise(doc, 24, None, body_size, font_name=body_font)
    add_plain_line(doc, 'a) "I remember locking the door." vs. b) "I remember to lock the door."', body_size, font_name=body_font)

    add_plain_line(doc,
        '(a) The gerund "locking" refers to a past event \u2014 I have a memory of '
        'having locked the door (I recall doing it).',
        body_size, font_name=body_font)
    add_plain_line(doc,
        '(b) The infinitive "to lock" refers to a future/habitual obligation \u2014 '
        'I don\u2019t forget to lock the door (I remember that I need to do it).',
        body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 25
    add_exercise(doc, 25, None, body_size, font_name=body_font)
    add_plain_line(doc, 'Transform "The experiment succeeded" into four nominal structures:', body_size, font_name=body_font)

    transforms = [
        ('a) That-clause as subject:',
         '"That the experiment succeeded pleased the researchers."'),
        ('b) Gerund phrase as subject:',
         '"The experiment\u2019s succeeding pleased the researchers." '
         'OR "The experiment succeeding pleased the researchers."'),
        ('c) Wh-clause as direct object:',
         '"They wondered whether the experiment had succeeded."'),
        ('d) Infinitive after "seem":',
         '"The experiment seemed to succeed." OR "The experiment seemed to have succeeded."'),
    ]

    for label, sample in transforms:
        add_plain_line(doc, label, body_size, indent=0.35, font_name=body_font)
        add_plain_line(doc, f'Sample: {sample}', body_size, indent=0.7, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 26
    add_exercise(doc, 26, None, body_size, font_name=body_font)
    add_plain_line(doc,
        'a) Extraposition moves a clausal subject to the end of the sentence, '
        'replacing it with the placeholder pronoun "it" in subject position. '
        'Example: "That she resigned surprised everyone" \u2192 '
        '"It surprised everyone that she resigned."',
        body_size, font_name=body_font)
    add_plain_line(doc,
        'b) A writer might prefer the extraposed version when the clausal subject '
        'is long or complex, as it follows the end-weight principle \u2014 '
        'placing heavier elements at the end for easier processing. '
        'It also sounds more natural in conversation.',
        body_size, font_name=body_font)
    add_plain_line(doc,
        'c) A writer might prefer the non-extraposed version to give the clause '
        'more prominence or emphasis (topic position), or when the clause is '
        'relatively short and doesn\u2019t create processing difficulty.',
        body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    doc.save(str(output_path))
    print(f"Created: {output_path}")


def main():
    script_dir = Path(__file__).parent
    homework_dir = script_dir.parent / 'Homework'

    create_answer_key(
        homework_dir / 'Chapter 14 Answer Key.docx',
        font_size=12
    )

    create_answer_key(
        homework_dir / 'Homework 14 Overhead.docx',
        overhead=True
    )


if __name__ == '__main__':
    main()
