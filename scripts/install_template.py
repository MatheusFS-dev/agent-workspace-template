#!/usr/bin/env python3
"""Install global or project-scoped assets from this portable template."""

from datetime import datetime
import json
from pathlib import Path
import shutil
import sys
import tomllib
from typing import Callable


GLOBAL_INSTRUCTIONS_PLACEHOLDER = "{{GLOBAL_INSTRUCTIONS}}"
GITIGNORE_HEADER = "# Agent workspace template"
InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], None]
InstallItem = tuple[Path | None, Path, str | None]


def get_template_root() -> Path:
    """Return the template repository root derived from this script location.

    Args:
        None.

    Returns:
        Path: Absolute repository root containing the template source tree.

    Raises:
        None.
    """
    return Path(__file__).resolve().parent.parent


def render_codex_config(template_root: Path) -> str:
    """Render Codex configuration from the sole global instructions source.

    Args:
        template_root: Absolute template repository root containing
            `configs/codex/config.toml.template` and `instructions/global.md`.

    Returns:
        str: TOML configuration with the global instructions embedded.

    Raises:
        RuntimeError: If the template has any number of placeholders other than
            one, the instructions contain a TOML multiline-string delimiter, or
            the rendered result is invalid TOML.
        OSError: If either source file cannot be read.
    """
    config_path = template_root / "configs" / "codex" / "config.toml.template"
    instructions_path = template_root / "instructions" / "global.md"
    config_text = config_path.read_text(encoding="utf-8")
    instructions_text = instructions_path.read_text(encoding="utf-8")

    placeholder_count = config_text.count(GLOBAL_INSTRUCTIONS_PLACEHOLDER)
    if placeholder_count != 1:
        raise RuntimeError(
            "Codex configuration template must contain exactly one "
            f"{GLOBAL_INSTRUCTIONS_PLACEHOLDER!r} placeholder; found "
            f"{placeholder_count}."
        )
    if "'''" in instructions_text:
        raise RuntimeError(
            "Global instructions cannot contain three consecutive single quotes "
            "because they are rendered into a TOML multiline literal."
        )

    rendered = config_text.replace(GLOBAL_INSTRUCTIONS_PLACEHOLDER, instructions_text)
    if GLOBAL_INSTRUCTIONS_PLACEHOLDER in rendered:
        raise RuntimeError("Rendered Codex configuration still contains a placeholder.")

    try:
        tomllib.loads(rendered)
    except tomllib.TOMLDecodeError as error:
        raise RuntimeError(f"Rendered Codex configuration is invalid TOML: {error}") from error

    return rendered


def validate_sources(template_root: Path) -> list[Path]:
    """Validate all template sources before an installer can write files.

    Args:
        template_root: Absolute template repository root to validate.

    Returns:
        list[Path]: Sorted source skill package directories. Each package has a
        direct `SKILL.md` file and is safe to copy as a complete folder.

    Raises:
        RuntimeError: If a required source is missing, JSON or rendered TOML is
            invalid, or a direct skill package does not contain `SKILL.md`.
        OSError: If a source cannot be read or enumerated.
    """
    required_paths = (
        template_root / "instructions" / "global.md",
        template_root / "configs" / "codex" / "config.toml.template",
        template_root / "configs" / "claude" / "settings.json",
        template_root / "configs" / "antigravity" / "settings.json",
        template_root / "project" / "AGENTS.md",
        template_root / "project" / "CLAUDE.md",
        template_root / "skills",
    )
    missing_paths = [path for path in required_paths if not path.exists()]
    if missing_paths:
        missing_text = ", ".join(str(path) for path in missing_paths)
        raise RuntimeError(f"Template source is missing: {missing_text}")

    for settings_path in (
        template_root / "configs" / "claude" / "settings.json",
        template_root / "configs" / "antigravity" / "settings.json",
    ):
        try:
            json.loads(settings_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise RuntimeError(f"Invalid JSON source {settings_path}: {error}") from error

    render_codex_config(template_root)

    skills_root = template_root / "skills"
    skill_packages = sorted(path for path in skills_root.iterdir() if path.is_dir())
    invalid_packages = [
        package for package in skill_packages
        if not (package / "SKILL.md").is_file()
    ]
    if invalid_packages:
        invalid_text = ", ".join(str(path) for path in invalid_packages)
        raise RuntimeError(
            "Every source skill must be a direct skills/<name>/SKILL.md package: "
            f"{invalid_text}"
        )

    return skill_packages


def prompt_target_root(input_function: InputFunction) -> Path:
    """Prompt for an existing destination project directory.

    Args:
        input_function: Prompt callable, normally `input`, which receives the
            prompt text and returns the user's response.

    Returns:
        Path: Resolved existing project directory selected by the user.

    Raises:
        ValueError: If the response is empty.
        FileNotFoundError: If the supplied directory does not exist.
        NotADirectoryError: If the supplied path is not a directory.
    """
    target_text = input_function("Target project directory: ").strip()
    if not target_text:
        raise ValueError("Target project directory cannot be empty.")

    target_root = Path(target_text).expanduser().resolve()
    if not target_root.exists():
        raise FileNotFoundError(f"Target project directory does not exist: {target_root}")
    if not target_root.is_dir():
        raise NotADirectoryError(f"Target project path is not a directory: {target_root}")
    return target_root


def prompt_codex_profiles(template_root: Path, input_function: InputFunction) -> list[Path]:
    """Prompt for optional Codex profiles to install with the base config.

    Args:
        template_root: Absolute template repository root containing
            `configs/codex/*.config.toml` profile files.
        input_function: Prompt callable, normally `input`, which receives the
            prompt text and returns the user's response.

    Returns:
        list[Path]: Selected profile source files. An empty response returns no
        profiles and installs only the base configuration.

    Raises:
        ValueError: If a name is unknown or repeated.
        OSError: If the profile directory cannot be enumerated.
    """
    profiles = sorted((template_root / "configs" / "codex").glob("*.config.toml"))
    if not profiles:
        return []

    profile_by_name = {
        profile.name.removesuffix(".config.toml"): profile for profile in profiles
    }
    available_names = ", ".join(profile_by_name)
    response = input_function(
        f"Codex profiles to install ({available_names}; blank for none): "
    ).strip()
    if not response:
        return []

    selected_names = [name.strip() for name in response.split(",")]
    if not all(selected_names):
        raise ValueError("Codex profile selection cannot contain an empty name.")
    if len(set(selected_names)) != len(selected_names):
        raise ValueError("Codex profile selection cannot repeat a profile.")

    unknown_names = [name for name in selected_names if name not in profile_by_name]
    if unknown_names:
        raise ValueError(f"Unknown Codex profile: {', '.join(unknown_names)}")
    return [profile_by_name[name] for name in selected_names]


def prompt_project_tools(input_function: InputFunction) -> set[str]:
    """Prompt for the project instruction formats to install.

    Args:
        input_function: Prompt callable, normally `input`, which receives the
            prompt text and returns the user's response.

    Returns:
        set[str]: Non-empty selection from `codex`, `antigravity`, and `claude`.

    Raises:
        ValueError: If the response is empty, contains empty values, repeats a
            tool, or contains a tool outside the accepted set.
    """
    response = input_function(
        "Project tools (codex, antigravity, claude; comma-separated): "
    ).strip().lower()
    if not response:
        raise ValueError("Choose at least one project tool.")

    selected_tools = [tool.strip() for tool in response.split(",")]
    if not all(selected_tools):
        raise ValueError("Project tool selection cannot contain an empty value.")
    if len(set(selected_tools)) != len(selected_tools):
        raise ValueError("Project tool selection cannot repeat a tool.")

    allowed_tools = {"codex", "antigravity", "claude"}
    unknown_tools = sorted(set(selected_tools) - allowed_tools)
    if unknown_tools:
        raise ValueError(f"Unknown project tool: {', '.join(unknown_tools)}")
    return set(selected_tools)


def prompt_yes_no(prompt: str, input_function: InputFunction) -> bool:
    """Prompt for an explicit yes or no response with a no default.

    Args:
        prompt: Full prompt text, including any displayed default.
        input_function: Prompt callable, normally `input`, which receives the
            prompt text and returns the user's response.

    Returns:
        bool: True for `y` or `yes`; false for `n`, `no`, or an empty response.

    Raises:
        ValueError: If the response is not an accepted yes/no value.
    """
    response = input_function(prompt).strip().lower()
    if response in ("", "n", "no"):
        return False
    if response in ("y", "yes"):
        return True
    raise ValueError("Enter yes, y, no, n, or press Enter for no.")


def path_exists(path: Path) -> bool:
    """Return whether a path exists, including a dangling symbolic link.

    Args:
        path: Filesystem path to inspect.

    Returns:
        bool: True when the path exists or is a symbolic link.

    Raises:
        None.
    """
    return path.exists() or path.is_symlink()


def backup_path(destination_path: Path) -> Path:
    """Create a unique timestamped adjacent backup pathname.

    Args:
        destination_path: Existing path that will be copied before replacement.

    Returns:
        Path: Non-existing sibling path ending in a timestamped backup suffix.

    Raises:
        None.
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    candidate = destination_path.with_name(
        f"{destination_path.name}.backup-{timestamp}"
    )
    counter = 1
    while path_exists(candidate):
        candidate = destination_path.with_name(
            f"{destination_path.name}.backup-{timestamp}-{counter}"
        )
        counter += 1
    return candidate


def copy_backup(destination_path: Path) -> Path:
    """Copy an existing managed destination to an adjacent backup path.

    Args:
        destination_path: Existing file, directory, or symbolic link to copy.

    Returns:
        Path: New backup path containing the destination's pre-replacement
        content or symbolic-link metadata.

    Raises:
        OSError: If the source cannot be copied or the backup cannot be made.
    """
    backup_destination = backup_path(destination_path)
    if destination_path.is_dir() and not destination_path.is_symlink():
        shutil.copytree(destination_path, backup_destination, symlinks=True)
    else:
        shutil.copy2(destination_path, backup_destination, follow_symlinks=False)
    return backup_destination


def remove_destination(destination_path: Path) -> None:
    """Remove a managed destination before replacing it with a full copy.

    Args:
        destination_path: Existing file, directory, or symbolic link to remove.

    Returns:
        None: The path no longer exists after a successful call.

    Raises:
        OSError: If the destination cannot be removed.
    """
    if destination_path.is_dir() and not destination_path.is_symlink():
        shutil.rmtree(destination_path)
    elif path_exists(destination_path):
        destination_path.unlink()


def replace_path(source_path: Path | None, destination_path: Path, content: str | None) -> None:
    """Replace a destination with either a source copy or rendered text.

    Args:
        source_path: Existing source file or directory to copy when `content` is
            None. It must be None when rendered text is supplied.
        destination_path: Target file or directory to replace completely.
        content: Rendered UTF-8 text to write when not None. This branch writes
            a file and never reads `source_path`; the other branch copies the
            supplied source path as a file or complete directory tree.

    Returns:
        None: The destination is replaced in place.

    Raises:
        RuntimeError: If neither or both source forms are supplied.
        FileNotFoundError: If a requested copy source does not exist.
        OSError: If removal, copying, or writing fails.
    """
    if (source_path is None) == (content is None):
        raise RuntimeError("Installation item must provide exactly one source form.")
    if source_path is not None and not path_exists(source_path):
        raise FileNotFoundError(f"Installation source does not exist: {source_path}")

    if path_exists(destination_path):
        remove_destination(destination_path)
    destination_path.parent.mkdir(parents=True, exist_ok=True)

    if content is not None:
        destination_path.write_text(content, encoding="utf-8")
    elif source_path is not None and source_path.is_dir():
        shutil.copytree(source_path, destination_path, symlinks=True)
    elif source_path is not None:
        shutil.copy2(source_path, destination_path, follow_symlinks=False)


def install_items(
    items: list[InstallItem],
    input_function: InputFunction,
    output_function: OutputFunction,
) -> bool:
    """Confirm conflicts, optionally back them up, and install all items.

    Args:
        items: Source, destination, and optional rendered-content tuples. Each
            destination is replaced as a complete managed path.
        input_function: Prompt callable used only when conflicts exist.
        output_function: Reporting callable used to list conflicts and backups.

    Returns:
        bool: True after all items are installed. False only when the user
        declines replacement; then this function makes no filesystem changes.

    Raises:
        OSError: If a requested backup, removal, copy, or write fails.
        ValueError: If an interactive confirmation is invalid.
    """
    conflicts = [destination for _, destination, _ in items if path_exists(destination)]
    if conflicts:
        output_function("Conflicting managed destinations:")
        for destination in conflicts:
            output_function(f"- {destination}")
        if not prompt_yes_no("Replace all listed paths? [y/N]: ", input_function):
            output_function("Installation cancelled; no files were changed.")
            return False
        if prompt_yes_no("Create backups of conflicting paths? [y/N]: ", input_function):
            for destination in conflicts:
                output_function(f"Backed up {destination} to {copy_backup(destination)}")

    for source_path, destination_path, content in items:
        replace_path(source_path, destination_path, content)
    return True


def global_skill_items(skill_packages: list[Path], destination_root: Path) -> list[InstallItem]:
    """Build complete skill-package copy items for one global tool directory.

    Args:
        skill_packages: Valid direct `skills/<name>` source package directories.
        destination_root: Tool-specific global skills directory that receives
            every package under its original directory name.

    Returns:
        list[InstallItem]: One complete-directory copy item per skill package.

    Raises:
        None.
    """
    return [(package, destination_root / package.name, None) for package in skill_packages]


def install_global_codex(
    template_root: Path | None = None,
    home_root: Path | None = None,
    input_function: InputFunction = input,
    output_function: OutputFunction = print,
) -> bool:
    """Interactively install the Codex global configuration, profiles, and skills.

    Args:
        template_root: Template root to use. None derives it from this script.
        home_root: User home directory to target. None uses `Path.home()`.
        input_function: Prompt callable for profile and conflict decisions.
        output_function: Reporting callable for conflicts, backups, and result.

    Returns:
        bool: True after installation, or false if conflict replacement is
        declined before any files are changed.

    Raises:
        RuntimeError: If template validation or rendered TOML validation fails.
        OSError: If files cannot be read, backed up, copied, or written.
        ValueError: If a selected profile or confirmation is invalid.
    """
    root = template_root or get_template_root()
    home = home_root or Path.home()
    skill_packages = validate_sources(root)
    selected_profiles = prompt_codex_profiles(root, input_function)
    codex_root = home / ".codex"
    items = [(None, codex_root / "config.toml", render_codex_config(root))]
    items.extend((profile, codex_root / profile.name, None) for profile in selected_profiles)
    items.extend(global_skill_items(skill_packages, codex_root / "skills"))
    installed = install_items(items, input_function, output_function)
    if installed:
        output_function(f"Installed Codex global template into {codex_root}")
    return installed


def install_global_claude(
    template_root: Path | None = None,
    home_root: Path | None = None,
    input_function: InputFunction = input,
    output_function: OutputFunction = print,
) -> bool:
    """Interactively install Claude global instructions, settings, and skills.

    Args:
        template_root: Template root to use. None derives it from this script.
        home_root: User home directory to target. None uses `Path.home()`.
        input_function: Prompt callable for conflict decisions.
        output_function: Reporting callable for conflicts, backups, and result.

    Returns:
        bool: True after installation, or false if conflict replacement is
        declined before any files are changed.

    Raises:
        RuntimeError: If template validation fails.
        OSError: If files cannot be read, backed up, copied, or written.
        ValueError: If a confirmation is invalid.
    """
    root = template_root or get_template_root()
    home = home_root or Path.home()
    skill_packages = validate_sources(root)
    claude_root = home / ".claude"
    items = [
        (root / "instructions" / "global.md", claude_root / "CLAUDE.md", None),
        (root / "configs" / "claude" / "settings.json", claude_root / "settings.json", None),
    ]
    items.extend(global_skill_items(skill_packages, claude_root / "skills"))
    installed = install_items(items, input_function, output_function)
    if installed:
        output_function(f"Installed Claude global template into {claude_root}")
    return installed


def install_global_antigravity(
    template_root: Path | None = None,
    home_root: Path | None = None,
    input_function: InputFunction = input,
    output_function: OutputFunction = print,
) -> bool:
    """Interactively install Antigravity CLI global rules, settings, and skills.

    Args:
        template_root: Template root to use. None derives it from this script.
        home_root: User home directory to target. None uses `Path.home()`.
        input_function: Prompt callable for conflict decisions.
        output_function: Reporting callable for conflicts, backups, and result.

    Returns:
        bool: True after installation, or false if conflict replacement is
        declined before any files are changed.

    Raises:
        RuntimeError: If template validation fails.
        OSError: If files cannot be read, backed up, copied, or written.
        ValueError: If a confirmation is invalid.
    """
    root = template_root or get_template_root()
    home = home_root or Path.home()
    skill_packages = validate_sources(root)
    gemini_root = home / ".gemini"
    antigravity_root = gemini_root / "antigravity-cli"
    items = [
        (root / "instructions" / "global.md", gemini_root / "GEMINI.md", None),
        (
            root / "configs" / "antigravity" / "settings.json",
            antigravity_root / "settings.json",
            None,
        ),
    ]
    items.extend(global_skill_items(skill_packages, antigravity_root / "skills"))
    installed = install_items(items, input_function, output_function)
    if installed:
        output_function(f"Installed Antigravity CLI global template into {gemini_root}")
    return installed


def prompt_gitignore_update(
    instruction_names: list[str],
    input_function: InputFunction,
) -> bool:
    """Prompt whether installed project instruction filenames enter `.gitignore`.

    Args:
        instruction_names: Installed project instruction filenames, limited to
            `AGENTS.md` and `CLAUDE.md` by the project installer.
        input_function: Prompt callable for the yes/no decision.

    Returns:
        bool: True when the caller should idempotently update `.gitignore`.

    Raises:
        ValueError: If the yes/no response is invalid.
    """
    names = ", ".join(instruction_names)
    return prompt_yes_no(f"Add {names} to .gitignore? [y/N]: ", input_function)


def update_gitignore(target_root: Path, instruction_names: list[str]) -> None:
    """Idempotently append only installed project instruction filenames.

    Args:
        target_root: Existing project directory containing or receiving
            `.gitignore`.
        instruction_names: Installed names to ignore. The function preserves
            existing content and appends only names absent from existing lines.

    Returns:
        None: The project `.gitignore` is created or updated when needed.

    Raises:
        OSError: If `.gitignore` cannot be read or written.
    """
    gitignore_path = target_root / ".gitignore"
    existing_text = ""
    existing_lines = []
    if gitignore_path.exists():
        existing_text = gitignore_path.read_text(encoding="utf-8")
        existing_lines = existing_text.splitlines()

    missing_names = [name for name in instruction_names if name not in existing_lines]
    needs_header = GITIGNORE_HEADER not in existing_lines
    if not missing_names and not needs_header:
        return

    with gitignore_path.open("a", encoding="utf-8") as gitignore_file:
        if existing_text and not existing_text.endswith("\n"):
            gitignore_file.write("\n")
        if existing_lines:
            gitignore_file.write("\n")
        if needs_header:
            gitignore_file.write(f"{GITIGNORE_HEADER}\n")
        for name in missing_names:
            gitignore_file.write(f"{name}\n")


def install_project(
    template_root: Path | None = None,
    input_function: InputFunction = input,
    output_function: OutputFunction = print,
) -> bool:
    """Interactively install selected project instruction files without skills.

    Args:
        template_root: Template root to use. None derives it from this script.
        input_function: Prompt callable for target, tool, ignore, and conflict
            decisions.
        output_function: Reporting callable for conflicts, backups, and result.

    Returns:
        bool: True after installation, or false if conflict replacement is
        declined before any files are changed.

    Raises:
        RuntimeError: If template validation fails.
        OSError: If project files cannot be read, backed up, copied, or written.
        ValueError: If a target, tool selection, or confirmation is invalid.
    """
    root = template_root or get_template_root()
    validate_sources(root)
    target_root = prompt_target_root(input_function)
    selected_tools = prompt_project_tools(input_function)

    instruction_names = []
    items = []
    if selected_tools & {"codex", "antigravity"}:
        instruction_names.append("AGENTS.md")
        items.append((root / "project" / "AGENTS.md", target_root / "AGENTS.md", None))
    if "claude" in selected_tools:
        instruction_names.append("CLAUDE.md")
        items.append((root / "project" / "CLAUDE.md", target_root / "CLAUDE.md", None))

    update_ignore = prompt_gitignore_update(instruction_names, input_function)
    installed = install_items(items, input_function, output_function)
    if not installed:
        return False
    if update_ignore:
        update_gitignore(target_root, instruction_names)
    output_function(f"Installed project instructions into {target_root}")
    return True


def run_menu() -> int:
    """Present the four installer workflows for direct script invocation.

    Args:
        None.

    Returns:
        int: Zero after a selected workflow completes or is cancelled, and two
        for an invalid menu selection.

    Raises:
        RuntimeError: If the selected workflow finds invalid template sources.
        OSError: If the selected workflow cannot update the filesystem.
        ValueError: If the user supplies invalid interactive input.
    """
    print("Portable agent template installer")
    print("1. Install global Codex")
    print("2. Install global Claude")
    print("3. Install global Antigravity CLI")
    print("4. Install project instructions")
    choice = input("Choose 1-4: ").strip()
    installers = {
        "1": install_global_codex,
        "2": install_global_claude,
        "3": install_global_antigravity,
        "4": install_project,
    }
    installer = installers.get(choice)
    if installer is None:
        print("Invalid selection. Choose 1, 2, 3, or 4.", file=sys.stderr)
        return 2
    installer()
    return 0


if __name__ == "__main__":
    raise SystemExit(run_menu())
