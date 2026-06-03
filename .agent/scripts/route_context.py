"""Route an agent task to the smallest required context files."""

from pathlib import Path
import re
import sys

EASY_TASK_PATTERN = re.compile(
    r"\b("
    r"easy mode|trivial|simple edit|simple question|"
    r"one[- ]line|one line|change one line|change this line|"
    r"typo|fix typo|markdown equation|render equation|"
    r"replace phrase|replace this phrase"
    r")\b",
    re.IGNORECASE,
)
NON_EASY_PATTERN = re.compile(
    r"\b("
    r"debug|debugging|refactor|architecture|file placement|module ownership|"
    r"pipeline|experiment|dataset|training|inference|performance|"
    r"cuda|tensorflow|pytorch|torch|driver|dependency|package conflict|"
    r"environment|venv|pip|conda|test suite|multi[- ]file|repository-wide|"
    r"reviewer|rebuttal|plot|figure|visuali[sz]ation"
    r")\b",
    re.IGNORECASE,
)
EASY_ESCALATION_QUESTION = (
    "This may require normal routing. Should I continue in easy mode, " "or load the normal context?"
)
ROUTES = [
    (
        "troubleshooting",
        re.compile(
            r"\b(driver|cuda|tensorflow|pytorch|torch|package conflict|dependency|linux|windows|kernel|nvidia|gpu|venv|pip|conda|import error)\b",
            re.IGNORECASE,
        ),
        [".agent/workflows/debugging.md"],
    ),
    (
        "plotting",
        re.compile(
            r"\b(plot|figure|visuali[sz]ation|matplotlib|chart|graph|histogram|scatter|boxplot|error\s*bar|publication figure)\b",
            re.IGNORECASE,
        ),
        [".agent/rules/plotting-style.md", ".agent/skills/scientific-plot-maker/SKILL.md"],
    ),
    (
        "paper_writing",
        re.compile(
            r"\b(manuscript|paper section|paper writing|scientific writing|reviewer|rebuttal|abstract|introduction|related work|conclusion|discussion|latex|ieee|journal|conference)\b",
            re.IGNORECASE,
        ),
        [".agent/modes/paper-writing.md", ".agent/skills/scribe/SKILL.md"],
    ),
    (
        "coding",
        re.compile(
            r"\b(implement|code|refactor|script|test|debug|function|class|module|repository|pipeline|experiment|dataset|training|inference|fix|bug)\b",
            re.IGNORECASE,
        ),
        [".agent/modes/coding.md"],
    ),
    (
        "long_task_state",
        re.compile(r"\b(session state|task state|resume state|long task state)\b", re.IGNORECASE),
        [".agent/workflows/long-task-state.md"],
    ),
]
PROJECT_MAP_PATTERN = re.compile(
    r"\b(architecture|file placement|where should|module ownership|repository structure|package layout|folder structure)\b",
    re.IGNORECASE,
)
PROJECT_MAP_COMMAND_PATTERN = re.compile(
    r"\b(populate|refresh|repair|regenerate|update|audit|fill)\b.*\b(project architecture|project map|architecture context|project architecture context)\b|\b(project architecture|project map|architecture context|project architecture context)\b.*\b(populate|refresh|repair|regenerate|update|audit|fill)\b",
    re.IGNORECASE,
)
MEMORY_PATTERN = re.compile(
    r"\b(remember|forget|memory|memories|previous decision|durable context)\b",
    re.IGNORECASE,
)
DEFAULT_FILES = ["AGENTS.md"]
EASY_TASK_FILES = ["AGENTS.md", ".agent/modes/easy-task.md"]


def read_request(arguments: list[str]) -> str:
    """Read the user request from arguments or standard input.

    Args:
        arguments: Raw positional arguments supplied after the script name.

    Returns:
        The request text used for routing.

    Raises:
        None.
    """
    if arguments:
        return " ".join(arguments)

    if not sys.stdin.isatty():
        return sys.stdin.read()

    return ""


def unique_preserve_order(items: list[str]) -> list[str]:
    """Remove duplicate strings while preserving order.

    Args:
        items: Values to deduplicate.

    Returns:
        Deduplicated values in first-seen order.

    Raises:
        None.
    """
    seen = set()
    result = []

    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)

    return result


def wants_easy_task_mode(request: str) -> bool:
    """Check whether the request asks for or clearly matches Easy Task Mode.

    Args:
        request: User task text.

    Returns:
        True when the request contains a conservative easy-task signal.

    Raises:
        None.
    """
    return EASY_TASK_PATTERN.search(request) is not None


def has_non_easy_signal(request: str) -> bool:
    """Check whether the request contains a signal that forbids Easy Task Mode.

    Args:
        request: User task text.

    Returns:
        True when the request likely needs normal routing or extra context.

    Raises:
        None.
    """
    return NON_EASY_PATTERN.search(request) is not None


def should_use_easy_task_mode(request: str) -> bool:
    """Decide whether Easy Task Mode is safe for the request.

    Args:
        request: User task text.

    Returns:
        True only when an easy-task signal exists and no non-easy signal exists.

    Raises:
        None.
    """
    return wants_easy_task_mode(request) and not has_non_easy_signal(request)


def should_ask_before_escalating(request: str) -> bool:
    """Decide whether the router should ask before loading normal context.

    Args:
        request: User task text.

    Returns:
        True when the user requested easy handling but the request is not certainly easy.

    Raises:
        None.
    """
    return wants_easy_task_mode(request) and has_non_easy_signal(request)


def route_files(request: str) -> list[str]:
    """Select context files for a request.

    Args:
        request: User task text.

    Returns:
        Ordered context file paths to read.

    Raises:
        None.
    """
    if should_use_easy_task_mode(request):
        return list(EASY_TASK_FILES)

    if should_ask_before_escalating(request):
        return list(DEFAULT_FILES)

    files = list(DEFAULT_FILES)
    matched_route = False

    for name, pattern, route_files_to_add in ROUTES:
        if pattern.search(request):
            matched_route = True
            files.extend(route_files_to_add)

    project_map_needed = PROJECT_MAP_PATTERN.search(request) is not None
    memory_needed = MEMORY_PATTERN.search(request) is not None

    if project_map_needed:
        files.append(".agent/context/project-map.md")

    if memory_needed:
        files.append(".agent/context/memories.md")

    if not matched_route and not project_map_needed and not memory_needed:
        files.append(".agent/index.yaml")

    return unique_preserve_order(files)


def route_commands(request: str) -> list[str]:
    """Select deterministic commands that should be run for a request.

    Args:
        request: User task text.

    Returns:
        Ordered shell commands relevant to the request.

    Raises:
        None.
    """
    commands = []

    if should_ask_before_escalating(request):
        return commands

    if PROJECT_MAP_COMMAND_PATTERN.search(request):
        commands.append("python .agent/scripts/update_project_map.py")

    return unique_preserve_order(commands)


def route_questions(request: str) -> list[str]:
    """Select questions to ask before reading more context.

    Args:
        request: User task text.

    Returns:
        Ordered questions the agent should ask before escalating context.

    Raises:
        None.
    """
    if should_ask_before_escalating(request):
        return [EASY_ESCALATION_QUESTION]

    return []


def main() -> int:
    """Print the selected context files.

    Args:
        None.

    Returns:
        Zero after printing routing output.

    Raises:
        None.
    """
    request = read_request(sys.argv[1:])
    files = route_files(request)
    commands = route_commands(request)
    questions = route_questions(request)

    for question in questions:
        print(f"ASK {question}")

    for command in commands:
        print(f"RUN {command}")

    for file_path in files:
        status = "READ" if Path(file_path).exists() else "MISSING"
        print(f"{status} {file_path}")

    return 0


raise SystemExit(main())
