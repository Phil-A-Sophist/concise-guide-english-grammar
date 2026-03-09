# Dropzone

This folder is the shared handoff point between Claude Desktop and Claude CLI.

## For Claude Desktop (Chat or CoWork)
Drop incoming files here using Supabase MCP:
  INSERT INTO claude_files (project_id, file_path, content, updated_at)
  VALUES ('{project_id}', 'data/dropzone/your-file.md', $CONTENT$...content...$CONTENT$, now())
  ON CONFLICT (project_id, file_path)
  DO UPDATE SET content = EXCLUDED.content, updated_at = now();

## For Claude CLI
At kickstart, Claude will report any files here. Integrate them where appropriate
(move content to data/memory/, data/living/, or code/ as needed), then delete from dropzone.

## File naming
Use descriptive names: YYYY-MM-DD-topic.md, or just topic.md for timeless content.
