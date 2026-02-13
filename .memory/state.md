# Project State

Task: 4
Last updated: 2026-02-12

## Overview
"A Concise Guide to English Grammar" is an open educational resource (OER) college textbook on English grammar, authored in PreTeXt XML (21 chapters) and published as HTML via GitHub Pages and as an EPUB ebook.

## Active Threads
- **Language example formatting standardization in Chapter 6** — Comprehensive pass applying refined marking rules:
  1. Font size reduction: `.foreign` and `q` elements scaled from 0.95em → 0.9em
  2. Standardized marking rules:
     - Paragraphs: quotation marks via `<q>` as default
     - Lists/tables/block quotes: no markers needed (font styling + grey background sufficient)
     - Parentheses: only for grouped multiple examples in a row (e.g., `(some, many, every, three)`)
  3. Full chapter scan underway to apply consistent marking throughout ch-06.ptx
  After this pass, Chapter 6 formatting will be complete and documented for rollout to remaining chapters.

## Open Questions
- Answer keys exist only for Chapters 4-15; Chapters 1-3 and 16-21 may still need them
- The REVISION_AUDIT.md references an older 27-chapter structure; it has not been updated to reflect the current 21-chapter organization
- Which chapters receive the language example formatting treatment next after Chapter 6 is finalized?

## Notes
Memory system initialized from existing project contents on 2026-02-07. Tasks 1-3 completed Ch6 formatting foundation. Task 4 (current) applies final standardization pass and documents the approach for broader rollout.
