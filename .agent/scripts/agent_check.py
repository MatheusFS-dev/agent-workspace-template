#!/usr/bin/env python3
"""Deterministic checks for agent-generated Python changes."""

import ast
from pathlib import Path
import re
import sys

DEFAULT_ROOTS = [Path("src"), Path("tests")]
DEFAULT_SELF_CHECK_FILES = [
    Path(".agent/scripts/agent_check.py"),
    Path(".agent/scripts/route_context.py"),
    Path(".agent/scripts/search_reference.py"),
    Path(".agent/scripts/memory_lint.py"),
    Path(".agent/scripts/update_project_map.py"),
]
FORBIDDEN_PATTERNS = {
    "argparse import": re.compile(r"^\s*(import argparse|from argparse import)"),
    "future annotations": re.compile(r"^\s*from __future__ import annotations"),
    "aligned assignment": re.compile(r"^\s*[A-Za-z_][A-Za-z0-9_]*\s{2,}="),
}
IGNORED_DIR_NAMES = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "build",
    "dist",
    "site-packages",
    "venv",
    ".venv",
}


def resolve_scan_paths(arguments: list[str]) -> list[Path]:
    """Resolve scan paths from command-line arguments or defaults.

    Args:
        arguments: Raw positional arguments supplied after the script name.

    Returns:
        Existing paths to scan. Defaults to `src`, `tests`, and the agent
        scripts when no explicit path is supplied.

    Raises:
        None.
    """
    if arguments:
        return [Path(argument) for argument in arguments]

    paths = [path for path in DEFAULT_ROOTS if path.exists()]
    paths.extend(path for path in DEFAULT_SELF_CHECK_FILES if path.exists())
    return paths


def should_skip(path: Path) -> bool:
    """Return whether a path belongs to an ignored directory.

    Args:
        path: File or directory path to evaluate.

    Returns:
        True when any path component is an ignored directory name.

    Raises:
        None.
    """
    return any(part in IGNORED_DIR_NAMES for part in path.parts)


def iter_python_files(paths: list[Path]) -> list[Path]:
    """Collect Python files from paths.

    Args:
        paths: Files or directories to scan.

    Returns:
        Sorted Python file paths that exist and are not ignored.

    Raises:
        None.
    """
    files = []

    for path in paths:
        if not path.exists() or should_skip(path):
            continue

        if path.is_file() and path.suffix == ".py":
            files.append(path)
            continue

        if path.is_dir():
            files.extend(
                child for child in path.rglob("*.py")
                if child.is_file() and not should_skip(child)
            )

    return sorted(set(files))


def find_regex_violations(path: Path) -> list[str]:
    """Find line-based coding-rule violations.

    Args:
        path: Python file to inspect.

    Returns:
        Violation messages containing file, line number, and rule name.

    Raises:
        OSError: If the file cannot be read.
    """
    violations = []
    lines = path.read_text(encoding="utf-8").splitlines()

    for line_number, line in enumerate(lines, start=1):
        for rule_name, pattern in FORBIDDEN_PATTERNS.items():
            if pattern.search(line):
                violations.append(f"{path}:{line_number}: {rule_name}")

    return violations


def has_docstring(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """Return whether a function node has a docstring.

    Args:
        node: Function or async function AST node.

    Returns:
        True when the node has a Python docstring.

    Raises:
        None.
    """
    return ast.get_docstring(node, clean=False) is not None


def is_overload_stub(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """Return whether a function is an overload or trivial stub.

    Args:
        node: Function or async function AST node.

    Returns:
        True when the function should not require a docstring.

    Raises:
        None.
    """
    decorator_names = {
        getattr(decorator, "id", "") for decorator in node.decorator_list
        if isinstance(decorator, ast.Name)
    }
    decorator_attrs = {
        getattr(decorator, "attr", "") for decorator in node.decorator_list
        if isinstance(decorator, ast.Attribute)
    }

    if "overload" in decorator_names or "overload" in decorator_attrs:
        return True

    if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
        return True

    if len(node.body) == 1 and isinstance(node.body[0], ast.Expr):
        value = node.body[0].value
        if isinstance(value, ast.Constant) and value.value is Ellipsis:
            return True

    return False


def find_missing_docstrings(path: Path) -> list[str]:
    """Find public functions and methods without docstrings.

    Args:
        path: Python file to parse and inspect.

    Returns:
        Violation messages for public functions and methods missing docstrings.

    Raises:
        OSError: If the file cannot be read.
        SyntaxError: If the file cannot be parsed.
    """
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=str(path))
    violations = []

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        if node.name.startswith("_") or is_overload_stub(node):
            continue

        if not has_docstring(node):
            violations.append(f"{path}:{node.lineno}: missing docstring: {node.name}")

    return violations


def run_checks(paths: list[Path]) -> list[str]:
    """Run all deterministic checks against Python files.

    Args:
        paths: Files or directories to inspect.

    Returns:
        Violation messages. Empty means all checks passed.

    Raises:
        None.
    """
    violations = []

    for path in iter_python_files(paths):
        try:
            violations.extend(find_regex_violations(path))
            violations.extend(find_missing_docstrings(path))
        except SyntaxError as error:
            violations.append(f"{path}:{error.lineno}: syntax error: {error.msg}")
        except OSError as error:
            violations.append(f"{path}: read error: {error}")

    return violations


def main() -> int:
    """Execute the agent check script.

    Args:
        None.

    Returns:
        Zero when checks pass, otherwise one.

    Raises:
        None.
    """
    paths = resolve_scan_paths(sys.argv[1:])
    violations = run_checks(paths)

    if violations:
        print("agent_check: failed")
        print("\n".join(violations))
        return 1

    print("agent_check: passed")
    return 0


raise SystemExit(main())
