#!/usr/bin/env python3
"""
Build script for Concise Guide to English Grammar.

Usage:
    python build.py           # Build both HTML and EPUB
    python build.py html      # Build HTML only
    python build.py epub      # Build EPUB only
"""

import subprocess
import shutil
import sys
import os
from pathlib import Path

# Paths
ROOT = Path(__file__).parent
OUTPUT_WEB = ROOT / "pretext" / "output" / "web"
DOCS_DIR = ROOT / "docs"
EPUB_DIR = ROOT / "epub"
PANDOC_PATH = Path(os.environ.get("LOCALAPPDATA", "")) / "Pandoc" / "pandoc.exe"

# Book metadata for EPUB
METADATA = {
    "title": "A Concise Guide to English Grammar",
    "author": "Phil A. Sophist",
    "language": "en-US",
}

# Chapter order for EPUB
CHAPTERS = [
    "frontmatter.html",
    "ch-01-introduction-to-linguistics-and-grammar.html",
    "ch-02-prescriptive-vs-descriptive-grammar.html",
    "ch-03-language-varieties.html",
    "ch-04-morphology-and-word-structure.html",
    "ch-05-open-classes.html",
    "ch-06-closed-classes.html",
    "ch-07-introduction-to-sentence-diagramming.html",
    "ch-08-basic-sentence-elements-and-sentence-patterns.html",
    "ch-09-compound-and-complex-sentences.html",
    "ch-10-verbs-part-one-tense-and-aspect.html",
    "ch-11-verbs-part-two-voice-and-modals.html",
    "ch-12-adverbials.html",
    "ch-13-nominals.html",
    "ch-14-adjectivals.html",
    "ch-15-punctuation.html",
    "ch-16-other-grammatical-forms.html",
    "ch-17-stylistic-choices.html",
    "ch-18-clarity-and-readability.html",
    "ch-19-organization-and-concision.html",
    "ch-20-genre-and-register.html",
    "ch-21-teaching-grammar.html",
    "backmatter.html",
]


def build_html():
    """Build HTML using PreTeXt."""
    print("Building HTML with PreTeXt...")
    result = subprocess.run(
        ["pretext", "build", "web"],
        cwd=ROOT,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"PreTeXt build failed:\n{result.stderr}")
        return False

    # Copy output to docs/ for GitHub Pages
    print("Copying to docs/ for GitHub Pages...")
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    shutil.copytree(OUTPUT_WEB, DOCS_DIR)

    # Add .nojekyll file for GitHub Pages (allows _static folder)
    (DOCS_DIR / ".nojekyll").touch()

    # Add custom CSS overrides
    apply_custom_css()

    print("HTML build complete!")
    return True


# Custom CSS to inject into HTML files
CUSTOM_CSS = """
/* Custom CSS for Concise Guide to English Grammar */

/* Typography: Sans-serif headings, Georgia body text */
:root {
    --font-headings: "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif !important;
    --font-body: Georgia, "Times New Roman", Times, serif !important;
}

/* Apply sans-serif to headings and table headers - BOLD BLACK */
h1, h2, .ptx-content h1, .ptx-content h2,
.heading .title, section > .heading > .title,
table th, .tabular-box th {
    font-family: "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif !important;
    font-weight: 700 !important;
    color: #000000 !important;
}

/* Apply sans-serif to navigation elements: TOC, navbar, dropdowns */
.ptx-toc, .ptx-toc a, .ptx-toc .toc-item,
.ptx-navbar, .ptx-navbar a,
.toc-title-line, .codenumber, .title,
.dropdown, .dropdown-menu, .dropdown a,
.searchbox, .searchbox input,
.ptx-sidebar, .ptx-sidebar a,
nav, nav a,
.toc-chapter, .toc-section,
.ptx-page-footer, .ptx-content-footer a {
    font-family: "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif !important;
}

/* Apply Georgia to body text with increased size (+3pt from default) */
.ptx-content, .ptx-content p, .ptx-content li,
.ptx-main .ptx-content {
    font-family: Georgia, "Times New Roman", Times, serif !important;
    font-size: 1.1875rem !important;  /* 19px instead of 16px default */
    line-height: 1.6 !important;
}

/* Widen the main content area for better readability on larger screens */
.ptx-main .ptx-content {
    max-width: 900px !important;
}
.ptx-content-footer {
    max-width: 900px !important;
}

/* Consistent table alignment - all tables left-aligned */
.tabular-box {
    margin-left: 0 !important;
    margin-right: auto !important;
}

.tabular-box.natural-width {
    margin-left: 0 !important;
    margin-right: auto !important;
}

.tabular-box.natural-width table {
    margin-left: 0 !important;
    margin-right: auto !important;
}

/* Ensure tables inside paragraphs sections are also left-aligned */
.paragraphs .tabular-box,
section .tabular-box {
    margin-left: 0 !important;
}

/* === Diagram Examples pages (dedicated reference sections) === */
/* Labels: bold black, normal size, above the diagram */
[id*="diagrams-"] .paragraphs .heading .title {
    font-size: 1em !important;
    font-weight: 700 !important;
    color: #000000 !important;
    margin-top: 1.5em !important;
    margin-bottom: 0.4em !important;
}

/* Images: left-aligned */
[id*="diagrams-"] .image-box {
    margin-left: 0 !important;
    margin-right: auto !important;
}

/* Bracket notation: left-aligned, tighter spacing below image */
[id*="diagrams-"] .para:has(.code-inline) {
    text-align: left !important;
    margin-top: 0.25em !important;
    margin-bottom: 0.25em !important;
}

/* === Inline diagrams (future use, outside diagram-examples sections) === */
/* Images: left-aligned */
.ptx-content .image-box {
    margin-left: 0 !important;
    margin-right: auto !important;
}

/* Bracket notation: left-aligned */
.ptx-content .para:has(.code-inline) {
    text-align: left !important;
}

/* Figure captions: small, not bold, left-aligned */
.ptx-content figcaption {
    font-size: 9pt !important;
    font-weight: normal !important;
    text-align: left !important;
    font-family: "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif !important;
    margin-top: 0.3em !important;
}

/* Keep figure images left-aligned (not centered) */
.ptx-content .figure-like .image-box {
    margin-left: 0 !important;
    margin-right: auto !important;
}

/* Hide the page footer with PreTeXt/Runestone/MathJax links */
#ptx-page-footer {
    display: none !important;
}

/* ===== Language Example Styling ===== */

/* Language examples (<foreign> element): sans-serif at body text size */
.ptx-content .foreign,
.ptx-content i.foreign {
    font-family: "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif !important;
    font-style: normal !important;
    font-size: inherit !important;
}

/* Broken-out example lists: light grey background with indentation */
.ptx-content ul:has(> li .foreign),
.ptx-content ol:has(> li .foreign) {
    background-color: #f5f6f8 !important;
    padding: 0.6em 1.5em !important;
    border-radius: 5px !important;
    margin-left: 1em !important;
    border-left: 3px solid #e2e4e8 !important;
}

/* Tables containing language examples: light grey background */
.ptx-content .tabular-box:has(.foreign) {
    background-color: #f5f6f8 !important;
    padding: 0.5em 0.75em !important;
    border-radius: 5px !important;
    margin-left: 1em !important;
    border-left: 3px solid #e2e4e8 !important;
}

/* Inline quotation marks around sentence examples: sans-serif */
.ptx-content q {
    font-family: "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif !important;
    font-size: inherit !important;
}
"""


def apply_custom_css():
    """Inject custom CSS into all HTML files."""
    style_tag = f"<style>{CUSTOM_CSS}</style>\n</head>"
    count = 0
    for html_file in DOCS_DIR.glob("*.html"):
        content = html_file.read_text(encoding="utf-8")
        if "</head>" in content and "/* Custom CSS for Concise Guide" not in content:
            content = content.replace("</head>", style_tag)
            html_file.write_text(content, encoding="utf-8")
            count += 1
    print(f"Injected custom CSS into {count} HTML files.")


def find_section_files(chapter_base: str) -> list[str]:
    """Find all section files for a chapter."""
    base = chapter_base.replace(".html", "")
    section_files = []
    for f in sorted(DOCS_DIR.glob(f"{base}-sec-*.html")):
        section_files.append(f.name)
    return section_files


def build_epub():
    """Build EPUB from HTML using Pandoc."""
    print("Building EPUB with Pandoc...")

    if not DOCS_DIR.exists():
        print("Error: docs/ folder not found. Run 'python build.py html' first.")
        return False

    # Build file list
    html_files = []
    for chapter in CHAPTERS:
        chapter_path = DOCS_DIR / chapter
        if chapter_path.exists():
            html_files.append(chapter_path)
            for section in find_section_files(chapter):
                section_path = DOCS_DIR / section
                if section_path.exists():
                    html_files.append(section_path)

    if not html_files:
        print("Error: No HTML files found!")
        return False

    print(f"Processing {len(html_files)} HTML files...")

    # Ensure epub directory exists
    EPUB_DIR.mkdir(exist_ok=True)
    output_file = EPUB_DIR / "Concise_Guide_to_English_Grammar.epub"

    # Build Pandoc command
    cmd = [
        str(PANDOC_PATH),
        "-f", "html",
        "-t", "epub",
        "-o", str(output_file),
        f"--metadata=title:{METADATA['title']}",
        f"--metadata=author:{METADATA['author']}",
        f"--metadata=lang:{METADATA['language']}",
        "--toc",
        "--toc-depth=2",
    ]
    cmd.extend(str(f) for f in html_files)

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=DOCS_DIR)

    if result.returncode != 0:
        print(f"Pandoc failed:\n{result.stderr}")
        return False

    size_kb = output_file.stat().st_size / 1024
    print(f"EPUB build complete: {output_file.name} ({size_kb:.1f} KB)")
    return True


def main():
    args = sys.argv[1:]

    if not args or "html" in args:
        if not build_html():
            sys.exit(1)

    if not args or "epub" in args:
        if not build_epub():
            sys.exit(1)

    print("\nBuild complete!")
    print(f"  HTML: {DOCS_DIR}/")
    print(f"  EPUB: {EPUB_DIR}/Concise_Guide_to_English_Grammar.epub")


if __name__ == "__main__":
    main()
