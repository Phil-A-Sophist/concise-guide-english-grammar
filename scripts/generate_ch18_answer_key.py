#!/usr/bin/env python3
"""
Generate Chapter 18 Answer Key and Overhead Answer Key .docx files.
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
    """Create the Chapter 18 Answer Key document."""
    doc = Document()

    style = doc.styles['Normal']
    style.font.name = 'Garamond'
    style.font.size = Pt(font_size)

    for i in range(1, 4):
        heading_style = doc.styles[f'Heading {i}']
        heading_style.font.name = 'Open Sans'
        heading_style.font.bold = True

    # Title
    title = doc.add_heading('Chapter 18: Clarity and Readability', level=1)
    title.runs[0].font.size = Pt(16 if font_size == 12 else 22)
    set_paragraph_spacing(title, space_before=0, space_after=6)

    subtitle = doc.add_heading('Answer Key', level=2)
    subtitle.runs[0].font.size = Pt(14 if font_size == 12 else 20)
    set_paragraph_spacing(subtitle, space_before=0, space_after=12)

    # =============================================
    # Part 1: Pronoun Reference
    # =============================================
    part = doc.add_heading('Part 1: Pronoun Reference', level=3)
    part.runs[0].font.size = Pt(12 if font_size == 12 else 18)

    # Exercise 1
    add_exercise(doc, 1, 'When John met Mark, he was surprised.', font_size)
    add_answer_line(doc, 'Problem:', 'Ambiguous reference \u2014 "he" could refer to John or Mark.', font_size)
    add_answer_line(doc, 'Revised:', 'When John met Mark, John was surprised.', font_size)
    add_plain_line(doc, '(Or: "When John met Mark, Mark was surprised.")', font_size)

    # Exercise 2
    add_exercise(doc, 2, 'They say the economy is improving.', font_size)
    add_answer_line(doc, 'Problem:', 'Vague reference \u2014 "they" has no identifiable antecedent.', font_size)
    add_answer_line(doc, 'Revised:', 'Economists say the economy is improving.', font_size)

    # Exercise 3
    add_exercise(doc, 3, 'She failed the test, which disappointed her parents.', font_size)
    add_answer_line(doc, 'Problem:',
        'Broad reference \u2014 "which" refers to the whole clause, not a specific noun.',
        font_size)
    add_answer_line(doc, 'Revised:', 'Her test failure disappointed her parents.', font_size)

    # Exercise 4
    add_exercise(doc, 4,
        'The committee reviewed the proposal and rejected it. This caused problems.',
        font_size)
    add_answer_line(doc, 'Problem:',
        'Broad reference \u2014 "this" could refer to the review, the rejection, or both.',
        font_size)
    add_answer_line(doc, 'Revised:', 'The committee\'s rejection of the proposal caused problems.', font_size)

    # Exercise 5
    add_exercise(doc, 5,
        'The teacher told the student that her presentation needed work.',
        font_size)
    add_answer_line(doc, 'Problem:',
        'Ambiguous reference \u2014 "her" could refer to the teacher or the student.',
        font_size)
    add_answer_line(doc, 'Revised:',
        'The teacher told the student that the student\'s presentation needed work.',
        font_size)

    # =============================================
    # Part 2: Modifier Placement
    # =============================================
    if font_size > 12:
        doc.add_page_break()
    part = doc.add_heading('Part 2: Modifier Placement', level=3)
    part.runs[0].font.size = Pt(12 if font_size == 12 else 18)

    # Exercise 6
    add_exercise(doc, 6, 'Having finished dinner, the movie was started.', font_size)
    add_answer_line(doc, 'Error type:', 'Dangling modifier \u2014 the movie did not finish dinner.', font_size)
    add_answer_line(doc, 'Revised:', 'Having finished dinner, we started the movie.', font_size)

    # Exercise 7
    add_exercise(doc, 7, 'She almost failed every exam.', font_size)
    add_answer_line(doc, 'Error type:',
        'Misplaced modifier \u2014 "almost" modifies "failed," but the intended meaning is '
        '"almost every."',
        font_size)
    add_answer_line(doc, 'Revised:', 'She failed almost every exam.', font_size)

    # Exercise 8
    add_exercise(doc, 8, 'Students who cheat often get caught.', font_size)
    add_answer_line(doc, 'Error type:',
        'Squinting modifier \u2014 "often" could modify "cheat" or "get caught."',
        font_size)
    add_answer_line(doc, 'Meaning 1:', 'Students who often cheat get caught.', font_size)
    add_answer_line(doc, 'Meaning 2:', 'Students who cheat get caught often.', font_size)

    # Exercise 9
    add_exercise(doc, 9,
        'To earn a good grade, the assignment must be completed carefully.',
        font_size)
    add_answer_line(doc, 'Error type:',
        'Dangling modifier \u2014 the assignment cannot earn a grade.',
        font_size)
    add_answer_line(doc, 'Revised:',
        'To earn a good grade, you must complete the assignment carefully.',
        font_size)

    # Exercise 10
    add_exercise(doc, 10, 'He only eats organic food on weekdays.', font_size)
    add_answer_line(doc, 'Error type:',
        'Misplaced modifier \u2014 "only" modifies "eats," but the intended meaning '
        'is "only on weekdays" or "only organic food."',
        font_size)
    add_answer_line(doc, 'Revised (if "only organic"):', 'He eats only organic food on weekdays.', font_size)
    add_answer_line(doc, 'Revised (if "only weekdays"):', 'He eats organic food only on weekdays.', font_size)

    # =============================================
    # Part 3: Structural Ambiguity
    # =============================================
    if font_size > 12:
        doc.add_page_break()
    part = doc.add_heading('Part 3: Structural Ambiguity', level=3)
    part.runs[0].font.size = Pt(12 if font_size == 12 else 18)

    # Exercise 11
    add_exercise(doc, 11, 'I photographed the elephant with a camera.', font_size)
    add_answer_line(doc, 'Meaning 1:',
        'I used a camera to photograph the elephant. (PP modifies VP)',
        font_size)
    add_answer_line(doc, 'Revised:', 'Using a camera, I photographed the elephant.', font_size)
    add_answer_line(doc, 'Meaning 2:',
        'The elephant had a camera. (PP modifies NP)',
        font_size)
    add_answer_line(doc, 'Revised:', 'I photographed the elephant that had a camera.', font_size)

    # Exercise 12
    add_exercise(doc, 12, 'Bright students and teachers attended the workshop.', font_size)
    add_answer_line(doc, 'Meaning 1:',
        'Only the students are bright. (ADJ modifies first conjunct only)',
        font_size)
    add_answer_line(doc, 'Revised:',
        'Teachers and bright students attended the workshop.',
        font_size)
    add_answer_line(doc, 'Meaning 2:',
        'Both the students and teachers are bright. (ADJ modifies entire coordination)',
        font_size)
    add_answer_line(doc, 'Revised:',
        'Bright students and bright teachers attended the workshop.',
        font_size)

    # Exercise 13
    add_exercise(doc, 13, 'The professor\'s assistant who was sick left early.', font_size)
    add_answer_line(doc, 'Meaning 1:',
        'The assistant was sick. (Relative clause modifies "assistant")',
        font_size)
    add_answer_line(doc, 'Revised:',
        'The professor\'s assistant, who was sick, left early.',
        font_size)
    add_answer_line(doc, 'Meaning 2:',
        'The professor was sick. (Relative clause modifies "professor")',
        font_size)
    add_answer_line(doc, 'Revised:',
        'The assistant of the professor who was sick left early.',
        font_size)

    # Exercise 14
    add_exercise(doc, 14, 'She watched the children playing in the park.', font_size)
    add_answer_line(doc, 'Meaning 1:',
        'She was in the park when she watched. (PP modifies VP)',
        font_size)
    add_answer_line(doc, 'Revised:',
        'In the park, she watched the children playing.',
        font_size)
    add_answer_line(doc, 'Meaning 2:',
        'The children were playing in the park. (PP modifies "playing" or NP)',
        font_size)
    add_answer_line(doc, 'Revised:',
        'She watched the children who were playing in the park.',
        font_size)

    # =============================================
    # Part 4: Parallel Structure and Sentence Complexity
    # =============================================
    if font_size > 12:
        doc.add_page_break()
    part = doc.add_heading('Part 4: Parallel Structure and Sentence Complexity', level=3)
    part.runs[0].font.size = Pt(12 if font_size == 12 else 18)

    # Exercise 15
    add_exercise(doc, 15, 'She enjoys reading, writing, and to paint.', font_size)
    add_answer_line(doc, 'Revised:', 'She enjoys reading, writing, and painting.', font_size)
    add_plain_line(doc, 'All three items are now gerunds, creating parallel structure.', font_size)

    # Exercise 16
    add_exercise(doc, 16, 'The job requires experience, dedication, and being creative.', font_size)
    add_answer_line(doc, 'Revised:', 'The job requires experience, dedication, and creativity.', font_size)
    add_plain_line(doc, 'All three items are now nouns, creating parallel structure.', font_size)

    # Exercise 17
    add_exercise(doc, 17,
        'He not only finished the report but also he proofread the entire document.',
        font_size)
    add_answer_line(doc, 'Revised:',
        'He not only finished the report but also proofread the entire document.',
        font_size)
    add_plain_line(doc,
        'The correlative conjunction "not only...but also" now connects parallel verb '
        'phrases ("finished the report" and "proofread the entire document").',
        font_size)

    # Exercise 18
    add_exercise(doc, 18,
        'The report, which was commissioned by the board that was established last year '
        'to oversee operations, contains recommendations that, if implemented, would '
        'significantly improve efficiency.',
        font_size)
    add_answer_line(doc, 'Revised:',
        'The board established a committee last year to oversee operations. The committee\'s '
        'report contains recommendations that would significantly improve efficiency if implemented.',
        font_size)

    # Exercise 19
    add_exercise(doc, 19,
        'The student, who had already completed the assignment that the professor assigned '
        'last week during the lecture that was held in the auditorium, submitted it early.',
        font_size)
    add_answer_line(doc, 'Revised:',
        'Last week, the professor assigned an assignment during a lecture in the auditorium. '
        'One student had already completed it and submitted it early.',
        font_size)

    # =============================================
    # Part 5: Comprehensive Revision
    # =============================================
    if font_size > 12:
        doc.add_page_break()
    part = doc.add_heading('Part 5: Comprehensive Revision', level=3)
    part.runs[0].font.size = Pt(12 if font_size == 12 else 18)

    # Exercise 20
    add_exercise(doc, 20, None, font_size)
    add_plain_line(doc, 'Sample revised paragraph:', font_size, indent=0, bold_prefix='')
    add_plain_line(doc,
        'When the team walked into the meeting, the tension was immediately apparent. '
        'The manager told the employees that their performance needed to improve. '
        'The employees\' frustration grew. The proposal was not only expensive but also '
        'time-consuming, requiring years to implement. After reviewing all options carefully, '
        'the leadership decided to wait. Everyone understood that patience would be '
        'necessary.',
        font_size)

    add_plain_line(doc, '', font_size, indent=0)
    add_plain_line(doc, 'Issues to identify (any four):', font_size, indent=0, bold_prefix='')
    add_plain_line(doc,
        '\u2022 Dangling modifier: "Walking into the meeting, the tension..." '
        '\u2014 tension was not walking',
        font_size)
    add_plain_line(doc,
        '\u2022 Ambiguous pronoun: "they needed to improve" '
        '\u2014 "they" is unclear (manager or employees?)',
        font_size)
    add_plain_line(doc,
        '\u2022 Broad reference: "This led to frustration" '
        '\u2014 "this" has no specific antecedent',
        font_size)
    add_plain_line(doc,
        '\u2022 Faulty parallelism: "not only expensive but also it would take years" '
        '\u2014 not parallel',
        font_size)
    add_plain_line(doc,
        '\u2022 Dangling modifier: "Having reviewed all options carefully, the decision was made" '
        '\u2014 the decision did not review options',
        font_size)
    add_plain_line(doc,
        '\u2022 Vague reference: "They say that patience is a virtue" '
        '\u2014 "they" has no antecedent',
        font_size)
    add_plain_line(doc,
        '\u2022 Broad reference: "which everyone understood" '
        '\u2014 "which" refers to an entire clause',
        font_size)

    doc.save(str(output_path))
    print(f"Created: {output_path}")


def main():
    script_dir = Path(__file__).parent
    homework_dir = script_dir.parent / 'Homework'

    create_answer_key(
        homework_dir / 'Chapter 18 Answer Key.docx',
        font_size=12
    )

    create_answer_key(
        homework_dir / 'Homework 18 Overhead.docx',
        font_size=22
    )


if __name__ == '__main__':
    main()
