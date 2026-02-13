# Project State

Task: 14
Last updated: 2026-02-13

## Overview
"A Concise Guide to English Grammar" is an open educational resource (OER) college textbook on English grammar, authored in PreTeXt XML (21 chapters) and published as HTML via GitHub Pages and as an EPUB ebook.

## Active Threads
- **Language example formatting rollout in progress** — Chapters 1-3 and 6 completed and committed. Chapters 4-5 currently being edited (unstaged changes in working tree).
  - Formatting rules: `<foreign>` for all language examples (sans-serif, 0.9em), `<q><foreign>` for inline examples, parentheses only for grouped multiples, `<delete>` for ungrammatical, `<em>` for emphasis only
  - Comprehensive documentation in STYLE_GUIDE.md ready for implementation across remaining chapters
- **REVISION_AUDIT.md being updated** — unstaged changes in working tree alongside ch-04/ch-05 edits

## Completed Recently
- REVISION_AUDIT.md fully updated to 21-chapter structure (was referencing old 27-chapter organization)
- Answer key status clarified: Ch 1-3 not needed (open-ended questions), Ch 4-15 exist, Ch 16-21 deferred
- Untracked files resolved: `nul` deleted, `.claude/` added to .gitignore, Diagram Examples folder committed
- Chapters 1-3 language example formatting applied, built, committed, and pushed
- Chapter 6 language example formatting completed (was the pilot chapter)

## Next Steps
- Complete and commit language example formatting for Chapters 4-5
- Continue rollout to Chapters 7-21
- Build HTML/EPUB after each batch of chapter updates
- Monitor REVISION_AUDIT.md for revision priorities

## Notes
- Answer keys: Chapters 4-15 exist; Chapters 1-3 and 16-21 not applicable or deferred
- .gitignore updated to exclude `.claude/` directory from version control
- Working tree has unstaged changes: .gitignore, .memory/state.md, ch-04.ptx, ch-05.ptx, REVISION_AUDIT.md
