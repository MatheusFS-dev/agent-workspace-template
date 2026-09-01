# Reviewer-Derived Writing Review Examples

Use these topical references during the single reviewer-informed revision pass. Load only the file matching the claims in the current text. These examples are abstracted from reviewer reactions and omit paper-specific systems, datasets, methods, numbers, names, and venues. They guide wording and claim scope. They do not authorize new experiments, citations, measurements, or facts.

## Routing

| Text contains | Load |
|---|---|
| Novelty, contribution type, standard tools presented as novelty | `claims-and-novelty.md` |
| Superiority, baselines, representation fairness, search-space fairness, prior-work comparisons | `comparisons-and-baselines.md` |
| Numerical gains, significance, proxy metrics, result interpretation, motivation evidence | `metrics-and-results.md` |
| Runtime, latency, throughput, power, energy, hardware, deployment cost | `deployment-and-efficiency.md` |
| Generalization, end-to-end scope, limitations, imbalance, failure modes, adverse conditions | `scope-and-limitations.md` |
| Dense prose, figures, tables, acronyms, spelling, terminology, title claims | `terminology-and-clarity.md` |

Load at most the files needed for the current paragraph or section. Do not load the full set by default.

## Common use rule

For each relevant claim, ask whether the wording makes the reader infer more than the supplied evidence supports. Narrow the claim, add the missing condition, or state the limitation directly. Do not invent experiments, citations, baselines, confidence intervals, measurements, or figure properties.
