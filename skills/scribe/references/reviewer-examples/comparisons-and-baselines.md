# Reviewer Examples: Comparisons and Baselines

Use this file only when the current paragraph or section contains the corresponding claim type. Apply the examples during the single reviewer-informed revision pass. Preserve supplied facts, numbers, citations, labels, equations, and terminology.

## Example 3, universal superiority is implied from limited evidence

Risky previous wording:

> The proposed model outperforms prior methods and provides the best overall performance.

Likely reviewer reaction:

> The improvement may be limited to one metric, one protocol, or one subset of baselines. The result should not be framed as a universal win on every metric.

Revision behavior:

- Replace universal claims with scoped claims.
- Specify the metric, protocol, and compared set.
- If not all metrics improve, state that directly.
- Use `strongest observed`, `among the compared models`, or `under the adopted protocol` when appropriate.

Safer pattern:

> The selected model gives the strongest observed result on the primary metric among the compared single-model baselines under the adopted protocol, but it does not dominate every operating point. The main outcome is therefore a favorable accuracy, latency, and complexity trade-off rather than absolute superiority across all metrics.
## Example 7, representation may bias the model comparison

Risky previous wording:

> A unified representation is used for all model families, and one family outperforms the others.

Likely reviewer reaction:

> The representation may naturally favor one family and handicap others. The comparison should make clear whether the input structure was preserved or transformed in a way that affects the family ranking.

Revision behavior:

- State whether the representation is shared or family-specific.
- If structure is flattened, aggregated, or otherwise transformed, acknowledge that the choice affects the comparison.
- If a natural baseline is excluded, provide a technical reason.
- If included, specify how its native structure is preserved.

Safer pattern:

> The comparison uses a shared representation to control preprocessing, but this choice can favor architectures aligned with that representation. The observed ranking should therefore be interpreted with respect to the selected input encoding rather than as an architecture-invariant conclusion.
## Example 8, search-space fairness is left implicit

Risky previous wording:

> The search compares several model families under the same protocol.

Likely reviewer reaction:

> The fairness of the cross-family search is unclear. Clarify whether budgets, parameter ranges, depth constraints, objectives, and pruning rules are comparable across families.

Revision behavior:

- Distinguish same trial budget from identical search spaces.
- Explain comparability in terms of budget, objective, data split, preprocessing, and constraints.
- Avoid claiming perfect fairness when families have inherently different design spaces.

Safer pattern:

> All families use the same training split, validation objective, pruning rule, and trial budget. The search spaces are family-specific, but their depth, width, and regularization ranges are constrained to comparable deployment-oriented regimes, with sampled configurations reported for reproducibility.
## Example 26, baseline fairness is under-specified

Risky previous wording:

> The newer model achieved higher accuracy than the baseline under a consistent evaluation protocol.

Likely reviewer reaction:

> Did the baseline use the same training strategy, data augmentation, loss function, input resolution, thresholds, and postprocessing? Is the comparison fair?

Revision behavior:

- When comparing model versions, specify same dataset split, resolution, augmentation policy, training schedule, thresholds, runtime backend, and postprocessing.
- If some settings differ due to model defaults, state that difference.
- Avoid saying a comparison is fair unless the controlled variables are listed.

Safer pattern:

> The models are compared under the same dataset split, input resolution, augmentation policy, decision threshold, postprocessing configuration, and evaluation script. Under these controlled settings, the reported difference reflects the trained configurations rather than changes in preprocessing or postprocessing.
## Example 27, published-method comparison is too broad

Risky previous wording:

> Relative to published pipelines, the observed accuracy-efficiency profile reflects a broader task and stricter evaluation.

Likely reviewer reaction:

> The results section lacks a comparison with published advanced methods under the same platform and protocol.

Revision behavior:

- Do not imply direct superiority over published systems when datasets, platforms, resolutions, labels, and metrics differ.
- Distinguish contextual related-work positioning from controlled baseline comparison.
- Use phrases such as `not directly comparable` and identify why.

Safer pattern:

> Published systems provide useful context, but their results are not directly comparable when they use different datasets, label spaces, hardware, input resolutions, and postprocessing. The controlled comparison is therefore limited to models retrained and evaluated under the same local protocol.
