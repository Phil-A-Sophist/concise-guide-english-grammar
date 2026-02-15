#!/usr/bin/env python3
"""
Generate Chapter 16 Answer Key and Overhead Answer Key .docx files.
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


def add_exercise(doc, number, sentence, font_size):
    """Add an exercise header with sentence."""
    p = doc.add_paragraph()
    run = p.add_run(f'Exercise {number}. ')
    run.bold = True
    run.font.size = Pt(font_size)
    if sentence:
        run = p.add_run(sentence)
        run.italic = True
        run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=6, space_after=3)
    return p


def add_answer_line(doc, label, answer, font_size, indent=0.35):
    """Add a label: answer line."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(indent)
    run = p.add_run(f'{label} ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run(answer)
    run.italic = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=0, space_after=2)
    return p


def add_plain_line(doc, text, font_size, indent=0.35, bold_prefix=None):
    """Add a plain text line with optional bold prefix."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(indent)
    if bold_prefix:
        run = p.add_run(bold_prefix)
        run.bold = True
        run.font.size = Pt(font_size)
    run = p.add_run(text)
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=0, space_after=2)
    return p


def create_answer_key(output_path, font_size=12):
    """Create the Chapter 16 Answer Key document."""
    doc = Document()

    style = doc.styles['Normal']
    style.font.name = 'Garamond'
    style.font.size = Pt(font_size)

    for i in range(1, 4):
        heading_style = doc.styles[f'Heading {i}']
        heading_style.font.name = 'Open Sans'
        heading_style.font.bold = True

    # Title
    title = doc.add_heading('Chapter 16: Other Grammatical Forms', level=1)
    title.runs[0].font.size = Pt(16 if font_size == 12 else 22)
    set_paragraph_spacing(title, space_before=0, space_after=6)

    subtitle = doc.add_heading('Answer Key', level=2)
    subtitle.runs[0].font.size = Pt(14 if font_size == 12 else 20)
    set_paragraph_spacing(subtitle, space_before=0, space_after=12)

    # =============================================
    # Part 1: Nonfinite Verb Forms
    # =============================================
    part = doc.add_heading('Part 1: Nonfinite Verb Forms', level=3)
    part.runs[0].font.size = Pt(12 if font_size == 12 else 18)

    # Exercise 1
    add_exercise(doc, 1, 'Swimming is excellent exercise.', font_size)
    add_answer_line(doc, 'Answer:', 'Swimming', font_size)
    add_plain_line(doc, 'Gerund (functioning as the subject of the sentence)', font_size)

    # Exercise 2
    add_exercise(doc, 2, 'The broken window needs repair.', font_size)
    add_answer_line(doc, 'Answer:', 'broken', font_size)
    add_plain_line(doc, 'Past participle (functioning adjectivally, modifying "window")', font_size)

    # Exercise 3
    add_exercise(doc, 3, 'I saw him running toward the door.', font_size)
    add_answer_line(doc, 'Answer:', 'running', font_size)
    add_plain_line(doc,
        'Present participle (functioning as an object complement after perception verb "saw")',
        font_size)

    # Exercise 4
    add_exercise(doc, 4, 'They made her apologize.', font_size)
    add_answer_line(doc, 'Answer:', 'apologize', font_size)
    add_plain_line(doc,
        'Bare infinitive (no "to"; after causative verb "made")',
        font_size)

    # Exercise 5
    add_exercise(doc, 5, 'Having finished the exam, she left the room.', font_size)
    add_answer_line(doc, 'Answer:', 'Having finished', font_size)
    add_plain_line(doc,
        'Perfect participle (past participle with "having"; functioning adverbially)',
        font_size)

    # =============================================
    # Part 2: Complement Clauses
    # =============================================
    if font_size > 12:
        doc.add_page_break()
    part = doc.add_heading('Part 2: Complement Clauses', level=3)
    part.runs[0].font.size = Pt(12 if font_size == 12 else 18)

    complements = [
        (6, 'She believes that honesty matters.',
         'that honesty matters',
         'That-clause (complement of the verb "believes")'),
        (7, 'He wants to succeed in his career.',
         'to succeed in his career',
         'Infinitive clause (complement of the verb "wants")'),
        (8, 'I wonder what she meant.',
         'what she meant',
         'Wh-clause (complement of the verb "wonder")'),
        (9, 'She enjoys reading novels.',
         'reading novels',
         'Gerund clause (complement of the verb "enjoys")'),
    ]

    for num, sentence, clause, classification in complements:
        add_exercise(doc, num, sentence, font_size)
        add_answer_line(doc, 'Complement clause:', clause, font_size)
        add_plain_line(doc, classification, font_size)

    # =============================================
    # Part 3: Special Constructions
    # =============================================
    if font_size > 12:
        doc.add_page_break()
    part = doc.add_heading('Part 3: Special Constructions', level=3)
    part.runs[0].font.size = Pt(12 if font_size == 12 else 18)

    constructions = [
        (10, 'It was John who broke the window.',
         'It-cleft (cleft sentence)',
         'Focuses attention on "John" as the agent. Presupposes that someone broke the window '
         'and highlights who did it.'),
        (11, 'There are three students waiting in the hall.',
         'Existential sentence',
         'Introduces new entities ("three students") into the discourse. '
         'The expletive "there" serves as a placeholder subject.'),
        (12, 'It surprised everyone that she resigned.',
         'Extraposition',
         'The subject clause "that she resigned" has been moved to the end, '
         'with "it" as a placeholder. This avoids a heavy subject and '
         'puts the surprising information at the end for emphasis.'),
        (13, 'That movie, I never liked.',
         'Topicalization',
         'The object "that movie" has been moved to the front of the sentence '
         'for emphasis, establishing it as the topic of discussion.'),
    ]

    for num, sentence, ctype, effect in constructions:
        add_exercise(doc, num, sentence, font_size)
        add_answer_line(doc, 'Construction type:', ctype, font_size)
        add_plain_line(doc, effect, font_size, bold_prefix='Effect: ')

    # =============================================
    # Part 4: Coordination and Revision
    # =============================================
    if font_size > 12:
        doc.add_page_break()
    part = doc.add_heading('Part 4: Coordination and Revision', level=3)
    part.runs[0].font.size = Pt(12 if font_size == 12 else 18)

    # Exercise 14
    add_exercise(doc, 14, 'She likes swimming, hiking, and to ride bikes.', font_size)
    add_answer_line(doc, 'Revised:', 'She likes swimming, hiking, and riding bikes.', font_size)
    add_plain_line(doc,
        'All three items are now gerunds, creating parallel structure.',
        font_size)

    # Exercise 15
    add_exercise(doc, 15, 'The candidate promised to cut taxes and creating jobs.', font_size)
    add_answer_line(doc, 'Revised:', 'The candidate promised to cut taxes and create jobs.', font_size)
    add_plain_line(doc,
        'Both items are now infinitives (sharing "to"), creating parallel structure.',
        font_size)

    # Exercise 16
    add_exercise(doc, 16, 'The committee rejected the budget.', font_size)
    add_answer_line(doc, 'Cleft version:', 'It was the budget that the committee rejected.', font_size)
    add_plain_line(doc,
        'The it-cleft focuses on "the budget" as the thing rejected.',
        font_size)

    # Exercise 17
    add_exercise(doc, 17, 'That she would resign surprised everyone.', font_size)
    add_answer_line(doc, 'Extraposed:', 'It surprised everyone that she would resign.', font_size)
    add_plain_line(doc,
        'The heavy subject clause moves to the end, with "it" as placeholder.',
        font_size)

    # =============================================
    # Part 5: Passage Analysis
    # =============================================
    if font_size > 12:
        doc.add_page_break()
    part = doc.add_heading('Part 5: Passage Analysis', level=3)
    part.runs[0].font.size = Pt(12 if font_size == 12 else 18)

    # Exercise 18
    add_exercise(doc, 18, None, font_size)
    add_plain_line(doc, 'Nonfinite verb forms in the passage:', font_size, indent=0, bold_prefix='')
    add_plain_line(doc,
        '\u2022 "Having examined" \u2014 perfect participle (adverbial, modifying "they")',
        font_size)
    add_plain_line(doc,
        '\u2022 "planned" \u2014 past participle (passive: "had been carefully planned")',
        font_size)
    add_plain_line(doc,
        '\u2022 "To identify" \u2014 to-infinitive (subject of "would require")',
        font_size)

    # Exercise 19
    add_exercise(doc, 19, None, font_size)
    add_plain_line(doc,
        '\u2022 Cleft sentence: "What surprised the investigators was the lack of evidence" (wh-cleft)',
        font_size)
    add_plain_line(doc,
        '\u2022 Existential sentence: "There were no witnesses"',
        font_size)
    add_plain_line(doc,
        '\u2022 Extraposition: "It was clear that someone with inside knowledge was responsible" '
        '("that" clause extraposed, "it" as placeholder)',
        font_size)

    # Exercise 20
    add_exercise(doc, 20, None, font_size)
    add_plain_line(doc,
        'a) Simple sentence: The lack of evidence surprised the investigators.',
        font_size)
    add_plain_line(doc,
        'b) It-cleft: It was the lack of evidence that surprised the investigators.',
        font_size)

    # Exercise 21
    add_exercise(doc, 21, None, font_size)
    add_plain_line(doc,
        'Open-ended. Accept answers that discuss how cleft sentences focus attention on '
        'specific elements (creating emphasis and contrast), while extraposition improves '
        'readability by avoiding heavy subjects. Both constructions manipulate information '
        'structure to control what readers notice first and to create stylistic effects such '
        'as suspense, emphasis, or smoother processing.',
        font_size)

    doc.save(str(output_path))
    print(f"Created: {output_path}")


def main():
    script_dir = Path(__file__).parent
    homework_dir = script_dir.parent / 'Homework'

    create_answer_key(
        homework_dir / 'Chapter 16 Answer Key.docx',
        font_size=12
    )

    create_answer_key(
        homework_dir / 'Homework 16 Overhead.docx',
        font_size=22
    )


if __name__ == '__main__':
    main()
