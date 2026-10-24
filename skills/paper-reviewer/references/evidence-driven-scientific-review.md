# Evidence-Driven Scientific Review

## Core principle

Read the manuscript as a connected argument. A strong review identifies the exact statement, method, figure, or omission that creates uncertainty, explains the scientific consequence, and asks the smallest question or revision that resolves it. The review should make clear that the manuscript itself, rather than a generic checklist, generated each comment.

## Trace the evidence chain

For each central conclusion, follow its support backward through results, analysis, data construction, acquisition, apparatus, and assumptions. Compare descriptions across sections and figures. A detail can be locally plausible while the full chain remains ambiguous.

Use the applicable rows below. Skip rows that do not match the study design.

| Evidence chain | What to establish |
|---|---|
| Contribution and related work | What kind of contribution is claimed, which cited work is closest, what concretely differs, and which experiment demonstrates that difference. |
| Apparatus across conditions | Whether configurations described as the same actually use the same receiver, signal path, settings, calibration, and processing. Identify any uncontrolled difference that could explain the result. |
| Measurement provenance | The independent acquisitions, repetitions, dates or periods, sites, channels, environmental conditions, and criteria used to verify labels or ground truth. |
| Sampling and partitions | What the independent experimental unit is, how windows or samples were selected, how train, calibration, and held-out subsets were formed, and whether dependence changes uncertainty estimates. |
| Condition classification | The rule used to assign cases to qualitative regimes such as noisy, Gaussian, impulsive, adverse, or representative. Determine whether the rule is quantitative, reproducible, and separate from the outcome being explained. |
| Calibration and deployment | How reference data are obtained, how often calibration changes, what drift invalidates it, and whether the required reference state is available during realistic operation. |
| Evaluation coverage | Whether channels, datasets, subjects, sites, devices, or operating points represent independent and sufficiently varied evidence for the stated conclusion. |
| Claim scope | Whether the abstract and conclusion describe the measured cases or silently generalize to broader environments, populations, standards, or deployments. |

For an empirical study, record a manuscript-grounded answer for every applicable row before prioritizing comments. This is an audit, not the report outline. Send only the strongest distinct concerns into the Reviewer Voice selection step. Do not let a general reproducibility inventory substitute for the distinct questions of whether configurations are actually equivalent and whether a calibration assumption is operationally feasible.

When a paper acknowledges a limitation, check its practical effect rather than treating the acknowledgment as resolution. For example, admitting that windows are dependent does not establish whether a confidence interval remains valid.

## Classify before drafting

- **Confirmed inconsistency:** state the conflicting manuscript evidence and request correction or reconciliation.
- **Ambiguous method or assumption:** state what is clear, ask one focused question about what is not, and explain why the answer changes interpretation.
- **Missing support for a material claim:** identify the claim and the evidence boundary, then request support or narrower wording.
- **Optional strengthening:** label it as optional or future work when the central claim does not require it.

Missing detail is not automatically a defect. First check captions, appendices, supplements, repositories, and cross-references. If the answer remains unclear, ask rather than assert that the authors did not perform the step.

## Drafting handoff

After completing the evidence audit, use Reviewer Voice and [Canonical Reviewer Style](canonical-reviewer-style.md) to select and draft the author-facing comments. The audit finds issues; the canonical issue #18 example determines the actual language of the opening assessment and numbered comments. Do not draft from the audit table itself. Do not turn audit categories into visible issue/impact/action labels or uniform sentence patterns.

## Novelty and recommendation gate

A defensible novelty criticism contains all three elements:

1. the closest work identified from the manuscript's cited literature
2. the specific methodological, empirical, or deployment overlap
3. the claimed contribution that remains unestablished after that comparison

Without those elements, request clearer positioning and do not use novelty as a rejection reason. External literature verification is required only when the user requests it or supplies sources that must be checked.

Every principal recommendation reason must be recoverable from a verified major author comment. A recommendation cannot rely on a generic impression that the work is incremental, straightforward, incomplete, or not ready.

## Final quality check

- Could each comment have been written without reading this particular manuscript? If so, add the missing anchor or remove it.
- Does every question have an answer that would materially change interpretation, reproducibility, or claim scope?
- Does each requested experiment follow from a central claim? Otherwise make it optional or request narrower wording.
- Are separate recordings, samples, and derived windows treated as different levels of evidence?
- Are praise, criticism, and the recommendation bounded by the same evidence?
