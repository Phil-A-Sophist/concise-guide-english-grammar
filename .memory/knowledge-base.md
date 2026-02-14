# Knowledge Base

Last updated: 2026-02-13

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

## Language Example Formatting

**Current approach:** Comprehensive multi-pronged formatting system using `<foreign>` PreTeXt element, documented in STYLE_GUIDE.md for rollout across all chapters. Chapters 1-6 completed and committed. Chapter 7 formatting deferred in Task 16 due to major structural revision priority; rollout resumes with Chapter 8.

1. **`<foreign>` element (REQUIRED):** All language examples use `<foreign>` → renders as `<i class="foreign">` → CSS overrides to sans-serif, non-italic, 0.9em
2. **`<q>` element (inline examples in paragraphs):** Automatically renders quotation marks: `<q><foreign>The dog barked.</foreign></q>` → "The dog barked."
3. **Parenthetical grouping:** Use parentheses only for grouped multiple examples: `<foreign>(some, many, every, three)</foreign>` (NOT individual examples)
4. **No markers in lists/tables/block quotes:** Font styling + grey background (#f5f6f8) with left border (CSS `:has(.foreign)`) provides sufficient distinction
5. **Highlighting within examples:** Use `<em>` inside `<foreign>`: `<foreign><em>The</em> dog barked.</foreign>`
6. **Ungrammatical examples:** Use `<delete>` inside `<foreign>`: `<foreign><delete>ungrammatical text</delete></foreign>` (renders as strikethrough)
7. **`<em>` element (emphasis ONLY):** Retain exclusively for emphasis, labels, and technical terms (NOT language examples)

**Documentation:** STYLE_GUIDE.md now contains:
- Core markup elements section
- Detailed marking rules by context (paragraphs, lists, tables, block quotes, grouped examples)
- Formatting examples showing correct and incorrect usage
- Quick reference table for all contexts
- CSS behavior reference
- PreTeXt XML template updates for Examples and Analyses section

**Previously tried:**
- Italics (`<em>`) for language examples — removed because it conflated emphasis with language mention
- `<c>` (code), `<alert>`, custom elements — rejected because `<foreign>` already maps to cleanly targetable CSS
- Literal tildes `~~text~~` for ungrammatical examples — abandoned in favor of semantic `<delete>` element
- Font size at 0.95em — refined to 0.9em for better sans-serif rendering consistency

**Context:** Chapters 1-6 formatting approved by user and fully documented. The approach balances visual clarity (sans-serif, reduced size, context-specific markers) with semantic correctness (proper PreTeXt XML elements, minimal over-marking). Manual chapter-by-chapter review required to apply rules consistently.

## Chapter 7 Major Revision (Task 16)

**Current approach:** Complete structural overhaul integrating PNG diagrams and new pedagogical content:
- Replaced all ASCII art diagrams with 10 SyntaxTreeHybrid-generated PNG images (ch07_*)
- Standardized all diagram labels to ALL CAPS (DET, PRON, ADJ, ADV, PREP, CONJ, AUX, ADJP, ADVP) for consistency across entire textbook
- Renamed "Complements" to "Objects and Complements" with revised text explaining both object and object-complement roles
- Enhanced "Structural Ambiguity" subsection with pedagogical framing (garden-path sentences, joke examples)
- Replaced "Diagramming Conventions" (section 7.6) with "Sentence Labeling Tables" introducing MVP (Minimum Viable Phrase) concept and Subject/Predicate roles; two worked examples included
- Added "Step-by-Step Sentence Analysis" (new section 7.7) teaching top-down and bottom-up parsing approaches with worked examples
- Homework Parts 3-5 rewritten: sentence labeling table exercises, diagram-plus-table exercises, structural ambiguity analysis (Marx Brothers joke: "Hanging Parsons" and garden-path sentence: "The horse raced past the barn fell")
- Updated Diagram Examples section with ch07-specific PNG images and bracket notation
- Expanded glossary with terminology from new sections
- Revised learning objectives to reflect new content structure

**Bracket notation approach:** 10 new entries added to `bracket_notations.txt` for ch07 diagrams. Old ch07 VP diagram entries preserved (not touched) because ch-05, ch-10, ch-11 reference them by ID.

**Context:** This revision represents the first major structural overhaul since the pilot formatting work on ch-06. Priority was given to ch07 due to its foundational role in the textbook (chapter on diagramming introduces critical techniques). Diagram integration, pedagogical clarity (MVP framing, top-down/bottom-up analysis), and homework modernization (table-based exercises) all prioritized for student learning outcomes.

## Archived
