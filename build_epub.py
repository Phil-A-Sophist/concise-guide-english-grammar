#!/usr/bin/env python3
"""
Build EPUB from PreTeXt HTML output using Pandoc.

Workflow: PreTeXt → HTML → EPUB
"""

import subprocess
import os
from pathlib import Path

# Configuration
DOCS_DIR = Path(__file__).parent / "docs"
OUTPUT_FILE = Path(__file__).parent / "output" / "Concise_Guide_to_English_Grammar.epub"
PANDOC_PATH = Path(os.environ.get("LOCALAPPDATA", "")) / "Pandoc" / "pandoc.exe"

# Book metadata
METADATA = {
    "title": "A Concise Guide to English Grammar",
    "author": "Phil A. Sophist",
    "language": "en-US",
}

# Chapter order (main chapter files only, in order)
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


def find_section_files(chapter_base: str) -> list[str]:
    """Find all section files for a chapter."""
    # Pattern: ch-XX-name-sec-XXX.html
    base = chapter_base.replace(".html", "")
    section_files = []

    for f in sorted(DOCS_DIR.glob(f"{base}-sec-*.html")):
        section_files.append(f.name)

    return section_files


def build_file_list() -> list[Path]:
    """Build the complete list of HTML files in order."""
    files = []

    for chapter in CHAPTERS:
        chapter_path = DOCS_DIR / chapter
        if chapter_path.exists():
            files.append(chapter_path)

            # Add section files for this chapter
            for section in find_section_files(chapter):
                section_path = DOCS_DIR / section
                if section_path.exists():
                    files.append(section_path)

    return files


def build_epub():
    """Build EPUB using Pandoc."""
    # Ensure output directory exists
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Get file list
    html_files = build_file_list()

    if not html_files:
        print("Error: No HTML files found!")
        return False

    print(f"Found {len(html_files)} HTML files to process")

    # Build Pandoc command
    cmd = [
        str(PANDOC_PATH),
        "-f", "html",
        "-t", "epub",
        "-o", str(OUTPUT_FILE),
        f"--metadata=title:{METADATA['title']}",
        f"--metadata=author:{METADATA['author']}",
        f"--metadata=lang:{METADATA['language']}",
        "--toc",
        "--toc-depth=2",
    ]

    # Add all HTML files
    cmd.extend(str(f) for f in html_files)

    print(f"Running Pandoc...")
    print(f"Output: {OUTPUT_FILE}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=DOCS_DIR)

        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False

        if OUTPUT_FILE.exists():
            size_kb = OUTPUT_FILE.stat().st_size / 1024
            print(f"Success! EPUB created: {size_kb:.1f} KB")
            return True
        else:
            print("Error: EPUB file was not created")
            return False

    except Exception as e:
        print(f"Error running Pandoc: {e}")
        return False


if __name__ == "__main__":
    build_epub()
