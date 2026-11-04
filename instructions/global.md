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

## Repeated misunderstanding gate

- Activate when the user indicates that the assistant still misunderstands the same goal or scope after an earlier correction, including statements such as "that is still not what I mean." A first correction alone does not trigger this gate: incorporate it and correct course normally.
- Stop the current solution and apologize directly in the user's language, for example: "Sorry, I'm not following what you want."
- Reread the relevant user request, corrections, and references. Inspect available evidence when needed. Treat prior assistant interpretations as hypotheses, not established user intent. Identify the problem the user wants fixed and where the previous answer diverged.
- Briefly state the current understanding and ask focused questions only about material uncertainty, as in Plan Mode. Give simple example outputs for plausible answers so the user can recognize the intended deliverable, such as a one-line message versus a one-line implementation plan. Do not repeat questions already answered.
- While the uncertainty remains, pause substantive work that depends on it. Read-only investigation may continue. Resume when the answers resolve the uncertainty, and do not require an extra confirmation. If a material ambiguity remains, ask a follow-up question.

## Coding gate

- Use the Superpowers plugin and its applicable skills for coding tasks unless the user explicitly requests otherwise.
- Inspect the target files and direct dependencies. Define expected behavior and a verification method before editing.
- Make the smallest compatible change and preserve repository conventions.
- Run the narrowest reliable checks after editing, such as syntax, import, targeted test, smoke test, lint, or type check.
- Add or preserve regression tests when behavior changes. Remove only temporary diagnostic artifacts.
- You may create temporary test scripts under `tests/` to validate the implementation. After validation is complete, delete all temporary test scripts, generated artifacts, caches, logs, and other files created solely for testing. Keep a test script or testing artifact only when explicitly requested.
- Every program must report progress. Never leave a running task silent. Print the stage before it starts, for example "Loading dataset" or "Training model". When the work is measurable, also show a progress bar, ETA, elapsed time, and throughput (use `tqdm` in Python).
- Avoid semicolons and em dashes in session responses.

### Scripts subgate

- In scripts (Python, bash, etc.), avoid command-line arguments. Prefer interactive prompts. Explain each prompt question briefly and show the available options when there are any. Keep prompts concise.
- The only argument added by default is `--dry-run`, and only when it makes sense for the script.
- Follow these script rules unless the user requests otherwise.

### Python subgate

- Prioritize `uv` for the virtual environment unless the user requests otherwise. Provide `pyproject.toml` and `uv.lock`.
- Use only `uv sync` to create and update the environment. Do not create sub-venvs, do not use `uv run`, and do not add `uv` arguments to commands or scripts.
- Default workflow: activate the venv, then run with `python3` normally.
- Do not implement any other `uv` usage unless the user explicitly requests it.
- Do not use `argparse` unless explicitly requested.
- Do not use `from __future__ import annotations`.
- Do not align assignments with extra spaces.
- Add complete Google-style docstrings to new public functions and methods.
- Include an `Examples:` section only when it clarifies non-obvious usage. Use concrete input with observable expected output; omit call-only examples and examples containing undefined placeholders.

#### ML training subgate

- Assume training can crash at any moment. Save checkpoints and make the script resume from the latest checkpoint on the next run.
- Avoid config files such as `.toml` for training parameters. Keep parameters directly in the Python script, inside a Config section formatted exactly like this:

```python
# ---------------------------------------------------------------------------- #
#                                    Config                                    #
# ---------------------------------------------------------------------------- #

# ADD CONFIGS HERE

# ---------------------------------------------------------------------------- #
```

- Exceptions: the user requests otherwise, there is too much redundancy across scripts, or parameters must be standardized across multiple tests.
- Use `os.environ` to set up GPU memory growth and the device. Default to GPU `cuda:0`.
- Print one line per epoch with the epoch index, the metrics (such as loss and validation score), and the epoch duration. Also show a per-batch progress bar with ETA.
- Follow these rules unless the user requests otherwise.

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

- Use the Superpowers plugin and the `scientific-plot-maker` skill when creating, modifying, styling, or reviewing plots, graphs, charts, axes-based data displays, or results visualizations.
- Apply this routing when plotting is nested inside a coding, debugging, research, or writing task.
- Do not use the plotting skill for conceptual illustrations, architecture diagrams, system diagrams, or data-flow diagrams.
- An explicit user request for another skill or method overrides this default routing.
- Preserve the data semantics, labels, units, uncertainty representation, and requested output format.

## Ingest gate

- Activate this gate only when the user explicitly asks to ingest, index, import,
  or prepare material as reusable agent context.
- Use the `ingest-context` skill for ingestion of the material.
- Never store generated ingestion artifacts elsewhere unless explicitly requested.
- Preserve source provenance and distinguish source content from generated
  summaries or interpretation.
- Never recursively load all of `.agents/context/` into context. Retrieve from
  the catalog, then the package overview, then only the required detailed files.

## Session handoff gate

- Activate this gate only when the user says `handoff context` or explicitly asks to save, checkpoint, or preserve session context; load, resume, or restore session context.
- Use the `session-handoff` skill to save or restore the portable task handoff.
- Do not activate this gate for ordinary progress updates or summaries.

## Repository docs gate

- Applies to repository documentation in Markdown (`.md`) other than `README.md` files, which follow the README gate.
- Put all docs under a `docs/` folder by default. Keep it organized with easy to understand filenames and subdirectories.
- When the user asks for a report after a task, save it under `docs/reports/`. Keep it concise and easy to understand.
- Start each report with a title, then the date and timestamp, then the content.
- Use simple language. A layperson, non-expert, or non-programmer must be able to understand what was done, what was tested, and the results.
- If the user asks for a detailed or technical report, explain the code step by step and include a worked example that "runs" through each step.
- Papers, `.tex` files, and PDF reports are not covered by this gate. They follow the scientific writing gate and the `scribe` skill.
- Follow these rules unless the user requests otherwise.
