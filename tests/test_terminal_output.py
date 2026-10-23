"""Terminal contract tests for standalone agent-workspace installers."""
import io
import importlib.util
from pathlib import Path
import unittest
from unittest import mock

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "toolbox_output.py"
SPEC = importlib.util.spec_from_file_location("agent_workspace_toolbox_output", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
TerminalOutput = MODULE.TerminalOutput


class TerminalOutputTests(unittest.TestCase):
    """Verify deterministic redirected formatting."""

    def test_levels_opening_blank_and_no_redirected_ansi(self):
        """Render prefixed semantic output without redirected color."""
        stream = io.StringIO()
        output = TerminalOutput("setup-agents-codex", stream, lambda: "09:32:23", False)
        output.info("Checking...")
        output.warn("Retry")
        output.success("Installed")
        self.assertEqual(
            stream.getvalue(),
            "\n[09:32:23 setup-agents-codex INFO] Checking...\n"
            "[09:32:23 setup-agents-codex WARN] Retry\n"
            "[09:32:23 setup-agents-codex SUCCESS] Installed\n",
        )

    def test_input_function_displays_readable_yes_no_defaults(self):
        """Translate legacy yes/no markers into explicit default labels."""
        for prompt, expected in (
            ("Replace all listed paths? [Y/n]: ", "[Y/n] (default: Y):"),
            ("Create backups? [y/N]: ", "[y/N] (default: n):"),
        ):
            stream = io.StringIO()
            output = TerminalOutput(
                "setup-agents-codex", stream, lambda: "09:32:23", False
            )
            with mock.patch("builtins.input", return_value=""):
                self.assertEqual(output.input_function(prompt), "")
            rendered = stream.getvalue()
            self.assertIn(expected, rendered)

    def test_menu_prefixes_only_question(self):
        """Render an interactive menu as one labeled block."""
        stream = io.StringIO()
        output = TerminalOutput("setup-agents-codex", stream, lambda: "09:32:23", False)
        output.menu("Choose a tool", ["1. First", "2. Second"])
        self.assertEqual(stream.getvalue(), "\n[09:32:23 setup-agents-codex PROMPT] Choose a tool\n  1. First\n  2. Second\n")


if __name__ == "__main__":
    unittest.main()
