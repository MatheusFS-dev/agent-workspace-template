#!/usr/bin/env python3
"""Expose agent template installers through the toolbox JSON protocol."""

import importlib.util
import json
from pathlib import Path
import sys


SCRIPT_ROOT = Path(__file__).resolve().parent
TEMPLATE_ROOT = Path(__file__).resolve().parents[2]
COMMAND_MODULES = {
    "setup-agents-codex": "codex",
    "setup-agents-claude": "claude",
    "setup-agents-antigravity": "antigravity",
    "setup-agents-opencode": "opencode",
    "setup-agents-project": "project",
}
BASE_QUESTION_IDS = {
    "setup-agents-codex": ("profiles",),
    "setup-agents-claude": ("profiles",),
    "setup-agents-antigravity": ("profiles",),
    "setup-agents-opencode": (),
    "setup-agents-project": (
        "target_directory",
        "agent_formats",
        "ignore_agent_files",
        "ignore_superpowers",
    ),
}
def maestro_guide(command, answers, template_root):
    """Return the launch instructions for a setup that installed Maestro."""
    if command == "setup-agents-codex":
        if "maestro" not in answers["profiles"]:
            return ""
        return (
            "Maestro is ready for local-LLM coding.\n\n"
            "  Start a Maestro session:\n"
            "    codex --profile maestro\n\n"
            "  Then describe the coding task. Maestro delegates implementation and\n"
            "  verification to its local worker MCP server."
        )
    if command == "setup-agents-claude" and "maestro" in answers["profiles"] and (template_root / "configs" / "claude" / "agents" / "maestro.md").is_file():
        return (
            "Maestro is ready for local-LLM coding.\n\n"
            "  Start a Maestro session:\n"
            "    claude --agent maestro\n\n"
            "  Then describe the coding task. Maestro delegates implementation and\n"
            "  verification to its local worker MCP server."
        )
    if command == "setup-agents-antigravity" and "maestro" in answers["profiles"] and (template_root / "configs" / "antigravity" / "agents" / "maestro" / "agent.md").is_file():
        return (
            "Maestro is ready for local-LLM coding.\n\n"
            "  Antigravity's installed profile is read-only and has no native Maestro\n"
            "  worker MCP integration. Start Codex or Claude Maestro instead."
        )
    return ""
CONFLICT_QUESTION_IDS = ("replace_conflicts", "create_backups")


def load_installer(name):
    """Load one sibling standalone installer without changing its behavior.

    Args:
        name (str): Installer suffix from ``codex``, ``claude``,
            ``antigravity``, or ``project``.

    Returns:
        module: Imported installer module providing validation and file
        operations.

    Raises:
        ImportError: If the installer module cannot be loaded.
        OSError: If the installer source cannot be read.

    Examples:
        Load the Codex installer implementation:

        >>> load_installer("codex").__name__.endswith("codex")
        True
    """
    path = SCRIPT_ROOT / f"install_{name}.py"
    spec = importlib.util.spec_from_file_location(f"toolbox_install_{name}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load installer: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


INSTALLERS = {name: load_installer(name) for name in set(COMMAND_MODULES.values())}


def question(question_id, question_type, title, options=None, default=None, required=False):
    """Build one typed questionnaire response.

    Args:
        question_id (str): Stable answer key unique within a tool workflow.
        question_type (str): One of ``text``, ``confirm``, ``single``, or
            ``multiple``; the toolbox renders the corresponding form control.
        title (str): User-facing prompt shown by the toolbox.
        options (list of dict): Selection values and labels for ``single`` or
            ``multiple`` questions. Defaults to no options for text and
            confirmation questions.

    Returns:
        dict: Protocol response with status ``question``.

    Raises:
        None.

    Examples:
        Build a confirmation question:

        >>> question("replace", "confirm", "Replace?")["status"]
        'question'
    """
    value = {
        "status": "question",
        "question": {
            "id": question_id,
            "type": question_type,
            "title": title,
            "default": default,
            "required": required,
        },
    }
    if options is not None:
        value["question"]["options"] = options
    return value


def _require_string_list(value, answer_id):
    """Validate a multiple-selection answer as unique non-empty strings.

    Args:
        value (object): Candidate answer received from JSON.
        answer_id (str): Answer identifier included in validation errors.

    Returns:
        list of str: Validated values in the submitted order.

    Raises:
        TypeError: If the value is not a list of strings.
        ValueError: If a value is empty or repeated.
    """
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise TypeError(f"answer {answer_id!r} must be a list of strings")
    if any(not item for item in value):
        raise ValueError(f"answer {answer_id!r} cannot contain an empty value")
    if len(set(value)) != len(value):
        raise ValueError(f"answer {answer_id!r} cannot contain duplicate values")
    return value


def _validate_request(request):
    """Validate the fixed envelope shared by questionnaire and run requests.

    Args:
        request (object): Decoded JSON request containing operation, package
            context, accumulated answers, and direct-command arguments.

    Returns:
        tuple: Command name, operation, answers mapping, and argument list.

    Raises:
        TypeError: If the request or one of its fields has the wrong type.
        ValueError: If a required field is missing or contains an unsupported
            value, package, answer identifier, or direct argument.
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
        raise ValueError(f"unsupported command: {command!r}")
    answers = request.get("answers")
    if not isinstance(answers, dict):
        raise TypeError("answers must be a JSON object")
    allowed_answers = set(BASE_QUESTION_IDS[command]) | set(CONFLICT_QUESTION_IDS)
    unknown_answers = sorted(set(answers) - allowed_answers)
    if unknown_answers:
        raise ValueError(f"unknown answer IDs: {', '.join(unknown_answers)}")
    arguments = request.get("arguments")
    if not isinstance(arguments, list) or not all(
        isinstance(argument, str) for argument in arguments
    ):
        raise TypeError("arguments must be a list of strings")
    if arguments:
        raise ValueError(f"{command} does not accept arguments")
    return command, operation, answers, arguments


def _validate_available_answers(command, answers, template_root):
    """Validate each supplied answer before it influences question routing.

    Args:
        command (str): Supported setup command owning the answers.
        answers (dict): Accumulated questionnaire answers.
        template_root (Path): Template root used to enumerate Codex profiles.

    Returns:
        None: Every currently supplied answer is valid.

    Raises:
        TypeError: If an answer has the wrong JSON type.
        ValueError: If an answer contains an unsupported selection.
    """
    for answer_id in CONFLICT_QUESTION_IDS:
        if answer_id in answers and not isinstance(answers[answer_id], bool):
            raise TypeError(f"answer {answer_id!r} must be a boolean")

    if command in ("setup-agents-codex", "setup-agents-claude", "setup-agents-antigravity") and "profiles" in answers:
        profiles = _require_string_list(answers["profiles"], "profiles")
        unknown = sorted(set(profiles) - {"maestro"})
        if unknown:
            raise ValueError(f"unknown Maestro profiles: {', '.join(unknown)}")

    if command == "setup-agents-project":
        if "target_directory" in answers and not isinstance(
            answers["target_directory"], str
        ):
            raise TypeError("answer 'target_directory' must be a string")
        if "target_directory" in answers and not answers["target_directory"].strip():
            raise ValueError("answer 'target_directory' cannot be empty")
        if "agent_formats" in answers:
            formats = _require_string_list(answers["agent_formats"], "agent_formats")
            if not formats:
                raise ValueError("answer 'agent_formats' must select at least one value")
            unknown = sorted(set(formats) - {"codex", "claude", "antigravity", "opencode"})
            if unknown:
                raise ValueError(f"unknown agent formats: {', '.join(unknown)}")
        for answer_id in ("ignore_agent_files", "ignore_superpowers"):
            if answer_id in answers and not isinstance(answers[answer_id], bool):
                raise TypeError(f"answer {answer_id!r} must be a boolean")


def _next_base_question(command, answers, template_root):
    """Return the next unresolved non-conflict question for one command.

    Args:
        command (str): Supported setup command.
        answers (dict): Validated accumulated answers.
        template_root (Path): Template root used to enumerate profile options.

    Returns:
        dict or None: Typed question response, or None when preparation can
        discover destination conflicts.

    Raises:
        OSError: If profile source directories cannot be enumerated.
    """
    if command in ("setup-agents-codex", "setup-agents-claude", "setup-agents-antigravity") and "profiles" not in answers:
        return question(
            "profiles",
            "multiple",
            f"{COMMAND_MODULES[command].capitalize()} profiles to install",
            [{"value": "maestro", "label": "maestro"}],
            ["maestro"],
        )
    if command == "setup-agents-project":
        questions = (
            ("target_directory", "text", "Target project directory", None, str(Path.cwd())),
            (
                "agent_formats",
                "multiple",
                "Agent instruction formats to install",
                [
                    {"value": "codex", "label": "Codex"},
                    {"value": "claude", "label": "Claude"},
                    {"value": "antigravity", "label": "Antigravity"},
                    {"value": "opencode", "label": "OpenCode"},
                ],
                ["codex", "antigravity", "claude"],
            ),
            (
                "ignore_agent_files",
                "confirm",
                "Add installed agent instruction files to .gitignore?",
                None,
                False,
            ),
            (
                "ignore_superpowers",
                "confirm",
                "Add Superpowers output directories to .gitignore?",
                None,
                True,
            ),
        )
        for answer_id, answer_type, title, options, default in questions:
            if answer_id not in answers:
                return question(answer_id, answer_type, title, options, default)
    return None


def prepare(command, answers, template_root=None, home_root=None):
    """Validate selections and construct installation items without writing.

    Args:
        command (str): One of the four ``setup-agents-*`` command names.
        answers (dict): Complete non-conflict answer mapping for the command.
        template_root (Path): Template source root. Defaults to the root derived
            from this adapter location.
        home_root (Path): User home destination for global workflows. Defaults
            to ``Path.home()``; project workflows use ``target_directory``.

    Returns:
        dict: Prepared installer module, immutable input-derived item list,
        conflict paths, optional ignore paths, and success message.

    Raises:
        RuntimeError: If the platform or required template sources are invalid.
        TypeError: If an answer has the wrong type.
        ValueError: If a required answer is missing or unsupported.
        FileNotFoundError: If the project target does not exist.
        NotADirectoryError: If the project target is not a directory.
        OSError: If sources cannot be read or enumerated.

    Examples:
        Prepare a Claude installation without applying it:

        >>> prepare("setup-agents-claude", {})["conflicts"]  # doctest: +SKIP
        []
    """
    if command not in COMMAND_MODULES:
        raise ValueError(f"unsupported command: {command!r}")
    root = Path(template_root) if template_root is not None else TEMPLATE_ROOT
    home = Path(home_root) if home_root is not None else Path.home()
    _validate_available_answers(command, answers, root)
    missing = [name for name in BASE_QUESTION_IDS[command] if name not in answers]
    if missing:
        raise ValueError(f"missing answer: {missing[0]}")

    installer = INSTALLERS[COMMAND_MODULES[command]]
    installer.validate_platform()
    ignored_paths = []
    target_root = None

    if command == "setup-agents-codex":
        skill_packages = installer.validate_sources(root)
        profiles_by_name = {
            path.name.removesuffix(".config.toml"): path
            for path in sorted((root / "configs" / "codex").glob("*.config.toml"))
            if path.name != "config.toml.template"
        }
        selected_profiles = [profiles_by_name[name] for name in answers["profiles"]]
        destination_root = home / ".codex"
        items = [(None, destination_root / "config.toml", installer.render_codex_config(root))]
        for profile in selected_profiles:
            if profile.name == "maestro.config.toml":
                items.append(
                    (
                        None,
                        destination_root / profile.name,
                        installer.render_maestro_config(root),
                    )
                )
                items.append(
                    (
                        root / "configs" / "codex" / "maestro_guard.py",
                        destination_root / "maestro_guard.py",
                        None,
                    )
                )
            else:
                items.append((profile, destination_root / profile.name, None))
        items.extend(
            (package, destination_root / "skills" / package.name, None)
            for package in skill_packages
        )
        success_message = f"Installed Codex global template into {destination_root}"
    elif command == "setup-agents-opencode":
        skill_packages = installer.validate_sources(root)
        destination_root = home / ".config" / "opencode"
        items = [
            (root / "instructions" / "global.md", destination_root / "AGENTS.md"),
            (root / "configs" / "opencode" / "opencode.json", destination_root / "opencode.json"),
        ]
        items.extend((package, destination_root / "skills" / package.name) for package in skill_packages)
        success_message = f"Installed OpenCode global template into {destination_root}"
    elif command in ("setup-agents-claude", "setup-agents-antigravity"):
        skill_packages = installer.validate_sources(root)
        agent_name = COMMAND_MODULES[command]
        if agent_name == "claude":
            destination_root = home / ".claude"
            instruction_root = destination_root
            assets_root = destination_root
            instruction_name = "CLAUDE.md"
        else:
            destination_root = home / ".gemini"
            instruction_root = destination_root
            assets_root = destination_root / "antigravity-cli"
            instruction_name = "GEMINI.md"
        items = [
            (root / "instructions" / "global.md", instruction_root / instruction_name),
            (
                root / "configs" / agent_name / "settings.json",
                assets_root / "settings.json",
            ),
        ]
        if agent_name == "claude":
            maestro_source = root / "configs" / "claude" / "agents" / "maestro.md"
            if "maestro" in answers["profiles"] and maestro_source.is_file():
                items.append((maestro_source, destination_root / "agents" / "maestro.md"))
        else:
            maestro_source = root / "configs" / "antigravity" / "agents" / "maestro" / "agent.md"
            if "maestro" in answers["profiles"] and maestro_source.is_file():
                items.append((maestro_source, destination_root / "config" / "agents" / "maestro" / "agent.md"))
        items.extend(
            (package, assets_root / "skills" / package.name)
            for package in skill_packages
        )
        display_name = "Claude" if agent_name == "claude" else "Antigravity CLI"
        success_message = f"Installed {display_name} global template into {destination_root}"
    else:
        installer.validate_sources(root)
        target_root = Path(answers["target_directory"]).expanduser().resolve()
        if not target_root.exists():
            raise FileNotFoundError(f"Target project directory does not exist: {target_root}")
        if not target_root.is_dir():
            raise NotADirectoryError(f"Target project path is not a directory: {target_root}")
        selected_tools = set(answers["agent_formats"])
        instruction_names = []
        items = []
        if selected_tools & {"codex", "antigravity", "opencode"}:
            instruction_names.append("AGENTS.md")
            items.append((root / "project" / "AGENTS.md", target_root / "AGENTS.md"))
        if "claude" in selected_tools:
            instruction_names.append("CLAUDE.md")
            items.append((root / "project" / "CLAUDE.md", target_root / "CLAUDE.md"))
        if answers["ignore_agent_files"]:
            ignored_paths.extend(instruction_names)
        if answers["ignore_superpowers"]:
            ignored_paths.extend(installer.SUPERPOWERS_GITIGNORE_LINES)
        success_message = f"Installed project instructions into {target_root}"

    # Conflict discovery is deliberately the last preparation step and performs
    # only path inspection, so every question can be answered before any write.
    if command == "setup-agents-codex":
        conflicts = [str(destination) for _, destination, _ in items if installer.path_exists(destination)]
    else:
        conflicts = [str(destination) for _, destination in items if installer.path_exists(destination)]
    return {
        "installer": installer,
        "items": items,
        "conflicts": conflicts,
        "target_root": target_root,
        "ignored_paths": ignored_paths,
        "success_message": success_message,
        "maestro_guide": maestro_guide(command, answers, root),
    }


def apply(preparation, replace_conflicts, create_backups, output_function=print):
    """Apply a prepared installation using explicit conflict decisions.

    Args:
        preparation (dict): Result returned by ``prepare``.
        replace_conflicts (bool): When true, replace every reported conflict;
            when false, a conflicting preparation is rejected before writes.
        create_backups (bool): When true, copy every conflicting path to an
            adjacent timestamped backup before replacement; when false, no
            backups are written. This has no effect without conflicts.
        output_function (callable): Receives backup and completion messages.
            Defaults to ``print``.

    Returns:
        None: Every prepared item and selected ignore rule is applied.

    Raises:
        TypeError: If either conflict decision is not a boolean.
        ValueError: If replacement is declined for existing conflicts.
        OSError: If a backup, copy, removal, or write fails.

    Examples:
        Apply a conflict-free preparation without backups:

        >>> apply(preparation, False, False)  # doctest: +SKIP
    """
    if not isinstance(replace_conflicts, bool):
        raise TypeError("replace_conflicts must be a boolean")
    if not isinstance(create_backups, bool):
        raise TypeError("create_backups must be a boolean")
    conflicts = preparation["conflicts"]
    if conflicts and not replace_conflicts:
        raise ValueError("replacement was declined for conflicting paths")
    installer = preparation["installer"]
    if create_backups:
        for conflict in conflicts:
            conflict_path = Path(conflict)
            output_function(f"Backed up {conflict_path} to {installer.copy_backup(conflict_path)}")

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
    output_function(preparation["success_message"])
    if preparation.get("maestro_guide"):
        output_function(preparation["maestro_guide"])


def handle_request(request, template_root=None, home_root=None, output_function=print):
    """Return the next question, readiness state, skip, or apply result.

    Args:
        request (object): Decoded JSON protocol request.
        template_root (Path): Template root override used by tests. Defaults to
            this adapter's repository root.
        home_root (Path): Home destination override used by tests. Defaults to
            the current user's home directory.
        output_function (callable): Receives apply status messages during a
            ``run`` operation. Defaults to ``print``.

    Returns:
        dict: Exactly one ``question``, ``ready``, or ``skipped`` response.

    Raises:
        TypeError: If the request or an answer has the wrong type.
        ValueError: If protocol fields, answers, or run state are invalid.
        RuntimeError: If platform or template validation fails.
        OSError: If preparation or application filesystem operations fail.

    Examples:
        Discover the first Codex question:

        >>> handle_request({  # doctest: +SKIP
        ...     "operation": "questions",
        ...     "package": {"name": "agent-workspace-template", "command": "setup-agents-codex"},
        ...     "answers": {},
        ...     "arguments": [],
        ... })["status"]
        'question'
    """
    command, operation, answers, _ = _validate_request(request)
    root = Path(template_root) if template_root is not None else TEMPLATE_ROOT
    _validate_available_answers(command, answers, root)
    next_question = _next_base_question(command, answers, root)
    if next_question is not None:
        if operation == "run":
            raise ValueError(f"missing answer: {next_question['question']['id']}")
        return next_question

    preparation = prepare(command, answers, root, home_root)
    if preparation["conflicts"]:
        if "replace_conflicts" not in answers:
            if operation == "run":
                raise ValueError("missing answer: replace_conflicts")
            return question(
                "replace_conflicts",
                "confirm",
                "Replace all conflicting paths?",
                default=True,
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
                "create_backups",
                "confirm",
                "Create backups of conflicting paths?",
                default=False,
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
        response = handle_request(request, output_function=lambda message: print(message, file=sys.stderr))
        json.dump(response, sys.stdout, sort_keys=True)
        sys.stdout.write("\n")
    except Exception as error:
        print(f"toolbox adapter error: {error}", file=sys.stderr)
        raise SystemExit(1) from error
