"""Focused tests for the portable agent template installer."""

import builtins
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
# Exercise only the native implementation while using the opposite scripts to
# prove that platform rejection happens before any interactive or write path.
if sys.platform.startswith("linux"):
    PLATFORM_NAME = "linux"
    OTHER_PLATFORM_NAME = "windows"
    PLATFORM_SCRIPT_ROOT = REPOSITORY_ROOT / "scripts" / "linux" / "python3"
    OTHER_PLATFORM_SCRIPT_ROOT = REPOSITORY_ROOT / "scripts" / "windows"
    HOME_ENVIRONMENT_VARIABLE = "HOME"
    OTHER_PLATFORM_ERROR = "Windows installer requires Windows."
elif sys.platform == "win32":
    PLATFORM_NAME = "windows"
    OTHER_PLATFORM_NAME = "linux"
    PLATFORM_SCRIPT_ROOT = REPOSITORY_ROOT / "scripts" / "windows"
    OTHER_PLATFORM_SCRIPT_ROOT = REPOSITORY_ROOT / "scripts" / "linux" / "python3"
    HOME_ENVIRONMENT_VARIABLE = "USERPROFILE"
    OTHER_PLATFORM_ERROR = "Linux installer requires Linux."
else:
    raise RuntimeError("Installer tests require Linux or Windows.")

INSTALLER_PATHS = {
    name: PLATFORM_SCRIPT_ROOT / f"install_{name}.py"
    for name in ("codex", "claude", "antigravity", "project")
}
OTHER_INSTALLER_PATHS = {
    name: OTHER_PLATFORM_SCRIPT_ROOT / f"install_{name}.py"
    for name in ("codex", "claude", "antigravity", "project")
}


def load_installer(name: str):
    """Load one workflow installer module directly from its script path.

    Args:
        name: Workflow name from `INSTALLER_PATHS` whose module should load.

    Returns:
        module: Imported installer module used by the focused tests.

    Raises:
        KeyError: If `name` does not identify a configured workflow.
        ImportError: If the installer cannot be loaded from its expected path.
    """
    installer_path = INSTALLER_PATHS[name]
    spec = importlib.util.spec_from_file_location(
        f"template_installer_{name}",
        installer_path,
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load installer: {installer_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_codex_without_tomllib():
    """Load the native Codex installer while hiding the stdlib TOML parser.

    Args:
        None.

    Returns:
        module: Codex installer loaded through its bundled TOML fallback path.

    Raises:
        AssertionError: If the installer cannot load without stdlib `tomllib`.
        ImportError: If another installer dependency cannot be imported.
    """
    original_import = builtins.__import__

    def import_without_tomllib(name, globals=None, locals=None, fromlist=(), level=0):
        """Reject only the stdlib TOML parser import during module loading."""
        if name == "tomllib":
            raise ModuleNotFoundError("No module named 'tomllib'", name="tomllib")
        return original_import(name, globals, locals, fromlist, level)

    try:
        with mock.patch.object(builtins, "__import__", side_effect=import_without_tomllib):
            return load_installer("codex")
    except ModuleNotFoundError as error:
        raise AssertionError(
            "Codex installer did not load its bundled TOML parser fallback"
        ) from error


CODEX_INSTALLER = load_installer("codex")
CLAUDE_INSTALLER = load_installer("claude")
ANTIGRAVITY_INSTALLER = load_installer("antigravity")
PROJECT_INSTALLER = load_installer("project")


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
            CODEX_INSTALLER.validate_sources(self.template_root)

        config_path.write_text(
            "a = '''{{GLOBAL_INSTRUCTIONS}}'''\nb = '''{{GLOBAL_INSTRUCTIONS}}'''\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(RuntimeError, "exactly one"):
            CODEX_INSTALLER.validate_sources(self.template_root)

    def test_codex_fallback_loads_bundled_tomli_2_2_1(self) -> None:
        """Load the native bundled Tomli package when `tomllib` is absent.

        Args:
            None.

        Returns:
            None: Assertions verify the fallback version and file location.

        Raises:
            None.
        """
        fallback_installer = load_codex_without_tomllib()

        self.assertEqual(fallback_installer.tomllib.__version__, "2.2.1")
        self.assertEqual(
            Path(fallback_installer.tomllib.__file__).resolve(),
            (PLATFORM_SCRIPT_ROOT / "_vendor" / "tomli" / "__init__.py").resolve(),
        )

    def test_codex_fallback_parses_valid_rendered_config(self) -> None:
        """Parse a rendered Codex configuration through bundled Tomli.

        Args:
            None.

        Returns:
            None: Assertions verify real fallback parsing of rendered content.

        Raises:
            None.
        """
        fallback_installer = load_codex_without_tomllib()

        rendered = fallback_installer.render_codex_config(self.template_root)

        self.assertEqual(
            fallback_installer.tomllib.loads(rendered)["developer_instructions"],
            "# Canonical instructions\n\nUse evidence.\n",
        )

    def test_codex_fallback_rejects_malformed_toml_before_writes(self) -> None:
        """Reject malformed fallback-parsed TOML before creating destinations.

        Args:
            None.

        Returns:
            None: Assertions verify validation failure and an untouched home.

        Raises:
            None.
        """
        fallback_installer = load_codex_without_tomllib()
        config_path = self.template_root / "configs" / "codex" / "config.toml.template"
        config_path.write_text(
            "developer_instructions = '''{{GLOBAL_INSTRUCTIONS}}'''\nbroken = [\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(RuntimeError, "invalid TOML"):
            fallback_installer.install_global_codex(
                self.template_root,
                self.home_root,
                prompt_answers(),
                self.output.append,
            )

        self.assertEqual(list(self.home_root.iterdir()), [])

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
        installed = CODEX_INSTALLER.install_global_codex(
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
            CODEX_INSTALLER.tomllib.loads(config_text)["developer_instructions"],
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
            CLAUDE_INSTALLER.install_global_claude(
                self.template_root,
                self.home_root,
                prompt_answers(),
                self.output.append,
            )
        )
        self.assertTrue(
            ANTIGRAVITY_INSTALLER.install_global_antigravity(
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
            installed = PROJECT_INSTALLER.install_project(
                self.template_root,
                input_function=prompt_answers(str(target_root), selection, "yes", "yes"),
                output_function=self.output.append,
            )
            self.assertTrue(installed)
            self.assertEqual((target_root / "AGENTS.md").exists(), expected_files[0])
            self.assertEqual((target_root / "CLAUDE.md").exists(), expected_files[1])
            self.assertFalse((target_root / "skills").exists())

            instruction_names = ["AGENTS.md"] if expected_files[0] else []
            if expected_files[1]:
                instruction_names.append("CLAUDE.md")
            PROJECT_INSTALLER.update_gitignore(
                target_root,
                [*instruction_names, *PROJECT_INSTALLER.SUPERPOWERS_GITIGNORE_LINES],
            )
            gitignore_text = (target_root / ".gitignore").read_text(encoding="utf-8")
            for name in instruction_names:
                self.assertEqual(gitignore_text.splitlines().count(name), 1)
            for path in ("docs/superpowers/specs/", "docs/superpowers/plans/"):
                self.assertEqual(gitignore_text.splitlines().count(path), 1)

    def test_project_gitignore_choices_are_independent(self) -> None:
        """Apply instruction and Superpowers ignore choices independently.

        Args:
            None.

        Returns:
            None: Assertions verify every combination of the two decisions.

        Raises:
            None.
        """
        cases = {
            ("yes", "no"): {"# Agent workspace template", "AGENTS.md", "CLAUDE.md"},
            ("no", "yes"): {
                "# Agent workspace template",
                "docs/superpowers/specs/",
                "docs/superpowers/plans/",
            },
            ("yes", "yes"): {
                "# Agent workspace template",
                "AGENTS.md",
                "CLAUDE.md",
                "docs/superpowers/specs/",
                "docs/superpowers/plans/",
            },
            ("no", "no"): set(),
        }
        for index, ((instruction_answer, superpowers_answer), expected_lines) in enumerate(
            cases.items()
        ):
            with self.subTest(
                instructions=instruction_answer,
                superpowers=superpowers_answer,
            ):
                target_root = self.root / f"project-ignore-{index}"
                target_root.mkdir()

                installed = PROJECT_INSTALLER.install_project(
                    self.template_root,
                    input_function=prompt_answers(
                        str(target_root),
                        "codex,claude",
                        instruction_answer,
                        superpowers_answer,
                    ),
                    output_function=self.output.append,
                )

                self.assertTrue(installed)
                gitignore_path = target_root / ".gitignore"
                actual_lines = (
                    set(gitignore_path.read_text(encoding="utf-8").splitlines())
                    if gitignore_path.exists()
                    else set()
                )
                self.assertEqual(actual_lines, expected_lines)

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

        cancelled = CLAUDE_INSTALLER.install_global_claude(
            self.template_root,
            self.home_root,
            prompt_answers("no"),
            self.output.append,
        )
        self.assertFalse(cancelled)
        self.assertEqual(instruction_path.read_text(encoding="utf-8"), "keep this\n")

        installed = CLAUDE_INSTALLER.install_global_claude(
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

    def test_each_workflow_ignores_unrelated_template_sources(self) -> None:
        """Install each workflow without source assets owned by other workflows.

        Args:
            None.

        Returns:
            None: Assertions verify that every installer has a narrow source
            validation boundary and still creates its expected destination.

        Raises:
            OSError: If a temporary fixture cannot be created or removed.
        """
        cases = (
            (
                CODEX_INSTALLER.install_global_codex,
                ("",),
                ("configs/claude", "configs/antigravity", "project"),
                ".codex/config.toml",
            ),
            (
                CLAUDE_INSTALLER.install_global_claude,
                (),
                ("configs/codex", "configs/antigravity", "project"),
                ".claude/CLAUDE.md",
            ),
            (
                ANTIGRAVITY_INSTALLER.install_global_antigravity,
                (),
                ("configs/codex", "configs/claude", "project"),
                ".gemini/GEMINI.md",
            ),
        )
        for index, (installer, answers, removed_paths, destination) in enumerate(cases):
            with self.subTest(destination=destination):
                template_root = self.root / f"isolated-template-{index}"
                template_root.mkdir()
                create_template(template_root)
                for relative_path in removed_paths:
                    shutil.rmtree(template_root / relative_path)
                home_root = self.root / f"isolated-home-{index}"
                home_root.mkdir()

                installed = installer(
                    template_root,
                    home_root,
                    prompt_answers(*answers),
                    self.output.append,
                )

                self.assertTrue(installed)
                self.assertTrue((home_root / destination).exists())

        project_template_root = self.root / "isolated-template-project"
        project_template_root.mkdir()
        create_template(project_template_root)
        shutil.rmtree(project_template_root / "instructions")
        shutil.rmtree(project_template_root / "configs")
        shutil.rmtree(project_template_root / "skills")
        target_root = self.root / "isolated-project"
        target_root.mkdir()

        installed = PROJECT_INSTALLER.install_project(
            project_template_root,
            input_function=prompt_answers(str(target_root), "codex", "no", "no"),
            output_function=self.output.append,
        )

        self.assertTrue(installed)
        self.assertTrue((target_root / "AGENTS.md").is_file())

    def test_workflows_reject_invalid_required_sources(self) -> None:
        """Reject malformed or missing sources owned by each workflow.

        Args:
            None.

        Returns:
            None: Assertions verify explicit validation errors for Claude,
            Antigravity, and project-owned inputs. Codex rendering validation is
            covered separately by the placeholder test.

        Raises:
            OSError: If a temporary fixture cannot be created or changed.
        """
        invalid_json_cases = (
            (CLAUDE_INSTALLER, "claude"),
            (ANTIGRAVITY_INSTALLER, "antigravity"),
        )
        for index, (installer, config_name) in enumerate(invalid_json_cases):
            with self.subTest(config_name=config_name):
                template_root = self.root / f"invalid-template-{index}"
                template_root.mkdir()
                create_template(template_root)
                settings_path = template_root / "configs" / config_name / "settings.json"
                settings_path.write_text("not json\n", encoding="utf-8")

                with self.assertRaisesRegex(RuntimeError, "Invalid JSON source"):
                    installer.validate_sources(template_root)

        project_template_root = self.root / "invalid-template-project"
        project_template_root.mkdir()
        create_template(project_template_root)
        (project_template_root / "project" / "CLAUDE.md").unlink()

        with self.assertRaisesRegex(RuntimeError, "Project template source is missing"):
            PROJECT_INSTALLER.validate_sources(project_template_root)

    def test_scripts_run_directly_without_a_workflow_menu(self) -> None:
        """Run each script as its documented workflow entry point.

        Args:
            None.

        Returns:
            None: Assertions verify zero exit codes and installed output files
            under isolated home and project directories.

        Raises:
            OSError: If a subprocess cannot start or a temporary path fails.
            subprocess.TimeoutExpired: If an installer does not complete within
                the ten-second smoke-test limit.
        """
        smoke_home = self.root / "smoke-home"
        smoke_home.mkdir()
        environment = os.environ.copy()
        environment[HOME_ENVIRONMENT_VARIABLE] = str(smoke_home)
        commands = (
            ("codex", "\n"),
            ("claude", ""),
            ("antigravity", ""),
        )
        for name, input_text in commands:
            with self.subTest(name=name):
                result = subprocess.run(
                    [sys.executable, str(INSTALLER_PATHS[name])],
                    input=input_text,
                    text=True,
                    capture_output=True,
                    env=environment,
                    cwd=REPOSITORY_ROOT,
                    timeout=10,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)

        target_root = self.root / "smoke-project"
        target_root.mkdir()
        project_result = subprocess.run(
            [sys.executable, str(INSTALLER_PATHS["project"])],
            input=f"{target_root}\ncodex\nno\nno\n",
            text=True,
            capture_output=True,
            env=environment,
            cwd=REPOSITORY_ROOT,
            timeout=10,
            check=False,
        )
        self.assertEqual(project_result.returncode, 0, project_result.stderr)
        self.assertTrue((smoke_home / ".codex" / "config.toml").is_file())
        self.assertTrue((smoke_home / ".claude" / "CLAUDE.md").is_file())
        self.assertTrue((smoke_home / ".gemini" / "GEMINI.md").is_file())
        self.assertTrue((target_root / "AGENTS.md").is_file())

    def test_other_platform_scripts_fail_before_writing(self) -> None:
        """Reject every opposite-platform entry point before filesystem writes.

        Args:
            None.

        Returns:
            None: Assertions verify nonzero exits, explicit platform errors,
            and an untouched temporary home directory.

        Raises:
            OSError: If a subprocess cannot start or a temporary path fails.
            subprocess.TimeoutExpired: If an installer does not complete within
                the ten-second smoke-test limit.
        """
        wrong_home = self.root / "wrong-platform-home"
        wrong_home.mkdir()
        environment = os.environ.copy()
        environment[HOME_ENVIRONMENT_VARIABLE] = str(wrong_home)

        for name, installer_path in OTHER_INSTALLER_PATHS.items():
            with self.subTest(name=name):
                result = subprocess.run(
                    [sys.executable, str(installer_path)],
                    text=True,
                    capture_output=True,
                    env=environment,
                    cwd=REPOSITORY_ROOT,
                    timeout=10,
                    check=False,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(OTHER_PLATFORM_ERROR, result.stderr)

        self.assertEqual(list(wrong_home.iterdir()), [])
