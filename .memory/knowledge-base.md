# Knowledge Base

Last updated: 2026-02-11

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

**Context:** The project uses a specific visual style: blue (#0000FF) for category labels (S, NP, VP), green (#008000) for terminal words. Standard abbreviations: S, NP, VP, PP, AdjP, AdvP, N, V, Adj, Adv, Det, Pro, Aux, Modal. Diagrams in dedicated sections historically used `<paragraphs><title>` labels with the image and bracket notation in `<c>` tags. This is being migrated to proper `<figure>` elements (see "Diagram Label Markup" topic below).

## Homework Delivery

**Current approach:** Homework is authored in PreTeXt (rendered in HTML output) and also distributed as downloadable Word (.docx) files in `Homework/`. For Chapters 5 and 6, dedicated Python scripts using python-docx generate the homework, answer key, and overhead files from scratch. These scripts open the corresponding Chapter 5 .docx file as a template (to inherit styles, numbering definitions, and page layout), clear all content, then programmatically build new content. Answer keys exist for Chapters 4-15. Exercises are numbered sequentially across subsections within each chapter.

**Previously tried:**
- `Homework/generate_homework_from_pretext.py` — generic script to generate Word files from PreTeXt source; still exists but per-chapter scripts (like `scripts/generate_ch06_homework.py`) give finer control over formatting

**Context:** Word files are needed so students can type answers digitally. The naming convention is "Chapter XX Homework.docx" and "Chapter XX Answer Key.docx". Overhead files are "Homework XX Overhead.docx". A format guide is documented in `Homework/README.md`. The homework generation pattern: open template -> clear body (preserving sectPr) -> add content via helper functions (h1, h2, first, body_text, bullet, blank) -> save. The overhead uses larger font sizes (22pt min) and page breaks before each question.

## Homework Script Architecture (python-docx)

**Current approach:** Scripts use `python-docx` to generate .docx files. Key patterns:
- Open an existing .docx as template to inherit styles (Heading 1, Heading 2, First Paragraph, Body Text, Compact, Normal)
- Clear all body elements except `w:sectPr` (page layout)
- Use helper functions: `h1()`, `h2()`, `first()`, `body_text()`, `bullet()`, `blank()` for consistent formatting
- For bullets, use the "Compact" style with `w:numPr` XML element (numId typically "1001")
- For overhead files, set `w:pageBreakBefore` on each question heading and add 270pt space-after to push answers to mid-page
- All overhead text uses minimum 22pt font (H1=28pt, H2=26pt, H3=24pt, Body=22pt)

**Context:** This pattern was established with Chapter 5 reformatting scripts and extended to Chapter 6 generation. The `make_numPr()`, `set_page_break_before()`, and `add_run()` helper functions are duplicated across scripts.

## Language Example Formatting

**Current approach:** Language examples in PreTeXt source do NOT use italics. The style guide (`reference_materials/STYLE_GUIDE.md`) has been updated to explicitly state this rule. All code examples in the style guide were also updated to remove italics from linguistic examples.

**What `<em>` is still used for (legitimate uses):**
- Technical terms on first use (e.g., `<em>noun phrase (NP)</em>`)
- Category/type labels (e.g., `<em>Articles</em>`, `<em>Common vs. Proper Nouns</em>`)
- Test labels (e.g., `<em>Test 1: Plural formation</em>`)
- Emphasis (e.g., `<em>is</em>`, `<em>doing</em>`)
- Figure captions showing example sentences
- Key Terms section listing

**What `<em>` should NOT be used for:**
- Linguistic examples (words being analyzed): use plain text
- Morpheme/affix labels (-s, -ing, -ish, -ly): use plain text
- Strikethrough examples (~~text~~): use plain `~~text~~` without `<em>` wrapper
- Example words in lists, tables, or bullet points: use plain text

**Previously tried:**
- Italics for language examples — removed across chapters 4-21 in five commits
- `<em>~~text~~</em>` for strikethrough — simplified to `~~text~~` during formatting audit

**Context:** The initial automated removal (5 commits) covered the bulk of cases. A follow-up formatting consistency audit addressed remaining issues: nested em tags, em-wrapped strikethrough examples, morpheme labels, and superlative form examples. Chapters 5 and 6 received the most thorough second-pass audit.

## Revision Priorities

**Current approach:** The REVISION_AUDIT.md identifies revision priorities. Note that it references the old 27-chapter structure, but the analysis of content quality per topic area remains relevant. Key findings: foundation chapters (1-3) are well-developed; core grammar chapters need diagram integration and example freshness review; verb system and advanced structure chapters need significant expansion.

**Context:** The audit flags specific examples in the sentence patterns chapter that may need originality review. ASCII diagrams throughout need replacement with SVG/PNG tree diagrams.

## Diagram Label Markup (paragraphs to figure conversion)

**Current approach:** Converting diagram labels from `<paragraphs>` elements to proper `<figure>` elements in PreTeXt source. The old pattern was:
```xml
<paragraphs>
  <title>X.Y.Z Label: Description</title>
</paragraphs>
<image source="diagrams/new/chXX_filename.png" width="XX%">
  <description>Accessibility description</description>
</image>
<p><c>[Bracket notation]</c></p>
```
The new pattern uses `<figure>` which is the semantically correct PreTeXt element for labeled images. This also requires updating the custom CSS in `build.py` -- the old CSS targeted `.paragraphs .heading .title` and `[id*="diagrams-"] .paragraphs` selectors which will need to target the new figure-based HTML output instead.

**Previously tried:**
- `<paragraphs><title>` for diagram labels — being replaced because `<figure>` is the proper PreTeXt semantic element for captioned images

**Context:** Chapters 5 and 6 are the first to be converted. Both chapters have extensive `<paragraphs>` usage (84 in ch-05, 92 in ch-06). The conversion will likely need to extend to chapters 7-16 which also have diagram sections. The CSS in build.py has specific selectors for both dedicated diagram-examples sections (`[id*="diagrams-"]`) and inline diagrams that will need updating.

## Archived
