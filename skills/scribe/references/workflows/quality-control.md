# Quality Control

> **Supporting module:** Part of the single `scribe-superpowers` skill. It combines the required one-pass revision and final verification while keeping them separate phases.

## Phase A: One Reviewer-Informed Revision

Apply this phase exactly once after drafting or materially rewriting prose. Review the initial draft internally for:

- unclear explanation or buried main message,
- redundancy and compressible length,
- awkward transitions or paragraph order,
- claim wording stronger than the evidence,
- reviewer-trigger wording that can be corrected textually,
- preservation drift in facts, numbers, citations, equations, labels, or terminology.

Create a brief hidden revision report, apply its changes once, then stop general polishing. Do not expose the report unless requested.

This phase may merge, split, narrow, qualify, reorder, or remove prose while preserving meaning. It must not invent evidence, redesign the study, demand new experiments, change the scientific position, assess acceptance probability, or replace supplied facts with reviewer preference.

## Phase B: Fresh Verification

Verify the revised artifact, not the initial draft. This phase is an objective contract check, not another style pass.

### Evidence and claims

- Every material claim is supported, scoped, or clearly framed as a limitation or future target.
- Novelty, comparison, deployment, and generalization claims state their boundary.
- Standard tools are not mislabeled as contributions.
- Aggregate differences are not described as statistically significant without evidence.
- Proxy metrics and module-level results are not presented as end-to-end validation.
- No citation, result, baseline, reviewer intent, dataset property, metric, or number was fabricated.

### Preservation

Compare against the supplied source for facts, causal relations, numbers, signs, units, citations, equations, labels, terminology, acronym expansion, notation, capitalization, and measured versus proposed status. Any change requires explicit user authorization.

### Structure and output

- The artifact performs its requested section or response role.
- Review-only work did not silently become rewriting.
- Reviewer responses answer each comment and promise only changes actually made or clearly proposed.
- Hidden brainstorming notes, revision reports, placeholders, and tool artifacts are absent.
- Formatting follows the requested plain-text or LaTeX contract.

When complete LaTeX sources and tools are available, compile or lint before claiming compilation success. Otherwise state only what was inspected.

## Correction Rule

Correct an identified objective violation and recheck that violation. Do not reopen the artifact for broad improvements. A broad reread for further polish is a prohibited second revision.
