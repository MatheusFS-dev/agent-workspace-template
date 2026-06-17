#!/usr/bin/env python3
"""Install the local agent template into another project root."""

from pathlib import Path
import shutil


TEMPLATE_ITEMS = (".agent", "AGENTS.md", "CLAUDE.md", "GEMINI.md")
GITIGNORE_HEADER = "# Agent stuff"
GITIGNORE_LINES = (".agent/", "AGENTS.md", "CLAUDE.md", "GEMINI.md")


def get_template_root() -> Path:
    """Return the repository root that contains the template assets.

    Returns:
        Path: Absolute path to the template repository root derived from this
        script location.

    Raises:
        RuntimeError: If the derived root does not contain all required
        template items, which indicates the script was moved away from the
        expected repository layout.
    """
    template_root = Path(__file__).resolve().parent.parent

    # Validate the expected layout up front so the installer fails clearly if
    # someone copies only the script without the template assets it depends on.
    missing_items = [
        item_name
        for item_name in TEMPLATE_ITEMS
        if not (template_root / item_name).exists()
    ]
    if missing_items:
        missing_text = ", ".join(missing_items)
        raise RuntimeError(
            f"Template root is missing required items: {missing_text}."
        )

    return template_root


def prompt_target_root() -> Path:
    """Prompt for the destination project root and validate it.

    Returns:
        Path: Absolute path to the destination directory entered by the user.

    Raises:
        ValueError: If the user provides an empty path.
        FileNotFoundError: If the provided path does not exist.
        NotADirectoryError: If the provided path exists but is not a directory.

    Examples:
        A valid response such as ``/home/user/project`` returns that directory
        as an absolute path. An empty response raises ``ValueError`` instead of
        guessing a default destination.
    """
    target_text = input("Target project root: ").strip()
    if not target_text:
        raise ValueError("Target project root cannot be empty.")

    target_root = Path(target_text).expanduser().resolve()
    if not target_root.exists():
        raise FileNotFoundError(
            f"Target project root does not exist: {target_root}"
        )
    if not target_root.is_dir():
        raise NotADirectoryError(
            f"Target project root is not a directory: {target_root}"
        )

    return target_root


def replace_path(source_path: Path, destination_path: Path) -> None:
    """Replace a destination path with a fresh copy from the template.

    Args:
        source_path (Path): File or directory inside the template repository
            that will be copied. If this path is a directory, the entire tree is
            copied. If this path is a file, only that file is copied.
        destination_path (Path): Final file or directory path inside the target
            project root. Existing files or directories at this path are always
            removed first so the installer performs a true overwrite instead of
            a merge.

    Returns:
        None: This function mutates the filesystem by deleting any existing
        destination path and copying the source into place.

    Raises:
        FileNotFoundError: If ``source_path`` does not exist.
        OSError: If the destination cannot be removed or the copy operation
            fails due to permissions, locks, or filesystem errors.

    Examples:
        Replacing ``target/.agent`` with the template ``.agent`` directory
        deletes the existing destination directory first, then copies the
        template directory tree fresh.
    """
    if not source_path.exists():
        raise FileNotFoundError(f"Template item does not exist: {source_path}")

    # Remove the existing destination first so overwriting a directory never
    # degenerates into a partial merge with stale files left behind.
    if destination_path.is_dir() and not destination_path.is_symlink():
        shutil.rmtree(destination_path)
    elif destination_path.exists() or destination_path.is_symlink():
        destination_path.unlink()

    if source_path.is_dir():
        shutil.copytree(source_path, destination_path)
    else:
        shutil.copy2(source_path, destination_path)


def copy_template_items(template_root: Path, target_root: Path) -> None:
    """Copy all template items into the selected project root.

    Args:
        template_root (Path): Absolute root of the template repository that
            contains the source `.agent`, `AGENTS.md`, `CLAUDE.md`, and
            `GEMINI.md` items.
        target_root (Path): Absolute destination project root chosen by the
            user. Every template item is copied directly into this directory.

    Returns:
        None: This function overwrites the destination paths in place.

    Raises:
        FileNotFoundError: If any required source item is missing from the
            template repository.
        OSError: If deleting or copying any destination path fails.
    """
    for item_name in TEMPLATE_ITEMS:
        replace_path(template_root / item_name, target_root / item_name)


def prompt_gitignore_update() -> bool:
    """Ask whether the copied configuration should stay local via `.gitignore`.

    Returns:
        bool: ``True`` when the user answers `y` or `yes`, which causes the
        installer to create or update `.gitignore`. ``False`` when the user
        answers `n`, `no`, or presses Enter, which leaves `.gitignore`
        unchanged.

    Raises:
        ValueError: If the user enters any response other than `y`, `yes`,
        `n`, `no`, or an empty line. This explicit failure avoids silently
        treating ambiguous input as consent or rejection.

    Examples:
        Pressing Enter returns ``False`` because the installer defaults to not
        modifying `.gitignore`. Typing ``yes`` returns ``True``.
    """
    response = input(
        "Add .agent/, AGENTS.md, CLAUDE.md, and GEMINI.md to .gitignore? [y/N]: "
    ).strip().lower()
    if response in ("", "n", "no"):
        return False
    if response in ("y", "yes"):
        return True
    raise ValueError(
        "Invalid response. Enter yes, y, no, n, or press Enter for no."
    )


def update_gitignore(target_root: Path) -> None:
    """Create or update `.gitignore` with the template-local entries section.

    Args:
        target_root (Path): Absolute project root that will receive the
            `.gitignore` update. If `.gitignore` does not exist, this function
            creates it. If it exists, this function ensures the `# Agent stuff`
            header is present and appends only missing template entries,
            preserving existing content and avoiding duplicates.

    Returns:
        None: This function writes to ``target_root / ".gitignore"``.

    Raises:
        OSError: If reading or writing `.gitignore` fails.

    Examples:
        If `.gitignore` already contains `AGENTS.md`, the function keeps that
        line, adds `# Agent stuff` if needed, and appends only the remaining
        missing template entries.
    """
    gitignore_path = target_root / ".gitignore"
    existing_lines = []
    existing_text = ""
    if gitignore_path.exists():
        existing_text = gitignore_path.read_text(encoding="utf-8")
        existing_lines = existing_text.splitlines()

    missing_lines = [
        line for line in GITIGNORE_LINES if line not in existing_lines
    ]
    needs_header = GITIGNORE_HEADER not in existing_lines
    if not needs_header and not missing_lines:
        return

    # Preserve existing content verbatim and only append genuinely missing
    # entries so repeat runs remain deterministic and duplicate-free.
    with gitignore_path.open("a", encoding="utf-8") as gitignore_file:
        if existing_text and existing_text[-1] != "\n":
            gitignore_file.write("\n")
        if existing_lines:
            gitignore_file.write("\n")
        if needs_header:
            gitignore_file.write(f"{GITIGNORE_HEADER}\n")
        for line in missing_lines:
            gitignore_file.write(f"{line}\n")


def run_installer() -> None:
    """Run the interactive template installer workflow.

    Returns:
        None: This function performs the interactive prompts and filesystem
        updates required to install the template into another project.

    Raises:
        RuntimeError: If the template repository layout is incomplete.
        ValueError: If the user enters an empty destination path or an invalid
            yes/no answer for the `.gitignore` prompt.
        FileNotFoundError: If the chosen target directory does not exist.
        NotADirectoryError: If the chosen target path is not a directory.
        OSError: If deleting, copying, reading, or writing files fails.

    Examples:
        Running ``python3 scripts/install_template.py`` prompts for a target
        directory, copies the template files there, and optionally updates
        `.gitignore`.
    """
    template_root = get_template_root()
    target_root = prompt_target_root()
    copy_template_items(template_root, target_root)

    if prompt_gitignore_update():
        update_gitignore(target_root)

    print(f"Installed template into: {target_root}")


if __name__ == "__main__":
    run_installer()
