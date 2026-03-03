# Desktop Memory Guide

How to read and write project memory from Claude Desktop (Chat or CoWork).
Memory lives in Supabase — use execute_sql to read and write it.

## File Roles

- **state.md** — Current status only. Active threads, what is in flight, what is next.
  Keep it concise. No historical detail — that belongs in the log or knowledge-base.

- **knowledge-base.md** — Stable decisions, solutions, and design patterns, organized by topic.
  Add an entry when something is resolved and worth remembering across sessions.
  Do not record events here — only durable knowledge.

- **logs/SESSION_LOG.md** — One entry per task. Format:
    ## Task N — YYYY-MM-DD
    <one-line summary of what happened>
  Append only. Never edit past entries.

- **project-map.md** — Inventory of all files and what they do.
  Only update when files are added or removed. Do not touch otherwise.

- **project-personality.md** — Project priorities, always/never rules, key gotchas.
  Update when project context or behavior rules change.

## Folder Structure

- **data/memory/** — Core memory. Always current. Updated every consolidation.
- **data/living/** — Living docs with update obligation (project-context, behavior guides,
  architecture, plans). Must stay aligned with memory. Reviewed each consolidation (step 9)
  and fully audited every 100 stops (--alignment). Memory is the source of truth over living.
- **data/static/** — Frozen snapshots. Write-once: research, reports, archives, one-time plans.
  Never edited after initial write. Drop files here for incoming research or session reports.
- **data/personality/** — Behavior and personality files. Unchanged by this split.

## Decision Rule

| What happened | Where it goes |
|---|---|
| Something is resolved and reusable | knowledge-base.md (new topic section) |
| Current status changed | state.md (update in place) |
| A task completed | SESSION_LOG.md (append entry) |
| A file was added or removed | project-map.md (update inventory) |
| Project priorities changed | project-personality.md |

## Formatting Rules

- Match the existing style and heading structure of the file you are editing.
- state.md: update sections in place — do not append history.
- knowledge-base.md: add a new ## heading for each new topic; update existing sections in place.
- SESSION_LOG.md: always append — never rewrite existing entries.
- Keep entries concise. One paragraph per topic is usually enough.

## Document Size Limits

- **knowledge-base.md** and **project-context.md** must stay at **80 lines or fewer**.
- When either document exceeds 80 lines:
  1. Condense by tightening language and merging related topics
  2. Move overflow (oldest/least-active sections) to a dated archive:
     `data/static/knowledge-base-archive-YYYY.md`
  3. Add a pointer in the main doc: `> See knowledge-base-archive-YYYY.md for archived topics`
  4. Add the archive file to project-map.md
- Kickstart sends up to 100 lines as a buffer — but the document target is 80.

## What NOT to Do

- Do not store session-specific context in knowledge-base.md (only stable, reusable knowledge).
- Do not duplicate content across files.
- Do not reformat or restructure files beyond what the edit requires.
- Do not write memory speculatively — only capture things that are confirmed and complete.
