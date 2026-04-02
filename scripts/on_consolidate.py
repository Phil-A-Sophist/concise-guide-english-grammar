#!/usr/bin/env python3
"""
Post-consolidation hook for concise-guide-english-grammar.

Syncs Homework/ folder to:
1. OneDrive — all files (docx, md, py, json) via shutil copy
2. Supabase claude_files — text files (md, py, json) via db.py
3. Supabase Storage — binary files (docx) via httpx upload

Uses MD5 hash manifest for change detection. Only syncs changed files.
"""

import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HOMEWORK_DIR = REPO_ROOT / "Homework"
MANIFEST_FILE = HOMEWORK_DIR / ".sync_manifest.json"

# Text extensions that go to claude_files
TEXT_EXTS = {".md", ".py", ".json"}
# Binary extensions that go to Supabase Storage
BINARY_EXTS = {".docx"}
# All syncable extensions (no PNGs — those live in assets/homework-images/)
SYNC_EXTS = TEXT_EXTS | BINARY_EXTS

# OneDrive path from env var, with fallback
ONEDRIVE_DIR = Path(os.environ.get(
    "HOMEWORK_ONEDRIVE_PATH",
    r"C:\Users\irphy\OneDrive - University of Colorado Colorado Springs"
    r"\++Cloud\+++++Spring26\Concise Guide Homework"
))

# Supabase config
SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
GRAMMAR_PROJECT_ID = "5f76a6a4-3840-4a9f-81bc-058b65036be5"
STORAGE_BUCKET = "grammar-binaries"


def file_hash(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest() -> dict:
    if MANIFEST_FILE.exists():
        return json.loads(MANIFEST_FILE.read_text())
    return {}


def save_manifest(manifest: dict):
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2))


def get_syncable_files() -> dict:
    files = {}
    for path in HOMEWORK_DIR.rglob("*"):
        if path.is_file() and path.suffix in SYNC_EXTS and path.name != ".sync_manifest.json":
            rel = str(path.relative_to(HOMEWORK_DIR))
            files[rel] = {"hash": file_hash(path), "size": path.stat().st_size}
    return files


def diff_manifest(old: dict, current: dict) -> tuple:
    """Returns (changed_paths, deleted_paths)."""
    changed = []
    for rel, info in current.items():
        old_info = old.get(rel)
        if not old_info or old_info.get("hash") != info["hash"]:
            changed.append(rel)
    deleted = [r for r in old if r not in current]
    return changed, deleted


def sync_onedrive(changed: list, deleted: list):
    if not ONEDRIVE_DIR.exists():
        print(f"  [SKIP] OneDrive path not found: {ONEDRIVE_DIR}")
        return
    for rel in changed:
        src = HOMEWORK_DIR / rel
        dst = ONEDRIVE_DIR / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"  [ONEDRIVE] Copied: {rel}")
    for rel in deleted:
        dst = ONEDRIVE_DIR / rel
        if dst.exists():
            dst.unlink()
            print(f"  [ONEDRIVE] Deleted: {rel}")


def sync_text_to_claude_files(changed: list, deleted: list):
    """Sync text files to claude_files table via db.py."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("  [SKIP] SUPABASE_URL/KEY not set — skipping claude_files sync")
        return

    # db.py lives in MemoryBot's memorybot_core/ — use absolute path
    memorybot_core = Path(r"C:\Users\irphy\Documents\MemoryBot\memorybot_core")
    sys.path.insert(0, str(memorybot_core))
    try:
        from db import get_client, write_file, delete_file
        client = get_client()
    except Exception as e:
        print(f"  [WARN] Could not init db client: {e}")
        return

    for rel in changed:
        if Path(rel).suffix not in TEXT_EXTS:
            continue
        src = HOMEWORK_DIR / rel
        try:
            content = src.read_text(encoding="utf-8")
            sb_path = f"Homework/{rel}".replace("\\", "/")
            write_file(client, GRAMMAR_PROJECT_ID, sb_path, content, pull_to_disk=False)
            print(f"  [CLAUDE_FILES] {sb_path}")
        except Exception as e:
            print(f"  [WARN] claude_files write failed ({rel}): {e}")

    for rel in deleted:
        if Path(rel).suffix not in TEXT_EXTS:
            continue
        try:
            sb_path = f"Homework/{rel}".replace("\\", "/")
            delete_file(client, GRAMMAR_PROJECT_ID, sb_path)
            print(f"  [CLAUDE_FILES] Deleted: {sb_path}")
        except Exception as e:
            print(f"  [WARN] claude_files delete failed ({rel}): {e}")


def sync_binary_to_storage(changed: list, deleted: list):
    """Upload binary files (docx) to Supabase Storage bucket via httpx."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("  [SKIP] SUPABASE_URL/KEY not set — skipping Storage sync")
        return

    try:
        import httpx
    except ImportError:
        print("  [SKIP] httpx not installed — skipping Storage sync")
        return

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
    }

    uploaded = 0
    failed = []
    for rel in changed:
        if Path(rel).suffix not in BINARY_EXTS:
            continue
        src = HOMEWORK_DIR / rel
        storage_path = rel.replace("\\", "/")
        with open(src, "rb") as f:
            file_data = f.read()
        ok = False
        for attempt in range(3):
            try:
                resp = httpx.post(
                    f"{SUPABASE_URL}/storage/v1/object/{STORAGE_BUCKET}/{storage_path}",
                    headers={**headers, "x-upsert": "true"},
                    content=file_data,
                    timeout=30.0,
                )
                resp.raise_for_status()
                uploaded += 1
                print(f"  [STORAGE] Uploaded: {storage_path}")
                ok = True
                break
            except Exception as e:
                if attempt < 2:
                    import time; time.sleep(1)
                else:
                    failed.append(rel)
                    print(f"  [WARN] Storage upload failed ({storage_path}): {e}")

    for rel in deleted:
        if Path(rel).suffix not in BINARY_EXTS:
            continue
        storage_path = rel.replace("\\", "/")
        try:
            httpx.delete(
                f"{SUPABASE_URL}/storage/v1/object/{STORAGE_BUCKET}/{storage_path}",
                headers=headers,
                timeout=15.0,
            )
            print(f"  [STORAGE] Deleted: {storage_path}")
        except Exception as e:
            print(f"  [WARN] Storage delete failed ({storage_path}): {e}")

    if uploaded:
        print(f"  [STORAGE] {uploaded} file(s) uploaded")
    return failed


def main():
    if not HOMEWORK_DIR.exists():
        print("[ON_CONSOLIDATE] No Homework/ directory — skipping")
        return

    old_manifest = load_manifest()
    current = get_syncable_files()
    changed, deleted = diff_manifest(old_manifest, current)

    if not changed and not deleted:
        print("[ON_CONSOLIDATE] Homework: no changes detected")
        return

    print(f"[ON_CONSOLIDATE] Homework: {len(changed)} changed, {len(deleted)} deleted")

    sync_onedrive(changed, deleted)
    sync_text_to_claude_files(changed, deleted)
    storage_failed = sync_binary_to_storage(changed, deleted) or []

    # Exclude failed uploads from manifest so they retry next run
    for rel in storage_failed:
        current.pop(rel, None)

    save_manifest(current)
    print("[ON_CONSOLIDATE] Homework sync complete")


if __name__ == "__main__":
    main()
