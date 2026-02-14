# Project State

Task: 17
Last updated: 2026-02-14

## Overview
"A Concise Guide to English Grammar" is an open educational resource (OER) college textbook on English grammar, authored in PreTeXt XML (21 chapters) and published as HTML via GitHub Pages and as an EPUB ebook.

## Active Threads
- **Systematic chapter improvement** — Working through chapters one at a time. Process documented in `.memory/chapter-improvement-process.md`. Each chapter gets: diagram audit, `<foreign>` formatting, homework review/fixes, Word file generation, build+push.
- **Language example formatting rollout** — Chapters 1-7 completed. Chapter 8 is next.
- **Homework difficulty calibration** — Chapters 8+ homework was flagged as too difficult. Model after ch4-7 patterns (15-25 exercises, identification-heavy, scaffolded examples).

## Completed in Task 17
- **Chapter 7 `<foreign>` conversion** — All language examples converted from `<em>` to `<foreign>` with context-appropriate markers. ~100+ edits across body text and homework.
- **Chapter 7 homework formatting** — Exercise numbering fixed to `<em>Exercise N.</em>`, labels converted to `<paragraphs><title>` block format. Homework content assessed as appropriate (15 exercises, 5 parts).
- **Chapter 7 Word files** — Generated Chapter 07 Homework.docx, Answer Key.docx, and Homework 07 Overhead.docx. Created `scripts/generate_ch07_answer_key.py`.
- **Process documentation** — Created `.memory/chapter-improvement-process.md` for future sessions.

## Next Steps
- Improve Chapter 8 (next in sequence)
- For each chapter: diagram audit → `<foreign>` conversion → homework fixes → Word files → build+push

## Notes
- **Snapshot reminder:** Create `state-t20.md` at Task 20. No snapshots exist yet.
- **Pre-existing unstaged changes:** PNG diagram files (ch08-ch16) and regenerated homework .docx files (all chapters) remain unstaged. Only commit target chapter's files.
