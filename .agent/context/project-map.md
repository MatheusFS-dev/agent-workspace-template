# Project Map

This file is a compact architecture index generated from the repository tree.
It is designed for routing and file-placement decisions, not full documentation.

## Refresh command

Run from the repository root:

```bash
python .agent/scripts/update_project_map.py
```

## Scanned root

- `project-template`

## Top-level layout

- `.agent`

Top-level files:

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`

## Source roots

None detected.

## Test roots

None detected.

## Documentation roots

None detected.

## Configuration and dependency files

None detected.

## Entrypoints and executable scripts

None detected.

## Python packages

None detected.

## Notable files by directory

- `./`: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`
- `.agent/`: `index.yaml`
- `.agent/context/`: `memories.md`, `project-map.md`
- `.agent/hooks/`: `claude-code-hooks.example.json`, `README.md`
- `.agent/modes/`: `coding.md`, `paper-writing.md`
- `.agent/rules/`: `plotting-style.md`
- `.agent/scripts/`: `agent_check.py`, `memory_lint.py`, `route_context.py`, `search_reference.py`, `update_project_map.py`
- `.agent/skills/scientific-plot-maker/`: `SKILL.md`
- `.agent/skills/scientific-plot-maker/references/`: `plot_examples.py`, `publication_plot_style.py`
- `.agent/skills/scientific-plot-maker/scripts/`: `install_plot_style.py`, `preview_plot_style.py`
- `.agent/skills/scribe/`: `SKILL.md`
- `.agent/skills/scribe/references/`: `scribe-style-guide.md`, `writing-guide-pages-27-52.md`
- `.agent/workflows/`: `debugging.md`, `long-task-state.md`

## File-type signal

- `.md`: 15
- `.py`: 9
- `.yaml`: 1
- `.json`: 1

## Excluded low-signal paths

- Ignored directories: 0
- Ignored files: 0

## Maintenance rule

Update this file with `python .agent/scripts/update_project_map.py` after significant directory, package, or entrypoint changes.
If this file conflicts with actual source files, trust the source files.
