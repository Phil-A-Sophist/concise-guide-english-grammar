#!/usr/bin/env python3
"""
Convert the Concise Guide to English Grammar markdown chapters to PreTeXt XML format.
"""

import re
import os
from pathlib import Path


def escape_xml(text):
    """Escape special XML characters."""
    if text is None:
        return ""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def sanitize_id(text):
    """Convert text to valid XML ID."""
    sanitized = re.sub(r'[^a-zA-Z0-9\s-]', '', text.lower())
    sanitized = re.sub(r'\s+', '-', sanitized.strip())
    sanitized = re.sub(r'-+', '-', sanitized)
    return sanitized[:50] or 'untitled'


def parse_markdown_chapter(content, chapter_num):
    """Parse markdown chapter content into structured data."""
    lines = content.split('\n')

    # Extract chapter title from first line (# N. Title)
    title_match = re.match(r'^#\s*\d+\.\s*(.+)$', lines[0].strip())
    chapter_title = title_match.group(1).strip() if title_match else f"Chapter {chapter_num}"

    # Parse sections
    sections = []
    current_section = None
    current_content = []
    in_homework = False
    homework_content = []
    in_glossary = False
    glossary_content = []

    for line in lines[1:]:
        # Check for main section headers (## X.X Title)
        section_match = re.match(r'^##\s*(\d+\.\d+)\s+(.+)$', line.strip())
        homework_match = re.match(r'^##\s*Homework:', line.strip())
        glossary_match = re.match(r'^##\s*Glossary', line.strip())
        learning_obj_match = re.match(r'^##\s*Learning Objectives', line.strip())

        if homework_match:
            # Save current section
            if current_section:
                sections.append({
                    'number': current_section['number'],
                    'title': current_section['title'],
                    'content': '\n'.join(current_content).strip()
                })
            in_homework = True
            in_glossary = False
            current_section = None
            current_content = []
            continue

        if glossary_match:
            if current_section:
                sections.append({
                    'number': current_section['number'],
                    'title': current_section['title'],
                    'content': '\n'.join(current_content).strip()
                })
            in_glossary = True
            in_homework = False
            current_section = None
            current_content = []
            continue

        if in_homework:
            homework_content.append(line)
            continue

        if in_glossary:
            glossary_content.append(line)
            continue

        if learning_obj_match:
            # Save current section if any
            if current_section:
                sections.append({
                    'number': current_section['number'],
                    'title': current_section['title'],
                    'content': '\n'.join(current_content).strip()
                })
            current_section = {'number': 'objectives', 'title': 'Learning Objectives'}
            current_content = []
            continue

        if section_match:
            # Save current section
            if current_section:
                sections.append({
                    'number': current_section['number'],
                    'title': current_section['title'],
                    'content': '\n'.join(current_content).strip()
                })
            current_section = {
                'number': section_match.group(1),
                'title': section_match.group(2).strip()
            }
            current_content = []
        else:
            current_content.append(line)

    # Save final section
    if current_section:
        sections.append({
            'number': current_section['number'],
            'title': current_section['title'],
            'content': '\n'.join(current_content).strip()
        })

    return {
        'title': chapter_title,
        'sections': sections,
        'homework': '\n'.join(homework_content).strip(),
        'glossary': '\n'.join(glossary_content).strip()
    }


def convert_markdown_to_pretext_content(md_content):
    """Convert markdown content to PreTeXt XML elements."""
    if not md_content.strip():
        return ""

    result = []
    lines = md_content.split('\n')
    i = 0
    list_type = None  # None, 'ul', or 'ol'
    in_blockquote = False
    blockquote_lines = []

    def close_list():
        nonlocal list_type
        if list_type:
            result.append(f'</{list_type}>')
            result.append('')
            list_type = None

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip horizontal rules
        if stripped == '---':
            i += 1
            continue

        # Handle blockquotes
        if stripped.startswith('>'):
            close_list()
            if not in_blockquote:
                in_blockquote = True
                blockquote_lines = []
            blockquote_lines.append(stripped[1:].strip())
            i += 1
            continue
        elif in_blockquote and stripped:
            # End blockquote
            in_blockquote = False
            result.append('<blockquote>')
            for bq_line in blockquote_lines:
                if bq_line:
                    result.append(f'  <p>{escape_xml(bq_line)}</p>')
            result.append('</blockquote>')
            result.append('')
            blockquote_lines = []
        elif in_blockquote and not stripped:
            in_blockquote = False
            result.append('<blockquote>')
            for bq_line in blockquote_lines:
                if bq_line:
                    result.append(f'  <p>{escape_xml(bq_line)}</p>')
            result.append('</blockquote>')
            result.append('')
            blockquote_lines = []
            i += 1
            continue

        # Handle subsection headers (### Title)
        subsec_match = re.match(r'^###\s+(.+)$', stripped)
        if subsec_match:
            close_list()
            result.append(f'<paragraphs>')
            result.append(f'  <title>{escape_xml(subsec_match.group(1))}</title>')
            result.append('</paragraphs>')
            result.append('')
            i += 1
            continue

        # Handle unordered list items
        list_match = re.match(r'^[-*]\s+(.+)$', stripped)
        if list_match:
            # Close any existing ordered list
            if list_type == 'ol':
                close_list()
            if not list_type:
                list_type = 'ul'
                result.append('<ul>')
            item_text = process_inline_formatting(list_match.group(1))
            result.append(f'  <li><p>{item_text}</p></li>')
            i += 1
            continue

        # Handle numbered list items
        num_list_match = re.match(r'^(\d+)\.\s+(.+)$', stripped)
        if num_list_match:
            # Close any existing unordered list
            if list_type == 'ul':
                close_list()
            if not list_type:
                list_type = 'ol'
                result.append('<ol>')
            item_text = process_inline_formatting(num_list_match.group(2))
            result.append(f'  <li><p>{item_text}</p></li>')
            i += 1
            continue

        # Not a list item - close any open list
        if list_type and not stripped:
            close_list()
            i += 1
            continue
        elif list_type and stripped:
            close_list()

        # Handle regular paragraphs
        if stripped:
            para_text = process_inline_formatting(stripped)
            result.append(f'<p>{para_text}</p>')
            result.append('')

        i += 1

    # Close any open lists
    close_list()
    if in_blockquote:
        result.append('<blockquote>')
        for bq_line in blockquote_lines:
            if bq_line:
                result.append(f'  <p>{escape_xml(bq_line)}</p>')
        result.append('</blockquote>')

    return '\n'.join(result)


def process_inline_formatting(text):
    """Process inline markdown formatting to PreTeXt."""
    # Escape XML first
    text = escape_xml(text)

    # Convert bold **text** to <em>text</em> (do this first to avoid conflicts)
    text = re.sub(r'\*\*([^*]+?)\*\*', r'<em>\1</em>', text)

    # Convert italic *text* to <em>text</em> (use same tag for simplicity)
    text = re.sub(r'\*([^*]+?)\*', r'<em>\1</em>', text)

    return text


def generate_chapter_xml(chapter_num, chapter_data):
    """Generate PreTeXt XML for a chapter."""
    chapter_id = f'ch-{chapter_num:02d}-{sanitize_id(chapter_data["title"])}'

    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '',
        f'<chapter xml:id="{chapter_id}" xmlns:xi="http://www.w3.org/2001/XInclude">',
        f'  <title>{escape_xml(chapter_data["title"])}</title>',
        ''
    ]

    for section in chapter_data['sections']:
        if section['number'] == 'objectives':
            xml_parts.append(f'  <objectives>')
            xml_parts.append(f'    <title>Learning Objectives</title>')
            xml_parts.append(f'    <ul>')
            # Parse objectives list
            obj_content = section['content']
            for line in obj_content.split('\n'):
                line = line.strip()
                if line.startswith('-'):
                    obj_text = process_inline_formatting(line[1:].strip())
                    xml_parts.append(f'      <li><p>{obj_text}</p></li>')
            xml_parts.append(f'    </ul>')
            xml_parts.append(f'  </objectives>')
            xml_parts.append('')
        else:
            section_id = f'{chapter_id}-sec-{sanitize_id(section["number"])}'
            xml_parts.append(f'  <section xml:id="{section_id}">')
            xml_parts.append(f'    <title>{escape_xml(section["title"])}</title>')
            xml_parts.append('')

            # Convert section content
            converted_content = convert_markdown_to_pretext_content(section['content'])
            # Indent the content
            for line in converted_content.split('\n'):
                if line.strip():
                    xml_parts.append(f'    {line}')
                else:
                    xml_parts.append('')

            xml_parts.append('  </section>')
            xml_parts.append('')

    # Add glossary if present
    if chapter_data['glossary']:
        xml_parts.append('  <glossary>')
        xml_parts.append('    <title>Glossary</title>')
        # Parse glossary entries
        for line in chapter_data['glossary'].split('\n'):
            line = line.strip()
            if line.startswith('**') and '**:' in line:
                match = re.match(r'\*\*(.+?)\*\*:\s*(.+)', line)
                if match:
                    term = escape_xml(match.group(1))
                    definition = process_inline_formatting(match.group(2))
                    xml_parts.append(f'    <gi>')
                    xml_parts.append(f'      <title>{term}</title>')
                    xml_parts.append(f'      <p>{definition}</p>')
                    xml_parts.append(f'    </gi>')
        xml_parts.append('  </glossary>')
        xml_parts.append('')

    xml_parts.append('</chapter>')

    return '\n'.join(xml_parts)


def generate_main_ptx(chapters):
    """Generate main.ptx file."""
    chapter_includes = '\n    '.join(
        f'<xi:include href="./ch-{i:02d}.ptx" />' for i in range(1, len(chapters) + 1)
    )

    return f'''<?xml version="1.0" encoding="utf-8"?>
<pretext xml:lang="en-US" xmlns:xi="http://www.w3.org/2001/XInclude">
  <xi:include href="./docinfo.ptx" />

  <book xml:id="concise-guide-english-grammar">
    <title>A Concise Guide to English Grammar</title>

    <xi:include href="./frontmatter.ptx" />

    {chapter_includes}

    <xi:include href="./backmatter.ptx" />
  </book>
</pretext>
'''


def generate_frontmatter():
    """Generate frontmatter.ptx file."""
    return '''<?xml version="1.0" encoding="UTF-8"?>

<frontmatter xmlns:xi="http://www.w3.org/2001/XInclude" xml:id="frontmatter">
  <titlepage>
    <author>
      <personname>Dr. Irene Phipps</personname>
    </author>
    <date>
      <today />
    </date>
  </titlepage>

  <colophon>
    <copyright>
      <year>2025</year>
      <holder>Dr. Irene Phipps</holder>
      <minilicense>Creative Commons Attribution</minilicense>
    </copyright>
  </colophon>

  <preface>
    <p>
      This textbook provides a comprehensive introduction to English grammar
      from a linguistic perspective. It is designed for undergraduate students
      who want to understand how English works, not just memorize rules.
    </p>
    <p>
      The book covers foundational concepts in linguistics, the structure of
      English words and sentences, the verb system, and practical applications
      for writing and teaching.
    </p>
  </preface>
</frontmatter>
'''


def generate_backmatter():
    """Generate backmatter.ptx file."""
    return '''<?xml version="1.0" encoding="UTF-8"?>

<backmatter xmlns:xi="http://www.w3.org/2001/XInclude" xml:id="backmatter">
  <colophon>
    <p>This book was created using PreTeXt.</p>
  </colophon>
</backmatter>
'''


def generate_docinfo():
    """Generate docinfo.ptx file."""
    return '''<?xml version="1.0" encoding="UTF-8"?>

<docinfo xmlns:xi="http://www.w3.org/2001/XInclude">
  <document-id>concise-guide-english-grammar</document-id>
  <blurb shelf="Language">
    A comprehensive introduction to English grammar from a linguistic perspective.
  </blurb>
</docinfo>
'''


def main():
    # Paths
    chapters_dir = Path("Writing Projects/concise_guide_to_english_grammar/chapters")
    output_dir = Path("source")

    # Chapter files in order
    chapter_files = [
        "chapter_01_introduction_to_linguistics.md",
        "chapter_02_prescriptive_vs_descriptive.md",
        "chapter_03_language_variation.md",
        "chapter_04_morphology.md",
        "chapter_05_open_classes.md",
        "chapter_06_closed_classes.md",
        "chapter_07_sentence_diagramming.md",
        "chapter_08_sentence_elements_patterns.md",
        "chapter_09_compound_complex_sentences.md",
        "chapter_10_verbs_tense_aspect.md",
        "chapter_11_verbs_voice_modals.md",
        "chapter_12_adverbials.md",
        "chapter_13_nominals.md",
        "chapter_14_adjectivals.md",
        "chapter_15_other_grammatical_forms.md",
        "chapter_16_stylistic_choices.md",
        "chapter_17_punctuation.md",
        "chapter_18_clarity_readability.md",
        "chapter_19_organization_concision.md",
        "chapter_20_genre_register.md",
        "chapter_21_teaching_grammar.md",
    ]

    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)

    chapters_data = []

    # Process each chapter
    for i, filename in enumerate(chapter_files, 1):
        filepath = chapters_dir / filename
        print(f"Processing chapter {i}: {filename}")

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse the chapter
        chapter_data = parse_markdown_chapter(content, i)
        chapters_data.append(chapter_data)

        # Generate XML
        xml_content = generate_chapter_xml(i, chapter_data)

        # Write chapter file
        output_file = output_dir / f"ch-{i:02d}.ptx"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        print(f"  -> Written to {output_file}")

    # Generate main files
    print("\nGenerating main.ptx...")
    with open(output_dir / 'main.ptx', 'w', encoding='utf-8') as f:
        f.write(generate_main_ptx(chapters_data))

    print("Generating frontmatter.ptx...")
    with open(output_dir / 'frontmatter.ptx', 'w', encoding='utf-8') as f:
        f.write(generate_frontmatter())

    print("Generating backmatter.ptx...")
    with open(output_dir / 'backmatter.ptx', 'w', encoding='utf-8') as f:
        f.write(generate_backmatter())

    print("Generating docinfo.ptx...")
    with open(output_dir / 'docinfo.ptx', 'w', encoding='utf-8') as f:
        f.write(generate_docinfo())

    print(f"\nConversion complete! {len(chapters_data)} chapters processed.")
    print(f"Files written to {output_dir}/")


if __name__ == '__main__':
    main()
