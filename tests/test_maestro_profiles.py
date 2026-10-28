from pathlib import Path
import importlib.util
import tempfile
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class MaestroProfilesTest(unittest.TestCase):
    def test_maestro_instructions_are_profile_scoped(self):
        maestro = (ROOT / "instructions" / "maestro.md").read_text(encoding="utf-8")
        self.assertIn("start_implementation", maestro)
        self.assertIn("maestro_worker", maestro)
        self.assertIn("three", maestro.lower())
        self.assertIn("Do not commit", maestro)
        self.assertNotIn("maestro_worker", (ROOT / "instructions" / "global.md").read_text(encoding="utf-8"))

    def test_maestro_profiles_exist_for_all_supported_agents(self):
        self.assertTrue((ROOT / "configs" / "codex" / "maestro.config.toml").is_file())
        self.assertTrue((ROOT / "configs" / "claude" / "agents" / "maestro.md").is_file())
        self.assertTrue((ROOT / "configs" / "antigravity" / "agents" / "maestro" / "agent.md").is_file())

    def test_codex_maestro_profile_renders_global_and_maestro_instructions(self):
        for platform in ("linux/python3", "windows"):
            with self.subTest(platform=platform):
                path = ROOT / "scripts" / platform / "install_codex.py"
                spec = importlib.util.spec_from_file_location("install_codex", path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                rendered = module.render_maestro_config(ROOT)
                self.assertIn("[mcp_servers.maestro_worker]", rendered)
                self.assertIn('command = "tb"', rendered)
                self.assertIn('"local-llm", "maestro-mcp"', rendered)
                self.assertIn("Global Task Gates", rendered)
                self.assertNotIn("{{MAESTRO_INSTRUCTIONS}}", rendered)

    def test_installed_maestro_profiles_stop_after_worker_failure(self):
        """Catch a controller taking over after the local worker exits unsuccessfully."""
        installer_root = ROOT / "scripts" / ("windows" if sys.platform == "win32" else "linux/python3")

        def load(name):
            spec = importlib.util.spec_from_file_location(name, installer_root / ("install_" + name + ".py"))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module

        with tempfile.TemporaryDirectory() as temporary_directory:
            home = Path(temporary_directory)
            self.assertTrue(load("codex").install_global_codex(ROOT, home, lambda _prompt: "maestro", lambda _message: None))
            self.assertTrue(load("claude").install_global_claude(ROOT, home, lambda _prompt: "maestro", lambda _message: None))
            self.assertTrue(load("antigravity").install_global_antigravity(ROOT, home, lambda _prompt: "maestro", lambda _message: None))

            installed_profiles = (
                home / ".codex" / "maestro.config.toml",
                home / ".claude" / "agents" / "maestro.md",
            )
            for profile in installed_profiles:
                with self.subTest(profile=profile):
                    instructions = profile.read_text(encoding="utf-8")
                    self.assertIn("A failed worker run is terminal", instructions)
                    self.assertIn("Do not implement, edit,", instructions)
                    self.assertIn("inspect partial changes", instructions)
                    self.assertIn("ask the user to fix the", instructions.lower())
            self.assertTrue((home / ".codex" / "maestro_guard.py").is_file())

    def test_standalone_installers_install_maestro_and_report_how_to_start_it(self):
        """Catch setup completion that advertises an unavailable Maestro profile."""
        installer_root = ROOT / "scripts" / ("windows" if sys.platform == "win32" else "linux/python3")

        def load(name):
            spec = importlib.util.spec_from_file_location(name, installer_root / ("install_" + name + ".py"))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module

        with tempfile.TemporaryDirectory() as temporary_directory:
            home = Path(temporary_directory)
            codex_output = []
            self.assertTrue(
                load("codex").install_global_codex(
                    ROOT, home, lambda _prompt: "maestro", codex_output.append
                )
            )
            codex_profile = (home / ".codex" / "maestro.config.toml").read_text(encoding="utf-8")
            self.assertIn("maestro_worker", codex_profile)
            self.assertIn("codex --profile maestro", "\n".join(codex_output))

            claude_output = []
            self.assertTrue(load("claude").install_global_claude(ROOT, home, lambda _prompt: "", claude_output.append))
            self.assertTrue((home / ".claude" / "agents" / "maestro.md").is_file())
            self.assertIn("claude --agent maestro", "\n".join(claude_output))

            antigravity_output = []
            self.assertTrue(load("antigravity").install_global_antigravity(ROOT, home, lambda _prompt: "", antigravity_output.append))
            self.assertTrue((home / ".gemini" / "config" / "agents" / "maestro" / "agent.md").is_file())
            self.assertIn("no native Maestro worker MCP integration", "\n".join(antigravity_output))

    def test_blank_codex_profile_selection_installs_maestro(self):
        """Catch a default Codex setup that leaves Maestro unavailable."""
        installer_root = ROOT / "scripts" / ("windows" if sys.platform == "win32" else "linux/python3")
        spec = importlib.util.spec_from_file_location(
            "install_codex", installer_root / "install_codex.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as temporary_directory:
            home = Path(temporary_directory)
            self.assertTrue(
                module.install_global_codex(ROOT, home, lambda _prompt: "", lambda _message: None)
            )
            profile = (home / ".codex" / "maestro.config.toml").read_text(encoding="utf-8")
            self.assertIn("maestro_worker", profile)

    def test_toolbox_codex_question_selects_maestro_by_default(self):
        """Catch toolbox setup presenting a default that omits Maestro."""
        path = ROOT / "scripts" / "linux" / "python3" / "toolbox_adapter.py"
        spec = importlib.util.spec_from_file_location("toolbox_adapter", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as temporary_directory:
            question = module.handle_request(
                {
                    "operation": "questions",
                    "package": {
                        "name": "agent-workspace-template",
                        "command": "setup-agents-codex",
                    },
                    "answers": {},
                    "arguments": [],
                },
                ROOT,
                Path(temporary_directory),
            )
            self.assertEqual(question["question"]["default"], ["maestro"])

    def test_toolbox_controller_setups_offer_only_maestro(self):
        """Catch controller setup questions that omit Maestro or retain Research."""
        path = ROOT / "scripts" / "linux" / "python3" / "toolbox_adapter.py"
        spec = importlib.util.spec_from_file_location("toolbox_adapter", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as temporary_directory:
            for command in ("setup-agents-codex", "setup-agents-claude", "setup-agents-antigravity"):
                with self.subTest(command=command):
                    question = module.handle_request(
                        {
                            "operation": "questions",
                            "package": {"name": "agent-workspace-template", "command": command},
                            "answers": {},
                            "arguments": [],
                        },
                        ROOT,
                        Path(temporary_directory),
                    )
                    self.assertEqual(question["question"]["id"], "profiles")
                    self.assertEqual(question["question"]["default"], ["maestro"])
                    self.assertEqual(question["question"]["options"], [{"value": "maestro", "label": "maestro"}])

class WindowsMaestroAdapterTest(unittest.TestCase):
    def test_profiles_are_selectable_installed_and_described(self):
        """Exercise Windows setup parity on either host platform."""
        path = ROOT / "scripts" / "windows" / "toolbox_adapter.py"
        spec = importlib.util.spec_from_file_location("windows_adapter", path)
        adapter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(adapter)
        for installer in adapter.INSTALLERS.values():
            installer.validate_platform = lambda: None
        with tempfile.TemporaryDirectory() as temporary_directory:
            home = Path(temporary_directory)
            for name, destination, guide in (
                ("codex", home / ".codex" / "maestro.config.toml", "codex --profile maestro"),
                ("claude", home / ".claude" / "agents" / "maestro.md", "claude --agent maestro"),
                ("antigravity", home / ".gemini" / "config" / "agents" / "maestro" / "agent.md", "Antigravity"),
            ):
                with self.subTest(name=name):
                    request = {"operation": "questions", "package": {"name": "agent-workspace-template", "command": "setup-agents-" + name}, "answers": {}, "arguments": []}
                    question = adapter.handle_request(request, ROOT, home)
                    self.assertEqual(question["question"]["default"], ["maestro"])
                    request.update(operation="run", answers={"profiles": ["maestro"]})
                    messages = []
                    adapter.handle_request(request, ROOT, home, output_function=messages.append)
                    self.assertTrue(destination.is_file())
                    self.assertIn(guide, "\n".join(messages))
