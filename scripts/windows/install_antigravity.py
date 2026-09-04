#!/usr/bin/env python3
"""Install Antigravity CLI global assets on Windows from this portable template."""

from datetime import datetime
import json
from pathlib import Path
import shutil
import sys
from typing import Callable, Optional


InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], None]
InstallItem = tuple[Path, Path]


def get_template_root() -> Path:
    """Return the template repository root derived from this script location.

    Args:
        None.

    Returns:
        Path: Absolute root containing the Antigravity template sources.

    Raises:
        None.
    """
    return Path(__file__).resolve().parents[2]


def validate_platform() -> None:
    """Require Windows before the installer can prompt or write files.

    Args:
        None.

    Returns:
        None: The current interpreter is running on Windows.

    Raises:
        RuntimeError: If the current interpreter is not running on Windows.
    """
    if sys.platform != "win32":
        raise RuntimeError("Windows installer requires Windows.")


def validate_sources(template_root: Path) -> list[Path]:
    """Validate the sources required by the Antigravity workflow.

    Args:
        template_root: Absolute template repository root to validate.

    Returns:
        list[Path]: Sorted direct skill package directories containing
        `SKILL.md` files.

    Raises:
        RuntimeError: If an Antigravity source is missing, settings JSON is
            invalid, or a direct skill package lacks `SKILL.md`.
        OSError: If a source cannot be read or enumerated.
    """
    instructions_path = template_root / "instructions" / "global.md"
    settings_path = template_root / "configs" / "antigravity" / "settings.json"
    skills_root = template_root / "skills"
    required_paths = (instructions_path, settings_path, skills_root)
    missing_paths = [path for path in required_paths if not path.exists()]
    if missing_paths:
        missing_text = ", ".join(str(path) for path in missing_paths)
        raise RuntimeError(f"Antigravity template source is missing: {missing_text}")

    try:
        json.loads(settings_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Invalid JSON source {settings_path}: {error}") from error

    skill_packages = sorted(path for path in skills_root.iterdir() if path.is_dir())
    invalid_packages = [
        package for package in skill_packages if not (package / "SKILL.md").is_file()
    ]
    if invalid_packages:
        invalid_text = ", ".join(str(path) for path in invalid_packages)
        raise RuntimeError(
            "Every source skill must be a direct skills/<name>/SKILL.md package: "
            f"{invalid_text}"
        )
    return skill_packages


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
    """Replace a destination with a complete source file or directory copy.

    Args:
        source_path: Existing source file or directory to copy.
        destination_path: Target file or directory to replace completely.

    Returns:
        None: The destination is replaced in place.

    Raises:
        FileNotFoundError: If the requested copy source does not exist.
        OSError: If removal or copying fails.
    """
    if not path_exists(source_path):
        raise FileNotFoundError(f"Installation source does not exist: {source_path}")
    if destination_path.is_dir() and not destination_path.is_symlink():
        shutil.rmtree(destination_path)
    elif path_exists(destination_path):
        destination_path.unlink()
    destination_path.parent.mkdir(parents=True, exist_ok=True)

    if source_path.is_dir():
        shutil.copytree(source_path, destination_path, symlinks=True)
    else:
        shutil.copy2(source_path, destination_path, follow_symlinks=False)


def install_items(
    items: list[InstallItem],
    input_function: InputFunction,
    output_function: OutputFunction,
) -> bool:
    """Confirm conflicts, optionally back them up, and install all items.

    Args:
        items: Source and destination pairs for complete path replacement.
        input_function: Prompt callable used only when conflicts exist.
        output_function: Reporting callable used for conflicts and backups.

    Returns:
        bool: True after installation; false when replacement is declined
        before any files are changed.

    Raises:
        OSError: If a backup, removal, or copy fails.
        ValueError: If an interactive confirmation is invalid.

    Examples:
        Install one source file into an empty destination:

        >>> install_items(  # doctest: +SKIP
        ...     [(Path("/template/GEMINI.md"), Path("/tmp/GEMINI.md"))], input, print
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


def install_global_antigravity(
    template_root: Optional[Path] = None,
    home_root: Optional[Path] = None,
    input_function: InputFunction = input,
    output_function: OutputFunction = print,
) -> bool:
    """Interactively install Antigravity global rules, settings, and skills.

    Args:
        template_root: Template root to use; None derives it from this script.
        home_root: User home directory to target; None uses `Path.home()`.
        input_function: Prompt callable for conflict decisions.
        output_function: Reporting callable for conflicts, backups, and result.

    Returns:
        bool: True after installation, or false if replacement is declined.

    Raises:
        RuntimeError: If the current platform is not Windows or required
            Antigravity sources are missing or invalid.
        OSError: If files cannot be read, backed up, copied, or written.
        ValueError: If a confirmation is invalid.

    Examples:
        Install from an explicit template into an explicit home directory:

        >>> install_global_antigravity(  # doctest: +SKIP
        ...     Path("/template"), Path("/tmp/home")
        ... )
        True
    """
    validate_platform()
    root = template_root or get_template_root()
    home = home_root or Path.home()
    skill_packages = validate_sources(root)
    gemini_root = home / ".gemini"
    antigravity_root = gemini_root / "antigravity-cli"
    items = [
        (root / "instructions" / "global.md", gemini_root / "GEMINI.md"),
        (
            root / "configs" / "antigravity" / "settings.json",
            antigravity_root / "settings.json",
        ),
    ]
    items.extend(
        (package, antigravity_root / "skills" / package.name)
        for package in skill_packages
    )
    installed = install_items(items, input_function, output_function)
    if installed:
        output_function(f"Installed Antigravity CLI global template into {gemini_root}")
    return installed


if __name__ == "__main__":
    install_global_antigravity()
