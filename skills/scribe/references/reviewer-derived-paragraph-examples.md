# Reviewer-Derived Writing Review Examples

Use this reference during the one-pass writing review after drafting any paragraph that makes a contribution, novelty, deployment, comparison, metric, dataset, figure-quality, table-quality, or limitation claim. These examples are abstracted from real reviewer reactions, but they deliberately omit paper-specific systems, datasets, methods, numbers, names, and venues. Their purpose is to prevent reviewer misunderstandings caused by wording, not to require new experiments.

## How to use these examples

Before returning final manuscript prose, search for claim-heavy wording:

```bash
grep -nEi "underexplored|novel|contribution|best|outperform|state of the art|superior|deployment|generaliz|simulation|benchmark|metric|proxy|unified|representation|fair|baseline|figure|vector|end-to-end|interpretable|risk|warning|tracking|motion|embedded|throughput|power|energy|imbalance|rare|adverse|background|confusion|multi-modal|table|acronym|typo|inconsistent|limitation|future work" draft.tex
```

For each hit, ask whether the paragraph makes the reader infer more than the text has actually supported. If so, narrow the claim, add the missing condition, or state the limitation directly. Do not invent experiments, citations, baselines, confidence intervals, measurements, or figure properties.

## Example 1, novelty framed as standard tool use

Risky previous wording:

> Systematic optimization remains underexplored in this setting. To address this gap, this work applies an automated search procedure to several model families.

Likely reviewer reaction:

> The text should clarify what is new beyond applying a known optimization tool. Readers need to know whether the contribution is methodological, empirical, or deployment-oriented.

Revision behavior:

- Do not imply that using a standard optimizer is itself the novelty.
- State the contribution type explicitly.
- If the work is empirical, call it a controlled empirical comparison, not a new method.
- Identify the controlled variables, such as representation, split, search budget, and evaluation protocol.

Safer pattern:

> This work uses automated search as a controlled comparative tool rather than as a new search algorithm. Under a common representation, search protocol, and evaluation split, it compares multiple model families to identify the most favorable accuracy-cost operating point for the target setting.

## Example 2, contribution sounds like a loose combination of known components

Risky previous wording:

> The work combines automated search, multimodal input, and compression to improve the target task.

Likely reviewer reaction:

> The core contribution is integration-driven and not clearly isolated. Clarify whether the contribution lies in the search space, the representation, the evaluation protocol, or the accuracy-efficiency optimization framework.

Revision behavior:

- Separate components from contribution.
- Do not list methods as if their combination automatically proves novelty.
- Add one sentence identifying the actual scientific or engineering question answered by the paragraph.

Safer pattern:

> The contribution is not the isolated invention of the search method, the input representation, or the compression technique. It is a controlled deployment-oriented comparison of these design choices under one protocol, showing which configuration provides the most favorable observed trade-off under the adopted data representation and evaluation setting.

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

## Example 4, small numerical gains are treated as decisive

Risky previous wording:

> The compressed model improves accuracy while reducing computational cost.

Likely reviewer reaction:

> If the numerical difference is small relative to run-to-run variability, the text should not describe it as an accuracy improvement. The supported contribution may be cost reduction at comparable accuracy.

Revision behavior:

- Do not describe tiny differences as improvements unless statistical support is available.
- If confidence intervals include zero, say `statistically comparable`.
- Put the practical benefit on the supported axis, usually complexity, latency, memory, or implementation simplicity.

Safer pattern:

> The compressed model preserves statistically comparable accuracy while reducing computational cost. Its practical value is the lower resource requirement, not a decisive accuracy gain.

## Example 5, statistical superiority is implied without paired evidence

Risky previous wording:

> The proposed model achieves a higher score than the closest prior baseline.

Likely reviewer reaction:

> If only aggregate metrics are available for prior works, the comparison is descriptive. It should not sound like a claim of statistical superiority because paired predictions or repeated-run evidence are unavailable.

Revision behavior:

- Use `descriptive comparison` for aggregate-only comparisons.
- Reserve statistical superiority for comparisons with paired predictions, confidence intervals, or formal tests.
- Avoid `significantly`, `decisively`, or `clearly superior` unless supported.

Safer pattern:

> Relative to prior aggregate reports, the model obtains the highest reported value on the primary metric among the compared entries. Because paired predictions are unavailable for those baselines, this comparison is descriptive rather than a test of statistical superiority.

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

## Example 9, static complexity and runtime are treated as interchangeable

Risky previous wording:

> The model has fewer operations and therefore lower latency.

Likely reviewer reaction:

> A model with larger static complexity can be faster on a specific device depending on implementation, memory access, batching, and execution path. The latency protocol and any mismatch need explanation.

Revision behavior:

- Specify device, batch size, warm-up, synchronization, repetitions, and reported statistic when latency is discussed.
- Treat operation counts as static complexity proxies, not direct runtime guarantees.
- Mention backend implementation, memory access, kernel overhead, hardware utilization, and conditional execution when relevant.

Safer pattern:

> Operation counts are reported as a static complexity proxy, whereas latency is measured on the target hardware. The two quantities need not be perfectly ordered because runtime also depends on memory access, backend implementation, hardware utilization, batching, and the actually executed path.

## Example 10, deployment claims rely on one measurement dimension

Risky previous wording:

> The low measured latency makes the method suitable for deployment.

Likely reviewer reaction:

> Practical deployment cannot be inferred from latency alone. The text should discuss synchronization, memory, robustness, distribution shift, integration cost, and operating constraints when those matter.

Revision behavior:

- Do not equate one timing result with deployment readiness.
- State which deployment dimension the evidence supports.
- Add remaining deployment constraints as limitations or scope conditions.

Safer pattern:

> The latency result supports real-time feasibility on the measured platform. Full deployment also depends on input synchronization, memory limits, distribution shift, robustness to changing conditions, integration with the surrounding system, and the reliability requirements of the target application.

## Example 11, proxy metric is presented as full system evaluation

Risky previous wording:

> The proposed metric links prediction quality to system-level performance.

Likely reviewer reaction:

> The metric is derived from an intermediate prediction or ranking, not a full end-to-end system simulation. It should be stated as a proxy metric.

Revision behavior:

- Name proxy metrics explicitly.
- State what the proxy includes and excludes.
- Avoid implying full system-level validation unless actually performed.

Safer pattern:

> The metric is used as a proxy system-level indicator derived from the model output. It connects prediction quality to an application-relevant quantity, but it is not a full end-to-end evaluation with all feedback, scheduling, environmental, and hardware effects included.

## Example 12, workflow description is too dense

Risky previous wording:

> The algorithms define preprocessing, search, training, compression, selection, and evaluation.

Likely reviewer reaction:

> The workflow is dense and difficult to follow. A simplified roadmap or conceptual explanation is needed before the algorithmic details.

Revision behavior:

- Add a short roadmap sentence before dense algorithms.
- Separate input processing, optimization, model selection, and evaluation into distinct sentences.
- When figures are available, point to them before algorithmic details.

Safer pattern:

> The pipeline has four stages: input preprocessing, model search, model selection, and final evaluation. The algorithm gives the optimization loop, while the system diagram summarizes the data flow.

## Example 13, one sentence carries method, result, and interpretation

Risky previous wording:

> The search evaluates several families using a shared representation, compares accuracy, complexity, latency, and a proxy metric, and shows that the compact family provides the strongest observed deployment-oriented trade-off under the adopted protocol.

Likely reviewer reaction:

> Long, information-dense sentences reduce readability, especially in methodology and results sections. Shorter sentences would improve comprehension.

Revision behavior:

- Split sentences containing three or more distinct claims.
- Put method, result, and interpretation in separate sentences.
- Prefer repeated nouns over unclear pronouns when the paragraph is technical.

Safer pattern:

> The search evaluates several model families under a shared representation. The comparison reports accuracy, complexity, latency, and a proxy metric. Under this setup, the compact family provides the strongest observed deployment-oriented trade-off.

## Example 14, figure-quality wording is incomplete

Risky previous wording:

> The figure summarizes the system, and all figures are provided as PDF.

Likely reviewer reaction:

> Figure labels may remain too small after two-column resizing. PDF files can still contain raster images inside vector containers.

Revision behavior:

- When describing figures, mention readability only if labels were actually enlarged or checked.
- Distinguish true vector graphics from raster images embedded in vector containers.
- For two-column venues, check whether labels remain readable after resizing.

Safer pattern:

> The figure should be regenerated or checked with labels large enough for two-column readability. The submitted file should also be verified as true vector artwork rather than a raster image embedded inside a PDF container.

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

## Example 16, result paragraph does not match the stated theme

Risky previous wording:

> A consistent evaluation protocol measures accuracy, latency, and energy, outlining practical trade-offs for the full embedded pipeline.

Likely reviewer reaction:

> The experiments do not align with the stated theme. The paper claims an end-to-end pipeline, but the results mainly report module-level accuracy and speed.

Revision behavior:

- Align the evaluation paragraph with the actual measured outputs.
- If only one module and system throughput were measured, avoid implying complete validation.
- State which metrics are module-level, which are system-level, and which modules are included in runtime.

Safer pattern:

> The evaluation reports module-level accuracy and platform-level runtime, power, and energy for the implemented loop. These results characterize perception accuracy and execution cost. They do not by themselves establish end-to-end decision quality unless the downstream module is evaluated with task-level metrics.

## Example 17, motivation remains qualitative

Risky previous wording:

> Tight compute and power budgets motivate the proposed embedded design.

Likely reviewer reaction:

> The introduction does not explain why this sensing and processing configuration is prioritized, nor how compute and power constraints shape the design choices.

Revision behavior:

- Explain the practical reason for the selected sensing or processing configuration.
- State the trade-off introduced by that choice.
- Tie the hardware budget to model size, resolution, runtime backend, power, memory, and latency choices.

Safer pattern:

> The design targets an embedded configuration because it lowers integration cost and enables local processing under limited power and memory. This constraint also restricts input resolution, model size, and downstream computation. The paper therefore emphasizes lightweight inference and simple decision logic rather than accuracy maximization with unconstrained resources.

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

## Example 23, custom throughput metric is treated as complete throughput

Risky previous wording:

> The custom throughput metric better reflects scene-dependent load and keeps downstream processing in the loop.

Likely reviewer reaction:

> The metric fluctuates with scene density and cannot independently characterize frame-level processing capability.

Revision behavior:

- Define the custom throughput metric precisely.
- Do not use it as a substitute for frame-level latency or processed frames per second.
- Pair it with per-frame latency, average workload, scene density, and stage decomposition when possible.

Safer pattern:

> The custom throughput metric is reported as a workload-dependent indicator, not as a frame-level throughput measure. Because it varies with input density, it should be interpreted together with processed frames per second, per-frame latency, average workload per frame, and stage-level timing.

## Example 24, power and energy efficiency are under-specified

Risky previous wording:

> The proposed setup establishes the best efficiency frontier under the evaluated workload.

Likely reviewer reaction:

> The power measurement protocol is unspecified, and energy-efficiency claims should be compared only against systems measured under comparable conditions.

Revision behavior:

- State how power was measured, including device boundary, sensor, sampling period, warm-up, idle subtraction, and workload.
- Avoid `efficiency frontier` unless the compared set is clearly defined.
- Use `among the tested devices` instead of broad claims unless a fair external comparison exists.

Safer pattern:

> Among the tested configurations, this setup gives the highest observed efficiency under the stated workload. This result is not a general efficiency frontier unless power is measured under a reproducible protocol and compared with published systems using comparable models, inputs, workloads, and postprocessing.

## Example 25, bottlenecks are hidden behind aggregate latency

Risky previous wording:

> The study focuses on system-level indicators: throughput, latency, power, and energy consumption.

Likely reviewer reaction:

> The latency stage decomposition is unspecified, making it impossible to identify performance bottlenecks or reproduce the results.

Revision behavior:

- State what latency includes, from input availability to output emission.
- If resolution or workload scaling is discussed, identify expected bottlenecks.
- Do not imply bottlenecks were measured if only end-to-end latency exists.

Safer pattern:

> System latency is defined as wall time from input availability to output emission, including preprocessing, inference, postprocessing, tracking or association, decision logic, and output prioritization when these stages are active. If only end-to-end latency is measured, bottleneck claims should remain qualitative unless stage-level profiling is reported.

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

## Example 29, table ordering, alignment, and terminology create reviewer friction

Risky previous wording:

> Table I lists related works and Table IV reports detailed results.

Likely reviewer reaction:

> Table entries are not ordered clearly, row and column alignment reduce readability, and terminology is inaccurate for the actual system design.

Revision behavior:

- Check table ordering against the venue style and reader expectation.
- Verify row and column alignment after compilation, not only in source code.
- Use accurate terms: `multi-class`, `multi-object`, `multi-task`, `single-sensor`, or `multi-sensor` as appropriate.
- Avoid `multi-modal` unless the system actually combines distinct modalities.

Safer pattern:

> The table organizes prior works by method category and uses terminology that matches the actual input sources and tasks. Citation order and table alignment should be checked in the compiled two-column PDF to avoid avoidable readability objections.

## Example 30, acronym and spelling inconsistencies weaken credibility

Risky previous wording:

> The title introduces a system acronym, but the acronym is not defined or used consistently in the abstract, body, figures, and conclusion.

Likely reviewer reaction:

> Undefined acronyms, inconsistent spelling, and mismatched figure labels make the manuscript look less mature even when the technical content is sound.

Revision behavior:

- Define every title acronym in the abstract or first paragraph when the venue permits it.
- Use the acronym again only when it helps, otherwise remove it from the title.
- Search compiled figures and source files for spelling inconsistencies, not only manuscript text.
- Treat figure text as manuscript text because reviewers read it the same way.

Safer pattern:

> The system acronym is introduced at first mention and used consistently thereafter. Figure labels, captions, and body text use the same spelling and terminology.

## Example 31, title or table claims enumerate capabilities that are not analyzed

Risky previous wording:

> The expanded taxonomy enables joint reasoning across multiple object categories and downstream functions.

Likely reviewer reaction:

> The table enumerates many categories or functions, but the experiments address only one performance dimension and do not explain category-specific confusion or mitigation strategies.

Revision behavior:

- If a class list or capability list is used to motivate a broad system, make sure the results discuss rare or safety-critical categories, not only aggregate metrics.
- Do not imply joint reasoning across functions unless the downstream function is evaluated or at least discussed with module-level evidence.
- Link class-space or capability claims to per-class performance, confusion, condition bins, or limitations.

Safer pattern:

> The expanded taxonomy allows the model to train and evaluate multiple categories under one label space. The current evidence is module-level, so taxonomy claims should be read together with per-class precision, recall, confusion, and error analyses rather than as proof of complete multi-function reasoning.
