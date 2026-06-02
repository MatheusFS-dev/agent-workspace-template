# AGENTS.md

Repository contract for AI agents. Read this file before planning, editing, or writing.

## Startup

1. Read this file.
2. Prefer running `python .agent/scripts/route_context.py "<user request>"` and read only the returned files.
3. If script execution is unavailable, read `.agent/index.yaml` and manually apply the same routing.
4. Do not recursively inspect `.agent/`.
5. Do not read prompt libraries, optional skills, references, assets, scripts, PDFs, or `.agent/context/memories.md` during startup.

## Modes and skills

- Coding tasks use `.agent/modes/coding.md`.
- Paper-writing tasks use `.agent/modes/paper-writing.md` and `.agent/skills/scribe/SKILL.md`.
- Plotting tasks use `.agent/rules/plotting-style.md` and `.agent/skills/scientific-plot-maker/SKILL.md`.
- Troubleshooting tasks use `.agent/workflows/debugging.md` before proposing fixes.
- Long-task state uses `.agent/workflows/long-task-state.md` only when the user explicitly asks for task-local state.

## Global behavior

- Be direct, technical, concise, and assumption-aware.
- Separate confirmed facts, assumptions, and uncertainty.
- Prefer minimal changes over broad rewrites.
- Prefer explicit failure over silent fallback behavior.
- Do not add speculative features.
- Do not invent project details, results, citations, reviewer intent, metrics, datasets, or experiments.
- Do not expose secrets, tokens, credentials, API keys, private data, or local machine identifiers.
- Do not commit generated large files, datasets, model weights, logs, or environment files unless explicitly requested.


## Project architecture refresh

When the user asks to populate, refresh, or repair the project architecture context, run `python .agent/scripts/update_project_map.py` from the repository root. Then read `.agent/context/project-map.md` for architecture and file-placement decisions. Do not manually traverse broad repository trees unless the generated map is insufficient.

## Deterministic checks

After Python code edits, run `python .agent/scripts/agent_check.py` when the environment supports it. This script enforces hard coding constraints such as forbidden imports, future annotations, aligned assignments, and missing docstrings.

After editing `.agent/context/memories.md`, run `python .agent/scripts/memory_lint.py` when the environment supports it.

## Context discipline

Read `.agent/context/project-map.md` only when repository structure or file placement matters.

Read `.agent/context/memories.md` only when durable prior context may affect the task, when the user asks to remember or forget something, or when updating durable project context. Keep it compact by pruning stale, duplicated, superseded, or low-value entries.

Session state is not a default route. Use `.agent/workflows/long-task-state.md` only on explicit user request, then create the state file at the narrowest relevant task location.

When context appears stale, trust actual repository files over prose context.
