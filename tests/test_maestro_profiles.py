from pathlib import Path
import importlib.util
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class MaestroProfilesTest(unittest.TestCase):
    def test_maestro_instructions_are_profile_scoped(self):
        maestro = (ROOT / "instructions" / "maestro.md").read_text(encoding="utf-8")
        self.assertIn("tb local-llm worker", maestro)
        self.assertIn("three", maestro.lower())
        self.assertIn("Do not commit", maestro)
        self.assertNotIn("tb local-llm worker", (ROOT / "instructions" / "global.md").read_text(encoding="utf-8"))

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
                self.assertIn("tb local-llm worker", rendered)
                self.assertIn("Global Task Gates", rendered)
                self.assertNotIn("{{MAESTRO_INSTRUCTIONS}}", rendered)

    def test_standalone_installers_install_maestro_and_report_how_to_start_it(self):
        """Catch setup completion that advertises an unavailable Maestro profile."""
        installer_root = ROOT / "scripts" / "linux" / "python3"

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
            self.assertIn("tb local-llm worker", codex_profile)
            self.assertIn("codex --profile maestro", "\n".join(codex_output))

            claude_output = []
            self.assertTrue(load("claude").install_global_claude(ROOT, home, lambda _prompt: "", claude_output.append))
            self.assertTrue((home / ".claude" / "agents" / "maestro.md").is_file())
            self.assertIn("claude --agent maestro", "\n".join(claude_output))

            antigravity_output = []
            self.assertTrue(load("antigravity").install_global_antigravity(ROOT, home, lambda _prompt: "", antigravity_output.append))
            self.assertTrue((home / ".gemini" / "config" / "agents" / "maestro" / "agent.md").is_file())
            self.assertIn("select the `maestro` agent", "\n".join(antigravity_output))
