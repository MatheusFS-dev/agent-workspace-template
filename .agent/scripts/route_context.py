"""Route an agent task to the smallest required context files."""

from pathlib import Path
import re
import sys


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


def route_files(request: str) -> list[str]:
    """Select context files for a request.

    Args:
        request: User task text.

    Returns:
        Ordered context file paths to read.

    Raises:
        None.
    """
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

    if PROJECT_MAP_COMMAND_PATTERN.search(request):
        commands.append("python .agent/scripts/update_project_map.py")

    return unique_preserve_order(commands)


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

    for command in commands:
        print(f"RUN {command}")

    for file_path in files:
        status = "READ" if Path(file_path).exists() else "MISSING"
        print(f"{status} {file_path}")

    return 0


raise SystemExit(main())
