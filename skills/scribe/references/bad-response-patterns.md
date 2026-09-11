# Bad Response Patterns

Use this compact reference to detect weak writing and reasoning. The examples are intentionally topic-neutral. Preserve valid scope and uncertainty, but do not manufacture weaknesses or bury the answer in caveats.

Keep each independent pattern in a descriptive `##` section of no more than 200 words. Extend a section only while it remains within that limit; otherwise add a new section. Search headings or keywords and read only the matching sections.

## Unsupported or premature claims

**Avoid:** Stating conclusions before presenting their method or evidence.

> The later analysis proves that the proposed approach is superior.

**Prefer:** Use prospective language before the evidence, then make the supported claim where the evidence appears.

> A later analysis evaluates this comparison. Its results show a lower error under the stated protocol.

**Avoid:** Inventing causes, intentions, completeness, or generality.

> The difference is caused by normalization, and the method works in all settings.

**Prefer:** Separate observation from explanation.

> The normalized variant performed better in this evaluation. The available experiment does not isolate the cause.

## Caveats that overwhelm the result

**Avoid:** Following every result with a long list of untested conditions.

> The method improves the metric, but this does not establish performance for other datasets, thresholds, devices, distributions, scales, or protocols.

This is repetitive, defensive, and may imply that a valid scoped result is useless.

**Prefer:** State the result and its material boundary once.

> The method improves the metric across the evaluated conditions.

Add a limitation only when it changes interpretation, answers a likely objection, or motivates future work. Never remove a real limitation merely to sound stronger.

## Limitations that appear to invalidate the work

**Avoid:** Describing scope boundaries as fundamental defects or listing every untested possibility.

> The evaluation uses one dataset and therefore cannot establish that the method is useful in practice. Other inputs, environments, objectives, or implementations may produce different behavior.

This overstates what the missing evidence means and invites readers to dismiss more than the evidence justifies.

**Prefer:** State the established result first, identify the exact boundary, and explain its consequence without speculation.

> The method improved the target metric on the evaluated dataset. Additional datasets are needed to determine how consistently this gain transfers to other data distributions.

Frame limitations with three elements:

1. **Established result:** What the evidence does support.
2. **Exact boundary:** What was not evaluated or cannot be inferred.
3. **Proportionate consequence:** What remains uncertain, without implying that the demonstrated result is invalid.

Use strong conclusions such as “the method is not practical,” “the result is not generalizable,” or “the evidence is insufficient” only when the evidence supports them. Otherwise name the unevaluated dimension precisely. Keep limitations brief and consolidate secondary ones in a discussion or future-work passage instead of attaching a defensive disclaimer to every result.

## Treating differences as deficiencies

**Avoid:** Calling every difference from the current work a limitation.

> Prior work uses a different input policy, which is a limitation.

**Prefer:** Distinguish characteristics from gaps the response actually addresses.

> Prior work studies a different input policy. The present analysis instead examines robustness to missing inputs.

Discuss a prior limitation only when the current work supplies relevant evidence or capability.

## Repeated evidence-boundary disclaimers

**Avoid:** Repeating the same comparison warning after every item.

> These values are not directly comparable because the protocols differ.

**Prefer:** State the common comparison rule once, then retain only item-specific qualifications.

> Numerical results are compared only within shared evaluation protocols. Study-specific differences are noted below where they affect interpretation.

## Dense, overloaded sentences

**Avoid:** Packing setup, transformation, optimization, and selection into one sentence.

> The system receives sparse inputs represented in a fixed tensor, normalizes intermediate values, scales each target independently, minimizes a profile loss, and selects the largest reconstructed value.

**Prefer:** Explain the sequence and purpose in short units.

> Sparse inputs are first mapped to a fixed-size tensor. The model reconstructs the target profile by minimizing mean squared error. At inference, it selects the largest predicted value.

Split a sentence when it contains multiple stages, contrasts, or definitions. Do not split related ideas into choppy fragments merely to shorten them.

## Unexplained notation, acronyms, and indexing

**Avoid:** Introducing symbols, abbreviations, thresholds, scale factors, or index conventions without definitions.

> The score is $q_i=(x_i-b)/a$, and the output uses one-based indices.

**Prefer:** Define each term at first use and explain non-obvious conventions.

> For item $i$, the normalized score is $q_i=(x_i-b)/a$, where $b$ is the offset and $a>0$ is the scale. Reported indices start at 1 to match the displayed labels.

Use one term and symbol for one concept throughout. Do not present finite values as exact limiting cases unless an explicit approximation convention is stated.

## Ambiguous metrics and aggregation

**Avoid:** Calling a metric decisive without defining its denominator, stabilizer, weights, or sensitivity.

> The normalized gap is the primary criterion and selects Model B.

**Prefer:** Define how the metric is computed, expose unstable cases, and corroborate it with an absolute view when scale normalization can distort rankings.

> The normalized gap uses equal weights and denominator stabilization by ε. Because small denominators can amplify differences, the absolute gap is also reported. Both views inform the comparison.

For resampling or confidence intervals, state what is resampled, whether pairing is preserved, how many replicates are used, and what statistic is recomputed.

## Unverifiable or vague comparisons

**Avoid:** Claims that a reader cannot confirm from a nearly overlapping figure.

> The proposed curve is consistently better.

**Prefer:** Supply the relevant numerical difference or table entry.

> The proposed curve is lower at all five settings, with absolute differences from 0.002 to 0.009.

Check every quoted value against the source artifact. Do not infer computational cost, difficulty, or causality from a proxy unless the evidence supports that inference.

## Irrelevant implementation detail

**Avoid:** Including validation guards, conversion checks, file-state commentary, unused configuration, command internals, or packaging details that do not help the audience understand or reproduce the result.

> A candidate is accepted only after conversion, allocation, interface validation, and application-level occupancy checks.

**Prefer:** Retain the methodologically relevant facts and explain why they matter.

> Candidates must fit the target memory and numeric-interface constraints before physical evaluation.

Do not omit details required for reproducibility, such as sample selection, calibration, environment versions, failure reasons, or measurement protocol. Put operational material in the appropriate reproducibility section rather than the main argument.

## Confusing presentation

**Avoid:** Dense prose in narrow table cells, redundant columns, unexplained labels, tiny text, inconsistent visual styles, or captions written like headlines.

**Prefer:**

- Keep table cells to short, parallel phrases; move explanations into prose.
- Remove columns that duplicate another field or do not affect interpretation.
- Explain non-obvious columns and failure states.
- Use readable type, consistent legends, scales, colors, and line styles.
- Write captions in sentence case unless a required style says otherwise.
- Use figures for patterns and tables for exact values.

## Redundancy and obvious commentary

**Avoid:** Narrating presentation choices or repeating conclusions.

> The plots are separated so both relationships remain readable.

> These complementary results are combined only after each comparison is shown.

**Prefer:** Present the plots or comparisons directly. Explain a structural choice only when readers would otherwise misinterpret the evidence.

Keep definitions in one authoritative location and use a short reminder or cross-reference elsewhere.

## Inconsistent scope and terminology

**Avoid:** Switching between validation and test data, exact and approximate labels, percentage and proportion, singular and set-valued targets, or short and official names without explanation.

**Prefer:** Establish a vocabulary and evidence scope, then apply them consistently across prose, equations, tables, figures, summaries, appendices, and glossary entries.

When removing or changing a concept, also check references, summaries, captions, tables, and downstream conclusions for contradictions.

## Weak revision behavior

**Avoid:** Copying an informal instruction directly into polished prose, editing only the named sentence when the change creates contradictions, or broadening the task into unrelated rewrites.

**Prefer:** Infer the intended claim, rewrite it for the target audience, and make the smallest set of consistency edits required. Preserve confirmed facts and leave unrelated content unchanged.
