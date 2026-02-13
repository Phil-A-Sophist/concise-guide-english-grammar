# Project State

Task: 3
Last updated: 2026-02-12

## Overview
"A Concise Guide to English Grammar" is an open educational resource (OER) college textbook on English grammar, authored in PreTeXt XML (21 chapters) and published as HTML via GitHub Pages and as an EPUB ebook.

## Active Threads
- **Language example formatting refinements** — Two small CSS/XML fixes to Chapter 6:
  1. Font size adjustment for `.foreign` class: reduce from inherit (19px) to 18px
  2. Strikethrough notation fix: replace literal `~~text~~` with proper PreTeXt `<delete>text</delete>` element for ungrammatical examples
  These build on the language example formatting system established in Task 2. After these fixes, Chapter 6 formatting will be complete.

## Open Questions
- Answer keys exist only for Chapters 4-15; Chapters 1-3 and 16-21 may still need them
- The REVISION_AUDIT.md references an older 27-chapter structure; it has not been updated to reflect the current 21-chapter organization
- Several chapters (particularly later ones covering advanced structures and applied grammar) may still need content expansion per the audit
- What is the next chapter to receive the language example formatting treatment after Chapter 6 refinements are complete?

## Notes
Memory system initialized from existing project contents on 2026-02-07. Task 1 began 2026-02-12. Task 2 completed Chapter 6 formatting overhaul with GitHub push. Task 3 applies final refinements to Chapter 6.
