#!/usr/bin/env python3
"""Regression tests for route context selection."""

from pathlib import Path
import subprocess
import sys
import unittest


SCRIPT_PATH = Path(__file__).with_name("route_context.py")


def run_route_context(request: str) -> str:
    """Run the route-context script and capture its standard output.

    Args:
        request: User task text routed through the script. The request is passed
            as a single argument so shell parsing does not alter the wording
            that drives route selection.

    Returns:
        The script standard output as decoded UTF-8 text.

    Raises:
        subprocess.CalledProcessError: If the routing script exits with a
            non-zero status.

    Examples:
        >>> "READ AGENTS.md" in run_route_context("fix typo in README")
        True
    """
    completed = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), request],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout


class RouteContextRegressionTests(unittest.TestCase):
    """Verify router behavior for known high-risk routing scenarios."""

    def test_easy_task_routes_only_easy_context(self) -> None:
        """Verify trivial edits use Easy Task Mode.

        Args:
            None.

        Returns:
            None.

        Raises:
            AssertionError: If the router loads non-easy-task context.
        """
        output = run_route_context("fix typo in README")
        self.assertIn("READ AGENTS.md", output)
        self.assertIn("READ .agent/modes/easy-task.md", output)
        self.assertNotIn(".agent/modes/coding.md", output)
        self.assertNotIn(".agent/context/project-map.md", output)

    def test_troubleshooting_without_edit_is_exclusive(self) -> None:
        """Verify troubleshooting stays exclusive without code-edit intent.

        Args:
            None.

        Returns:
            None.

        Raises:
            AssertionError: If coding mode is loaded for a pure debugging task.
        """
        output = run_route_context("debug CUDA import error")
        self.assertIn("READ .agent/workflows/debugging.md", output)
        self.assertNotIn(".agent/modes/coding.md", output)

    def test_paper_writing_dominates_training_terms(self) -> None:
        """Verify paper-writing terms suppress coding without edit intent.

        Args:
            None.

        Returns:
            None.

        Raises:
            AssertionError: If coding mode leaks into a writing request.
        """
        output = run_route_context("write reviewer response about the training pipeline")
        self.assertIn("READ .agent/modes/paper-writing.md", output)
        self.assertIn("READ .agent/skills/scribe/SKILL.md", output)
        self.assertNotIn(".agent/modes/coding.md", output)

    def test_repo_analysis_uses_project_map_not_coding(self) -> None:
        """Verify repository-analysis requests load the project map only.

        Args:
            None.

        Returns:
            None.

        Raises:
            AssertionError: If coding mode is loaded for repository analysis.
        """
        output = run_route_context("analyze this repo token usage")
        self.assertIn("READ .agent/context/project-map.md", output)
        self.assertNotIn(".agent/modes/coding.md", output)

    def test_generic_architecture_terms_do_not_load_project_map(self) -> None:
        """Verify non-repository architecture wording avoids project-map context.

        Args:
            None.

        Returns:
            None.

        Raises:
            AssertionError: If generic architecture language still triggers
                repository-structure routing.
        """
        prompts = [
            "Rewrite this paragraph about the neural network architecture.",
            "Explain the model architecture in the paper.",
            "Improve this system architecture description.",
            "Compare PointNet++ and DGCNN architectures.",
        ]

        for prompt in prompts:
            with self.subTest(prompt=prompt):
                output = run_route_context(prompt)
                self.assertNotIn(".agent/context/project-map.md", output)

    def test_repository_architecture_phrases_load_project_map(self) -> None:
        """Verify repository-architecture wording still loads the project map.

        Args:
            None.

        Returns:
            None.

        Raises:
            AssertionError: If repository-organization prompts stop reading
                the project-map context.
        """
        prompts = [
            "Explain the project architecture.",
            "Review the repository architecture for this repo.",
            "Where should this file go?",
            "Decide the package layout for this module.",
        ]

        for prompt in prompts:
            with self.subTest(prompt=prompt):
                output = run_route_context(prompt)
                self.assertIn("READ .agent/context/project-map.md", output)

    def test_project_map_refresh_reads_regenerated_map(self) -> None:
        """Verify refresh requests read the regenerated project map.

        Args:
            None.

        Returns:
            None.

        Raises:
            AssertionError: If the refresh command is emitted without reading
                the updated project map afterward.
        """
        output = run_route_context("Update the project map.")
        self.assertIn("RUN python3 .agent/scripts/update_project_map.py", output)
        self.assertIn("READ .agent/context/project-map.md", output)
        self.assertNotIn("READ .agent/index.yaml", output)

    def test_plot_script_uses_coding_and_plotting(self) -> None:
        """Verify mixed plotting implementation requests load both contexts.

        Args:
            None.

        Returns:
            None.

        Raises:
            AssertionError: If required coding or plotting context is missing.
        """
        output = run_route_context("create a script to plot a histogram")
        self.assertIn("READ .agent/modes/coding.md", output)
        self.assertIn("READ .agent/rules/plotting-style.md", output)
        self.assertIn("READ .agent/skills/scientific-plot-maker/SKILL.md", output)

    def test_full_example_routes_specific_file(self) -> None:
        """Verify full-example requests load specific risk files only.

        Args:
            None.

        Returns:
            None.

        Raises:
            AssertionError: If the deprecated monolithic file is loaded.
        """
        output = run_route_context("fix duplicate failure and show full example")
        self.assertIn("READ .agent/modes/examples/test-first-verification.md", output)
        self.assertNotIn(".agent/modes/coding-full-examples.md", output)

    def test_risk_searches_are_capped(self) -> None:
        """Verify compact-card search routing stays within the configured cap.

        Args:
            None.

        Returns:
            None.

        Raises:
            AssertionError: If more than two search commands are emitted.
        """
        output = run_route_context("add feature, make it faster, robust, fix duplicate failure")
        search_lines = [
            line for line in output.splitlines()
            if "RUN python3 .agent/scripts/search_reference.py" in line
        ]
        self.assertLessEqual(len(search_lines), 2)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
