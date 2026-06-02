"""Lint the compact durable agent memory file."""

from pathlib import Path
import re
import sys


DEFAULT_MEMORY_PATH = Path(".agent/context/memories.md")
TARGET_TOKEN_LIMIT = 1200
WARNING_TOKEN_LIMIT = 1500
REPEATED_RULE_PATTERNS = [
    re.compile(r"do not use argparse", re.IGNORECASE),
    re.compile(r"future__ import annotations", re.IGNORECASE),
    re.compile(r"google-style docstrings", re.IGNORECASE),
    re.compile(r"read .*index.yaml", re.IGNORECASE),
]


def approximate_tokens(text: str) -> int:
    """Estimate token count from character count.

    Args:
        text: Text to estimate.

    Returns:
        Approximate token count using four characters per token.

    Raises:
        None.
    """
    return max(1, len(text) // 4)


def extract_bullets(text: str) -> list[str]:
    """Extract normalized bullet entries.

    Args:
        text: Markdown text to inspect.

    Returns:
        Normalized bullet lines.

    Raises:
        None.
    """
    bullets = []

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        normalized = re.sub(r"\s+", " ", stripped[2:].lower()).strip()
        bullets.append(normalized)

    return bullets


def find_duplicate_bullets(bullets: list[str]) -> list[str]:
    """Find duplicate memory bullets.

    Args:
        bullets: Normalized bullet entries.

    Returns:
        Duplicate bullet texts.

    Raises:
        None.
    """
    seen = set()
    duplicates = []

    for bullet in bullets:
        if bullet in seen and bullet not in duplicates:
            duplicates.append(bullet)
        seen.add(bullet)

    return duplicates


def find_repeated_rules(text: str) -> list[str]:
    """Find memories that appear to duplicate global rules.

    Args:
        text: Memory file text.

    Returns:
        Descriptions of repeated rule patterns.

    Raises:
        None.
    """
    matches = []

    for pattern in REPEATED_RULE_PATTERNS:
        if pattern.search(text):
            matches.append(pattern.pattern)

    return matches


def lint_memory(path: Path) -> list[str]:
    """Lint a memory file.

    Args:
        path: Memory file path.

    Returns:
        Warning or error messages.

    Raises:
        OSError: If the file cannot be read.
    """
    text = path.read_text(encoding="utf-8")
    messages = []
    token_count = approximate_tokens(text)

    if token_count > WARNING_TOKEN_LIMIT:
        messages.append(
            f"memory exceeds warning budget: approx {token_count} tokens, target {TARGET_TOKEN_LIMIT}"
        )

    duplicates = find_duplicate_bullets(extract_bullets(text))
    for duplicate in duplicates:
        messages.append(f"duplicate bullet: {duplicate[:120]}")

    for repeated_rule in find_repeated_rules(text):
        messages.append(f"memory appears to duplicate global rule pattern: {repeated_rule}")

    return messages


def main() -> int:
    """Execute memory linting.

    Args:
        None.

    Returns:
        Zero when lint passes, otherwise one.

    Raises:
        None.
    """
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_MEMORY_PATH

    if not path.exists():
        print(f"memory_lint: file not found: {path}")
        return 1

    try:
        messages = lint_memory(path)
    except OSError as error:
        print(f"memory_lint: read error: {error}")
        return 1

    if messages:
        print("memory_lint: warnings")
        print("\n".join(messages))
        return 1

    print("memory_lint: passed")
    return 0


raise SystemExit(main())
