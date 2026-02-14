#!/usr/bin/env python3
"""
Generate Chapter 10 Answer Key and Overhead Answer Key .docx files.
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
    """Create the Chapter 10 Answer Key document."""
    doc = Document()

    style = doc.styles['Normal']
    style.font.name = 'Garamond'
    style.font.size = Pt(font_size)

    for i in range(1, 4):
        heading_style = doc.styles[f'Heading {i}']
        heading_style.font.name = 'Open Sans'
        heading_style.font.bold = True

    # Title
    title = doc.add_heading('Chapter 10: Verbs Part One \u2014 Tense and Aspect', level=1)
    title.runs[0].font.size = Pt(16 if font_size == 12 else 22)
    set_paragraph_spacing(title, space_before=0, space_after=6)

    subtitle = doc.add_heading('Answer Key', level=2)
    subtitle.runs[0].font.size = Pt(14 if font_size == 12 else 20)
    set_paragraph_spacing(subtitle, space_before=0, space_after=12)

    # =============================================
    # Part 1: Identification
    # =============================================
    part = doc.add_heading('Part 1: Identification', level=3)
    part.runs[0].font.size = Pt(12 if font_size == 12 else 18)

    exercises_p1 = [
        (1, 'The researchers have analyzed the experimental data.',
         [('Auxiliary verb(s):', 'have'),
          ('Main verb:', 'analyzed'),
          ('Tense:', 'present'),
          ('Aspect:', 'perfect')]),
        (2, 'Yesterday, she was working in the library when I called.',
         [('Auxiliary verb(s):', 'was'),
          ('Main verb:', 'working'),
          ('Tense:', 'past'),
          ('Aspect:', 'progressive')]),
        (3, 'By next month, they will have completed the entire project.',
         [('Auxiliary verb(s):', 'will, have'),
          ('Main verb:', 'completed'),
          ('Tense:', 'future'),
          ('Aspect:', 'perfect')]),
        (4, 'The professor teaches linguistics every semester.',
         [('Auxiliary verb(s):', 'none'),
          ('Main verb:', 'teaches'),
          ('Tense:', 'present'),
          ('Aspect:', 'simple')]),
        (5, 'The students had been studying for three hours before the test began.',
         [('Auxiliary verb(s):', 'had, been'),
          ('Main verb:', 'studying'),
          ('Tense:', 'past'),
          ('Aspect:', 'perfect progressive')]),
    ]

    for num, sentence, answers in exercises_p1:
        add_exercise(doc, num, sentence, font_size)
        for label, answer in answers:
            add_answer_line(doc, label, answer, font_size)

    # =============================================
    # Part 2: Sentence Completion
    # =============================================
    if font_size > 12:
        doc.add_page_break()
    part = doc.add_heading('Part 2: Sentence Completion', level=3)
    part.runs[0].font.size = Pt(12 if font_size == 12 else 18)

    completions = [
        (6, 'Present progressive: Right now, the children ________ (play) in the park.',
         'are playing'),
        (7, 'Past perfect: By the time I arrived, they ________ (already / leave).',
         'had already left'),
        (8, 'Present perfect progressive: She ________ (work) on this project for six months.',
         'has been working'),
        (9, 'Future progressive: At noon tomorrow, I ________ (meet) with the committee.',
         'will be meeting'),
        (10, 'Past simple: The team ________ (finish) the assignment last night.',
         'finished'),
    ]

    for num, prompt, answer in completions:
        add_exercise(doc, num, prompt, font_size)
        add_answer_line(doc, 'Answer:', answer, font_size)

    # =============================================
    # Part 3: Sentence Writing
    # =============================================
    if font_size > 12:
        doc.add_page_break()
    part = doc.add_heading('Part 3: Sentence Writing', level=3)
    part.runs[0].font.size = Pt(12 if font_size == 12 else 18)

    p = doc.add_paragraph()
    run = p.add_run('Exercises 11\u201315 are open-ended. Accept any grammatically correct sentence that demonstrates the requested tense-aspect combination.')
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=3, space_after=6)

    writing = [
        (11, 'Present perfect (experience up to now)',
         '"She has traveled to Japan three times."'),
        (12, 'Past progressive (background action interrupted)',
         '"I was reading when the doorbell rang."'),
        (13, 'Future perfect (action completed before future point)',
         '"By December, we will have finished the renovation."'),
        (14, 'Present simple (general truth)',
         '"The Earth revolves around the Sun."'),
        (15, 'Past perfect (one past event before another)',
         '"By the time the ambulance arrived, the patient had already recovered."'),
    ]

    for num, structure, sample in writing:
        add_exercise(doc, num, None, font_size)
        add_plain_line(doc, f'{structure}:', font_size, bold_prefix='Structure: ')
        add_plain_line(doc, f'Sample: {sample}', font_size)

    # =============================================
    # Part 4: Distinguishing Meaning
    # =============================================
    if font_size > 12:
        doc.add_page_break()
    part = doc.add_heading('Part 4: Distinguishing Meaning', level=3)
    part.runs[0].font.size = Pt(12 if font_size == 12 else 18)

    # Exercise 16
    add_exercise(doc, 16, None, font_size)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('a) ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('She read the report.')
    run.italic = True
    run.font.size = Pt(font_size)
    run = p.add_run('  vs.  ')
    run.font.size = Pt(font_size)
    run = p.add_run('b) ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('She has read the report.')
    run.italic = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=3, space_after=2)

    add_plain_line(doc,
        '(a) Past simple \u2014 states a completed past event with no connection to now. '
        '(b) Present perfect \u2014 implies present relevance: she has read it, so she knows its contents now.',
        font_size, indent=0.7)

    # Exercise 17
    add_exercise(doc, 17, None, font_size)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('a) ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('When I arrived, they left.')
    run.italic = True
    run.font.size = Pt(font_size)
    run = p.add_run('  vs.  ')
    run.font.size = Pt(font_size)
    run = p.add_run('b) ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('When I arrived, they had left.')
    run.italic = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=3, space_after=2)

    add_plain_line(doc,
        '(a) Past simple for both verbs \u2014 the events happened in sequence: I arrived, '
        'then they left (my arrival may have caused their departure). '
        '(b) Past perfect "had left" \u2014 they left BEFORE I arrived; they were already gone when I got there.',
        font_size, indent=0.7)

    # Exercise 18
    add_exercise(doc, 18, None, font_size)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('a) ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('He works at a bank.')
    run.italic = True
    run.font.size = Pt(font_size)
    run = p.add_run('  vs.  ')
    run.font.size = Pt(font_size)
    run = p.add_run('b) ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run('He is working at a bank.')
    run.italic = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=3, space_after=2)

    add_plain_line(doc,
        '(a) Present simple \u2014 permanent or habitual situation: this is his regular job. '
        '(b) Present progressive \u2014 temporary situation: he is working there right now but it may not be permanent '
        '(e.g., a summer job or temporary assignment).',
        font_size, indent=0.7)

    # =============================================
    # Part 5: Contextual Analysis
    # =============================================
    if font_size > 12:
        doc.add_page_break()
    part = doc.add_heading('Part 5: Contextual Analysis', level=3)
    part.runs[0].font.size = Pt(12 if font_size == 12 else 18)

    # Exercise 19
    add_exercise(doc, 19, None, font_size)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('Passage: ')
    run.bold = True
    run.font.size = Pt(font_size)
    run = p.add_run(
        'Maria moved to Boston in 2018. She has lived there ever since. When I visited her last summer, '
        'she was working on her dissertation. She has been writing it for two years now. By next June, '
        'she will have finished the entire project. After that, she will be looking for a teaching position.'
    )
    run.italic = True
    run.font.size = Pt(font_size)
    set_paragraph_spacing(p, space_before=3, space_after=4)

    verb_phrases = [
        ('moved:', 'past simple'),
        ('has lived:', 'present perfect'),
        ('visited:', 'past simple'),
        ('was working:', 'past progressive'),
        ('has been writing:', 'present perfect progressive'),
        ('will have finished:', 'future perfect'),
        ('will be looking:', 'future progressive'),
    ]

    for verb, tense_aspect in verb_phrases:
        add_answer_line(doc, verb, tense_aspect, font_size, indent=0.7)

    # Exercise 20
    add_exercise(doc, 20, None, font_size)

    add_plain_line(doc,
        '"Moved" (past simple) presents the action as a completed event in the past \u2014 the move happened '
        'and is over. "Has lived" (present perfect) connects the past event to the present \u2014 she moved '
        'in 2018 and STILL lives there now. The writer uses past simple for the completed action of moving '
        'and present perfect for the ongoing state of living there, because the living continues into the present.',
        font_size)

    # Exercise 21
    add_exercise(doc, 21, 'She studies linguistics.', font_size)

    for sub, rewrite, explanation in [
        ('a) Past progressive:',
         '"She was studying linguistics."',
         'Changes from a habitual/general statement to a temporary, ongoing activity at a specific past moment.'),
        ('b) Present perfect:',
         '"She has studied linguistics."',
         'Changes from a current habit to a completed experience with present relevance (she has this knowledge now).'),
        ('c) Future perfect:',
         '"She will have studied linguistics (by graduation)."',
         'Projects the activity into the future as something that will be completed before a reference point.'),
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.35)
        run = p.add_run(sub)
        run.bold = True
        run.font.size = Pt(font_size)
        set_paragraph_spacing(p, space_before=3, space_after=2)

        add_plain_line(doc, f'Rewrite: {rewrite}', font_size, indent=0.7)
        add_plain_line(doc, f'Meaning change: {explanation}', font_size, indent=0.7)

    doc.save(str(output_path))
    print(f"Created: {output_path}")


def main():
    script_dir = Path(__file__).parent
    homework_dir = script_dir.parent / 'Homework'

    create_answer_key(
        homework_dir / 'Chapter 10 Answer Key.docx',
        font_size=12
    )

    create_answer_key(
        homework_dir / 'Homework 10 Overhead.docx',
        font_size=22
    )


if __name__ == '__main__':
    main()
