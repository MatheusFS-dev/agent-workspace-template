#!/usr/bin/env python3
"""Extract relevant sections from reference files without loading them fully."""

from pathlib import Path
import re
import sys

# If you want, change 1200 characters to 600 or 800. This directly reduces worst-case coding-task overhead from about 3160 search-output tokens to roughly 1660 to 2160 tokens.
DEFAULT_CONTEXT_CHARS = 1200
MAX_RESULTS = 5


def normalize(text: str) -> str:
    """Normalize text for case-insensitive matching.

    Args:
        text: Raw text to normalize.

    Returns:
        Lowercase text with repeated whitespace collapsed.

    Raises:
        None.
    """
    normalized = re.sub(r"[^a-z0-9]+", " ", text.lower())
    return re.sub(r"\s+", " ", normalized).strip()


def split_sections(text: str) -> list[tuple[str, str]]:
    """Split Markdown-like text into sections.

    Args:
        text: Reference file content.

    Returns:
        Tuples of section title and section body.

    Raises:
        None.
    """
    sections = []
    current_title = "Document start"
    current_lines = []

    for line in text.splitlines():
        if line.startswith("#"):
            if current_lines:
                sections.append((current_title, "\n".join(current_lines).strip()))
            current_title = line.strip()
            current_lines = []
            continue
        current_lines.append(line)

    if current_lines:
        sections.append((current_title, "\n".join(current_lines).strip()))

    return [(title, body) for title, body in sections if body]


def score_section(title: str, body: str, keywords: list[str]) -> int:
    """Score a section by keyword matches.

    Args:
        title: Section title.
        body: Section body.
        keywords: Search keywords or phrases.

    Returns:
        Integer relevance score. Higher is more relevant.

    Raises:
        None.
    """
    title_text = normalize(title)
    body_text = normalize(body)
    score = 0

    for keyword in keywords:
        normalized_keyword = normalize(keyword)
        if not normalized_keyword:
            continue
        score += 4 * title_text.count(normalized_keyword)
        score += body_text.count(normalized_keyword)

    return score


def trim_body(body: str, keywords: list[str], max_chars: int) -> str:
    """Trim a body around the first keyword hit.

    Args:
        body: Section body.
        keywords: Keywords used to find the most relevant excerpt.
        max_chars: Maximum number of characters to return.

    Returns:
        Trimmed body excerpt.

    Raises:
        None.
    """
    if len(body) <= max_chars:
        return body.strip()

    normalized_body = body.lower()
    hit_positions = [
        normalized_body.find(keyword.lower()) for keyword in keywords
        if keyword and normalized_body.find(keyword.lower()) >= 0
    ]
    center = min(hit_positions) if hit_positions else 0
    start = max(0, center - max_chars // 3)
    end = min(len(body), start + max_chars)
    excerpt = body[start:end].strip()

    if start > 0:
        excerpt = "..." + excerpt
    if end < len(body):
        excerpt = excerpt + "..."

    return excerpt


def search_reference(path: Path, keywords: list[str]) -> list[tuple[int, str, str]]:
    """Search a reference file and return top matching sections.

    Args:
        path: Reference file to search.
        keywords: Keywords or phrases to match.

    Returns:
        Tuples of score, title, and excerpt.

    Raises:
        OSError: If the file cannot be read.
    """
    text = path.read_text(encoding="utf-8")
    sections = split_sections(text)
    scored_sections = []

    for title, body in sections:
        score = score_section(title, body, keywords)
        if score > 0:
            excerpt = trim_body(body, keywords, DEFAULT_CONTEXT_CHARS)
            scored_sections.append((score, title, excerpt))

    return sorted(scored_sections, key=lambda item: item[0], reverse=True)[:MAX_RESULTS]


def main() -> int:
    """Execute reference search from positional arguments.

    Args:
        None.

    Returns:
        Zero when matches are found, one when no match is found, and two for
        invalid usage.

    Raises:
        None.
    """
    if len(sys.argv) < 3:
        print("Usage: python3 search_reference.py <file> <keywords...>")
        return 2

    path = Path(sys.argv[1])
    keywords = sys.argv[2:]

    if not path.exists():
        print(f"Reference file not found: {path}")
        return 2

    try:
        matches = search_reference(path, keywords)
    except OSError as error:
        print(f"Could not read {path}: {error}")
        return 2

    if not matches:
        print("No matching sections found.")
        return 1

    for index, (score, title, excerpt) in enumerate(matches, start=1):
        print(f"## Match {index}, score {score}: {title}")
        print(excerpt)
        print()

    return 0


raise SystemExit(main())
