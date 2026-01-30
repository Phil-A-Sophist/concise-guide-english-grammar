# Claude Code Project Configuration

## Concise Guide to English Grammar

This file contains project-specific instructions for Claude Code sessions.

---

## Project Overview

- **Type:** Open educational resource (OER) college textbook
- **Subject:** English grammar for undergraduate students
- **Structure:** 21 chapters organized thematically
- **Source format:** PreTeXt XML (single source of truth)
- **Output formats:** HTML (GitHub Pages), EPUB

---

## Project Structure

```
concise-guide-english-grammar/
├── pretext/
│   ├── source/       # PreTeXt .ptx files (EDIT HERE)
│   ├── config/       # publication.ptx
│   └── output/       # Temporary build output (gitignored)
├── docs/             # HTML output for GitHub Pages
├── epub/             # EPUB output
├── assets/           # Images and diagrams
├── Homework/         # Word files for student download
├── reference_materials/  # Style guides, outlines, instructor materials
├── scripts/          # Utility scripts
├── build.py          # Build script
└── project.ptx       # PreTeXt project configuration
```

---

## Style Guide

**IMPORTANT:** When editing any content, always reference `reference_materials/STYLE_GUIDE.md` for:
- Writing conventions and tone
- Formatting standards
- Terminology preferences
- Example formatting

---

## Build Workflow

### Source of Truth
- **PreTeXt XML files** in `pretext/source/` are the single source of truth
- Do NOT edit Markdown files (they no longer exist)
- Do NOT edit HTML files directly (they are generated)

### Build Process

Run from the repository root:

```bash
python build.py           # Build both HTML and EPUB
python build.py html      # Build HTML only
python build.py epub      # Build EPUB only
```

### What the Build Does

1. **HTML Build:**
   - Runs `pretext build web`
   - Copies output from `pretext/output/web/` to `docs/`
   - Creates `.nojekyll` file for GitHub Pages
   - Applies custom CSS overrides (wider content area, consistent table alignment)

2. **EPUB Build:**
   - Converts HTML from `docs/` to EPUB using Pandoc
   - Outputs to `epub/Concise_Guide_to_English_Grammar.epub`

### Custom CSS

The build script automatically injects custom CSS into each HTML file's `<head>` section as an inline `<style>` tag. This approach ensures the styles override PreTeXt defaults regardless of CSS cascade order.

**Custom styles applied:**
- **Wider content area** (900px instead of default 696px) for better readability
- **Consistent table alignment** (all tables left-aligned with `!important` flags)

To modify these customizations, edit the `CUSTOM_CSS` constant in `build.py`.

### Output Locations

| Format | Location | Purpose |
|--------|----------|---------|
| HTML | `docs/` | GitHub Pages (https://phil-a-sophist.github.io/concise-guide-english-grammar/) |
| EPUB | `epub/Concise_Guide_to_English_Grammar.epub` | Downloadable ebook |

### Post-Build Cleanup

After every build, verify:
1. `pretext/output/` contains only temporary files (gitignored)
2. `docs/` contains the latest HTML with `.nojekyll` file
3. `epub/` contains the latest EPUB
4. No stray files in root directory
5. Delete any `.error_schema.log` or `codechat_config.yaml` if regenerated

### Commit and Push

**All builds should end with committing and pushing all changes to GitHub.** This ensures:
- The GitHub Pages site is updated with the latest HTML
- Changes are backed up and version-controlled
- Collaborators have access to the latest version

### Homework Workflow

When homework is created or updated in PreTeXt:
1. Build the HTML version (`python build.py html`)
2. Create a Word (.docx) version of the homework in `Homework/`
3. Format the Word file for digital completion:
   - Include blank lines or text fields where students can type answers
   - Use clear numbering that matches the PreTeXt version
   - Name files consistently: `ch-XX-homework.docx` and `ch-XX-answer-key.docx`

The `Homework/` folder contains Word files that students can download and complete digitally.

---

## Editing Content

### To Edit Chapter Content:
1. Open `pretext/source/ch-XX.ptx`
2. Make changes using PreTeXt XML syntax
3. Run `python build.py` to rebuild
4. Verify output in browser and/or EPUB reader

### PreTeXt Basics:
- Paragraphs: `<p>Text here</p>`
- Emphasis: `<em>italics</em>`, `<term>bold terminology</term>`
- Lists: `<ul><li><p>item</p></li></ul>` or `<ol>` for numbered
- Sections: `<section xml:id="unique-id"><title>Title</title>...</section>`

---

## Diagram Creation

### Key Files
| File | Purpose |
|------|---------|
| `scripts/generate_diagrams.py` | SVG generation script |
| `assets/diagrams/*.svg` | Generated diagram images |
| `reference_materials/image_inventory.md` | Image extraction log |
| `reference_materials/image_inventory_detailed.md` | Image-to-chapter mapping |

### Adding Diagrams to PreTeXt:
```xml
<figure xml:id="fig-unique-id">
  <caption>Description of diagram</caption>
  <image source="diagrams/filename.svg" width="60%">
    <description>Alt text for accessibility</description>
  </image>
</figure>
```

### Style Requirements
- **Blue (#0000FF):** Category labels (S, NP, VP, etc.)
- **Green (#008000):** Terminal words
- Use standard abbreviations: S, NP, VP, PP, AdjP, AdvP, N, V, Adj, Adv, Det, Pro, Aux, Modal

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
- `image_inventory.md` - Extracted images list
- `image_inventory_detailed.md` - Image-to-chapter mapping
- `PPTs/` - Instructor PowerPoint presentations
- `Other Class Materials/` - Handouts and tests
