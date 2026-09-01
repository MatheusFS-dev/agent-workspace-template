# Drafting Academic Prose

> **Supporting module:** Part of the single `scribe-superpowers` skill. Load it only through the root routing table.

## Purpose

Produce concise, formal, readable academic prose while preserving supplied scientific content and limiting every claim to available evidence.

## Internal Preparation

For substantial prose, determine internally:

1. task, audience, section role, and output format,
2. central claim the text is allowed to make,
3. evidence supporting that claim and claims the evidence cannot support,
4. likely reviewer misunderstanding,
5. narrative spine: problem, gap, challenge, insight, contribution, evidence, limitation.

Do not expose these notes unless the user requested an outline or plan.

## Writing Contract

- Prefer direct, formal, readable prose and third person unless the user or venue requires otherwise.
- Preserve facts, causal relationships, numbers, signs, units, ordering, citations, citation keys, equations, labels, terminology, acronym meanings, and distinctions among measured, simulated, inferred, proposed, and future work.
- Keep novelty, causality, superiority, deployment, robustness, interpretability, significance, and generalization claims conservative and explicitly scoped.
- Do not present standard models, optimizers, compression methods, tools, or ordinary combinations as novelty unless the supplied work establishes that contribution.
- Do not infer statistical significance from small aggregate differences, end-to-end performance from a module metric, or broad deployment readiness from one device or timing result.
- Avoid unnecessary bullets in manuscript prose. Prefer commas and full stops over semicolons or long dashes. Split dense sentences for double-column readability.

## Claim Construction

For each important claim, identify:

- the precise assertion,
- supporting experiment, analysis, citation, figure, or table,
- metric and protocol,
- baseline set or operating condition,
- qualifier that prevents overgeneralization.

When support is incomplete, narrow the sentence. Do not compensate with persuasive language such as `best`, `state of the art`, `superior`, `robust`, `generalizable`, `real-time`, or `deployment-ready`.

## Paragraph Construction

A paragraph should have one main message, the mechanism or evidence needed to support it, a scoped interpretation, and a transition that advances the section argument. Separate method, result, and interpretation when combining them obscures the logic. Remove repeated motivation and repeated contribution wording.

## Code-to-Prose Translation

Describe mechanisms, inputs, outputs, assumptions, parameter roles, scientifically relevant processing order, limitations, failure conditions, and measured behavior. Do not narrate loops, assignments, logging, file handling, or implementation trivia unless they affect reproducibility or interpretation.

## Formatting Route

Use plain text unless LaTeX is requested. For LaTeX, citations, acronyms, equations, units, BibTeX, or cross-references, load `references/scribe-style-guide.md`. Never invent missing citation metadata.

After the initial draft or material rewrite, load `quality-control.md` exactly once.
