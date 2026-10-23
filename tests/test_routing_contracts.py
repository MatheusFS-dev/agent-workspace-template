"""Contract tests for routing plots and non-plot scientific figures."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


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
            "`create-publication-figures`",
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


if __name__ == "__main__":
    unittest.main()
