#!/usr/bin/env python2.7
"""Expose Python 2.7 agent installers through the toolbox JSON protocol."""

import glob
import imp
import json
import os
import sys


SCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_ROOT = os.path.abspath(os.path.join(SCRIPT_ROOT, "..", "..", ".."))
COMMAND_MODULES = {
    "setup-agents-codex": "codex",
    "setup-agents-claude": "claude",
    "setup-agents-antigravity": "antigravity",
    "setup-agents-project": "project",
}
BASE_QUESTION_IDS = {
    "setup-agents-codex": ("profiles",),
    "setup-agents-claude": (),
    "setup-agents-antigravity": (),
    "setup-agents-project": (
        "target_directory",
        "agent_formats",
        "ignore_agent_files",
        "ignore_superpowers",
    ),
}
CONFLICT_QUESTION_IDS = ("replace_conflicts", "create_backups")
STRING_TYPES = (basestring,)


def load_installer(name):
    """Load one sibling Python 2.7 standalone installer.

    Args:
        name (str): Installer suffix from codex, claude, antigravity, or
            project.

    Returns:
        module: Loaded installer providing validation and file operations.

    Raises:
        ImportError: If the installer or its required TOML dependency cannot
            be imported.
        IOError: If the installer source cannot be read.
    """
    path = os.path.join(SCRIPT_ROOT, "install_{0}.py".format(name))
    return imp.load_source("toolbox_install_{0}".format(name), path)


INSTALLERS = dict(
    (name, load_installer(name)) for name in set(COMMAND_MODULES.values())
)


def question(question_id, question_type, title, options=None):
    """Build one typed questionnaire response.

    Args:
        question_id (str): Stable answer key unique within one workflow.
        question_type (str): Text, confirm, single, or multiple control type.
        title (str): User-facing prompt text.
        options (list of dict): Selection values and labels. Defaults to None
            for text and confirmation controls.

    Returns:
        dict: Protocol response with status question.

    Raises:
        None.
    """
    value = {
        "status": "question",
        "question": {
            "id": question_id,
            "type": question_type,
            "title": title,
        },
    }
    if options is not None:
        value["question"]["options"] = options
    return value


def require_string_list(value, answer_id):
    """Validate a multiple-selection answer.

    Args:
        value (object): Candidate JSON answer.
        answer_id (str): Identifier included in validation errors.

    Returns:
        list of str: Unique non-empty submitted values in order.

    Raises:
        TypeError: If the answer is not a list of strings.
        ValueError: If a value is empty or repeated.
    """
    if not isinstance(value, list) or not all(
            isinstance(item, STRING_TYPES) for item in value):
        raise TypeError("answer {0!r} must be a list of strings".format(answer_id))
    if any(not item for item in value):
        raise ValueError(
            "answer {0!r} cannot contain an empty value".format(answer_id)
        )
    if len(set(value)) != len(value):
        raise ValueError(
            "answer {0!r} cannot contain duplicate values".format(answer_id)
        )
    return value


def validate_request(request):
    """Validate a questionnaire or run request envelope.

    Args:
        request (object): Decoded JSON object with operation, package context,
            accumulated answers, and direct-command arguments.

    Returns:
        tuple: Command name, operation, answers mapping, and argument list.

    Raises:
        TypeError: If the envelope or one of its fields has the wrong type.
        ValueError: If a required field is missing or unsupported.
    """
    if not isinstance(request, dict):
        raise TypeError("request must be a JSON object")
    operation = request.get("operation")
    if operation not in ("questions", "run"):
        raise ValueError("operation must be 'questions' or 'run'")
    package = request.get("package")
    if not isinstance(package, dict):
        raise TypeError("package must be a JSON object")
    if package.get("name") != "agent-workspace-template":
        raise ValueError("package name must be 'agent-workspace-template'")
    command = package.get("command")
    if command not in COMMAND_MODULES:
        raise ValueError("unsupported command: {0!r}".format(command))
    answers = request.get("answers")
    if not isinstance(answers, dict):
        raise TypeError("answers must be a JSON object")
    allowed = set(BASE_QUESTION_IDS[command]) | set(CONFLICT_QUESTION_IDS)
    unknown = sorted(set(answers) - allowed)
    if unknown:
        raise ValueError("unknown answer IDs: {0}".format(", ".join(unknown)))
    arguments = request.get("arguments")
    if not isinstance(arguments, list) or not all(
            isinstance(argument, STRING_TYPES) for argument in arguments):
        raise TypeError("arguments must be a list of strings")
    if arguments:
        raise ValueError("{0} does not accept arguments".format(command))
    return command, operation, answers, arguments


def validate_available_answers(command, answers, template_root):
    """Validate every supplied answer before routing the next question.

    Args:
        command (str): Supported setup command owning the answers.
        answers (dict): Accumulated questionnaire answers.
        template_root (str): Template root used to enumerate profiles.

    Returns:
        None: All supplied answers are valid.

    Raises:
        TypeError: If an answer has the wrong JSON type.
        ValueError: If an answer contains an unsupported selection.
    """
    for answer_id in CONFLICT_QUESTION_IDS:
        if answer_id in answers and not isinstance(answers[answer_id], bool):
            raise TypeError("answer {0!r} must be a boolean".format(answer_id))
    if command == "setup-agents-codex" and "profiles" in answers:
        profiles = require_string_list(answers["profiles"], "profiles")
        available = set(
            os.path.basename(path)[:-len(".config.toml")]
            for path in glob.glob(
                os.path.join(template_root, "configs", "codex", "*.config.toml")
            )
            if os.path.basename(path) != "config.toml.template"
        )
        unknown = sorted(set(profiles) - available)
        if unknown:
            raise ValueError(
                "unknown Codex profiles: {0}".format(", ".join(unknown))
            )
    if command == "setup-agents-project":
        if "target_directory" in answers and not isinstance(
                answers["target_directory"], STRING_TYPES):
            raise TypeError("answer 'target_directory' must be a string")
        if "target_directory" in answers and not answers["target_directory"].strip():
            raise ValueError("answer 'target_directory' cannot be empty")
        if "agent_formats" in answers:
            formats = require_string_list(answers["agent_formats"], "agent_formats")
            if not formats:
                raise ValueError("answer 'agent_formats' must select at least one value")
            unknown = sorted(
                set(formats) - set(("codex", "claude", "antigravity"))
            )
            if unknown:
                raise ValueError(
                    "unknown agent formats: {0}".format(", ".join(unknown))
                )
        for answer_id in ("ignore_agent_files", "ignore_superpowers"):
            if answer_id in answers and not isinstance(answers[answer_id], bool):
                raise TypeError("answer {0!r} must be a boolean".format(answer_id))


def next_base_question(command, answers, template_root):
    """Return the next unresolved non-conflict question.

    Args:
        command (str): Supported setup command.
        answers (dict): Validated accumulated answers.
        template_root (str): Template root used for profile options.

    Returns:
        dict or None: Typed question, or None when preparation can start.

    Raises:
        OSError: If profile sources cannot be enumerated.
    """
    if command == "setup-agents-codex" and "profiles" not in answers:
        profile_names = sorted(
            os.path.basename(path)[:-len(".config.toml")]
            for path in glob.glob(
                os.path.join(template_root, "configs", "codex", "*.config.toml")
            )
            if os.path.basename(path) != "config.toml.template"
        )
        return question(
            "profiles",
            "multiple",
            "Codex profiles to install",
            [{"value": name, "label": name} for name in profile_names],
        )
    if command == "setup-agents-project":
        questions = (
            ("target_directory", "text", "Target project directory", None),
            (
                "agent_formats",
                "multiple",
                "Agent instruction formats to install",
                [
                    {"value": "codex", "label": "Codex"},
                    {"value": "claude", "label": "Claude"},
                    {"value": "antigravity", "label": "Antigravity"},
                ],
            ),
            (
                "ignore_agent_files", "confirm",
                "Add installed agent instruction files to .gitignore?", None,
            ),
            (
                "ignore_superpowers", "confirm",
                "Add Superpowers output directories to .gitignore?", None,
            ),
        )
        for answer_id, answer_type, title, options in questions:
            if answer_id not in answers:
                return question(answer_id, answer_type, title, options)
    return None


def prepare(command, answers, template_root=None, home_root=None):
    """Construct validated installation items without writing files.

    Args:
        command (str): One of the four setup-agents command names.
        answers (dict): Complete non-conflict answer mapping.
        template_root (str): Template source root. Defaults to the root derived
            from this adapter.
        home_root (str): Home destination for global workflows. Defaults to
            the current user's expanded home path.

    Returns:
        dict: Prepared items, conflicts, ignore paths, and installer context.

    Raises:
        RuntimeError: If the platform or sources are invalid.
        TypeError: If an answer has the wrong type.
        ValueError: If a required answer is missing or unsupported.
        IOError: If source files cannot be read.
        OSError: If source paths cannot be enumerated.
    """
    if command not in COMMAND_MODULES:
        raise ValueError("unsupported command: {0!r}".format(command))
    root = template_root or TEMPLATE_ROOT
    home = home_root or os.path.expanduser("~")
    validate_available_answers(command, answers, root)
    missing = [name for name in BASE_QUESTION_IDS[command] if name not in answers]
    if missing:
        raise ValueError("missing answer: {0}".format(missing[0]))
    installer = INSTALLERS[COMMAND_MODULES[command]]
    installer.validate_platform()
    ignored_paths = []
    target_root = None

    if command == "setup-agents-codex":
        skills = installer.validate_sources(root)
        profile_paths = glob.glob(
            os.path.join(root, "configs", "codex", "*.config.toml")
        )
        profiles = dict(
            (os.path.basename(path)[:-len(".config.toml")], path)
            for path in profile_paths
            if os.path.basename(path) != "config.toml.template"
        )
        destination_root = os.path.join(home, ".codex")
        items = [(
            None,
            os.path.join(destination_root, "config.toml"),
            installer.render_codex_config(root),
        )]
        items.extend(
            (profiles[name], os.path.join(destination_root, os.path.basename(profiles[name])), None)
            for name in answers["profiles"]
        )
        items.extend(
            (skill, os.path.join(destination_root, "skills", os.path.basename(skill)), None)
            for skill in skills
        )
        success_message = "Installed Codex global template into {0}".format(
            destination_root
        )
    elif command in ("setup-agents-claude", "setup-agents-antigravity"):
        skills = installer.validate_sources(root)
        agent_name = COMMAND_MODULES[command]
        if agent_name == "claude":
            destination_root = os.path.join(home, ".claude")
            assets_root = destination_root
            instruction_name = "CLAUDE.md"
        else:
            destination_root = os.path.join(home, ".gemini")
            assets_root = os.path.join(destination_root, "antigravity-cli")
            instruction_name = "GEMINI.md"
        items = [
            (
                os.path.join(root, "instructions", "global.md"),
                os.path.join(destination_root, instruction_name),
            ),
            (
                os.path.join(root, "configs", agent_name, "settings.json"),
                os.path.join(assets_root, "settings.json"),
            ),
        ]
        items.extend(
            (skill, os.path.join(assets_root, "skills", os.path.basename(skill)))
            for skill in skills
        )
        display_name = "Claude" if agent_name == "claude" else "Antigravity CLI"
        success_message = "Installed {0} global template into {1}".format(
            display_name, destination_root
        )
    else:
        installer.validate_sources(root)
        target_root = os.path.abspath(os.path.expanduser(answers["target_directory"]))
        if not os.path.exists(target_root):
            raise IOError("Target project directory does not exist: {0}".format(target_root))
        if not os.path.isdir(target_root):
            raise ValueError("Target project path is not a directory: {0}".format(target_root))
        selected = set(answers["agent_formats"])
        instruction_names = []
        items = []
        if selected & set(("codex", "antigravity")):
            instruction_names.append("AGENTS.md")
            items.append((
                os.path.join(root, "project", "AGENTS.md"),
                os.path.join(target_root, "AGENTS.md"),
            ))
        if "claude" in selected:
            instruction_names.append("CLAUDE.md")
            items.append((
                os.path.join(root, "project", "CLAUDE.md"),
                os.path.join(target_root, "CLAUDE.md"),
            ))
        if answers["ignore_agent_files"]:
            ignored_paths.extend(instruction_names)
        if answers["ignore_superpowers"]:
            ignored_paths.extend(installer.SUPERPOWERS_GITIGNORE_LINES)
        success_message = "Installed project instructions into {0}".format(target_root)

    if command == "setup-agents-codex":
        conflicts = [destination for _, destination, _ in items if installer.path_exists(destination)]
    else:
        conflicts = [destination for _, destination in items if installer.path_exists(destination)]
    return {
        "installer": installer,
        "items": items,
        "conflicts": conflicts,
        "target_root": target_root,
        "ignored_paths": ignored_paths,
        "success_message": success_message,
    }


def apply(preparation, replace_conflicts, create_backups, output_function=None):
    """Apply one prepared installation using explicit decisions.

    Args:
        preparation (dict): Result returned by prepare.
        replace_conflicts (bool): Replace all conflicts when true; reject the
            preparation before writes when false.
        create_backups (bool): Copy conflicts to adjacent backups when true;
            write no backups when false.
        output_function (callable): Receives backup and completion messages.
            Defaults to the installer's Unicode-safe output function.

    Returns:
        None: Prepared items and ignore selections are applied.

    Raises:
        TypeError: If either decision is not a boolean.
        ValueError: If replacement is declined for existing conflicts.
        OSError: If backup or replacement operations fail.
    """
    if not isinstance(replace_conflicts, bool):
        raise TypeError("replace_conflicts must be a boolean")
    if not isinstance(create_backups, bool):
        raise TypeError("create_backups must be a boolean")
    conflicts = preparation["conflicts"]
    if conflicts and not replace_conflicts:
        raise ValueError("replacement was declined for conflicting paths")
    installer = preparation["installer"]
    output = output_function or installer.output_text
    if create_backups:
        for conflict in conflicts:
            output("Backed up {0} to {1}".format(conflict, installer.copy_backup(conflict)))
    if len(preparation["items"][0]) == 3:
        for source, destination, content in preparation["items"]:
            installer.replace_path(source, destination, content)
    else:
        for source, destination in preparation["items"]:
            installer.replace_path(source, destination)
    if preparation["ignored_paths"]:
        installer.update_gitignore(
            preparation["target_root"], preparation["ignored_paths"]
        )
    output(preparation["success_message"])


def handle_request(request, template_root=None, home_root=None, output_function=None):
    """Route one protocol request through questions, skip, or apply.

    Args:
        request (object): Decoded protocol request.
        template_root (str): Template root override. Defaults to the repository
            root derived from this script.
        home_root (str): Home destination override. Defaults to the current
            user's expanded home path.
        output_function (callable): Receives apply messages for run requests.
            Defaults to the installer's output function.

    Returns:
        dict: One question, ready, or skipped protocol response.

    Raises:
        TypeError: If request data has the wrong type.
        ValueError: If request data or run state is invalid.
        RuntimeError: If platform or template validation fails.
        OSError: If preparation or application fails.
    """
    command, operation, answers, unused_arguments = validate_request(request)
    del unused_arguments
    root = template_root or TEMPLATE_ROOT
    validate_available_answers(command, answers, root)
    next_question = next_base_question(command, answers, root)
    if next_question is not None:
        if operation == "run":
            raise ValueError(
                "missing answer: {0}".format(next_question["question"]["id"])
            )
        return next_question
    preparation = prepare(command, answers, root, home_root)
    if preparation["conflicts"]:
        if "replace_conflicts" not in answers:
            if operation == "run":
                raise ValueError("missing answer: replace_conflicts")
            return question(
                "replace_conflicts", "confirm", "Replace all conflicting paths?"
            )
        if not answers["replace_conflicts"]:
            reason = "replacement declined: " + ", ".join(preparation["conflicts"])
            if operation == "run":
                raise ValueError(reason)
            return {"status": "skipped", "reason": reason}
        if "create_backups" not in answers:
            if operation == "run":
                raise ValueError("missing answer: create_backups")
            return question(
                "create_backups", "confirm",
                "Create backups of conflicting paths?",
            )
    if operation == "questions":
        return {"status": "ready"}
    apply(
        preparation,
        answers.get("replace_conflicts", False),
        answers.get("create_backups", False),
        output_function,
    )
    return {"status": "ready"}


if __name__ == "__main__":
    try:
        request = json.load(sys.stdin)
        response = handle_request(
            request, output_function=lambda message: sys.stderr.write(
                "{0}\n".format(message)
            )
        )
        sys.stdout.write("{0}\n".format(json.dumps(response, sort_keys=True)))
    except Exception as error:
        sys.stderr.write("toolbox adapter error: {0}\n".format(error))
        raise SystemExit(1)
