# Project State — Snapshot at Task 20

Task: 20
Snapshot date: 2026-02-14

## Overview
"A Concise Guide to English Grammar" is an open educational resource (OER) college textbook on English grammar, authored in PreTeXt XML (21 chapters) and published as HTML via GitHub Pages and as an EPUB ebook.

## Active Threads
- **Systematic chapter improvement** — Working through chapters one at a time. Process documented in `.memory/chapter-improvement-process.md`. Each chapter gets: diagram audit, `<foreign>` formatting, homework review/fixes, Word file generation, build+push.
- **Language example formatting rollout** — Chapters 1-9 completed. Chapter 10 is next.
- **Homework difficulty calibration** — Chapters 8+ homework was flagged as too difficult. Ch8-9 assessed as appropriate (18 exercises each, 5 parts, scaffolded progression). Continue monitoring for ch10+.

## Completed Chapters
- Chapters 1-6: `<foreign>` formatting only
- Chapter 7: Full structural overhaul (diagrams, MVP tables, step-by-step analysis, homework rewrite)
- Chapter 8: Full improvement (`<foreign>` conversion 213 instances, homework formatting fixes, Word files — committed 426b103)
- Chapter 9: Full improvement (`<foreign>` conversion 113 instances, homework formatting, Word files — committed 858a9b4)

## Next Steps
- Improve Chapter 10 (starting now)
- For each chapter: diagram audit -> `<foreign>` conversion -> homework fixes -> Word files -> build+push

## Notes
- **Pre-existing unstaged changes:** PNG diagram files (ch09-ch16) and regenerated homework .docx files (all chapters) remain unstaged. Only commit target chapter's files.
- **Ch8 unused NP diagrams:** 8 ch08_np_* PNGs exist but are not in the Diagram Examples section. Could add later.
