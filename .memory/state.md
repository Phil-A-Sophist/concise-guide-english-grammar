# Project State

Task: 1
Last updated: 2026-02-12

## Overview
"A Concise Guide to English Grammar" is an open educational resource (OER) college textbook on English grammar, authored in PreTeXt XML (21 chapters) and published as HTML via GitHub Pages and as an EPUB ebook.

## Active Threads
- **Language example formatting overhaul** — Reformatting how language examples appear throughout the textbook. Multi-pronged approach: (1) language examples use sans-serif font at paragraph size, (2) inline examples get parentheses or quotation marks, (3) examples over 150 chars get broken out as block quotes or lists, (4) broken-out examples get indentation and light grey background. Chapter 6 is the test chapter; will expand to other chapters after validation.
- **Prior work:** Incorrect italics were already removed from language examples as a prerequisite step.

## Open Questions
- Answer keys exist only for Chapters 4-15; Chapters 1-3 and 16-21 may still need them
- The REVISION_AUDIT.md references an older 27-chapter structure; it has not been updated to reflect the current 21-chapter organization
- Several chapters (particularly later ones covering advanced structures and applied grammar) may still need content expansion per the audit
- How will the new example formatting be implemented in PreTeXt? Custom CSS classes, `<c>` tags, `<blockquote>` elements, or some other mechanism? Decision pending based on Chapter 6 test results.

## Notes
Memory system initialized from existing project contents on 2026-02-07. Task 1 began 2026-02-12.
