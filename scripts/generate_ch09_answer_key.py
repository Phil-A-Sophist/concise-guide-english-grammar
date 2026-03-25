#!/usr/bin/env python3
"""
Generate Chapter 9 Answer Key and Overhead Answer Key .docx files.
Updated to match revised homework structure: Conjunctions and Clauses (5 parts, 14 exercises).
"""

from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches
from answer_key_helpers import (
    set_paragraph_spacing, add_spacer_row, add_exercise, add_answer_line,
    add_plain_line, add_sub_sentence, setup_document, add_title_page,
    add_part_heading, exercise_separator, get_font_config,
    add_labeling_table, add_bracket_line, blank_labels,
)


DIAGRAM_EXERCISES = [
    {
        'sub': 'a)',
        'sentence': 'Marcus and Elena traveled.',
        'words':   ['Marcus', 'and', 'Elena', 'traveled'],
        'roles':   ['Subj',   '',    '',       'Pred'],
        'phrases': ['NP',     'CONJ','',        'VP'],
        'pos':     ['N',      'CONJ','N',       'V'],
        'bracket': '[S [NP [N Marcus] [CONJ and] [N Elena]] [VP [V traveled]]]',
    },
    {
        'sub': 'b)',
        'sentence': 'The dog barked and chased the squirrel.',
        'words':   ['The',  'dog', 'barked', 'and',  'chased', 'the',  'squirrel'],
        'roles':   ['Subj', '',    'Pred',   '',     '',       '',     ''],
        'phrases': ['NP',   '',    'VP',     'CONJ', 'VP',     'NP',   ''],
        'pos':     ['DET',  'N',   'V',      'CONJ', 'V',      'DET',  'N'],
        'bracket': '[S [NP [DET The] [N dog]] [VP [V barked] [CONJ and] [VP [V chased] [NP [DET the] [N squirrel]]]]]',
    },
    {
        'sub': 'c)',
        'sentence': 'She writes poetry, and he composes music.',
        'words':   ['She',   'writes', 'poetry', 'and',  'he',   'composes', 'music'],
        'roles':   ['IC',    '',       '',       '',     'IC',   '',         ''],
        'phrases': ['NP',    'VP',     'NP',     'CC',   'NP',   'VP',       'NP'],
        'pos':     ['PRON',  'V',      'N',      'CONJ', 'PRON', 'V',        'N'],
        'bracket': '[S [IC [NP [PRON She]] [VP [V writes] [NP [N poetry]]]] [CC [CONJ and]] [IC [NP [PRON he]] [VP [V composes] [NP [N music]]]]]',
    },
    {
        'sub': 'd)',
        'sentence': 'When it rained, we stayed inside.',
        'words':   ['When', 'it',   'rained', 'we',   'stayed', 'inside'],
        'roles':   ['DC',   '',     '',       'IC',   '',       ''],
        'phrases': ['COMP', 'NP',   'VP',     'NP',   'VP',     'ADVP'],
        'pos':     ['COMP', 'PRON', 'V',      'PRON', 'V',      'ADV'],
        'bracket': '[S [DC [COMP When] [NP [PRON it]] [VP [V rained]]] [IC [NP [PRON we]] [VP [V stayed] [ADVP [ADV inside]]]]]',
    },
]


def create_answer_key(output_path, font_size=12, overhead=False):
    doc = Document()
    cfg = setup_document(doc, overhead)
    body_font = cfg['body_font']
    body_size = cfg['body_size']

    add_title_page(doc, 'Chapter 9: Conjunctions and Clauses', cfg, overhead)

    # =============================================
    # Part 1: Sentence Type Identification
    # =============================================
    add_part_heading(doc, 'Part 1: Sentence Type Identification', cfg, overhead)

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

    exercise_separator(doc, overhead)

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

    exercise_separator(doc, overhead)

    # Exercise 3
    add_exercise(doc, 3,
        'The exhausted marathon runner from Kenya and her experienced coach celebrated after the race.',
        body_size, font_name=body_font)

    add_answer_line(doc, 'Sentence type:', 'Simple', body_size, font_name=body_font)
    add_plain_line(doc,
        'One independent clause with a compound NP subject ("The exhausted marathon runner from Kenya" + '
        '"her experienced coach"). "After the race" is a prepositional phrase, not a dependent clause '
        '(no subject-verb pair). The compound NP keeps both names as NPs inside a larger NP \u2014 '
        'not two separate clauses.',
        body_size, indent=0.7, font_name=body_font)

    exercise_separator(doc, overhead)

    # =============================================
    # Part 2: Sentence Writing
    # =============================================
    add_part_heading(doc, 'Part 2: Sentence Writing', cfg, overhead)

    p = doc.add_paragraph()
    run = p.add_run('Exercises 4\u20137 are open-ended. Accept any grammatically correct sentence that matches the requested structure.')
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=6)

    # Exercise 4: compound sentence with semicolon + conjunctive adverb
    add_exercise(doc, 4, 'Write a compound sentence using a semicolon, conjunctive adverb, and comma.', body_size, font_name=body_font)
    add_plain_line(doc, 'Structure: Compound sentence using semicolon + conjunctive adverb + comma', body_size, bold_prefix='', font_name=body_font)
    add_plain_line(doc, 'Sample: "The test was difficult; however, most students passed."', body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc, 'Also acceptable: "The project was late. Nevertheless, the client was satisfied."', body_size, indent=0.7, font_name=body_font)

    exercise_separator(doc, overhead)

    # Exercise 5: complex sentence with cause/reason
    add_exercise(doc, 5, 'Write a complex sentence with a dependent clause showing cause or reason.', body_size, font_name=body_font)
    add_plain_line(doc, 'Structure: Complex sentence with dependent clause showing cause/reason', body_size, bold_prefix='', font_name=body_font)
    add_plain_line(doc, 'Sample: "Because the roads were icy, school was canceled."', body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc, 'Also acceptable: "She left early since she had an appointment."', body_size, indent=0.7, font_name=body_font)

    exercise_separator(doc, overhead)

    # Exercise 6: compound-complex sentence
    add_exercise(doc, 6, 'Write a compound-complex sentence (two ICs joined by FANBOYS + at least one DC).', body_size, font_name=body_font)
    add_plain_line(doc, 'Structure: Compound-complex (two ICs joined by FANBOYS + at least one DC)', body_size, bold_prefix='', font_name=body_font)
    add_plain_line(doc, 'Sample: "Although the weather was terrible, the game continued, and the fans cheered."', body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc, 'Sample: "She studied all night because the exam was important, and she passed."', body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc, 'Check: two ICs connected by a coordinating conjunction + at least one DC with a subordinating conjunction.', body_size, indent=0.7, font_name=body_font)

    exercise_separator(doc, overhead)

    # Exercise 7: DC first vs last, emphasis
    add_exercise(doc, 7, 'Write a complex sentence two ways: DC first, then DC last. Which version places more emphasis on the main clause?', body_size, font_name=body_font)
    add_plain_line(doc, 'Structure: Complex sentence \u2014 one version DC first, one version DC last', body_size, bold_prefix='', font_name=body_font)
    add_plain_line(doc, 'Sample Version 1 (DC first): "Because she studied all week, she passed the exam."', body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc, 'Sample Version 2 (DC last): "She passed the exam because she studied all week."', body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc,
        'More emphasis on main clause: Version 2 places the main clause first and unqualified. '
        'Version 1 announces background context first, so the main clause feels like a conclusion. '
        'Both are correct \u2014 the choice depends on what the writer wants the reader to notice first.',
        body_size, indent=0.7, font_name=body_font)

    exercise_separator(doc, overhead)

    # =============================================
    # Part 3: Error Correction
    # =============================================
    add_part_heading(doc, 'Part 3: Error Correction', cfg, overhead)

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

    exercise_separator(doc, overhead)

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

    exercise_separator(doc, overhead)

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

    exercise_separator(doc, overhead)

    # =============================================
    # Part 4: Sentence Tables and Diagrams
    # =============================================
    add_part_heading(doc, 'Part 4: Sentence Tables and Diagrams', cfg, overhead)

    add_exercise(doc, 11, 'Complete the table and draw a tree diagram for each sentence.', body_size, font_name=body_font)

    for ex in DIAGRAM_EXERCISES:
        add_sub_sentence(doc, ex['sub'], ex['sentence'], body_size, font_name=body_font)
        add_labeling_table(
            doc,
            words=ex['words'],
            pos_labels=ex['pos'],
            phrase_labels=ex['phrases'],
            role_labels=ex['roles'],
            font_size=body_size - 2,
        )
        add_bracket_line(doc, ex['bracket'], body_size, indent=0.35, font_name=body_font)
        exercise_separator(doc, overhead)

    # =============================================
    # Part 5: Emphasis, End-Weight, and Clause Revision
    # =============================================
    add_part_heading(doc, 'Part 5: Emphasis, End-Weight, and Clause Revision', cfg, overhead)

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
        'Both facts carry equal weight in the original \u2014 using "and" signals this equality.'
    )
    run.font.size = Pt(body_size)
    run.font.name = body_font
    set_paragraph_spacing(p, space_before=3, space_after=2)

    exercise_separator(doc, overhead)

    # Exercise 13: end-weight
    add_exercise(doc, 13, 'Revise the following front-loaded sentence using end-weight, then explain why the revision is easier to read.', body_size, font_name=body_font)

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

    exercise_separator(doc, overhead)

    # Exercise 14: clause density revision
    add_exercise(doc, 14, 'Revise the following passage using subordination. Then explain one of your revisions.', body_size, font_name=body_font)

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
        homework_dir / 'Answer Keys' / 'Chapter 09 Answer Key.docx',
        font_size=12
    )

    create_answer_key(
        homework_dir / 'Overheads' / 'Homework 09 Overhead.docx',
        overhead=True
    )


if __name__ == '__main__':
    main()
