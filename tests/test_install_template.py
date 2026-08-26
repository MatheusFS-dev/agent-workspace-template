"""Focused tests for the portable agent template installer."""

import importlib.util
from pathlib import Path
import tempfile
import tomllib
import unittest


INSTALLER_PATH = Path(__file__).resolve().parents[1] / "scripts" / "install_template.py"


def load_installer():
    """Load the installer module directly from its script path.

    Args:
        None.

    Returns:
        module: Imported installer module used by the focused tests.

    Raises:
        ImportError: If the installer cannot be loaded from its expected path.
    """
    spec = importlib.util.spec_from_file_location("template_installer", INSTALLER_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load installer: {INSTALLER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


INSTALLER = load_installer()


def prompt_answers(*answers: str):
    """Build a deterministic prompt callable for one installer interaction.

    Args:
        *answers: Responses returned in prompt order. Every response is used
            exactly once by the caller that consumes the resulting callable.

    Returns:
        Callable[[str], str]: Prompt callable that yields the supplied answers.

    Raises:
        StopIteration: If the installer asks for more responses than provided.
    """
    answer_iterator = iter(answers)

    def respond(prompt: str) -> str:
        """Return the next planned answer regardless of prompt wording.

        Args:
            prompt: Prompt text passed by the installer; it is unused because
                test responses are ordered deterministically.

        Returns:
            str: Next configured response.

        Raises:
            StopIteration: If no configured response remains.
        """
        del prompt
        return next(answer_iterator)

    return respond


def create_template(template_root: Path, include_profile: bool = True) -> None:
    """Create a minimal valid installer template inside a temporary directory.

    Args:
        template_root: Empty directory that receives the fixture source tree.
        include_profile: When true, add a `research.config.toml` source profile;
            when false, create no optional Codex profile.

    Returns:
        None: The fixture directory is populated with valid required sources.

    Raises:
        OSError: If a fixture source cannot be created or written.
    """
    (template_root / "instructions").mkdir()
    (template_root / "configs" / "codex").mkdir(parents=True)
    (template_root / "configs" / "claude").mkdir(parents=True)
    (template_root / "configs" / "antigravity").mkdir(parents=True)
    (template_root / "project").mkdir()
    (template_root / "skills" / "first-skill").mkdir(parents=True)
    (template_root / "skills" / "second-skill").mkdir(parents=True)
    (template_root / "instructions" / "global.md").write_text(
        "# Canonical instructions\n\nUse evidence.\n",
        encoding="utf-8",
    )
    (template_root / "configs" / "codex" / "config.toml.template").write_text(
        "developer_instructions = '''{{GLOBAL_INSTRUCTIONS}}'''\nmodel = 'test'\n",
        encoding="utf-8",
    )
    if include_profile:
        (template_root / "configs" / "codex" / "research.config.toml").write_text(
            "web_search = 'live'\n",
            encoding="utf-8",
        )
    (template_root / "configs" / "claude" / "settings.json").write_text(
        "{\"model\": \"test\"}\n",
        encoding="utf-8",
    )
    (template_root / "configs" / "antigravity" / "settings.json").write_text(
        "{\"verbosity\": \"low\"}\n",
        encoding="utf-8",
    )
    (template_root / "project" / "AGENTS.md").write_text("Project rules\n", encoding="utf-8")
    (template_root / "project" / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
    for name in ("first-skill", "second-skill"):
        (template_root / "skills" / name / "SKILL.md").write_text(
            f"# {name}\n",
            encoding="utf-8",
        )


class InstallTemplateTest(unittest.TestCase):
    """Verify source validation, mappings, confirmations, and project scope."""

    def setUp(self) -> None:
        """Create isolated template, home, and project roots for each test.

        Args:
            None.

        Returns:
            None: Test attributes point to populated temporary directories.

        Raises:
            OSError: If temporary fixture sources cannot be created.
        """
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.template_root = self.root / "template"
        self.template_root.mkdir()
        create_template(self.template_root)
        self.home_root = self.root / "home"
        self.home_root.mkdir()
        self.output = []

    def tearDown(self) -> None:
        """Remove the temporary fixture tree after each focused test.

        Args:
            None.

        Returns:
            None: All temporary test files are removed.

        Raises:
            None.
        """
        self.temporary_directory.cleanup()

    def test_validation_rejects_missing_or_duplicate_placeholder(self) -> None:
        """Reject Codex templates that do not expose exactly one marker.

        Args:
            None.

        Returns:
            None: Assertions verify explicit template validation failures.

        Raises:
            None.
        """
        config_path = self.template_root / "configs" / "codex" / "config.toml.template"
        config_path.write_text("model = 'test'\n", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "exactly one"):
            INSTALLER.validate_sources(self.template_root)

        config_path.write_text(
            "a = '''{{GLOBAL_INSTRUCTIONS}}'''\nb = '''{{GLOBAL_INSTRUCTIONS}}'''\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(RuntimeError, "exactly one"):
            INSTALLER.validate_sources(self.template_root)

    def test_codex_renders_single_source_and_copies_selected_profile_and_skills(self) -> None:
        """Render global instructions once into Codex and copy all skills.

        Args:
            None.

        Returns:
            None: Assertions verify TOML rendering, selected profile mapping,
            and complete source-skill installation.

        Raises:
            None.
        """
        installed = INSTALLER.install_global_codex(
            self.template_root,
            self.home_root,
            prompt_answers("research"),
            self.output.append,
        )

        self.assertTrue(installed)
        config_path = self.home_root / ".codex" / "config.toml"
        config_text = config_path.read_text(encoding="utf-8")
        self.assertIn("# Canonical instructions", config_text)
        self.assertNotIn("{{GLOBAL_INSTRUCTIONS}}", config_text)
        self.assertEqual(
            tomllib.loads(config_text)["developer_instructions"],
            "# Canonical instructions\n\nUse evidence.\n",
        )
        self.assertTrue((self.home_root / ".codex" / "research.config.toml").is_file())
        self.assertEqual(
            sorted(path.name for path in (self.home_root / ".codex" / "skills").iterdir()),
            ["first-skill", "second-skill"],
        )

    def test_claude_and_antigravity_destination_mappings(self) -> None:
        """Install global files into the documented Claude and Antigravity paths.

        Args:
            None.

        Returns:
            None: Assertions verify global-rule, setting, and skill locations.

        Raises:
            None.
        """
        self.assertTrue(
            INSTALLER.install_global_claude(
                self.template_root,
                self.home_root,
                prompt_answers(),
                self.output.append,
            )
        )
        self.assertTrue(
            INSTALLER.install_global_antigravity(
                self.template_root,
                self.home_root,
                prompt_answers(),
                self.output.append,
            )
        )
        self.assertEqual(
            (self.home_root / ".claude" / "CLAUDE.md").read_text(encoding="utf-8"),
            (self.template_root / "instructions" / "global.md").read_text(encoding="utf-8"),
        )
        self.assertTrue((self.home_root / ".claude" / "settings.json").is_file())
        self.assertTrue((self.home_root / ".claude" / "skills" / "first-skill").is_dir())
        self.assertTrue((self.home_root / ".gemini" / "GEMINI.md").is_file())
        self.assertTrue(
            (self.home_root / ".gemini" / "antigravity-cli" / "settings.json").is_file()
        )
        self.assertTrue(
            (self.home_root / ".gemini" / "antigravity-cli" / "skills" / "second-skill").is_dir()
        )

    def test_project_selection_matrix_and_gitignore_idempotence(self) -> None:
        """Install only the selected project files and avoid ignore duplicates.

        Args:
            None.

        Returns:
            None: Assertions cover Codex, Antigravity, Claude, and mixed
            selection behavior plus repeatable `.gitignore` updates.

        Raises:
            None.
        """
        cases = {
            "codex": (True, False),
            "antigravity": (True, False),
            "claude": (False, True),
            "codex,antigravity,claude": (True, True),
        }
        for index, (selection, expected_files) in enumerate(cases.items()):
            target_root = self.root / f"project-{index}"
            target_root.mkdir()
            installed = INSTALLER.install_project(
                self.template_root,
                input_function=prompt_answers(str(target_root), selection, "yes"),
                output_function=self.output.append,
            )
            self.assertTrue(installed)
            self.assertEqual((target_root / "AGENTS.md").exists(), expected_files[0])
            self.assertEqual((target_root / "CLAUDE.md").exists(), expected_files[1])
            self.assertFalse((target_root / "skills").exists())

            instruction_names = ["AGENTS.md"] if expected_files[0] else []
            if expected_files[1]:
                instruction_names.append("CLAUDE.md")
            INSTALLER.update_gitignore(target_root, instruction_names)
            gitignore_text = (target_root / ".gitignore").read_text(encoding="utf-8")
            for name in instruction_names:
                self.assertEqual(gitignore_text.splitlines().count(name), 1)
            for path in ("docs/superpowers/specs/", "docs/superpowers/plans/"):
                self.assertEqual(gitignore_text.splitlines().count(path), 1)

    def test_conflict_cancellation_and_optional_backups(self) -> None:
        """Leave conflicts untouched on cancellation and back them up on consent.

        Args:
            None.

        Returns:
            None: Assertions verify both confirmation paths before replacement.

        Raises:
            None.
        """
        claude_root = self.home_root / ".claude"
        claude_root.mkdir()
        instruction_path = claude_root / "CLAUDE.md"
        instruction_path.write_text("keep this\n", encoding="utf-8")

        cancelled = INSTALLER.install_global_claude(
            self.template_root,
            self.home_root,
            prompt_answers("no"),
            self.output.append,
        )
        self.assertFalse(cancelled)
        self.assertEqual(instruction_path.read_text(encoding="utf-8"), "keep this\n")

        installed = INSTALLER.install_global_claude(
            self.template_root,
            self.home_root,
            prompt_answers("yes", "yes"),
            self.output.append,
        )
        self.assertTrue(installed)
        self.assertEqual(
            instruction_path.read_text(encoding="utf-8"),
            (self.template_root / "instructions" / "global.md").read_text(encoding="utf-8"),
        )
        backups = list(claude_root.glob("CLAUDE.md.backup-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(encoding="utf-8"), "keep this\n")
