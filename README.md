# A Concise Guide to English Grammar

An open educational resource (OER) textbook for undergraduate English grammar courses.

---

## For AI Assistants (Claude Code)

**IMPORTANT: Before editing or creating any content for this book, you MUST read `STYLE_GUIDE.md` to ensure consistency with existing chapters.**

The style guide defines:
- Header levels and formatting
- Example presentation formats
- List and table conventions
- Homework section structure
- Common mistakes to avoid

**After completing edits, always:**
1. Regenerate the EPUB using `generate_epub.py`
2. Rebuild the web version using `pretext build web`
3. Check both EPUB and HTML output for formatting issues

---

## Project Structure

```
concise_guide_to_english_grammar/
├── chapters/           # Markdown source files for each chapter
├── Homework/           # Separate homework files and answer keys
├── assets/
│   ├── diagrams/       # SVG diagram files
│   └── images/         # Other images
├── guides/             # Reference guides (diagramming, etc.)
├── scripts/            # Generation scripts
├── STYLE_GUIDE.md      # Formatting conventions (READ FIRST)
├── CLAUDE.md           # Project configuration for Claude Code
├── generate_epub.py    # EPUB generation script
└── README.md           # This file
```

---

## Chapter Organization (21 Chapters)

### Foundations (Chapters 1-4)
1. Introduction to Linguistics and Grammar
2. Prescriptive vs. Descriptive Grammar
3. Language Varieties (Sociolinguistics)
4. Morphology and Word Structure

### Core Grammar (Chapters 5-9)
5. Open Classes (nouns, verbs, adjectives, adverbs)
6. Closed Classes (determiners, pronouns, prepositions)
7. Introduction to Sentence Diagramming
8. Basic Sentence Elements and Sentence Patterns
9. Compound and Complex Sentences

### The Verb System (Chapters 10-11)
10. Verbs Part One: Tense and Aspect
11. Verbs Part Two: Voice and Modals

### Form and Function (Chapters 12-15)
12. Adverbials
13. Adjectivals
14. Nominals
15. Punctuation

### Other Topics (Chapters 16-21)
16. Other Grammatical Forms
17. Stylistic Choices
18. Clarity and Readability
19. Organization and Concision
20. Genre and Register
21. Teaching Grammar (L1 and L2)

---

## Building the Book

### Generate EPUB
```bash
cd "Writing Projects/concise_guide_to_english_grammar"
python generate_epub.py
```

### Build Web Version
```bash
cd /path/to/bookmaker
python convert_grammar_to_pretext.py  # Update .ptx files
pretext build web                      # Build HTML
```

### Deploy to GitHub Pages
The `docs/` folder in the bookmaker root contains the web version. After building:
```bash
cp -r output/web/* docs/
```

---

## Key Files

| File | Purpose |
|------|---------|
| `STYLE_GUIDE.md` | **Read first** - Formatting conventions |
| `CLAUDE.md` | Project configuration for Claude Code |
| `generate_epub.py` | Creates EPUB from markdown chapters |
| `guides/Diagramming_Guide.md` | Syntax tree diagram conventions |

---

## Output Formats

- **EPUB**: Primary format, generated from markdown
- **HTML**: Web version via PreTeXt, hosted on GitHub Pages
- **PDF**: Potential future format via PreTeXt

---

## License

This is an Open Educational Resource (OER). See license details in the book's front matter.
