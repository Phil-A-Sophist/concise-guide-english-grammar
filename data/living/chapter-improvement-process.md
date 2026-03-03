# Chapter Improvement Process

Step-by-step process for systematically improving chapters 8-21.
Chapters 1-18 done. Chapter 19 is next.

## Quick Start

When user says "improve Chapter X" or "let's do Chapter X next":
1. Read this file and `data/memory/state.md`
2. Execute Steps 1-4 below in order
3. Build, commit (chapter-specific files only), push

---

## Step 1: Diagram Audit

**Goal:** Ensure chapter uses SyntaxTreeHybrid PNG diagrams, not old SVGs.

1. List PNGs: `assets/diagrams/new/chXX_*`
2. List old SVGs: `assets/diagrams/chXX*`
3. Grep chapter: `<image source=` to see current references
4. If old SVGs referenced → replace paths with new PNGs
5. If no PNGs exist → diagrams may need generation first

---

## Step 2: Style Guide Compliance — `<foreign>` Conversion

**Decision rule:** Text discussed AS a piece of language → `<foreign>`. Emphasis/labels/terms → keep `<em>`.

| Context | Before | After |
|---------|--------|-------|
| Inline in paragraph | `<em>The dog barked.</em>` | `<q><foreign>The dog barked.</foreign></q>` |
| In list item | `<em>the dog</em>` | `<foreign>the dog</foreign>` (bare) |
| In table cell | `the dog, she` | `<foreign>the dog</foreign>, <foreign>she</foreign>` |
| Highlighted word | `<em>The</em> dog` | `<foreign><em>The</em> dog</foreign>` |
| `&quot;word&quot;` | `&quot;dog&quot;` | `<q><foreign>dog</foreign></q>` |
| Grouped examples | `(<em>a, an, the</em>)` | `(<foreign>a, an, the</foreign>)` |
| Ungrammatical | `~~text~~` | `<foreign><delete>text</delete></foreign>` |

**Keep as `<em>`:** Labels ("Example:", "Step 1—"), emphasis, technical terms being introduced, Key Terms line, category labels ("For reading:").

**`&quot;` shortcut:** Followed by "is a", "forms", "modifies", "attaches" → language example → convert. Otherwise keep.

**Efficient strategy:** Work section by section. Within each: tables first → lists → paragraph text. Skip labels and emphasis.

---

## Step 3: Homework Formatting

**3A:** All exercises must use: `<em>Exercise N.</em>` (not bare numbers).

**3B:** Section labels use block format:
```xml
<paragraphs><title>Instructions</title></paragraphs>
<p>instructions text...</p>
<paragraphs><title>Example (completed)</title></paragraphs>
<paragraphs><title>Exercises</title></paragraphs>
```

**3C:** Exercise sentences use bare `<foreign>` (not `<q><foreign>`).

**3D Difficulty check:** 15-25 exercises, 5 parts, 60% identification, scaffolded, 30-60 min.

---

## Step 4: Generate Word Files

- **Student homework:** `cd Homework && python generate_homework_from_pretext.py` (all chapters) → only stage `Chapter XX Homework.docx`
- **Answer key + overhead:** Create/run `scripts/generate_chXX_answer_key.py` (use ch07 script as template)

---

## Step 5: Build and Commit

```bash
python build.py
```

Verify: no build errors, `<foreign>` renders correctly in HTML.

**Commit — only stage chapter-specific files:**
- `pretext/source/ch-XX.ptx`
- `Homework/Chapter XX Homework.docx`, `Answer Key.docx`, `Overhead.docx`
- `scripts/generate_chXX_answer_key.py`
- `docs/ch-XX-*.html`, `docs/index.html`, `docs/lunr-pretext-search-index.js`
- `epub/Concise_Guide_to_English_Grammar.epub`
- `data/memory/*.md`

**Do NOT stage:** Other chapters' homework files, pre-existing unstaged PNGs.

---

## Chapters Status

- [x] Ch1-6: `<foreign>` formatting only
- [x] Ch7: Full overhaul (Tasks 16-17)
- [x] Ch8-18: Full improvement (Tasks 18-34; commit hashes in data/static/knowledge-base-archive-2026.md)
- [ ] Ch19: Organization and Concision — **NEXT**
- [ ] Ch20: Genre and Register
- [ ] Ch21: Teaching Grammar
