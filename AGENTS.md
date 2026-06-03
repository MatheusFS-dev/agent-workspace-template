# AGENTS.md

Repository contract for AI agents. Read this file before planning, editing, or writing.

## Startup

1. Read this file.
2. Before normal routing, apply the Easy Task Gate.
3. If Easy Task Mode does not apply, prefer running `python .agent/scripts/route_context.py "<user request>"` and read only the returned files.
4. For route cost visibility, run `python .agent/scripts/route_context.py --stats "<user request>"`.
5. If script execution is unavailable, read `.agent/index.yaml` and manually apply the same routing.
6. Do not recursively inspect `.agent/`.
7. Do not read prompt libraries, optional skills, references, assets, scripts, PDFs, or `.agent/context/memories.md` during startup.
8. Never run broad startup commands such as `tree .agent`, `find .agent`, `grep -R .agent`, `cat .agent/**`, or equivalent broad reads. Use the router first.

## Easy Task Gate

Use Easy Task Mode only when the request is explicitly small or unambiguously small.

Good easy-task examples:

- answer a simple question,
- change one literal line,
- fix a typo,
- fix Markdown equation rendering,
- replace a short phrase,
- edit only provided text.

When Easy Task Mode applies, read only:

- `AGENTS.md`,
- `.agent/modes/easy-task.md`.

Do not load coding, troubleshooting, paper-writing, plotting, project map, memories, skills, references, or long-task state.

If it is not certain that the task is easy, ask the user before loading more context.

If an easy task becomes non-trivial during execution, stop and ask before escalating.

## Modes and skills

- Easy tasks use `.agent/modes/easy-task.md`.
- Coding tasks use `.agent/modes/coding.md`.
- Coding examples are retrieval-gated. Search `.agent/modes/coding-example-cards.md` when the router emits a search command or when a coding task matches a known risk.
- Full coding examples live in `.agent/modes/examples/` by risk category. Read only the exact risk file when the compact card is insufficient, when the user requests a full example, or when the same failure mode remains ambiguous.
- Paper-writing tasks use `.agent/modes/paper-writing.md` and `.agent/skills/scribe/SKILL.md`.
- Plotting tasks use `.agent/rules/plotting-style.md` and `.agent/skills/scientific-plot-maker/SKILL.md`.
- Repository-analysis tasks use `.agent/context/project-map.md` unless the user explicitly asks for implementation or code editing.
- Troubleshooting tasks use `.agent/workflows/debugging.md` before proposing fixes. Do not load coding mode for troubleshooting unless code editing is explicitly requested.
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

Reference files must be searched with `python .agent/scripts/search_reference.py <file> <keywords...>` before any full read. A full reference read requires a reason: search output was insufficient, the reference itself is being edited, or the user explicitly requested full-reference analysis.

Session state is not a default route. Use `.agent/workflows/long-task-state.md` only on explicit user request, then create the state file at the narrowest relevant task location.

When context appears stale, trust actual repository files over prose context.
