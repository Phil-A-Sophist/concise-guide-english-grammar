# Project Map

Last updated: 2026-02-15
Task: 37

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
- `pretext/source/ch-13.ptx` — Chapter 13: Adjectivals
- `pretext/source/ch-14.ptx` — Chapter 14: Nominals
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
- `assets/diagrams/new/` — PNG diagram images (120+ files, ch05-ch16, includes 10 ch07 files) with bracket notation reference

## assets/images/diagrams/ — Extracted Source Images

- Original images extracted from PowerPoint lecture slides (F25 series)
- Organized by lecture week/day (W1D1, W6D1, W6D2, W8D1, W8D2, W11D1, etc.)
- `assets/images/diagrams/renamed/` — Renamed versions of extracted images

## Homework/

- `Homework/Chapter 01 Homework.docx` through `Chapter 21 Homework.docx` — Student homework files (Word format)
- `Homework/Chapter 04 Answer Key.docx` through `Chapter 16 Answer Key.docx` — Answer keys (Chapters 4-16)
- `Homework/Chapter 18 Answer Key.docx` — Answer key (Chapter 18; no Ch17 answer key yet)
- `Homework/Homework 04 Overhead.docx`, `Homework/Homework 05 Overhead.docx` — Classroom overheads (Chapters 4-5)
- `Homework/Homework 07 Overhead.docx` through `Homework/Homework 16 Overhead.docx` — Classroom overheads (Chapters 7-16, 22pt projection format)
- `Homework/Homework 18 Overhead.docx` — Classroom overhead for Chapter 18 (no Ch06, Ch17 overheads yet)
- `Homework/generate_homework_from_pretext.py` — Script to generate Word homework files from PreTeXt source
- `Homework/generate_hw_diagrams.py` — Generates SyntaxTreeHybrid diagram PNGs for practice assignments via Playwright
- `Homework/diagrams/` — Generated diagram PNGs for SyntaxTreeHybrid practice assignment
- `Homework/SyntaxTreeHybrid Instructions.md` — Student instructions for using SyntaxTreeHybrid tool
- `Homework/SyntaxTreeHybrid Instructions.docx` — Word version of SyntaxTreeHybrid instructions
- `Homework/SyntaxTreeHybrid Practice Assignment.md` — Practice assignment for SyntaxTreeHybrid
- `Homework/SyntaxTreeHybrid Practice Assignment.docx` — Word version of practice assignment
- `Homework/SyntaxTreeHybrid Answer Key.md` — Answer key for SyntaxTreeHybrid practice
- `Homework/SyntaxTreeHybrid Answer Key.docx` — Word version of answer key

## Homework/Exams/

- `Homework/Exams/ENGL 3110 - S26 - Exam One.md` — Student exam (Markdown source)
- `Homework/Exams/ENGL 3110 - S26 - Exam One.docx` — Student exam (Word format)
- `Homework/Exams/ENGL 3110 - S26 - Exam One - Answer Key.md` — Answer key (Markdown source, with diagram references)
- `Homework/Exams/ENGL 3110 - S26 - Exam One - Answer Key.docx` — Answer key (Word format, with embedded diagrams)
- `Homework/Exams/ENGL 3110 - S26 - Exam One Study Guide.md` — Study guide (Markdown source)
- `Homework/Exams/ENGL 3110 - S26 - Exam One Study Guide.docx` — Study guide (Word format)
- `Homework/Exams/ENGL 3110 - S26 - Exam One Study Guide - Answer Key.md` — Study guide answer key (Markdown source)
- `Homework/Exams/ENGL 3110 - S26 - Exam One Study Guide - Answer Key.docx` — Study guide answer key (Word format)
- `Homework/Exams/generate_exam_diagrams.py` — Generates SyntaxTreeHybrid diagram PNGs for exam answer key via Playwright
- `Homework/Exams/generate_exam_docx.py` — Generates both exam and answer key .docx files with embedded diagrams
- `Homework/Exams/generate_study_guide_diagrams.py` — Generates SyntaxTreeHybrid diagram PNGs for study guide via Playwright
- `Homework/Exams/generate_study_guide_docx.py` — Generates study guide and study guide answer key .docx files
- `Homework/Exams/diagrams/` — 11 generated diagram PNGs (1 exam example + 5 exam answer key diagrams + 5 study guide answer key diagrams: sg_q14-sg_q18)

## scripts/

- `scripts/generate_diagrams.py` — SVG diagram generation script
- `scripts/generate_new_diagrams.py` — Updated/new diagram generation script
- `scripts/generate_ch07_answer_key.py` through `scripts/generate_ch16_answer_key.py` — Answer key and overhead .docx generators (Chapters 7-16)
- `scripts/generate_ch18_answer_key.py` — Answer key and overhead .docx generator (Chapter 18; no Ch17 script yet)
- `scripts/fix_nested_em.py` — Utility script to fix nested `<em><em>` patterns in PreTeXt source
- `scripts/process_chapters.py` — Batch chapter processing utility
- `scripts/remove_example_italics.py` — Script to remove italics from language examples (v1)
- `scripts/remove_example_italics_v2.py` — Updated script to remove italics from language examples (v2)

## reference_materials/

- `reference_materials/STYLE_GUIDE.md` — Writing conventions, formatting standards, PreTeXt patterns
- `reference_materials/REVISION_AUDIT.md` — Chapter-by-chapter quality assessment and revision priorities
- `reference_materials/series_bible.md` — Pedagogical approach, chapter features, target outcomes
- `reference_materials/outlines.md` — Chapter outlines
- `reference_materials/image_inventory.md` — Extracted images list
- `reference_materials/image_inventory_detailed.md` — Image-to-chapter mapping
- `reference_materials/diagram_bracket_notation.md` — Bracket notation reference for diagrams
- `reference_materials/diagram_examples_by_chapter.md` — Diagram examples organized by chapter
- `reference_materials/bracket_notations.txt` — Bracket notation entries for all chapter diagrams (updated with ch07 entries in Task 16)
- `reference_materials/PPTs/` — Instructor PowerPoint presentations (source material)
- `reference_materials/Other Class Materials/` — Handouts and tests
- `reference_materials/Grammar Textbooks/` — Reference textbook materials

## .claude/

- `.claude/commands/memory-check.md` — Custom slash command: memory health check
- `.claude/commands/memory-status.md` — Custom slash command: memory status display
- `.claude/skills/memory-system/SKILL.md` — Memory system skill definition
- `.claude/settings.local.json` — Claude Code local permission settings

## .memory/

- `.memory/state.md` — Current compressed project state (rewritten every cycle)
- `.memory/project-map.md` — Index of project files and artifacts
- `.memory/knowledge-base.md` — Decisions, solutions, and hard-won knowledge by topic
- `.memory/chapter-improvement-process.md` — Step-by-step process for systematic chapter improvements (diagrams, formatting, homework, Word files)
- `.memory/state-t20.md` — State snapshot at Task 20
- `.memory/state-t30.md` — State snapshot at Task 30
- `.memory/reference/project-context.md` — Project context extracted from CLAUDE.md during v3 deployment

## logs/

- Build log files (dated 2026-01-29 through 2026-02-06)

## generated-assets/

- Empty directory (likely for PreTeXt-generated assets)
