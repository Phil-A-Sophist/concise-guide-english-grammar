#!/usr/bin/env python3
"""
Generate Chapter 16 Answer Key and Overhead Answer Key .docx files.
"""

from pathlib import Path
from docx import Document

from answer_key_helpers import (
    set_paragraph_spacing, add_spacer_row, add_exercise, add_answer_line,
    add_plain_line, setup_document, add_title_page, add_part_heading,
    exercise_separator, get_font_config,
)


def create_answer_key(output_path, font_size=12, overhead=False):
    """Create the Chapter 16 Answer Key document."""
    doc = Document()
    cfg = setup_document(doc, overhead)
    body_font = cfg['body_font']
    body_size = cfg['body_size']

    add_title_page(doc, 'Chapter 16: Other Grammatical Forms', cfg, overhead)

    # =============================================
    # Part 1: Nonfinite Verb Forms
    # =============================================
    add_part_heading(doc, 'Part 1: Nonfinite Verb Forms', cfg, overhead)

    # Exercise 1
    add_exercise(doc, 1, 'Swimming is excellent exercise.', body_size, font_name=body_font)
    add_answer_line(doc, 'Answer:', 'Swimming', body_size, font_name=body_font)
    add_plain_line(doc, 'Gerund (functioning as the subject of the sentence)', body_size, font_name=body_font)
    exercise_separator(doc, overhead)

    # Exercise 2
    add_exercise(doc, 2, 'The broken window needs repair.', body_size, font_name=body_font)
    add_answer_line(doc, 'Answer:', 'broken', body_size, font_name=body_font)
    add_plain_line(doc, 'Past participle (functioning adjectivally, modifying "window")', body_size, font_name=body_font)
    exercise_separator(doc, overhead)

    # Exercise 3
    add_exercise(doc, 3, 'I saw him running toward the door.', body_size, font_name=body_font)
    add_answer_line(doc, 'Answer:', 'running', body_size, font_name=body_font)
    add_plain_line(doc,
        'Present participle (functioning as an object complement after perception verb "saw")',
        body_size, font_name=body_font)
    exercise_separator(doc, overhead)

    # Exercise 4
    add_exercise(doc, 4, 'They made her apologize.', body_size, font_name=body_font)
    add_answer_line(doc, 'Answer:', 'apologize', body_size, font_name=body_font)
    add_plain_line(doc,
        'Bare infinitive (no "to"; after causative verb "made")',
        body_size, font_name=body_font)
    exercise_separator(doc, overhead)

    # Exercise 5
    add_exercise(doc, 5, 'Having finished the exam, she left the room.', body_size, font_name=body_font)
    add_answer_line(doc, 'Answer:', 'Having finished', body_size, font_name=body_font)
    add_plain_line(doc,
        'Perfect participle (past participle with "having"; functioning adverbially)',
        body_size, font_name=body_font)
    exercise_separator(doc, overhead)

    # =============================================
    # Part 2: Complement Clauses
    # =============================================
    add_part_heading(doc, 'Part 2: Complement Clauses', cfg, overhead)

    complements = [
        (6, 'She believes that honesty matters.',
         'that honesty matters',
         'That-clause (complement of the verb "believes")'),
        (7, 'He wants to succeed in his career.',
         'to succeed in his career',
         'Infinitive clause (complement of the verb "wants")'),
        (8, 'I wonder what she meant.',
         'what she meant',
         'Wh-clause (complement of the verb "wonder")'),
        (9, 'She enjoys reading novels.',
         'reading novels',
         'Gerund clause (complement of the verb "enjoys")'),
    ]

    for num, sentence, clause, classification in complements:
        add_exercise(doc, num, sentence, body_size, font_name=body_font)
        add_answer_line(doc, 'Complement clause:', clause, body_size, font_name=body_font)
        add_plain_line(doc, classification, body_size, font_name=body_font)
        exercise_separator(doc, overhead)

    # =============================================
    # Part 3: Special Constructions
    # =============================================
    add_part_heading(doc, 'Part 3: Special Constructions', cfg, overhead)

    constructions = [
        (10, 'It was John who broke the window.',
         'It-cleft (cleft sentence)',
         'Focuses attention on "John" as the agent. Presupposes that someone broke the window '
         'and highlights who did it.'),
        (11, 'There are three students waiting in the hall.',
         'Existential sentence',
         'Introduces new entities ("three students") into the discourse. '
         'The expletive "there" serves as a placeholder subject.'),
        (12, 'It surprised everyone that she resigned.',
         'Extraposition',
         'The subject clause "that she resigned" has been moved to the end, '
         'with "it" as a placeholder. This avoids a heavy subject and '
         'puts the surprising information at the end for emphasis.'),
        (13, 'That movie, I never liked.',
         'Topicalization',
         'The object "that movie" has been moved to the front of the sentence '
         'for emphasis, establishing it as the topic of discussion.'),
    ]

    for num, sentence, ctype, effect in constructions:
        add_exercise(doc, num, sentence, body_size, font_name=body_font)
        add_answer_line(doc, 'Construction type:', ctype, body_size, font_name=body_font)
        add_plain_line(doc, effect, body_size, bold_prefix='Effect: ', font_name=body_font)
        exercise_separator(doc, overhead)

    # =============================================
    # Part 4: Coordination and Revision
    # =============================================
    add_part_heading(doc, 'Part 4: Coordination and Revision', cfg, overhead)

    # Exercise 14
    add_exercise(doc, 14, 'She likes swimming, hiking, and to ride bikes.', body_size, font_name=body_font)
    add_answer_line(doc, 'Revised:', 'She likes swimming, hiking, and riding bikes.', body_size, font_name=body_font)
    add_plain_line(doc,
        'All three items are now gerunds, creating parallel structure.',
        body_size, font_name=body_font)
    exercise_separator(doc, overhead)

    # Exercise 15
    add_exercise(doc, 15, 'The candidate promised to cut taxes and creating jobs.', body_size, font_name=body_font)
    add_answer_line(doc, 'Revised:', 'The candidate promised to cut taxes and create jobs.', body_size, font_name=body_font)
    add_plain_line(doc,
        'Both items are now infinitives (sharing "to"), creating parallel structure.',
        body_size, font_name=body_font)
    exercise_separator(doc, overhead)

    # Exercise 16
    add_exercise(doc, 16, 'The committee rejected the budget.', body_size, font_name=body_font)
    add_answer_line(doc, 'Cleft version:', 'It was the budget that the committee rejected.', body_size, font_name=body_font)
    add_plain_line(doc,
        'The it-cleft focuses on "the budget" as the thing rejected.',
        body_size, font_name=body_font)
    exercise_separator(doc, overhead)

    # Exercise 17
    add_exercise(doc, 17, 'That she would resign surprised everyone.', body_size, font_name=body_font)
    add_answer_line(doc, 'Extraposed:', 'It surprised everyone that she would resign.', body_size, font_name=body_font)
    add_plain_line(doc,
        'The heavy subject clause moves to the end, with "it" as placeholder.',
        body_size, font_name=body_font)
    exercise_separator(doc, overhead)

    # =============================================
    # Part 5: Passage Analysis
    # =============================================
    add_part_heading(doc, 'Part 5: Passage Analysis', cfg, overhead)

    # Exercise 18
    add_exercise(doc, 18, 'Identify the nonfinite verb forms in the passage.', body_size, font_name=body_font)
    add_plain_line(doc, 'Nonfinite verb forms in the passage:', body_size, indent=0, bold_prefix='', font_name=body_font)
    add_plain_line(doc,
        '\u2022 "Having examined" \u2014 perfect participle (adverbial, modifying "they")',
        body_size, font_name=body_font)
    add_plain_line(doc,
        '\u2022 "planned" \u2014 past participle (passive: "had been carefully planned")',
        body_size, font_name=body_font)
    add_plain_line(doc,
        '\u2022 "To identify" \u2014 to-infinitive (subject of "would require")',
        body_size, font_name=body_font)
    exercise_separator(doc, overhead)

    # Exercise 19
    add_exercise(doc, 19, 'Identify the special constructions in the passage.', body_size, font_name=body_font)
    add_plain_line(doc,
        '\u2022 Cleft sentence: "What surprised the investigators was the lack of evidence" (wh-cleft)',
        body_size, font_name=body_font)
    add_plain_line(doc,
        '\u2022 Existential sentence: "There were no witnesses"',
        body_size, font_name=body_font)
    add_plain_line(doc,
        '\u2022 Extraposition: "It was clear that someone with inside knowledge was responsible" '
        '("that" clause extraposed, "it" as placeholder)',
        body_size, font_name=body_font)
    exercise_separator(doc, overhead)

    # Exercise 20
    add_exercise(doc, 20, 'Rewrite the wh-cleft as a simple sentence and as an it-cleft.', body_size, font_name=body_font)
    add_plain_line(doc,
        'a) Simple sentence: The lack of evidence surprised the investigators.',
        body_size, font_name=body_font)
    add_plain_line(doc,
        'b) It-cleft: It was the lack of evidence that surprised the investigators.',
        body_size, font_name=body_font)
    exercise_separator(doc, overhead)

    # Exercise 21
    add_exercise(doc, 21, 'Discuss how cleft sentences and extraposition affect emphasis and readability in the passage.', body_size, font_name=body_font)
    add_plain_line(doc,
        'Open-ended. Accept answers that discuss how cleft sentences focus attention on '
        'specific elements (creating emphasis and contrast), while extraposition improves '
        'readability by avoiding heavy subjects. Both constructions manipulate information '
        'structure to control what readers notice first and to create stylistic effects such '
        'as suspense, emphasis, or smoother processing.',
        body_size, font_name=body_font)
    exercise_separator(doc, overhead)

    doc.save(str(output_path))
    print(f"Created: {output_path}")


def main():
    script_dir = Path(__file__).parent
    homework_dir = script_dir.parent / 'Homework'

    create_answer_key(
        homework_dir / 'Answer Keys' / 'Chapter 16 Answer Key.docx',
        font_size=12
    )

    create_answer_key(
        homework_dir / 'Overheads' / 'Homework 16 Overhead.docx',
        overhead=True
    )


if __name__ == '__main__':
    main()
