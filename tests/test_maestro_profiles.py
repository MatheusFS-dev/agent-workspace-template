from pathlib import Path
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
