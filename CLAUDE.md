# concise-guide-english-grammar

## Normal Startup
Hooks run automatically. Proceed in RESEARCH mode once kickstart completes.

## If Kickstart Failed
Run: `python memorybot_core/agent.py --kickstart`
Or manually read: memorybot-local/personality.md, memorybot-local/state.md,
memorybot-local/project-map.md, memorybot-local/knowledge-base.md

## Claude Desktop
Call `grammar_kickstart()` via MCP server. If unavailable, use Supabase MCP
to read the above files from project id: 5f76a6a4-3840-4a9f-81bc-058b65036be5.
Drop incoming files at data/dropzone/.

## File Architecture

```
concise-guide-english-grammar/
├── CLAUDE.md              <- This file (permanent local — lean OS only)
├── .supabase_fetch.py     <- Permanent local — first boot, pulls everything else
├── memorybot_core/        <- Stubs pointing to shared MemoryBot implementation (gitignored)
├── memorybot-local/       <- This project's memory (state, map, KB, personality, logs)
├── .claude/               <- Permissions + settings (gitignored)
├── data/                  <- Supabase AND local AND git-tracked (unique to this project)
│   ├── living/            <- Active reference docs with update obligation
│   ├── static/            <- Write-once plans and archives
│   └── dropzone/          <- Desktop ↔ CLI handoff
└── pretext/               <- PreTeXt XML source (single source of truth for book content)
```

## Git
**This is a live student site.** Every push updates the student-facing textbook immediately.
- `data/` and `memorybot-local/` ARE git-tracked (project content + memory backup).
- `memorybot_core/` and `.claude/` are gitignored (pulled from Supabase).
- For chapter work: always commit chapter-specific files only. Never `git add -A`.

## New Machine Setup
Clone repo → set SUPABASE_URL and SUPABASE_KEY env vars → open Claude Code → done.

## Self-Management
- **This file:** Under 60 lines. No project content, behavior, or permissions here.
- **personality.md / project-personality.md:** Live in Supabase at memorybot-local/.
- **settings.json:** Permissions only. Hooks are in global ~/.claude/settings.json.
