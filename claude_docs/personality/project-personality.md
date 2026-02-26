# Project Personality: concise-guide-english-grammar

---

## Project Context

# Project Context: A Concise Guide to English Grammar

## Purpose
Open Educational Resource (OER) college textbook for undergraduate English grammar courses. 21 chapters organized thematically: Foundations, Core Grammar, The Verb System, Form and Function, Writing and Style, Applied Grammar. Published to GitHub Pages and EPUB.

## Tech Stack
- PreTeXt XML (single source of truth in pretext/)
- Python build script (build.py) — builds HTML + EPUB with CSS injection
- Pandoc (EPUB generation)
- GitHub Pages deployment (docs/ folder)

## Key Files
- `pretext/` — Source .ptx files (chapters, front matter, back matter)
- `build.py` — Custom build script for HTML and EPUB
- `project.ptx` — PreTeXt project configuration
- `docs/` — HTML output for GitHub Pages
- `epub/` — EPUB output
- `assets/` — Images and diagrams
- `Homework/` — Word files for students
- `reference_materials/` — Style guides, outlines, instructor materials
- `README.md` — 180+ line documentation (chapter list, build instructions, homework workflow)

## Commands
- `python build.py` — Build HTML and EPUB
- `pretext build` — Alternative PreTeXt build
- Published at: https://phil-a-sophist.github.io/concise-guide-english-grammar/

## Status
Published and in use. 21 chapters complete.

## Gotchas
- pretext/ folder is the single source of truth — don't edit docs/ or epub/ directly
- build.py injects custom CSS during EPUB generation
- Homework files are Word format (.docx) for student distribution

---

## Always / Never

**Always:**
- Follow project conventions established in existing code
- Update project-map.md when adding new files
- Embed metadata into files after generating/modifying them

**Never:**
- Modify files outside the project directory without asking
- Skip memory consolidation at session start

**When in doubt:**
- Check project-map.md for file structure
- Check knowledge-base.md for past decisions

---

## Key Gotchas

See "Gotchas" section in Project Context above.
