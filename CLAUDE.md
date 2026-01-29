# Claude Code Project Configuration

## Concise Guide to English Grammar

This file contains project-specific instructions for Claude Code sessions.

---

## Project Overview

- **Type:** Open educational resource (OER) college textbook
- **Subject:** English grammar for undergraduate students
- **Structure:** 21 chapters organized thematically
- **Output formats:** EPUB (primary), potential future HTML/PDF

---

## Diagram Creation

When creating or modifying sentence diagrams, **always reference `guides/Diagramming_Guide.md`** for:
- Style conventions and node labels
- Bracket notation syntax
- Generation workflow
- Common structure templates

### Key Files

| File | Purpose |
|------|---------|
| `guides/Diagramming_Guide.md` | Authoritative reference for all diagrams |
| `documents/diagram_sources.txt` | Master file with bracket notation |
| `scripts/generate_diagrams.py` | SVG generation script |
| `assets/diagrams/*.svg` | Generated diagram images |

### Workflow for New Diagrams

1. Add bracket notation to `documents/diagram_sources.txt`
2. Run `python scripts/generate_diagrams.py`
3. Insert image reference in markdown: `![caption](assets/diagrams/filename.svg)`
4. Test with `python generate_epub.py`

### Style Requirements

- **Blue (#0000FF):** Category labels (S, NP, VP, etc.)
- **Green (#008000):** Terminal words
- Use standard abbreviations: S, NP, VP, PP, AdjP, AdvP, N, V, Adj, Adv, Det, Pro, Aux, Modal

---

## EPUB Generation

Generate EPUB with:
```bash
python generate_epub.py
```

Images are loaded from `assets/images/diagrams/renamed/` and `assets/diagrams/`.

---

## Chapter Organization (21 Chapters)

### Foundations (Chapters 1-4)
1. Introduction to Linguistics and Grammar
2. Prescriptive vs. Descriptive Grammar
3. Sociolinguistics
4. Morphology

### Core Grammar (Chapters 5-9)
5. Open Classes (nouns, verbs, adjectives, adverbs and their phrases)
6. Closed Classes (determiners, pronouns, prepositions; PP functions)
7. Introduction to Sentence Diagramming
8. Basic Sentence Elements and Sentence Patterns
9. Compound and Complex Sentences

### The Verb System (Chapters 10-11)
10. Verbs Part One: Tense and Aspect
11. Verbs Part Two: Voice and Modals

### Form and Function (Chapters 12-15)
12. Adverbials
13. Nominals
14. Adjectivals
15. Other Grammatical Forms

### Writing and Style (Chapters 16-19)
16. Stylistic Choices
17. Punctuation
18. Clarity and Readability
19. Organization and Concision

### Applied Grammar (Chapters 20-21)
20. Genre and Register
21. Teaching Grammar (L1 and L2)

---

## Key Conventions

- Chapter headers use format: `# N. Chapter Title` (not "Chapter N:")
- Internal section numbers match chapter: Chapter 8 has sections 8.1, 8.2, etc.
- Cross-references use chapter numbers: "as discussed in Chapter 6"
- ASCII diagrams are being replaced with SVG images
- Tables use standard markdown format
- Examples use *italics* for linguistic data

---

## Instructor Materials

Reference materials from the instructor are in:
- `reference_materials/PPTs/` - PowerPoint presentations
- `reference_materials/Other Class Materials/` - Handouts and tests
- `assets/images/diagrams/` - Extracted diagram images

These materials inform style decisions but are not part of the textbook itself.
