#!/usr/bin/env python3
"""Install the Codex global assets on Linux from this portable template."""

from datetime import datetime
from pathlib import Path
import shutil
import sys
import tomllib
from typing import Callable


GLOBAL_INSTRUCTIONS_PLACEHOLDER = "{{GLOBAL_INSTRUCTIONS}}"
InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], None]
InstallItem = tuple[Path | None, Path, str | None]


def get_template_root() -> Path:
    """Return the template repository root derived from this script location.

    Args:
        None.

    Returns:
        Path: Absolute repository root containing the Codex template sources.

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


def render_codex_config(template_root: Path) -> str:
    """Render Codex configuration from the global instructions source.

    Args:
        template_root: Absolute template repository root containing the Codex
            configuration template and global instructions file.

    Returns:
        str: Valid TOML configuration with global instructions embedded.

    Raises:
        RuntimeError: If the placeholder count is not one, the instructions
            cannot fit a TOML multiline literal, or the result is invalid TOML.
        OSError: If either source file cannot be read.

    Examples:
        Render a repository's Codex configuration before writing it:

        >>> render_codex_config(Path("/path/to/template"))  # doctest: +SKIP
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

    # Render from the single canonical instructions source and reject any
    # marker introduced by that source instead of shipping unresolved config.
    rendered = config_text.replace(GLOBAL_INSTRUCTIONS_PLACEHOLDER, instructions_text)
    if GLOBAL_INSTRUCTIONS_PLACEHOLDER in rendered:
        raise RuntimeError("Rendered Codex configuration still contains a placeholder.")
    try:
        tomllib.loads(rendered)
    except tomllib.TOMLDecodeError as error:
        raise RuntimeError(f"Rendered Codex configuration is invalid TOML: {error}") from error
    return rendered


def validate_sources(template_root: Path) -> list[Path]:
    """Validate the sources required by the Codex workflow.

    Args:
        template_root: Absolute template repository root to validate.

    Returns:
        list[Path]: Sorted direct skill package directories containing
        `SKILL.md` files.

    Raises:
        RuntimeError: If a required Codex source is missing, rendered TOML is
            invalid, or a direct skill package lacks `SKILL.md`.
        OSError: If a source cannot be read or enumerated.
    """
    required_paths = (
        template_root / "instructions" / "global.md",
        template_root / "configs" / "codex" / "config.toml.template",
        template_root / "skills",
    )
    missing_paths = [path for path in required_paths if not path.exists()]
    if missing_paths:
        missing_text = ", ".join(str(path) for path in missing_paths)
        raise RuntimeError(f"Codex template source is missing: {missing_text}")

    render_codex_config(template_root)
    skills_root = template_root / "skills"
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


def prompt_codex_profiles(template_root: Path, input_function: InputFunction) -> list[Path]:
    """Prompt for optional Codex profiles to install with the base config.

    Args:
        template_root: Absolute template root containing Codex profile files.
        input_function: Prompt callable that returns the user's response.

    Returns:
        list[Path]: Selected profile files, or an empty list for a blank answer.

    Raises:
        ValueError: If a profile name is unknown, empty, or repeated.
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


def replace_path(source_path: Path | None, destination_path: Path, content: str | None) -> None:
    """Replace a destination with either a source copy or rendered text.

    Args:
        source_path: Source file or directory when `content` is None.
        destination_path: Target path to replace completely.
        content: Rendered UTF-8 text when not None; this mode requires
            `source_path` to be None.

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

    if destination_path.is_dir() and not destination_path.is_symlink():
        shutil.rmtree(destination_path)
    elif path_exists(destination_path):
        destination_path.unlink()
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
        items: Source, destination, and optional rendered-content tuples.
        input_function: Prompt callable used only when conflicts exist.
        output_function: Reporting callable used for conflicts and backups.

    Returns:
        bool: True after installation; false when replacement is declined
        before any files are changed.

    Raises:
        OSError: If a backup, removal, copy, or write fails.
        ValueError: If an interactive confirmation is invalid.

    Examples:
        Install one rendered configuration into an empty destination:

        >>> install_items(  # doctest: +SKIP
        ...     [(None, Path("/tmp/config.toml"), "model = 'test'\\n")], input, print
        ... )
        True
    """
    # Resolve every conflict before the first write so declining replacement
    # leaves the destination tree untouched.
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


def install_global_codex(
    template_root: Path | None = None,
    home_root: Path | None = None,
    input_function: InputFunction = input,
    output_function: OutputFunction = print,
) -> bool:
    """Interactively install Codex global configuration, profiles, and skills.

    Args:
        template_root: Template root to use; None derives it from this script.
        home_root: User home directory to target; None uses `Path.home()`.
        input_function: Prompt callable for profile and conflict decisions.
        output_function: Reporting callable for conflicts, backups, and result.

    Returns:
        bool: True after installation, or false if replacement is declined.

    Raises:
        RuntimeError: If the current platform is not Linux, required Codex
            sources are missing, or rendered TOML is invalid.
        OSError: If files cannot be read, backed up, copied, or written.
        ValueError: If a profile selection or confirmation is invalid.

    Examples:
        Install from an explicit template into an explicit home directory:

        >>> install_global_codex(  # doctest: +SKIP
        ...     Path("/template"), Path("/tmp/home"), lambda _: ""
        ... )
        True
    """
    validate_platform()
    root = template_root or get_template_root()
    home = home_root or Path.home()
    skill_packages = validate_sources(root)
    selected_profiles = prompt_codex_profiles(root, input_function)
    codex_root = home / ".codex"
    items = [(None, codex_root / "config.toml", render_codex_config(root))]
    items.extend((profile, codex_root / profile.name, None) for profile in selected_profiles)
    items.extend(
        (package, codex_root / "skills" / package.name, None)
        for package in skill_packages
    )
    installed = install_items(items, input_function, output_function)
    if installed:
        output_function(f"Installed Codex global template into {codex_root}")
    return installed


if __name__ == "__main__":
    install_global_codex()
