# Style Guide: A Concise Guide to English Grammar

This document defines the formatting conventions for all chapters in this textbook. Consistency across chapters ensures professional presentation in both EPUB and HTML formats.

---

## Typography

### Fonts
- **Titles and Headings (H1, H2)**: Sans-serif (Open Sans or system sans-serif stack)
- **Body text/Paragraphs**: Serif (Garamond or system serif stack)
- **Monospace/code**: Inconsolata or system monospace

### Heading Hierarchy
The visual design pairs sans-serif headings with serif body text—a classic typographic combination that creates clear visual hierarchy while maintaining readability for extended reading.

---

## Document Structure

### Chapter Header
```markdown
# N. Chapter Title
```
- Use `#` (level 1) only for the chapter title
- Include chapter number followed by period, then title
- Example: `# 4. Morphology and Word Structure`

### Standard Sections (in order)

1. **Learning Objectives** - Always present
2. **Key Terms** - Optional, when helpful
3. **Main content sections** (numbered 4.1, 4.2, etc.)
4. **Homework section**
5. **Chapter Summary**
6. **Glossary**

---

## Header Levels

### Level 2 (`##`) - Major Sections
Use for:
- Learning Objectives
- Key Terms
- Numbered content sections (e.g., `## 4.1 Section Title`)
- Homework
- Chapter Summary
- Glossary

### Level 3 (`###`) - Subsections
Use for named subsections within a major section:
```markdown
### Morphological Tests for Nouns
### Types of Compounds
### Practice Analysis
```
- Do NOT number these—use descriptive titles only
- Use sparingly; not every paragraph needs a subsection header

### Level 4 (`####`) - Rare Use Only
Use `####` sparingly and only for:
- Homework example labels: `#### Example (completed):`
- Occasional sub-subsections when truly necessary

**Avoid** using `####` for categorized lists or example types. Instead, use bold text within paragraphs (see Examples section below).

---

## Text Formatting

### Bold (`**text**`)
Use for:
- Key terms being defined: `**Morphology** is the study of...`
- Important principles or rules: `**A word can only be divided into morphemes if the base is a word in modern English.**`
- Category labels in lists: `**Noun + Noun:**`
- Emphasis on critical concepts

### Italics (`*text*`)
Use for:
- Emphasis on important concepts or distinctions
- Titles of works: `*Adventures of Huckleberry Finn*`
- Technical terms on first use (when not bolded)

Do NOT use italics for:
- Linguistic examples or words being analyzed — use `<foreign>` instead (see Language Example Formatting below)
- Lists of example words

### Strikethrough for Ungrammatical Examples
Use the PreTeXt `<delete>` element for ungrammatical constructions. It renders as `<del>` in HTML (strikethrough):
```xml
<foreign><delete>The happy's effect</delete></foreign>
```
Do NOT use `~~text~~` (literal tildes do not render as strikethrough in PreTeXt).

### Grammaticality Judgments
- ✓ for grammatical/correct
- ✗ for ungrammatical/incorrect

### Labeled Content: Inline vs. Block Format

When content has an italicized or bolded label followed by explanatory text, choose the format based on content length:

**Inline format** (label and content on same line):
Use when the content is brief—a few words, a short list, or one short sentence.
```markdown
*Example:* The word unhappy contains two morphemes.

**Prefix:** A morpheme attached before the base.
```

**Block format** (label on its own line, content below and indented):
Use when the explanation runs longer than one line or contains multiple sentences.
```markdown
*Example*
    The word unhappy contains two morphemes. The prefix un- attaches
    to the base happy, changing its meaning to the opposite. This is
    a productive pattern in English.
```

In PreTeXt, use `<paragraphs><title>` for block-format labels:
```xml
<paragraphs>
  <title>Example</title>
</paragraphs>
<p>The word unhappy contains two morphemes. The prefix un-
attaches to the base happy, changing its meaning to the opposite.</p>
```

---

## Language Example Formatting

Language examples (words, phrases, or sentences being discussed as linguistic objects) use a distinct visual treatment to separate them from the surrounding explanatory prose. This requires a manual read-through of each chapter to distinguish language examples from genuine emphasis.

### PreTeXt Element: `<foreign>`

All language examples use the `<foreign>` element, which renders as `<i class="foreign">` in HTML. Custom CSS overrides this to display as **sans-serif, non-italic, at 0.9em** (slightly smaller than body text).

```xml
<foreign>the dog barked</foreign>
```

**What counts as a language example:**
- Words being discussed as words: "the determiner `<q><foreign>the</foreign></q>` signals..."
- Phrases or sentences presented as examples of grammatical structures
- Pattern notation: `<foreign>Det + Adj + N</foreign>`
- Items in example lists, table cells with example words/phrases

**What is NOT a language example (keep as `<em>` or `<term>`):**
- Technical terms being defined: `<term>Closed classes</term> resist new members.`
- Emphasis on concepts: `<em>Case matters</em>: Use subject forms...`
- Category labels: `<em>Articles</em>—the most common determiners:`
- Test labels: `<em>Test 1: Adjectives are gradable.</em>`

### Inline Examples in Paragraphs: Quotation Marks

Single language examples within paragraph text use `<q>` (quotation marks) as the default marker:

```xml
<p>The determiner <q><foreign>a</foreign></q> signals indefinite reference.</p>
```

This renders as: The determiner "a" signals indefinite reference.

For inline sentence examples, wrap the full sentence:

```xml
<p>When you hear <q><foreign>I saw the dog,</foreign></q> the determiner signals...</p>
```

### Grouped Multiple Examples: Parentheses

When listing multiple language examples together as a set, use parentheses around the group:

```xml
<p>They indicate quantity (<foreign>some</foreign>, <foreign>many</foreign>, <foreign>every</foreign>, <foreign>three</foreign>).</p>
```

This is the ONLY use of parentheses for language examples. Do not parenthesize single examples.

If a series of examples was previously formatted with separate parentheses around each word, consolidate into one grouped set:
- Before: `(<foreign>his</foreign>), (<foreign>my</foreign>), (<foreign>your</foreign>)`
- After: `(<foreign>his</foreign>, <foreign>my</foreign>, <foreign>your</foreign>)`

### Lists, Tables, and Block Quotes: No Markers

In bulleted lists, numbered lists, tables, and block quotes, language examples need **no quotation marks or parentheses**. The font change plus the grey background (applied by CSS) provides sufficient visual distinction:

```xml
<ul>
  <li><p><foreign>the big dog</foreign></p></li>
  <li><p><foreign>my old friend</foreign></p></li>
</ul>
```

In list items that mix example and explanatory text, the example appears bare:

```xml
<li><p><foreign>very tall</foreign> — <foreign>tall</foreign> is an adjective</p></li>
```

### Highlighting Within Examples

To highlight a specific word within a language example, use `<em>` inside `<foreign>`:

```xml
<foreign><em>The</em> dog barked.</foreign>
```

This renders the full phrase in sans-serif, with the target word additionally emphasized.

### Ungrammatical Examples

Use `<delete>` inside `<foreign>` for struck-through ungrammatical examples:

```xml
<foreign><delete>Dog barked.</delete></foreign>
```

Often paired with a grammatical counterpart:

```xml
<li><p><foreign><em>She</em> left.</foreign> (not <foreign><delete>Her left.</delete></foreign>)</p></li>
```

### CSS Behavior (Reference)

The following CSS rules are injected by `build.py`:
- `.foreign` / `i.foreign`: sans-serif, non-italic, 0.9em
- `q`: sans-serif, 0.9em (matches foreign text in quoted context)
- `ul:has(> li .foreign)`, `ol:has(> li .foreign)`: grey background (#f5f6f8), left border, indentation
- `.tabular-box:has(.foreign)`: same grey background treatment
- `del`: browser-default strikethrough

### Quick Reference Table

| Context | Marker | Example |
|---------|--------|---------|
| Single word/phrase in paragraph | Quotation marks (`<q>`) | `<q><foreign>the</foreign></q>` |
| Sentence example in paragraph | Quotation marks (`<q>`) | `<q><foreign>The dog barked.</foreign></q>` |
| Grouped multiples in paragraph | Parentheses | `(<foreign>a</foreign>, <foreign>an</foreign>)` |
| Example in list item | None | `<foreign>the big dog</foreign>` |
| Example in table cell | None | `<foreign>a book</foreign>` |
| Ungrammatical example | Strikethrough | `<foreign><delete>text</delete></foreign>` |
| Highlighted word in example | `<em>` inside `<foreign>` | `<foreign><em>The</em> dog</foreign>` |

---

## Lists

### Bullet Lists
Use `-` for bullets:
```markdown
- First item
- Second item
- Third item
```

### Numbered Lists
Use for sequential steps or ordered items:
```markdown
1. First step
2. Second step
3. Third step
```

### Definition-Style Lists

**Short content (same line):** When the content after the label is brief (a few words or a short list), keep everything on the same line:
```markdown
**Spatial:** in, on, at, above, below

**Temporal:** before, after, during, since

**Abstract:** of, for, with, by, about
```

**Extended content (block format):** When the content requires more than one line of explanation, use block format—put the label on its own line, then the explanation below it, indented:
```markdown
**Spatial Prepositions**
    Words like in, on, and at indicate physical location or position.
    These are among the most common prepositions in English and often have
    metaphorical extensions (e.g., in love, on fire).
```

**Guidelines for choosing format:**
- Same-line format: Use for lists of examples, single-sentence definitions, or content that fits comfortably on one line
- Block format: Use when the explanation runs longer than one line or includes multiple sentences

---

## Examples and Analyses

Use the Language Example Formatting system (above) for all examples. This section provides PreTeXt XML templates for common analysis patterns.

### Inline Examples in Prose

Always wrap inline language examples using the `<q><foreign>` pattern documented above:

```xml
<p>For example, <q><foreign>happy</foreign></q> is an adjective because it can be compared (<q><foreign>happier</foreign></q>, <q><foreign>happiest</foreign></q>) and modified by <q><foreign>very</foreign></q> (<q><foreign>very happy</foreign></q>).</p>
```

Or, using grouped parentheses for multiple related examples:

```xml
<p>Adjectives can be modified by adverbs such as <foreign>(very, somewhat, extremely, rather)</foreign>.</p>
```

### Formatted Example Analyses

For morpheme breakdowns or grammatical analyses, use PreTeXt list structures:

**Simple format (preferred):**
```xml
<p><q><foreign>Unhappy</foreign></q> = un- + happy</p>
<ul>
  <li><p>un- = bound morpheme (prefix meaning "not")</p></li>
  <li><p>happy = free morpheme</p></li>
  <li><p>Total: 2 morphemes</p></li>
</ul>
```

**For incorrect analyses:**
```xml
<p><q><delete><foreign>Ugly</foreign></delete></q> ≠ ug + -ly</p>
<ul>
  <li><p>"Ug" is not a word in English ✗</p></li>
  <li><p>One morpheme</p></li>
</ul>
```

### Categorized Examples

When presenting multiple types/categories, use bold labels (NOT `####` headers):

**Correct:**
```xml
<p><strong>Type 1: Non-Existent Bases</strong></p>
<p>Some words look like they contain familiar affixes, but the remaining "base" isn't actually a word in English.</p>
<p><q><delete><foreign>Ugly</foreign></delete></q> ≠ ug + -ly</p>
<ul>
  <li><p>"Ug" is not a word in English ✗</p></li>
  <li><p>One morpheme</p></li>
</ul>
```

**Incorrect (do not use):**
```xml
<title>Type 1: Non-Existent Bases</title>
```

---

## Tables

Use standard markdown tables with alignment:
```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
```

- Keep tables readable in both wide (HTML) and narrow (EPUB) formats
- Avoid overly wide tables with many columns

### Sentence Labeling Tables

Sentence labeling tables have four rows: **Role**, **Phrase**, **Word**, and **POS**. The Word and POS rows always have one cell per word. The Role and Phrase rows use **merged cells** (colspan) to show how words group into phrases and roles.

**Merge rules:**
- **Completed tables** (examples, answer keys): Merge cells in Role and Phrase rows to span the words they cover.
- **Student exercise tables** (blanks for students to fill): Keep one cell per word so students have individual cells to write in.
- **Partially completed tables**: Merge only the rows that are already filled in; leave blank rows unmerged.

**Example (merged):** For "The old man sat quietly":
- Role: "Subject" spans 3 columns (The, old, man); "Predicate" spans 2 (sat, quietly)
- Phrase: "NP" spans 3 columns (The, old, man); "MVP" spans 1 (sat); "ADVP" spans 1 (quietly)

**PreTeXt format:**
```xml
<tabular halign="center">
  <row header="yes">
    <cell>Role</cell>
    <cell colspan="3">Subject</cell>
    <cell colspan="2">Predicate</cell>
  </row>
  <row>
    <cell>Phrase</cell>
    <cell colspan="3">NP</cell>
    <cell>MVP</cell>
    <cell>ADVP</cell>
  </row>
  <row>
    <cell>Word</cell>
    <cell>The</cell>
    <cell>old</cell>
    <cell>man</cell>
    <cell>sat</cell>
    <cell>quietly</cell>
  </row>
  <row>
    <cell>POS</cell>
    <cell>DET</cell>
    <cell>ADJ</cell>
    <cell>N</cell>
    <cell>V</cell>
    <cell>ADV</cell>
  </row>
</tabular>
```

**Word (.docx) format:** Use `cell.merge(other_cell)` in python-docx to merge cells in the Role and Phrase rows.

**Markdown format:** Standard Markdown does not support colspan. Use raw HTML `<table>` elements with `colspan` attributes when labeling tables appear in `.md` files.

**HTML format:** Use `<td colspan="N">` in `<table>` elements (generated automatically by PreTeXt from the XML above).

---

## Diagrams

### ASCII Diagrams
Use fenced code blocks for tree diagrams:
```markdown
```
        NP
    ┌───┼───┐
   Det  Adj  N
    │    │   │
   the  tall student
```
```

### SVG Diagrams
Reference with standard markdown image syntax:
```markdown
![Description](assets/diagrams/filename.svg)
```

---

## Section Separators

Use `---` (horizontal rule) to separate:
- Major sections within a chapter
- Before and after the homework section
- Between homework parts (optional)

Do NOT use multiple `---` in succession.

---

## Homework Section Format

### PreTeXt Structure

```xml
<section xml:id="ch-XX-homework">
  <title>Homework: [Chapter Topic]</title>

  <subsection xml:id="ch-XX-homework-1">
    <title>[Descriptive Section Title]</title>

    <paragraphs>
      <title>Instructions</title>
    </paragraphs>
    <p>[Clear instructions for this part]</p>

    <paragraphs>
      <title>Example (completed)</title>
    </paragraphs>
    <p>[Completed example showing expected format]</p>

    <paragraphs>
      <title>Exercises</title>
    </paragraphs>

    <p><em>Exercise 1.</em> [First exercise]</p>

    <p><em>Exercise 2.</em> [Second exercise]</p>
    <ul>
      <li><p>[Indented sub-item for exercise]</p></li>
      <li><p>[Another sub-item]</p></li>
    </ul>

  </subsection>
</section>
```

### Key Homework Conventions

**Section and Subsection Titles:**
- Use `<section>` for the main homework section titled "Homework: [Topic]"
- Use `<subsection>` for each part with descriptive titles only (e.g., "Morpheme Identification")
- Do NOT include "Part 1:", "Part 2:" in titles—the automatic numbering (4.5.1, 4.5.2) provides this
- Do NOT include time estimates in titles

**Headings within subsections:**
- Use `<paragraphs><title>Instructions</title></paragraphs>` for instructions
- Use `<paragraphs><title>Example (completed)</title></paragraphs>` for examples
- Use `<paragraphs><title>Exercises</title></paragraphs>` before the exercises begin
- Use `<paragraphs><title>Passage</title></paragraphs>` when providing reading passages
- Do NOT include colons in these titles (PreTeXt adds punctuation automatically)

**Exercise numbering and formatting:**
- Label each exercise as "Exercise 1.", "Exercise 2.", etc. using `<em>Exercise 1.</em>`
- Continue numbering sequentially across all subsections (Exercise 1-5, then 6-10, etc.)
- **Short exercises:** If the exercise content is brief (a few words), keep on the same line: `<em>Exercise 1.</em> Identify the noun.`
- **Extended exercises:** If the exercise requires multi-line explanation, put the label on its own line, then the content in a separate paragraph or list below it:
```xml
<paragraphs>
  <title>Exercise 1</title>
</paragraphs>
<p>Analyze the following sentence for morpheme boundaries. Identify each
morpheme as free or bound, and explain your reasoning.</p>
```

**Indentation for sub-items:**
- Use `<ul>` bullet lists to indent content that belongs to an exercise
- This includes prompts like "Create a word with one suffix:", "Morphemes:", etc.
- Indentation helps delineate the content of each exercise

**Time estimates:**
- Include total estimated time at the end of the homework section
- Do NOT include per-part time estimates in subsection titles

---

## Glossary Format

```markdown
## Glossary

**Term**: Definition text here.

**Another Term**: Definition text here.
```

- Bold the term, follow with colon
- One definition per term
- Alphabetical order preferred

---

## Cross-References

Refer to other chapters by number:
```markdown
As discussed in Chapter 5...
See section 6.2 for more detail...
```

---

## Special Characters

- Use em-dash (—) for parenthetical statements, not double hyphens
- Use proper quotation marks (" ") not straight quotes where possible
- Use ≠ for "does not equal" in linguistic analysis

---

## Common Mistakes to Avoid

1. **Over-using `####` headers** - Use bold text for categories instead
2. **Inconsistent example formatting** - Follow the patterns above
3. **Missing horizontal rules** - Use `---` between major sections
4. **Numbered subsections** - Subsection headers should be descriptive, not numbered
5. **Mixing formatting styles** - Keep example presentations consistent within a chapter
6. **Too many header levels** - Flatten structure where possible

---

## Quality Checklist

Before finalizing a chapter, verify:

- [ ] Chapter header uses `# N. Title` format
- [ ] Learning Objectives present and properly formatted
- [ ] Section numbers match chapter (4.1, 4.2 for Chapter 4)
- [ ] Subsection headers use `###` without numbers
- [ ] `####` used sparingly (homework examples only)
- [ ] Language examples use `<foreign>` (not `<em>`) with correct markers per context
- [ ] Examples use consistent formatting throughout
- [ ] Tables render properly
- [ ] Horizontal rules separate major sections
- [ ] Homework includes time estimates
- [ ] Glossary terms are bold with definitions
- [ ] Check both EPUB and HTML output for rendering issues
