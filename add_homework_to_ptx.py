#!/usr/bin/env python3
"""
Extract homework sections from markdown chapters and add them to PreTeXt files.
"""

import re
import os
from pathlib import Path


def extract_homework_section(md_content):
    """Extract the homework section from markdown."""
    match = re.search(r'^## Homework:.*?(?=^## Glossary|\Z)', md_content, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(0).strip()
    return None


def markdown_to_pretext(homework_md, chapter_num):
    """Convert homework markdown to PreTeXt XML."""
    lines = homework_md.split('\n')

    # Get the homework title
    title_match = re.match(r'^## Homework:\s*(.+)$', lines[0])
    homework_title = title_match.group(1).strip() if title_match else "Homework"

    # Start building the PreTeXt section
    xml_id = f"ch-{chapter_num:02d}-homework"
    ptx = [f'  <section xml:id="{xml_id}">']
    ptx.append(f'    <title>Homework: {homework_title}</title>')
    ptx.append('')

    current_part = None
    in_list = False
    in_blockquote = False
    blockquote_lines = []

    i = 1  # Skip the title line
    while i < len(lines):
        line = lines[i].rstrip()

        # Skip name/date lines and horizontal rules
        if line.startswith('**Name:') or line.startswith('**Date:') or line == '---':
            i += 1
            continue

        # Skip "Due before" lines
        if line.startswith('*Due '):
            i += 1
            continue

        # Handle Part headers (### Part A:, ### Part B:, etc.)
        part_match = re.match(r'^###\s+Part\s+([A-Z]):\s*(.+)$', line)
        if part_match:
            if in_list:
                ptx.append('    </ul>')
                in_list = False
            ptx.append('')
            ptx.append('    <paragraphs>')
            ptx.append(f'      <title>Part {part_match.group(1)}: {part_match.group(2)}</title>')
            ptx.append('    </paragraphs>')
            ptx.append('')
            current_part = part_match.group(1)
            i += 1
            continue

        # Handle numbered questions (**1.** text)
        question_match = re.match(r'^\*\*(\d+)\.\*\*\s*(.+)$', line)
        if question_match:
            if in_list:
                ptx.append('    </ul>')
                in_list = False

            q_num = question_match.group(1)
            q_text = question_match.group(2)
            # Convert markdown formatting
            q_text = convert_inline_formatting(q_text)
            ptx.append(f'    <p><em>Question {q_num}.</em> {q_text}</p>')
            ptx.append('')
            i += 1
            continue

        # Handle blockquotes (> text)
        if line.startswith('>'):
            if not in_blockquote:
                in_blockquote = True
                blockquote_lines = []
            # Remove the > prefix
            bq_line = line[1:].strip() if len(line) > 1 else ''
            bq_line = convert_inline_formatting(bq_line)
            blockquote_lines.append(bq_line)
            i += 1
            continue
        elif in_blockquote and line.strip() == '':
            # End of blockquote
            in_blockquote = False
            ptx.append('    <blockquote>')
            for bq in blockquote_lines:
                if bq:
                    ptx.append(f'      <p>{bq}</p>')
            ptx.append('    </blockquote>')
            ptx.append('')
            blockquote_lines = []
            i += 1
            continue

        # Handle bullet points (- text or * text)
        bullet_match = re.match(r'^[-*]\s+(.+)$', line)
        if bullet_match:
            if not in_list:
                ptx.append('    <ul>')
                in_list = True
            bullet_text = bullet_match.group(1)
            bullet_text = convert_inline_formatting(bullet_text)
            ptx.append(f'      <li><p>{bullet_text}</p></li>')
            i += 1
            continue

        # Handle regular paragraphs
        if line.strip() and not line.startswith('#'):
            if in_list:
                ptx.append('    </ul>')
                in_list = False
            text = convert_inline_formatting(line)
            ptx.append(f'    <p>{text}</p>')
            ptx.append('')

        i += 1

    # Close any open elements
    if in_blockquote:
        ptx.append('    <blockquote>')
        for bq in blockquote_lines:
            if bq:
                ptx.append(f'      <p>{bq}</p>')
        ptx.append('    </blockquote>')

    if in_list:
        ptx.append('    </ul>')

    ptx.append('  </section>')

    return '\n'.join(ptx)


def convert_inline_formatting(text):
    """Convert markdown inline formatting to PreTeXt."""
    # Convert bold (**text**)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<em>\1</em>', text)
    # Convert italic (*text*)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    # Convert quotes
    text = text.replace('"', '"').replace('"', '"')
    # Escape special XML characters (but not our tags)
    text = text.replace('&', '&amp;')
    # Fix any double-escaped ampersands
    text = text.replace('&amp;amp;', '&amp;')
    return text


def insert_homework_into_ptx(ptx_content, homework_ptx):
    """Insert the homework section before the glossary in a PreTeXt file."""
    # Find the glossary tag and insert homework before it
    if '<glossary>' in ptx_content:
        return ptx_content.replace('<glossary>', homework_ptx + '\n\n  <glossary>')
    elif '</chapter>' in ptx_content:
        # If no glossary, insert before </chapter>
        return ptx_content.replace('</chapter>', homework_ptx + '\n\n</chapter>')
    return ptx_content


def main():
    md_dir = Path("Writing Projects/concise_guide_to_english_grammar/chapters")
    ptx_dir = Path("source")

    # Mapping of chapter numbers to markdown files
    chapter_files = {
        1: "chapter_01_introduction_to_linguistics.md",
        2: "chapter_02_prescriptive_vs_descriptive.md",
        3: "chapter_03_language_variation.md",
        4: "chapter_04_morphology.md",
        5: "chapter_05_open_classes.md",
        6: "chapter_06_closed_classes.md",
        7: "chapter_07_sentence_diagramming.md",
        8: "chapter_08_sentence_elements_patterns.md",
        9: "chapter_09_compound_complex_sentences.md",
        10: "chapter_10_verbs_tense_aspect.md",
        11: "chapter_11_verbs_voice_modals.md",
        12: "chapter_12_adverbials.md",
        13: "chapter_13_nominals.md",
        14: "chapter_14_adjectivals.md",
        15: "chapter_15_other_grammatical_forms.md",
        16: "chapter_16_stylistic_choices.md",
        17: "chapter_17_punctuation.md",
        18: "chapter_18_clarity_readability.md",
        19: "chapter_19_organization_concision.md",
        20: "chapter_20_genre_register.md",
        21: "chapter_21_teaching_grammar.md",
    }

    print("Adding homework sections to PreTeXt files...\n")

    for chapter_num, md_file in chapter_files.items():
        md_path = md_dir / md_file
        ptx_path = ptx_dir / f"ch-{chapter_num:02d}.ptx"

        print(f"Processing Chapter {chapter_num}...")

        # Read markdown
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Extract homework
        homework_md = extract_homework_section(md_content)
        if not homework_md:
            print(f"  -> No homework section found in {md_file}")
            continue

        # Convert to PreTeXt
        homework_ptx = markdown_to_pretext(homework_md, chapter_num)

        # Read existing PTX file
        with open(ptx_path, 'r', encoding='utf-8') as f:
            ptx_content = f.read()

        # Check if homework already exists
        if f'xml:id="ch-{chapter_num:02d}-homework"' in ptx_content:
            print(f"  -> Homework section already exists, skipping")
            continue

        # Insert homework
        new_ptx = insert_homework_into_ptx(ptx_content, homework_ptx)

        # Write back
        with open(ptx_path, 'w', encoding='utf-8') as f:
            f.write(new_ptx)

        print(f"  -> Added homework section to {ptx_path}")

    print("\nDone! Run 'pretext build web' to rebuild the HTML.")


if __name__ == '__main__':
    main()
