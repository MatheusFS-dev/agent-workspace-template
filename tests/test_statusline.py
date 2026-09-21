"""Regression tests for the shared Claude and AGY statusline formatter."""

import json
from pathlib import Path
import subprocess
import sys
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
FORMATTER_PATH = REPOSITORY_ROOT / "configs" / "statusline" / "statusline.py"


def render_statusline(payload):
    """Render one statusline payload with the configured formatter when present.

    Args:
        payload: JSON-serializable statusline data supplied by an agent CLI.

    Returns:
        str: Formatter output without a trailing newline, or an empty string
        while the formatter is not yet implemented.

    Raises:
        subprocess.CalledProcessError: If an existing formatter exits with an
            error.
    """
    if not FORMATTER_PATH.is_file():
        return ""
    result = subprocess.run(
        [sys.executable, str(FORMATTER_PATH)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


class StatuslineFormatterTest(unittest.TestCase):
    """Verify the fields shared by Claude Code and Antigravity CLI."""

    def test_formats_claude_model_context_and_rate_limits(self):
        """Render Claude's model, effort, folder, context, and rate windows."""
        output = render_statusline(
            {
                "model": {"display_name": "Sonnet"},
                "effort": {"level": "high"},
                "workspace": {"current_dir": "/work/example-project"},
                "context_window": {"used_percentage": 23.5},
                "rate_limits": {
                    "five_hour": {"used_percentage": 17.3},
                    "seven_day": {"used_percentage": 42.4},
                },
            }
        )

        self.assertEqual(
            output,
            "Sonnet (high) · example-project · ctx 24% · 5H 17% · week 42%",
        )

    def test_formats_agy_model_context_and_quota_buckets(self):
        """Render AGY's model, context, and five-hour and weekly quotas."""
        output = render_statusline(
            {
                "model": {"display_name": "Gemini 3.5 Flash (High)"},
                "workspace": {"current_dir": "/work/example-project"},
                "context_window": {"used_percentage": 14.24},
                "quota": {
                    "gemini-five-hour": {"remaining_fraction": 0.75},
                    "gemini-weekly": {"remaining_fraction": 0.5},
                },
            }
        )

        self.assertEqual(
            output,
            "Gemini 3.5 Flash (High) · example-project · ctx 14% · 5H 25% · week 50%",
        )
