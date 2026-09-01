#!/usr/bin/env python3
"""Install project-scoped instructions on Linux from this portable template."""

from datetime import datetime
from pathlib import Path
import shutil
import sys
from typing import Callable, Optional


GITIGNORE_HEADER = "# Agent workspace template"
SUPERPOWERS_GITIGNORE_LINES = (
    "docs/superpowers/specs/",
    "docs/superpowers/plans/",
)
InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], None]
InstallItem = tuple[Path, Path]


def get_template_root() -> Path:
    """Return the template repository root derived from this script location.

    Args:
        None.

    Returns:
        Path: Absolute repository root containing project instruction sources.

    Raises:
        None.
    """
    return Path(__file__).resolve().parents[3]


def validate_platform() -> None:
    """Require Linux before the installer can prompt or write files.

    Args:
        None.

    Returns:
        None: The current interpreter is running on Linux.

    Raises:
        RuntimeError: If the current interpreter is not running on Linux.
    """
    if not sys.platform.startswith("linux"):
        raise RuntimeError("Linux installer requires Linux.")


def validate_sources(template_root: Path) -> None:
    """Validate the sources required by the project workflow.

    Args:
        template_root: Absolute template repository root to validate.

    Returns:
        None: Both project instruction sources exist after validation.

    Raises:
        RuntimeError: If either project instruction source is missing.
    """
    required_paths = (
        template_root / "project" / "AGENTS.md",
        template_root / "project" / "CLAUDE.md",
    )
    missing_paths = [path for path in required_paths if not path.is_file()]
    if missing_paths:
        missing_text = ", ".join(str(path) for path in missing_paths)
        raise RuntimeError(f"Project template source is missing: {missing_text}")


def prompt_target_root(input_function: InputFunction) -> Path:
    """Prompt for an existing destination project directory.

    Args:
        input_function: Prompt callable that returns the user's response.

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


def prompt_project_tools(input_function: InputFunction) -> set[str]:
    """Prompt for the project instruction formats to install.

    Args:
        input_function: Prompt callable that returns the user's response.

    Returns:
        set[str]: Non-empty selection from Codex, Antigravity, and Claude.

    Raises:
        ValueError: If the response is empty, repeated, or contains an unknown
            or empty tool name.
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
        input_function: Prompt callable that returns the user's response.

    Returns:
        bool: True for yes; false for no or an empty response.

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
        Path: Non-existing sibling path ending in a backup suffix.

    Raises:
        None.
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    candidate = destination_path.with_name(f"{destination_path.name}.backup-{timestamp}")
    counter = 1
    while path_exists(candidate):
        candidate = destination_path.with_name(
            f"{destination_path.name}.backup-{timestamp}-{counter}"
        )
        counter += 1
    return candidate


def copy_backup(destination_path: Path) -> Path:
    """Copy an existing destination to an adjacent backup path.

    Args:
        destination_path: Existing file, directory, or symbolic link to copy.

    Returns:
        Path: Backup path containing the pre-replacement destination.

    Raises:
        OSError: If the source cannot be copied or the backup cannot be made.
    """
    backup_destination = backup_path(destination_path)
    if destination_path.is_dir() and not destination_path.is_symlink():
        shutil.copytree(destination_path, backup_destination, symlinks=True)
    else:
        shutil.copy2(destination_path, backup_destination, follow_symlinks=False)
    return backup_destination


def replace_path(source_path: Path, destination_path: Path) -> None:
    """Replace a destination with a complete source file copy.

    Args:
        source_path: Existing project instruction file to copy.
        destination_path: Target instruction file to replace completely.

    Returns:
        None: The destination is replaced in place.

    Raises:
        FileNotFoundError: If the requested source does not exist.
        OSError: If removal or copying fails.
    """
    if not source_path.is_file():
        raise FileNotFoundError(f"Installation source does not exist: {source_path}")
    if destination_path.is_dir() and not destination_path.is_symlink():
        shutil.rmtree(destination_path)
    elif path_exists(destination_path):
        destination_path.unlink()
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, destination_path, follow_symlinks=False)


def install_items(
    items: list[InstallItem],
    input_function: InputFunction,
    output_function: OutputFunction,
) -> bool:
    """Confirm conflicts, optionally back them up, and install all items.

    Args:
        items: Source and destination pairs for complete file replacement.
        input_function: Prompt callable used only when conflicts exist.
        output_function: Reporting callable used for conflicts and backups.

    Returns:
        bool: True after installation; false when replacement is declined
        before any files are changed.

    Raises:
        OSError: If a backup, removal, or copy fails.
        ValueError: If an interactive confirmation is invalid.

    Examples:
        Install one instruction file into an empty project:

        >>> install_items(  # doctest: +SKIP
        ...     [(Path("/template/AGENTS.md"), Path("/tmp/AGENTS.md"))], input, print
        ... )
        True
    """
    # Resolve every conflict before the first write so declining replacement
    # leaves the destination tree untouched.
    conflicts = [destination for _, destination in items if path_exists(destination)]
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

    for source_path, destination_path in items:
        replace_path(source_path, destination_path)
    return True


def prompt_gitignore_updates(
    instruction_names: list[str],
    input_function: InputFunction,
) -> tuple[bool, bool]:
    """Prompt separately for project-instruction and Superpowers ignore rules.

    Args:
        instruction_names: Installed project instruction filenames included in
            the first prompt.
        input_function: Prompt callable for both yes/no decisions.

    Returns:
        tuple[bool, bool]: Whether to ignore the installed instruction files,
            followed by whether to ignore the Superpowers output directories.

    Raises:
        ValueError: If either yes/no response is invalid.
    """
    names = " and ".join(instruction_names)
    ignore_instructions = prompt_yes_no(
        f"Add {names} to .gitignore? [y/N]: ",
        input_function,
    )
    ignore_superpowers = prompt_yes_no(
        "Add Superpowers docs to .gitignore? [y/N]: ",
        input_function,
    )
    return ignore_instructions, ignore_superpowers


def update_gitignore(target_root: Path, ignored_paths: list[str]) -> None:
    """Idempotently append selected project paths to `.gitignore`.

    Args:
        target_root: Existing project directory containing or receiving
            `.gitignore`.
        ignored_paths: Project-relative file or directory paths to ignore.

    Returns:
        None: The `.gitignore` is created or updated only when needed.

    Raises:
        OSError: If `.gitignore` cannot be read or written.

    Examples:
        Add the installed Codex instruction file to an existing project:

        >>> update_gitignore(Path("/tmp/project"), ["AGENTS.md"])  # doctest: +SKIP
    """
    gitignore_path = target_root / ".gitignore"
    existing_text = ""
    existing_lines = []
    if gitignore_path.exists():
        existing_text = gitignore_path.read_text(encoding="utf-8")
        existing_lines = existing_text.splitlines()

    missing_names = [name for name in ignored_paths if name not in existing_lines]
    needs_header = GITIGNORE_HEADER not in existing_lines
    if not missing_names and not needs_header:
        return

    # Preserve the existing file verbatim and add one separated managed block.
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
    template_root: Optional[Path] = None,
    input_function: InputFunction = input,
    output_function: OutputFunction = print,
) -> bool:
    """Interactively install selected project instruction files without skills.

    Args:
        template_root: Template root to use; None derives it from this script.
        input_function: Prompt callable for target, tool, ignore, and conflict
            decisions.
        output_function: Reporting callable for conflicts, backups, and result.

    Returns:
        bool: True after installation, or false if replacement is declined.

    Raises:
        RuntimeError: If the current platform is not Linux or required project
            instruction sources are missing.
        OSError: If project files cannot be read, backed up, copied, or written.
        ValueError: If a target, tool selection, or confirmation is invalid.

    Examples:
        Install Codex instructions into an explicitly selected project:

        >>> answers = iter(["/tmp/project", "codex", "no", "no"])
        >>> install_project(  # doctest: +SKIP
        ...     Path("/template"), lambda _: next(answers)
        ... )
        True
    """
    validate_platform()
    root = template_root or get_template_root()
    validate_sources(root)
    target_root = prompt_target_root(input_function)
    selected_tools = prompt_project_tools(input_function)

    # Codex and Antigravity share AGENTS.md while Claude consumes the separate
    # importing file, so mixed selections create each destination only once.
    instruction_names = []
    items = []
    if selected_tools & {"codex", "antigravity"}:
        instruction_names.append("AGENTS.md")
        items.append((root / "project" / "AGENTS.md", target_root / "AGENTS.md"))
    if "claude" in selected_tools:
        instruction_names.append("CLAUDE.md")
        items.append((root / "project" / "CLAUDE.md", target_root / "CLAUDE.md"))

    ignore_instructions, ignore_superpowers = prompt_gitignore_updates(
        instruction_names,
        input_function,
    )
    installed = install_items(items, input_function, output_function)
    if not installed:
        return False
    ignored_paths = []
    if ignore_instructions:
        ignored_paths.extend(instruction_names)
    if ignore_superpowers:
        ignored_paths.extend(SUPERPOWERS_GITIGNORE_LINES)
    if ignored_paths:
        update_gitignore(target_root, ignored_paths)
    output_function(f"Installed project instructions into {target_root}")
    return True


if __name__ == "__main__":
    install_project()
