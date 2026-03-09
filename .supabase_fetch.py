#!/usr/bin/env python3
"""
.supabase_fetch.py — Session start: pull runnable files from Supabase to disk.

This is a PERMANENT LOCAL FILE. It cannot pull itself.
Runs as the FIRST SessionStart hook before any meta-agent code exists on disk.

What it does:
  1. Reads SUPABASE_URL and SUPABASE_KEY from environment
  2. Derives project name from this file's parent directory name
  3. Looks up the project in Supabase
  4. Fetches metadata (file_path, updated_at) for all pull_to_disk=true files
  5. Compares against .sync_manifest.json — skips files that are up to date
  6. Pulls content only for missing or stale files
  7. Creates .claude/settings.local.json if missing (first-run setup)
  8. Verifies code/meta-agent/agent.py is present
  9. Exits 0 on success, exits 1 loudly on any failure

Files written:
  Dirty pull_to_disk=true files: data/, code/meta-agent/, .claude/ (settings, hooks, commands)
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
PROJECT_NAME = PROJECT_ROOT.name  # e.g. "MemoryBot"


def get_env():
    url = os.environ.get('SUPABASE_URL', '').rstrip('/')
    key = os.environ.get('SUPABASE_KEY', '')

    if not url:
        print("ERROR [fetch]: SUPABASE_URL is not set.", file=sys.stderr)
        print("Fix: Add SUPABASE_URL to your system environment variables and restart.", file=sys.stderr)
        sys.exit(1)
    if not key:
        print("ERROR [fetch]: SUPABASE_KEY is not set.", file=sys.stderr)
        print("Fix: Add SUPABASE_KEY to your system environment variables and restart.", file=sys.stderr)
        sys.exit(1)

    return url, key


def make_headers(key):
    return {
        'apikey': key,
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json',
    }


def rest_get(url, key, table, params):
    try:
        import httpx
    except ImportError:
        print("ERROR [fetch]: httpx is not installed.", file=sys.stderr)
        print("Fix: Run 'pip install httpx'", file=sys.stderr)
        sys.exit(1)

    try:
        response = httpx.get(
            f'{url}/rest/v1/{table}',
            headers=make_headers(key),
            params=params,
            timeout=15.0,
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"ERROR [fetch]: Could not reach Supabase: {e}", file=sys.stderr)
        print("Fix: Check your internet connection and SUPABASE_URL.", file=sys.stderr)
        sys.exit(1)


def get_project_id(url, key):
    data = rest_get(url, key, 'projects', {
        'select': 'id',
        'name': f'eq.{PROJECT_NAME}',
    })
    if not data:
        print(f"ERROR [fetch]: Project '{PROJECT_NAME}' not found in Supabase.", file=sys.stderr)
        print("Fix: Run 'python code/scripts/seed_supabase.py' to seed this project.", file=sys.stderr)
        sys.exit(1)
    return data[0]['id']


def get_file_metadata(url, key, project_id):
    """Fetch file_path + updated_at for all pull_to_disk files — no content."""
    data = rest_get(url, key, 'claude_files', {
        'select': 'file_path,updated_at',
        'project_id': f'eq.{project_id}',
        'pull_to_disk': 'eq.true',
    })
    if not data:
        print(f"ERROR [fetch]: No pull_to_disk files found for project '{PROJECT_NAME}'.", file=sys.stderr)
        print("Fix: Run 'python code/scripts/seed_supabase.py' to seed this project.", file=sys.stderr)
        sys.exit(1)
    return data


def load_manifest(project_root):
    """Load existing .sync_manifest.json. Returns file_path -> entry dict."""
    manifest_path = project_root / '.sync_manifest.json'
    if not manifest_path.exists():
        return {}
    try:
        data = json.loads(manifest_path.read_text(encoding='utf-8'))
        return data.get('files', {})
    except Exception:
        return {}


def get_dirty_paths(metadata, manifest, project_root):
    """Return file_paths that need pulling: local missing or Supabase updated_at changed."""
    dirty = []
    for row in metadata:
        file_path = row['file_path']
        supabase_updated_at = row.get('updated_at', '')
        local_file = project_root / file_path
        manifest_entry = manifest.get(file_path, {})

        if not local_file.exists():
            dirty.append(file_path)
        elif manifest_entry.get('supabase_updated_at', '') != supabase_updated_at:
            dirty.append(file_path)

    return dirty


def fetch_content_for_paths(url, key, project_id, file_paths):
    """Fetch file_path + content for a specific set of paths using IN filter."""
    if not file_paths:
        return []
    paths_str = ','.join(f'"{p}"' for p in file_paths)
    data = rest_get(url, key, 'claude_files', {
        'select': 'file_path,content,updated_at',
        'project_id': f'eq.{project_id}',
        'file_path': f'in.({paths_str})',
    })
    return data or []


def write_files(files):
    written = []
    failed = []

    for row in files:
        file_path = row['file_path']
        content = row['content']
        dest = PROJECT_ROOT / file_path

        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content, encoding='utf-8')
            written.append(file_path)
        except Exception as e:
            failed.append(f"{file_path}: {e}")

    return written, failed


def ensure_local_settings(project_root):
    """Create .claude/settings.local.json if it doesn't exist (first-run setup)."""
    local_settings = project_root / ".claude" / "settings.local.json"
    if not local_settings.exists():
        default = {
            "$schema": "https://json.schemastore.org/claude-code-settings.json",
            "permissions": {"allow": [], "deny": []}
        }
        local_settings.parent.mkdir(parents=True, exist_ok=True)
        local_settings.write_text(json.dumps(default, indent=2), encoding="utf-8")
        print("[NEW] settings.local.json created")
    else:
        print("[OK] settings.local.json exists")


def verify_structure(project_root):
    """Verify that critical files landed on disk after the fetch."""
    agent = project_root / "code" / "meta-agent" / "agent.py"
    if agent.exists():
        print("[OK] Structure verified")
    else:
        print("[!!] code/meta-agent/agent.py missing -- fetch may have failed", file=sys.stderr)


def build_manifest(project_id, project_root, metadata, written, existing_manifest):
    """Rebuild manifest: carry over clean entries, compute fresh SHA256 for written files."""
    updated_at_map = {row['file_path']: row.get('updated_at', '') for row in metadata}
    written_set = set(written)

    manifest = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'project_id': project_id,
        'files': {},
    }

    # Carry over entries for files that were not re-pulled
    for file_path, entry in existing_manifest.items():
        if file_path not in written_set and file_path in updated_at_map:
            manifest['files'][file_path] = {
                'sha256': entry['sha256'],
                'supabase_updated_at': updated_at_map[file_path],
                'size_bytes': entry.get('size_bytes', 0),
            }

    # Compute fresh SHA256 for newly written files
    for file_path in written:
        dest = project_root / file_path
        try:
            content_bytes = dest.read_bytes()
            sha256 = hashlib.sha256(content_bytes).hexdigest()
            manifest['files'][file_path] = {
                'sha256': sha256,
                'supabase_updated_at': updated_at_map.get(file_path, ''),
                'size_bytes': len(content_bytes),
            }
        except Exception:
            pass

    manifest_path = project_root / '.sync_manifest.json'
    try:
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
        print(f"[MANIFEST] {len(manifest['files'])} file(s) hashed -> .sync_manifest.json")
    except Exception as e:
        print(f"[WARN] Could not write manifest: {e}", file=sys.stderr)


def main():
    print("=== SUPABASE FETCH ===")

    url, key = get_env()
    project_id = get_project_id(url, key)

    # Phase 1: metadata only — no content downloaded yet
    metadata = get_file_metadata(url, key, project_id)
    existing_manifest = load_manifest(PROJECT_ROOT)
    dirty_paths = get_dirty_paths(metadata, existing_manifest, PROJECT_ROOT)

    total = len(metadata)
    skipped = total - len(dirty_paths)

    # Phase 2: fetch content only for dirty files
    if dirty_paths:
        files_to_write = fetch_content_for_paths(url, key, project_id, dirty_paths)
        written, failed = write_files(files_to_write)
    else:
        written, failed = [], []

    print(f"[FETCH] {len(written)} file(s) pulled, {skipped} skipped (up to date)")

    if failed:
        for f in failed:
            print(f"[WARN] Failed to write: {f}", file=sys.stderr)

    if not written and not skipped:
        print("ERROR [fetch]: No files were written to disk.", file=sys.stderr)
        sys.exit(1)

    ensure_local_settings(PROJECT_ROOT)
    verify_structure(PROJECT_ROOT)
    build_manifest(project_id, PROJECT_ROOT, metadata, written, existing_manifest)

    print("FETCH COMPLETE.")


if __name__ == '__main__':
    main()
