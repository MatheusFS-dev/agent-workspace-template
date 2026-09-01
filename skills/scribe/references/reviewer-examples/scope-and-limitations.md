# Reviewer Examples: Scope and Limitations

Use this file only when the current paragraph or section contains the corresponding claim type. Apply the examples during the single reviewer-informed revision pass. Preserve supplied facts, numbers, citations, labels, equations, and terminology.

## Example 6, generalization is hidden in the conclusion

Risky previous wording:

> Compact models are best for deployment.

Likely reviewer reaction:

> The conclusion may hold only for the adopted representation, benchmark, preprocessing, and deployment assumptions. It is unclear whether it transfers to different datasets, input formats, target devices, or real-world conditions.

Revision behavior:

- Scope conclusions to the dataset, representation, search space, hardware, and protocol when those are fixed.
- Add concrete domain-gap mechanisms when relevant.
- Do not bury dataset limitations only in future work.

Safer pattern:

> Under the adopted representation, searched spaces, benchmark, and target-device measurements, compact models provide the strongest observed standalone accuracy-cost trade-off. Different encodings, operating conditions, datasets, or hardware backends may change both absolute performance and the model ranking.
## Example 15, end-to-end system is claimed but only one module is evaluated

Risky previous wording:

> This work presents a single end-to-end pipeline that performs sensing, tracking, motion estimation, decision logic, and real-time alerts.

Likely reviewer reaction:

> The methodology emphasizes a full pipeline, but the experiments quantify only one module. The core system claim appears unsupported by empirical evidence.

Revision behavior:

- Do not let an abstract or contribution paragraph make the full pipeline sound validated unless every claimed stage has relevant evidence.
- Separate implemented components from experimentally evaluated components.
- If downstream logic was not quantitatively tested, call it an implemented design component or future validation target.
- Add the missing validation axis when available.

Safer pattern:

> The system implements sensing, tracking, motion cues, decision logic, and alert generation in one pipeline. The present evaluation quantifies the sensing module and platform-level execution cost. Validation of decision correctness and alert reliability remains separate unless warning-level labels or module-level tests are reported.
## Example 18, interpretability is overclaimed

Risky previous wording:

> The decision module produces an interpretable score for real-time alerts.

Likely reviewer reaction:

> Does interpretability mean that the rules are inspectable, that users understand the output, or that experts validated the decision logic?

Revision behavior:

- Do not imply validated human interpretability unless a user study or expert validation exists.
- If rules are manually designed, say so directly.
- Distinguish rule inspectability from empirical validity.
- If no annotated decision labels exist, do not claim score accuracy.

Safer pattern:

> The decision module provides an inspectable score through transparent rules and tunable parameters. In this version, interpretability refers to the visibility of the rule structure, not to user-study validation or empirically verified decision correctness.
## Example 19, known failure modes of a lightweight component are unqualified

Risky previous wording:

> The system estimates short-term motion with a lightweight tracking cue.

Likely reviewer reaction:

> Lightweight motion cues can fail under low signal quality, high speed, blur, occlusion, or feature-poor conditions. The text should state whether these edge cases were evaluated.

Revision behavior:

- Present the component as a lightweight cue, not a universally robust estimator.
- State known failure modes when the paper concerns real-time or safety-critical operation.
- If no comparison with stronger alternatives exists, frame it as future work rather than implying optimality.

Safer pattern:

> The tracking cue is used because it is lightweight and suitable for embedded execution. Its estimates can degrade under low signal quality, blur, fast motion, occlusion, and feature-poor regions. A full robustness study should compare this cue with stronger alternatives under controlled adverse conditions.
## Example 20, unified dataset wording hides imbalance and source heterogeneity

Risky previous wording:

> A curated unified dataset harmonizes several public sources into one label space.

Likely reviewer reaction:

> What are the scale, diversity, and annotation quality of the dataset? What is the impact of class imbalance on rare categories? Were baselines trained under the same strategy?

Revision behavior:

- Whenever `unified dataset` or `unified label space` is used, include source datasets, class list, size, imbalance, and annotation consistency when space allows.
- Mention rare classes and underrepresented conditions when they affect claims.
- Do not imply uniform data quality across merged sources.
- Clarify whether baselines use the same split, augmentations, resolution, loss, thresholds, and postprocessing.

Safer pattern:

> The dataset unifies multiple sources through explicit label remapping. Because the sources differ in frequency, scene diversity, and annotation conventions, the resulting label space is imbalanced. Rare classes and underrepresented conditions should therefore be interpreted through class-aware metrics rather than only aggregate scores.
## Example 21, error source is noted but not analyzed

Risky previous wording:

> Background errors remain the main failure mode.

Likely reviewer reaction:

> The discussion merely notes the problem without explaining causes or mitigation.

Revision behavior:

- When reporting error patterns, identify plausible mechanisms, such as small object size, low contrast, truncation, occlusion, label noise, annotation inconsistency, or class overlap.
- Connect the error to a concrete mitigation.
- Avoid generic statements that do not help the reader understand failure modes.

Safer pattern:

> Background errors are concentrated in small, low-contrast, or partially occluded categories. This suggests that aggregate metrics mask class-specific failure modes. Mitigation should focus on targeted sample collection, class-aware sampling, condition-stratified reporting, and temporal confirmation.
## Example 22, false positives from static context are dismissed too easily

Risky previous wording:

> The decision logic prioritizes dynamic objects and filters static context.

Likely reviewer reaction:

> Can the system handle false positives from static objects or background structures?

Revision behavior:

- Do not claim static-object filtering unless the filtering rule and evidence are described.
- Distinguish truly irrelevant static context from stationary but safety-relevant objects.
- State whether filtering uses motion, persistence, context priors, geometry, or explicit calibration.

Safer pattern:

> The decision logic downweights objects with low apparent motion and stable position, but stationary relevant objects remain a possible false-alert source without explicit context reasoning or calibration. This limitation is important in cluttered environments with many static structures.
## Example 28, adverse-condition robustness is overgeneralized

Risky previous wording:

> The dataset spans heterogeneous environmental conditions and supports generalization in typical real-world settings.

Likely reviewer reaction:

> Some adverse conditions are sparse, which limits robustness claims under those conditions.

Revision behavior:

- State the actual distribution of adverse-condition samples when known.
- Do not claim robustness under conditions that are sparse or absent in the dataset.
- Move untested robustness to limitations and future work, not results.

Safer pattern:

> The dataset mainly supports evaluation under the dominant conditions represented in the collected samples. Because adverse-condition samples are sparse, the reported results should not be interpreted as evidence of robustness under degraded settings. Targeted acquisition and stress testing are needed.
