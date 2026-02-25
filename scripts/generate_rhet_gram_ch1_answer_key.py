#!/usr/bin/env python3
"""
Generate Answer Key and Overhead Answer Key for
Homework Rhet Gram Ch 1 - S26.docx
"""

from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


# ─── helpers ────────────────────────────────────────────────────────────────

def set_spacing(paragraph, before=0, after=0):
    pPr = paragraph._p.get_or_add_pPr()
    sp = OxmlElement('w:spacing')
    sp.set(qn('w:before'), str(int(before * 20)))
    sp.set(qn('w:after'),  str(int(after  * 20)))
    pPr.append(sp)


def spacer(doc, font_name, size):
    """Blank spacer paragraph (for overhead use)."""
    p = doc.add_paragraph()
    run = p.add_run()
    run.font.name = font_name
    run.font.size = Pt(size)
    set_spacing(p, 0, 0)
    return p


def heading(doc, text, level, font_name, size, before=4, after=6):
    p = doc.add_heading(text, level=level)
    for run in p.runs:
        run.font.name = font_name
        run.font.size = Pt(size)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
    set_spacing(p, before, after)
    return p


def exercise_line(doc, number, sentence, font_name, size):
    """Bold 'Exercise N.' followed by italic sentence."""
    p = doc.add_paragraph()
    r = p.add_run(f'Exercise {number}.  ')
    r.bold = True; r.font.name = font_name; r.font.size = Pt(size)
    if sentence:
        r2 = p.add_run(sentence)
        r2.italic = True; r2.font.name = font_name; r2.font.size = Pt(size)
    set_spacing(p, 6, 2)
    return p


def labeled_line(doc, label, answer, font_name, size, indent=0.35):
    """Bold label + plain answer, indented."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(indent)
    r = p.add_run(label + ' ')
    r.bold = True; r.font.name = font_name; r.font.size = Pt(size)
    r2 = p.add_run(answer)
    r2.font.name = font_name; r2.font.size = Pt(size)
    set_spacing(p, 0, 2)
    return p


def plain_line(doc, text, font_name, size, indent=0.35, bold=False):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(indent)
    r = p.add_run(text)
    r.font.name = font_name; r.font.size = Pt(size); r.bold = bold
    set_spacing(p, 0, 2)
    return p


def italic_line(doc, text, font_name, size, indent=0.35):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(indent)
    r = p.add_run(text)
    r.italic = True; r.font.name = font_name; r.font.size = Pt(size)
    set_spacing(p, 0, 2)
    return p


def sub_item(doc, letter, answer, font_name, size, indent=0.35):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(indent)
    r = p.add_run(f'{letter})  ')
    r.bold = True; r.font.name = font_name; r.font.size = Pt(size)
    r2 = p.add_run(answer)
    r2.font.name = font_name; r2.font.size = Pt(size)
    set_spacing(p, 0, 2)
    return p


def add_table(doc, words, phrases, pos_list, font_name, size):
    """
    Add a 3-row word-analysis table.
    words    = list of words (columns 1+)
    phrases  = phrase label per word
    pos_list = part-of-speech per word
    """
    n = len(words)
    table = doc.add_table(rows=3, cols=n + 1)
    table.style = 'Table Grid'

    headers = ['Phrase', 'Word', 'Part of Speech']
    data_rows = [phrases, words, pos_list]

    for r_idx, (hdr, data) in enumerate(zip(headers, data_rows)):
        row = table.rows[r_idx]
        # header cell
        cell = row.cells[0]
        p = cell.paragraphs[0]
        run = p.add_run(hdr)
        run.bold = True
        run.font.name = font_name
        run.font.size = Pt(size)
        # data cells
        for c_idx, val in enumerate(data):
            cell = row.cells[c_idx + 1]
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.name = font_name
            run.font.size = Pt(size)
            if r_idx == 0:  # phrase row — bold
                run.bold = True

    # compact spacing after table
    p_after = doc.add_paragraph()
    p_after.add_run()
    set_spacing(p_after, 2, 4)
    return table


# ─── sentence data ──────────────────────────────────────────────────────────

PRACTICE = [
    {
        'label': 'Practice One',
        'sentence': 'Bears seldomly attack without a very good reason.',
        'words':   ['Bears', 'seldomly', 'attack', 'without', 'a', 'very', 'good', 'reason'],
        'phrases': ['NP',    'VP',       'VP',     'PP',      'PP', 'PP',  'PP',   'PP'],
        'pos':     ['N',     'Adv',      'V',      'Prep',    'Det','Adv', 'Adj',  'N'],
    },
    {
        'label': 'Practice Two',
        'sentence': 'Stephen usually sits alone at home.',
        'words':   ['Stephen', 'usually', 'sits', 'alone', 'at',   'home'],
        'phrases': ['NP',      'VP',      'VP',   'VP',    'PP',   'PP'],
        'pos':     ['N',       'Adv',     'V',    'Adv',   'Prep', 'N'],
    },
    {
        'label': 'Practice Three',
        'sentence': 'My younger brother works for the city.',
        'words':   ['My',  'younger', 'brother', 'works', 'for',  'the', 'city'],
        'phrases': ['NP',  'NP',      'NP',      'VP',    'PP',   'PP',  'PP'],
        'pos':     ['Det', 'Adj',     'N',       'V',     'Prep', 'Det', 'N'],
    },
    {
        'label': 'Practice Four',
        'sentence': 'The painfully long discussion continued incessantly until noon.',
        'words':   ['The', 'painfully', 'long', 'discussion', 'continued', 'incessantly', 'until', 'noon'],
        'phrases': ['NP',  'NP',        'NP',   'NP',         'VP',        'VP',          'PP',    'PP'],
        'pos':     ['Det', 'Adv',       'Adj',  'N',          'V',         'Adv',         'Prep',  'N'],
    },
    {
        'label': 'Example Five',
        'sentence': 'All my dearest friends from highschool suddenly left.',
        'words':   ['All', 'my',  'dearest', 'friends', 'from', 'highschool', 'suddenly', 'left'],
        'phrases': ['NP',  'NP',  'NP',      'NP',      'PP',   'PP',         'VP',       'VP'],
        'pos':     ['Det', 'Det', 'Adj',     'N',       'Prep', 'N',          'Adv',      'V'],
    },
]


# ─── document builder ───────────────────────────────────────────────────────

def build(output_path, overhead=False):
    if overhead:
        body_font   = 'Arial Narrow'
        body_size   = 18
        h1_size     = 22
        h2_size     = 20
        h3_size     = 18
        tbl_size    = 14
    else:
        body_font   = 'Garamond'
        body_size   = 12
        h1_size     = 16
        h2_size     = 14
        h3_size     = 12
        tbl_size    = 11

    doc = Document()

    # default style
    doc.styles['Normal'].font.name = body_font
    doc.styles['Normal'].font.size = Pt(body_size)

    # ── Title ──────────────────────────────────────────────────────────────
    heading(doc, 'Rhetorical Grammar: Chapter 1', 1, body_font, h1_size, before=0, after=4)
    heading(doc, 'Answer Key', 2, body_font, h2_size, before=0, after=10)
    if overhead:
        spacer(doc, body_font, body_size)

    # ══════════════════════════════════════════════════════════════════════
    # Exercise 1: Headwords and determiners
    # ══════════════════════════════════════════════════════════════════════
    heading(doc, 'Exercise 1: Headwords and Determiners', 3, body_font, h3_size, before=6, after=4)

    # Sentence 1
    exercise_line(doc, '1a', 'CGI helped produce the lush, cinematic rain forests of James '
                  "Cameron\u2019s Avatar as well as the teeming orc armies of Peter Jackson\u2019s Hobbit series.",
                  body_font, body_size)
    labeled_line(doc, 'Headwords:', 'CGI \u2022 rain forests \u2022 Avatar \u2022 armies \u2022 series  '
                 '(also Cameron and Jackson inside possessive DPs)', body_font, body_size)
    labeled_line(doc, 'Determiners:', 'the (before \u201clush, cinematic rain forests\u201d) \u2022 '
                 "James Cameron\u2019s (possessive Det for \u201cAvatar\u201d) \u2022 "
                 'the (before \u201cteeming orc armies\u201d) \u2022 '
                 "Peter Jackson\u2019s (possessive Det for \u201cHobbit series\u201d)",
                 body_font, body_size)
    if overhead:
        spacer(doc, body_font, body_size)

    # Sentence 2
    exercise_line(doc, '1b', 'In the operating room, surgeons may rely on three-dimensional images '
                  "to improve their patients\u2019 prognoses.",
                  body_font, body_size)
    labeled_line(doc, 'Headwords:', 'room \u2022 surgeons \u2022 images \u2022 prognoses',
                 body_font, body_size)
    labeled_line(doc, 'Determiners:', 'the (before \u201coperating room\u201d) \u2022 '
                 "their patients\u2019 (possessive Det for \u201cprognoses\u201d)",
                 body_font, body_size)
    if overhead:
        spacer(doc, body_font, body_size)

    # Sentence 3
    exercise_line(doc, '1c', 'Clearly, this innovation has the potential to shape our future.',
                  body_font, body_size)
    labeled_line(doc, 'Headwords:', 'innovation \u2022 potential \u2022 future', body_font, body_size)
    labeled_line(doc, 'Determiners:', 'this (before \u201cinnovation\u201d) \u2022 '
                 'the (before \u201cpotential\u201d) \u2022 our (before \u201cfuture\u201d)',
                 body_font, body_size)
    if overhead:
        spacer(doc, body_font, body_size)
        doc.add_page_break()

    # ══════════════════════════════════════════════════════════════════════
    # Exercise 2: Subject / Predicate
    # ══════════════════════════════════════════════════════════════════════
    heading(doc, 'Exercise 2: Subject / Predicate', 3, body_font, h3_size, before=6, after=4)

    ex2 = [
        ("The mayor\u2019s husband / spoke against the ordinance.",
         "The mayor\u2019s husband", "spoke against the ordinance"),
        ("The merchants in town / are unhappy.",
         "The merchants in town", "are unhappy"),
        ("The three white monkeys / carelessly climbed on their tall tree.",
         "The three white monkeys", "carelessly climbed on their tall tree"),
    ]
    for i, (marked, subj, pred) in enumerate(ex2, 1):
        exercise_line(doc, f'2.{i}', marked, body_font, body_size)
        labeled_line(doc, 'Subject:', subj, body_font, body_size)
        labeled_line(doc, 'Predicate:', pred, body_font, body_size)
        if overhead:
            spacer(doc, body_font, body_size)

    if overhead:
        doc.add_page_break()

    # ══════════════════════════════════════════════════════════════════════
    # Exercise 3: Prepositional Phrases
    # ══════════════════════════════════════════════════════════════════════
    heading(doc, 'Exercise 3: Prepositional Phrases', 3, body_font, h3_size, before=6, after=4)

    exercise_line(doc, '3.1', 'Birthday cakes are common in many Western cultures.',
                  body_font, body_size)
    labeled_line(doc, 'PP:', '\u201cin many Western cultures\u201d', body_font, body_size)
    labeled_line(doc, 'Function:', 'Adverbial \u2014 modifies \u201care common,\u201d '
                 'indicating context/location', body_font, body_size)
    if overhead:
        spacer(doc, body_font, body_size)

    exercise_line(doc, '3.2', 'Cupcakes are a popular alternative to birthday cakes.',
                  body_font, body_size)
    labeled_line(doc, 'PP:', '\u201cto birthday cakes\u201d', body_font, body_size)
    labeled_line(doc, 'Function:', 'Adjectival \u2014 modifies the noun \u201calternative\u201d',
                 body_font, body_size)
    if overhead:
        spacer(doc, body_font, body_size)

    exercise_line(doc, '3.3', 'The man in the big red hat spoke eloquently about his vacation to Morocco.',
                  body_font, body_size)
    labeled_line(doc, 'PP 1:', '\u201cin the big red hat\u201d', body_font, body_size)
    labeled_line(doc, 'Function:', 'Adjectival \u2014 modifies the noun \u201cman\u201d',
                 body_font, body_size)
    labeled_line(doc, 'PP 2:', '\u201cabout his vacation\u201d', body_font, body_size)
    labeled_line(doc, 'Function:', 'Adverbial \u2014 modifies the verb \u201cspoke\u201d',
                 body_font, body_size)
    labeled_line(doc, 'PP 3:', '\u201cto Morocco\u201d', body_font, body_size)
    labeled_line(doc, 'Function:', 'Adjectival \u2014 modifies the noun \u201cvacation\u201d',
                 body_font, body_size)
    if overhead:
        spacer(doc, body_font, body_size)
        doc.add_page_break()

    # ══════════════════════════════════════════════════════════════════════
    # Exercise 4: Sentence Labeling Tables
    # ══════════════════════════════════════════════════════════════════════
    heading(doc, 'Exercise 4: Sentence Labeling Tables', 3, body_font, h3_size, before=6, after=4)

    note = doc.add_paragraph()
    r = note.add_run('Note: ')
    r.bold = True; r.font.name = body_font; r.font.size = Pt(body_size)
    r2 = note.add_run('Diagrams will vary. Confirm that subject NP, VP, and any PPs are '
                      'correctly identified and that the diagram matches the table analysis below.')
    r2.font.name = body_font; r2.font.size = Pt(body_size)
    set_spacing(note, 0, 8)

    for item in PRACTICE:
        # sub-heading for each practice item
        lbl = doc.add_paragraph()
        lbl.add_run(item['label'] + ':  ').bold = True
        lbl.runs[0].font.name = body_font
        lbl.runs[0].font.size = Pt(body_size)
        r_s = lbl.add_run(item['sentence'])
        r_s.italic = True; r_s.font.name = body_font; r_s.font.size = Pt(body_size)
        set_spacing(lbl, 6, 3)

        add_table(doc, item['words'], item['phrases'], item['pos'], body_font, tbl_size)

        if overhead:
            spacer(doc, body_font, body_size)
            doc.add_page_break()

    # ── save ───────────────────────────────────────────────────────────────
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    print(f'Saved: {output_path}')


# ─── main ────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    base = Path(__file__).parent.parent / 'Homework'

    build(base / 'Homework Rhet Gram Ch 1 - S26 Answer Key.docx', overhead=False)
    build(base / 'Homework Rhet Gram Ch 1 - S26 Overhead.docx',   overhead=True)
