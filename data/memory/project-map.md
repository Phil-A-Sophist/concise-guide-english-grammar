# Project Map: concise-guide-english-grammar

Last updated: 2026-03-03

## Root (permanent local — git tracked)

- `CLAUDE.md` — Project OS (lean, boot sequence only)
- `.supabase_fetch.py` — Permanent local boot script. Pulls pull_to_disk=True files from Supabase at session start.
- `.gitignore` — Ignores code/, .claude/, build outputs
- `README.md` — Project overview, build instructions, chapter listing
- `build.py` — Build script: HTML + EPUB with CSS injection
- `project.ptx` — PreTeXt project configuration
- `requirements.txt` — Python dependencies (PreTeXt 2.36.0)
- `memory-guide.md` — CoWork reference for memory editing patterns

## PreTeXt Source (pretext/ — git tracked, single source of truth)

- `pretext/source/main.ptx` — Root document
- `pretext/source/ch-01.ptx` through `ch-21.ptx` — 21 chapters
- `pretext/source/docinfo.ptx`, `frontmatter.ptx`, `backmatter.ptx` — Document structure
- `pretext/config/publication.ptx` — Publication configuration

## Output (git tracked)

- `docs/` — HTML output for GitHub Pages
- `epub/` — EPUB output

## Assets (git tracked)

- `assets/diagrams/` — SVG diagrams (ch04-ch16)
- `assets/diagrams/new/` — PNG diagrams via SyntaxTreeHybrid (ch05-ch18)
- `assets/images/diagrams/` — Source images from PowerPoint slides

## Homework (git tracked)

- `Homework/Chapter XX Homework.docx` — Student files (all 21 chapters)
- `Homework/Chapter XX Answer Key.docx` — Answer keys (Ch4-16, Ch18)
- `Homework/Homework XX Overhead.docx` — Projection-format keys (Ch4-16, Ch18)
- `Homework/generate_homework_from_pretext.py` — Generates student .docx files
- `Homework/Exams/` — Exam One + Study Guide + Bonus assignments (.md, .docx, scripts)

## Scripts (git tracked)

- `scripts/generate_diagrams.py`, `generate_new_diagrams.py` — SVG/PNG generation
- `scripts/generate_ch07_answer_key.py` through `ch18` — Chapter-specific answer key scripts
- Various utility scripts (fix_nested_em.py, process_chapters.py, etc.)

## Reference Materials (git tracked)

- `reference_materials/STYLE_GUIDE.md` — Writing conventions, formatting standards
- `reference_materials/REVISION_AUDIT.md` — Chapter quality assessment
- `reference_materials/series_bible.md` — Pedagogical approach
- `reference_materials/bracket_notations.txt` — Bracket notation entries for all diagrams
- `reference_materials/diagram_bracket_notation.md` — Bracket notation reference
- `reference_materials/PPTs/`, `Other Class Materials/` — Instructor materials

## Claude Code Config (.claude/ — pulled from Supabase on boot, gitignored)

- `.claude/settings.json` — Hooks + permissions
- `.claude/settings.local.json` — Machine-specific (gitignored, never Supabase)
- `.claude/commands/` — Custom slash commands
- `.claude/hooks/` — Lifecycle hook scripts

## Meta-Agent Code (code/ — pulled from Supabase on boot, gitignored)

- `code/meta-agent/agent.py` — Entry point
- `code/meta-agent/db.py` — Supabase REST client
- `code/meta-agent/modes/` — bootstrap, kickstart, review, consolidate, finalize, audit

## Memory (data/ — Supabase primary, also local + git tracked)

- `data/memory/state.md` — Current project state
- `data/memory/project-map.md` — This file
- `data/memory/knowledge-base.md` — Design decisions and solutions
- `data/memory/logs/SESSION_LOG.md` — Session log (per-task entries)
- `data/memory/downloads/` — Drop zone for incoming files

## Personality (data/personality/ — Supabase primary, also local + git tracked)

- `data/personality/personality.md` — Universal base behaviors
- `data/personality/project-personality.md` — Grammar project context and behaviors

## Living Documents (data/living/ — Supabase primary, also local + git tracked)

- `data/living/desktop-memory-guide.md` — Memory editing guide for Claude Desktop
- `data/living/chapter-improvement-process.md` — Step-by-step chapter improvement process
- `data/living/project-context.md` — Build workflow, chapter structure, quick reference
- `data/living/solutions.md` — Global solutions reference

## Static Documents (data/static/ — Supabase primary, also local + git tracked)

- `data/static/knowledge-base-archive-2026.md` — Archived KB topics (pre-2026-03-03)
- `data/static/state-t20.md`, `state-t30.md`, `state-t40.md` — State snapshots

## Recently Captured (description pending)
- `Homework/Exams/generate_exam_docx.py` — [captured this session — update description]
- `Homework/Exams/generate_exam_diagrams.py` — [captured this session — update description]
