![Agent Workspace Template header](https://capsule-render.vercel.app/api?height=190&type=blur&color=7f5af0&section=header&text=Agent%20Workspace%20Template&fontColor=fffffe&fontSize=42)

<div align="center">

```text
 █████╗  ██████╗ ███████╗███╗   ██╗████████╗    ██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗███████╗██████╗  █████╗  ██████╗███████╗    ████████╗███████╗███╗   ███╗██████╗ ██╗      █████╗ ████████╗███████╗
██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝    ██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝    ╚══██╔══╝██╔════╝████╗ ████║██╔══██╗██║     ██╔══██╗╚══██╔══╝██╔════╝
███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║       ██║ █╗ ██║██║   ██║██████╔╝█████╔╝ ███████╗██████╔╝███████║██║     █████╗         ██║   █████╗  ██╔████╔██║██████╔╝██║     ███████║   ██║   █████╗  
██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║       ██║███╗██║██║   ██║██╔══██╗██╔═██╗ ╚════██║██╔═══╝ ██╔══██║██║     ██╔══╝         ██║   ██╔══╝  ██║╚██╔╝██║██╔═══╝ ██║     ██╔══██║   ██║   ██╔══╝  
██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║       ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗███████║██║     ██║  ██║╚██████╗███████╗       ██║   ███████╗██║ ╚═╝ ██║██║     ███████╗██║  ██║   ██║   ███████╗
╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝        ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝       ╚═╝   ╚══════╝╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
                                                                                                                                                                                              
```

</div>

<p align="center">
  <a href="https://github.com/DenverCoder1/readme-typing-svg"><img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&color=%237F5AF0&size=22&center=true&vCenter=true&width=760&height=32&lines=Reusable%20configurations%20for%20coding%20agents" alt="Reusable configurations for coding agents" /></a>
</p>

<p align="center">
  <a href="https://github.com/MatheusFS-dev/agent-workspace-template/blob/main/LICENSE"><img src="https://img.shields.io/github/license/MatheusFS-dev/agent-workspace-template?style=flat-square" alt="License" /></a>
  <a href="https://github.com/MatheusFS-dev/agent-workspace-template/stargazers"><img src="https://img.shields.io/github/stars/MatheusFS-dev/agent-workspace-template?style=flat-square" alt="Stars" /></a>
  <a href="https://github.com/MatheusFS-dev/agent-workspace-template/network/members"><img src="https://img.shields.io/github/forks/MatheusFS-dev/agent-workspace-template?style=flat-square" alt="Forks" /></a>
  <a href="https://visitor-badge.laobi.icu/badge?page_id=MatheusFS-dev.agent-workspace-template"><img src="https://visitor-badge.laobi.icu/badge?page_id=MatheusFS-dev.agent-workspace-template" alt="Visitors" /></a>
</p>

This repository provides user-scoped rules, tool settings, and reusable skill
packages for Codex, Claude Code, Antigravity CLI, and OpenCode, plus minimal project
instruction files. It intentionally does not install an agent workspace,
project memory, user settings, or skills into a project.

## Table of Contents

- [my-toolbox Integration](#my-toolbox-integration)
- [Template Layout](#template-layout)
- [Installation](#installation)
- [Conflict and Backup Behavior](#conflict-and-backup-behavior)
- [Add or Update a Skill](#add-or-update-a-skill)
- [Verification](#verification)
- [Contributing](#contributing)
- [License](#license)
- [Collaborators](#collaborators)

## my-toolbox Integration

This repository is maintained as a Git submodule of [my-toolbox](https://github.com/MatheusFS-dev/my-toolbox) at `assets/payload/packages/agent-workspace-template`. Provides the user-scoped agent configurations, reusable skills, and project instruction templates bundled by my-toolbox.

To initialize the submodules in an existing my-toolbox checkout, run this from its repository root:

```bash
git submodule update --init --recursive
```

Changes to this component belong in this repository. The parent repository pins the component to a specific commit through its submodule reference.

## Template Layout

```text
configs/
  antigravity/settings.json
  claude/settings.json
  codex/config.toml.template
  opencode/opencode.json
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
      install_opencode.py
      install_codex.py
      install_project.py
      requirements.txt
    python3/
      install_antigravity.py
      install_claude.py
      install_opencode.py
      install_codex.py
      install_project.py
  windows/
    install_antigravity.py
    install_claude.py
    install_opencode.py
    install_codex.py
    install_project.py
```

`instructions/global.md` is the only editable global-instructions source.
Codex renders it into `config.toml` at install time. Claude Code and
Antigravity CLI receive that file directly, so there are no duplicate global
instruction templates to keep synchronized.

Every direct `skills/<name>/SKILL.md` folder is a complete global skill package.
The bundled `scribe` package contains its own `scripts/search_reference.py`.

## Installation

The primary installers require Python 3.9 or newer. On Linux, run the installer
for the workflow you need with `python3`:

```bash
python3 scripts/linux/python3/install_codex.py
python3 scripts/linux/python3/install_claude.py
python3 scripts/linux/python3/install_antigravity.py
python3 scripts/linux/python3/install_opencode.py
python3 scripts/linux/python3/install_project.py
```

On Python 3.9 and 3.10, the Codex installers use the bundled Tomli 2.2.1 TOML
parser fallback; no package installation is required.

Linux-only Python 2.7 variants are also available. Install the Codex variant's
pinned TOML dependency, then run the required workflow with `python2.7`:

```bash
python2.7 -m pip install -r scripts/linux/python2/requirements.txt
python2.7 scripts/linux/python2/install_codex.py
python2.7 scripts/linux/python2/install_claude.py
python2.7 scripts/linux/python2/install_antigravity.py
python2.7 scripts/linux/python2/install_opencode.py
python2.7 scripts/linux/python2/install_project.py
```

Only the Python 2.7 Codex installer requires the TOML dependency. The other
Python 2.7 variants use only the standard library.

On Windows, use the Python launcher from PowerShell or Command Prompt:

```powershell
py scripts\windows\install_codex.py
py scripts\windows\install_claude.py
py scripts\windows\install_antigravity.py
py scripts\windows\install_opencode.py
py scripts\windows\install_project.py
```

Each script runs one workflow directly, rejects the wrong operating system
before prompting or writing, and does not import another local installer
module. The corresponding `install_global_codex`, `install_global_claude`,
`install_global_antigravity`, `install_global_opencode`, and `install_project` functions remain available
for focused Python tests or embedding.

### Global installs

| Tool | Installed paths |
| --- | --- |
| Codex | `~/.codex/config.toml`, selected `~/.codex/*.config.toml` profile files, and `~/.codex/skills/<skill-name>/` |
| Claude Code | `~/.claude/CLAUDE.md`, `~/.claude/settings.json`, `~/.claude/statusline.py`, and `~/.claude/skills/<skill-name>/` |
| Antigravity CLI | `~/.gemini/GEMINI.md`, `~/.gemini/antigravity-cli/settings.json`, `~/.gemini/antigravity-cli/statusline.py`, and `~/.gemini/antigravity-cli/skills/<skill-name>/` |
| OpenCode | `~/.config/opencode/AGENTS.md`, `~/.config/opencode/opencode.json`, and `~/.config/opencode/skills/<skill-name>/` |

On Windows, `~` is the current `%USERPROFILE%` directory.

The default status lines show the active model and reasoning level, current
folder, context used, and 5-hour and weekly usage. Codex renders these natively;
Claude Code and Antigravity CLI run their installed `statusline.py` formatter.

Antigravity support is intentionally CLI-only. Its global rules stay in
`~/.gemini/GEMINI.md`; Antigravity CLI discovers global skills from its separate
`~/.gemini/antigravity-cli/skills/` directory. See the
[Antigravity CLI migration guide](https://www.antigravity.google/docs/cli/gcli-migration/)
and [global skills documentation](https://www.antigravity.google/docs/cli/plugins/).

### Project installs

The installer prompts for an existing project directory and a non-empty
selection of `codex`, `antigravity`, `claude`, and/or `opencode`.

- Codex, Antigravity, and OpenCode install `AGENTS.md`.
- Claude installs `CLAUDE.md`, which imports `AGENTS.md`.
- Skills and user-level settings are never copied to a project.

Claude Code supports user-level `CLAUDE.md` and project `CLAUDE.md` imports; see
its [memory documentation](https://code.claude.com/docs/en/memory).

After selecting project files, the installer can add the installed instruction
filenames plus `docs/superpowers/specs/` and `docs/superpowers/plans/` to the
target `.gitignore`. The update is idempotent and defaults to no.

## Conflict and Backup Behavior

Before any write, the selected installer validates its sources and lists all
managed destination paths that already exist. If there are conflicts, one
replacement confirmation is required and defaults to no. If replacement is
accepted, the installer separately asks whether to create backups.

When backups are requested, only conflicting managed paths are copied to unique
timestamped sibling names before replacement. The installer never merges,
silently overwrites, prunes unrelated destinations, or restores failed writes.
It replaces only same-named managed skills and leaves skills that are not in the
source template untouched.

## Add or Update a Skill

Drop a complete folder containing `SKILL.md` directly under `skills/`, then rerun
the relevant global installer. The installer validates every direct skill package
and copies every valid package for that tool. Project installs intentionally do
not copy skills.

## Verification

Run the focused installer tests:

```bash
python3 -m unittest discover -s tests -v
```

The tests cover platform rejection, source-template validation, single-source
Codex rendering, global destination mappings, complete skill copying, project
selection, repeated `.gitignore` updates, conflict cancellation, replacement,
and optional backups.

## Contributing

> [!IMPORTANT]
> Read the [Code of Conduct](CODE_OF_CONDUCT.md) and run the installer tests in [Verification](#verification) before opening a pull request. Keep `instructions/global.md` as the single global-instructions source.

1. Fork this repository.
2. Create a focused branch from `main`.
3. Commit a scoped change with its verification.
4. Push the branch to your fork.
5. Open a pull request describing the change and checks performed.

## License

This project is licensed under the [Apache License 2.0](LICENSE), the same license used by my-toolbox. Third-party components retain their own license notices.

## Collaborators

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/MatheusFS-dev" title="Matheus Ferreira Silva">
        <img src="https://avatars.githubusercontent.com/u/99222557?v=4" width="100px" alt="Matheus Ferreira Silva's GitHub avatar" /><br />
        <sub><b>Matheus Ferreira Silva</b></sub>
      </a>
    </td>
  </tr>
</table>
