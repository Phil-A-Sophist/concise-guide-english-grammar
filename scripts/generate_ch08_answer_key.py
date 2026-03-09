#!/usr/bin/env python3
"""
Generate Chapter 8 Answer Key and Overhead Answer Key .docx files.
Updated to match revised homework structure (5 parts, 14 exercises).
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
    """Add a sub-part label (a, b, c...) with italic sentence."""
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

    # Exercise 1: Identify DO/IO/SC/OC
    add_exercise(doc, 1, None, body_size, font_name=body_font)

    add_sub_sentence(doc, 'a)', 'The committee awarded the outstanding student a prestigious scholarship.', body_size, font_name=body_font)
    add_answer_line(doc, 'Indirect Object (IO):', 'the outstanding student', body_size, indent=0.7, font_name=body_font)
    add_answer_line(doc, 'Direct Object (DO):', 'a prestigious scholarship', body_size, indent=0.7, font_name=body_font)

    add_sub_sentence(doc, 'b)', 'The homemade soup tasted absolutely delicious.', body_size, font_name=body_font)
    add_answer_line(doc, 'Subject Complement (SC):', 'absolutely delicious (AdjP)', body_size, indent=0.7, font_name=body_font)

    add_sub_sentence(doc, 'c)', 'The judges declared the young contestant the winner.', body_size, font_name=body_font)
    add_answer_line(doc, 'Direct Object (DO):', 'the young contestant', body_size, indent=0.7, font_name=body_font)
    add_answer_line(doc, 'Object Complement (OC):', 'the winner (NP)', body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # Exercise 2: Argument vs. adverbial
    add_exercise(doc, 2, None, body_size, font_name=body_font)

    for sub, sentence, verdict, explanation in [
        ('a)', 'She placed the documents on the desk.',
         'Argument (required)',
         '"On the desk" is required by "placed." Remove it: *She placed the documents. \u2717 — ungrammatical without a location argument.'),
        ('b)', 'She found the documents on the desk.',
         'Adverbial (optional)',
         '"On the desk" is an optional location modifier. Remove it: She found the documents. \u2713 — still grammatical.'),
        ('c)', 'The professor is extremely knowledgeable about linguistics.',
         'Argument (required)',
         '"Extremely knowledgeable about linguistics" is the subject complement required by "is." Remove it: *The professor is. \u2717 — incomplete.'),
        ('d)', 'The professor lectured extremely knowledgeably about linguistics.',
         'Adverbial (optional)',
         '"Extremely knowledgeably about linguistics" is an optional manner/topic modifier. Remove it: The professor lectured. \u2713 — still grammatical.'),
    ]:
        add_sub_sentence(doc, sub, sentence, body_size, font_name=body_font)
        add_answer_line(doc, 'Answer:', verdict, body_size, indent=0.7, font_name=body_font)
        add_plain_line(doc, explanation, body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # =============================================
    # Part 2: Sentence Pattern Identification
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 2: Sentence Pattern Identification', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    patterns = [
        (3, 'The exhausted marathon runner collapsed at the finish line yesterday.',
         'Pattern 1 (Intransitive)',
         'Main verb: "collapsed." "At the finish line" and "yesterday" are adverbials (optional — answer where? and when?). '
         'Without adverbials: "The exhausted marathon runner collapsed." — complete with subject + intransitive verb. '
         '"Collapsed" does not require an object or complement.'),
        (4, "My grandmother's secret recipe remains a family treasure.",
         'Pattern 3 (Linking verb)',
         'Main verb: "remains." "A family treasure" is a subject complement (NP identifying the subject). '
         'Be substitution test: "My grandmother\'s secret recipe is a family treasure" \u2713. '
         'Since the verb is not "be" itself but passes the be-substitution test, this is Pattern 3 (Linking), not Pattern 2 (Copular be).'),
        (5, 'The committee considered the proposal inadequate.',
         'Pattern 6 (Ditransitive: DO + OC)',
         'Main verb: "considered." Two elements follow the verb: "the proposal" (NP) + "inadequate" (AdjP). '
         'Do they refer to the same thing? Yes — the proposal is described as inadequate. '
         'Therefore "the proposal" = Direct Object, "inadequate" = Object Complement.'),
        (6, 'The chef prepared the guests an extraordinary seven-course meal.',
         'Pattern 5 (Ditransitive: IO + DO)',
         'Main verb: "prepared." Two NPs follow the verb: "the guests" and "an extraordinary seven-course meal." '
         'Do they refer to the same thing? No — the guests \u2260 the meal. '
         'Can rephrase with "for": "prepared an extraordinary seven-course meal for the guests." '
         '"The guests" = Indirect Object, "an extraordinary seven-course meal" = Direct Object.'),
        (7, 'The situation grew increasingly tense during the negotiations.',
         'Pattern 3 (Linking verb)',
         'Main verb: "grew." "During the negotiations" is an adverbial (time) — set aside. '
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
    # Part 3: Sentence Writing
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 3: Sentence Writing', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    p = doc.add_paragraph()
    run = p.add_run('Exercises 8\u201310 are open-ended. Accept any grammatically correct sentence that follows the requested pattern with elements correctly labeled.')
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=6)

    for num, pattern_label, sample in [
        (8, 'Pattern 4 (S + V + DO)',
         'Sample: "[The dog]_S [chased]_V [the cat]_DO."'),
        (9, 'Pattern 5 (S + V + IO + DO)',
         'Sample: "[The teacher]_S [gave]_V [the students]_IO [a quiz]_DO."'),
        (10, 'Pattern 6 (S + V + DO + OC)',
         'Sample: "[The class]_S [elected]_V [Maria]_DO [president]_OC."'),
    ]:
        add_exercise(doc, num, None, body_size, font_name=body_font)
        add_plain_line(doc, f'{pattern_label}:', body_size, bold_prefix='Pattern: ', font_name=body_font)
        add_plain_line(doc, sample, body_size, font_name=body_font)
        if overhead:
            add_spacer_row(doc)

    # =============================================
    # Part 4: Sentence Tables and Diagrams
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 4: Sentence Tables and Diagrams', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    add_exercise(doc, 11, 'Complete each table and draw a tree diagram.', body_size, font_name=body_font)

    table_items = [
        ('a)', 'Pattern 1 (Intransitive): Birds sing.',
         [('Birds', 'S (NP)'), ('sing', 'V (VP)')],
         '[S [NP [N Birds]] [VP [V sing]]]'),
        ('b)', 'Pattern 2 (Copular Be): The solution was simple.',
         [('The solution', 'S (NP)'), ('was', 'V (be)'), ('simple', 'SC (AdjP)')],
         '[S [NP [DET The] [N solution]] [VP [V was] [ADJP [ADJ simple]]]]'),
        ('c)', 'Pattern 3 (Linking Verb): The music sounded beautiful.',
         [('The music', 'S (NP)'), ('sounded', 'V (LV)'), ('beautiful', 'SC (AdjP)')],
         '[S [NP [DET The] [N music]] [VP [V sounded] [ADJP [ADJ beautiful]]]]'),
        ('d)', 'Pattern 4 (Transitive): The student finished the report.',
         [('The student', 'S (NP)'), ('finished', 'V'), ('the report', 'DO (NP)')],
         '[S [NP [DET The] [N student]] [VP [V finished] [NP [DET the] [N report]]]]'),
        ('e)', 'Pattern 5 (Ditransitive, IO + DO): The professor gave the class a deadline.',
         [('The professor', 'S (NP)'), ('gave', 'V'), ('the class', 'IO (NP)'), ('a deadline', 'DO (NP)')],
         '[S [NP [DET The] [N professor]] [VP [V gave] [NP [DET the] [N class]] [NP [DET a] [N deadline]]]]'),
        ('f)', 'Pattern 6 (Ditransitive, DO + OC): The board declared the plan inadequate.',
         [('The board', 'S (NP)'), ('declared', 'V'), ('the plan', 'DO (NP)'), ('inadequate', 'OC (AdjP)')],
         '[S [NP [DET The] [N board]] [VP [V declared] [NP [DET the] [N plan]] [ADJP [ADJ inadequate]]]]'),
    ]

    for sub, label, cells, bracket in table_items:
        add_sub_sentence(doc, sub, label, body_size, font_name=body_font)
        # Show table labels
        table_text = ' | '.join(f'"{phrase}" \u2192 {lbl}' for phrase, lbl in cells)
        add_plain_line(doc, f'Table: {table_text}', body_size, indent=0.7, font_name=body_font)
        add_plain_line(doc, f'Bracket notation: {bracket}', body_size, indent=0.7, font_name=body_font)
        if overhead:
            add_spacer_row(doc)

    # =============================================
    # Part 5: Analysis and Reflection
    # =============================================
    doc.add_page_break()
    part = doc.add_heading('Part 5: Analysis and Reflection', level=3)
    part.runs[0].font.size = Pt(heading3_size)

    # Exercise 12: "put" valency
    add_exercise(doc, 12, 'She put the book on the shelf.', body_size, font_name=body_font)

    for sub, answer in [
        ('What happens if you remove "the book"?',
         '*She put on the shelf. \u2717 — ungrammatical. "The book" is a required argument (Direct Object).'),
        ('What happens if you remove "on the shelf"?',
         '*She put the book. \u2717 — ungrammatical/incomplete. "On the shelf" is a required locative argument.'),
        ('What does this tell you about the valency of "put"?',
         '"Put" requires THREE arguments: a subject, a direct object, and a locative phrase. '
         'It has valency 3 — unusual among English verbs, most of which require only two.'),
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

    # Exercise 13: linking vs transitive
    add_exercise(doc, 13, None, body_size, font_name=body_font)

    add_sub_sentence(doc, 'a)', 'The milk smells sour. vs. The detective smells trouble.', body_size, font_name=body_font)
    add_plain_line(doc,
        '"The milk smells sour" — linking verb (Pattern 3). "Sour" is a subject complement describing the milk.',
        body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc,
        '"The detective smells trouble" — transitive verb (Pattern 4). "Trouble" is a direct object.',
        body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc,
        'Be substitution test: "The milk is sour" \u2713 (makes sense \u2192 linking). '
        '"The detective is trouble" \u2717 (doesn\'t make sense \u2192 not linking, therefore transitive).',
        body_size, indent=0.7, font_name=body_font)

    if overhead:
        add_spacer_row(doc)

    # Exercise 14: argument vs adverbial reflection
    add_exercise(doc, 14, None, body_size, font_name=body_font)

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
        '(removing it yields *She put the book — ungrammatical). But in "She read the book on the table," '
        '"on the table" is an adverbial (removing it yields She read the book — fine). '
        'The first sentence requires a locative argument; the second does not.'
    )
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=0, space_after=2)

    doc.save(str(output_path))
    print(f'Created: {output_path}')


def main():
    script_dir = Path(__file__).parent
    homework_dir = script_dir.parent / 'Homework'

    create_answer_key(
        homework_dir / 'Chapter 08 Answer Key.docx',
        font_size=12
    )

    create_answer_key(
        homework_dir / 'Homework 08 Overhead.docx',
        overhead=True
    )


if __name__ == '__main__':
    main()
