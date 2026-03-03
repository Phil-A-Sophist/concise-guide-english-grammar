# Project Personality: concise-guide-english-grammar

---

## Snapshot

"A Concise Guide to English Grammar" is an open educational resource (OER) college textbook for undergraduate English grammar courses. 21 chapters organized thematically. Authored in PreTeXt XML, published via GitHub Pages (HTML) and EPUB. Active development: systematic chapter improvement pipeline, chapters 19-21 pending.

**Stack:** PreTeXt XML · Python build script · GitHub Pages · Pandoc (EPUB)
**Repo:** Phil-A-Sophist/concise-guide-english-grammar — live deployment to students. Git is both version control AND the live site.

---

## Current Priorities

1. Systematic chapter improvement pipeline — Ch19 next, then Ch20-21
2. Each chapter: diagram audit → `<foreign>` formatting → homework fixes → Word files → build+push
3. Process documented in `data/living/chapter-improvement-process.md`

---

## Always / Never

**Always:**
- Commit and push after each chapter improvement — the repo IS the live student site
- Only commit chapter-specific files — pre-existing unstaged PNG/docx files exist in many chapters
- Run `python build.py` and verify before committing
- Update `data/memory/project-map.md` when adding new files
- Reference `reference_materials/STYLE_GUIDE.md` before editing PreTeXt content
- Write changes to Supabase as you go (but data/ is also local+git — both are source of truth)

**Never:**
- Edit docs/ or epub/ directly — they are generated outputs
- Edit PreTeXt source files that aren't the current chapter without explicit instruction
- Use `git add -A` or `git add .` — always add specific files to avoid staging wrong chapters
- Commit exam answer keys or instructor materials without explicit user confirmation

**When in doubt:**
- Check data/living/chapter-improvement-process.md for the exact chapter improvement steps
- Check data/memory/knowledge-base.md for past decisions on formatting, homework, diagrams
- Ask before committing anything touching multiple chapters

---

## Key Gotchas

- **Live site:** Every push to GitHub updates the student-facing textbook. Be careful.
- **Pre-existing unstaged changes:** PNG diagrams (ch08-ch16) and .docx homework files exist but are intentionally unstaged. Do NOT commit them accidentally.
- **Homework script:** `generate_homework_from_pretext.py` regenerates ALL chapters. Only stage the target chapter's .docx.
- **PreTeXt:** `pretext/source/` is the single source of truth. `docs/` and `epub/` are generated.
- **Supabase + local:** data/ is both Supabase AND git-tracked (unlike other projects). Both are current.
- **Python:** Use `python` (system). No venv needed for meta-agent. PreTeXt builds may need the venv.

---

## Workflow

Open project → meta-agent bootstraps → work on chapter → build → verify locally → commit specific files → push.

---

## Key Commands

- `python build.py` — Build HTML and EPUB
- `python code/meta-agent/agent.py --kickstart` — Load session memory
- `python code/meta-agent/agent.py --consolidate` — Run consolidation
- `cd Homework && python generate_homework_from_pretext.py` — Generate student .docx files
