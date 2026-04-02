#!/usr/bin/env python3
"""
Generate Chapter 13 Answer Key and Overhead Answer Key .docx files.
"""

from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches

from answer_key_helpers import (
    set_paragraph_spacing, add_spacer_row, add_exercise, add_answer_line,
    add_plain_line, setup_document, add_title_page, add_part_heading,
    get_font_config, add_bracket_line, blank_labels, add_diagram_image,
    add_multilevel_from_bracket, load_chapter_roles,
    parse_bracket_to_multilevel, add_multilevel_labeling_table,
    question_page_break, answer_page_break,
)


DIAGRAM_DIR = Path(__file__).parent.parent / 'Homework' / 'diagrams' / 'ch13'


DIAGRAM_EXERCISES = [
    {
        'num': 16, 'sentence': 'The student who won the award celebrated.',
        'words':   ['The', 'student', 'who', 'won', 'the', 'award', 'celebrated'],
        'roles':   ['Subj', '', '', '', '', '', 'Pred'],
        'phrases': ['NP', '', 'RC', 'VP', 'NP', '', 'VP'],
        'pos':     ['DET', 'N', 'REL', 'V', 'DET', 'N', 'V'],
        'bracket': '[S [NP [DET The] [N student] [RC [REL who] [VP [V won] [NP [DET the] [N award]]]]] [VP [V celebrated]]]',
        'diagram': 'ch13_hw_ex16_student_award',
    },
    {
        'num': 17, 'sentence': 'The extremely tall building collapsed.',
        'words':   ['The', 'extremely', 'tall', 'building', 'collapsed'],
        'roles':   ['Subj', '', '', '', 'Pred'],
        'phrases': ['NP', 'ADJP', '', '', 'VP'],
        'pos':     ['DET', 'ADV', 'ADJ', 'N', 'V'],
        'bracket': '[S [NP [DET The] [ADJP [ADV extremely] [ADJ tall]] [N building]] [VP [V collapsed]]]',
        'diagram': 'ch13_hw_ex17_tall_building',
    },
    {
        'num': 18, 'sentence': 'The book on the table is mine.',
        'words':   ['The', 'book', 'on', 'the', 'table', 'is', 'mine'],
        'roles':   ['Subj', '', '', '', '', 'Pred', 'SC'],
        'phrases': ['NP', '', 'PP', 'NP', '', 'VP', 'NP'],
        'pos':     ['DET', 'N', 'PREP', 'DET', 'N', 'V', 'PRON'],
        'bracket': '[S [NP [DET The] [N book] [PP [PREP on] [NP [DET the] [N table]]]] [VP [V is] [NP [PRON mine]]]]',
        'diagram': 'ch13_hw_ex18_book_table',
    },
    {
        'num': 19, 'sentence': 'Running water flowed through the pipe.',
        'words':   ['Running', 'water', 'flowed', 'through', 'the', 'pipe'],
        'roles':   ['Subj', '', 'Pred', '', '', ''],
        'phrases': ['NP', '', 'VP', 'PP', 'NP', ''],
        'pos':     ['V', 'N', 'V', 'PREP', 'DET', 'N'],
        'bracket': '[S [NP [V Running] [N water]] [VP [V flowed] [PP [PREP through] [NP [DET the] [N pipe]]]]]',
        'diagram': 'ch13_hw_ex19_running_water',
    },
    {
        'num': 20, 'sentence': 'The woman wearing the red coat smiled.',
        'words':   ['The', 'woman', 'wearing', 'the', 'red', 'coat', 'smiled'],
        'roles':   ['Subj', '', '', '', '', '', 'Pred'],
        'phrases': ['NP', '', 'VP', 'NP', '', '', 'VP'],
        'pos':     ['DET', 'N', 'V', 'DET', 'ADJ', 'N', 'V'],
        'bracket': '[S [NP [DET The] [N woman] [VP [V wearing] [NP [DET the] [ADJP [ADJ red]] [N coat]]]] [VP [V smiled]]]',
        'diagram': 'ch13_hw_ex20_woman_coat',
    },
]


def create_answer_key(output_path, font_size=12, overhead=False):
    """Create the Chapter 13 Answer Key document."""
    doc = Document()
    cfg = setup_document(doc, overhead)
    body_font = cfg['body_font']
    body_size = cfg['body_size']

    add_title_page(doc, 'Chapter 13: Adjectivals', cfg, overhead)

    # =============================================
    # Part 1: Identification and Classification
    # =============================================
    add_part_heading(doc, 'Part 1: Identification and Classification', cfg, overhead)

    # Exercise 1
    add_exercise(doc, 1, 'The book on the top shelf belongs to my professor.', body_size, font_name=body_font)
    answer_page_break(doc, overhead)
    add_answer_line(doc, 'Form:', 'prepositional phrase', body_size, font_name=body_font)
    add_plain_line(doc, 'Modifies "book" \u2014 tells which book', body_size, font_name=body_font)

    question_page_break(doc, overhead)

    # Exercise 2
    add_exercise(doc, 2, 'The woman who won the award gave an inspiring speech.', body_size, font_name=body_font)
    answer_page_break(doc, overhead)
    add_answer_line(doc, 'Form:', 'relative clause', body_size, font_name=body_font)
    add_plain_line(doc, 'Modifies "woman" \u2014 identifies which woman', body_size, font_name=body_font)

    question_page_break(doc, overhead)

    # Exercise 3
    add_exercise(doc, 3, 'The broken window needs to be repaired immediately.', body_size, font_name=body_font)
    answer_page_break(doc, overhead)
    add_answer_line(doc, 'Form:', 'past participle (single-word adjectival)', body_size, font_name=body_font)
    add_plain_line(doc, 'Modifies "window" \u2014 describes the window\u2019s state', body_size, font_name=body_font)

    question_page_break(doc, overhead)

    # Exercise 4
    add_exercise(doc, 4, 'I need something to eat before the meeting.', body_size, font_name=body_font)
    answer_page_break(doc, overhead)
    add_answer_line(doc, 'Form:', 'infinitive phrase', body_size, font_name=body_font)
    add_plain_line(doc, 'Modifies "something" \u2014 specifies what kind of something', body_size, font_name=body_font)

    question_page_break(doc, overhead)

    # Exercise 5
    add_exercise(doc, 5, 'The government report was released yesterday.', body_size, font_name=body_font)
    answer_page_break(doc, overhead)
    add_answer_line(doc, 'Form:', 'noun (used as adjectival)', body_size, font_name=body_font)
    add_plain_line(doc, 'Modifies "report" \u2014 classifies the type of report', body_size, font_name=body_font)

    question_page_break(doc, overhead)

    # Exercise 6
    add_exercise(doc, 6, 'The students waiting in line seemed impatient.', body_size, font_name=body_font)
    answer_page_break(doc, overhead)
    add_answer_line(doc, 'Form:', 'present participial phrase', body_size, font_name=body_font)
    add_plain_line(doc, 'Modifies "students" \u2014 identifies which students', body_size, font_name=body_font)

    question_page_break(doc, overhead)

    # Exercise 7
    add_exercise(doc, 7, 'We found a very comfortable chair at the antique store.', body_size, font_name=body_font)
    answer_page_break(doc, overhead)
    add_answer_line(doc, 'Form:', 'adjective phrase', body_size, font_name=body_font)
    add_plain_line(doc, 'Modifies "chair" \u2014 describes the chair', body_size, font_name=body_font)

    # =============================================
    # Part 2: Restrictive vs. Non-Restrictive
    # =============================================
    add_part_heading(doc, 'Part 2: Restrictive vs. Non-Restrictive', cfg, overhead)

    classifications = [
        (8, 'The students who completed the extra assignment received bonus points.',
         'Restrictive (R)',
         'No commas set off the clause. It identifies which students received bonus points \u2014 '
         'only those who completed the extra assignment, not all students.'),
        (9, 'The Eiffel Tower, which was built in 1889, attracts millions of visitors.',
         'Non-restrictive (NR)',
         'Commas set off the clause. The Eiffel Tower is already uniquely identified; '
         'the clause adds supplementary information about when it was built.'),
        (10, 'The car that I bought last year already needs repairs.',
         'Restrictive (R)',
         'No commas; "that" is used (typical of restrictive clauses). '
         'The clause identifies which car \u2014 specifically the one bought last year.'),
        (11, 'My neighbor\u2019s dog, a golden retriever, barks every morning.',
         'Non-restrictive (NR)',
         'Commas set off the appositive. The dog is already identified as "my neighbor\u2019s dog"; '
         '"a golden retriever" adds extra descriptive information.'),
    ]

    for i, (num, sentence, classification, explanation) in enumerate(classifications):
        if i > 0:
            question_page_break(doc, overhead)
        add_exercise(doc, num, sentence, body_size, font_name=body_font)
        answer_page_break(doc, overhead)
        add_answer_line(doc, 'Type:', classification, body_size, font_name=body_font)
        add_plain_line(doc, explanation, body_size, font_name=body_font)

    # =============================================
    # Part 3: Sentence Combining
    # =============================================
    add_part_heading(doc, 'Part 3: Sentence Combining', cfg, overhead)

    p = doc.add_paragraph()
    run = p.add_run('Exercises 12\u201315 are open-ended. Accept any grammatically correct combination using the requested structure.')
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=6)

    combinations = [
        (12, 'Relative clause: This is the book. I told you about it.',
         '"This is the book that I told you about."'),
        (13, 'Relative clause: The scientist won a Nobel Prize. Her research changed medicine.',
         '"The scientist whose research changed medicine won a Nobel Prize."'),
        (14, 'Participial phrase: The students were exhausted from the exam. They went home early.',
         '"Exhausted from the exam, the students went home early."'),
        (15, 'Participial phrase: The letter was written in 1945. The letter was found in the attic.',
         '"Written in 1945, the letter was found in the attic." '
         'OR "The letter, written in 1945, was found in the attic."'),
    ]

    for i, (num, prompt, sample) in enumerate(combinations):
        if i > 0:
            question_page_break(doc, overhead)
        add_exercise(doc, num, f'Combine using the specified structure: {prompt}', body_size, font_name=body_font)
        add_plain_line(doc, prompt, body_size, bold_prefix='Prompt: ', font_name=body_font)
        answer_page_break(doc, overhead)
        add_plain_line(doc, f'Sample: {sample}', body_size, font_name=body_font)

    # =============================================
    # Part 4: Diagramming Adjectivals
    # =============================================
    add_part_heading(doc, 'Part 4: Diagramming Adjectivals', cfg, overhead)

    ch_roles = load_chapter_roles(13)
    mode = 'overhead' if overhead else 'answer_key'
    for i, ex in enumerate(DIAGRAM_EXERCISES):
        if i > 0:
            question_page_break(doc, overhead)
        add_exercise(doc, ex['num'], ex['sentence'], body_size, font_name=body_font)
        answer_page_break(doc, overhead)
        bracket_key = ' '.join(ex['bracket'].split())
        add_multilevel_from_bracket(doc, ex['bracket'],
                                     roles_dict=ch_roles.get(bracket_key),
                                     mode=mode, font_size=body_size)
        add_bracket_line(doc, ex['bracket'], body_size, font_name=body_font)
        add_diagram_image(doc, DIAGRAM_DIR, ex['diagram'], width_inches=cfg['diagram_width'])

    # =============================================
    # Part 5: Error Correction and Analysis
    # =============================================
    add_part_heading(doc, 'Part 5: Error Correction and Analysis', cfg, overhead)

    # Exercise 21: Dangling Participle Correction
    add_exercise(doc, 21, 'Correct each dangling participle:', body_size, font_name=body_font)

    danglers = [
        ('21A)', 'Walking through the park, the flowers were beautiful.',
         '"Walking through the park, I thought the flowers were beautiful." '
         'OR "As I walked through the park, the flowers were beautiful."',
         'The original implies the flowers were walking.'),
        ('21B)', 'Having finished the report, the computer was shut down.',
         '"Having finished the report, she shut down the computer."',
         'The original implies the computer finished the report.'),
        ('21C)', 'Exhausted from the journey, the bed looked inviting.',
         '"Exhausted from the journey, I thought the bed looked inviting."',
         'The original implies the bed was exhausted.'),
    ]

    answer_page_break(doc, overhead)
    for label, original, corrected, explanation in danglers:
        add_plain_line(doc, f'{label} {original}', body_size, indent=0.35, font_name=body_font)
        add_plain_line(doc, f'Corrected: {corrected}', body_size, indent=0.7, font_name=body_font)
        add_plain_line(doc, f'Explanation: {explanation}', body_size, indent=0.7, font_name=body_font)

    question_page_break(doc, overhead)

    # Exercise 22: Meaning Analysis
    add_exercise(doc, 22, 'Explain the meaning difference between restrictive and non-restrictive versions:', body_size, font_name=body_font)
    answer_page_break(doc, overhead)
    add_plain_line(doc,
        '22A) "My brother who lives in Chicago is a doctor."',
        body_size, font_name=body_font)
    add_plain_line(doc,
        'Restrictive: implies the speaker has more than one brother. The clause '
        'identifies which brother \u2014 the one in Chicago (as opposed to brothers elsewhere).',
        body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc,
        '22B) "My brother, who lives in Chicago, is a doctor."',
        body_size, font_name=body_font)
    add_plain_line(doc,
        'Non-restrictive: implies the speaker has only one brother. The clause '
        'adds supplementary information about where he lives; it doesn\u2019t serve '
        'to distinguish him from other brothers.',
        body_size, indent=0.7, font_name=body_font)

    question_page_break(doc, overhead)

    # Exercise 23: Multiple Adjectivals
    add_exercise(doc, 23, 'Identify and analyze the adjectivals in the noun phrase:', body_size, font_name=body_font)
    add_plain_line(doc,
        'The talented young American jazz musician from New Orleans who won the competition',
        body_size, font_name=body_font)

    answer_page_break(doc, overhead)
    add_plain_line(doc, '23A) Adjectivals identified:', body_size, font_name=body_font)

    adjectivals = [
        ('"talented"', 'adjective (pre-modifier, opinion)'),
        ('"young"', 'adjective (pre-modifier, age)'),
        ('"American"', 'adjective (pre-modifier, origin)'),
        ('"jazz"', 'noun as adjectival (pre-modifier, purpose/type)'),
        ('"from New Orleans"', 'prepositional phrase (post-modifier)'),
        ('"who won the competition"', 'relative clause (post-modifier)'),
    ]

    for word, form in adjectivals:
        add_plain_line(doc, f'{word} \u2014 {form}', body_size, indent=0.7, font_name=body_font)

    add_plain_line(doc,
        '23B) Pre-modifiers follow this typical order: determiner \u2192 opinion \u2192 size \u2192 '
        'age \u2192 shape \u2192 color \u2192 origin \u2192 material \u2192 purpose \u2192 NOUN. '
        'In this example: opinion (talented) \u2192 age (young) \u2192 origin (American) \u2192 '
        'type (jazz) \u2192 NOUN (musician).',
        body_size, font_name=body_font)

    add_plain_line(doc,
        '23C) Post-modifiers follow the noun because they are longer, more complex structures '
        '(phrases and clauses) that would be unwieldy before the noun. English places shorter, '
        'simpler modifiers before the noun and longer, more complex ones after it. '
        'PPs and relative clauses are too heavy for pre-nominal position.',
        body_size, font_name=body_font)

    doc.save(str(output_path))
    print(f"Created: {output_path}")


def create_student_homework(output_path):
    """Create the Chapter 13 Student Homework with blank multi-level tables."""
    from answer_key_helpers import parse_bracket_to_multilevel, add_multilevel_labeling_table
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Garamond'
    style.font.size = Pt(12)
    fs = 12

    # Set landscape
    section = doc.sections[0]
    section.page_width, section.page_height = section.page_height, section.page_width
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

    p = doc.add_paragraph()
    run = p.add_run('Chapter 13 Homework: Adjectivals')
    run.bold = True
    run.font.size = Pt(16)
    run.font.name = 'Garamond'
    set_paragraph_spacing(p, space_before=0, space_after=4)

    # Part 4 with blank multi-level tables
    p = doc.add_paragraph()
    set_paragraph_spacing(p, space_before=10, space_after=4)
    run = p.add_run('Part 4: Diagramming Adjectivals')
    run.bold = True
    run.font.size = Pt(14)
    run.font.name = 'Garamond'

    for ex in DIAGRAM_EXERCISES:
        p = doc.add_paragraph()
        set_paragraph_spacing(p, space_before=6, space_after=2)
        run = p.add_run(f'Exercise {ex["num"]}. ')
        run.bold = True
        run.font.size = Pt(fs)
        run.font.name = 'Garamond'
        run = p.add_run(ex['sentence'])
        run.italic = True
        run.font.size = Pt(fs)
        run.font.name = 'Garamond'

        td = parse_bracket_to_multilevel(ex['bracket'])
        add_multilevel_labeling_table(doc, td, mode='student', font_size=fs)

        p = doc.add_paragraph()
        run = p.add_run('Bracket notation: _____')
        run.font.size = Pt(fs)
        run.font.name = 'Garamond'

    doc.save(str(output_path))
    print(f'Created: {output_path}')


def main():
    script_dir = Path(__file__).parent
    homework_dir = script_dir.parent / 'Homework'

    create_student_homework(
        homework_dir / 'Student' / 'Chapter 13 Homework.docx'
    )

    create_answer_key(
        homework_dir / 'Answer Keys' / 'Chapter 13 Answer Key.docx',
        font_size=12
    )

    create_answer_key(
        homework_dir / 'Overheads' / 'Homework 13 Overhead.docx',
        overhead=True
    )


if __name__ == '__main__':
    main()
