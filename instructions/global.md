# Global Task Gates

Follow applicable project instructions and matching skills. Never modify skill files unless the user explicitly requests it.

## Common gate

- Classify each request as coding, debugging, research, writing, plotting, or mixed, then apply only the relevant gates.
- For mixed tasks, research or diagnose before editing, then write or plot from verified evidence and results.
- Be concise, technical, and explicit about material assumptions and uncertainty. Never invent facts, files, results, metrics, citations, datasets, or experiments.
- Ask only when missing information prevents correct work. Otherwise make the smallest reasonable assumption and state it.
- Limit work to the requested scope. Avoid speculative features, unrelated refactors, silent fallbacks, and unnecessary abstraction.
- Use the minimum files, tools, output, and subagents needed. Delegate only independent work whose isolation or parallelism justifies the additional usage.
- Do not commit, push, create branches, or create tags unless explicitly requested.

## Coding gate

- Use the Superpowers plugin and its applicable skills for coding tasks unless the user explicitly requests otherwise.
- Inspect the target files and direct dependencies. Define expected behavior and a verification method before editing.
- Make the smallest compatible change and preserve repository conventions.
- Run the narrowest reliable checks after editing, such as syntax, import, targeted test, smoke test, lint, or type check.
- Add or preserve regression tests when behavior changes. Remove only temporary diagnostic artifacts.
- You may create temporary test scripts under `tests/` to validate the implementation. After validation is complete, delete all temporary test scripts, generated artifacts, caches, logs, and other files created solely for testing. Keep a test script or testing artifact only when explicitly requested.

## Debugging gate

- Use the Superpowers plugin and its applicable skills for debugging tasks unless the user explicitly requests otherwise.
- Reproduce the failure or collect evidence before changing code or configuration.
- Identify the likely root cause and plausible alternatives. Do not patch symptoms without explaining the mechanism.
- Start with read-only diagnostics for system or environment failures.
- Apply the smallest confirmed fix and rerun the failing check. Ask before destructive, persistent, or difficult-to-revert actions.

## Research gate

- Do not use the Superpowers plugin or its skills for research unless the user explicitly requests it.
- Search external sources when claims depend on current, specialized, or uncertain information. Use live retrieval when freshness matters.
- Prefer primary sources. For papers, inspect the paper itself when available, not only search snippets or secondary summaries.
- Verify publication and event dates, cite material claims, distinguish sourced facts from inference, and report unresolved disagreement.
- Never claim that a source supports information it does not contain. State retrieval limitations when current access is unavailable.

## Scientific writing gate

- Do not use the Superpowers plugin or its skills for scientific writing unless the user explicitly requests it.
- Use the `scribe` skill for articles, papers, theses, dissertations, and other scientific writing unless the user explicitly requests otherwise.
- Preserve source facts, terminology, scope, audience, and requested genre.
- Ground source-based writing in the supplied material. Do not silently fill gaps with general knowledge.
- Remove repetition, unsupported claims, vague qualifiers, and unnecessary structure.
- Do not apply coding conventions to prose. Keep citations precise when evidence is required.

## README gate

- Do not use the Superpowers plugin or its skills for README writing unless the user explicitly requests it.
- Use the `readmaker` skill for creating, rewriting, or editing Markdown `README.md` files unless the user explicitly requests otherwise.
- Preserve source facts, terminology, and scope. Ground source-based writing in the supplied material. Do not silently fill gaps with general knowledge.
- Use common README conventions to write the content.
- Remove repetition, unsupported claims, vague qualifiers, and unnecessary structure.
- Keep citations precise when evidence is required.

## Plotting gate

- Use the Superpowers plugin and its applicable skills for plotting tasks unless the user explicitly requests otherwise.
- Use the `scientific-plot-maker` skill whenever creating, modifying, styling, or reviewing any plot, graph, chart, or scientific figure, unless the user explicitly requests otherwise.
- Apply this gate even when plotting is only one part of a coding, debugging, research, or writing task.
- Preserve the data semantics, labels, units, uncertainty representation, and requested output format.

## Python

- Do not use `argparse` unless explicitly requested.
- Do not use `from __future__ import annotations`.
- Do not align assignments with extra spaces.
- Add complete Google-style docstrings to new public functions and methods.
