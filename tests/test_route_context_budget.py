"""Validate and report route-context budget estimates for key prompt classes.

This test module exercises ``.agent/scripts/route_context.py --stats`` with a
small matrix of representative prompts. For each prompt, it parses the router's
reported ``TOTAL_CONTEXT_RISK`` upper bound, prints a compact report line with
the measured value and allowed budget, and fails if the route grows beyond its
configured ceiling.

The purpose of the test is not to lock token counts to exact values. Instead,
it provides a human-readable budget report during test runs while enforcing
loose upper bounds that catch accidental route explosions.
"""

from pathlib import Path
import re
import subprocess
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parent.parent
ROUTER_PATH = REPO_ROOT / ".agent" / "scripts" / "route_context.py"
TOTAL_CONTEXT_RISK_PATTERN = re.compile(
    r"^TOTAL_CONTEXT_RISK approx_tokens<=([0-9]+)$",
    re.MULTILINE,
)


def run_route_context_with_stats(request: str) -> str:
    """Run the router with stats enabled and return its output.

    Args:
        request: User request text passed as a single argument to the router.
            The function always enables ``--stats`` so the router prints token
            estimates. Using a single argument preserves the original wording
            that drives route selection and avoids shell-splitting changes.

    Returns:
        str: The router standard output decoded as text.

    Raises:
        subprocess.CalledProcessError: If the router exits with a non-zero
            status while processing the supplied request.

    Examples:
        >>> "TOTAL_CONTEXT_RISK" in run_route_context_with_stats("fix typo in README")
        True
    """
    completed_process = subprocess.run(
        [sys.executable, str(ROUTER_PATH), "--stats", request],
        check=True,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    return completed_process.stdout


def parse_total_context_risk(route_output: str) -> int:
    """Extract the total context-risk upper bound from router output.

    Args:
        route_output: Full text emitted by ``route_context.py --stats``. The
            parser accepts only the existing ``approx_tokens<=N`` form because
            this test is intended to fail fast if the router stops reporting a
            bounded total risk estimate.

    Returns:
        int: The parsed upper-bound token estimate reported for
        ``TOTAL_CONTEXT_RISK``.

    Raises:
        AssertionError: If the expected ``TOTAL_CONTEXT_RISK approx_tokens<=N``
            line is missing or does not match the supported format.

    Examples:
        >>> parse_total_context_risk("TOTAL_CONTEXT_RISK approx_tokens<=123\\n")
        123
    """
    match = TOTAL_CONTEXT_RISK_PATTERN.search(route_output)
    if match is None:
        raise AssertionError(
            "Expected a 'TOTAL_CONTEXT_RISK approx_tokens<=N' line in router "
            f"output, but got:\n{route_output}"
        )
    return int(match.group(1))


def format_budget_report_line(
    scenario_name: str,
    total_context_risk: int,
    budget: int,
) -> str:
    """Build a human-readable report line for one routing scenario.

    Args:
        scenario_name: Descriptive label for the prompt category being tested.
            This text is shown verbatim in the printed report so the output can
            be scanned quickly during local debugging or CI log review.
        total_context_risk: Parsed ``TOTAL_CONTEXT_RISK`` upper bound reported
            by the router for the scenario. Larger values indicate the router
            would load more context for that prompt.
        budget: Maximum allowed token estimate for the scenario. If the
            measured risk is above this value, the corresponding assertion in
            the test fails.

    Returns:
        str: A compact status line containing the scenario name, measured risk,
        allowed budget, and remaining headroom.

    Raises:
        None.

    Examples:
        >>> format_budget_report_line("repo analysis", 1768, 3000)
        '[route-budget] repo analysis: risk=1768 budget=3000 headroom=1232'
    """
    headroom = budget - total_context_risk
    return (
        f"[route-budget] {scenario_name}: risk={total_context_risk} "
        f"budget={budget} headroom={headroom}"
    )


class RouteContextBudgetTests(unittest.TestCase):
    """Verify representative router scenarios stay within budget ceilings."""

    def test_representative_routes_stay_within_context_budgets(self) -> None:
        """Check route-cost ceilings for representative prompt categories.

        Args:
            None.

        Returns:
            None.

        Raises:
            AssertionError: If any prompt exceeds its configured budget or the
                router stops emitting a parseable bounded total.
        """
        print("\nRoute-context budget report:")

        # These prompts mirror the repository's documented routing categories.
        # Upper bounds stay intentionally loose so minor wording edits in routed
        # files do not cause churn, while still catching accidental route growth.
        test_cases = [
            ("simple typo edit", "fix typo in README", 3500),
            (
                "normal coding task",
                "implement a normal coding task to add a small helper function and unit test",
                4500,
            ),
            ("repo analysis", "analyze this repo token usage", 3000),
            (
                "paper-writing task",
                "write reviewer response about the training pipeline",
                4500,
            ),
            ("plotting task", "create a script to plot a histogram", 4500),
            (
                "coding task with risk cards",
                "add feature, make it faster, robust, fix duplicate failure",
                7000,
            ),
            (
                "project-map refresh",
                "refresh project architecture context",
                3500,
            ),
        ]

        for scenario_name, prompt, budget in test_cases:
            with self.subTest(scenario=scenario_name):
                route_output = run_route_context_with_stats(prompt)
                total_context_risk = parse_total_context_risk(route_output)
                print(format_budget_report_line(scenario_name, total_context_risk, budget))
                self.assertLessEqual(
                    total_context_risk,
                    budget,
                    msg=(
                        f"Scenario '{scenario_name}' exceeded its budget of "
                        f"{budget} tokens with reported risk "
                        f"{total_context_risk}.\nRouter output:\n{route_output}"
                    ),
                )


if __name__ == "__main__":
    raise SystemExit(unittest.main())
