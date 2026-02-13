# Project State

Task: 5
Last updated: 2026-02-12

## Overview
"A Concise Guide to English Grammar" is an open educational resource (OER) college textbook on English grammar, authored in PreTeXt XML (21 chapters) and published as HTML via GitHub Pages and as an EPUB ebook.

## Active Threads
- **Language example formatting standardization completed for Chapter 6 and STYLE_GUIDE.md** — User approved Chapter 6 formatting. Comprehensive rules now documented in STYLE_GUIDE.md:
  1. `<foreign>` element: all language examples (sans-serif, 0.9em)
  2. `<q><foreign>` for inline examples in paragraphs (quotation marks)
  3. Parentheses only for grouped multiples: `(<example1>, <example2>, ...)`
  4. No markers in lists/tables/block quotes (grey background via CSS sufficient)
  5. `<delete>` for ungrammatical examples (strikethrough)
  6. `<em>` retained only for emphasis, labels, technical terms
  7. Quick reference table and CSS behavior documented for implementation

## Open Questions
- Answer keys exist only for Chapters 4-15; Chapters 1-3 and 16-21 may still need them
- The REVISION_AUDIT.md references an older 27-chapter structure; it has not been updated to reflect the current 21-chapter organization
- Priority order for applying language formatting to remaining chapters (1-5, 7-21)?

## Notes
Chapter 6 formatting approved. STYLE_GUIDE.md now contains comprehensive Language Example Formatting System with PreTeXt XML examples, quick reference table, and CSS behavior documentation. Ready for rollout to all remaining chapters.
