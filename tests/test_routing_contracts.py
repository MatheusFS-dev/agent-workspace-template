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


if __name__ == "__main__":
    unittest.main()
