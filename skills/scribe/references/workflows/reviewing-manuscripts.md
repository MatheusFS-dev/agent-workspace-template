# Reviewing Manuscripts

> **Supporting module:** Part of the single `scribe-superpowers` skill. Load it for manuscript or section diagnosis.

## Boundary

Return diagnostics and targeted actions. Rewrite passages only when explicitly requested. Do not present missing experiments, reviewer intent, acceptance likelihood, or inferred results as facts.

## Review Process

1. Establish the manuscript or section thesis, audience, requested depth, available evidence, and output format.
2. Reverse outline the text. Record each paragraph's main message, supporting evidence, and relationship to the thesis. Check whether the sequence forms a coherent argument.
3. Build a claim-evidence map linking major claims to experiments, analyses, citations, figures, tables, metrics, protocols, and limitations.
4. Separate textual ambiguity from absent evidence. A wording fix cannot repair an unsupported scientific claim.
5. Report findings by severity and provide a concrete action such as move, merge, split, narrow, expand, define, support, qualify, or remove.

## Reviewer-Risk Checks

Check whether the manuscript:

- frames standard tools or ordinary combinations as novelty,
- claims universal superiority from limited baselines or aggregate-only results,
- hides dataset, representation, search-space, preprocessing, threshold, or hardware boundaries,
- treats static complexity, measured latency, throughput, power, and energy as interchangeable,
- presents a proxy or module metric as complete system validation,
- claims interpretability without defining and validating what it means,
- describes downstream decision, ranking, warning, tracking, scoring, or control components without evaluating them,
- generalizes from one dataset, site, simulator, device, workload, or adverse condition,
- omits class imbalance, annotation quality, rare-class, and heterogeneous-source limitations,
- contains inconsistent terminology, acronyms, notation, figure labels, table ordering, or spelling.

Load one relevant file under `references/reviewer-examples/` when an example is needed. Do not load the entire reviewer corpus.

## Recommended Output

1. Scope and review basis
2. Major findings
3. Structural findings from the reverse outline
4. Claim-evidence findings
5. Terminology and presentation findings
6. Prioritized revision actions
7. Evidence gaps that cannot be solved textually

After drafting the report, use `quality-control.md` to revise and verify the report without converting it into a manuscript rewrite.
