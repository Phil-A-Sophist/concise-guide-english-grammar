# Project State

Task: 39
Last updated: 2026-02-16

## Overview
"A Concise Guide to English Grammar" is an open educational resource (OER) college textbook on English grammar, authored in PreTeXt XML (21 chapters) and published as HTML via GitHub Pages and as an EPUB ebook.

## Active Threads
- **Systematic chapter improvement** — Working through chapters one at a time. Process documented in `.memory/chapter-improvement-process.md`. Each chapter gets: diagram audit, `<foreign>` formatting, homework review/fixes, Word file generation, build+push.
- **Language example formatting rollout** — Chapters 1-18 completed. Chapter 19 is next.
- **Homework difficulty calibration** — Ch8-18 assessed as appropriate (18-26 exercises each, 5 parts, scaffolded progression). Continue monitoring.
- **Exam One creation** — Exam One (Spring 2026, Chapters 4-7) completed: student exam, answer key with diagrams, .docx generation script. All SyntaxTreeHybrid diagrams generated and embedded.

## Currently Working On
- **Chapter 19 improvement** (Organization and Concision) — Next in the systematic improvement pipeline.

## Completed Chapters
- Chapters 1-6: `<foreign>` formatting only
- Chapter 7: Full structural overhaul (diagrams, MVP tables, step-by-step analysis, homework rewrite)
- Chapter 8: Full improvement (213 `<foreign>` instances -- 426b103)
- Chapter 9: Full improvement (113 `<foreign>` instances -- 858a9b4)
- Chapter 10: Full improvement (181 `<foreign>` instances -- c57d00a)
- Chapter 11: Full improvement (174 `<foreign>` instances -- 7cc7b51)
- Chapter 12: Full improvement (127 `<foreign>` instances -- f0c02fc)
- Chapter 13: Full improvement (131 `<foreign>` instances -- de41b9e)
- Chapter 14: Full improvement (147 `<foreign>` instances -- 395ae45)
- Chapter 15: Full improvement (98 `<foreign>` instances -- 89f308d)
- Chapter 16: Full improvement (126 `<foreign>` instances -- b6f048e)
- Chapter 17: Full improvement (Stylistic Choices -- 1899dee)
- Chapter 18: Full improvement (83 `<foreign>` instances, 20 exercises -- 9e56a92, answer key 1b8c3b2)

## Next Steps
- Improve Chapter 19 (Organization and Concision)
- Continue with Chapters 20-21

## Notes
- **Snapshot schedule:** `state-t20.md` and `state-t30.md` exist. Next snapshot at Task 40.
- **Pre-existing unstaged changes:** PNG diagram files (ch08-ch16) and regenerated homework .docx files (all chapters) remain unstaged. Only commit target chapter's files.
- **Ch8 unused NP diagrams:** 8 ch08_np_* PNGs exist but are not in the Diagram Examples section. Could add later.
- **Ch13 note:** Chapter is titled "Adjectivals" (not "Nominals" as listed in some references). Diagram Examples section had misleading "nominal structures" description -- corrected to "complement clause structures."
- **Ch14 note:** Chapter titled "Nominals." Diagram Examples section actually contains adjectival structure diagrams -- mismatch but left as-is for now.
- **Ch15 note:** No diagrams. Fixed severely malformed apostrophe section headings. Fixed `~~` ungrammatical examples with `<delete>`.
- **Ch16 note:** No diagrams. Homework restructured from flat format to 5-part format.
- **Ch17 note:** No diagrams. Homework restructured to 5-part format. No answer key script yet.
- **Ch18 note:** No diagrams. Added Chapter Summary section. Homework restructured to 5-part format (20 exercises). Answer key and overhead committed (1b8c3b2).
- **Exam One:** Covers Chapters 4-7. 100 pts + 10 bonus. .docx generation script at `Homework/Exams/generate_exam_docx.py`.
