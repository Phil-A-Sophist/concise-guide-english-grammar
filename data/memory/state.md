# Project State: concise-guide-english-grammar

Stops: 59
Last updated: 2026-03-03

## Overview
"A Concise Guide to English Grammar" is an OER college textbook on English grammar (21 chapters). Authored in PreTeXt XML, published as HTML via GitHub Pages and as EPUB. Active development: systematic chapter improvement pipeline, Chapters 19-21 pending.

## Active Threads
- **Systematic chapter improvement** — One at a time. Each: diagram audit, `<foreign>` formatting, homework fixes, Word file, build+push. Process in `data/living/chapter-improvement-process.md`.
- **Language example rollout** — Chapters 1-18 done. Chapter 19 next.
- **Homework calibration** — Ch8-18 appropriate. Monitor.
- **Exam One** — Spring 2026, Ch4-7. Complete.

## Currently Working On
- **Chapter 19** (Organization and Concision) — next in systematic improvement pipeline.

## Completed Chapters
Ch1-6: `<foreign>` only. Ch7: Full overhaul (diagrams, MVP tables, homework rewrite).
Ch8-18: Full improvement (see data/static/knowledge-base-archive-2026.md for individual commit hashes).
- **Ch9 major restructure** (this session): renamed "Conjunctions and Clauses"; added Clauses/Phrases + Conjoined Phrases sections; flip test + subordinating conjunctions merged into Complex Sentences; removed sec-95 (Types of DCs) and sec-96 (Subordinating Conjunctions); replaced sec-99 with Writing section (end-weight, emphasis, clause clarity); updated sec-97 (compound-complex rules, period default for conjunctive adverbs); homework restructured (5 parts, 14 exercises; new Part 4 tables+diagrams, Part 5 emphasis/end-weight).

## Notes
- **Snapshots:** state-t20/t30/t40 in data/static/. Next snapshot at Task 60 (due next).
- **Unstaged:** PNG diagrams (ch08-ch16) and .docx homework files remain unstaged. Commit per-chapter only.
- **Ch13:** Titled "Adjectivals." Diagram section says "complement clause structures" (not nominals).
- **Ch14:** Titled "Nominals" but has adjectival diagrams — mismatch left as-is.
- **Memory system:** Migrated to Supabase architecture (2026-03-03). data/ is git-tracked backup.
- **Homework/:** Gitignored. Files stay local for LMS upload — not tracked in GitHub.
<!-- session-end: 2026-03-03 (session 2) -->