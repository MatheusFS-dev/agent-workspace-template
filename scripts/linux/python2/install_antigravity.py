#!/usr/bin/env python2.7
"""Install Antigravity CLI global assets on Linux with Python 2.7."""

from datetime import datetime
import errno
import glob
import io
import json
import os
import shutil
import sys


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
        str: Absolute repository root containing the Antigravity template sources.

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


def read_text(path):
    """Read a UTF-8 text file completely.

    Args:
        path (str): Existing text file to read.

    Returns:
        unicode: Decoded file contents.

    Raises:
        IOError: If the file cannot be opened or read.
        UnicodeError: If the file is not valid UTF-8.
    """
    with io.open(path, "r", encoding="utf-8") as source_file:
        return source_file.read()


def validate_sources(template_root):
    """Validate the sources required by the Antigravity workflow.

    Args:
        template_root (str): Absolute template repository root to validate.

    Returns:
        list of str: Sorted direct skill package directories containing
            SKILL.md files.

    Raises:
        RuntimeError: If a required source is missing, settings JSON is
            invalid, or a direct skill package lacks SKILL.md.
        IOError: If a source cannot be read.
        UnicodeError: If the settings file is not valid UTF-8.
    """
    instructions_path = os.path.join(template_root, "instructions", "global.md")
    settings_path = os.path.join(template_root, "configs", "antigravity", "settings.json")
    skills_root = os.path.join(template_root, "skills")
    required_paths = (instructions_path, settings_path, skills_root)
    missing_paths = [path for path in required_paths if not os.path.exists(path)]
    if missing_paths:
        raise RuntimeError(
            "Antigravity template source is missing: {0}".format(", ".join(missing_paths))
        )

    try:
        json.loads(read_text(settings_path))
    except ValueError as error:
        raise RuntimeError("Invalid JSON source {0}: {1}".format(settings_path, error))

    skill_packages = sorted(
        path for path in glob.glob(os.path.join(skills_root, "*"))
        if os.path.isdir(path)
    )
    invalid_packages = [
        package for package in skill_packages
        if not os.path.isfile(os.path.join(package, "SKILL.md"))
    ]
    if invalid_packages:
        raise RuntimeError(
            "Every source skill must be a direct skills/<name>/SKILL.md package: {0}".format(
                ", ".join(invalid_packages)
            )
        )
    return skill_packages


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
    if not path_exists(source_path):
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


def install_global_antigravity(
        template_root=None, home_root=None, input_function=raw_input,
        output_function=output_text):
    """Interactively install Antigravity global instructions, settings, and skills.

    Args:
        template_root (str): Template root to use; None derives it from this
            script. Defaults to None.
        home_root (str): User home directory to target; None expands '~'.
            Defaults to None.
        input_function (callable): Prompt callable for conflict decisions.
            Defaults to raw_input.
        output_function (callable): Status callable for conflicts, backups, and
            the final result. Defaults to output_text.

    Returns:
        bool: True after installation, or false if replacement is declined.

    Raises:
        RuntimeError: If Linux is not active or required sources are invalid.
        OSError: If files cannot be read, backed up, copied, or written.
        ValueError: If a confirmation is invalid.

    Examples:
        Install from explicit template and home directories:

        >>> install_global_antigravity("/template", "/tmp/home")  # doctest: +SKIP
        True
    """
    validate_platform()
    root = template_root or get_template_root()
    home = home_root or os.path.expanduser("~")
    skill_packages = validate_sources(root)
    gemini_root = os.path.join(home, ".gemini")
    antigravity_root = os.path.join(gemini_root, "antigravity-cli")
    items = [
        (os.path.join(root, "instructions", "global.md"),
         os.path.join(gemini_root, "GEMINI.md")),
        (os.path.join(root, "configs", "antigravity", "settings.json"),
         os.path.join(antigravity_root, "settings.json")),
    ]
    items.extend(
        (package, os.path.join(antigravity_root, "skills", os.path.basename(package)))
        for package in skill_packages
    )
    installed = install_items(items, input_function, output_function)
    if installed:
        output_function(
            "Installed Antigravity CLI global template into {0}".format(gemini_root)
        )
    return installed


if __name__ == "__main__":
    install_global_antigravity()

