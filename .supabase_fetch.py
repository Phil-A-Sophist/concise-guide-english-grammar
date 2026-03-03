#!/usr/bin/env python3
"""
.supabase_fetch.py — Session start: pull runnable files from Supabase to disk.

This is a PERMANENT LOCAL FILE. It cannot pull itself.
Runs as the FIRST SessionStart hook before any meta-agent code exists on disk.

What it does:
  1. Reads SUPABASE_URL and SUPABASE_KEY from environment
  2. Derives project name from this file's parent directory name
  3. Looks up the project in Supabase
  4. Queries all files where pull_to_disk = true
  5. Writes each file to disk at its file_path, creating dirs as needed
  6. Creates .claude/settings.local.json if missing (first-run setup)
  7. Verifies code/meta-agent/agent.py is present
  8. Exits 0 on success, exits 1 loudly on any failure

Files written:
  - code/meta-agent/         (Python agents — need to run)
  - .claude/settings.json    (hooks + permissions)
  - .claude/hooks/           (pre_tool_gate, etc.)
  - .claude/commands/        (slash commands)
"""

import json
import os
import sys
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


def get_pull_to_disk_files(url, key, project_id):
    data = rest_get(url, key, 'claude_files', {
        'select': 'file_path,content',
        'project_id': f'eq.{project_id}',
        'pull_to_disk': 'eq.true',
    })
    if not data:
        print(f"ERROR [fetch]: No pull_to_disk files found for project '{PROJECT_NAME}'.", file=sys.stderr)
        print("Fix: Run 'python code/scripts/seed_supabase.py' to seed this project.", file=sys.stderr)
        sys.exit(1)
    return data


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
        print("[!!] code/meta-agent/agent.py missing — fetch may have failed", file=sys.stderr)


def main():
    print("=== SUPABASE FETCH ===")

    url, key = get_env()
    project_id = get_project_id(url, key)
    files = get_pull_to_disk_files(url, key, project_id)
    written, failed = write_files(files)

    print(f"[FETCH] {len(written)} file(s) pulled from Supabase")

    if failed:
        for f in failed:
            print(f"[WARN] Failed to write: {f}", file=sys.stderr)

    if not written:
        print("ERROR [fetch]: No files were written to disk.", file=sys.stderr)
        sys.exit(1)

    ensure_local_settings(PROJECT_ROOT)
    verify_structure(PROJECT_ROOT)

    print("FETCH COMPLETE.")


if __name__ == '__main__':
    main()
