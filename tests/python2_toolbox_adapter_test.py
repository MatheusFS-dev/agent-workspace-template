"""Python 2.7 runtime tests for the toolbox adapter fallback."""

import imp
import io
import json
import os
import shutil
import tempfile
import unittest


REPOSITORY_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ADAPTER_PATH = os.path.join(
    REPOSITORY_ROOT, "scripts", "linux", "python2", "toolbox_adapter.py"
)


def write_text(path, content):
    """Create a parent directory and write one UTF-8 fixture file.

    Args:
        path (str): Destination fixture path.
        content (unicode): Complete file content.

    Returns:
        None: The fixture exists after the call.

    Raises:
        IOError: If the directory or file cannot be created.
    """
    parent = os.path.dirname(path)
    if not os.path.isdir(parent):
        os.makedirs(parent)
    with io.open(path, "w", encoding="utf-8") as destination:
        destination.write(content)


def protocol_request(command, operation, answers):
    """Build one valid Python 2 adapter protocol request.

    Args:
        command (str): Supported setup command name.
        operation (str): Questions or run protocol operation.
        answers (dict): Accumulated answer mapping.

    Returns:
        dict: Complete request including an empty direct-argument list.

    Raises:
        None.
    """
    return {
        "operation": operation,
        "package": {
            "name": "agent-workspace-template",
            "command": command,
        },
        "answers": answers,
        "arguments": [],
    }


class Python2ToolboxAdapterTest(unittest.TestCase):
    """Verify the fallback interpreter performs preparation and explicit apply."""

    def setUp(self):
        """Create a minimal valid template and isolated destinations.

        Args:
            None.

        Returns:
            None: Test attributes reference fresh fixtures.

        Raises:
            IOError: If fixture files cannot be created.
            ImportError: If the adapter or TOML dependency cannot load.
        """
        self.root = tempfile.mkdtemp()
        self.template = os.path.join(self.root, "template")
        self.home = os.path.join(self.root, "home")
        self.project = os.path.join(self.root, "project")
        os.makedirs(self.home)
        os.makedirs(self.project)
        write_text(os.path.join(self.template, "instructions", "global.md"), u"Rules\n")
        write_text(
            os.path.join(self.template, "configs", "codex", "config.toml.template"),
            u"developer_instructions = '''{{GLOBAL_INSTRUCTIONS}}'''\n",
        )
        write_text(
            os.path.join(self.template, "configs", "codex", "research.config.toml"),
            u"web_search = 'live'\n",
        )
        write_text(os.path.join(self.template, "configs", "claude", "settings.json"), u"{}\n")
        write_text(os.path.join(self.template, "configs", "antigravity", "settings.json"), u"{}\n")
        write_text(os.path.join(self.template, "project", "AGENTS.md"), u"Project rules\n")
        write_text(os.path.join(self.template, "project", "CLAUDE.md"), u"@AGENTS.md\n")
        write_text(os.path.join(self.template, "skills", "sample", "SKILL.md"), u"# Sample\n")
        self.adapter = imp.load_source("python2_toolbox_adapter", ADAPTER_PATH)

    def tearDown(self):
        """Remove the isolated fixture tree.

        Args:
            None.

        Returns:
            None: All test files are removed.

        Raises:
            None.
        """
        shutil.rmtree(self.root)

    def test_preparation_discovers_conflict_without_writing(self):
        """Catch fallback preparation mutating a conflict before consent.

        Args:
            None.

        Returns:
            None: Assertions verify the conflict and unchanged content.

        Raises:
            IOError: If the fixture cannot be read.
        """
        conflict = os.path.join(self.home, ".codex", "config.toml")
        write_text(conflict, u"existing\n")
        preparation = self.adapter.prepare(
            "setup-agents-codex", {"profiles": []}, self.template, self.home
        )
        self.assertEqual(preparation["conflicts"], [conflict])
        with io.open(conflict, "r", encoding="utf-8") as source:
            self.assertEqual(source.read(), u"existing\n")

    def test_questions_and_project_run_use_typed_answers(self):
        """Catch fallback routing or apply ignoring explicit project answers.

        Args:
            None.

        Returns:
            None: Assertions verify question type and installed project file.

        Raises:
            IOError: If the project fixture cannot be written or read.
        """
        response = self.adapter.handle_request(
            protocol_request("setup-agents-codex", "questions", {}),
            self.template,
            self.home,
        )
        self.assertEqual(response["question"]["id"], "profiles")
        answers = {
            "target_directory": self.project,
            "agent_formats": ["codex"],
            "ignore_agent_files": False,
            "ignore_superpowers": False,
        }
        response = self.adapter.handle_request(
            protocol_request("setup-agents-project", "run", answers),
            self.template,
            self.home,
            output_function=lambda message: None,
        )
        self.assertEqual(response, {"status": "ready"})
        with io.open(os.path.join(self.project, "AGENTS.md"), "r", encoding="utf-8") as source:
            self.assertEqual(source.read(), u"Project rules\n")


if __name__ == "__main__":
    unittest.main()
