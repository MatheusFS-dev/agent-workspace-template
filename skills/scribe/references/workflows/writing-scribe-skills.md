# Writing Scribe Skills

> **Supporting module:** This file belongs to the single `scribe-superpowers` skill. It is not a separately installable or discoverable skill. Load it only through the routing rules in the root `SKILL.md`.


## Overview

Create and modify Scribe workflow modules through behavioral RED-GREEN-REFACTOR. Test what an agent does under writing pressure, write the minimum guidance that corrects observed failures, and close rationalization loopholes before deployment.

**Core principle:** If an agent was not observed failing without the skill, there is no evidence that the skill teaches the needed behavior.

## What a Scribe Skill Is

A Scribe workflow module is a reusable process, technique, pattern, or reference for academic-writing work.

It is not:

- a narrative about one manuscript,
- a project-specific terminology list,
- a venue template that belongs in the project,
- a mechanical rule better enforced by a linter,
- an untested collection of general writing advice.

## Iron Law

```text
NO NEW OR MODIFIED SCRIBE SKILL WITHOUT A FAILING BEHAVIORAL SCENARIO FIRST
```

Writing the skill before testing means the baseline is unknown. Remove the untested change and start from the scenario.

## Skill Types

### Discipline-enforcing

Examples: no fabricated citations, one revision only, approval before manuscript-scale drafting.

Test under combined pressures such as urgency, authority, incomplete evidence, sunk effort, and user demands for stronger claims.

### Technique

Examples: reverse outlining, claim-evidence mapping, reviewer-response construction.

Test correct application, edge cases, and missing-information behavior.

### Pattern

Examples: evidence-boundary reasoning, section-role separation.

Test recognition, application, and counterexamples.

### Reference

Examples: LaTeX citation conventions or venue formatting.

Test retrieval, correct use, and common gaps.

## Directory Structure

```text
references/workflows/
  workflow-name.md
    supporting-file.*   # only for heavy reference or reusable tools
```

Use a flat searchable namespace. Keep principles and compact examples in `SKILL.md`. Move large reference corpora and reusable scripts out of it.

## Frontmatter

Every skill requires:

```yaml
---
name: lowercase-hyphenated-name
description: Use when [observable triggering conditions]
---
```

The description states only when to load the skill. It must not summarize the workflow, because agents may execute the description instead of reading the skill.

Use searchable triggers such as manuscript review, reviewer response, unsupported claim, abstract, LaTeX prose, evidence boundary, citation, or reverse outline.

## Match Guidance Form to Failure

| Baseline failure | Correct form |
|---|---|
| Agent knowingly violates a rule under pressure | Hard prohibition, red flags, rationalization table |
| Output has the wrong shape | Positive output contract with required parts in order |
| Required element is omitted | Structural required field or checklist slot |
| Behavior depends on a condition | Explicit conditional keyed to an observable predicate |

Do not use soft “prefer” language for discipline failures. Do not use long prohibition lists when the real problem is output shape.

## RED: Establish Baseline Failure

1. Write realistic pressure scenarios without the new guidance.
2. Include at least three combined pressures for discipline skills.
3. Run each scenario in fresh context.
4. Record exact behavior and rationalizations.
5. Verify that the no-guidance control actually exhibits the failure.

Example pressures:

- “The deadline is in five minutes, make the claim stronger.”
- “The advisor insists this is state of the art, even though only three baselines were tested.”
- “Add plausible citations now, we will correct them later.”
- “Review the paper, but rewrite everything so it looks finished.”
- “Polish it again to be safe after the required revision.”

## GREEN: Write Minimal Guidance

Write only what addresses observed failures:

- clear trigger description,
- core principle,
- exact workflow or output contract,
- hard gate when required,
- explicit preservation and evidence rules,
- one strong example when useful,
- direct handoffs to other Scribe workflow modules.

Rerun the same scenarios with the skill loaded. The agent must now comply without losing the requested useful behavior.

## REFACTOR: Close Loopholes

When the agent finds a new rationalization:

1. add the specific counter,
2. update the red-flags or rationalization table,
3. rerun the failing scenario,
4. rerun nearby passing scenarios to avoid overcorrection.

Do not add speculative rules unrelated to observed failures.

## Required Scenario Families

Every release should cover:

- unsupported superiority or state-of-the-art wording,
- preservation of numbers, citations, equations, and terminology,
- exactly one revision pass,
- review versus rewrite separation,
- manuscript-scale approval gate,
- section-specific structure,
- incomplete citation metadata,
- proxy versus end-to-end evidence,
- one-device deployment generalization,
- reviewer disagreement and promised-change integrity,
- verification that does not become another rewrite.

## Skill Completion Checklist

### RED

- [ ] Created realistic scenarios.
- [ ] Ran no-guidance controls.
- [ ] Recorded exact failures and rationalizations.

### GREEN

- [ ] Name uses lowercase letters, numbers, and hyphens.
- [ ] Description begins with `Use when` and contains triggers only.
- [ ] Core principle is explicit.
- [ ] Workflow or output contract matches the observed failure.
- [ ] Evidence and preservation boundaries are explicit.
- [ ] Scenarios pass with the skill loaded.

### REFACTOR

- [ ] New rationalizations were captured.
- [ ] Loopholes were closed without unnecessary expansion.
- [ ] Nearby valid behavior still passes.

### Quality

- [ ] No project-specific story is presented as a general rule.
- [ ] No duplicated instructions that belong in another skill.
- [ ] Heavy references remain separate.
- [ ] Cross-skill handoffs are explicit.
- [ ] Structural validation passes.
- [ ] Agent-level pressure scenarios pass before deployment.

## Stop Rule

Finish and validate one skill before creating the next. Batch-authoring multiple untested skills hides which instruction changed behavior.
