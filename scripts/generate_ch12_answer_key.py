#!/usr/bin/env python3
"""
Generate Chapter 12 Answer Key and Overhead Answer Key .docx files.
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
    """Create the Chapter 12 Answer Key document."""
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
    title = doc.add_heading('Chapter 12: Adverbials', level=1)
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
    add_exercise(doc, 1, 'Last week, the students studied diligently in the library.', body_size, font_name=body_font)
    add_answer_line(doc, 'Adverbial 1:', 'Last week \u2014 NP \u2014 time', body_size, font_name=body_font)
    add_answer_line(doc, 'Adverbial 2:', 'diligently \u2014 AdvP \u2014 manner', body_size, font_name=body_font)
    add_answer_line(doc, 'Adverbial 3:', 'in the library \u2014 PP \u2014 place', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 2
    add_exercise(doc, 2, 'If you need assistance, please call the help desk immediately.', body_size, font_name=body_font)
    add_answer_line(doc, 'Adverbial 1:', 'If you need assistance \u2014 adverb clause \u2014 condition', body_size, font_name=body_font)
    add_answer_line(doc, 'Adverbial 2:', 'immediately \u2014 AdvP \u2014 time', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # Exercise 3
    add_exercise(doc, 3, 'She left early to catch her flight.', body_size, font_name=body_font)
    add_answer_line(doc, 'Adverbial 1:', 'early \u2014 AdvP \u2014 time', body_size, font_name=body_font)
    add_answer_line(doc, 'Adverbial 2:', 'to catch her flight \u2014 infinitive phrase \u2014 purpose', body_size, font_name=body_font)
    if overhead:
        add_spacer_row(doc)

    # =============================================
    # Part 2: Adjunct, Disjunct, or Conjunct
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 2: Adjunct, Disjunct, or Conjunct', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    classifications = [
        (4, 'She answered the questions honestly.',
         'adjunct',
         'Honestly modifies the verb answered, telling how she answered (manner). '
         'It is integrated into the clause and can be questioned: "Did she answer honestly?"'),
        (5, 'Honestly, I don\u2019t think that\u2019s a good idea.',
         'disjunct',
         'Honestly expresses the speaker\u2019s stance/attitude toward the statement. '
         'It is not part of the proposition \u2014 it cannot be questioned or negated within the clause.'),
        (6, 'The data were inconclusive. Nevertheless, the researchers published their findings.',
         'conjunct',
         'Nevertheless connects the two sentences, showing a contrast/concession relationship between them.'),
        (7, 'He spoke softly so the children wouldn\u2019t wake up.',
         'adjunct',
         'Softly modifies the verb spoke, telling how he spoke (manner). It is integrated into the clause.'),
        (8, 'The experiment failed. Therefore, they redesigned the protocol.',
         'conjunct',
         'Therefore connects the two sentences, showing a cause-result relationship.'),
    ]

    for num, sentence, classification, explanation in classifications:
        add_exercise(doc, num, sentence, body_size, font_name=body_font)
        add_answer_line(doc, 'Classification:', classification, body_size, font_name=body_font)
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
    run = p.add_run('Exercises 9\u201313 are open-ended. Accept any grammatically correct adverbial of the requested type.')
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=6)

    completions = [
        (9, 'PP of time: __________, the committee will announce its decision.',
         '"After the meeting, the committee will announce its decision."'),
        (10, 'Adverb clause of reason: She stayed home __________.',
         '"She stayed home because she was feeling ill."'),
        (11, 'Infinitive phrase of purpose: He went to the store __________.',
         '"He went to the store to buy groceries."'),
        (12, 'Adverb clause of concession: __________, we decided to proceed with the project.',
         '"Although the budget was tight, we decided to proceed with the project."'),
        (13, 'Participial phrase as adverbial: __________, she answered all the questions correctly.',
         '"Having studied all night, she answered all the questions correctly."'),
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
    run = p.add_run('Exercises 14\u201318 are open-ended. Accept any grammatically correct sentence that demonstrates the requested structure.')
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=6)

    writing = [
        (14, 'Adverb clause of time',
         '"While the children were playing outside, their parents prepared dinner."'),
        (15, 'Disjunct expressing attitude',
         '"Unfortunately, the flight was delayed by three hours."'),
        (16, 'Conjunct showing contrast',
         '"The restaurant was expensive. However, the food was outstanding."'),
        (17, 'Adverb clause of purpose',
         '"She whispered so that the baby wouldn\u2019t wake up."'),
        (18, 'Participial phrase as adverbial of reason',
         '"Exhausted from the long hike, they decided to set up camp early."'),
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

    # Exercise 19
    add_exercise(doc, 19, None, body_size, font_name=body_font)
    add_plain_line(doc, 'Identify five adverbials in the passage:', body_size, font_name=body_font)

    adverbials = [
        ('Yesterday', 'NP', 'time'),
        ('finally', 'AdvP', 'time (completion)'),
        ('Surprisingly', 'AdvP (disjunct)', 'speaker attitude'),
        ('diligently', 'AdvP', 'manner'),
        ('for three years', 'PP', 'time (duration)'),
        ('because funding was severely limited', 'adverb clause', 'reason'),
        ('in a prestigious journal', 'PP', 'place'),
        ('last month', 'NP', 'time'),
        ('If additional funding becomes available', 'adverb clause', 'condition'),
        ('next year', 'NP', 'time'),
        ('in a new laboratory', 'PP', 'place'),
    ]

    add_plain_line(doc, 'Any five of the following are acceptable:', body_size, font_name=body_font)

    for adv, form, role in adverbials:
        add_plain_line(doc, f'"{adv}" \u2014 {form} \u2014 {role}', body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # Exercise 20
    add_exercise(doc, 20, None, body_size, font_name=body_font)
    add_plain_line(doc,
        '"Surprisingly" is a disjunct because it comments on the entire sentence from the '
        'speaker\u2019s perspective \u2014 it expresses the speaker\u2019s surprise at the '
        'results. It is not part of the proposition: you cannot ask "Did the results '
        'surprisingly contradict the findings?" in the same way.',
        body_size, font_name=body_font)
    add_plain_line(doc,
        '"Diligently" is an adjunct because it modifies the verb "worked," telling how '
        'they worked. It is integrated into the clause structure: you can question it '
        '("Did they work diligently?") and negate it ("They didn\u2019t work diligently").',
        body_size, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # Exercise 21
    add_exercise(doc, 21, None, body_size, font_name=body_font)
    add_plain_line(doc, 'Rewrite with "yesterday" in three positions:', body_size, font_name=body_font)

    positions = [
        ('Initial:', '"Yesterday, the researchers finally completed their groundbreaking study."',
         'Sets the time frame first; "yesterday" functions as a scene-setting topic.'),
        ('Medial:', '"The researchers yesterday finally completed their groundbreaking study."',
         'Places "yesterday" closer to the verb; slightly unusual but emphasizes the recency.'),
        ('Final:', '"The researchers finally completed their groundbreaking study yesterday."',
         'Default/neutral position; "yesterday" receives end-focus as new information.'),
    ]

    for label, rewrite, effect in positions:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.35)
        run = p.add_run(label)
        run.bold = True
        run.font.size = Pt(body_size)
        run.font.name = body_font
        set_paragraph_spacing(p, space_before=3, space_after=2)

        add_plain_line(doc, rewrite, body_size, indent=0.7, font_name=body_font)
        add_plain_line(doc, f'Effect: {effect}', body_size, indent=0.7, font_name=body_font)

    doc.save(str(output_path))
    print(f"Created: {output_path}")


def main():
    script_dir = Path(__file__).parent
    homework_dir = script_dir.parent / 'Homework'

    create_answer_key(
        homework_dir / 'Chapter 12 Answer Key.docx',
        font_size=12
    )

    create_answer_key(
        homework_dir / 'Homework 12 Overhead.docx',
        overhead=True
    )


if __name__ == '__main__':
    main()
