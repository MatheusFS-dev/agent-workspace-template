# Coding Mode

Use this mode for implementation, debugging, refactoring, scripts, tests, data processing, ML pipelines, and repository maintenance.

This file is the compact always-loaded coding contract. Detailed examples are retrieval-gated by risk category to reduce repeated context cost while preserving behavior-shaping guidance.

## Before editing

1. Identify the requested behavior and the smallest relevant file set.
2. State assumptions only when they affect implementation correctness.
3. Before implementing:
    - State assumptions explicitly.
    - If something is unclear or underspecified, ask targeted questions before coding.
    - If there are multiple plausible interpretations, present them instead of picking one silently.
    - If a simpler approach exists, say so.
    - Push back on unnecessary complexity when warranted.
    - Stop and name what is confusing instead of guessing.
4. For multi-step work, use `1. [Step] -> verify: [check]`.
    Examples:
        - "Fix the bug" -> reproduce it with a test or concrete failure case, then make it pass.
        - "Add validation" -> define invalid inputs, add checks, then verify behavior.
        - "Refactor X" -> preserve behavior, then verify before and after.
5. Inspect only target files and directly relevant dependencies.

## Implementation behavior

- Make surgical changes only.
- Do not refactor unrelated code.
- Do not add speculative features, broad configurability, hidden fallback behavior, or silent recovery.
- Prefer explicit errors over implicit defaults.
- Match the repository style.
- Keep functions small and composable.
- Remove only unused imports or code introduced by the change.
- Comment intent, assumptions, rationale, and edge cases, not obvious mechanics.
- If the solution is longer or more abstract than necessary, simplify it.
- Use this test: would a senior engineer consider this overcomplicated? If yes, rewrite it more simply.

## Testing the implementation

Unless the user explicitly requests otherwise, follow this rule:

- After implementation, add targeted tests to verify the change inside the project `tests/` folder.
- After verification passed, delete these tests. They should be used only for agent-side verification.

## Verification

After Python code edits, run:

```bash
python .agent/scripts/agent_check.py
```

Use the narrowest reliable project check after the agent check, such as syntax/import check, targeted unit test, smoke test, integration test, or full suite.

Report verification as:

```text
Verification:
- command: ...
- result: passed | failed | not run
- reason if not run: ...
```

If verification fails, report the exact failure, identify whether it is caused by the change, environment, missing dependency, missing data, or pre-existing issue, then make the smallest confirmed correction.

## Troubleshooting

For drivers, CUDA, package conflicts, Python environments, OS issues, dependency errors, TensorFlow, PyTorch, or similar failures, read `.agent/workflows/debugging.md` first. Diagnose before proposing fixes.

## Risk-specific examples

Do not load all examples by default. Use targeted search first:

```bash
python .agent/scripts/search_reference.py .agent/modes/coding-example-cards.md hidden assumptions
python .agent/scripts/search_reference.py .agent/modes/coding-example-cards.md drive-by refactoring
python .agent/scripts/search_reference.py .agent/modes/coding-example-cards.md test-first verification
```

Use the matching `.agent/modes/examples/<risk>.md` file only when:

- the compact card is insufficient,
- the user asks for examples,
- the same failure mode remains ambiguous after reading the card,
- a complex task has high risk of unwanted behavior.

## Example risk index

- Ambiguous feature scope -> Hidden Assumptions.
- Vague speed, quality, or performance request -> Multiple Interpretations.
- Simple feature request -> Over-abstraction.
- Bug fix or crash fix -> Drive-by Refactoring.
- Small local patch -> Style Drift.
- Vague system-level fix -> Vague vs. Verifiable.
- Multi-step feature -> Multi-Step Verification.
- Reported failure, edge case, or regression -> Test-First Verification.
