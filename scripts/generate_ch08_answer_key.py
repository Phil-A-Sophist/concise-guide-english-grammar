#!/usr/bin/env python3
"""
Generate Chapter 8 Answer Key and Overhead Answer Key .docx files.
Updated to match revised homework structure (5 parts, 14 exercises).
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
        'label': 'Pattern 1 (Intransitive): Birds sing.',
        'words':   ['Birds', 'sing'],
        'roles':   ['Subj', 'Pred'],
        'phrases': ['NP', 'VP'],
        'pos':     ['N', 'V'],
        'bracket': '[S [NP [N Birds]] [VP [V sing]]]',
    },
    {
        'sub': 'b)',
        'label': 'Pattern 2 (Copular Be): The solution was simple.',
        'words':   ['The', 'solution', 'was', 'simple'],
        'roles':   ['Subj', '', 'Pred', 'SC'],
        'phrases': ['NP', '', 'VP', 'ADJP'],
        'pos':     ['DET', 'N', 'V', 'ADJ'],
        'bracket': '[S [NP [DET The] [N solution]] [VP [V was] [ADJP [ADJ simple]]]]',
    },
    {
        'sub': 'c)',
        'label': 'Pattern 3 (Linking Verb): The music sounded beautiful.',
        'words':   ['The', 'music', 'sounded', 'beautiful'],
        'roles':   ['Subj', '', 'Pred', 'SC'],
        'phrases': ['NP', '', 'VP', 'ADJP'],
        'pos':     ['DET', 'N', 'V', 'ADJ'],
        'bracket': '[S [NP [DET The] [N music]] [VP [V sounded] [ADJP [ADJ beautiful]]]]',
    },
    {
        'sub': 'd)',
        'label': 'Pattern 4 (Transitive): The student finished the report.',
        'words':   ['The', 'student', 'finished', 'the', 'report'],
        'roles':   ['Subj', '', 'Pred', 'DO', ''],
        'phrases': ['NP', '', 'VP', 'NP', ''],
        'pos':     ['DET', 'N', 'V', 'DET', 'N'],
        'bracket': '[S [NP [DET The] [N student]] [VP [V finished] [NP [DET the] [N report]]]]',
    },
    {
        'sub': 'e)',
        'label': 'Pattern 5 (Ditransitive, IO + DO): The professor gave the class a deadline.',
        'words':   ['The', 'professor', 'gave', 'the', 'class', 'a', 'deadline'],
        'roles':   ['Subj', '', 'Pred', 'IO', '', 'DO', ''],
        'phrases': ['NP', '', 'VP', 'NP', '', 'NP', ''],
        'pos':     ['DET', 'N', 'V', 'DET', 'N', 'DET', 'N'],
        'bracket': '[S [NP [DET The] [N professor]] [VP [V gave] [NP [DET the] [N class]] [NP [DET a] [N deadline]]]]',
    },
    {
        'sub': 'f)',
        'label': 'Pattern 6 (Ditransitive, DO + OC): The board declared the plan inadequate.',
        'words':   ['The', 'board', 'declared', 'the', 'plan', 'inadequate'],
        'roles':   ['Subj', '', 'Pred', 'DO', '', 'OC'],
        'phrases': ['NP', '', 'VP', 'NP', '', 'ADJP'],
        'pos':     ['DET', 'N', 'V', 'DET', 'N', 'ADJ'],
        'bracket': '[S [NP [DET The] [N board]] [VP [V declared] [NP [DET the] [N plan]] [ADJP [ADJ inadequate]]]]',
    },
]


def create_answer_key(output_path, font_size=12, overhead=False):
    doc = Document()
    cfg = setup_document(doc, overhead)
    body_font = cfg['body_font']
    body_size = cfg['body_size']

    add_title_page(doc, 'Chapter 8: Basic Sentence Elements and Sentence Patterns', cfg, overhead)

    # =============================================
    # Part 1: Sentence Element Identification
    # =============================================
    add_part_heading(doc, 'Part 1: Sentence Element Identification', cfg, overhead)

    # Exercise 1: Identify DO/IO/SC/OC
    add_exercise(doc, 1, 'Identify the direct object, indirect object, subject complement, or object complement in each sentence.', body_size, font_name=body_font)

    add_sub_sentence(doc, 'a)', 'The committee awarded the outstanding student a prestigious scholarship.', body_size, font_name=body_font)
    add_answer_line(doc, 'Indirect Object (IO):', 'the outstanding student', body_size, indent=0.7, font_name=body_font)
    add_answer_line(doc, 'Direct Object (DO):', 'a prestigious scholarship', body_size, indent=0.7, font_name=body_font)

    add_sub_sentence(doc, 'b)', 'The homemade soup tasted absolutely delicious.', body_size, font_name=body_font)
    add_answer_line(doc, 'Subject Complement (SC):', 'absolutely delicious (AdjP)', body_size, indent=0.7, font_name=body_font)

    add_sub_sentence(doc, 'c)', 'The judges declared the young contestant the winner.', body_size, font_name=body_font)
    add_answer_line(doc, 'Direct Object (DO):', 'the young contestant', body_size, indent=0.7, font_name=body_font)
    add_answer_line(doc, 'Object Complement (OC):', 'the winner (NP)', body_size, indent=0.7, font_name=body_font)

    exercise_separator(doc, overhead)

    # Exercise 2: Argument vs. adverbial
    add_exercise(doc, 2, 'Determine whether the underlined element is an argument (required) or an adverbial (optional). Explain your reasoning.', body_size, font_name=body_font)

    for sub, sentence, verdict, explanation in [
        ('a)', 'She placed the documents on the desk.',
         'Argument (required)',
         '"On the desk" is required by "placed." Remove it: *She placed the documents. \u2717 \u2014 ungrammatical without a location argument.'),
        ('b)', 'She found the documents on the desk.',
         'Adverbial (optional)',
         '"On the desk" is an optional location modifier. Remove it: She found the documents. \u2713 \u2014 still grammatical.'),
        ('c)', 'The professor is extremely knowledgeable about linguistics.',
         'Argument (required)',
         '"Extremely knowledgeable about linguistics" is the subject complement required by "is." Remove it: *The professor is. \u2717 \u2014 incomplete.'),
        ('d)', 'The professor lectured extremely knowledgeably about linguistics.',
         'Adverbial (optional)',
         '"Extremely knowledgeably about linguistics" is an optional manner/topic modifier. Remove it: The professor lectured. \u2713 \u2014 still grammatical.'),
    ]:
        add_sub_sentence(doc, sub, sentence, body_size, font_name=body_font)
        add_answer_line(doc, 'Answer:', verdict, body_size, indent=0.7, font_name=body_font)
        add_plain_line(doc, explanation, body_size, indent=0.7, font_name=body_font)

    exercise_separator(doc, overhead)

    # =============================================
    # Part 2: Sentence Pattern Identification
    # =============================================
    add_part_heading(doc, 'Part 2: Sentence Pattern Identification', cfg, overhead)

    patterns = [
        (3, 'The exhausted marathon runner collapsed at the finish line yesterday.',
         'Pattern 1 (Intransitive)',
         'Main verb: "collapsed." "At the finish line" and "yesterday" are adverbials (optional \u2014 answer where? and when?). '
         'Without adverbials: "The exhausted marathon runner collapsed." \u2014 complete with subject + intransitive verb. '
         '"Collapsed" does not require an object or complement.'),
        (4, "My grandmother's secret recipe remains a family treasure.",
         'Pattern 3 (Linking verb)',
         'Main verb: "remains." "A family treasure" is a subject complement (NP identifying the subject). '
         'Be substitution test: "My grandmother\'s secret recipe is a family treasure" \u2713. '
         'Since the verb is not "be" itself but passes the be-substitution test, this is Pattern 3 (Linking), not Pattern 2 (Copular be).'),
        (5, 'The committee considered the proposal inadequate.',
         'Pattern 6 (Ditransitive: DO + OC)',
         'Main verb: "considered." Two elements follow the verb: "the proposal" (NP) + "inadequate" (AdjP). '
         'Do they refer to the same thing? Yes \u2014 the proposal is described as inadequate. '
         'Therefore "the proposal" = Direct Object, "inadequate" = Object Complement.'),
        (6, 'The chef prepared the guests an extraordinary seven-course meal.',
         'Pattern 5 (Ditransitive: IO + DO)',
         'Main verb: "prepared." Two NPs follow the verb: "the guests" and "an extraordinary seven-course meal." '
         'Do they refer to the same thing? No \u2014 the guests \u2260 the meal. '
         'Can rephrase with "for": "prepared an extraordinary seven-course meal for the guests." '
         '"The guests" = Indirect Object, "an extraordinary seven-course meal" = Direct Object.'),
        (7, 'The situation grew increasingly tense during the negotiations.',
         'Pattern 3 (Linking verb)',
         'Main verb: "grew." "During the negotiations" is an adverbial (time) \u2014 set aside. '
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
        exercise_separator(doc, overhead)

    # =============================================
    # Part 3: Sentence Writing
    # =============================================
    add_part_heading(doc, 'Part 3: Sentence Writing', cfg, overhead)

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
        add_exercise(doc, num, f'Write a sentence using {pattern_label} and label each element.', body_size, font_name=body_font)
        add_plain_line(doc, f'{pattern_label}:', body_size, bold_prefix='Pattern: ', font_name=body_font)
        add_plain_line(doc, sample, body_size, font_name=body_font)
        exercise_separator(doc, overhead)

    # =============================================
    # Part 4: Sentence Tables and Diagrams
    # =============================================
    add_part_heading(doc, 'Part 4: Sentence Tables and Diagrams', cfg, overhead)

    add_exercise(doc, 11, 'Complete each table and draw a tree diagram.', body_size, font_name=body_font)

    for ex in DIAGRAM_EXERCISES:
        add_sub_sentence(doc, ex['sub'], ex['label'], body_size, font_name=body_font)
        add_labeling_table(
            doc,
            words=ex['words'],
            pos_labels=ex['pos'],
            phrase_labels=ex['phrases'],
            role_labels=ex['roles'],
            font_size=body_size,
        )
        add_bracket_line(doc, ex['bracket'], body_size, indent=0.7, font_name=body_font)
        exercise_separator(doc, overhead)

    # =============================================
    # Part 5: Analysis and Reflection
    # =============================================
    add_part_heading(doc, 'Part 5: Analysis and Reflection', cfg, overhead)

    # Exercise 12: "put" valency
    add_exercise(doc, 12, 'She put the book on the shelf.', body_size, font_name=body_font)

    for sub, answer in [
        ('What happens if you remove "the book"?',
         '*She put on the shelf. \u2717 \u2014 ungrammatical. "The book" is a required argument (Direct Object).'),
        ('What happens if you remove "on the shelf"?',
         '*She put the book. \u2717 \u2014 ungrammatical/incomplete. "On the shelf" is a required locative argument.'),
        ('What does this tell you about the valency of "put"?',
         '"Put" requires THREE arguments: a subject, a direct object, and a locative phrase. '
         'It has valency 3 \u2014 unusual among English verbs, most of which require only two.'),
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.35)
        run = p.add_run(sub)
        run.bold = True
        run.font.size = Pt(body_size)
        run.font.name = body_font
        set_paragraph_spacing(p, space_before=3, space_after=2)
        add_plain_line(doc, answer, body_size, indent=0.7, font_name=body_font)

    exercise_separator(doc, overhead)

    # Exercise 13: linking vs transitive
    add_exercise(doc, 13, 'Explain the difference between the two uses of "smells" in the following sentences.', body_size, font_name=body_font)

    add_sub_sentence(doc, 'a)', 'The milk smells sour. vs. The detective smells trouble.', body_size, font_name=body_font)
    add_plain_line(doc,
        '"The milk smells sour" \u2014 linking verb (Pattern 3). "Sour" is a subject complement describing the milk.',
        body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc,
        '"The detective smells trouble" \u2014 transitive verb (Pattern 4). "Trouble" is a direct object.',
        body_size, indent=0.7, font_name=body_font)
    add_plain_line(doc,
        'Be substitution test: "The milk is sour" \u2713 (makes sense \u2192 linking). '
        '"The detective is trouble" \u2717 (doesn\'t make sense \u2192 not linking, therefore transitive).',
        body_size, indent=0.7, font_name=body_font)

    exercise_separator(doc, overhead)

    # Exercise 14: argument vs adverbial reflection
    add_exercise(doc, 14, 'In your own words, explain the difference between an argument and an adverbial. Why does this distinction matter for identifying sentence patterns? Give an example.', body_size, font_name=body_font)

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
        '(removing it yields *She put the book \u2014 ungrammatical). But in "She read the book on the table," '
        '"on the table" is an adverbial (removing it yields She read the book \u2014 fine). '
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
        homework_dir / 'Answer Keys' / 'Chapter 08 Answer Key.docx',
        font_size=12
    )

    create_answer_key(
        homework_dir / 'Overheads' / 'Homework 08 Overhead.docx',
        overhead=True
    )


if __name__ == '__main__':
    main()
