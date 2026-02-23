#!/usr/bin/env python3
"""
Generate Chapter 11 Answer Key and Overhead Answer Key .docx files.
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
    """Create the Chapter 11 Answer Key document."""
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
    title = doc.add_heading('Chapter 11: Verbs Part Two \u2014 Voice and Modals', level=1)
    title.runs[0].font.size = Pt(heading1_size)
    set_paragraph_spacing(title, space_before=0, space_after=6)

    subtitle = doc.add_heading('Answer Key', level=2)
    subtitle.runs[0].font.size = Pt(heading2_size)
    set_paragraph_spacing(subtitle, space_before=0, space_after=12)

    if overhead:
        add_spacer_row(doc)

    # =============================================
    # Part 1: Voice Identification
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 1: Voice Identification', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    # Exercise 1
    add_exercise(doc, 1, 'The researchers carefully analyzed the data.', body_size, font_name=body_font)
    add_answer_line(doc, 'Voice:', 'active', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 2
    add_exercise(doc, 2, 'Three errors were discovered in the code.', body_size, font_name=body_font)
    add_answer_line(doc, 'Voice:', 'passive', body_size, font_name=body_font)
    add_answer_line(doc, 'Agent:', 'none stated', body_size, font_name=body_font)
    add_plain_line(doc, 'Active version: "Someone discovered three errors in the code."', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 3
    add_exercise(doc, 3, 'The new policy will be announced tomorrow.', body_size, font_name=body_font)
    add_answer_line(doc, 'Voice:', 'passive', body_size, font_name=body_font)
    add_answer_line(doc, 'Agent:', 'none stated', body_size, font_name=body_font)
    add_plain_line(doc, 'Active version: "Someone/They will announce the new policy tomorrow."', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 4
    add_exercise(doc, 4, 'Someone stole my bicycle last night.', body_size, font_name=body_font)
    add_answer_line(doc, 'Voice:', 'active', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 5
    add_exercise(doc, 5, 'The building was constructed in 1920.', body_size, font_name=body_font)
    add_answer_line(doc, 'Voice:', 'passive', body_size, font_name=body_font)
    add_answer_line(doc, 'Agent:', 'none stated', body_size, font_name=body_font)
    add_plain_line(doc, 'Active version: "Someone/They constructed the building in 1920."', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # =============================================
    # Part 2: Voice Transformation
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 2: Voice Transformation', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    transformations = [
        (6, 'Active to passive: The team is preparing the presentation.',
         'The presentation is being prepared by the team.'),
        (7, 'Active to passive: Someone had stolen the documents before the investigation began.',
         'The documents had been stolen before the investigation began.'),
        (8, 'Passive to active: The experiment was conducted by the research team.',
         'The research team conducted the experiment.'),
        (9, 'Passive to active: The proposal will be reviewed by the committee next week.',
         'The committee will review the proposal next week.'),
        (10, 'Active to passive: The company will hire fifty new employees.',
         'Fifty new employees will be hired by the company.'),
    ]

    for num, prompt, answer in transformations:
        add_exercise(doc, num, prompt, body_size, font_name=body_font)
        add_answer_line(doc, 'Answer:', answer, body_size, font_name=body_font)
        if overhead:
            add_spacer_row(doc)

    # =============================================
    # Part 3: Modal Meaning
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 3: Modal Meaning', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    modals = [
        (11, 'She can speak three languages fluently.',
         [('Modal:', 'can'), ('Meaning:', 'ability')]),
        (12, 'That might be the correct answer, but I\u2019m not certain.',
         [('Modal:', 'might'), ('Meaning:', 'possibility')]),
        (13, 'You should apologize for your mistake.',
         [('Modal:', 'should'), ('Meaning:', 'advice')]),
        (14, 'He must be exhausted after running the marathon.',
         [('Modal:', 'must'), ('Meaning:', 'deduction (epistemic)')]),
        (15, 'May I leave the room early?',
         [('Modal:', 'may'), ('Meaning:', 'permission')]),
        (16, 'They could have won the game if they had practiced more.',
         [('Modal:', 'could (have)'), ('Meaning:', 'past possibility (unrealized)')]),
    ]

    for num, sentence, answers in modals:
        add_exercise(doc, num, sentence, body_size, font_name=body_font)
        for label, answer in answers:
            add_answer_line(doc, label, answer, body_size, font_name=body_font)
        if overhead:
            add_spacer_row(doc)

    # Exercise 17
    add_exercise(doc, 17, None, body_size, font_name=body_font)
    add_plain_line(doc, 'Explain the difference between the two uses of must:', body_size, font_name=body_font)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('a) ')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    run = p.add_run('You must wear a seatbelt.')
    run.italic = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)

    add_plain_line(doc,
        'Meaning type: deontic (obligation). The speaker is stating a rule or requirement '
        'that the listener is obligated to follow.',
        body_size, indent=0.7, font_name=body_font)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('b) ')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    run = p.add_run('She\u2019s not answering the phone. She must be asleep.')
    run.italic = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)

    add_plain_line(doc,
        'Meaning type: epistemic (deduction). The speaker is drawing a logical conclusion '
        'based on evidence (she\u2019s not answering), not imposing an obligation.',
        body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # =============================================
    # Part 4: Sentence Writing
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 4: Sentence Writing', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    p = doc.add_paragraph()
    run = p.add_run('Exercises 18\u201322 are open-ended. Accept any grammatically correct sentence that meets the stated criteria.')
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=6)

    writing = [
        (18, 'Passive voice for scientific writing',
         '"The samples were analyzed using mass spectrometry."'),
        (19, 'Should have + past participle (criticism/regret)',
         '"You should have called before stopping by."'),
        (20, 'Must for logical deduction (not obligation)',
         '"The lights are off\u2014they must have gone to bed already."'),
        (21, 'Could for past unrealized possibility',
         '"We could have taken the train, but we decided to drive instead."'),
        (22, 'Get-passive for unexpected event',
         '"She got promoted after only three months on the job."'),
    ]

    for num, structure, sample in writing:
        add_exercise(doc, num, None, body_size, font_name=body_font)
        add_plain_line(doc, f'{structure}:', body_size, bold_prefix='Prompt: ', font_name=body_font)
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
    add_plain_line(doc, 'Identify passive voice constructions in the passage:', body_size, font_name=body_font)

    passives = [
        ('was announced (yesterday by the CEO)',
         'Focuses on the policy (the topic) rather than the CEO; maintains topic continuity '
         'from the subject "The new policy."'),
        ('will be made (after all responses have been reviewed)',
         'Agent is unspecified, emphasizing the process and the decision rather than who '
         'will make it; creates a sense of objectivity.'),
        ('have been reviewed',
         'Embedded passive in the subordinate clause; keeps "responses" as the focus '
         'rather than naming who will review them.'),
    ]

    for i, (construction, reason) in enumerate(passives, 1):
        add_plain_line(doc, f'Passive {i}: "{construction}"', body_size, indent=0.35, font_name=body_font)
        add_plain_line(doc, f'Reason: {reason}', body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # Exercise 24
    add_exercise(doc, 24, None, body_size, font_name=body_font)
    add_plain_line(doc, 'Identify modals and classify as epistemic or deontic:', body_size, font_name=body_font)

    modal_analysis = [
        ('must (submit)', 'deontic \u2014 obligation (employees are required to submit feedback)'),
        ('should (improve)', 'epistemic \u2014 expectation/prediction (management believes the changes will likely improve efficiency)'),
        ('might (create)', 'epistemic \u2014 possibility (workers think it is possible the policy will create challenges)'),
        ('will (be made)', 'epistemic \u2014 prediction about the future (the decision will happen after review)'),
    ]

    for modal, classification in modal_analysis:
        add_answer_line(doc, f'{modal}:', classification, body_size, indent=0.35, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # Exercise 25
    add_exercise(doc, 25, 'The manager rejected the proposal.', body_size, font_name=body_font)

    for sub, answer in [
        ('a) Passive rewrite:',
         '"The proposal was rejected by the manager." (or without agent: "The proposal was rejected.")'),
        ('b) When passive is more appropriate:',
         'When the focus is on the proposal rather than the manager \u2014 for example, '
         'in a report about the proposal\u2019s status, or when the writer wants to '
         'de-emphasize who made the decision to soften the tone.'),
        ('c) When active is preferred:',
         'When accountability matters \u2014 for example, when it is important to know '
         'exactly who rejected the proposal, or when the writer wants a direct, '
         'clear statement of responsibility.'),
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.35)
        run = p.add_run(sub)
        run.bold = True
        run.font.size = Pt(body_size)
        run.font.name = body_font
        set_paragraph_spacing(p, space_before=3, space_after=2)

        add_plain_line(doc, answer, body_size, indent=0.7, font_name=body_font)

    doc.save(str(output_path))
    print(f"Created: {output_path}")


def main():
    script_dir = Path(__file__).parent
    homework_dir = script_dir.parent / 'Homework'

    create_answer_key(
        homework_dir / 'Chapter 11 Answer Key.docx',
        font_size=12
    )

    create_answer_key(
        homework_dir / 'Homework 11 Overhead.docx',
        overhead=True
    )


if __name__ == '__main__':
    main()
