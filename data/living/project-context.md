> **Size limit: 80 lines.** See memory-guide.md for condensation rules.

# Project Context: concise-guide-english-grammar

Last updated: 2026-03-03

## Purpose and Structure

OER college textbook, 21 chapters thematically organized. PreTeXt XML source → HTML (GitHub Pages) + EPUB. Published at: https://phil-a-sophist.github.io/concise-guide-english-grammar/

Sections: Foundations (1-4), Core Grammar (5-9), The Verb System (10-11), Form and Function (12-15), Writing and Style (16-19), Applied Grammar (20-21).

## Build Workflow

```bash
python build.py        # Build HTML + EPUB (run from repo root)
python build.py html   # HTML only
python build.py epub   # EPUB only
```

**What it does:** `pretext build web` → copies to `docs/` → injects custom CSS inline → creates `.nojekyll`. EPUB via Pandoc from `docs/`.

**After build:** Verify `docs/` has latest HTML. No stray `.error_schema.log` or `codechat_config.yaml`.

**CSS:** Inline `<style>` tag in each HTML `<head>`. Modify `CUSTOM_CSS` constant in build.py.

## Key Rules

- **Source of truth:** `pretext/source/*.ptx` — never edit `docs/` or `epub/` directly
- **Commit:** Always chapter-specific files only. Never `git add -A`.
- **Live site:** Every push updates student-facing textbook immediately.
- **Style guide:** Reference `reference_materials/STYLE_GUIDE.md` before editing content.

## Diagram Style

Blue (#0000FF) for category labels (S, NP, VP, etc.), green (#008000) for terminal words. Reference `reference_materials/bracket_notations.txt` for existing notation entries.

Each diagram in PreTeXt:
```xml
<paragraphs><title>X.Y.Z Label: Description</title></paragraphs>
<image source="diagrams/new/chXX_filename.png" width="XX%">
  <description>Alt text</description>
</image>
<p><c>[Bracket notation]</c></p>
```

## Exam/Assignment Files

Located in `Homework/Exams/`. Scripts generate .docx from inline data (not from Markdown). Diagrams via SyntaxTreeHybrid + Playwright → PNG. Do not commit answer keys without explicit user confirmation.
