# Memory Consolidation Instructions

## Purpose
This file defines the memory consolidation subagent process. Run at session start by reading and executing these instructions.

## When to Run
- Every session start (triggered by CLAUDE.md session start sequence)
- Every 20 tasks (self-review cycle)

## Consolidation Steps

### 1. Read Current State
Read `.memory/state.md` to understand the current task counter and active threads.

### 2. Check Snapshot Schedule
- State snapshots are saved at every 10th task (t20, t30, t40, etc.)
- If the current task number equals or exceeds the next snapshot threshold, create a snapshot
- Name: `.memory/state-tXX.md` where XX is the task number
- Content: copy of `.memory/state.md` at that moment

### 3. Consolidate Memory Files
Review these files for staleness and compress aggressively:
- `.memory/state.md` — Remove completed items that are fully documented elsewhere
- `.memory/project-map.md` — Update if new files were added/removed
- `.memory/knowledge-base.md` — Add new decisions; archive superseded approaches

### 4. Update project-map.md
If new scripts, Homework files, or source files were created since the last update, add them to the appropriate section of `.memory/project-map.md`.

### 5. Report
Output a brief summary of what was consolidated, snapshotted, or updated.

## Snapshot Format

```markdown
# Project State — Snapshot at Task XX

Task: XX
Snapshot date: YYYY-MM-DD

## Overview
[Same as state.md overview]

## Active Threads
[Same as state.md active threads at time of snapshot]

## Currently Working On
[Same as state.md currently working on]

## Completed Chapters
[Same as state.md completed chapters]

## Next Steps
[Same as state.md next steps]

## Notes
[Same as state.md notes]
```
