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
    "This may require normal routing. Should I continue in easy mode, or load the normal context?"
)
TROUBLESHOOTING_PATTERN = re.compile(
    r"\b(driver|cuda|tensorflow|pytorch|torch|package conflict|dependency|linux|windows|kernel|nvidia|gpu|venv|pip|conda|import error|crash|installation failure)\b",
    re.IGNORECASE,
)
CODE_EDIT_PATTERN = re.compile(
    r"\b("
    r"implement|edit|patch|modify|change|refactor|"
    r"write code|add code|fix code|update file|create script|"
    r"add test|unit test|write a script|make a script|"
    r"create file|update script|modify code"
    r")\b",
    re.IGNORECASE,
)
CODING_TOPIC_PATTERN = re.compile(
    r"\b("
    r"code|function|class|module|script|test|bug|fix|"
    r"repository|pipeline|experiment|dataset|training|inference"
    r")\b",
    re.IGNORECASE,
)
ROUTES = [
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
        CODING_TOPIC_PATTERN,
        [".agent/modes/coding.md"],
    ),
    (
        "long_task_state",
        re.compile(r"\b(session state|task state|resume state|long task state)\b", re.IGNORECASE),
        [".agent/workflows/long-task-state.md"],
    ),
]
CODING_EXAMPLE_ROUTES = [
    (
        "hidden assumptions",
        re.compile(r"\b(export|save|load|generate|support|integrate|add feature|new feature)\b", re.IGNORECASE),
    ),
    (
        "multiple interpretations",
        re.compile(r"\b(faster|better|cleaner|robust|scalable|secure|optimi[sz]e|improve performance)\b", re.IGNORECASE),
    ),
    (
        "over abstraction",
        re.compile(r"\b(simple|small|just|only|basic|minimal|straightforward)\b", re.IGNORECASE),
    ),
    (
        "drive by refactoring",
        re.compile(r"\b(fix|bug|crash|error|broken|validator|edge case)\b", re.IGNORECASE),
    ),
    (
        "style drift",
        re.compile(r"\b(add logging|log|small change|local patch|patch|guard|message)\b", re.IGNORECASE),
    ),
    (
        "vague vs verifiable",
        re.compile(r"\b(fix the .*system|fix .*pipeline|fix .*module|make .*work|not working)\b", re.IGNORECASE),
    ),
    (
        "multi step verification",
        re.compile(r"\b(rate limiting|middleware|multi[- ]file|feature|workflow|pipeline)\b", re.IGNORECASE),
    ),
    (
        "test first verification",
        re.compile(r"\b(breaks|fails|failure|regression|duplicate|nondeterministic|reproduce|reported)\b", re.IGNORECASE),
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
FULL_EXAMPLE_PATTERN = re.compile(
    r"\b(full example|full examples|show examples|detailed example|example code|wrong and right)\b",
    re.IGNORECASE,
)
REPOSITORY_ANALYSIS_PATTERN = re.compile(
    r"\b("
    r"analy[sz]e this repo|analy[sz]e this repository|"
    r"audit this repo|audit this repository|"
    r"repo overview|repository overview|"
    r"understand this repo|understand this repository|"
    r"context usage|token usage|context cost|token cost"
    r")\b",
    re.IGNORECASE,
)
DEFAULT_FILES = ["AGENTS.md"]
EASY_TASK_FILES = ["AGENTS.md", ".agent/modes/easy-task.md"]
CONTEXT_TOKEN_DIVISOR = 4
MAX_CODING_EXAMPLE_SEARCHES = 2
CODING_EXAMPLE_PRIORITY = [
    "vague vs verifiable",
    "hidden assumptions",
    "test first verification",
    "drive by refactoring",
    "multiple interpretations",
    "multi step verification",
    "style drift",
    "over abstraction",
]
SEARCH_REFERENCE_MAX_RESULTS = 5
SEARCH_REFERENCE_CONTEXT_CHARS = 1200
SEARCH_REFERENCE_OVERHEAD_TOKENS = 80
CODING_FULL_EXAMPLE_FILES = {
    "hidden assumptions": ".agent/modes/examples/hidden-assumptions.md",
    "multiple interpretations": ".agent/modes/examples/multiple-interpretations.md",
    "over abstraction": ".agent/modes/examples/over-abstraction.md",
    "drive by refactoring": ".agent/modes/examples/drive-by-refactoring.md",
    "style drift": ".agent/modes/examples/style-drift.md",
    "vague vs verifiable": ".agent/modes/examples/vague-vs-verifiable.md",
    "multi step verification": ".agent/modes/examples/multi-step-verification.md",
    "test first verification": ".agent/modes/examples/test-first-verification.md",
}


def read_request(arguments: list[str]) -> tuple[str, bool]:
    """Read the user request from arguments or standard input.

    Args:
        arguments: Raw positional arguments supplied after the script name.

    Returns:
        A tuple containing the request text and whether statistics should be
        printed with route output.

    Raises:
        None.
    """
    show_stats = False
    filtered_arguments = []

    for argument in arguments:
        if argument in {"--stats", "--show-stats"}:
            show_stats = True
            continue
        filtered_arguments.append(argument)

    if filtered_arguments:
        return " ".join(filtered_arguments), show_stats

    if not sys.stdin.isatty():
        return sys.stdin.read(), show_stats

    return "", show_stats


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


def approximate_tokens_for_file(file_path: str) -> int | None:
    """Estimate token cost for a file path.

    Args:
        file_path: Repository-relative file path.

    Returns:
        Approximate token count when the file exists, otherwise None.

    Raises:
        None.
    """
    path = Path(file_path)
    if not path.exists() or not path.is_file():
        return None

    try:
        return max(1, len(path.read_text(encoding="utf-8")) // CONTEXT_TOKEN_DIVISOR)
    except OSError:
        return None


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


def is_troubleshooting_request(request: str) -> bool:
    """Return whether the request primarily asks for troubleshooting.

    Args:
        request: User task text.

    Returns:
        True when troubleshooting keywords are present.

    Raises:
        None.
    """
    return TROUBLESHOOTING_PATTERN.search(request) is not None


def wants_code_edit(request: str) -> bool:
    """Return whether the request explicitly asks for code editing.

    Args:
        request: User task text.

    Returns:
        True when implementation or file-editing language is present.

    Raises:
        None.
    """
    return CODE_EDIT_PATTERN.search(request) is not None


def is_coding_request(request: str) -> bool:
    """Return whether coding context should be considered for the request.

    Args:
        request: User task text.

    Returns:
        True when the request contains editing intent or strong coding terms.
        When `True`, coding mode may still be suppressed by higher-priority
        routing such as troubleshooting or paper-writing exclusivity. When
        `False`, broad nouns like `repository` or `training` alone do not load
        coding mode.

    Raises:
        None.
    """
    if wants_code_edit(request):
        return True

    strong_coding_terms = re.compile(
        r"\b(code|function|class|script|test|bug|fix)\b",
        re.IGNORECASE,
    )
    return strong_coding_terms.search(request) is not None


def is_paper_writing_request(request: str) -> bool:
    """Return whether the request is primarily about academic writing.

    Args:
        request: User task text.

    Returns:
        True when paper-writing keywords are present. This is used to keep
        writing requests from pulling coding mode unless editing intent is
        explicit.

    Raises:
        None.
    """
    paper_pattern = next(pattern for name, pattern, _files in ROUTES if name == "paper_writing")
    return paper_pattern.search(request) is not None


def matching_route_names(request: str) -> list[str]:
    """Return names of normal routes that match the request.

    Args:
        request: User task text.

    Returns:
        Route names whose patterns match the request.

    Raises:
        None.
    """
    names = []

    if is_troubleshooting_request(request):
        names.append("troubleshooting")

    for name, pattern, _files in ROUTES:
        if name == "coding" and not is_coding_request(request):
            continue
        if pattern.search(request):
            names.append(name)

    return unique_preserve_order(names)


def is_coding_route_active(request: str) -> bool:
    """Return whether coding context should be loaded.

    Args:
        request: User task text.

    Returns:
        True when coding mode is active after troubleshooting exclusivity is applied.

    Raises:
        None.
    """
    if is_troubleshooting_request(request) and not wants_code_edit(request):
        return False

    if is_paper_writing_request(request) and not wants_code_edit(request):
        return False

    return any(name == "coding" for name in matching_route_names(request))


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

    troubleshooting_active = is_troubleshooting_request(request)
    troubleshooting_exclusive = troubleshooting_active and not wants_code_edit(request)
    repository_analysis_needed = REPOSITORY_ANALYSIS_PATTERN.search(request) is not None

    if troubleshooting_active:
        matched_route = True
        files.append(".agent/workflows/debugging.md")

    if not troubleshooting_exclusive:
        for name, pattern, route_files_to_add in ROUTES:
            if name == "long_task_state" and not pattern.search(request):
                continue
            if name == "coding" and not is_coding_request(request):
                continue
            if name == "coding" and is_paper_writing_request(request) and not wants_code_edit(request):
                continue
            if pattern.search(request):
                matched_route = True
                files.extend(route_files_to_add)

    project_map_needed = PROJECT_MAP_PATTERN.search(request) is not None
    project_map_command_needed = PROJECT_MAP_COMMAND_PATTERN.search(request) is not None
    memory_needed = MEMORY_PATTERN.search(request) is not None

    # Refresh-style project-map requests must read the regenerated file after
    # emitting the update command; otherwise the agent would refresh context
    # without loading the updated architecture information.
    if project_map_needed or repository_analysis_needed or project_map_command_needed:
        files.append(".agent/context/project-map.md")

    if memory_needed:
        files.append(".agent/context/memories.md")

    for full_example_file in matching_full_example_files(request):
        files.append(full_example_file)

    if (
        not matched_route
        and not project_map_needed
        and not project_map_command_needed
        and not memory_needed
        and not repository_analysis_needed
    ):
        files.append(".agent/index.yaml")

    return unique_preserve_order(files)


def matching_coding_example_keywords(request: str) -> list[str]:
    """Select coding example keywords for risk-specific searches.

    Args:
        request: User task text.

    Returns:
        Ordered example-card search keywords.

    Raises:
        None.
    """
    if not is_coding_route_active(request):
        return []

    keywords = []
    for keyword, pattern in CODING_EXAMPLE_ROUTES:
        if pattern.search(request):
            keywords.append(keyword)

    return prioritize_coding_example_keywords(unique_preserve_order(keywords))


def prioritize_coding_example_keywords(keywords: list[str]) -> list[str]:
    """Prioritize and cap matched coding example keywords.

    Args:
        keywords: Matched risk keywords in discovery order.

    Returns:
        Ordered keywords capped to the configured search budget. Higher-priority
        risks are emitted first so routed search output stays bounded. Lower-
        priority unmatched values are preserved afterward until the cap is hit.

    Raises:
        None.
    """
    keyword_set = set(keywords)
    prioritized = [keyword for keyword in CODING_EXAMPLE_PRIORITY if keyword in keyword_set]
    remaining = [keyword for keyword in keywords if keyword not in CODING_EXAMPLE_PRIORITY]
    return unique_preserve_order(prioritized + remaining)[:MAX_CODING_EXAMPLE_SEARCHES]


def matching_full_example_files(request: str) -> list[str]:
    """Select full example files for a coding request.

    Args:
        request: User task text.

    Returns:
        Ordered full-example file paths for matched coding risks. Returns an
        empty list when the request does not explicitly ask for a full example.

    Raises:
        None.
    """
    if not FULL_EXAMPLE_PATTERN.search(request):
        return []

    return [
        CODING_FULL_EXAMPLE_FILES[keyword]
        for keyword in matching_coding_example_keywords(request)
        if keyword in CODING_FULL_EXAMPLE_FILES
    ]


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
        commands.append("python3 .agent/scripts/update_project_map.py")

    for keyword in matching_coding_example_keywords(request):
        commands.append(
            "python3 .agent/scripts/search_reference.py .agent/modes/coding-example-cards.md "
            f"{keyword}"
        )

    return unique_preserve_order(commands)


def approximate_tokens_for_command(command: str) -> int | None:
    """Estimate token output cost for a routed command.

    Args:
        command: Routed shell command.

    Returns:
        An approximate output token count when the command is well understood.
        Returns `None` for unknown commands so stats output can mark the value as
        unknown instead of inventing a misleading estimate.

    Raises:
        None.
    """
    if "search_reference.py" in command:
        excerpt_tokens = (
            SEARCH_REFERENCE_MAX_RESULTS
            * SEARCH_REFERENCE_CONTEXT_CHARS
            // CONTEXT_TOKEN_DIVISOR
        )
        return excerpt_tokens + SEARCH_REFERENCE_OVERHEAD_TOKENS

    if "update_project_map.py" in command:
        return 20

    return None


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


def format_file_line(file_path: str, show_stats: bool) -> str:
    """Format a route file line.

    Args:
        file_path: Repository-relative file path.
        show_stats: Whether to include approximate token cost.

    Returns:
        A route output line.

    Raises:
        None.
    """
    status = "READ" if Path(file_path).exists() else "MISSING"
    if not show_stats:
        return f"{status} {file_path}"

    token_count = approximate_tokens_for_file(file_path)
    if token_count is None:
        return f"{status} {file_path} approx_tokens=unknown"

    return f"{status} {file_path} approx_tokens={token_count}"


def print_route_output(request: str, show_stats: bool) -> None:
    """Print route questions, commands, files, and optional statistics.

    Args:
        request: User task text.
        show_stats: Whether to include approximate token cost.

    Returns:
        None.

    Raises:
        None.
    """
    files = route_files(request)
    commands = route_commands(request)
    questions = route_questions(request)

    for question in questions:
        print(f"ASK {question}")

    total_tokens = 0
    command_total_tokens = 0
    has_unknown = False

    for command in commands:
        if show_stats:
            token_count = approximate_tokens_for_command(command)
            if token_count is None:
                print(f"RUN {command} approx_output_tokens=unknown")
                has_unknown = True
            else:
                print(f"RUN {command} approx_output_tokens<={token_count}")
                command_total_tokens += token_count
        else:
            print(f"RUN {command}")

    for file_path in files:
        print(format_file_line(file_path, show_stats))
        token_count = approximate_tokens_for_file(file_path)
        if token_count is None:
            has_unknown = True
        else:
            total_tokens += token_count

    if show_stats:
        if has_unknown:
            print(f"TOTAL_FILE approx_tokens>={total_tokens}")
            print(f"TOTAL_COMMAND_OUTPUT approx_tokens>={command_total_tokens}")
            print(f"TOTAL_CONTEXT_RISK approx_tokens>={total_tokens + command_total_tokens}")
        else:
            print(f"TOTAL_FILE approx_tokens={total_tokens}")
            print(f"TOTAL_COMMAND_OUTPUT approx_tokens<={command_total_tokens}")
            print(f"TOTAL_CONTEXT_RISK approx_tokens<={total_tokens + command_total_tokens}")


def main() -> int:
    """Print the selected context files.

    Args:
        None.

    Returns:
        Zero after printing routing output.

    Raises:
        None.
    """
    request, show_stats = read_request(sys.argv[1:])
    print_route_output(request, show_stats)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
