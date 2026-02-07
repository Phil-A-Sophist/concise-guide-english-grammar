# Project Map

Last updated: 2026-02-07
Task: 0

## Root Directory

- `CLAUDE.md` — AI assistant project configuration and instructions
- `README.md` — Project overview, build instructions, chapter listing
- `build.py` — Build script: runs PreTeXt for HTML, Pandoc for EPUB, injects custom CSS
- `project.ptx` — PreTeXt project configuration file
- `requirements.txt` — Python dependencies (PreTeXt 2.36.0)

## pretext/source/ — PreTeXt XML Source Files (Single Source of Truth)

- `pretext/source/main.ptx` — Root document that includes all chapters
- `pretext/source/docinfo.ptx` — Document metadata and configuration
- `pretext/source/frontmatter.ptx` — Title page, preface, front matter
- `pretext/source/backmatter.ptx` — Back matter content
- `pretext/source/ch-01.ptx` — Chapter 1: Introduction to Linguistics and Grammar
- `pretext/source/ch-01-sample.ptx` — Sample/alternate version of Chapter 1
- `pretext/source/ch-02.ptx` — Chapter 2: Prescriptive vs. Descriptive Grammar
- `pretext/source/ch-03.ptx` — Chapter 3: Language Varieties
- `pretext/source/ch-04.ptx` — Chapter 4: Morphology and Word Structure
- `pretext/source/ch-05.ptx` — Chapter 5: Open Classes
- `pretext/source/ch-06.ptx` — Chapter 6: Closed Classes
- `pretext/source/ch-07.ptx` — Chapter 7: Introduction to Sentence Diagramming
- `pretext/source/ch-08.ptx` — Chapter 8: Basic Sentence Elements and Sentence Patterns
- `pretext/source/ch-09.ptx` — Chapter 9: Compound and Complex Sentences
- `pretext/source/ch-10.ptx` — Chapter 10: Verbs Part One: Tense and Aspect
- `pretext/source/ch-11.ptx` — Chapter 11: Verbs Part Two: Voice and Modals
- `pretext/source/ch-12.ptx` — Chapter 12: Adverbials
- `pretext/source/ch-13.ptx` — Chapter 13: Nominals
- `pretext/source/ch-14.ptx` — Chapter 14: Adjectivals
- `pretext/source/ch-15.ptx` — Chapter 15: Punctuation
- `pretext/source/ch-16.ptx` — Chapter 16: Other Grammatical Forms
- `pretext/source/ch-17.ptx` — Chapter 17: Stylistic Choices
- `pretext/source/ch-18.ptx` — Chapter 18: Clarity and Readability
- `pretext/source/ch-19.ptx` — Chapter 19: Organization and Concision
- `pretext/source/ch-20.ptx` — Chapter 20: Genre and Register
- `pretext/source/ch-21.ptx` — Chapter 21: Teaching Grammar

## pretext/config/

- `pretext/config/publication.ptx` — PreTeXt publication configuration (output settings)

## docs/ — HTML Output (GitHub Pages)

- Generated HTML files for all chapters and sections
- `docs/external/diagrams/` — SVG diagrams copied from assets for web display
- `docs/.nojekyll` — Marker file for GitHub Pages (allows _static folder)

## epub/

- `epub/Concise_Guide_to_English_Grammar.epub` — Generated EPUB ebook

## assets/diagrams/ — SVG Diagram Source Files

- 60+ SVG files for syntax tree diagrams organized by chapter (ch04-ch16)
- Covers morpheme trees, phrase structures (NP, VP, AdjP, AdvP, PP), sentence patterns, and verb auxiliaries
- `assets/diagrams/manifest.txt` — Manifest listing diagram files
- `assets/diagrams/new/` — PNG diagram images (110+ files, ch05-ch16) with bracket notation reference

## assets/images/diagrams/ — Extracted Source Images

- Original images extracted from PowerPoint lecture slides (F25 series)
- Organized by lecture week/day (W1D1, W6D1, W6D2, W8D1, W8D2, W11D1, etc.)
- `assets/images/diagrams/renamed/` — Renamed versions of extracted images

## Homework/

- `Homework/Chapter 01 Homework.docx` through `Chapter 21 Homework.docx` — Student homework files (Word format)
- `Homework/Chapter 04 Answer Key.docx` through `Chapter 15 Answer Key.docx` — Answer keys (Chapters 4-15)
- `Homework/generate_homework_from_pretext.py` — Script to generate Word homework files from PreTeXt source

## scripts/

- `scripts/generate_diagrams.py` — SVG diagram generation script
- `scripts/generate_new_diagrams.py` — Updated/new diagram generation script

## reference_materials/

- `reference_materials/STYLE_GUIDE.md` — Writing conventions, formatting standards, PreTeXt patterns
- `reference_materials/REVISION_AUDIT.md` — Chapter-by-chapter quality assessment and revision priorities
- `reference_materials/series_bible.md` — Pedagogical approach, chapter features, target outcomes
- `reference_materials/outlines.md` — Chapter outlines
- `reference_materials/image_inventory.md` — Extracted images list
- `reference_materials/image_inventory_detailed.md` — Image-to-chapter mapping
- `reference_materials/diagram_bracket_notation.md` — Bracket notation reference for diagrams
- `reference_materials/diagram_examples_by_chapter.md` — Diagram examples organized by chapter
- `reference_materials/PPTs/` — Instructor PowerPoint presentations (source material)
- `reference_materials/Other Class Materials/` — Handouts and tests
- `reference_materials/Grammar Textbooks/` — Reference textbook materials

## logs/

- Build log files (dated 2026-01-29 through 2026-02-06)

## generated-assets/

- Empty directory (likely for PreTeXt-generated assets)
