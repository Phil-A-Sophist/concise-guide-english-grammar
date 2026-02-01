#!/usr/bin/env python3
"""
Generate Word homework documents from PreTeXt source files.
Extracts homework sections from ch-XX.ptx files and creates formatted .docx files.

Formatting requirements:
- No name/date fields (digital completion)
- Minimal space between headings and text
- Space between activities for student answers
- Match the book content
"""

import os
import re
from pathlib import Path
from lxml import etree
from docx import Document
from docx.shared import Pt, Inches, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def set_paragraph_spacing(paragraph, space_before=0, space_after=0):
    """Set paragraph spacing in points."""
    pPr = paragraph._p.get_or_add_pPr()
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:before'), str(int(space_before * 20)))  # Convert to twips
    spacing.set(qn('w:after'), str(int(space_after * 20)))
    pPr.append(spacing)


def extract_text_from_element(elem):
    """Extract text content from an XML element, handling nested elements."""
    text_parts = []

    if elem.text:
        text_parts.append(elem.text)

    for child in elem:
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag

        if tag == 'em':
            # Italic text
            text_parts.append(('italic', extract_text_from_element(child)))
        elif tag == 'term':
            # Bold text
            text_parts.append(('bold', extract_text_from_element(child)))
        elif tag == 'c':
            # Code/monospace
            text_parts.append(('code', extract_text_from_element(child)))
        elif tag == 'q':
            # Quoted text
            inner = extract_text_from_element(child)
            text_parts.append(f'"{inner}"')
        else:
            # Other elements - just get text
            text_parts.append(extract_text_from_element(child))

        if child.tail:
            text_parts.append(child.tail)

    # Flatten the list for simple text extraction
    result = []
    for part in text_parts:
        if isinstance(part, tuple):
            result.append(part[1] if isinstance(part[1], str) else ''.join(str(p) for p in part[1] if isinstance(p, str)))
        else:
            result.append(str(part))

    return ''.join(result)


def add_formatted_text(paragraph, elem):
    """Add formatted text to a paragraph, preserving italic/bold."""
    if elem.text:
        paragraph.add_run(elem.text)

    for child in elem:
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag

        if tag == 'em':
            run = paragraph.add_run(extract_text_from_element(child))
            run.italic = True
        elif tag == 'term':
            run = paragraph.add_run(extract_text_from_element(child))
            run.bold = True
        elif tag == 'c':
            run = paragraph.add_run(extract_text_from_element(child))
            run.font.name = 'Consolas'
        elif tag == 'q':
            paragraph.add_run('"')
            add_formatted_text(paragraph, child)
            paragraph.add_run('"')
        else:
            add_formatted_text(paragraph, child)

        if child.tail:
            paragraph.add_run(child.tail)


def process_homework_section(doc, section, chapter_num):
    """Process a homework section and add it to the document."""

    for elem in section:
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag

        if tag == 'title':
            # Main homework title - already handled
            continue

        elif tag == 'subsection':
            # Handle subsections (like in Chapter 4)
            process_subsection(doc, elem)

        elif tag == 'paragraphs':
            # Section heading (Part A, Part B, Instructions, etc.)
            title_elem = elem.find('.//{*}title')
            if title_elem is not None:
                title_text = extract_text_from_element(title_elem)
                para = doc.add_paragraph()
                run = para.add_run(title_text)
                run.bold = True
                run.font.size = Pt(12)
                set_paragraph_spacing(para, space_before=12, space_after=3)

        elif tag == 'p':
            # Regular paragraph or question
            text = extract_text_from_element(elem)

            # Check if it's a question/exercise
            if text.strip().startswith(('Question', 'Exercise')):
                # Add space before question
                para = doc.add_paragraph()
                add_formatted_text(para, elem)
                set_paragraph_spacing(para, space_before=6, space_after=3)

                # Add answer space
                answer_para = doc.add_paragraph()
                answer_para.add_run('[Your answer here]')
                answer_para.runs[0].font.color.rgb = None  # Default color
                answer_para.runs[0].font.italic = True
                set_paragraph_spacing(answer_para, space_before=0, space_after=12)
            else:
                para = doc.add_paragraph()
                add_formatted_text(para, elem)
                set_paragraph_spacing(para, space_before=0, space_after=3)

        elif tag == 'ul':
            # Unordered list
            for li in elem.findall('.//{*}li'):
                p_elem = li.find('.//{*}p')
                if p_elem is not None:
                    para = doc.add_paragraph(style='List Bullet')
                    add_formatted_text(para, p_elem)
                    set_paragraph_spacing(para, space_before=0, space_after=3)

                    # Check if list item expects an answer
                    text = extract_text_from_element(p_elem)
                    if text.endswith('?)') or text.endswith(':'):
                        # Add answer space for each list item
                        answer_para = doc.add_paragraph()
                        answer_para.paragraph_format.left_indent = Inches(0.5)
                        answer_para.add_run('[Answer]').italic = True
                        set_paragraph_spacing(answer_para, space_before=0, space_after=6)

        elif tag == 'ol':
            # Ordered list
            for i, li in enumerate(elem.findall('.//{*}li'), 1):
                p_elem = li.find('.//{*}p')
                if p_elem is not None:
                    para = doc.add_paragraph(style='List Number')
                    add_formatted_text(para, p_elem)
                    set_paragraph_spacing(para, space_before=0, space_after=3)

        elif tag == 'blockquote':
            # Blockquote - indent the text
            for p_elem in elem.findall('.//{*}p'):
                para = doc.add_paragraph()
                para.paragraph_format.left_indent = Inches(0.5)
                add_formatted_text(para, p_elem)
                set_paragraph_spacing(para, space_before=0, space_after=3)

        elif tag == 'tabular':
            # Table - simplified handling
            add_table(doc, elem)


def process_subsection(doc, subsection):
    """Process a homework subsection."""
    # Get subsection title
    title_elem = subsection.find('.//{*}title')
    if title_elem is not None:
        title_text = extract_text_from_element(title_elem)
        para = doc.add_heading(title_text, level=2)
        set_paragraph_spacing(para, space_before=12, space_after=6)

    for elem in subsection:
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag

        if tag == 'title':
            continue

        elif tag == 'paragraphs':
            title_elem = elem.find('.//{*}title')
            if title_elem is not None:
                title_text = extract_text_from_element(title_elem)
                para = doc.add_paragraph()
                run = para.add_run(title_text)
                run.bold = True
                set_paragraph_spacing(para, space_before=9, space_after=3)

        elif tag == 'p':
            text = extract_text_from_element(elem)
            para = doc.add_paragraph()
            add_formatted_text(para, elem)
            set_paragraph_spacing(para, space_before=0, space_after=3)

            # Add answer space for exercises
            if text.strip().startswith('Exercise'):
                answer_para = doc.add_paragraph()
                answer_para.add_run('[Your answer here]').italic = True
                set_paragraph_spacing(answer_para, space_before=0, space_after=12)

        elif tag == 'ul':
            for li in elem.findall('.//{*}li'):
                p_elem = li.find('.//{*}p')
                if p_elem is not None:
                    para = doc.add_paragraph(style='List Bullet')
                    add_formatted_text(para, p_elem)
                    set_paragraph_spacing(para, space_before=0, space_after=3)

        elif tag == 'tabular':
            add_table(doc, elem)


def add_table(doc, tabular_elem):
    """Add a table to the document."""
    rows = tabular_elem.findall('.//{*}row')
    if not rows:
        return

    # Count columns from first row
    first_row = rows[0]
    cells = first_row.findall('.//{*}cell')
    num_cols = len(cells)

    if num_cols == 0:
        return

    table = doc.add_table(rows=len(rows), cols=num_cols)
    table.style = 'Table Grid'

    for i, row in enumerate(rows):
        cells = row.findall('.//{*}cell')
        for j, cell in enumerate(cells):
            if j < num_cols:
                cell_text = extract_text_from_element(cell)
                table.rows[i].cells[j].text = cell_text

                # Bold header row
                if row.get('header') == 'yes' or i == 0:
                    for paragraph in table.rows[i].cells[j].paragraphs:
                        for run in paragraph.runs:
                            run.bold = True


def extract_homework_from_ptx(ptx_path):
    """Extract homework section from a PreTeXt file."""
    try:
        tree = etree.parse(str(ptx_path))
        root = tree.getroot()

        # Find homework section
        homework_sections = root.xpath('//*[contains(@xml:id, "homework")]',
                                       namespaces={'xml': 'http://www.w3.org/XML/1998/namespace'})

        if not homework_sections:
            # Try without namespace
            for section in root.iter():
                xml_id = section.get('{http://www.w3.org/XML/1998/namespace}id', '')
                if 'homework' in xml_id:
                    return section
        else:
            return homework_sections[0]

    except Exception as e:
        print(f"Error parsing {ptx_path}: {e}")

    return None


def get_chapter_title(ptx_path):
    """Get chapter title from PreTeXt file."""
    try:
        tree = etree.parse(str(ptx_path))
        root = tree.getroot()

        # Find chapter title
        title_elem = root.find('.//{*}chapter/{*}title')
        if title_elem is None:
            title_elem = root.find('.//{*}title')

        if title_elem is not None:
            return extract_text_from_element(title_elem)

    except Exception as e:
        print(f"Error getting title from {ptx_path}: {e}")

    return None


def get_homework_title(homework_section):
    """Get homework section title."""
    title_elem = homework_section.find('.//{*}title')
    if title_elem is not None:
        title = extract_text_from_element(title_elem)
        # Remove "Homework: " prefix if present
        if title.startswith('Homework:'):
            title = title[9:].strip()
        return title
    return None


def create_homework_document(chapter_num, chapter_title, homework_title, homework_section, output_path):
    """Create a Word document for the homework."""
    doc = Document()

    # Set up document styles
    style = doc.styles['Normal']
    style.font.name = 'Garamond'
    style.font.size = Pt(11)

    # Set up heading styles
    for i in range(1, 4):
        heading_style = doc.styles[f'Heading {i}']
        heading_style.font.name = 'Open Sans'
        heading_style.font.bold = True

    # Add title
    title = doc.add_heading(f'Chapter {chapter_num}: {chapter_title}', level=1)
    title.runs[0].font.size = Pt(16)
    set_paragraph_spacing(title, space_before=0, space_after=6)

    # Add homework subtitle
    if homework_title:
        subtitle = doc.add_heading(f'Homework: {homework_title}', level=2)
        subtitle.runs[0].font.size = Pt(14)
        set_paragraph_spacing(subtitle, space_before=0, space_after=12)

    # Process homework content
    process_homework_section(doc, homework_section, chapter_num)

    # Save document
    doc.save(str(output_path))
    print(f"Created: {output_path}")


def main():
    # Paths
    script_dir = Path(__file__).parent
    pretext_source = script_dir.parent / 'pretext' / 'source'
    output_dir = script_dir

    # Process each chapter
    for chapter_num in range(1, 22):
        ptx_file = pretext_source / f'ch-{chapter_num:02d}.ptx'

        if not ptx_file.exists():
            print(f"Chapter {chapter_num} file not found: {ptx_file}")
            continue

        print(f"\nProcessing Chapter {chapter_num}...")

        # Get chapter title
        chapter_title = get_chapter_title(ptx_file)
        if not chapter_title:
            print(f"  Could not get chapter title")
            continue

        # Extract homework section
        homework_section = extract_homework_from_ptx(ptx_file)
        if homework_section is None:
            print(f"  No homework section found")
            continue

        # Get homework title
        homework_title = get_homework_title(homework_section)

        # Create output filename
        output_file = output_dir / f'Chapter {chapter_num:02d} Homework.docx'

        # Create document
        create_homework_document(
            chapter_num,
            chapter_title,
            homework_title,
            homework_section,
            output_file
        )

    print("\nDone!")


if __name__ == '__main__':
    main()
