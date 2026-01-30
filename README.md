# A Concise Guide to English Grammar

An open educational resource (OER) textbook for undergraduate English grammar courses.

**[Read Online](https://phil-a-sophist.github.io/concise-guide-english-grammar/)**

---

## Project Overview

- **Type:** Open educational resource (OER) college textbook
- **Subject:** English grammar for undergraduate students
- **Structure:** 21 chapters organized thematically
- **Source format:** PreTeXt XML
- **Output formats:** HTML (GitHub Pages), EPUB

---

## Project Structure

```
concise-guide-english-grammar/
├── pretext/
│   ├── source/           # PreTeXt .ptx files (single source of truth)
│   ├── config/           # publication.ptx configuration
│   └── output/           # Temporary build output (gitignored)
├── docs/                 # HTML output for GitHub Pages
├── epub/                 # EPUB output
├── assets/               # Images and diagrams
├── Homework/             # Word files for student download
├── reference_materials/  # Style guides, outlines, instructor materials
├── scripts/              # Utility scripts
├── build.py              # Build script
├── project.ptx           # PreTeXt project configuration
├── CLAUDE.md             # AI assistant instructions
└── README.md             # This file
```

---

## Building the Book

### Prerequisites

- Python 3.x
- PreTeXt CLI (`pip install pretext`)
- Node.js (required by PreTeXt)
- Pandoc (for EPUB generation)

### Build Commands

Run from the repository root:

```bash
python build.py           # Build both HTML and EPUB
python build.py html      # Build HTML only
python build.py epub      # Build EPUB only
```

### What the Build Does

1. **HTML Build:**
   - Runs `pretext build web`
   - Copies output to `docs/` for GitHub Pages
   - Creates `.nojekyll` file (required for GitHub Pages)
   - Applies custom CSS (wider content, consistent table alignment)

2. **EPUB Build:**
   - Converts HTML from `docs/` to EPUB using Pandoc
   - Outputs to `epub/Concise_Guide_to_English_Grammar.epub`

### Custom CSS

The build script appends custom CSS to override PreTeXt defaults:
- Content area widened to 900px (from 696px) for better readability
- All tables consistently left-aligned

To modify, edit the `CUSTOM_CSS` constant in `build.py`.

### Output Locations

| Format | Location | Purpose |
|--------|----------|---------|
| HTML | `docs/` | GitHub Pages hosting |
| EPUB | `epub/Concise_Guide_to_English_Grammar.epub` | Downloadable ebook |

### Homework Workflow

When homework sections are created or updated in PreTeXt:
1. Build the HTML version
2. Create a corresponding Word (.docx) file in `Homework/`
3. Format the Word file for digital completion (with space for students to type answers)
4. Name files: `ch-XX-homework.docx` and `ch-XX-answer-key.docx`

### Commit and Push

All builds should end with committing and pushing all changes to GitHub. This updates the live GitHub Pages site.

---

## Editing Content

### Source of Truth

**PreTeXt XML files** in `pretext/source/` are the single source of truth.
- Do NOT edit HTML files directly (they are generated)
- Edit `.ptx` files, then rebuild

### To Edit a Chapter

1. Open the relevant file in `pretext/source/` (e.g., `ch-01.ptx`)
2. Make changes using PreTeXt XML syntax
3. Run `python build.py` to rebuild
4. Verify output in browser and/or EPUB reader

---

## Chapter Organization (21 Chapters)

### Foundations (Chapters 1-4)
1. Introduction to Linguistics and Grammar
2. Prescriptive vs. Descriptive Grammar
3. Language Varieties
4. Morphology and Word Structure

### Core Grammar (Chapters 5-9)
5. Open Classes
6. Closed Classes
7. Introduction to Sentence Diagramming
8. Basic Sentence Elements and Sentence Patterns
9. Compound and Complex Sentences

### The Verb System (Chapters 10-11)
10. Verbs Part One: Tense and Aspect
11. Verbs Part Two: Voice and Modals

### Form and Function (Chapters 12-15)
12. Adverbials
13. Nominals
14. Adjectivals
15. Punctuation

### Writing and Style (Chapters 16-19)
16. Other Grammatical Forms
17. Stylistic Choices
18. Clarity and Readability
19. Organization and Concision

### Applied Grammar (Chapters 20-21)
20. Genre and Register
21. Teaching Grammar

---

## Reference Materials

Located in `reference_materials/`:
- `STYLE_GUIDE.md` - Writing and formatting conventions
- `outlines.md` - Chapter outlines
- `series_bible.md` - Pedagogical approach
- `REVISION_AUDIT.md` - Chapter quality assessment
- `PPTs/` - Instructor PowerPoint presentations

---

## For AI Assistants

See `CLAUDE.md` for project-specific instructions, including:
- Build workflow details
- Style guide requirements
- PreTeXt editing basics
- Post-build cleanup checklist

---

## License

This is an Open Educational Resource (OER). See license details in the book's front matter.
