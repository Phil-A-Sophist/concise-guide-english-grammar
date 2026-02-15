# Chapter Improvement Process

This document describes the systematic chapter-by-chapter improvement process. Follow this for each chapter starting from Chapter 8.

## Quick Start

When the user says "improve Chapter X" or "let's do Chapter X next":

1. Read this file and `.memory/state.md`
2. Spawn memory consolidation agent in background
3. Execute the 4 steps below in order
4. Build, commit, push

---

## Step 1: Diagram Audit (5 min)

**Goal:** Ensure the chapter uses SyntaxTreeHybrid PNG diagrams, not old SVGs.

1. List PNG files: `assets/diagrams/new/chXX_*`
2. List old SVGs: `assets/diagrams/chXX*` or `assets/diagrams/ch-XX*`
3. Grep the chapter for `<image source=` to see current references
4. If old SVGs are referenced, replace paths with new PNGs
5. If no PNGs exist for the chapter, note this — diagrams may need generation first

**Ch7 result:** Already complete (8 unique PNGs, no old SVGs). Chapters 8+ will likely need SVG→PNG replacement.

---

## Step 2: Style Guide Compliance — `<foreign>` Conversion (main work)

**Goal:** Convert all language examples from `<em>` to `<foreign>` per STYLE_GUIDE.md.

### Decision Rule

Ask: "Is this text being discussed AS a piece of language (its form, structure, grammar)?"
- **YES** → use `<foreign>` (with `<q>` if inline in a paragraph)
- **NO** (emphasis, label, technical term, concept, speech) → keep `<em>` or `<term>`

### Conversion Patterns

| Context | Before | After |
|---------|--------|-------|
| Inline in paragraph | `<em>The dog barked.</em>` | `<q><foreign>The dog barked.</foreign></q>` |
| In list item | `<em>the dog</em>` | `<foreign>the dog</foreign>` (bare) |
| In table cell | `the dog, she` | `<foreign>the dog</foreign>, <foreign>she</foreign>` (bare) |
| Highlighted word in example | `<em>The</em> dog` | `<foreign><em>The</em> dog</foreign>` |
| `&quot;word&quot;` language mention | `&quot;dog&quot;` | `<q><foreign>dog</foreign></q>` |
| Grouped in parentheses | `(<em>a, an, the</em>)` | `(<foreign>a, an, the</foreign>)` |

### What to KEEP as `<em>` (do NOT convert)

- **Labels**: "Example:", "Step 1—...", "Instructions:", "In noun phrases:"
- **Emphasis**: "how", "inside", "meaning depends on structure"
- **Technical terms being introduced**: "noun phrase (NP)", "tree diagrams", "head"
- **Key Terms line** at top of chapter
- **Category labels**: "For reading:", "For writing:"

### What to convert to `<term>` (if defining a term)

- Bold terminology being formally defined: `<term>structural ambiguity</term>`

### Efficient Editing Strategy

Work section by section through the chapter. Within each section:
1. **Tables first** — convert Examples columns to `<foreign>` (many individual items)
2. **Lists next** — convert to bare `<foreign>`
3. **Paragraph text last** — convert `<em>` sentences to `<q><foreign>`, convert `&quot;` mentions
4. **Skip** labels, emphasis, and technical terms

### `&quot;` Classification Shortcut

- If followed by "is a", "forms", "modifies", "attaches" → language example → convert
- If describing a concept, question, or paraphrase → keep as `&quot;` or `<q>` without `<foreign>`

---

## Step 3: Homework Formatting

### 3A: Check Exercise Numbering

All exercises must use: `<em>Exercise N.</em>` (not `<em>N.</em>` or bare numbers).

Grep check: `grep "Exercise \d" ch-XX.ptx` should match all exercises.

### 3B: Check Section Labels

Homework subsections must use block labels:
```xml
<paragraphs>
  <title>Instructions</title>
</paragraphs>
<p>The actual instructions text...</p>

<paragraphs>
  <title>Example (completed)</title>
</paragraphs>

<paragraphs>
  <title>Exercises</title>
</paragraphs>
```

NOT inline: `<p><em>Instructions:</em> text...</p>`

### 3C: Apply `<foreign>` to Homework Examples

Exercise sentences use bare `<foreign>` (not `<q><foreign>`):
```xml
<p><em>Exercise 1.</em> <foreign>The dog barked loudly.</foreign></p>
```

### 3D: Assess Homework Difficulty

Compare against ch4-7 model:
- 15-25 exercises per chapter, 5 subsections
- Mix: identification (60%), analysis (30%), creation (10%)
- Scaffolded examples before every exercise set
- 30-60 minutes total estimated time
- If ch8+ homework seems too hard, simplify toward ch4-7 patterns

---

## Step 4: Generate Word Files

Three files per chapter:

### 4A: Student Homework (.docx)

The `generate_homework_from_pretext.py` script processes ALL chapters. To regenerate just one:
```bash
cd Homework && python generate_homework_from_pretext.py
```
Then only stage `Chapter XX Homework.docx` in the commit.

**Gotcha:** The script expects `<em>Exercise N.</em>` numbering pattern (regex: `r'^\s*(Question|Exercise)\s+\d+'`). Fix numbering in Step 3A first.

### 4B: Answer Key (.docx)

Must be created manually or via a chapter-specific script since answers aren't in PreTeXt source.

Pattern: create `scripts/generate_chXX_answer_key.py` using `scripts/generate_ch07_answer_key.py` as template. The script generates both the Answer Key and Overhead in one run.

File: `Homework/Chapter XX Answer Key.docx`

### 4C: Overhead Answer Key (.docx)

Answer key formatted for classroom projection (22pt font, page breaks between parts).

File: `Homework/Homework XX Overhead.docx`

---

## Step 5: Build and Publish

```bash
python build.py          # Builds both HTML and EPUB
```

Verify:
- No build errors
- `<foreign>` renders as `<i class="foreign">` in HTML
- Grep check: `grep -c 'class="foreign"' docs/ch-XX-*.html`

### Commit Strategy

**Only stage chapter-specific files:**
- `pretext/source/ch-XX.ptx`
- `Homework/Chapter XX Homework.docx`
- `Homework/Chapter XX Answer Key.docx`
- `Homework/Homework XX Overhead.docx`
- `scripts/generate_chXX_answer_key.py`
- `docs/ch-XX-*.html`
- `docs/index.html`, `docs/lunr-pretext-search-index.js`
- `epub/Concise_Guide_to_English_Grammar.epub`
- `.memory/*.md`

**Do NOT stage** other chapters' homework files or pre-existing unstaged changes (PNG files, etc.).

---

## Lessons Learned from Chapter 7

1. **Skip extensive diagram exploration if chapter already has PNGs** — just verify with a quick grep
2. **The homework generation script regenerates ALL chapters** — only commit the target chapter's .docx
3. **Pre-existing unstaged changes exist in the repo** (PNG files ch08-ch16, other homework files) — be careful with `git add`; use specific file paths, never `git add -A`
4. **`&quot;` conversion requires judgment calls** — use the classification shortcut above
5. **Tables with many individual examples** (like Common Labels) have lots of `<foreign>` wraps — these are tedious but mechanical
6. **Section titles can use Unicode quotes** ("...") instead of `&quot;` — PreTeXt handles them fine

## Chapters Completed

- [x] Chapter 1 (formatting only, Tasks 8-15)
- [x] Chapter 2 (formatting only, Tasks 8-15)
- [x] Chapter 3 (formatting only, Tasks 8-15)
- [x] Chapter 4 (formatting only, Tasks 8-15)
- [x] Chapter 5 (formatting only, Tasks 8-15)
- [x] Chapter 6 (formatting only, Tasks 8-15)
- [x] Chapter 7 (full improvement: formatting + homework + Word files, Task 17)
- [x] Chapter 8 (full improvement: formatting + homework + Word files, Task 18)
- [x] Chapter 9 (full improvement: formatting + homework + Word files, Task 19)
- [x] Chapter 10 (full improvement: formatting + homework + Word files, Task 20)
- [x] Chapter 11 (full improvement: formatting + homework + Word files, Task 21)
- [x] Chapter 12 (full improvement: formatting + homework + Word files, Task 22)
- [x] Chapter 13 (full improvement: formatting + homework + Word files, Task 25)
- [x] Chapter 14 (full improvement: formatting + homework + Word files, Task 26)
- [x] Chapter 15 (full improvement: formatting + homework + Word files, Task 27)
- [ ] Chapter 16-21
