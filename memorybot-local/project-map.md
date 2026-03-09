# Project Map: concise-guide-english-grammar

Last updated: 2026-03-08

## Project Identity

- **Git:** github.com/Phil-A-Sophist/concise-guide-english-grammar (git IS the live student site — every push deploys)
- **Supabase project ID:** 5f76a6a4-3840-4a9f-81bc-058b65036be5
- **Supabase MCP project:** hqzchuhewxwrezubqfyf (PKBase-Base)
- **VDB:** Active. Collection: `kb_fragments`. 11 entries seeded. search_kb() hybrid vector+FTS via RRF.
- **Unique architecture:** data/ AND memorybot-local/ are Supabase primary AND local AND git-tracked.

## memorybot_core (Infrastructure stubs — local+Supabase, gitignored)

Thin forwarding stubs pointing to the shared MemoryBot implementation.
Do not add logic here — all meta-agent code lives at C:/Users/irphy/Documents/MemoryBot/memorybot_core/.

- `memorybot_core/agent.py` — Stub: forwards all calls to MemoryBot memorybot_core with --project-root .
- `memorybot_core/db.py` — Supabase REST client (shared infrastructure copy)
- `memorybot_core/hooks/post_write_sync.py` — PostToolUse hook: syncs memorybot-local/, data/, CLAUDE.md, .claude/ to Supabase

## memorybot-local (Project Memory — local+Supabase, git-tracked)

This project's operational memory. Written and maintained by the meta-agent system.

**Core memory**
- `memorybot-local/state.md` — Current project state: Alignment counter, active threads, overview.
- `memorybot-local/project-map.md` — This file
- `memorybot-local/knowledge-base.md` — Design decisions and solutions by topic. ≤80 lines.
- `memorybot-local/CORRECTIONS.md` — Append-only factual corrections

**Personality**
- `memorybot-local/personality.md` — Universal base behaviors: RESEARCH/PLAN/GO protocol
- `memorybot-local/project-personality.md` — Grammar persona, objectives, always/never, key commands

**Logs**
- `memorybot-local/logs/MEMORY_LOG.md` — Diagnostic log: one entry per stop and per task (append-only)
- `memorybot-local/logs/SESSION_LOG.md` — Session history: one entry per task (written at consolidation)

**Snapshots**
- `memorybot-local/snapshots/state-sN.md` — State snapshots at consolidation. 10 most recent kept.

## Root (permanent local — git tracked)

- `CLAUDE.md` — Project OS. ≤60 lines. Boot sequence and file architecture only.
- `.supabase_fetch.py` — Permanent local boot script
- `build.py` — Build script: HTML + EPUB with CSS injection
- `project.ptx` — PreTeXt project configuration
- `requirements.txt` — Python dependencies (PreTeXt 2.36.0)

## Claude Code Config (.claude/ — local+Supabase, gitignored)

- `.claude/settings.json` — Permissions only
- `.claude/settings.local.json` — Machine-specific (gitignored, never Supabase)

## PreTeXt Source (pretext/ — git tracked, single source of truth)

- `pretext/source/main.ptx` — Root document
- `pretext/source/ch-01.ptx` through `ch-21.ptx` — 21 chapters
- `pretext/source/docinfo.ptx`, `frontmatter.ptx`, `backmatter.ptx` — Document structure
- `pretext/config/publication.ptx` — Publication configuration

## Output (generated — never edit directly)

- `docs/` — HTML output served via GitHub Pages
- `epub/` — EPUB output

## Assets (git tracked)

- `assets/diagrams/` — SVG diagrams (ch04-ch16)
- `assets/diagrams/new/` — PNG diagrams via SyntaxTreeHybrid (ch05-ch18)

## Homework (gitignored — local LMS use only)

- `Homework/Chapter XX Homework.docx` — Student files (all 21 chapters)
- `Homework/Chapter XX Answer Key.docx` — Answer keys (Ch4-16, Ch18)
- `Homework/generate_homework_from_pretext.py` — Regenerates ALL chapters (stage only target .docx)
- `Homework/Exams/` — Exam + Study Guide + Bonus assignments

## Reference Materials (git tracked)

- `reference_materials/STYLE_GUIDE.md` — Writing conventions (read before editing content)
- `reference_materials/REVISION_AUDIT.md` — Chapter quality assessment
- `reference_materials/series_bible.md` — Pedagogical approach
- `reference_materials/bracket_notations.txt` — Bracket notation entries

## Living Documents (data/living/ — Supabase AND local AND git-tracked)

- `data/living/chapter-improvement-process.md` — Step-by-step chapter improvement process
- `data/living/project-context.md` — Project overview, build workflow, key rules

## Static Documents (data/static/ — Supabase AND local AND git-tracked)

- `data/static/knowledge-base-archive-2026.md` — Archived KB topics (pre-2026-03-03)
