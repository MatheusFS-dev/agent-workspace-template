#!/usr/bin/env python2.7
"""Install Codex global assets on Linux with Python 2.7."""

from datetime import datetime
import errno
import glob
import io
import os
import shutil
import sys


GLOBAL_INSTRUCTIONS_PLACEHOLDER = "{{GLOBAL_INSTRUCTIONS}}"

try:
    import toml
except ImportError:
    raise ImportError(
        "Python 2 Codex installer requires toml==0.10.2; run python2.7 -m pip "
        "install -r scripts/linux/python2/requirements.txt."
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
        str: Absolute repository root containing the Codex template sources.

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


def render_codex_config(template_root):
    """Render Codex configuration from the global instructions source.

    Args:
        template_root (str): Absolute template repository root containing the
            configuration template and global instructions file.

    Returns:
        unicode: Valid TOML configuration with global instructions embedded.

    Raises:
        RuntimeError: If the placeholder count is not one, instructions cannot
            fit a TOML multiline literal, or the result is invalid TOML.
        IOError: If either source file cannot be read.
        UnicodeError: If either source file is not valid UTF-8.

    Examples:
        Render a repository configuration before writing it:

        >>> render_codex_config("/path/to/template")  # doctest: +SKIP
    """
    config_path = os.path.join(
        template_root, "configs", "codex", "config.toml.template"
    )
    instructions_path = os.path.join(template_root, "instructions", "global.md")
    config_text = read_text(config_path)
    instructions_text = read_text(instructions_path)

    placeholder_count = config_text.count(GLOBAL_INSTRUCTIONS_PLACEHOLDER)
    if placeholder_count != 1:
        raise RuntimeError(
            "Codex configuration template must contain exactly one "
            "{0!r} placeholder; found {1}.".format(
                GLOBAL_INSTRUCTIONS_PLACEHOLDER, placeholder_count
            )
        )
    if "'''" in instructions_text:
        raise RuntimeError(
            "Global instructions cannot contain three consecutive single quotes "
            "because they are rendered into a TOML multiline literal."
        )

    # Render from the canonical instructions source and reject any marker
    # introduced by that source instead of shipping unresolved configuration.
    rendered = config_text.replace(
        GLOBAL_INSTRUCTIONS_PLACEHOLDER, instructions_text
    )
    if GLOBAL_INSTRUCTIONS_PLACEHOLDER in rendered:
        raise RuntimeError("Rendered Codex configuration still contains a placeholder.")
    try:
        toml.loads(rendered)
    except (TypeError, ValueError) as error:
        raise RuntimeError(
            "Rendered Codex configuration is invalid TOML: {0}".format(error)
        )
    return rendered


def validate_sources(template_root):
    """Validate the sources required by the Codex workflow.

    Args:
        template_root (str): Absolute template repository root to validate.

    Returns:
        list of str: Sorted direct skill package directories containing
            SKILL.md files.

    Raises:
        RuntimeError: If a required source is missing, rendered TOML is
            invalid, or a direct skill package lacks SKILL.md.
        IOError: If a source cannot be read.
        UnicodeError: If a source is not valid UTF-8.
    """
    required_paths = (
        os.path.join(template_root, "instructions", "global.md"),
        os.path.join(template_root, "configs", "codex", "config.toml.template"),
        os.path.join(template_root, "skills"),
    )
    missing_paths = [path for path in required_paths if not os.path.exists(path)]
    if missing_paths:
        raise RuntimeError(
            "Codex template source is missing: {0}".format(", ".join(missing_paths))
        )

    render_codex_config(template_root)
    skills_root = os.path.join(template_root, "skills")
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


def prompt_codex_profiles(template_root, input_function):
    """Prompt for optional Codex profiles to install with the base config.

    Args:
        template_root (str): Absolute root containing Codex profile files.
        input_function (callable): Prompt callable returning the selection.

    Returns:
        list of str: Selected profile paths, or an empty list for a blank answer.

    Raises:
        ValueError: If a profile name is unknown, empty, or repeated.
    """
    profiles = sorted(
        glob.glob(os.path.join(template_root, "configs", "codex", "*.config.toml"))
    )
    if not profiles:
        return []

    suffix = ".config.toml"
    profile_by_name = dict(
        (os.path.basename(profile)[:-len(suffix)], profile) for profile in profiles
    )
    available_names = ", ".join(sorted(profile_by_name))
    response = input_function(
        "Codex profiles to install ({0}; blank for none): ".format(available_names)
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
        raise ValueError("Unknown Codex profile: {0}".format(", ".join(unknown_names)))
    return [profile_by_name[name] for name in selected_names]


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


def replace_path(source_path, destination_path, content):
    """Replace a destination with either a source copy or rendered text.

    Args:
        source_path (str or None): Copy source when content is None.
        destination_path (str): Target path to replace completely.
        content (unicode or None): Rendered UTF-8 text when source_path is None.

    Returns:
        None: The destination is replaced in place.

    Raises:
        RuntimeError: If neither or both source forms are supplied.
        IOError: With ENOENT if a requested copy source does not exist.
        OSError: If removal, directory creation, copying, or writing fails.
    """
    if (source_path is None) == (content is None):
        raise RuntimeError("Installation item must provide exactly one source form.")
    if source_path is not None and not path_exists(source_path):
        raise IOError(errno.ENOENT, "Installation source does not exist", source_path)

    if os.path.isdir(destination_path) and not os.path.islink(destination_path):
        shutil.rmtree(destination_path)
    elif path_exists(destination_path):
        os.unlink(destination_path)
    parent_path = os.path.dirname(destination_path)
    if not os.path.isdir(parent_path):
        os.makedirs(parent_path)

    if content is not None:
        with io.open(destination_path, "w", encoding="utf-8") as destination_file:
            destination_file.write(content)
    else:
        copy_path(source_path, destination_path)


def install_items(items, input_function, output_function):
    """Confirm conflicts, optionally back them up, and install all items.

    Args:
        items (list of tuple): Source, destination, and optional rendered
            content tuples.
        input_function (callable): Prompt callable used only for conflicts.
        output_function (callable): Status callable for conflicts and backups.

    Returns:
        bool: True after installation; false when replacement is declined
            before any files are changed.

    Raises:
        OSError: If a backup, removal, copy, or write fails.
        ValueError: If an interactive confirmation is invalid.

    Examples:
        Install rendered configuration into an empty destination:

        >>> install_items([(None, "/target", u"x = 1\n")], lambda _: "", output_text)
        True
    """
    # Resolve every conflict before the first write so cancellation leaves the
    # destination tree untouched.
    conflicts = [
        destination for _, destination, _ in items if path_exists(destination)
    ]
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

    for source_path, destination_path, content in items:
        replace_path(source_path, destination_path, content)
    return True


def install_global_codex(
        template_root=None, home_root=None, input_function=raw_input,
        output_function=output_text):
    """Interactively install Codex global configuration, profiles, and skills.

    Args:
        template_root (str): Template root to use; None derives it from this
            script. Defaults to None.
        home_root (str): User home directory to target; None expands '~'.
            Defaults to None.
        input_function (callable): Prompt callable for profile and conflict
            decisions. Defaults to raw_input.
        output_function (callable): Status callable for conflicts, backups, and
            the final result. Defaults to output_text.

    Returns:
        bool: True after installation, or false if replacement is declined.

    Raises:
        RuntimeError: If Linux is not active, sources are missing, or rendered
            TOML is invalid.
        OSError: If files cannot be read, backed up, copied, or written.
        ValueError: If a profile selection or confirmation is invalid.

    Examples:
        Install from explicit template and home directories:

        >>> install_global_codex("/template", "/tmp/home", lambda _: "")  # doctest: +SKIP
        True
    """
    validate_platform()
    root = template_root or get_template_root()
    home = home_root or os.path.expanduser("~")
    skill_packages = validate_sources(root)
    selected_profiles = prompt_codex_profiles(root, input_function)
    codex_root = os.path.join(home, ".codex")
    items = [
        (None, os.path.join(codex_root, "config.toml"), render_codex_config(root))
    ]
    items.extend(
        (profile, os.path.join(codex_root, os.path.basename(profile)), None)
        for profile in selected_profiles
    )
    items.extend(
        (package, os.path.join(codex_root, "skills", os.path.basename(package)), None)
        for package in skill_packages
    )
    installed = install_items(items, input_function, output_function)
    if installed:
        output_function("Installed Codex global template into {0}".format(codex_root))
    return installed


if __name__ == "__main__":
    install_global_codex()
