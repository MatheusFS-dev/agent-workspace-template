"""Contract tests for the portable session-handoff skill."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "skills" / "session-handoff" / "SKILL.md"


def read_skill() -> str:
    """Return the session-handoff contract in lowercase.

    Returns:
        Lowercase skill text for case-insensitive contract assertions.
    """
    return SKILL_PATH.read_text(encoding="utf-8").lower()


class SessionHandoffSkillContractTest(unittest.TestCase):
    """Keep session handoffs portable, safe, and reconciled on resume."""

    def test_save_and_load_are_explicit_and_use_one_fixed_destination(self) -> None:
        """Require explicit checkpoint or resume requests and one task record."""
        skill = read_skill()

        self.assertIn("activate only when the user explicitly asks", skill)
        self.assertIn("save / checkpoint mode", skill)
        self.assertIn("load / resume mode", skill)
        self.assertIn(".agent/state/current_task.md", skill)
        self.assertIn("replace the single current-task file", skill)
        self.assertIn("never append", skill)
        self.assertIn("git root", skill)
        self.assertIn("fall back to the current directory", skill)

    def test_checkpoint_contract_is_complete_safe_and_non_mutating(self) -> None:
        """Require the complete schema while excluding unsafe retained content."""
        skill = read_skill()

        for field in (
            "iso-8601",
            "objective",
            "acceptance criteria",
            "constraints and decisions",
            "completed work and current state",
            "branch, head, and concise worktree status",
            "verification commands and observed results",
            "blockers and risks",
            "ordered next actions",
            "repository-relative files and relevant urls",
        ):
            self.assertIn(field, skill)

        for exclusion in (
            "secrets",
            "credentials",
            "absolute home paths",
            "raw transcripts",
            "hidden reasoning",
            "unsupported inferences",
        ):
            self.assertIn(exclusion, skill)

        self.assertIn("do not stage, commit, push, or modify `.gitignore`", skill)

    def test_resume_reconciles_drift_without_inheriting_authorization(self) -> None:
        """Require stale-state checks and forbid replaying saved authority."""
        skill = read_skill()

        for current_fact in (
            "saved branch",
            "head",
            "worktree state",
            "references",
            "relevant external status",
        ):
            self.assertIn(current_fact, skill)

        self.assertIn("mark drift explicitly", skill)
        self.assertIn("missing or malformed", skill)
        self.assertIn("do not invent context", skill)
        self.assertIn("context, not authorization", skill)
        self.assertIn("do not replay completed actions", skill)
        self.assertIn("do not trust stale results", skill)
        self.assertIn("do not inherit permission for new mutations", skill)


if __name__ == "__main__":
    unittest.main()
