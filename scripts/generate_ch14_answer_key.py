#!/usr/bin/env python3
"""
Generate Chapter 14 homework files: Student Homework, Answer Key, and Overhead.
"""

from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches

from answer_key_helpers import (
    set_paragraph_spacing, add_spacer_row, add_exercise, add_answer_line,
    add_plain_line, setup_document, add_title_page, add_part_heading,
    exercise_separator, get_font_config, add_bracket_line, add_diagram_image,
    add_multilevel_from_bracket, load_chapter_roles,
    parse_bracket_to_multilevel, add_multilevel_labeling_table,
    question_page_break, answer_page_break,
)


DIAGRAM_DIR = Path(__file__).parent.parent / 'Homework' / 'diagrams' / 'ch14'


DIAGRAM_EXERCISES = [
    {
        'num': 18, 'sentence': 'What she said surprised everyone.',
        'words':   ['What', 'she', 'said', 'surprised', 'everyone'],
        'roles':   ['Subj', '', '', 'Pred', 'DO'],
        'phrases': ['NOM', 'NP', 'VP', 'VP', 'NP'],
        'pos':     ['PRON', 'PRON', 'V', 'V', 'PRON'],
        'bracket': '[S [NOM [PRON What] [NP [PRON she]] [VP [V said]]] [VP [V surprised] [NP [PRON everyone]]]]',
        'diagram': 'ch14_hw_ex18_what_said',
    },
    {
        'num': 19, 'sentence': 'He enjoys swimming in the lake.',
        'words':   ['He', 'enjoys', 'swimming', 'in', 'the', 'lake'],
        'roles':   ['Subj', 'Pred', 'DO', '', '', ''],
        'phrases': ['NP', 'VP', 'NOM', 'PP', 'NP', ''],
        'pos':     ['PRON', 'V', 'V', 'PREP', 'DET', 'N'],
        'bracket': '[S [NP [PRON He]] [VP [V enjoys] [NOM [V swimming] [PP [PREP in] [NP [DET the] [N lake]]]]]]',
        'diagram': 'ch14_hw_ex19_enjoys_swimming',
    },
    {
        'num': 20, 'sentence': 'To win the race was her only goal.',
        'words':   ['To', 'win', 'the', 'race', 'was', 'her', 'only', 'goal'],
        'roles':   ['Subj', '', '', '', 'Pred', 'SC', '', ''],
        'phrases': ['NOM', 'VP', 'NP', '', 'VP', 'NP', '', ''],
        'pos':     ['PART', 'V', 'DET', 'N', 'V', 'DET', 'ADJ', 'N'],
        'bracket': '[S [NOM [PART To] [VP [V win] [NP [DET the] [N race]]]] [VP [V was] [NP [DET her] [ADJP [ADJ only]] [N goal]]]]',
        'diagram': 'ch14_hw_ex20_to_win',
    },
    {
        'num': 21, 'sentence': 'The fact that he lied angered them.',
        'words':   ['The', 'fact', 'that', 'he', 'lied', 'angered', 'them'],
        'roles':   ['Subj', '', '', '', '', 'Pred', 'DO'],
        'phrases': ['NP', '', 'SBAR', 'NP', 'VP', 'VP', 'NP'],
        'pos':     ['DET', 'N', 'COMP', 'PRON', 'V', 'V', 'PRON'],
        'bracket': '[S [NP [DET The] [N fact] [SBAR [COMP that] [S [NP [PRON he]] [VP [V lied]]]]] [VP [V angered] [NP [PRON them]]]]',
        'diagram': 'ch14_hw_ex21_fact_lied',
    },
    {
        'num': 22, 'sentence': 'She asked whether we could help.',
        'words':   ['She', 'asked', 'whether', 'we', 'could', 'help'],
        'roles':   ['Subj', 'Pred', 'DO', '', '', ''],
        'phrases': ['NP', 'VP', 'SBAR', 'NP', 'VP', ''],
        'pos':     ['PRON', 'V', 'COMP', 'PRON', 'MOD', 'V'],
        'bracket': '[S [NP [PRON She]] [VP [V asked] [SBAR [COMP whether] [S [NP [PRON we]] [VP [MOD could] [V help]]]]]]',
        'diagram': 'ch14_hw_ex22_asked_whether',
    },
]


def create_answer_key(output_path, font_size=12, overhead=False):
    """Create the Chapter 14 Answer Key document."""
    doc = Document()
    cfg = setup_document(doc, overhead)
    body_font = cfg['body_font']
    body_size = cfg['body_size']

    add_title_page(doc, 'Chapter 14: Nominals', cfg, overhead)

    # =============================================
    # Part 1: Identification and Classification
    # =============================================
    add_part_heading(doc, 'Part 1: Identification and Classification', cfg, overhead)

    # Exercise 1
    add_exercise(doc, 1, 'I don\u2019t know whether she received my message.', body_size, font_name=body_font)
    answer_page_break(doc, overhead)
    add_answer_line(doc, 'Form:', 'wh-clause (whether-clause)', body_size, font_name=body_font)
    add_answer_line(doc, 'Function:', 'direct object (of "know")', body_size, font_name=body_font)

    # Exercise 2
    question_page_break(doc, overhead)
    add_exercise(doc, 2, 'The problem is that we lack sufficient funding.', body_size, font_name=body_font)
    answer_page_break(doc, overhead)
    add_answer_line(doc, 'Form:', 'that-clause', body_size, font_name=body_font)
    add_answer_line(doc, 'Function:', 'subject complement', body_size, font_name=body_font)

    # Exercise 3
    question_page_break(doc, overhead)
    add_exercise(doc, 3, 'To learn a new language requires dedication and practice.', body_size, font_name=body_font)
    answer_page_break(doc, overhead)
    add_answer_line(doc, 'Form:', 'infinitive phrase', body_size, font_name=body_font)
    add_answer_line(doc, 'Function:', 'subject', body_size, font_name=body_font)

    # Exercise 4
    question_page_break(doc, overhead)
    add_exercise(doc, 4, 'What the scientist discovered changed the field of biology.', body_size, font_name=body_font)
    answer_page_break(doc, overhead)
    add_answer_line(doc, 'Form:', 'wh-clause', body_size, font_name=body_font)
    add_answer_line(doc, 'Function:', 'subject', body_size, font_name=body_font)

    # Exercise 5
    question_page_break(doc, overhead)
    add_exercise(doc, 5, 'She enjoys reading mystery novels on rainy afternoons.', body_size, font_name=body_font)
    answer_page_break(doc, overhead)
    add_answer_line(doc, 'Form:', 'gerund phrase', body_size, font_name=body_font)
    add_answer_line(doc, 'Function:', 'direct object (of "enjoys")', body_size, font_name=body_font)

    # Exercise 6
    question_page_break(doc, overhead)
    add_exercise(doc, 6, 'He asked who would be attending the conference.', body_size, font_name=body_font)
    answer_page_break(doc, overhead)
    add_answer_line(doc, 'Form:', 'wh-clause', body_size, font_name=body_font)
    add_answer_line(doc, 'Function:', 'direct object (of "asked")', body_size, font_name=body_font)

    # Exercise 7
    question_page_break(doc, overhead)
    add_exercise(doc, 7, 'Her greatest fear is making a mistake in public.', body_size, font_name=body_font)
    answer_page_break(doc, overhead)
    add_answer_line(doc, 'Form:', 'gerund phrase', body_size, font_name=body_font)
    add_answer_line(doc, 'Function:', 'subject complement', body_size, font_name=body_font)

    # =============================================
    # Part 2: Functional Analysis
    # =============================================
    add_part_heading(doc, 'Part 2: Functional Analysis', cfg, overhead)

    functions = [
        (8, 'That the project failed disappointed everyone.',
         'subject',
         'The that-clause is the subject of "disappointed."'),
        (9, 'The committee discussed how they would proceed.',
         'direct object',
         'The wh-clause is the direct object of "discussed."'),
        (10, 'She\u2019s interested in learning more about linguistics.',
         'object of preposition',
         'The gerund phrase is the object of the preposition "in."'),
        (11, 'The main issue is whether we should continue.',
         'subject complement',
         'The wh-clause follows the linking verb "is" and renames "the main issue."'),
        (12, 'I appreciate your helping us with the move.',
         'direct object',
         'The gerund phrase (with possessive) is the direct object of "appreciate."'),
    ]

    for i, (num, sentence, function, explanation) in enumerate(functions):
        if i > 0:
            question_page_break(doc, overhead)
        add_exercise(doc, num, sentence, body_size, font_name=body_font)
        answer_page_break(doc, overhead)
        add_answer_line(doc, 'Function:', function, body_size, font_name=body_font)
        add_plain_line(doc, explanation, body_size, font_name=body_font)

    # =============================================
    # Part 3: Sentence Completion
    # =============================================
    add_part_heading(doc, 'Part 3: Sentence Completion', cfg, overhead)

    p = doc.add_paragraph()
    run = p.add_run('Exercises 13\u201317 are open-ended. Accept any grammatically correct nominal of the requested type.')
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=6)

    completions = [
        (13, 'Gerund phrase as subject: __________ can be challenging for new employees.',
         '"Learning new software can be challenging for new employees."'),
        (14, 'Wh-clause as direct object: The detective investigated __________.',
         '"The detective investigated who had access to the building."'),
        (15, 'Infinitive phrase as subject complement: Her goal this year is __________.',
         '"Her goal this year is to complete her dissertation."'),
        (16, 'That-clause as subject: __________ surprised everyone at the meeting.',
         '"That the CEO resigned surprised everyone at the meeting."'),
        (17, 'Gerund phrase as object of preposition: She succeeded by __________.',
         '"She succeeded by studying consistently throughout the semester."'),
    ]

    for i, (num, prompt, sample) in enumerate(completions):
        if i > 0:
            question_page_break(doc, overhead)
        add_exercise(doc, num, prompt, body_size, font_name=body_font)
        answer_page_break(doc, overhead)
        add_plain_line(doc, f'Sample: {sample}', body_size, font_name=body_font)

    # =============================================
    # Part 4: Diagramming Nominals
    # =============================================
    add_part_heading(doc, 'Part 4: Diagramming Nominals', cfg, overhead)

    ch_roles = load_chapter_roles(14)
    mode = 'overhead' if overhead else 'answer_key'

    for i, ex in enumerate(DIAGRAM_EXERCISES):
        if i > 0:
            question_page_break(doc, overhead)
        add_exercise(doc, ex['num'], ex['sentence'], body_size, font_name=body_font)
        answer_page_break(doc, overhead)
        bracket_key = ' '.join(ex['bracket'].split())
        add_multilevel_from_bracket(doc, ex['bracket'], roles_dict=ch_roles.get(bracket_key), mode=mode, font_size=body_size)
        add_bracket_line(doc, ex['bracket'], body_size, font_name=body_font)
        add_diagram_image(doc, DIAGRAM_DIR, ex['diagram'], width_inches=cfg['diagram_width'])

    # =============================================
    # Part 5: Analysis and Application
    # =============================================
    add_part_heading(doc, 'Part 5: Analysis and Application', cfg, overhead)

    # Exercise 23
    add_exercise(doc, 23, 'Explain the grammatical and meaning differences between these pairs.', body_size, font_name=body_font)
    add_plain_line(doc, '23A) "She stopped smoking." vs. 23B) "She stopped to smoke."', body_size, font_name=body_font)
    answer_page_break(doc, overhead)

    add_plain_line(doc,
        'Grammatical difference: In (a), "smoking" is a gerund \u2014 it functions as '
        'the direct object of "stopped." In (b), "to smoke" is an infinitive phrase \u2014 '
        'it functions as an adverbial of purpose.',
        body_size, font_name=body_font)
    add_plain_line(doc,
        'Meaning difference: (a) means she quit the habit of smoking. '
        '(b) means she paused what she was doing in order to have a smoke.',
        body_size, font_name=body_font)

    # Exercise 24
    question_page_break(doc, overhead)
    add_exercise(doc, 24, 'Explain the grammatical and meaning differences between these pairs.', body_size, font_name=body_font)
    add_plain_line(doc, '24A) "I remember locking the door." vs. 24B) "I remember to lock the door."', body_size, font_name=body_font)
    answer_page_break(doc, overhead)

    add_plain_line(doc,
        '(a) The gerund "locking" refers to a past event \u2014 I have a memory of '
        'having locked the door (I recall doing it).',
        body_size, font_name=body_font)
    add_plain_line(doc,
        '(b) The infinitive "to lock" refers to a future/habitual obligation \u2014 '
        'I don\u2019t forget to lock the door (I remember that I need to do it).',
        body_size, font_name=body_font)

    # Exercise 25
    question_page_break(doc, overhead)
    add_exercise(doc, 25, 'Transform "The experiment succeeded" into four nominal structures.', body_size, font_name=body_font)
    answer_page_break(doc, overhead)

    transforms = [
        ('25A) That-clause as subject:',
         '"That the experiment succeeded pleased the researchers."'),
        ('25B) Gerund phrase as subject:',
         '"The experiment\u2019s succeeding pleased the researchers." '
         'OR "The experiment succeeding pleased the researchers."'),
        ('25C) Wh-clause as direct object:',
         '"They wondered whether the experiment had succeeded."'),
        ('25D) Infinitive after "seem":',
         '"The experiment seemed to succeed." OR "The experiment seemed to have succeeded."'),
    ]

    for label, sample in transforms:
        add_plain_line(doc, label, body_size, indent=0.35, font_name=body_font)
        add_plain_line(doc, f'Sample: {sample}', body_size, indent=0.7, font_name=body_font)

    # Exercise 26
    question_page_break(doc, overhead)
    add_exercise(doc, 26, 'Answer the following questions about extraposition.', body_size, font_name=body_font)
    answer_page_break(doc, overhead)
    add_plain_line(doc,
        '26A) Extraposition moves a clausal subject to the end of the sentence, '
        'replacing it with the placeholder pronoun "it" in subject position. '
        'Example: "That she resigned surprised everyone" \u2192 '
        '"It surprised everyone that she resigned."',
        body_size, font_name=body_font)
    add_plain_line(doc,
        '26B) A writer might prefer the extraposed version when the clausal subject '
        'is long or complex, as it follows the end-weight principle \u2014 '
        'placing heavier elements at the end for easier processing. '
        'It also sounds more natural in conversation.',
        body_size, font_name=body_font)
    add_plain_line(doc,
        '26C) A writer might prefer the non-extraposed version to give the clause '
        'more prominence or emphasis (topic position), or when the clause is '
        'relatively short and doesn\u2019t create processing difficulty.',
        body_size, font_name=body_font)

    doc.save(str(output_path))
    print(f"Created: {output_path}")


def create_student_homework(output_path):
    """Create the Chapter 14 Student Homework with blank multi-level tables."""
    doc = Document()

    # Basic styling — Garamond 12pt, landscape
    style = doc.styles['Normal']
    style.font.name = 'Garamond'
    style.font.size = Pt(12)
    fs = 12

    section = doc.sections[0]
    section.page_width = Inches(11)
    section.page_height = Inches(8.5)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)

    # Title
    p = doc.add_paragraph()
    run = p.add_run('Chapter 14 Homework: Nominals')
    run.bold = True
    run.font.size = Pt(16)
    run.font.name = 'Garamond'
    set_paragraph_spacing(p, space_before=0, space_after=4)

    # --- Part 4: Diagramming Nominals ---
    p = doc.add_paragraph()
    set_paragraph_spacing(p, space_before=10, space_after=4)
    run = p.add_run('Part 4: Diagramming Nominals')
    run.bold = True
    run.font.size = Pt(14)
    run.font.name = 'Garamond'

    p = doc.add_paragraph()
    run = p.add_run('Instructions: ')
    run.bold = True
    run.font.size = Pt(fs)
    run.font.name = 'Garamond'
    run = p.add_run('For each sentence, complete the labeling table and write the bracket notation.')
    run.font.size = Pt(fs)
    run.font.name = 'Garamond'

    for ex in DIAGRAM_EXERCISES:
        p = doc.add_paragraph()
        set_paragraph_spacing(p, space_before=8, space_after=2)
        run = p.add_run(f'Exercise {ex["num"]}. ')
        run.bold = True
        run.font.size = Pt(fs)
        run.font.name = 'Garamond'
        run = p.add_run(ex['sentence'])
        run.italic = True
        run.font.size = Pt(fs)
        run.font.name = 'Garamond'

        table_data = parse_bracket_to_multilevel(ex['bracket'])
        add_multilevel_labeling_table(doc, table_data, mode='student', font_size=10)

        p = doc.add_paragraph()
        run = p.add_run('Bracket notation: _____')
        run.font.size = Pt(fs)
        run.font.name = 'Garamond'

    doc.save(str(output_path))
    print(f"Created: {output_path}")


def main():
    script_dir = Path(__file__).parent
    homework_dir = script_dir.parent / 'Homework'

    create_student_homework(
        homework_dir / 'Student' / 'Chapter 14 Homework.docx'
    )

    create_answer_key(
        homework_dir / 'Answer Keys' / 'Chapter 14 Answer Key.docx',
        font_size=12
    )

    create_answer_key(
        homework_dir / 'Overheads' / 'Homework 14 Overhead.docx',
        overhead=True
    )


if __name__ == '__main__':
    main()
