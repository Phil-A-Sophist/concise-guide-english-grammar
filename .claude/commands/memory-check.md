Run a full health check on this project's memory system. Do not make any changes -- this is a read-only diagnostic.

## Supabase Project Detection

First, check: does `code/meta-agent/db.py` exist in this project directory?

### If YES (Supabase-backed memory project):

Use the Supabase MCP tools to check memory health:

1. Get the project ID:
   ```sql
   SELECT id, name FROM projects WHERE name = 'MemoryBot';
   ```

2. List all files under `data/memory/`:
   ```sql
   SELECT file_path, length(content) as bytes, updated_at
   FROM claude_files
   WHERE project_id = '[id]' AND file_path LIKE 'data/memory/%'
   ORDER BY file_path;
   ```

3. Verify these required files exist: `data/memory/state.md`, `data/memory/project-map.md`, `data/memory/knowledge-base.md`, `data/memory/logs/SESSION_LOG.md`

4. Read `data/memory/state.md` -- verify it has a `Task: {n}` counter and was updated recently.

5. Check for unrouted downloads:
   ```sql
   SELECT file_path FROM claude_files
   WHERE project_id = '[id]' AND file_path LIKE 'data/memory/downloads/%';
   ```

6. Check session log freshness -- compare the highest task number in `SESSION_LOG.md` against the task number in `state.md`. They should be within 1-2 tasks.

Summarize: what's healthy, what needs attention, and any recommended actions.

### If NO (disk-based project):

Check the following:

1. Does `claude_docs/memory/` exist? List all files and folders present.
2. Verify the standard folder structure: state.md, project-map.md, knowledge-base.md, scripts/, reference/, templates/, logs/, downloads/, sub/
3. Report any missing folders or files that should exist.
4. Read state.md -- report the current task count and last update date.
5. Check all downloads/ folders (root and sub-projects) for unrouted items.
6. List all snapshot files (state-t*.md) and their task numbers.
7. Check each sub-project compartment has project-map.md and knowledge-base.md.
8. If this is a git repo, report the current branch and whether there are uncommitted changes.

Summarize: what's healthy, what needs attention, and any recommended actions.
