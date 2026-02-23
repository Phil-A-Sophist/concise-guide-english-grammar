#!/usr/bin/env python3
"""
Generate Chapter 8 Answer Key and Overhead Answer Key .docx files.
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
    """Create the Chapter 8 Answer Key document."""
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

    # Set up styles
    style = doc.styles['Normal']
    style.font.name = body_font
    style.font.size = Pt(body_size)

    for i in range(1, 4):
        heading_style = doc.styles[f'Heading {i}']
        heading_style.font.name = 'Open Sans' if not overhead else 'Arial Narrow'
        heading_style.font.bold = True

    # Title
    title = doc.add_heading('Chapter 8: Basic Sentence Elements and Sentence Patterns', level=1)
    title.runs[0].font.size = Pt(heading1_size)
    set_paragraph_spacing(title, space_before=0, space_after=6)

    subtitle = doc.add_heading('Answer Key', level=2)
    subtitle.runs[0].font.size = Pt(heading2_size)
    set_paragraph_spacing(subtitle, space_before=0, space_after=12)

    if overhead:
        add_spacer_row(doc)

    # =============================================
    # Part 1: Sentence Element Identification
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 1: Sentence Element Identification', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    # Exercise 1
    add_exercise(doc, 1,
        'The ambitious young researcher from the university laboratory discovered a remarkable solution.',
        body_size, font_name=body_font)

    for label, answer in [
        ('Subject NP:', 'The ambitious young researcher from the university laboratory'),
        ('Predicate:', 'discovered a remarkable solution'),
        ('Main verb:', 'discovered'),
        ('Direct object:', 'a remarkable solution'),
    ]:
        add_answer_line(doc, label, answer, body_size, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # Exercise 2
    add_exercise(doc, 2, None, body_size, font_name=body_font)

    # 2a
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('a) ')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    run = p.add_run('The committee awarded the outstanding student a prestigious scholarship.')
    run.italic = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)

    add_answer_line(doc, 'IO:', 'the outstanding student', body_size, indent=0.7, font_name=body_font)
    add_answer_line(doc, 'DO:', 'a prestigious scholarship', body_size, indent=0.7, font_name=body_font)

    # 2b
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('b) ')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    run = p.add_run('The homemade soup tasted absolutely delicious.')
    run.italic = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)

    add_answer_line(doc, 'SC:', 'absolutely delicious (AdjP)', body_size, indent=0.7, font_name=body_font)

    # 2c
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('c) ')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    run = p.add_run('The judges declared the young contestant the winner.')
    run.italic = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)

    add_answer_line(doc, 'DO:', 'the young contestant', body_size, indent=0.7, font_name=body_font)
    add_answer_line(doc, 'OC:', 'the winner (NP)', body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # Exercise 3
    add_exercise(doc, 3, None, body_size, font_name=body_font)

    for sub, sentence, answer in [
        ('a)', 'She placed the documents on the desk.',
         'Argument \u2014 required by "placed." Remove it: *She placed the documents. \u2717 (incomplete without location)'),
        ('b)', 'She found the documents on the desk.',
         'Adverbial \u2014 optional location modifier. Remove it: She found the documents. \u2713 (still grammatical)'),
        ('c)', 'The professor is extremely knowledgeable about linguistics.',
         'Argument \u2014 subject complement required by "is." Remove it: *The professor is. \u2717 (incomplete)'),
        ('d)', 'The professor lectured extremely knowledgeably about linguistics.',
         'Adverbial \u2014 optional manner/topic modifier. Remove it: The professor lectured. \u2713 (still grammatical)'),
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.35)
        run = p.add_run(f'{sub} ')
        run.bold = True
        run.font.size = Pt(body_size)
        run.font.name = body_font
        run = p.add_run(sentence)
        run.italic = True
        run.font.size = Pt(body_size)
        run.font.name = body_font
        set_paragraph_spacing(p, space_before=3, space_after=2)

        add_plain_line(doc, answer, body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # =============================================
    # Part 2: Sentence Completion
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 2: Sentence Completion', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    p = doc.add_paragraph()
    run = p.add_run('Exercises 4\u20137 are open-ended. Accept any grammatically correct completion that matches the requested element type.')
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=6)

    for num, prompt, sample in [
        (4, 'The dedicated students completed _____.', 'Sample: "their research project" (NP as direct object)'),
        (5, 'The generous donor gave _____.', 'Sample: "the school a generous donation" (IO: the school, DO: a generous donation)'),
        (6, 'After the long hike, the exhausted climbers seemed _____.', 'Sample: "completely exhausted" (AdjP as subject complement)'),
        (7, 'The board of directors elected her _____.', 'Sample: "chairperson" (NP as object complement)'),
    ]:
        add_exercise(doc, num, prompt, body_size, font_name=body_font)
        add_plain_line(doc, sample, body_size, font_name=body_font)
        if overhead:
            add_spacer_row(doc)

    # =============================================
    # Part 3: Sentence Pattern Identification
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 3: Sentence Pattern Identification', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    patterns = [
        (8, 'The exhausted marathon runner collapsed at the finish line yesterday.',
         'Pattern 1 (Intransitive)',
         'Main verb: "collapsed." "At the finish line" and "yesterday" are adverbials (optional\u2014answer "where?" and "when?"). '
         'Without adverbials: "The exhausted marathon runner collapsed."\u2014complete with subject + intransitive verb. '
         '"Collapsed" does not require an object or complement.'),
        (9, "My grandmother's secret recipe remains a family treasure.",
         'Pattern 3 (Linking verb)',
         'Main verb: "remains." "A family treasure" is a subject complement (NP identifying the subject). '
         'Be substitution test: "My grandmother\'s secret recipe is a family treasure" \u2713. '
         'Since the verb is not "be" itself but passes the be-substitution test, this is Pattern 3 (Linking), not Pattern 2 (Copular be).'),
        (10, 'The committee considered the proposal inadequate.',
         'Pattern 6 (DO + OC)',
         'Main verb: "considered." Two elements follow the verb: "the proposal" (NP) + "inadequate" (AdjP). '
         'Do they refer to the same thing? Yes\u2014the proposal is described as inadequate. '
         'Therefore "the proposal" = DO and "inadequate" = OC.'),
        (11, 'The chef prepared the guests an extraordinary seven-course meal.',
         'Pattern 5 (IO + DO)',
         'Main verb: "prepared." Two NPs follow the verb: "the guests" and "an extraordinary seven-course meal." '
         'Do they refer to the same thing? No\u2014the guests \u2260 the meal. '
         'Can rephrase with "for": "prepared an extraordinary seven-course meal for the guests." '
         '"The guests" = IO, "an extraordinary seven-course meal" = DO.'),
        (12, 'The situation grew increasingly tense during the negotiations.',
         'Pattern 3 (Linking verb)',
         'Main verb: "grew." "During the negotiations" is an adverbial (time)\u2014set aside. '
         '"Increasingly tense" is a subject complement (AdjP describing the subject). '
         'Be substitution test: "The situation was increasingly tense" \u2713. Pattern 3 (Linking).'),
    ]

    for num, sentence, pattern, explanation in patterns:
        add_exercise(doc, num, sentence, body_size, font_name=body_font)
        add_answer_line(doc, 'Pattern:', pattern, body_size, font_name=body_font)

        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.35)
        run = p.add_run('Explanation: ')
        run.bold = True
        run.font.size = Pt(body_size)
        run.font.name = body_font
        run = p.add_run(explanation)
        run.font.size = Pt(body_size)
        run.font.name = body_font
        set_paragraph_spacing(p, space_before=0, space_after=2)

        if overhead:
            add_spacer_row(doc)

    # =============================================
    # Part 4: Sentence Writing
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 4: Sentence Writing', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    p = doc.add_paragraph()
    run = p.add_run('Exercises 13\u201315 are open-ended. Accept any grammatically correct sentence that follows the requested pattern with elements correctly labeled.')
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=6)

    for num, pattern, sample in [
        (13, 'Pattern 4 (S + V + DO)',
         'Sample: "[The dog]_S [chased]_V [the cat]_DO."'),
        (14, 'Pattern 5 (S + V + IO + DO)',
         'Sample: "[The teacher]_S [gave]_V [the students]_IO [a quiz]_DO."'),
        (15, 'Pattern 6 (S + V + DO + OC)',
         'Sample: "[The class]_S [elected]_V [Maria]_DO [president]_OC."'),
    ]:
        add_exercise(doc, num, None, body_size, font_name=body_font)
        add_plain_line(doc, f'{pattern}:', body_size, bold_prefix='Pattern: ', font_name=body_font)
        add_plain_line(doc, sample, body_size, font_name=body_font)
        if overhead:
            add_spacer_row(doc)

    # =============================================
    # Part 5: Analysis and Reflection
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 5: Analysis and Reflection', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    # Exercise 16
    add_exercise(doc, 16, 'She put the book on the shelf.', body_size, font_name=body_font)

    for sub, answer in [
        ('What happens if you remove "the book"?',
         '*She put on the shelf. \u2717 \u2014 ungrammatical. "The book" is a required argument (DO).'),
        ('What happens if you remove "on the shelf"?',
         '*She put the book. \u2717 \u2014 ungrammatical/incomplete. "On the shelf" is a required argument (locative).'),
        ('What does this tell you about the valency of "put"?',
         '"Put" requires THREE arguments: a subject, a direct object, and a locative phrase. '
         'It has valency 3, making it unusual among English verbs.'),
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.35)
        run = p.add_run(sub)
        run.bold = True
        run.font.size = Pt(body_size)
        run.font.name = body_font
        set_paragraph_spacing(p, space_before=3, space_after=2)

        add_plain_line(doc, answer, body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # Exercise 17
    add_exercise(doc, 17, None, body_size, font_name=body_font)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('a) ')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    run = p.add_run('The milk smells sour.')
    run.italic = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    run = p.add_run(' vs. ')
    run.font.size = Pt(body_size)
    run.font.name = body_font
    run = p.add_run('The detective smells trouble.')
    run.italic = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)

    add_plain_line(doc,
        '"The milk smells sour" \u2014 linking verb (Pattern 3). "Sour" is a subject complement describing the milk.',
        body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc,
        '"The detective smells trouble" \u2014 transitive verb (Pattern 4). "Trouble" is a direct object.',
        body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc,
        'Be substitution test: "The milk is sour" \u2713 (makes sense \u2192 linking). '
        '"The detective is trouble" \u2717 (doesn\'t make sense \u2192 not linking, therefore transitive).',
        body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # Exercise 18
    add_exercise(doc, 18, None, body_size, font_name=body_font)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('Model response: ')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    run = p.add_run(
        'Arguments are elements required by the verb to form a grammatical sentence; '
        'removing them makes the sentence ungrammatical or changes its meaning dramatically. '
        'Adverbials provide optional information about time, place, manner, or reason; '
        'removing them leaves a grammatical sentence intact. This distinction matters because '
        'sentence patterns are defined by the required elements (arguments), not the optional ones (adverbials). '
        'For example, in "She put the book on the table," "on the table" is an argument '
        '(removing it yields *She put the book, which is ungrammatical). But in "She read the book on the table," '
        '"on the table" is an adverbial (removing it yields She read the book, which is fine). '
        'The first sentence requires a locative argument; the second does not.'
    )
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=0, space_after=2)

    doc.save(str(output_path))
    print(f"Created: {output_path}")


def main():
    script_dir = Path(__file__).parent
    homework_dir = script_dir.parent / 'Homework'

    # Create Answer Key (standard size)
    create_answer_key(
        homework_dir / 'Chapter 08 Answer Key.docx',
        font_size=12
    )

    # Create Overhead Answer Key
    create_answer_key(
        homework_dir / 'Homework 08 Overhead.docx',
        overhead=True
    )


if __name__ == '__main__':
    main()
