"""Generate a compact project architecture context file from the repository tree."""

from collections import Counter, defaultdict
from pathlib import Path
import os

OUTPUT_PATH = Path(".agent/context/project-map.md")
MAX_LIST_ITEMS = 40
MAX_DEPTH = 4
MAX_FILES_PER_DIRECTORY = 12
MAX_PACKAGE_MODULES = 30
IGNORE_DIRECTORIES = {
    ".git",
    ".hg",
    ".svn",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "site-packages",
    ".idea",
    ".vscode",
    "wandb",
    "runs",
    "outputs",
    "checkpoints",
    "models",
    "weights",
    "datasets",
    "data",
    "logs",
}
AGENT_INTERNAL_PARTS = {
    "scripts",
    "references",
    "assets",
    "prompts",
    "examples",
}
IGNORE_FILE_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".so",
    ".dll",
    ".dylib",
    ".zip",
    ".tar",
    ".gz",
    ".7z",
    ".rar",
    ".pt",
    ".pth",
    ".onnx",
    ".h5",
    ".hdf5",
    ".ckpt",
    ".npy",
    ".npz",
    ".parquet",
    ".feather",
    ".db",
    ".sqlite",
    ".sqlite3",
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".svg",
    ".csv",
    ".jsonl",
    ".log",
    ".xlsx",
    ".docx",
    ".pptx",
}
CONFIG_FILES = {
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "requirements.txt",
    "requirements-dev.txt",
    "environment.yml",
    "environment.yaml",
    "Pipfile",
    "poetry.lock",
    "uv.lock",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "Cargo.toml",
    "go.mod",
    "Makefile",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    ".pre-commit-config.yaml",
    "tox.ini",
    "pytest.ini",
}
ENTRYPOINT_NAMES = {
    "main.py",
    "app.py",
    "run.py",
    "train.py",
    "evaluate.py",
    "infer.py",
    "inference.py",
    "server.py",
    "cli.py",
}
SOURCE_DIRECTORY_NAMES = {
    "src",
    "app",
    "apps",
    "lib",
    "libs",
    "package",
    "packages",
}
TEST_DIRECTORY_NAMES = {"test", "tests", "testing"}
DOC_DIRECTORY_NAMES = {"doc", "docs", "documentation"}


class ProjectSummary:
    """Container for project architecture facts collected from the filesystem."""

    def __init__(self) -> None:
        """Initialize an empty project summary.

        Args:
            None.

        Returns:
            None.

        Raises:
            None.
        """
        self.top_level_directories: list[Path] = []
        self.top_level_files: list[Path] = []
        self.config_files: list[Path] = []
        self.source_roots: list[Path] = []
        self.test_roots: list[Path] = []
        self.doc_roots: list[Path] = []
        self.entrypoints: list[Path] = []
        self.python_packages: list[Path] = []
        self.notable_files_by_directory: dict[Path, list[Path]] = defaultdict(list)
        self.extension_counts: Counter[str] = Counter()
        self.ignored_directory_count = 0
        self.ignored_file_count = 0
        self.agent_internal_count = 0


def find_repository_root(start: Path) -> Path:
    """Find the most likely repository root.

    Args:
        start: Directory used as the search starting point.

    Returns:
        The first ancestor containing `.agent`, `.git`, or a known project
        configuration file. If no marker is found, returns `start`.

    Raises:
        None.
    """
    current = start.resolve()

    for candidate in [current, *current.parents]:
        if (candidate / ".agent").is_dir() or (candidate / ".git").is_dir():
            return candidate

        if any((candidate / file_name).exists() for file_name in CONFIG_FILES):
            return candidate

    return current


def should_ignore_directory(path: Path) -> bool:
    """Return whether a directory should be excluded from architecture scanning.

    Args:
        path: Directory path to check.

    Returns:
        True when the directory is generated, external, bulky, or low-signal.

    Raises:
        None.
    """
    return path.name in IGNORE_DIRECTORIES


def is_agent_internal_path(path: Path) -> bool:
    """Return whether a path is internal agent implementation detail.

    Args:
        path: Repository-relative path.

    Returns:
        True when the path points to `.agent` internals that should not appear
        as normal project architecture context.

    Raises:
        None.
    """
    parts = path.parts
    if not parts or parts[0] != ".agent":
        return False

    return any(part in AGENT_INTERNAL_PARTS for part in parts[1:])


def should_ignore_file(path: Path) -> bool:
    """Return whether a file should be excluded from architecture scanning.

    Args:
        path: File path to check.

    Returns:
        True when the file is generated, binary, compressed, or likely bulky.

    Raises:
        None.
    """
    return path.suffix.lower() in IGNORE_FILE_SUFFIXES


def relative_to_root(path: Path, root: Path) -> Path:
    """Convert a path to a repository-relative path.

    Args:
        path: Absolute or relative path to convert.
        root: Repository root used as the reference point.

    Returns:
        A path relative to `root`.

    Raises:
        ValueError: If `path` cannot be represented relative to `root`.
    """
    return path.resolve().relative_to(root.resolve())


def safe_iterdir(path: Path) -> list[Path]:
    """List directory entries without raising on inaccessible directories.

    Args:
        path: Directory to inspect.

    Returns:
        Sorted directory entries. Returns an empty list when the directory cannot
        be read.

    Raises:
        None.
    """
    try:
        return sorted(path.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower()))
    except OSError:
        return []


def collect_project_summary(root: Path) -> ProjectSummary:
    """Collect compact architecture facts from a repository tree.

    Args:
        root: Repository root to scan.

    Returns:
        A populated project summary.

    Raises:
        None.
    """
    summary = ProjectSummary()

    for item in safe_iterdir(root):
        if item.is_dir():
            if should_ignore_directory(item):
                summary.ignored_directory_count += 1
                continue
            summary.top_level_directories.append(relative_to_root(item, root))
        elif item.is_file():
            if should_ignore_file(item):
                summary.ignored_file_count += 1
                continue
            summary.top_level_files.append(relative_to_root(item, root))

    for current_root, directories, files in os.walk(root):
        current_path = Path(current_root)
        relative_current = relative_to_root(current_path, root)
        depth = 0 if str(relative_current) == "." else len(relative_current.parts)

        kept_directories = []
        for directory_name in sorted(directories):
            directory_path = current_path / directory_name
            relative_directory = relative_to_root(directory_path, root)
            if should_ignore_directory(directory_path):
                summary.ignored_directory_count += 1
                continue
            if is_agent_internal_path(relative_directory):
                summary.agent_internal_count += 1
                continue
            kept_directories.append(directory_name)
        directories[:] = kept_directories

        if depth > MAX_DEPTH:
            directories[:] = []
            continue

        sorted_files = sorted(files, key=str.lower)
        visible_files = []

        for file_name in sorted_files:
            file_path = current_path / file_name
            relative_file = relative_to_root(file_path, root)
            if should_ignore_file(file_path):
                summary.ignored_file_count += 1
                continue
            if is_agent_internal_path(relative_file):
                summary.agent_internal_count += 1
                continue

            visible_files.append(relative_file)
            suffix = file_path.suffix.lower() or "[no extension]"
            summary.extension_counts[suffix] += 1

            if file_name in CONFIG_FILES:
                summary.config_files.append(relative_file)

            if file_name in ENTRYPOINT_NAMES:
                summary.entrypoints.append(relative_file)

            if file_name == "__init__.py":
                summary.python_packages.append(relative_current)

        if visible_files:
            summary.notable_files_by_directory[relative_current].extend(visible_files[:MAX_FILES_PER_DIRECTORY])

        for directory_name in directories:
            directory_path = current_path / directory_name
            relative_directory = relative_to_root(directory_path, root)
            normalized_name = directory_name.lower()

            if normalized_name in SOURCE_DIRECTORY_NAMES:
                summary.source_roots.append(relative_directory)
            elif normalized_name in TEST_DIRECTORY_NAMES:
                summary.test_roots.append(relative_directory)
            elif normalized_name in DOC_DIRECTORY_NAMES:
                summary.doc_roots.append(relative_directory)

    summary.config_files = sorted(set(summary.config_files))
    summary.source_roots = sorted(set(summary.source_roots))
    summary.test_roots = sorted(set(summary.test_roots))
    summary.doc_roots = sorted(set(summary.doc_roots))
    summary.entrypoints = sorted(set(summary.entrypoints))
    summary.python_packages = sorted(set(summary.python_packages))[:MAX_PACKAGE_MODULES]

    return summary


def format_path_list(paths: list[Path], empty_text: str = "None detected.") -> list[str]:
    """Format paths as Markdown bullet lines.

    Args:
        paths: Paths to render.
        empty_text: Text to return when no paths are available.

    Returns:
        Markdown lines.

    Raises:
        None.
    """
    if not paths:
        return [empty_text]

    return [f"- `{path.as_posix()}`" for path in paths[:MAX_LIST_ITEMS]]


def format_directory_summary(summary: ProjectSummary) -> list[str]:
    """Format top-level directory and file information.

    Args:
        summary: Project summary to render.

    Returns:
        Markdown lines describing the top-level layout.

    Raises:
        None.
    """
    lines = ["## Top-level layout", ""]
    lines.extend(format_path_list(summary.top_level_directories))

    if summary.top_level_files:
        lines.extend(["", "Top-level files:", ""])
        lines.extend(format_path_list(summary.top_level_files))

    return lines


def format_notable_directories(summary: ProjectSummary) -> list[str]:
    """Format compact per-directory notable files.

    Args:
        summary: Project summary to render.

    Returns:
        Markdown lines with bounded file examples by directory.

    Raises:
        None.
    """
    lines = ["## Notable files by directory", ""]
    directories = sorted(summary.notable_files_by_directory.keys())[:MAX_LIST_ITEMS]

    if not directories:
        return [*lines, "None detected."]

    for directory in directories:
        display_directory = "." if str(directory) == "." else directory.as_posix()
        files = summary.notable_files_by_directory[directory]
        rendered_files = ", ".join(f"`{path.name}`" for path in files[:MAX_FILES_PER_DIRECTORY])
        lines.append(f"- `{display_directory}/`: {rendered_files}")

    return lines


def format_extension_summary(summary: ProjectSummary) -> list[str]:
    """Format dominant file extensions.

    Args:
        summary: Project summary to render.

    Returns:
        Markdown lines with extension counts.

    Raises:
        None.
    """
    lines = ["## File-type signal", ""]

    if not summary.extension_counts:
        return [*lines, "None detected."]

    for extension, count in summary.extension_counts.most_common(12):
        lines.append(f"- `{extension}`: {count}")

    return lines


def render_project_map(root: Path, summary: ProjectSummary) -> str:
    """Render a project map Markdown document.

    Args:
        root: Repository root that was scanned.
        summary: Project summary to render.

    Returns:
        Markdown content for `.agent/context/project-map.md`.

    Raises:
        None.
    """
    lines = [
        "# Project Map",
        "",
        "This file is a compact architecture index generated from the repository tree.",
        "It is designed for routing and file-placement decisions, not full documentation.",
        "Agent internals such as scripts, references, assets, and prompt folders are intentionally hidden from normal architecture context.",
        "",
        "## Refresh command",
        "",
        "Run from the repository root:",
        "",
        "```bash",
        "python3 .agent/scripts/update_project_map.py",
        "```",
        "",
        "## Scanned root",
        "",
        f"- `{root.name}`",
        "",
    ]

    lines.extend(format_directory_summary(summary))
    lines.extend(["", "## Source roots", ""])
    lines.extend(format_path_list(summary.source_roots))
    lines.extend(["", "## Test roots", ""])
    lines.extend(format_path_list(summary.test_roots))
    lines.extend(["", "## Documentation roots", ""])
    lines.extend(format_path_list(summary.doc_roots))
    lines.extend(["", "## Configuration and dependency files", ""])
    lines.extend(format_path_list(summary.config_files))
    lines.extend(["", "## Entrypoints and executable scripts", ""])
    lines.extend(format_path_list(summary.entrypoints))
    lines.extend(["", "## Python packages", ""])
    lines.extend(format_path_list(summary.python_packages))
    lines.extend([""])
    lines.extend(format_notable_directories(summary))
    lines.extend([""])
    lines.extend(format_extension_summary(summary))
    lines.extend(
        [
            "",
            "## Excluded low-signal paths",
            "",
            f"- Ignored directories: {summary.ignored_directory_count}",
            f"- Ignored files: {summary.ignored_file_count}",
            f"- Hidden agent internals: {summary.agent_internal_count}",
            "",
            "## Maintenance rule",
            "",
            "Update this file with `python3 .agent/scripts/update_project_map.py` after significant directory, package, or entrypoint changes.",
            "If this file conflicts with actual source files, trust the source files.",
        ]
    )

    return "\n".join(lines).strip() + "\n"


def write_project_map(root: Path, output_path: Path) -> Path:
    """Scan a repository and write the project map file.

    Args:
        root: Repository root to scan.
        output_path: Repository-relative output path for the Markdown file.

    Returns:
        The absolute path written.

    Raises:
        OSError: If the output directory or file cannot be written.
    """
    summary = collect_project_summary(root)
    output_absolute = root / output_path
    output_absolute.parent.mkdir(parents=True, exist_ok=True)
    output_absolute.write_text(render_project_map(root, summary), encoding="utf-8")
    return output_absolute


def main() -> int:
    """Update the project architecture context file.

    Args:
        None.

    Returns:
        Zero when the project map is written successfully.

    Raises:
        None.
    """
    root = find_repository_root(Path.cwd())
    output_path = write_project_map(root, OUTPUT_PATH)
    relative_output = relative_to_root(output_path, root)
    print(f"Updated {relative_output.as_posix()}")
    return 0


raise SystemExit(main())
