#!/usr/bin/env python3
"""Generate EPUB from Concise Guide to English Grammar markdown chapters."""

from ebooklib import epub
import re
import os
import base64

# Book metadata
TITLE = "A Concise Guide to English Grammar"
AUTHOR = "Phillip Haisley"
LANGUAGE = "en"
IDENTIFIER = "concise-guide-english-grammar-v1"

def markdown_to_html(md_content, book, image_items):
    """Convert markdown to HTML with support for tables, lists, images."""
    html = md_content

    # Handle images first - ![alt](path)
    def replace_image(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        # Normalize path
        img_filename = os.path.basename(img_path)
        return f'<figure><img src="images/{img_filename}" alt="{alt_text}"/><figcaption>{alt_text}</figcaption></figure>'

    html = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_image, html)

    # Convert headers
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)

    # Convert horizontal rules
    html = re.sub(r'^---+$', r'<hr/>', html, flags=re.MULTILINE)

    # Convert tables
    def convert_table(match):
        table_text = match.group(0)
        lines = [l.strip() for l in table_text.strip().split('\n') if l.strip()]
        if len(lines) < 2:
            return table_text

        # Parse header row
        header_cells = [c.strip() for c in lines[0].split('|') if c.strip()]

        # Skip separator line (line with dashes)
        data_lines = [l for l in lines[2:] if not re.match(r'^[\|\-\s:]+$', l)]

        table_html = '<table>\n<thead>\n<tr>'
        for cell in header_cells:
            table_html += f'<th>{cell}</th>'
        table_html += '</tr>\n</thead>\n<tbody>\n'

        for line in data_lines:
            cells = [c.strip() for c in line.split('|') if c.strip()]
            table_html += '<tr>'
            for cell in cells:
                # Handle bold/italic in cells
                cell = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', cell)
                cell = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', cell)
                table_html += f'<td>{cell}</td>'
            table_html += '</tr>\n'

        table_html += '</tbody>\n</table>'
        return table_html

    # Match tables (lines starting/ending with |)
    html = re.sub(r'(?:^\|.+\|$\n?)+', convert_table, html, flags=re.MULTILINE)

    # Convert unordered lists
    def convert_ul(match):
        list_text = match.group(0)
        items = re.findall(r'^[\-\*]\s+(.+)$', list_text, re.MULTILINE)
        if not items:
            return list_text
        list_html = '<ul>\n'
        for item in items:
            # Handle bold/italic in items
            item = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', item)
            item = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', item)
            list_html += f'<li>{item}</li>\n'
        list_html += '</ul>'
        return list_html

    html = re.sub(r'(?:^[\-\*]\s+.+$\n?)+', convert_ul, html, flags=re.MULTILINE)

    # Convert ordered lists
    def convert_ol(match):
        list_text = match.group(0)
        items = re.findall(r'^\d+\.\s+(.+)$', list_text, re.MULTILINE)
        if not items:
            return list_text
        list_html = '<ol>\n'
        for item in items:
            item = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', item)
            item = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', item)
            list_html += f'<li>{item}</li>\n'
        list_html += '</ol>'
        return list_html

    html = re.sub(r'(?:^\d+\.\s+.+$\n?)+', convert_ol, html, flags=re.MULTILINE)

    # Convert bold (must come before italic)
    html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)

    # Convert italic
    html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html)

    # Convert checkmarks and X marks
    html = html.replace('✓', '&#10003;')
    html = html.replace('✗', '&#10007;')

    # Convert paragraphs
    paragraphs = html.split('\n\n')
    processed = []
    # Block-level tags that should NOT be wrapped in <p>
    block_tags = ['<h1', '<h2', '<h3', '<h4', '<hr', '<table', '<ul', '<ol', '<figure', '<p']
    for p in paragraphs:
        p = p.strip()
        if p and not any(p.startswith(tag) for tag in block_tags):
            # Wrap in <p> - this includes paragraphs starting with inline tags like <strong>, <em>
            p = f'<p>{p}</p>'
        processed.append(p)

    html = '\n\n'.join(processed)

    return html

def create_epub():
    """Create the EPUB file."""
    book = epub.EpubBook()

    # Set metadata
    book.set_identifier(IDENTIFIER)
    book.set_title(TITLE)
    book.set_language(LANGUAGE)
    book.add_author(AUTHOR)

    # Add CSS for textbook styling
    style = '''
    body {
        font-family: Georgia, serif;
        margin: 5%;
        line-height: 1.6;
    }
    h1 {
        text-align: center;
        margin-top: 1em;
        margin-bottom: 0.5em;
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.3em;
    }
    h2 {
        color: #2980b9;
        margin-top: 1.5em;
        border-bottom: 1px solid #bdc3c7;
        padding-bottom: 0.2em;
    }
    h3 {
        color: #34495e;
        margin-top: 1em;
    }
    h4 {
        color: #7f8c8d;
        margin-top: 0.8em;
    }
    p {
        margin: 0.8em 0;
    }
    hr {
        margin: 2em auto;
        width: 50%;
        border: none;
        border-top: 1px solid #bdc3c7;
    }
    em { font-style: italic; }
    strong { font-weight: bold; }

    table {
        border-collapse: collapse;
        margin: 1em 0;
        width: 100%;
        font-size: 0.9em;
    }
    th, td {
        border: 1px solid #bdc3c7;
        padding: 0.5em;
        text-align: left;
    }
    th {
        background-color: #ecf0f1;
        font-weight: bold;
    }
    tr:nth-child(even) {
        background-color: #f9f9f9;
    }

    ul, ol {
        margin: 0.8em 0;
        padding-left: 2em;
    }
    li {
        margin: 0.3em 0;
    }

    figure {
        text-align: center;
        margin: 1.5em 0;
    }
    figure img {
        max-width: 100%;
        height: auto;
    }
    figcaption {
        font-style: italic;
        color: #7f8c8d;
        font-size: 0.9em;
        margin-top: 0.5em;
    }

    .glossary-term {
        font-weight: bold;
        color: #2c3e50;
    }
    '''
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)

    chapters = []
    image_items = {}

    script_dir = os.path.dirname(os.path.abspath(__file__))
    chapters_dir = os.path.join(script_dir, 'chapters')

    # Image directories to search
    image_dirs = [
        os.path.join(script_dir, 'assets', 'images', 'diagrams', 'renamed'),
        os.path.join(script_dir, 'assets', 'diagrams'),  # New SVG diagrams
    ]

    # First, add all images to the book
    for images_dir in image_dirs:
        if os.path.exists(images_dir):
            for img_file in os.listdir(images_dir):
                if img_file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                    img_path = os.path.join(images_dir, img_file)
                    with open(img_path, 'rb') as f:
                        img_content = f.read()

                    # Determine media type
                    if img_file.endswith('.svg'):
                        media_type = 'image/svg+xml'
                    elif img_file.endswith('.png'):
                        media_type = 'image/png'
                    else:
                        media_type = 'image/jpeg'

                    img_item = epub.EpubItem(
                        uid=img_file.replace('.', '_').replace('-', '_'),
                        file_name=f'images/{img_file}',
                        media_type=media_type,
                        content=img_content
                    )
                    book.add_item(img_item)
                    image_items[img_file] = img_item
                    print(f"Added image: {img_file}")

    # Title page
    title_content = f'''
    <html>
    <head><title>{TITLE}</title></head>
    <body style="text-align: center;">
    <h1 style="margin-top: 20%; border: none;">{TITLE}</h1>
    <p style="font-size: 1.2em; margin-top: 2em;">{AUTHOR}</p>
    <hr style="width: 50%; margin: 2em auto;"/>
    <p style="margin-top: 2em; font-weight: bold;">Open Educational Resource (OER)</p>
    <p style="font-size: 0.9em; margin: 1em 10%;">This work is licensed under a Creative Commons Attribution 4.0 International License (CC BY 4.0). You are free to share, copy, redistribute, adapt, remix, transform, and build upon this material for any purpose, even commercially, as long as you give appropriate credit.</p>
    </body>
    </html>
    '''
    title_page = epub.EpubHtml(title='Title Page', file_name='title.xhtml', lang='en')
    title_page.content = title_content
    book.add_item(title_page)
    chapters.append(title_page)

    # Read and add each chapter
    chapter_files = sorted([f for f in os.listdir(chapters_dir) if f.startswith('chapter_') and f.endswith('.md')])

    for chapter_file in chapter_files:
        chapter_path = os.path.join(chapters_dir, chapter_file)

        with open(chapter_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Extract chapter title from first line
        lines = md_content.strip().split('\n')
        chapter_title = lines[0].replace('# ', '') if lines else chapter_file

        # Get chapter number for file naming
        match = re.search(r'chapter_(\d+)', chapter_file)
        chapter_num = match.group(1) if match else '00'

        # Convert to HTML
        html_content = markdown_to_html(md_content, book, image_items)

        # Create chapter
        chapter = epub.EpubHtml(
            title=chapter_title,
            file_name=f'chapter_{chapter_num}.xhtml',
            lang='en'
        )
        chapter.content = f'''
        <html>
        <head>
            <title>{chapter_title}</title>
            <link rel="stylesheet" href="style/nav.css" type="text/css"/>
        </head>
        <body>
        {html_content}
        </body>
        </html>
        '''
        chapter.add_item(nav_css)

        book.add_item(chapter)
        chapters.append(chapter)
        print(f"Added: {chapter_title}")

    # Create Table of Contents with parts
    # chapters[0] = Title page
    # chapters[1:7] = Ch 1-6 (Foundations)
    # chapters[7:12] = Ch 7-11 (Words and Phrases)
    # chapters[12:16] = Ch 12-15 (Sentence Structures)
    # chapters[16:22] = Ch 16-21 (The Verb System)
    # chapters[22:25] = Ch 22-24 (Advanced Structures)
    # chapters[25:27] = Ch 25-26 (Application)
    # chapters[27] = Bibliography
    book.toc = [
        (epub.Section('Title'), [chapters[0]]),
        (epub.Section('Part I: Foundations'), chapters[1:7]),
        (epub.Section('Part II: Words and Phrases'), chapters[7:12]),
        (epub.Section('Part III: Sentence Structures'), chapters[12:16]),
        (epub.Section('Part IV: The Verb System'), chapters[16:22]),
        (epub.Section('Part V: Advanced Structures'), chapters[22:25]),
        (epub.Section('Part VI: Application'), chapters[25:27]),
        (epub.Section('Back Matter'), chapters[27:]),
    ]

    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define spine
    book.spine = ['nav'] + chapters

    # Write EPUB file
    output_path = os.path.join(script_dir, 'Concise_Guide_to_English_Grammar.epub')
    epub.write_epub(output_path, book, {})
    print(f"\nEPUB created: {output_path}")
    return output_path

if __name__ == '__main__':
    create_epub()
