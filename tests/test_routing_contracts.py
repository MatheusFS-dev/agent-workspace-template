"""Contract tests for routing plots and non-plot scientific figures."""

import json
from pathlib import Path
import subprocess
import sys
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROMPT_REMINDER = (
    "Follow the global instructions. Classify the request, apply its gate: "
    "code/debug=Superpowers, even small edits. "
    "Plots=Superpowers+scientific-plot-maker. Research=no Superpowers. "
    "Papers=scribe. README=readmaker. Docs=docs/ folder. "
    "Only if asked: ingest=ingest-context, handoff=session-handoff."
)


def read(relative_path: str) -> str:
    """Return one repository policy file as lowercase text.

    Args:
        relative_path: Repository-relative path to the policy file.

    Returns:
        Lowercase file contents for case-insensitive contract checks.
    """
    return (ROOT / relative_path).read_text(encoding="utf-8").lower()


class RoutingContractTest(unittest.TestCase):
    """Keep plot routing distinct from conceptual-figure routing."""

    def test_repeated_misunderstanding_gate_requests_clarification(self) -> None:
        """Stop repeated wrong-scope answers until the user's intent is clear."""
        instructions = read("instructions/global.md")

        self.assertIn("## repeated misunderstanding gate", instructions)
        self.assertIn("after an earlier correction", instructions)
        self.assertIn("a first correction alone", instructions)
        self.assertIn("apologize directly", instructions)
        self.assertIn("reread the relevant user request, corrections, and references", instructions)
        self.assertIn("treat prior assistant interpretations as hypotheses", instructions)
        self.assertIn("simple example outputs", instructions)
        self.assertIn("resume when the answers resolve the uncertainty", instructions)
        self.assertIn("do not require an extra confirmation", instructions)

    def test_global_gate_routes_explicit_context_handoffs_to_the_skill(self) -> None:
        """Route only explicit session preservation and restoration requests."""
        instructions = read("instructions/global.md")

        self.assertIn("## session handoff gate", instructions)
        self.assertIn("`session-handoff` skill", instructions)
        self.assertIn("handoff context", instructions)
        self.assertIn("save, checkpoint, or preserve session context", instructions)
        self.assertIn("load, resume, or restore session context", instructions)
        self.assertIn("ordinary progress updates or summaries", instructions)

    def test_global_gate_routes_only_axes_based_data_displays_to_plotting(self) -> None:
        """Route nested plots while excluding conceptual diagrams."""
        instructions = read("instructions/global.md")

        self.assertIn(
            "`scientific-plot-maker` skill when creating, modifying, styling, or "
            "reviewing plots, graphs, charts, axes-based data displays, or results "
            "visualizations",
            instructions,
        )
        self.assertIn(
            "plotting is nested inside a coding, debugging, research, or writing task",
            instructions,
        )
        self.assertIn(
            "do not use the plotting skill for conceptual illustrations, architecture "
            "diagrams, system diagrams, or data-flow diagrams",
            instructions,
        )
        self.assertIn(
            "explicit user request for another skill or method overrides this default "
            "routing",
            instructions,
        )

    def test_plot_skill_excludes_non_plot_figures_and_preserves_override(self) -> None:
        """Prevent the plotting skill from claiming diagrams or user overrides."""
        skill = read("skills/scientific-plot-maker/SKILL.md")

        self.assertIn(
            "use this skill for axes-based data displays and results visualizations",
            skill,
        )
        self.assertIn(
            "do not use it for conceptual illustrations, architecture or system "
            "diagrams, or data-flow diagrams",
            skill,
        )
        self.assertIn(
            "explicit user request for another skill or method overrides this default "
            "routing",
            skill,
        )

    def test_scribe_routes_paper_visuals_by_visual_type(self) -> None:
        """Send manuscript charts to plotting and diagrams to figure creation."""
        skill = read("skills/scribe/SKILL.md")

        self.assertIn(
            "route plots, graphs, charts, axes-based data displays, and results "
            "visualizations to `scientific-plot-maker`",
            skill,
        )
        self.assertIn(
            "route non-plot paper visuals, including conceptual illustrations, "
            "architecture or system diagrams, and data-flow diagrams, to "
            "`create-publication-figures-latex`",
            skill,
        )
        self.assertIn(
            "explicit user request for another skill or method overrides this default "
            "routing",
            skill,
        )

    def test_scribe_coloring_marks_only_exact_revised_spans(self) -> None:
        """Keep unchanged manuscript text outside blue revision markup."""
        skill = read("skills/scribe/SKILL.md")
        style_guide = read("skills/scribe/references/scribe-style-guide.md")
        response_workflow = read("skills/scribe/references/workflows/responding-to-reviewers.md")
        response_template = read("skills/scribe/assets/response-letter.tex")

        self.assertIn("only the exact modified or added span", skill)
        self.assertIn("never wrap an entire paragraph in blue", skill)
        self.assertIn("keep unchanged text outside blue revision markup", style_guide)
        self.assertIn("never wrap an entire paragraph in blue", style_guide)
        self.assertIn("only the exact changed or added span in blue", response_workflow)
        self.assertIn("leave retained context uncolored", response_workflow)
        self.assertNotIn(
            r"\newenvironment{revisionexcerpt}{\begingroup\color{blue}}{\endgroup}",
            response_template,
        )


class PromptReminderContractTest(unittest.TestCase):
    """Keep the per-prompt reminder aligned with the global gates."""

    def test_coding_gate_covers_small_edits(self) -> None:
        """Require Superpowers for small coding edits as well."""
        instructions = read("instructions/global.md")

        self.assertIn(
            "use the superpowers plugin and its applicable skills for coding tasks, "
            "including small edits, unless the user explicitly requests otherwise.",
            instructions,
        )

    def test_claude_settings_install_the_prompt_reminder_hook(self) -> None:
        """Install the reminder as a Claude UserPromptSubmit command hook."""
        settings = json.loads(
            (ROOT / "configs" / "claude" / "settings.json").read_text(encoding="utf-8")
        )

        entries = settings["hooks"]["UserPromptSubmit"]
        commands = [
            handler["command"] for entry in entries for handler in entry["hooks"]
        ]
        self.assertEqual(len(commands), 1)
        self.assertIn(PROMPT_REMINDER, commands[0])

    def test_codex_template_installs_the_prompt_reminder_hook(self) -> None:
        """Install the same reminder as a Codex UserPromptSubmit command hook."""
        template = (ROOT / "configs" / "codex" / "config.toml.template").read_text(
            encoding="utf-8"
        )

        config = tomllib.loads(template)

        handlers = [
            handler
            for entry in config["hooks"]["UserPromptSubmit"]
            for handler in entry["hooks"]
        ]
        self.assertEqual(len(handlers), 1)
        self.assertEqual(handlers[0]["type"], "command")
        self.assertIn(PROMPT_REMINDER, handlers[0]["command"])
        self.assertIn(PROMPT_REMINDER, handlers[0]["command_windows"])

    def test_antigravity_hook_template_runs_the_reminder_script(self) -> None:
        """Register the reminder script on the PreInvocation event."""
        hooks = json.loads(
            (ROOT / "configs" / "antigravity" / "hooks.json").read_text(encoding="utf-8")
        )

        self.assertEqual(list(hooks), ["global-instructions-reminder"])
        handlers = hooks["global-instructions-reminder"]["PreInvocation"]
        self.assertEqual(len(handlers), 1)
        self.assertEqual(handlers[0]["type"], "command")
        self.assertIn("prompt_reminder.py", handlers[0]["command"])

    def run_reminder_script(self, stdin_text: str) -> subprocess.CompletedProcess:
        """Run the Antigravity reminder script with one stdin payload.

        Args:
            stdin_text: Raw text sent to the hook on standard input.

        Returns:
            subprocess.CompletedProcess: Captured exit code and output.
        """
        return subprocess.run(
            [sys.executable, "-I", str(ROOT / "configs" / "antigravity" / "prompt_reminder.py")],
            input=stdin_text,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

    def test_antigravity_script_injects_once_per_user_prompt(self) -> None:
        """Inject on the first model call of a prompt and stay silent afterwards."""
        first = self.run_reminder_script(json.dumps({"invocationNum": 0}))
        later = self.run_reminder_script(json.dumps({"invocationNum": 1}))

        self.assertEqual(first.returncode, 0)
        self.assertEqual(
            json.loads(first.stdout),
            {"injectSteps": [{"ephemeralMessage": PROMPT_REMINDER}]},
        )
        self.assertEqual(later.returncode, 0)
        self.assertEqual(later.stdout, "")

    def test_antigravity_script_ignores_unreadable_input(self) -> None:
        """Never break an Antigravity turn because of malformed hook input."""
        for stdin_text in ("", "{not json", "[]", json.dumps({"other": 1})):
            result = self.run_reminder_script(stdin_text)

            self.assertEqual(result.returncode, 0, stdin_text)
            self.assertEqual(result.stdout, "", stdin_text)

    def test_reminder_is_agent_neutral(self) -> None:
        """Avoid naming a specific agent or instruction file in the reminder."""
        reminder = PROMPT_REMINDER.lower()

        for name in ("claude", "codex", "gemini", "antigravity", "opencode", ".md"):
            self.assertNotIn(name, reminder)


if __name__ == "__main__":
    unittest.main()
