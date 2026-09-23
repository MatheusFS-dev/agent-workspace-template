"""Contract tests for useful Python docstring examples."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DocstringInstructionContractTest(unittest.TestCase):
    """Keep examples optional, concrete, and observable."""

    def test_examples_are_required_only_for_non_obvious_usage(self) -> None:
        """Reject unconditional, call-only, and placeholder examples."""
        instructions = (ROOT / "instructions" / "global.md").read_text(
            encoding="utf-8"
        ).lower()

        self.assertIn("google-style docstrings", instructions)
        self.assertIn("public functions and methods", instructions)
        self.assertIn("examples:", instructions)
        self.assertIn("non-obvious usage", instructions)
        self.assertIn("concrete input", instructions)
        self.assertIn("observable expected output", instructions)
        self.assertIn("call-only examples", instructions)
        self.assertIn("undefined placeholders", instructions)


if __name__ == "__main__":
    unittest.main()
