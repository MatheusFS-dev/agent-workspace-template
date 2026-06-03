# Project Map

This file is a compact architecture index generated from the repository tree.
It is designed for routing and file-placement decisions, not full documentation.
Agent internals such as scripts, references, assets, and prompt folders are intentionally hidden from normal architecture context.

## Refresh command

Run from the repository root:

```bash
python3 .agent/scripts/update_project_map.py
```

## Scanned root

- `agent-workspace-template`

## Top-level layout

- `.agent`
- `.github`
- `scripts`
- `tests`

Top-level files:

- `.gitignore`
- `AGENTS.md`
- `CITATION.cff`
- `CLAUDE.md`
- `CODE_OF_CONDUCT.md`
- `GEMINI.md`
- `LICENSE`
- `README.md`

## Source roots

None detected.

## Test roots

- `tests`

## Documentation roots

None detected.

## Configuration and dependency files

None detected.

## Entrypoints and executable scripts

None detected.

## Python packages

None detected.

## Notable files by directory

- `./`: `.gitignore`, `AGENTS.md`, `CITATION.cff`, `CLAUDE.md`, `CODE_OF_CONDUCT.md`, `GEMINI.md`, `LICENSE`, `README.md`
- `.agent/`: `index.yaml`
- `.agent/context/`: `memories.md`, `project-map.md`
- `.agent/hooks/`: `claude-code-hooks.example.json`, `README.md`
- `.agent/modes/`: `coding-example-cards.md`, `coding-full-examples.md`, `coding.md`, `easy-task.md`, `paper-writing.md`
- `.agent/rules/`: `plotting-style.md`
- `.agent/skills/scientific-plot-maker/`: `SKILL.md`
- `.agent/skills/scribe/`: `SKILL.md`
- `.agent/workflows/`: `debugging.md`, `long-task-state.md`
- `.github/`: `FUNDING.yml`
- `.github/ISSUE_TEMPLATE/`: `bug_report.md`, `feature_request.md`
- `scripts/`: `install_template.py`

## File-type signal

- `.md`: 20
- `[no extension]`: 2
- `.cff`: 1
- `.yaml`: 1
- `.json`: 1
- `.yml`: 1
- `.py`: 1

## Excluded low-signal paths

- Ignored directories: 4
- Ignored files: 0
- Hidden agent internals: 5

## Maintenance rule

Update this file with `python3 .agent/scripts/update_project_map.py` after significant directory, package, or entrypoint changes.
If this file conflicts with actual source files, trust the source files.
