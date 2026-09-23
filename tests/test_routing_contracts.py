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

        for display in ("plot", "graph", "chart", "axes-based data display"):
            self.assertIn(display, instructions)
        for containing_task in ("coding", "debugging", "research", "writing"):
            self.assertIn(containing_task, instructions)
        for excluded_visual in (
            "conceptual illustration",
            "architecture diagram",
            "system diagram",
            "data-flow diagram",
        ):
            self.assertIn(excluded_visual, instructions)
        self.assertIn("explicit user request", instructions)
        self.assertIn("overrides", instructions)

    def test_plot_skill_excludes_non_plot_figures_and_preserves_override(self) -> None:
        """Prevent the plotting skill from claiming diagrams or user overrides."""
        skill = read("skills/scientific-plot-maker/SKILL.md")

        self.assertIn("axes-based", skill)
        self.assertIn("results visualization", skill)
        self.assertIn("conceptual illustration", skill)
        self.assertIn("architecture", skill)
        self.assertIn("data-flow diagram", skill)
        self.assertIn("explicit user request", skill)
        self.assertIn("overrides", skill)

    def test_scribe_routes_paper_visuals_by_visual_type(self) -> None:
        """Send manuscript charts to plotting and diagrams to figure creation."""
        skill = read("skills/scribe/SKILL.md")

        self.assertIn("scientific-plot-maker", skill)
        self.assertIn("create-publication-figures", skill)
        self.assertIn("results visualization", skill)
        self.assertIn("architecture", skill)
        self.assertIn("data-flow", skill)
        self.assertIn("explicit user request", skill)
        self.assertIn("overrides", skill)


if __name__ == "__main__":
    unittest.main()
