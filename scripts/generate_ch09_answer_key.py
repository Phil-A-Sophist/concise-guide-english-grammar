#!/usr/bin/env python3
"""
Generate Chapter 9 Answer Key and Overhead Answer Key .docx files.
Updated to match revised homework structure: Conjunctions and Clauses (5 parts, 14 exercises).
"""

from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def set_paragraph_spacing(paragraph, space_before=0, space_after=0):
    pPr = paragraph._p.get_or_add_pPr()
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:before'), str(int(space_before * 20)))
    spacing.set(qn('w:after'), str(int(space_after * 20)))
    pPr.append(spacing)


def add_spacer_row(doc):
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
    sz.set(qn('w:val'), '40')
    rPr.append(sz)
    pPr.append(rPr)
    set_paragraph_spacing(p, space_before=0, space_after=0)
    return p


def add_exercise(doc, number, sentence, font_size, font_name=None):
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


def add_sub_sentence(doc, sub, sentence, font_size, font_name=None):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run(f'{sub} ')
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
    set_paragraph_spacing(p, space_before=3, space_after=2)
    return p


def create_answer_key(output_path, font_size=12, overhead=False):
    if overhead:
        body_font = 'Arial Narrow'
        body_size = 18
        heading1_size = 22
        heading2_size = 20
        heading3_size = 16
    else:
        body_font = 'Garamond'
        body_size = font_size
        heading1_size = 16
        heading2_size = 14
        heading3_size = 12

    doc = Document()

    style = doc.styles['Normal']
    style.font.name = body_font
    style.font.size = Pt(body_size)

    for i in range(1, 4):
        heading_style = doc.styles[f'Heading {i}']
        heading_style.font.name = 'Open Sans' if not overhead else 'Arial Narrow'
        heading_style.font.bold = True

    # Title
    title = doc.add_heading('Chapter 9: Conjunctions and Clauses', level=1)
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
        '\u2022 "The professor\u2026has retired" \u2014 IC',
        body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc,
        '\u2022 "who taught my linguistics class" \u2014 DC (modifies "professor")',
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
        '\u2022 "Because the deadline was extended" \u2014 DC (dependent clause, reason)',
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
        'One independent clause with a compound NP subject ("The exhausted marathon runner from Kenya" + '
        '"her experienced coach"). "After the race" is a prepositional phrase, not a dependent clause '
        '(no subject-verb pair). The compound NP keeps both names as NPs inside a larger NP — '
        'not two separate clauses.',
        body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # =============================================
    # Part 2: Sentence Writing
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 2: Sentence Writing', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    p = doc.add_paragraph()
    run = p.add_run('Exercises 4\u20137 are open-ended. Accept any grammatically correct sentence that matches the requested structure.')
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=6)

    # Exercise 4: compound sentence with semicolon + conjunctive adverb
    add_exercise(doc, 4, None, body_size, font_name=body_font)
    add_plain_line(doc, 'Structure: Compound sentence using semicolon + conjunctive adverb + comma', body_size, bold_prefix='', font_name=body_font)
    add_plain_line(doc, 'Sample: "The test was difficult; however, most students passed."', body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc, 'Also acceptable: "The project was late. Nevertheless, the client was satisfied."', body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # Exercise 5: complex sentence with cause/reason
    add_exercise(doc, 5, None, body_size, font_name=body_font)
    add_plain_line(doc, 'Structure: Complex sentence with dependent clause showing cause/reason', body_size, bold_prefix='', font_name=body_font)
    add_plain_line(doc, 'Sample: "Because the roads were icy, school was canceled."', body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc, 'Also acceptable: "She left early since she had an appointment."', body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # Exercise 6: compound-complex sentence
    add_exercise(doc, 6, None, body_size, font_name=body_font)
    add_plain_line(doc, 'Structure: Compound-complex (two ICs joined by FANBOYS + at least one DC)', body_size, bold_prefix='', font_name=body_font)
    add_plain_line(doc, 'Sample: "Although the weather was terrible, the game continued, and the fans cheered."', body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc, 'Sample: "She studied all night because the exam was important, and she passed."', body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc, 'Check: two ICs connected by a coordinating conjunction + at least one DC with a subordinating conjunction.', body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # Exercise 7: DC first vs last, emphasis
    add_exercise(doc, 7, None, body_size, font_name=body_font)
    add_plain_line(doc, 'Structure: Complex sentence — one version DC first, one version DC last', body_size, bold_prefix='', font_name=body_font)
    add_plain_line(doc, 'Sample Version 1 (DC first): "Because she studied all week, she passed the exam."', body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc, 'Sample Version 2 (DC last): "She passed the exam because she studied all week."', body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc,
        'More emphasis on main clause: Version 2 places the main clause first and unqualified. '
        'Version 1 announces background context first, so the main clause feels like a conclusion. '
        'Both are correct — the choice depends on what the writer wants the reader to notice first.',
        body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # =============================================
    # Part 3: Error Correction
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 3: Error Correction', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    # Exercise 8
    add_exercise(doc, 8,
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

    # Exercise 9
    add_exercise(doc, 9,
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

    # Exercise 10
    add_exercise(doc, 10,
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
    # Part 4: Sentence Tables and Diagrams
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 4: Sentence Tables and Diagrams', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    add_exercise(doc, 11, 'Complete the table and draw a tree diagram for each sentence.', body_size, font_name=body_font)

    table_items = [
        ('a)', 'Compound NP (simple sentence): Marcus and Elena traveled.',
         '"Marcus" \u2192 NP | "and Elena" \u2192 NP (conjoined) | overall subject \u2192 compound NP | "traveled" \u2192 VP',
         '[S [NP [NP [N Marcus]] [CONJ and] [NP [N Elena]]] [VP [V traveled]]]',
         'Simple sentence (one IC). The conjunction joins two NPs into a larger compound NP subject — not two clauses.'),
        ('b)', 'Compound VP (simple sentence): The dog barked and chased the squirrel.',
         '"The dog" \u2192 NP (S) | "barked" \u2192 VP | "chased the squirrel" \u2192 VP (conjoined) | overall predicate \u2192 compound VP',
         '[S [NP [DET The] [N dog]] [VP [VP [V barked]] [CONJ and] [VP [V chased] [NP [DET the] [N squirrel]]]]]',
         'Simple sentence (one IC). Each conjunct keeps its own VP node inside the compound VP.'),
        ('c)', 'Compound sentence: She writes poetry, and he composes music.',
         '"She writes poetry" \u2192 IC | "and" \u2192 CONJ | "he composes music" \u2192 IC',
         '[S [IC [NP [PRON She]] [VP [V writes] [NP [N poetry]]]] [CONJ and] [IC [NP [PRON he]] [VP [V composes] [NP [N music]]]]]',
         'Compound sentence (two ICs). Each side has its own subject and predicate.'),
        ('d)', 'Complex sentence: When it rained, we stayed inside.',
         '"When it rained" \u2192 DC | "we stayed inside" \u2192 IC | subordinating conjunction: "When"',
         '[S [DC [SUB When] [NP [PRON it]] [VP [V rained]]] [IC [NP [PRON we]] [VP [V stayed] [ADVP [ADV inside]]]]]',
         'Complex sentence (1 IC + 1 DC). The DC comes first and is followed by a comma.'),
    ]

    for sub, label, table_text, bracket, note in table_items:
        add_sub_sentence(doc, sub, label, body_size, font_name=body_font)
        add_plain_line(doc, f'Table: {table_text}', body_size, indent=0.7, font_name=body_font)
        add_plain_line(doc, f'Bracket notation: {bracket}', body_size, indent=0.7, font_name=body_font)
        add_plain_line(doc, f'Note: {note}', body_size, indent=0.7, font_name=body_font)
        if overhead:
            add_spacer_row(doc)

    # =============================================
    # Part 5: Emphasis, End-Weight, and Clause Revision
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 5: Emphasis, End-Weight, and Clause Revision', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    # Exercise 12: emphasis (subordination for different effects)
    add_exercise(doc, 12,
        'The experiment failed, and the researchers were disappointed.',
        body_size, font_name=body_font)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('a) Emphasize disappointment (make "the researchers were disappointed" the main clause):')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)
    add_plain_line(doc,
        '"Because the experiment failed, the researchers were disappointed."',
        body_size, indent=0.7, font_name=body_font)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('b) Emphasize the failure (make "the experiment failed" the main clause):')
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
        'Coordination is the best choice when neither idea should be pushed into the background. '
        'Both facts carry equal weight in the original — using "and" signals this equality.'
    )
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)

    if overhead:
        add_spacer_row(doc)

    # Exercise 13: end-weight
    add_exercise(doc, 13, None, body_size, font_name=body_font)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('Original (front-loaded): ')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    run = p.add_run('That the committee rejected the proposal without reading it completely surprised the students.')
    run.italic = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('a) End-weighted revision:')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)
    add_plain_line(doc,
        '"The students were surprised that the committee rejected the proposal without reading it completely."',
        body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc,
        'Also acceptable: "It surprised the students that the committee rejected the proposal without reading it completely."',
        body_size, indent=0.7, font_name=body_font)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('b) Why is the revised version easier to read?')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)
    add_plain_line(doc,
        'End-weight: placing the heavy noun clause ("that the committee rejected\u2026") at the end allows '
        'readers to process the main point first ("The students were surprised"), then receive the explanation. '
        'In the original, readers must hold the long clause in memory before they know what the sentence is about.',
        body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # Exercise 14: clause density revision
    add_exercise(doc, 14, None, body_size, font_name=body_font)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('Original: ')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    run = p.add_run('The lecture was long and the material was difficult and students were confused and they asked many questions and the professor stayed late to help.')
    run.italic = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('Revised passage:')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)
    add_plain_line(doc,
        'Sample: "Because the lecture was long and the material was difficult, students were confused '
        'and asked many questions. The professor stayed late to help."',
        body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc,
        'Other arrangements acceptable as long as at least one subordinating conjunction is used and the logical '
        'relationships (cause \u2192 effect) are made explicit.',
        body_size, indent=0.7, font_name=body_font)

    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    run = p.add_run('Explanation of one revision:')
    run.bold = True
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)
    add_plain_line(doc,
        'Sample: Using "because" to subordinate the two cause clauses ("the lecture was long," "the material was '
        'difficult") makes explicit that these are reasons for the students\'s confusion, not just separate events. '
        'Subordination changes what the reader sees as the main point: the confusion and questions, not the lecture length.',
        body_size, indent=0.7, font_name=body_font)

    doc.save(str(output_path))
    print(f'Created: {output_path}')


def main():
    script_dir = Path(__file__).parent
    homework_dir = script_dir.parent / 'Homework'

    create_answer_key(
        homework_dir / 'Chapter 09 Answer Key.docx',
        font_size=12
    )

    create_answer_key(
        homework_dir / 'Homework 09 Overhead.docx',
        overhead=True
    )


if __name__ == '__main__':
    main()
