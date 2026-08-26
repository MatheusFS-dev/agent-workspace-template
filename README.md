```text
    _    ____ _____ _   _ _____
   / \  / ___| ____| \ | |_   _|
  / _ \| |  _|  _| |  \| | | |
 / ___ \ |_| | |___| |\  | | |
/_/   \_\____|_____|_| \_| |_|

__        _____  ____  _  ______ ____   _    ____ _____
\ \      / / _ \|  _ \| |/ / ___|  _ \ / \  / ___| ____|
 \ \ /\ / / | | | |_) | ' /\___ \| |_) / _ \| |   |  _|
  \ V  V /| |_| |  _ <| . \ ___) |  __/ ___ \ |___| |___
   \_/\_/  \___/|_| \_\_|\_\____/|_| /_/   \_\____|_____|

 _____ _____ __  __ ____  _        _  _____ _____
|_   _| ____|  \/  |  _ \| |      / \|_   _| ____|
  | | |  _| | |\/| | |_) | |     / _ \ | | |  _|
  | | | |___| |  | |  __/| |___ / ___ \| | | |___
  |_| |_____|_|  |_|_|   |_____/_/   \_\_| |_____|
```

This repository provides user-scoped rules, tool settings, and reusable skill
packages for Codex, Claude Code, and Antigravity CLI, plus minimal project
instruction files. It intentionally does not install an agent workspace,
project memory, user settings, or skills into a project.

## Template layout

```text
configs/
  antigravity/settings.json
  claude/settings.json
  codex/config.toml.template
  codex/research.config.toml
instructions/
  global.md
project/
  AGENTS.md
  CLAUDE.md
skills/
  <skill-name>/SKILL.md
scripts/
  linux/
    python2/
      install_antigravity.py
      install_claude.py
      install_codex.py
      install_project.py
      requirements.txt
    python3/
      install_antigravity.py
      install_claude.py
      install_codex.py
      install_project.py
  windows/
    install_antigravity.py
    install_claude.py
    install_codex.py
    install_project.py
```

`instructions/global.md` is the only editable global-instructions source.
Codex renders it into `config.toml` at install time. Claude Code and
Antigravity CLI receive that file directly, so there are no duplicate global
instruction templates to keep synchronized.

Every direct `skills/<name>/SKILL.md` folder is a complete global skill package.
The bundled `scribe` package contains its own `scripts/search_reference.py`.

## Install

The primary installers require Python 3.11 or newer. On Linux, run the installer
for the workflow you need with `python3`:

```bash
python3 scripts/linux/python3/install_codex.py
python3 scripts/linux/python3/install_claude.py
python3 scripts/linux/python3/install_antigravity.py
python3 scripts/linux/python3/install_project.py
```

Linux-only Python 2.7 variants are also available. Install the Codex variant's
pinned TOML dependency, then run the required workflow with `python2.7`:

```bash
python2.7 -m pip install -r scripts/linux/python2/requirements.txt
python2.7 scripts/linux/python2/install_codex.py
python2.7 scripts/linux/python2/install_claude.py
python2.7 scripts/linux/python2/install_antigravity.py
python2.7 scripts/linux/python2/install_project.py
```

Only the Python 2.7 Codex installer requires the TOML dependency. The other
Python 2.7 variants use only the standard library.

On Windows, use the Python launcher from PowerShell or Command Prompt:

```powershell
py scripts\windows\install_codex.py
py scripts\windows\install_claude.py
py scripts\windows\install_antigravity.py
py scripts\windows\install_project.py
```

Each script runs one workflow directly, rejects the wrong operating system
before prompting or writing, and does not import another local installer
module. The corresponding `install_global_codex`, `install_global_claude`,
`install_global_antigravity`, and `install_project` functions remain available
for focused Python tests or embedding.

### Global installs

| Tool | Installed paths |
| --- | --- |
| Codex | `~/.codex/config.toml`, selected `~/.codex/*.config.toml` profile files, and `~/.codex/skills/<skill-name>/` |
| Claude Code | `~/.claude/CLAUDE.md`, `~/.claude/settings.json`, and `~/.claude/skills/<skill-name>/` |
| Antigravity CLI | `~/.gemini/GEMINI.md`, `~/.gemini/antigravity-cli/settings.json`, and `~/.gemini/antigravity-cli/skills/<skill-name>/` |

On Windows, `~` is the current `%USERPROFILE%` directory.

Antigravity support is intentionally CLI-only. Its global rules stay in
`~/.gemini/GEMINI.md`; Antigravity CLI discovers global skills from its separate
`~/.gemini/antigravity-cli/skills/` directory. See the
[Antigravity CLI migration guide](https://www.antigravity.google/docs/cli/gcli-migration/)
and [global skills documentation](https://www.antigravity.google/docs/cli/plugins/).

### Project installs

The installer prompts for an existing project directory and a non-empty
selection of `codex`, `antigravity`, and/or `claude`.

- Codex and Antigravity install `AGENTS.md`.
- Claude installs `CLAUDE.md`, which imports `AGENTS.md`.
- Skills and user-level settings are never copied to a project.

Claude Code supports user-level `CLAUDE.md` and project `CLAUDE.md` imports; see
its [memory documentation](https://code.claude.com/docs/en/memory).

After selecting project files, the installer can add the installed instruction
filenames plus `docs/superpowers/specs/` and `docs/superpowers/plans/` to the
target `.gitignore`. The update is idempotent and defaults to no.

## Conflict and backup behavior

Before any write, the selected installer validates its sources and lists all
managed destination paths that already exist. If there are conflicts, one
replacement confirmation is required and defaults to no. If replacement is
accepted, the installer separately asks whether to create backups.

When backups are requested, only conflicting managed paths are copied to unique
timestamped sibling names before replacement. The installer never merges,
silently overwrites, prunes unrelated destinations, or restores failed writes.
It replaces only same-named managed skills and leaves skills that are not in the
source template untouched.

## Add or update a skill

Drop a complete folder containing `SKILL.md` directly under `skills/`, then rerun
the relevant global installer. The installer validates every direct skill package
and copies every valid package for that tool. Project installs intentionally do
not copy skills.

## Verification

Run the focused installer tests:

```bash
python -m unittest tests/test_install_template.py
```

The tests cover platform rejection, source-template validation, single-source
Codex rendering, global destination mappings, complete skill copying, project
selection, repeated `.gitignore` updates, conflict cancellation, replacement,
and optional backups.
