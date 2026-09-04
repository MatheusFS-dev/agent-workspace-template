"""Behavior tests for the non-interactive toolbox questionnaire adapter."""

import importlib.util
from pathlib import Path
import tempfile
import unittest

from test_install_template import PLATFORM_SCRIPT_ROOT, create_template


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
ADAPTER_PATH = PLATFORM_SCRIPT_ROOT / "toolbox_adapter.py"


def load_adapter():
    """Load the native Python 3 toolbox adapter from its script path.

    Args:
        None.

    Returns:
        module: Imported adapter module used by these behavior tests.

    Raises:
        ImportError: If the adapter cannot be loaded from its expected path.
    """
    spec = importlib.util.spec_from_file_location("toolbox_adapter", ADAPTER_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load adapter: {ADAPTER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def request(command, operation="questions", answers=None, arguments=None):
    """Build one valid adapter protocol request.

    Args:
        command: Toolbox command name identifying one setup workflow.
        operation: Protocol operation; ``questions`` discovers the next form
            field and ``run`` applies completed answers. Defaults to
            ``questions``.
        answers: Previously collected answer mapping. Defaults to an empty
            mapping when omitted.
        arguments: Direct-command argument list. Defaults to an empty list;
            setup workflows currently reject non-empty argument lists.

    Returns:
        dict: Complete request object accepted by ``handle_request``.

    Raises:
        None.

    Examples:
        Build the initial Codex questionnaire request:

        >>> request("setup-agents-codex")["operation"]
        'questions'
    """
    return {
        "operation": operation,
        "package": {
            "name": "agent-workspace-template",
            "command": command,
        },
        "answers": answers or {},
        "arguments": arguments or [],
    }


class ToolboxAdapterTest(unittest.TestCase):
    """Verify dynamic questions, write-free preparation, and explicit apply."""

    def setUp(self):
        """Create isolated template, home, and project directories.

        Args:
            None.

        Returns:
            None: Test attributes reference fresh filesystem fixtures.

        Raises:
            OSError: If temporary fixture directories cannot be created.
            ImportError: If the adapter cannot be imported.
        """
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.template_root = self.root / "template"
        self.template_root.mkdir()
        create_template(self.template_root)
        self.home_root = self.root / "home"
        self.home_root.mkdir()
        self.project_root = self.root / "project"
        self.project_root.mkdir()
        self.adapter = load_adapter()

    def tearDown(self):
        """Remove all temporary test files.

        Args:
            None.

        Returns:
            None: The fixture tree is removed.

        Raises:
            None.
        """
        self.temporary_directory.cleanup()

    def test_codex_preparation_reports_conflicts_without_writing(self):
        """Catch preparation that mutates destinations before user consent.

        Args:
            None.

        Returns:
            None: Assertions verify conflict discovery and unchanged content.

        Raises:
            OSError: If fixture files cannot be created or read.
        """
        codex_root = self.home_root / ".codex"
        codex_root.mkdir()
        config_path = codex_root / "config.toml"
        config_path.write_text("existing\n", encoding="utf-8")

        preparation = self.adapter.prepare(
            "setup-agents-codex",
            {"profiles": ["research"]},
            self.template_root,
            self.home_root,
        )

        self.assertEqual(preparation["conflicts"], [str(config_path)])
        self.assertEqual(config_path.read_text(encoding="utf-8"), "existing\n")
        self.assertFalse((codex_root / "research.config.toml").exists())

    def test_codex_questions_are_dynamic_and_do_not_repeat(self):
        """Catch a resolved question being returned again or skipped early.

        Args:
            None.

        Returns:
            None: Assertions verify profile, conflict, backup, and ready states.

        Raises:
            OSError: If conflict fixtures cannot be created.
        """
        first = self.adapter.handle_request(
            request("setup-agents-codex"), self.template_root, self.home_root
        )
        self.assertEqual(first["question"]["id"], "profiles")
        self.assertEqual(first["question"]["type"], "multiple")

        codex_root = self.home_root / ".codex"
        codex_root.mkdir()
        (codex_root / "config.toml").write_text("existing\n", encoding="utf-8")
        second = self.adapter.handle_request(
            request("setup-agents-codex", answers={"profiles": []}),
            self.template_root,
            self.home_root,
        )
        self.assertEqual(second["question"]["id"], "replace_conflicts")

        third = self.adapter.handle_request(
            request(
                "setup-agents-codex",
                answers={"profiles": [], "replace_conflicts": True},
            ),
            self.template_root,
            self.home_root,
        )
        self.assertEqual(third["question"]["id"], "create_backups")

        ready = self.adapter.handle_request(
            request(
                "setup-agents-codex",
                answers={
                    "profiles": [],
                    "replace_conflicts": True,
                    "create_backups": False,
                },
            ),
            self.template_root,
            self.home_root,
        )
        self.assertEqual(ready, {"status": "ready"})

    def test_declining_replacement_skips_with_conflicting_paths(self):
        """Catch conflict rejection that runs or omits the skip reason.

        Args:
            None.

        Returns:
            None: Assertions verify skipped status and exact conflict path.

        Raises:
            OSError: If the conflict fixture cannot be created.
        """
        claude_root = self.home_root / ".claude"
        claude_root.mkdir()
        conflict_path = claude_root / "CLAUDE.md"
        conflict_path.write_text("existing\n", encoding="utf-8")

        response = self.adapter.handle_request(
            request(
                "setup-agents-claude",
                answers={"replace_conflicts": False},
            ),
            self.template_root,
            self.home_root,
        )

        self.assertEqual(response["status"], "skipped")
        self.assertEqual(response["reason"], f"replacement declined: {conflict_path}")
        self.assertEqual(conflict_path.read_text(encoding="utf-8"), "existing\n")

    def test_antigravity_run_uses_existing_cli_destination_mapping(self):
        """Catch toolbox application drifting from standalone destinations.

        Args:
            None.

        Returns:
            None: Assertions verify Gemini rules and Antigravity CLI assets.

        Raises:
            OSError: If installed fixture files cannot be read.
        """
        response = self.adapter.handle_request(
            request("setup-agents-antigravity", operation="run"),
            self.template_root,
            self.home_root,
            output_function=lambda message: None,
        )

        self.assertEqual(response, {"status": "ready"})
        self.assertTrue((self.home_root / ".gemini" / "GEMINI.md").is_file())
        antigravity_root = self.home_root / ".gemini" / "antigravity-cli"
        self.assertTrue((antigravity_root / "settings.json").is_file())
        self.assertTrue((antigravity_root / "skills" / "first-skill").is_dir())
        self.assertFalse((self.home_root / ".antigravity").exists())

    def test_codex_and_claude_run_apply_profiles_and_explicit_backups(self):
        """Catch global apply ignoring profiles or explicit backup consent.

        Args:
            None.

        Returns:
            None: Assertions verify Codex profile installation and Claude backup.

        Raises:
            OSError: If installed or backup fixture files cannot be read.
        """
        codex_response = self.adapter.handle_request(
            request(
                "setup-agents-codex",
                operation="run",
                answers={"profiles": ["research"]},
            ),
            self.template_root,
            self.home_root,
            output_function=lambda message: None,
        )
        self.assertEqual(codex_response, {"status": "ready"})
        self.assertTrue(
            (self.home_root / ".codex" / "research.config.toml").is_file()
        )

        claude_root = self.home_root / ".claude"
        claude_root.mkdir()
        conflict = claude_root / "CLAUDE.md"
        conflict.write_text("existing\n", encoding="utf-8")
        claude_response = self.adapter.handle_request(
            request(
                "setup-agents-claude",
                operation="run",
                answers={
                    "replace_conflicts": True,
                    "create_backups": True,
                },
            ),
            self.template_root,
            self.home_root,
            output_function=lambda message: None,
        )
        self.assertEqual(claude_response, {"status": "ready"})
        backups = list(claude_root.glob("CLAUDE.md.backup-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(encoding="utf-8"), "existing\n")

    def test_project_run_applies_all_explicit_answers_without_prompts(self):
        """Catch project application that prompts or ignores form answers.

        Args:
            None.

        Returns:
            None: Assertions verify files and both independent ignore choices.

        Raises:
            OSError: If project files cannot be written or read.
        """
        answers = {
            "target_directory": str(self.project_root),
            "agent_formats": ["codex", "claude"],
            "ignore_agent_files": True,
            "ignore_superpowers": False,
        }

        response = self.adapter.handle_request(
            request("setup-agents-project", operation="run", answers=answers),
            self.template_root,
            self.home_root,
            output_function=lambda message: None,
        )

        self.assertEqual(response, {"status": "ready"})
        self.assertEqual(
            (self.project_root / "AGENTS.md").read_text(encoding="utf-8"),
            "Project rules\n",
        )
        self.assertEqual(
            (self.project_root / "CLAUDE.md").read_text(encoding="utf-8"),
            "@AGENTS.md\n",
        )
        gitignore_text = (self.project_root / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("AGENTS.md", gitignore_text)
        self.assertIn("CLAUDE.md", gitignore_text)
        self.assertNotIn("docs/superpowers/specs/", gitignore_text)

    def test_project_questions_cover_every_required_answer(self):
        """Catch omission or reordering of required project form fields.

        Args:
            None.

        Returns:
            None: Assertions verify the stable pre-execution question order.

        Raises:
            None.
        """
        answers = {}
        expected = [
            ("target_directory", str(self.project_root)),
            ("agent_formats", ["antigravity"]),
            ("ignore_agent_files", False),
            ("ignore_superpowers", True),
        ]
        for question_id, answer in expected:
            response = self.adapter.handle_request(
                request("setup-agents-project", answers=answers),
                self.template_root,
                self.home_root,
            )
            self.assertEqual(response["question"]["id"], question_id)
            answers[question_id] = answer

        self.assertEqual(
            self.adapter.handle_request(
                request("setup-agents-project", answers=answers),
                self.template_root,
                self.home_root,
            ),
            {"status": "ready"},
        )

    def test_protocol_validation_rejects_invalid_requests_and_answers(self):
        """Catch malformed protocol values reaching preparation or apply.

        Args:
            None.

        Returns:
            None: Assertions verify explicit validation failures.

        Raises:
            None.
        """
        invalid_requests = [
            {},
            request("unknown-command"),
            request("setup-agents-claude", operation="invalid"),
            request("setup-agents-claude", arguments=["unexpected"]),
            request("setup-agents-codex", answers={"profiles": ["missing"]}),
            request("setup-agents-project", answers={"target_directory": 3}),
        ]
        for invalid_request in invalid_requests:
            with self.subTest(invalid_request=invalid_request):
                with self.assertRaises((TypeError, ValueError)):
                    self.adapter.handle_request(
                        invalid_request,
                        self.template_root,
                        self.home_root,
                    )

    def test_run_rejects_missing_answers_and_declined_conflicts(self):
        """Catch execution with incomplete answers or rejected conflicts.

        Args:
            None.

        Returns:
            None: Assertions verify run never creates files in invalid states.

        Raises:
            OSError: If conflict fixtures cannot be created.
        """
        with self.assertRaisesRegex(ValueError, "missing answer"):
            self.adapter.handle_request(
                request("setup-agents-codex", operation="run"),
                self.template_root,
                self.home_root,
            )

        claude_root = self.home_root / ".claude"
        claude_root.mkdir()
        conflict_path = claude_root / "CLAUDE.md"
        conflict_path.write_text("existing\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "declined"):
            self.adapter.handle_request(
                request(
                    "setup-agents-claude",
                    operation="run",
                    answers={"replace_conflicts": False},
                ),
                self.template_root,
                self.home_root,
            )
        self.assertEqual(conflict_path.read_text(encoding="utf-8"), "existing\n")


if __name__ == "__main__":
    unittest.main()
