# Knowledge Base

Last updated: 2026-02-07

## Source Format and Build Pipeline

**Current approach:** PreTeXt XML is the single source of truth. All content lives in `pretext/source/*.ptx` files. The build pipeline uses `python build.py` which runs `pretext build web` for HTML, copies output to `docs/` for GitHub Pages, injects custom CSS inline into each HTML file, and optionally generates EPUB via Pandoc.

**Previously tried:**
- Markdown source files — abandoned in favor of PreTeXt XML for richer semantic markup and multi-format output

**Context:** PreTeXt was chosen because it supports structured textbook features (exercises, figures, cross-references) and generates both HTML and EPUB from a single source. The project uses PreTeXt 2.36.0.

## Custom CSS Strategy

**Current approach:** Custom CSS is injected directly into each HTML file's `<head>` as an inline `<style>` tag by `build.py`. This overrides PreTeXt defaults regardless of cascade order. Key customizations: Garamond body text with Open Sans headings, wider content area (900px vs 696px default), left-aligned tables, diagram styling, and hidden page footer.

**Context:** Inline injection was chosen over external stylesheets to guarantee override priority. The `CUSTOM_CSS` constant in `build.py` is the single place to modify styles.

## Chapter Reorganization (27 to 21 Chapters)

**Current approach:** The textbook was consolidated from 27 chapters to 21 chapters organized in 6 thematic sections: Foundations (1-4), Core Grammar (5-9), The Verb System (10-11), Form and Function (12-15), Writing and Style (16-19), and Applied Grammar (20-21).

**Context:** The REVISION_AUDIT.md still references the original 27-chapter structure. The current 21-chapter structure is the active one reflected in PreTeXt source files and CLAUDE.md.

## Diagram Workflow

**Current approach:** Tree diagrams are generated as SVGs using Python scripts (`scripts/generate_diagrams.py`, `scripts/generate_new_diagrams.py`) and stored in `assets/diagrams/`. PNG versions for newer diagrams live in `assets/diagrams/new/`. Original source images were extracted from instructor PowerPoint slides and stored in `assets/images/diagrams/`. Diagrams are referenced in PreTeXt using `<image source="diagrams/filename.svg">` syntax.

**Context:** The project uses a specific visual style: blue (#0000FF) for category labels (S, NP, VP), green (#008000) for terminal words. Standard abbreviations: S, NP, VP, PP, AdjP, AdvP, N, V, Adj, Adv, Det, Pro, Aux, Modal. Each diagram in dedicated sections uses a `<paragraphs><title>` label, the image, and bracket notation in `<c>` tags.

## Homework Delivery

**Current approach:** Homework is authored in PreTeXt (rendered in HTML output) and also distributed as downloadable Word (.docx) files in `Homework/`. A script `generate_homework_from_pretext.py` assists with Word file generation. Answer keys exist for Chapters 4-15. Exercises are numbered sequentially across subsections within each chapter.

**Context:** Word files are needed so students can type answers digitally. The naming convention is "Chapter XX Homework.docx" and "Chapter XX Answer Key.docx".

## Revision Priorities

**Current approach:** The REVISION_AUDIT.md identifies revision priorities. Note that it references the old 27-chapter structure, but the analysis of content quality per topic area remains relevant. Key findings: foundation chapters (1-3) are well-developed; core grammar chapters need diagram integration and example freshness review; verb system and advanced structure chapters need significant expansion.

**Context:** The audit flags specific examples in the sentence patterns chapter that may need originality review. ASCII diagrams throughout need replacement with SVG/PNG tree diagrams.

## Archived
