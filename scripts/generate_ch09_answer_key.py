#!/usr/bin/env python3
"""
Generate Chapter 9 Answer Key and Overhead Answer Key .docx files.
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
    """Create the Chapter 9 Answer Key document."""
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
    title = doc.add_heading('Chapter 9: Compound and Complex Sentences', level=1)
    title.runs[0].font.size = Pt(heading1_size)
    set_paragraph_spacing(title, space_before=0, space_after=6)

    subtitle = doc.add_heading('Answer Key', level=2)
    subtitle.runs[0].font.size = Pt(heading2_size)
    set_paragraph_spacing(subtitle, space_before=0, space_after=12)

    if overhead:
        add_spacer_row(doc)

    # =============================================
    # Part 1: Sentence Type Identification
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 1: Sentence Type Identification', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    # Exercise 1
    add_exercise(doc, 1,
        'The professor who taught my linguistics class has retired, but she still occasionally gives guest lectures.',
        body_size, font_name=body_font)

    add_answer_line(doc, 'Sentence type:', 'Compound-complex', body_size, font_name=body_font)
    add_plain_line(doc, 'Clauses:', body_size, bold_prefix='', font_name=body_font)
    add_plain_line(doc,
        '\u2022 "The professor...has retired" \u2014 IC',
        body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc,
        '\u2022 "who taught my linguistics class" \u2014 DC (relative clause modifying "professor")',
        body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc,
        '\u2022 "she still occasionally gives guest lectures" \u2014 IC',
        body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # Exercise 2
    add_exercise(doc, 2,
        'Because the deadline was extended, I had time to revise my paper thoroughly.',
        body_size, font_name=body_font)

    add_answer_line(doc, 'Sentence type:', 'Complex', body_size, font_name=body_font)
    add_plain_line(doc,
        '\u2022 "Because the deadline was extended" \u2014 DC (adverb clause, reason)',
        body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc,
        '\u2022 "I had time to revise my paper thoroughly" \u2014 IC',
        body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # Exercise 3
    add_exercise(doc, 3,
        'The exhausted marathon runner from Kenya and her experienced coach celebrated after the race.',
        body_size, font_name=body_font)

    add_answer_line(doc, 'Sentence type:', 'Simple', body_size, font_name=body_font)
    add_plain_line(doc,
        'One independent clause with a compound subject ("The exhausted marathon runner from Kenya" + "her experienced coach"). '
        '"After the race" is a prepositional phrase, not a dependent clause (no subject-verb pair).',
        body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # Exercise 4
    add_exercise(doc, 4, None, body_size, font_name=body_font)

    # 4a
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('a) ')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    run = p.add_run('The candidate who impressed the committee received the position.')
    run.italic = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)

    add_answer_line(doc, 'Dependent clause:', '"who impressed the committee"', body_size, indent=0.7, font_name=body_font)
    add_answer_line(doc, 'Type:', 'Relative clause (modifies "candidate")', body_size, indent=0.7, font_name=body_font)

    # 4b
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('b) ')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    run = p.add_run('I wonder whether she received my message.')
    run.italic = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)

    add_answer_line(doc, 'Dependent clause:', '"whether she received my message"', body_size, indent=0.7, font_name=body_font)
    add_answer_line(doc, 'Type:', 'Noun clause (direct object of "wonder")', body_size, indent=0.7, font_name=body_font)

    # 4c
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('c) ')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    run = p.add_run('We will leave when the meeting ends.')
    run.italic = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)

    add_answer_line(doc, 'Dependent clause:', '"when the meeting ends"', body_size, indent=0.7, font_name=body_font)
    add_answer_line(doc, 'Type:', 'Adverb clause (time)', body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # =============================================
    # Part 2: Sentence Completion
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 2: Sentence Completion', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    p = doc.add_paragraph()
    run = p.add_run('Exercises 5\u20138 are open-ended. Accept any grammatically correct completion that matches the requested element type.')
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=6)

    for num, prompt, sample in [
        (5, 'The evidence was compelling ________ the jury remained skeptical.',
         'Sample: ", but" or ", yet" (coordinating conjunction showing contrast)'),
        (6, '________ you finish your assignment, you may leave early.',
         'Sample: "When" or "After" or "Once" (subordinating conjunction, time)'),
        (7, 'The experiment produced unexpected results ________ the team decided to repeat it.',
         'Sample: "; therefore," or "; consequently," (semicolon + conjunctive adverb + comma)'),
        (8, 'The professor praised the students ________.',
         'Sample: "who completed the extra credit assignment" (dependent clause\u2014relative clause)'),
    ]:
        add_exercise(doc, num, prompt, body_size, font_name=body_font)
        add_plain_line(doc, sample, body_size, font_name=body_font)
        if overhead:
            add_spacer_row(doc)

    # =============================================
    # Part 3: Sentence Writing
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 3: Sentence Writing', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    p = doc.add_paragraph()
    run = p.add_run('Exercises 9\u201312 are open-ended. Accept any grammatically correct sentence that matches the requested structure.')
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=6)

    for num, structure, sample in [
        (9, 'Compound sentence with semicolon + conjunctive adverb',
         'Sample: "The test was difficult; however, most students passed."'),
        (10, 'Complex sentence with adverb clause (cause/reason)',
         'Sample: "Because the roads were icy, school was canceled."'),
        (11, 'Complex sentence with relative clause modifying the subject',
         'Sample: "The student who studied every night earned the highest grade."'),
        (12, 'Compound-complex sentence',
         'Sample: "Although the weather was terrible, the game continued, and the fans cheered."'),
    ]:
        add_exercise(doc, num, None, body_size, font_name=body_font)
        add_plain_line(doc, f'{structure}:', body_size, bold_prefix='Structure: ', font_name=body_font)
        add_plain_line(doc, sample, body_size, font_name=body_font)
        if overhead:
            add_spacer_row(doc)

    # =============================================
    # Part 4: Error Correction
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 4: Error Correction', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    # Exercise 13
    add_exercise(doc, 13,
        'The assignment was challenging, many students struggled to finish it on time.',
        body_size, font_name=body_font)
    add_plain_line(doc, 'Error type: Comma splice', body_size, bold_prefix='', font_name=body_font)
    add_plain_line(doc,
        'Correction 1: "The assignment was challenging, and many students struggled to finish it on time." (add coordinating conjunction)',
        body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc,
        'Correction 2: "The assignment was challenging; many students struggled to finish it on time." (replace comma with semicolon)',
        body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # Exercise 14
    add_exercise(doc, 14,
        'She enjoys hiking he prefers swimming.',
        body_size, font_name=body_font)
    add_plain_line(doc, 'Error type: Run-on (fused sentence)', body_size, bold_prefix='', font_name=body_font)
    add_plain_line(doc,
        'Correction 1: "She enjoys hiking, but he prefers swimming." (add comma + coordinating conjunction)',
        body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc,
        'Correction 2: "She enjoys hiking; he prefers swimming." (add semicolon)',
        body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # Exercise 15
    add_exercise(doc, 15,
        'The restaurant was crowded, we decided to order takeout instead.',
        body_size, font_name=body_font)
    add_plain_line(doc, 'Error type: Comma splice', body_size, bold_prefix='', font_name=body_font)
    add_plain_line(doc,
        'Correction 1: "The restaurant was crowded, so we decided to order takeout instead." (add coordinating conjunction)',
        body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc,
        'Correction 2: "Because the restaurant was crowded, we decided to order takeout instead." (subordinate one clause)',
        body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # =============================================
    # Part 5: Analysis and Reflection
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 5: Analysis and Reflection', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    # Exercise 16
    add_exercise(doc, 16,
        'The experiment failed, and the researchers were disappointed.',
        body_size, font_name=body_font)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('a) Emphasize disappointment (make it the main clause):')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)
    add_plain_line(doc,
        '"Because the experiment failed, the researchers were disappointed."',
        body_size, indent=0.7, font_name=body_font)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('b) Emphasize the failure (make it the main clause):')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)
    add_plain_line(doc,
        '"Although the researchers were disappointed, the experiment had failed."',
        body_size, indent=0.7, font_name=body_font)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('c) ')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    run = p.add_run(
        'The coordinated version (original) presents both ideas as equally important. '
        'Coordination is the best choice when neither idea should be subordinated to the other.'
    )
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)

    if overhead:
        add_spacer_row(doc)

    # Exercise 17
    add_exercise(doc, 17, None, body_size, font_name=body_font)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('Passage: ')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    run = p.add_run(
        'When the storm began, the hikers sought shelter. They found a small cave, '
        'and they waited there for hours. Although they were cold and hungry, they remained '
        'calm because they had prepared for emergencies.'
    )
    run.italic = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=4)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('a) Clauses:')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)

    add_plain_line(doc, 'Independent clauses:', body_size, indent=0.7, bold_prefix='', font_name=body_font)
    add_plain_line(doc, '\u2022 "the hikers sought shelter"', body_size, indent=1.0, font_name=body_font)
    add_plain_line(doc, '\u2022 "They found a small cave"', body_size, indent=1.0, font_name=body_font)
    add_plain_line(doc, '\u2022 "they waited there for hours"', body_size, indent=1.0, font_name=body_font)
    add_plain_line(doc, '\u2022 "they remained calm"', body_size, indent=1.0, font_name=body_font)

    add_plain_line(doc, 'Dependent clauses:', body_size, indent=0.7, bold_prefix='', font_name=body_font)
    add_plain_line(doc, '\u2022 "When the storm began" \u2014 adverb clause (time)', body_size, indent=1.0, font_name=body_font)
    add_plain_line(doc, '\u2022 "Although they were cold and hungry" \u2014 adverb clause (contrast)', body_size, indent=1.0, font_name=body_font)
    add_plain_line(doc, '\u2022 "because they had prepared for emergencies" \u2014 adverb clause (reason)', body_size, indent=1.0, font_name=body_font)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('b) Sentence types:')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)

    add_plain_line(doc,
        'Sentence 1: "When the storm began, the hikers sought shelter." \u2014 Complex (1 IC + 1 DC)',
        body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc,
        'Sentence 2: "They found a small cave, and they waited there for hours." \u2014 Compound (2 ICs)',
        body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc,
        'Sentence 3: "Although they were cold and hungry, they remained calm because they had prepared for emergencies." \u2014 Complex (1 IC + 2 DCs)',
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
        'Writers should choose coordination when two ideas are equally important and deserve '
        'equal emphasis. Subordination is preferable when one idea supports, explains, or provides '
        'context for another\u2014placing the less important idea in a dependent clause guides the reader '
        'to focus on the main point. For example, "The exam was difficult, and many students struggled" '
        '(coordination) presents both facts equally, while "Because the exam was difficult, many students '
        'struggled" (subordination) emphasizes the students\u2019 struggle and treats the exam\u2019s difficulty '
        'as background information.'
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
        homework_dir / 'Chapter 09 Answer Key.docx',
        font_size=12
    )

    # Create Overhead Answer Key
    create_answer_key(
        homework_dir / 'Homework 09 Overhead.docx',
        overhead=True
    )


if __name__ == '__main__':
    main()
