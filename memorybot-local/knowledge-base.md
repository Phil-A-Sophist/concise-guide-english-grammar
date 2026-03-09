> **Size limit: 80 lines.** When this document exceeds 80 lines, condense it.
> Move overflow to `data/static/knowledge-base-archive-YYYY.md` and add a pointer here.

# Knowledge Base

Last updated: 2026-03-03

## Build Pipeline

PreTeXt XML is the single source of truth (`pretext/source/*.ptx`). Build with `python build.py` → runs `pretext build web` → copies to `docs/` for GitHub Pages + injects custom CSS inline. EPUB via Pandoc. Published: https://phil-a-sophist.github.io/concise-guide-english-grammar/

**Custom CSS:** Injected as inline `<style>` into each HTML `<head>` by build.py. Key overrides: Garamond body text, 900px width (vs 696px default), left-aligned tables. Modify `CUSTOM_CSS` constant in build.py.

**Diagram workflow:** SVGs in `assets/diagrams/`. PNG versions (newer) in `assets/diagrams/new/`. Colors: blue (#0000FF) category labels, green (#008000) terminals. Standard abbrevs: S, NP, VP, PP, AdjP, AdvP, N, V, Adj, Adv, Det, Pro, Aux, Modal.

## Homework Delivery

Three files per chapter: `Chapter XX Homework.docx`, `Chapter XX Answer Key.docx`, `Homework XX Overhead.docx`. Generate student files: `cd Homework && python generate_homework_from_pretext.py` (processes ALL chapters — only commit target chapter's .docx). Answer keys via chapter-specific scripts in scripts/. Answers keys exist Ch4-16, Ch18. Missing: Ch17, Ch19-21.

**Exercise format:** `<em>Exercise N.</em>` (required for script regex). Section labels use `<paragraphs><title>` block format.

**Difficulty model:** 15-25 exercises, 5 parts, identification-heavy (60%), scaffolded, 30-60 min.

## Language Example Formatting (`<foreign>`)

Chapters 1-18 complete. Ch19 next. Rule: text discussed AS language → `<foreign>`. Emphasis/labels/terms → keep `<em>`.

- Inline paragraph: `<q><foreign>The dog barked.</foreign></q>`
- List/table: bare `<foreign>the dog</foreign>`
- Highlight within: `<foreign><em>The</em> dog barked.</foreign>`
- Ungrammatical: `<foreign><delete>text</delete></foreign>`
- `&quot;` shortcut: followed by "is a", "forms", "modifies" → language example → convert

## Exam Creation

Author in Markdown → generate .docx via python-docx. Tree diagrams via SyntaxTreeHybrid + Playwright → PNG → embed. Scripts: `generate_exam_diagrams.py`, `generate_exam_docx.py`. Exam One structure: Ch4-7, 100 pts + 10 bonus, Section A (25 MC) + Section B (5 diagramming).

## Sentence Labeling Tables

PreTeXt: `<tabular top="minor" left="minor">` with `<col halign="left" right="minor"/>`. Student tables pre-merge Role/Phrase cells with `colspan` (blank_labels() + compute_spans()). Word docs: `Table Grid` style.

> See `data/static/knowledge-base-archive-2026.md` for: Ch7 revision detail, MVP removal, Ch7 homework structure, revision priorities, chapter reorganization history.
