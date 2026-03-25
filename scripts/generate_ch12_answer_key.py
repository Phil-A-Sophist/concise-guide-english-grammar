#!/usr/bin/env python3
"""
Generate Chapter 12 Answer Key and Overhead Answer Key .docx files.
"""

from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches

from answer_key_helpers import (
    set_paragraph_spacing, add_spacer_row, add_exercise, add_answer_line,
    add_plain_line, setup_document, add_title_page, add_part_heading,
    exercise_separator, get_font_config,
    add_labeling_table, add_bracket_line, blank_labels,
)


DIAGRAM_EXERCISES = [
    {
        'num': 14, 'sentence': 'She spoke very clearly.',
        'words':   ['She', 'spoke', 'very', 'clearly'],
        'roles':   ['Subj', 'Pred', '', ''],
        'phrases': ['NP', 'VP', 'ADVP', ''],
        'pos':     ['PRON', 'V', 'ADV', 'ADV'],
        'bracket': '[S [NP [PRON She]] [VP [V spoke] [ADVP [ADV very] [ADV clearly]]]]',
    },
    {
        'num': 15, 'sentence': 'The train arrived after midnight.',
        'words':   ['The', 'train', 'arrived', 'after', 'midnight'],
        'roles':   ['Subj', '', 'Pred', 'Advl', ''],
        'phrases': ['NP', '', 'VP', 'PP', ''],
        'pos':     ['DET', 'N', 'V', 'PREP', 'N'],
        'bracket': '[S [NP [DET The] [N train]] [VP [V arrived] [PP [PREP after] [NP [N midnight]]]]]',
    },
    {
        'num': 16, 'sentence': 'He walked slowly through the park.',
        'words':   ['He', 'walked', 'slowly', 'through', 'the', 'park'],
        'roles':   ['Subj', 'Pred', '', 'Advl', '', ''],
        'phrases': ['NP', 'VP', 'ADVP', 'PP', 'NP', ''],
        'pos':     ['PRON', 'V', 'ADV', 'PREP', 'DET', 'N'],
        'bracket': '[S [NP [PRON He]] [VP [V walked] [ADVP [ADV slowly]] [PP [PREP through] [NP [DET the] [N park]]]]]',
    },
    {
        'num': 17, 'sentence': 'Unfortunately, the game was cancelled.',
        'words':   ['Unfortunately', 'the', 'game', 'was', 'cancelled'],
        'roles':   ['Disjunct', 'Subj', '', 'Pred', ''],
        'phrases': ['ADVP', 'NP', '', 'VP', ''],
        'pos':     ['ADV', 'DET', 'N', 'AUX', 'V'],
        'bracket': '[S [ADVP [ADV Unfortunately]] [NP [DET the] [N game]] [VP [AUX was] [V cancelled]]]',
    },
    {
        'num': 18, 'sentence': 'She left early because the roads were icy.',
        'words':   ['She', 'left', 'early', 'because', 'the', 'roads', 'were', 'icy'],
        'roles':   ['Subj', 'Pred', '', 'Advl', '', '', '', ''],
        'phrases': ['NP', 'VP', 'ADVP', 'SBAR', 'NP', '', 'VP', 'ADJP'],
        'pos':     ['PRON', 'V', 'ADV', 'COMP', 'DET', 'N', 'V', 'ADJ'],
        'bracket': '[S [NP [PRON She]] [VP [V left] [ADVP [ADV early]]] [SBAR [COMP because] [S [NP [DET the] [N roads]] [VP [V were] [ADJP [ADJ icy]]]]]]',
    },
]


def create_answer_key(output_path, font_size=12, overhead=False):
    """Create the Chapter 12 Answer Key document."""
    doc = Document()
    cfg = setup_document(doc, overhead)
    body_font = cfg['body_font']
    body_size = cfg['body_size']

    add_title_page(doc, 'Chapter 12: Adverbials', cfg, overhead)

    # =============================================
    # Part 1: Identification and Classification
    # =============================================
    add_part_heading(doc, 'Part 1: Identification and Classification', cfg, overhead)

    # Exercise 1
    add_exercise(doc, 1, 'Last week, the students studied diligently in the library.', body_size, font_name=body_font)
    add_answer_line(doc, 'Adverbial 1:', 'Last week \u2014 NP \u2014 time', body_size, font_name=body_font)
    add_answer_line(doc, 'Adverbial 2:', 'diligently \u2014 AdvP \u2014 manner', body_size, font_name=body_font)
    add_answer_line(doc, 'Adverbial 3:', 'in the library \u2014 PP \u2014 place', body_size, font_name=body_font)

    exercise_separator(doc, overhead)

    # Exercise 2
    add_exercise(doc, 2, 'If you need assistance, please call the help desk immediately.', body_size, font_name=body_font)
    add_answer_line(doc, 'Adverbial 1:', 'If you need assistance \u2014 adverb clause \u2014 condition', body_size, font_name=body_font)
    add_answer_line(doc, 'Adverbial 2:', 'immediately \u2014 AdvP \u2014 time', body_size, font_name=body_font)

    exercise_separator(doc, overhead)

    # Exercise 3
    add_exercise(doc, 3, 'She left early to catch her flight.', body_size, font_name=body_font)
    add_answer_line(doc, 'Adverbial 1:', 'early \u2014 AdvP \u2014 time', body_size, font_name=body_font)
    add_answer_line(doc, 'Adverbial 2:', 'to catch her flight \u2014 infinitive phrase \u2014 purpose', body_size, font_name=body_font)

    # =============================================
    # Part 2: Adjunct, Disjunct, or Conjunct
    # =============================================
    add_part_heading(doc, 'Part 2: Adjunct, Disjunct, or Conjunct', cfg, overhead)

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

    for i, (num, sentence, classification, explanation) in enumerate(classifications):
        if i > 0:
            exercise_separator(doc, overhead)
        add_exercise(doc, num, sentence, body_size, font_name=body_font)
        add_answer_line(doc, 'Classification:', classification, body_size, font_name=body_font)
        add_plain_line(doc, explanation, body_size, font_name=body_font)

    # =============================================
    # Part 3: Sentence Completion
    # =============================================
    add_part_heading(doc, 'Part 3: Sentence Completion', cfg, overhead)

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

    for i, (num, prompt, sample) in enumerate(completions):
        if i > 0:
            exercise_separator(doc, overhead)
        add_exercise(doc, num, f'Complete the sentence with the specified adverbial type: {prompt}', body_size, font_name=body_font)
        add_plain_line(doc, prompt, body_size, bold_prefix='Prompt: ', font_name=body_font)
        add_plain_line(doc, f'Sample: {sample}', body_size, font_name=body_font)

    # =============================================
    # Part 4: Diagramming Adverbials
    # =============================================
    add_part_heading(doc, 'Part 4: Diagramming Adverbials', cfg, overhead)

    for i, ex in enumerate(DIAGRAM_EXERCISES):
        if i > 0:
            exercise_separator(doc, overhead)
        add_exercise(doc, ex['num'], ex['sentence'], body_size, font_name=body_font)
        add_labeling_table(
            doc,
            words=ex['words'],
            pos_labels=ex['pos'],
            phrase_labels=ex['phrases'],
            role_labels=ex['roles'],
            font_size=body_size,
        )
        add_bracket_line(doc, ex['bracket'], body_size, font_name=body_font)

    # =============================================
    # Part 5: Analysis and Application
    # =============================================
    add_part_heading(doc, 'Part 5: Analysis and Application', cfg, overhead)

    # Exercise 19
    add_exercise(doc, 19, 'Identify five adverbials in the passage:', body_size, font_name=body_font)

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

    exercise_separator(doc, overhead)

    # Exercise 20
    add_exercise(doc, 20, 'Explain the difference between "Surprisingly" (disjunct) and "diligently" (adjunct):', body_size, font_name=body_font)
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

    exercise_separator(doc, overhead)

    # Exercise 21
    add_exercise(doc, 21, 'Rewrite with "yesterday" in three positions:', body_size, font_name=body_font)

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
        homework_dir / 'Answer Keys' / 'Chapter 12 Answer Key.docx',
        font_size=12
    )

    create_answer_key(
        homework_dir / 'Overheads' / 'Homework 12 Overhead.docx',
        overhead=True
    )


if __name__ == '__main__':
    main()
