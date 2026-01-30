# Style Guide: A Concise Guide to English Grammar

This document defines the formatting conventions for all chapters in this textbook. Consistency across chapters ensures professional presentation in both EPUB and HTML formats.

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
- Linguistic examples (words being analyzed): `*happy*`, `*un-*`, `*rewriters*`
- Titles of works: `*Adventures of Huckleberry Finn*`
- Technical terms on first use (when not bolded)

### Strikethrough for Ungrammatical Examples
Use `*~~text~~*` for ungrammatical constructions:
```markdown
*~~The happy's effect~~*
```

### Grammaticality Judgments
- ✓ for grammatical/correct
- ✗ for ungrammatical/incorrect

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
For categorized examples, use bold labels followed by content:
```markdown
**Spatial:** *in*, *on*, *at*, *above*, *below*

**Temporal:** *before*, *after*, *during*, *since*

**Abstract:** *of*, *for*, *with*, *by*, *about*
```

---

## Examples and Analyses

### Inline Examples
Present simple examples within prose:
```markdown
For example, *happy* is an adjective because it can be compared (*happier*, *happiest*) and modified by *very* (*very happy*).
```

### Formatted Example Analyses
For morpheme breakdowns or grammatical analyses, use a consistent format:

**Simple format (preferred):**
```markdown
*Unhappy* = *un-* + *happy*
- *un-* = bound morpheme (prefix meaning "not")
- *happy* = free morpheme
- Total: 2 morphemes
```

**For incorrect analyses:**
```markdown
*Ugly* ≠ *ug* + *-ly*
- "Ug" is not a word in English ✗
- One morpheme
```

### Categorized Examples
When presenting multiple types/categories, use bold labels (NOT `####` headers):

**Correct:**
```markdown
**Type 1: Non-Existent Bases**

Some words look like they contain familiar affixes, but the remaining "base" isn't actually a word in English.

*Ugly* ≠ *ug* + *-ly*
- "Ug" is not a word in English ✗
- One morpheme
```

**Incorrect (do not use):**
```markdown
#### Type 1: Non-Existent Bases
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

**Exercise numbering:**
- Label each exercise as "Exercise 1.", "Exercise 2.", etc. using `<em>Exercise 1.</em>`
- Continue numbering sequentially across all subsections (Exercise 1-5, then 6-10, etc.)

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
- [ ] Examples use consistent formatting throughout
- [ ] Tables render properly
- [ ] Horizontal rules separate major sections
- [ ] Homework includes time estimates
- [ ] Glossary terms are bold with definitions
- [ ] Check both EPUB and HTML output for rendering issues
