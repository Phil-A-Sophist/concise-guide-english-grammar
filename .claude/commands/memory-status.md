Quick status view of the memory system. No changes -- just read and report.

## Supabase Project Detection

First, check: does `code/meta-agent/db.py` exist in this project directory?

### If YES (Supabase-backed memory project):

Use the Supabase MCP `execute_sql` tool:

1. Get the project ID and read state.md:
   ```sql
   SELECT cf.content
   FROM claude_files cf
   JOIN projects p ON cf.project_id = p.id
   WHERE p.name = 'MemoryBot' AND cf.file_path = 'data/memory/state.md';
   ```

2. Display the full contents of state.md.
3. Note the task count and last update date.
4. Check for items in downloads/:
   ```sql
   SELECT file_path FROM claude_files cf
   JOIN projects p ON cf.project_id = p.id
   WHERE p.name = 'MemoryBot' AND cf.file_path LIKE 'data/memory/downloads/%';
   ```
5. List any downloads found.

### If NO (disk-based project):

1. Display the current contents of `claude_docs/memory/state.md`.
2. Note the task count and last update date.
3. List any items sitting in downloads/ folders (root and sub-projects).
4. If any sub-projects exist, show one-line status for each.
