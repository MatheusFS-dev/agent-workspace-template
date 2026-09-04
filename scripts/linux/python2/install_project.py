#!/usr/bin/env python2.7
"""Install project-scoped instructions on Linux with Python 2.7."""

from datetime import datetime
import errno
import io
import os
import shutil
import sys


GITIGNORE_HEADER = "# Agent workspace template"
SUPERPOWERS_GITIGNORE_LINES = (
    "docs/superpowers/specs/",
    "docs/superpowers/plans/",
)


def output_text(message):
    """Write one installer status message to standard output.

    Args:
        message (str): Status text without a trailing newline.

    Returns:
        None: The message is written immediately.

    Raises:
        IOError: If standard output cannot be written.
    """
    sys.stdout.write("{0}\n".format(message))


def get_template_root():
    """Return the template repository root derived from this script location.

    Args:
        None.

    Returns:
        str: Absolute repository root containing project instruction sources.

    Raises:
        None.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def validate_platform():
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


def validate_sources(template_root):
    """Validate the sources required by the project workflow.

    Args:
        template_root (str): Absolute template repository root to validate.

    Returns:
        None: Both project instruction sources exist after validation.

    Raises:
        RuntimeError: If either project instruction source is missing.
    """
    required_paths = (
        os.path.join(template_root, "project", "AGENTS.md"),
        os.path.join(template_root, "project", "CLAUDE.md"),
    )
    missing_paths = [path for path in required_paths if not os.path.isfile(path)]
    if missing_paths:
        raise RuntimeError(
            "Project template source is missing: {0}".format(", ".join(missing_paths))
        )


def prompt_target_root(input_function):
    """Prompt for an existing destination project directory.

    Args:
        input_function (callable): Prompt callable returning the path response.

    Returns:
        str: Absolute existing project directory selected by the user.

    Raises:
        ValueError: If the response is empty.
        IOError: With ENOENT if the supplied directory does not exist.
        OSError: With ENOTDIR if the supplied path is not a directory.
    """
    target_text = input_function("Target project directory: ").strip()
    if not target_text:
        raise ValueError("Target project directory cannot be empty.")

    target_root = os.path.abspath(os.path.expanduser(target_text))
    if not os.path.exists(target_root):
        raise IOError(
            errno.ENOENT, "Target project directory does not exist", target_root
        )
    if not os.path.isdir(target_root):
        raise OSError(
            errno.ENOTDIR, "Target project path is not a directory", target_root
        )
    return target_root


def prompt_project_tools(input_function):
    """Prompt for the project instruction formats to install.

    Args:
        input_function (callable): Prompt callable returning the tool response.

    Returns:
        set of str: Non-empty selection from codex, antigravity, and claude.

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

    allowed_tools = set(("codex", "antigravity", "claude"))
    unknown_tools = sorted(set(selected_tools) - allowed_tools)
    if unknown_tools:
        raise ValueError("Unknown project tool: {0}".format(", ".join(unknown_tools)))
    return set(selected_tools)


def prompt_yes_no(prompt, input_function):
    """Prompt for an explicit yes or no response with a no default.

    Args:
        prompt (str): Full prompt text, including any displayed default.
        input_function (callable): Prompt callable returning the response.

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


def path_exists(path):
    """Return whether a path exists, including a dangling symbolic link.

    Args:
        path (str): Filesystem path to inspect.

    Returns:
        bool: True when the path exists or is a symbolic link.

    Raises:
        None.
    """
    return os.path.lexists(path)


def backup_path(destination_path):
    """Create a unique timestamped adjacent backup pathname.

    Args:
        destination_path (str): Existing path copied before replacement.

    Returns:
        str: Non-existing sibling path ending in a backup suffix.

    Raises:
        None.
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    candidate = "{0}.backup-{1}".format(destination_path, timestamp)
    counter = 1
    while path_exists(candidate):
        candidate = "{0}.backup-{1}-{2}".format(destination_path, timestamp, counter)
        counter += 1
    return candidate


def copy_path(source_path, destination_path):
    """Copy a file, directory, or symbolic link without dereferencing links.

    Args:
        source_path (str): Existing source path to copy.
        destination_path (str): Non-existing destination path to create.

    Returns:
        None: The complete source path is copied.

    Raises:
        OSError: If link recreation, directory copying, or file copying fails.
    """
    # Python 2 shutil cannot preserve a top-level symlink through copy2, so
    # recreate the link with its original target text.
    if os.path.islink(source_path):
        os.symlink(os.readlink(source_path), destination_path)
    elif os.path.isdir(source_path):
        shutil.copytree(source_path, destination_path, symlinks=True)
    else:
        shutil.copy2(source_path, destination_path)


def copy_backup(destination_path):
    """Copy an existing destination to an adjacent backup path.

    Args:
        destination_path (str): Existing file, directory, or link to copy.

    Returns:
        str: Backup path containing the pre-replacement destination.

    Raises:
        OSError: If the source cannot be copied or the backup cannot be made.
    """
    backup_destination = backup_path(destination_path)
    copy_path(destination_path, backup_destination)
    return backup_destination


def replace_path(source_path, destination_path):
    """Replace a destination with a complete source path copy.

    Args:
        source_path (str): Existing source file, directory, or symbolic link.
        destination_path (str): Target path to replace completely.

    Returns:
        None: The destination is replaced in place.

    Raises:
        IOError: With ENOENT if the requested copy source does not exist.
        OSError: If removal, directory creation, or copying fails.
    """
    if not os.path.isfile(source_path):
        raise IOError(errno.ENOENT, "Installation source does not exist", source_path)
    if os.path.isdir(destination_path) and not os.path.islink(destination_path):
        shutil.rmtree(destination_path)
    elif path_exists(destination_path):
        os.unlink(destination_path)
    parent_path = os.path.dirname(destination_path)
    if not os.path.isdir(parent_path):
        os.makedirs(parent_path)
    copy_path(source_path, destination_path)


def install_items(items, input_function, output_function):
    """Confirm conflicts, optionally back them up, and install all items.

    Args:
        items (list of tuple): Source and destination string pairs for complete
            path replacement.
        input_function (callable): Prompt callable used only for conflicts.
        output_function (callable): Status callable for conflicts and backups.

    Returns:
        bool: True after installation; false when replacement is declined
            before any files are changed.

    Raises:
        OSError: If a backup, removal, or copy fails.
        ValueError: If an interactive confirmation is invalid.

    Examples:
        Install one file into an empty destination:

        >>> install_items([("/source", "/target")], lambda _: "", output_text)
        True
    """
    # Resolve every conflict before the first write so cancellation leaves the
    # destination tree untouched.
    conflicts = [destination for _, destination in items if path_exists(destination)]
    if conflicts:
        output_function("Conflicting managed destinations:")
        for destination in conflicts:
            output_function("- {0}".format(destination))
        if not prompt_yes_no("Replace all listed paths? [y/N]: ", input_function):
            output_function("Installation cancelled; no files were changed.")
            return False
        if prompt_yes_no("Create backups of conflicting paths? [y/N]: ", input_function):
            for destination in conflicts:
                output_function(
                    "Backed up {0} to {1}".format(destination, copy_backup(destination))
                )

    for source_path, destination_path in items:
        replace_path(source_path, destination_path)
    return True


def prompt_gitignore_updates(instruction_names, input_function):
    """Prompt separately for instruction and Superpowers ignore rules.

    Args:
        instruction_names (list of str): Installed instruction filenames shown
            in the first prompt.
        input_function (callable): Prompt callable for both yes/no decisions.

    Returns:
        tuple of bool: Whether to ignore instruction files, followed by whether
            to ignore the Superpowers output directories.

    Raises:
        ValueError: If either yes/no response is invalid.
    """
    names = " and ".join(instruction_names)
    ignore_instructions = prompt_yes_no(
        "Add {0} to .gitignore? [y/N]: ".format(names), input_function
    )
    ignore_superpowers = prompt_yes_no(
        "Add Superpowers docs to .gitignore? [y/N]: ", input_function
    )
    return ignore_instructions, ignore_superpowers


def update_gitignore(target_root, ignored_paths):
    """Idempotently append selected project paths to .gitignore.

    Args:
        target_root (str): Existing project directory containing or receiving
            the .gitignore file.
        ignored_paths (list of str): Project-relative paths to ignore.

    Returns:
        None: The file is created or updated only when lines are missing.

    Raises:
        IOError: If .gitignore cannot be read or written.
        UnicodeError: If existing content is not valid UTF-8.

    Examples:
        Add one installed instruction filename:

        >>> update_gitignore("/tmp/project", ["AGENTS.md"])  # doctest: +SKIP
    """
    gitignore_path = os.path.join(target_root, ".gitignore")
    existing_text = u""
    existing_lines = []
    if os.path.exists(gitignore_path):
        with io.open(gitignore_path, "r", encoding="utf-8") as gitignore_file:
            existing_text = gitignore_file.read()
        existing_lines = existing_text.splitlines()

    missing_names = [name for name in ignored_paths if name not in existing_lines]
    needs_header = GITIGNORE_HEADER not in existing_lines
    if not missing_names and not needs_header:
        return

    # Preserve existing content verbatim and add one separated managed block.
    with io.open(gitignore_path, "a", encoding="utf-8") as gitignore_file:
        if existing_text and not existing_text.endswith("\n"):
            gitignore_file.write(u"\n")
        if existing_lines:
            gitignore_file.write(u"\n")
        if needs_header:
            gitignore_file.write(u"{0}\n".format(GITIGNORE_HEADER))
        for name in missing_names:
            gitignore_file.write(u"{0}\n".format(name))


def install_project(
        template_root=None, input_function=raw_input,
        output_function=output_text):
    """Interactively install selected project instruction files without skills.

    Args:
        template_root (str): Template root to use; None derives it from this
            script. Defaults to None.
        input_function (callable): Prompt callable for target, tool, ignore,
            and conflict decisions. Defaults to raw_input.
        output_function (callable): Status callable for conflicts, backups, and
            the final result. Defaults to output_text.

    Returns:
        bool: True after installation, or false if replacement is declined.

    Raises:
        RuntimeError: If Linux is not active or instruction sources are missing.
        OSError: If project files cannot be read, backed up, copied, or written.
        ValueError: If a target, selection, or confirmation is invalid.

    Examples:
        Install Codex instructions into an explicitly selected project:

        >>> answers = iter(["/tmp/project", "codex", "no", "no"])
        >>> install_project("/template", lambda _: next(answers))  # doctest: +SKIP
        True
    """
    validate_platform()
    root = template_root or get_template_root()
    validate_sources(root)
    target_root = prompt_target_root(input_function)
    selected_tools = prompt_project_tools(input_function)

    # Codex and Antigravity share AGENTS.md while Claude consumes its separate
    # importing file, so mixed selections create each destination only once.
    instruction_names = []
    items = []
    if selected_tools & set(("codex", "antigravity")):
        instruction_names.append("AGENTS.md")
        items.append(
            (os.path.join(root, "project", "AGENTS.md"),
             os.path.join(target_root, "AGENTS.md"))
        )
    if "claude" in selected_tools:
        instruction_names.append("CLAUDE.md")
        items.append(
            (os.path.join(root, "project", "CLAUDE.md"),
             os.path.join(target_root, "CLAUDE.md"))
        )

    ignore_instructions, ignore_superpowers = prompt_gitignore_updates(
        instruction_names, input_function
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
    output_function("Installed project instructions into {0}".format(target_root))
    return True


if __name__ == "__main__":
    install_project()
