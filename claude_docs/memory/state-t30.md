# Project State — Snapshot at Task 30

Task: 30
Snapshot date: 2026-02-15

## Overview
"A Concise Guide to English Grammar" is an open educational resource (OER) college textbook on English grammar, authored in PreTeXt XML (21 chapters) and published as HTML via GitHub Pages and as an EPUB ebook.

## Active Threads
- **Systematic chapter improvement** — Working through chapters one at a time. Process documented in `.memory/chapter-improvement-process.md`. Each chapter gets: diagram audit, `<foreign>` formatting, homework review/fixes, Word file generation, build+push.
- **Language example formatting rollout** — Chapters 1-16 completed. Chapter 17 is next.
- **Homework difficulty calibration** — Ch8-16 assessed as appropriate (18-26 exercises each, 5 parts, scaffolded progression). Continue monitoring.

## Currently Working On
- **Chapter 17 improvement** (Stylistic Choices) — Next chapter in queue.

## Completed Chapters
- Chapters 1-6: `<foreign>` formatting only
- Chapter 7: Full structural overhaul (diagrams, MVP tables, step-by-step analysis, homework rewrite)
- Chapter 8: Full improvement (213 `<foreign>` instances — 426b103)
- Chapter 9: Full improvement (113 `<foreign>` instances — 858a9b4)
- Chapter 10: Full improvement (181 `<foreign>` instances — c57d00a)
- Chapter 11: Full improvement (174 `<foreign>` instances — 7cc7b51)
- Chapter 12: Full improvement (127 `<foreign>` instances — f0c02fc)
- Chapter 13: Full improvement (131 `<foreign>` instances — de41b9e)
- Chapter 14: Full improvement (147 `<foreign>` instances — 395ae45)
- Chapter 15: Full improvement (98 `<foreign>` instances — 89f308d)
- Chapter 16: Full improvement (126 `<foreign>` instances — b6f048e)

## Next Steps
- Complete Chapter 17 improvement (Stylistic Choices)
- Continue with Chapters 18-21

## Notes
- **Snapshot schedule:** `state-t20.md` and `state-t30.md` exist. Next snapshot at Task 40.
- **Pre-existing unstaged changes:** PNG diagram files (ch08-ch16) and regenerated homework .docx files (all chapters) remain unstaged. Only commit target chapter's files.
- **Ch8 unused NP diagrams:** 8 ch08_np_* PNGs exist but are not in the Diagram Examples section. Could add later.
- **Ch13 note:** Chapter is titled "Adjectivals" (not "Nominals" as listed in some references). Diagram Examples section had misleading "nominal structures" description — corrected to "complement clause structures."
- **Ch14 note:** Chapter titled "Nominals." Diagram Examples section actually contains adjectival structure diagrams — mismatch but left as-is for now.
- **Ch15 note:** No diagrams. Fixed severely malformed apostrophe section headings (lines 276, 283 had `*<em>` asterisk markdown artifacts). Fixed `~~` ungrammatical examples with `<delete>`.
- **Ch16 note:** No diagrams (2 ch16_* PNGs exist but not referenced in chapter). Removed empty objective list item. Homework restructured from flat format (14 Questions, no subsections) to 5-part format (21 Exercises). Added `<term>` for key grammatical terms. Fixed nested `<em><em>` patterns. Converted `~~` parallelism errors to `<delete>`.
