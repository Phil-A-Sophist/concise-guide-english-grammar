# Project State

Task: 29
Last updated: 2026-02-15

## Overview
"A Concise Guide to English Grammar" is an open educational resource (OER) college textbook on English grammar, authored in PreTeXt XML (21 chapters) and published as HTML via GitHub Pages and as an EPUB ebook.

## Active Threads
- **Systematic chapter improvement** — Working through chapters one at a time. Process documented in `.memory/chapter-improvement-process.md`. Each chapter gets: diagram audit, `<foreign>` formatting, homework review/fixes, Word file generation, build+push.
- **Language example formatting rollout** — Chapters 1-15 completed. Chapter 16 is next.
- **Homework difficulty calibration** — Ch8-15 assessed as appropriate (18-26 exercises each, 5 parts, scaffolded progression). Continue monitoring.

## Currently Working On
- **Chapter 16 improvement** (Other Grammatical Forms) — Next chapter in queue.

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

## Next Steps
- Complete Chapter 16 improvement (Other Grammatical Forms)
- Continue with Chapters 17-21

## Notes
- **Snapshot schedule:** `state-t20.md` exists. Next snapshot at Task 30.
- **Pre-existing unstaged changes:** PNG diagram files (ch08-ch16) and regenerated homework .docx files (all chapters) remain unstaged. Only commit target chapter's files.
- **Ch8 unused NP diagrams:** 8 ch08_np_* PNGs exist but are not in the Diagram Examples section. Could add later.
- **Ch13 note:** Chapter is titled "Adjectivals" (not "Nominals" as listed in some references). Diagram Examples section had misleading "nominal structures" description — corrected to "complement clause structures."
- **Ch14 note:** Chapter titled "Nominals." Diagram Examples section actually contains adjectival structure diagrams — mismatch but left as-is for now.
- **Ch15 note:** No diagrams. Fixed severely malformed apostrophe section headings (lines 276, 283 had `*<em>` asterisk markdown artifacts). Fixed `~~` ungrammatical examples with `<delete>`.
