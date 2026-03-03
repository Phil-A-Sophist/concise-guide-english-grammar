# Project State: concise-guide-english-grammar

Stops: 52
Last updated: 2026-03-03

## Overview
"A Concise Guide to English Grammar" is an OER college textbook on English grammar (21 chapters). Authored in PreTeXt XML, published as HTML via GitHub Pages and as EPUB. Active development: systematic chapter improvement pipeline, Chapters 19-21 pending.

## Active Threads
- **Systematic chapter improvement** — One at a time. Each: diagram audit, `<foreign>` formatting, homework fixes, Word file, build+push. Process in `data/living/chapter-improvement-process.md`.
- **Language example rollout** — Chapters 1-18 done. Chapter 19 next.
- **Homework calibration** — Ch8-18 appropriate (18-26 exercises, 5 parts, scaffolded). Monitor.
- **Exam One** — Spring 2026, Ch4-7. Complete. Q24 updated (prepositional phrase question, "for wizards" sentence).

## Currently Working On
- **Chapter 19** (Organization and Concision) — next in systematic improvement pipeline.

## Completed Chapters
Ch1-6: `<foreign>` only. Ch7: Full overhaul (diagrams, MVP tables, homework rewrite).
Ch8-18: Full improvement (see data/static/knowledge-base-archive-2026.md for individual commit hashes).

## Notes
- **Snapshots:** state-t20/t30/t40 in data/static/. Next snapshot at Task 50.
- **Inline diagrams added:** Ch8-13 each have 8 new inline syntax tree diagrams (48 total). Script: scripts/generate_ch08_13_diagrams.py.
- **Ch13:** Titled "Adjectivals." Diagram section says "complement clause structures" (not nominals).
- **Ch14:** Titled "Nominals" but has adjectival diagrams — mismatch left as-is.
- **Memory system:** Migrated to Supabase architecture (2026-03-03). data/ is git-tracked backup.
- **Homework/:** Gitignored. Files stay local for LMS upload — not tracked in GitHub.
<!-- session-end: 2026-03-03 -->