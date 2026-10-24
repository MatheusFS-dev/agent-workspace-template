"""OpenCode installer and adapter contract tests."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OpenCodeSetupTests(unittest.TestCase):
    def test_standalone_install_and_conflicts(self):
        for platform in ('linux/python3', 'windows'):
            installer = load(ROOT / 'scripts' / platform / 'install_opencode.py')
            if platform == 'windows':
                installer.validate_platform = lambda: None
            with tempfile.TemporaryDirectory() as directory:
                home = Path(directory)
                messages = []
                self.assertTrue(installer.install_global_opencode(ROOT, home, output_function=messages.append))
                target = home / '.config' / 'opencode'
                self.assertEqual((target / 'AGENTS.md').read_bytes(), (ROOT / 'instructions/global.md').read_bytes())
                self.assertEqual(json.loads((target / 'opencode.json').read_text())['permission'], 'allow')
                self.assertTrue((target / 'skills/scribe/SKILL.md').is_file())
                self.assertFalse(installer.install_global_opencode(ROOT, home, input_function=lambda _: 'n', output_function=messages.append))
                self.assertIn('Installation cancelled; no files were changed.', messages)
                (target / 'AGENTS.md').write_text('old instructions')
                answers = iter(['y', 'y'])
                self.assertTrue(installer.install_global_opencode(ROOT, home, input_function=lambda _: next(answers), output_function=messages.append))
                backups = list(target.glob('AGENTS.md.backup-*'))
                self.assertEqual(len(backups), 1)
                self.assertEqual(backups[0].read_text(), 'old instructions')
                self.assertEqual((target / 'AGENTS.md').read_bytes(), (ROOT / 'instructions/global.md').read_bytes())

    def test_adapter_project_mixed_selection(self):
        for platform in ('linux/python3', 'windows'):
            adapter = load(ROOT / 'scripts' / platform / 'toolbox_adapter.py')
            adapter.INSTALLERS['opencode'].validate_platform = lambda: None
            adapter.INSTALLERS['project'].validate_platform = lambda: None
            with tempfile.TemporaryDirectory() as directory:
                home = Path(directory)
                prepared = adapter.prepare('setup-agents-opencode', {}, ROOT, home)
                self.assertEqual(len(prepared['conflicts']), 0)
                adapter.INSTALLERS['opencode'].validate_sources(ROOT)
                (home / '.config/opencode').mkdir(parents=True)
                (home / '.config/opencode/AGENTS.md').write_text('conflict')
                conflicted = adapter.prepare('setup-agents-opencode', {}, ROOT, home)
                self.assertEqual(conflicted['conflicts'], [str(home / '.config/opencode/AGENTS.md')])
                self.assertEqual(len(prepared['items']), len(list((ROOT / 'skills').iterdir())) + 2)
                project = adapter.prepare('setup-agents-project', {'target_directory': directory, 'agent_formats': ['codex', 'opencode'], 'ignore_agent_files': False, 'ignore_superpowers': False}, ROOT, home)
                self.assertEqual(len(project['items']), 1)
                self.assertEqual(project['items'][0][1], home / 'AGENTS.md')


if __name__ == '__main__':
    unittest.main()
