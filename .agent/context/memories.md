# Agent Memories

Compact durable project context that should survive across agent sessions.

## Rules

- Read only when durable prior context may affect the task or when updating this file.
- Store decisions, constraints, conventions, and project facts that materially affect future work.
- Do not store transient task progress, chat logs, or rules already encoded in `AGENTS.md`, mode files, or source code.
- Prefer one-line bullets grouped by topic.
- Target 500 to 1,200 tokens.
- Remove stale, duplicated, superseded, or low-value entries before adding new context.
- Trust repository files over memories when they disagree.
- After editing, run `python3 .agent/scripts/memory_lint.py` when available.

## Format

```md
## Topic
- YYYY-MM-DD, compact durable memory. Add rationale or affected files only if needed.
```

## Current memories

No durable project-specific memories have been recorded yet.
