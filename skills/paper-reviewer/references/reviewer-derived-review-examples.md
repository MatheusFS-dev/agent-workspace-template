# Reviewer-Derived Review Example Bank

Use this reference only when the user explicitly requests example-driven stress testing. It is an issue-discovery bank, not a voice or phrasing guide. The candidate angles are legacy topic prompts and must not be copied or imitated in the final review. Discover concerns here, verify them against the manuscript, then draft only through Reviewer Voice. These examples are abstracted from real reviewer reactions. Do not cite them as external evidence or force one onto a manuscript unless the supplied paper actually shows the issue.

## How to use these examples

When reviewing a manuscript, scan the paper for claim-heavy wording and evidence gaps. Typical trigger terms include:

```bash
grep -nEi "underexplored|novel|contribution|best|outperform|state of the art|superior|deployment|generaliz|simulation|benchmark|metric|proxy|unified|representation|fair|baseline|figure|vector|end-to-end|interpretable|risk|warning|tracking|motion|embedded|throughput|power|energy|imbalance|rare|adverse|background|confusion|multi-modal|table|acronym|typo|inconsistent|limitation|future work|latency|FLOPs|complexity|statistical|confidence|ablation|robustness|real-time|measurement|receiver|calibrat|threshold|held-out|subset|independen|Gaussian|impulsive|recording" manuscript.tex
```

For each hit, decide whether the issue belongs in grammar/language, lenient review, standard review, or adversarial review:

- Use grammar/language when the issue is wording, terminology, acronym definition, table readability, figure labels, or sentence density.
- Use lenient review when the issue can be solved by clarification, scoping, or a small discussion.
- Use standard review when the issue affects reproducibility, fairness, evidence, metric interpretation, or claim support.
- Use adversarial review when the issue undermines novelty, core validation, experimental alignment, or the manuscript's main contribution.

Never invent experiments, baselines, datasets, statistics, or measurements. If the paper does not provide enough information, phrase the reviewer comment as a request for clarification or as a limitation.

## Example 1, novelty framed as standard tool use

Trigger:

> The paper says a standard optimizer, architecture search method, statistical tool, or well-known algorithm is underexplored and presents its use as the main contribution.

Likely reviewer concern:

> The manuscript should clarify what is new beyond applying a known tool. Is the contribution methodological, empirical, comparative, or deployment-oriented?

What to check:

- Whether the paper claims novelty from tool usage alone.
- Whether the contribution is isolated from the components used.
- Whether controlled variables are stated, such as representation, split, search budget, objective, and protocol.

Candidate comment angle:

> The novelty statement should be sharpened. At present, the manuscript appears to rely on applying an established tool to the target problem, but it is not clear whether the original contribution is a new method, a controlled empirical comparison, a deployment study, or a new evaluation protocol.

## Example 2, contribution sounds like a loose combination of known components

Trigger:

> The contribution is presented as a combination of several familiar modules.

Likely reviewer concern:

> The core contribution is integration-driven and not clearly isolated.

What to check:

- Whether the paper explains why the integration answers a specific scientific or engineering question.
- Whether each component is known and the paper only concatenates them.
- Whether the authors distinguish implementation novelty from methodological novelty.

Candidate comment angle:

> The contribution should be separated from the list of components. The manuscript should explain what insight or capability emerges from the proposed combination that is not already implied by the individual known modules.

## Example 3, universal superiority is implied from limited evidence

Trigger:

> The paper says the proposed method is best, superior, or outperforms prior work without strict scoping.

Likely reviewer concern:

> The result may hold only for one metric, one protocol, one benchmark, or one subset of baselines.

What to check:

- Whether all metrics support the superiority claim.
- Whether the compared set is complete and controlled.
- Whether the claim is limited to the actual benchmark and protocol.

Candidate comment angle:

> The performance claim should be scoped more carefully. The manuscript should specify the metric, protocol, and compared baselines for which the proposed method is strongest, and it should avoid implying superiority across all operating points if some metrics remain competitive for prior methods.

## Example 4, small numerical gains are treated as decisive

Trigger:

> A very small numerical difference is described as an improvement or gain.

Likely reviewer concern:

> The difference may be within run-to-run variability or measurement noise.

What to check:

- Whether the paper reports repeated runs, confidence intervals, standard deviations, or statistical tests.
- Whether the practical contribution is actually cost, latency, memory, or simplicity rather than accuracy.

Candidate comment angle:

> The manuscript should avoid presenting marginal numerical differences as decisive improvements unless supported by variability analysis. If the difference is within expected run-to-run variation, the result should be framed as comparable performance with another practical advantage.

## Example 5, statistical superiority is implied without paired evidence

Trigger:

> The paper compares against prior aggregate results and suggests statistical superiority.

Likely reviewer concern:

> Aggregate-only comparisons are descriptive unless paired predictions, repeated runs, or compatible uncertainty estimates are available.

What to check:

- Whether prior baselines were reproduced locally.
- Whether per-sample predictions or repeated-run statistics are available.
- Whether the word `significant` is used without a statistical basis.

Candidate comment angle:

> The comparison with prior work should be described as descriptive unless the authors have paired predictions or repeated-run evidence. The manuscript should avoid language suggesting statistical superiority over externally reported baselines when only aggregate values are available.

## Example 6, generalization is hidden in the conclusion

Trigger:

> The conclusion generalizes from one dataset, simulation, site, device, or preprocessing choice.

Likely reviewer concern:

> The result may not transfer to different datasets, hardware, operating conditions, codebooks, environments, or real-world measurements.

What to check:

- Whether the paper is based on a single benchmark or simulated dataset.
- Whether deployment or generalization claims are stated broader than the evidence.
- Whether concrete domain-gap mechanisms are discussed.

Candidate comment angle:

> The conclusion should be scoped to the adopted dataset, representation, hardware, and protocol. The manuscript should state which factors may change the reported ranking or absolute performance, rather than implying a general deployment rule.

## Example 7, representation may bias the model comparison

Trigger:

> A shared representation is used to compare different model families.

Likely reviewer concern:

> The representation may favor one architecture family and handicap another.

What to check:

- Whether the input structure is flattened, aggregated, tokenized, gridded, or graph-constructed.
- Whether each family receives a representation compatible with its inductive bias.
- Whether natural baselines are excluded without justification.

Candidate comment angle:

> The manuscript should discuss whether the chosen representation biases the model-family comparison. If one architecture family is better aligned with the encoding, the observed ranking should be interpreted as conditional on that representation rather than architecture-invariant.

## Example 8, search-space fairness is left implicit

Trigger:

> The paper compares multiple model families using search or tuning.

Likely reviewer concern:

> The fairness of budgets, parameter ranges, pruning rules, depth constraints, and objectives is unclear.

What to check:

- Whether all families used the same split, objective, trial budget, and stopping criteria.
- Whether family-specific spaces have comparable depth, width, regularization, and deployment constraints.
- Whether logs or sampled configurations are available.

Candidate comment angle:

> The cross-family comparison would be stronger if the authors clarified search-space fairness. In particular, the manuscript should state whether the budgets, parameter ranges, pruning rules, depth constraints, and optimization objectives were comparable across the evaluated families.

## Example 9, static complexity and runtime are treated as interchangeable

Trigger:

> The paper assumes fewer operations necessarily imply lower latency.

Likely reviewer concern:

> Static complexity and measured runtime can diverge because of memory access, kernel launch overhead, backend implementation, conditional paths, and hardware utilization.

What to check:

- Whether latency protocol is defined.
- Whether device, batch size, warm-up, synchronization, and repetitions are stated.
- Whether surprising complexity-latency inversions are explained.

Candidate comment angle:

> The complexity and latency discussion should distinguish static operation counts from measured runtime. The manuscript should define the latency protocol and explain any cases where the ordering of runtime differs from the ordering of FLOPs or parameter count.

## Example 10, deployment claims rely on one measurement dimension

Trigger:

> The paper claims deployment readiness based only on latency, FLOPs, accuracy, or GPU timing.

Likely reviewer concern:

> Practical deployment also depends on memory, synchronization, robustness, distribution drift, integration constraints, and sustained operation.

What to check:

- Whether the target device and workload are representative.
- Whether power, memory, input/output, preprocessing, and postprocessing are included.
- Whether environmental or operational constraints are acknowledged.

Candidate comment angle:

> The deployment claim should be narrowed. The reported measurements support one aspect of deployment feasibility, but the manuscript should also discuss remaining constraints such as memory, synchronization, robustness, distribution shift, sustained power, and integration with the target system.

## Example 11, proxy metric is presented as full system evaluation

Trigger:

> A proxy metric is used to claim system-level or communication-level performance.

Likely reviewer concern:

> The proxy may not include all physical, operational, or downstream effects.

What to check:

- Whether the metric is derived from rankings, scores, heuristics, or partial simulation.
- Whether full end-to-end validation is actually performed.
- Whether exclusions are stated.

Candidate comment angle:

> The manuscript should explicitly identify this metric as a proxy. It should state what the metric captures and what it excludes, and it should avoid implying a full end-to-end system evaluation unless such an evaluation is actually reported.

## Example 12, methodology workflow is too dense

Trigger:

> Algorithms or method paragraphs combine preprocessing, training, search, model selection, and evaluation in one dense block.

Likely reviewer concern:

> The workflow is difficult to follow even if the technical steps are correct.

What to check:

- Whether the method is introduced with a stage-level roadmap.
- Whether a flowchart or conceptual diagram is needed.
- Whether inputs, loops, outputs, and evaluation stages are separated.

Candidate comment angle:

> The methodology would benefit from a clearer workflow explanation. The authors should separate input processing, model construction or search, training, selection, and final evaluation, either in the text or in a simplified diagram.

## Example 13, sentences carry method, result, and interpretation at once

Trigger:

> Long sentences contain several claims, metrics, baselines, and interpretations.

Likely reviewer concern:

> Readability and comprehension suffer, especially in methodology and results sections.

What to check:

- Whether a sentence contains three or more distinct claims.
- Whether the subject changes inside the sentence.
- Whether result and interpretation should be separated.

Candidate comment angle:

> Some sentences are overly dense and should be divided. Separating method, result, and interpretation would make the manuscript easier to follow and reduce the chance of misinterpretation.

## Example 14, figure-quality claims are incomplete

Trigger:

> The paper says figures are high quality or vector format without checking readability after publication scaling.

Likely reviewer concern:

> Labels may be unreadable in two-column format, and a PDF/EPS container may still contain rasterized bitmap content.

What to check:

- Whether figure labels remain readable after resizing.
- Whether panels, arrows, legends, and annotations are legible.
- Whether vector graphics are truly vector, not raster images embedded in vector containers.

Candidate comment angle:

> The authors should verify figure readability in the final venue format. In particular, internal labels, legends, and annotations should remain readable after two-column resizing, and submitted PDF/EPS figures should not merely embed low-resolution raster images.

## Example 15, end-to-end system is claimed but only one module is evaluated

Trigger:

> The paper claims an end-to-end system but evaluates only a detector, classifier, predictor, or isolated module.

Likely reviewer concern:

> The core end-to-end contribution is unsupported by empirical evidence.

What to check:

- Whether downstream logic, decisions, alerts, control, or final system outputs are evaluated.
- Whether module-level and system-level metrics are distinguished.
- Whether the abstract and contributions overstate the evaluated scope.

Candidate comment angle:

> The experiments do not fully support the end-to-end framing. The manuscript should distinguish implemented modules from quantitatively validated modules and should avoid presenting module-level results as evidence of complete system-level performance.

## Example 16, results do not align with the stated theme

Trigger:

> The introduction and method emphasize one contribution, but the results focus on a different or narrower component.

Likely reviewer concern:

> The experimental section does not validate the central claim of the paper.

What to check:

- Whether the stated theme appears in the evaluation metrics.
- Whether the core module has quantitative results.
- Whether the discussion explains what remains unvalidated.

Candidate comment angle:

> The experimental design should be aligned more closely with the stated contribution. If the paper emphasizes a complete pipeline or decision module, the results should include metrics for that component or explicitly state that the evaluation is limited to a narrower subsystem.

## Example 17, motivation remains qualitative

Trigger:

> The paper motivates the work with broad claims such as real-time, low-power, safety-critical, costly, or practical, but gives no quantitative context.

Likely reviewer concern:

> The need for the proposed design is not sufficiently justified.

What to check:

- Whether bottlenecks of existing methods are quantified.
- Whether compute, memory, latency, power, cost, or data constraints are connected to design choices.
- Whether alternatives are acknowledged.

Candidate comment angle:

> The motivation should be made more quantitative. The manuscript should explain which bottlenecks in existing approaches motivate the proposed design and how the target constraints shape the architecture, input resolution, runtime backend, or evaluation metrics.

## Example 18, interpretability is overclaimed

Trigger:

> The paper calls a rule-based, attention-based, fuzzy, saliency, or transparent-looking component interpretable.

Likely reviewer concern:

> Interpretability may not have been validated by users, experts, or task-specific evidence.

What to check:

- Whether interpretability means inspectability, explainability, causal validity, human usefulness, or regulatory transparency.
- Whether rules or explanations were manually designed.
- Whether user, expert, or annotation-based validation exists.

Candidate comment angle:

> The interpretability claim should be scoped. If no user study, expert validation, or explanation-faithfulness analysis is provided, the manuscript should describe the component as inspectable or transparent rather than empirically validated as interpretable.

## Example 19, known failure modes of a lightweight component are left unqualified

Trigger:

> The paper uses a lightweight classical, heuristic, or simplified component in a safety, deployment, or robustness-sensitive setting.

Likely reviewer concern:

> Known edge-case failures are not discussed or compared against stronger alternatives.

What to check:

- Whether low-light, high-speed, noise, occlusion, drift, calibration, synchronization, sparse data, or domain shift can break the component.
- Whether the paper implies robustness without evidence.
- Whether alternative methods are considered.

Candidate comment angle:

> The manuscript should acknowledge the known failure modes of the lightweight component and clarify whether those edge cases were evaluated. If they were not evaluated, the limitation should be stated and stronger alternatives should be considered as future work or comparison baselines.

## Example 20, unified dataset wording hides imbalance and source heterogeneity

Trigger:

> The paper describes a unified dataset, merged label space, harmonized benchmark, or combined corpus.

Likely reviewer concern:

> The scale, diversity, annotation quality, class imbalance, and source heterogeneity are unclear.

What to check:

- Whether all data sources are named and characterized.
- Whether class counts, rare classes, and adverse-condition coverage are reported.
- Whether label remapping and annotation consistency are discussed.
- Whether baselines use the same training strategy and split.

Candidate comment angle:

> The dataset construction needs more detail. The manuscript should report source composition, label remapping, class imbalance, annotation consistency, and rare-class coverage so that readers can interpret aggregate metrics and failure cases correctly.

## Example 21, error source is noted but not analyzed

Trigger:

> The paper says a failure mode is the main error source but gives no mechanism or mitigation.

Likely reviewer concern:

> The discussion is descriptive rather than analytical.

What to check:

- Whether confusion, false positives, false negatives, or background errors are explained.
- Whether likely causes are connected to data, model, resolution, labels, or operating conditions.
- Whether concrete mitigation strategies are proposed.

Candidate comment angle:

> The error analysis should go beyond naming the dominant failure mode. The authors should discuss plausible causes and mitigation strategies, such as class-aware sampling, higher resolution, stratified analysis, temporal filtering, calibration, or targeted data collection.

## Example 22, false positives from static context are dismissed too easily

Trigger:

> The paper claims that decision logic filters irrelevant or static context.

Likely reviewer concern:

> Static or stationary objects may still trigger false positives without explicit calibration, context modeling, or motion compensation.

What to check:

- Whether the filtering rule is described.
- Whether false positives are measured.
- Whether motion, persistence, priors, geometry, or calibration are used.

Candidate comment angle:

> The manuscript should clarify how false positives from static or stationary context are handled. If no explicit mechanism or evaluation is provided, this should be treated as a limitation rather than an established capability.

## Example 23, custom throughput metric is treated as complete throughput

Trigger:

> The paper introduces a workload-dependent throughput metric and uses it as if it were frame-level throughput.

Likely reviewer concern:

> The metric may fluctuate with scene density or workload and cannot independently characterize processing speed.

What to check:

- Whether the custom metric is precisely defined.
- Whether per-frame latency or FPS is also reported.
- Whether workload density and stage timing are included.

Candidate comment angle:

> The custom throughput metric should not replace frame-level latency or processed frames per second. The manuscript should define the metric precisely and interpret it together with workload density, FPS, per-frame latency, and stage-level timing.

## Example 24, power and energy efficiency are under-specified

Trigger:

> The paper reports power, energy, or efficiency without protocol details.

Likely reviewer concern:

> Results may not be reproducible or comparable to published systems.

What to check:

- Whether the measurement boundary is defined.
- Whether the measurement instrument, sampling period, warm-up, idle subtraction, and workload are described.
- Whether external comparisons use comparable conditions.

Candidate comment angle:

> The power and energy-efficiency analysis requires a clearer protocol. The authors should state the measurement boundary, instrumentation, warm-up, sampling period, idle handling, and workload, and should avoid broad efficiency claims unless comparisons are made under compatible conditions.

## Example 25, bottlenecks are hidden behind aggregate latency

Trigger:

> The paper reports only aggregate latency while discussing bottlenecks or scalability.

Likely reviewer concern:

> Without stage decomposition, readers cannot reproduce the timing or identify the performance bottleneck.

What to check:

- Whether latency includes preprocessing, inference, postprocessing, tracking, decision logic, I/O, synchronization, and output generation.
- Whether scaling to higher resolution, larger batch, or denser scenes is discussed.
- Whether stage-level profiling exists.

Candidate comment angle:

> The latency analysis should define the measured interval and, ideally, decompose timing by stage. If only end-to-end latency is reported, the manuscript should avoid attributing bottlenecks to specific modules without profiling evidence.

## Example 26, baseline fairness is under-specified

Trigger:

> The paper compares against a baseline but omits training or evaluation details.

Likely reviewer concern:

> The comparison may reflect different preprocessing, augmentation, loss, resolution, thresholds, or postprocessing rather than the method itself.

What to check:

- Whether splits, input resolution, augmentation, training schedule, loss, thresholds, postprocessing, and evaluation scripts are the same.
- Whether baseline implementations are reproduced or cited from prior work.
- Whether differences are acknowledged.

Candidate comment angle:

> The baseline comparison needs stronger fairness documentation. The manuscript should state which training and evaluation settings are shared across methods and which settings differ, especially preprocessing, augmentation, loss, resolution, thresholds, postprocessing, and evaluation scripts.

## Example 27, published-method comparison is too broad

Trigger:

> The paper compares to published systems with different datasets, hardware, labels, or metrics.

Likely reviewer concern:

> The comparison may be contextual rather than controlled.

What to check:

- Whether the paper directly compares under the same dataset, platform, and protocol.
- Whether published results are used only for context.
- Whether limitations of cross-paper comparison are stated.

Candidate comment angle:

> The comparison with published methods should distinguish controlled baselines from contextual related work. If datasets, platforms, labels, input resolutions, or metrics differ, the manuscript should avoid implying direct superiority.

## Example 28, adverse-condition robustness is overgeneralized

Trigger:

> The paper claims robustness or generalization across conditions that are sparse or absent in the data.

Likely reviewer concern:

> The evidence does not support robustness under rare, adverse, or degraded conditions.

What to check:

- Whether condition distributions are reported.
- Whether stress tests or condition-stratified results are available.
- Whether limitations and future work acknowledge missing conditions.

Candidate comment angle:

> The robustness claim should be narrowed. The manuscript should report the distribution of adverse or rare conditions and should avoid interpreting aggregate results as evidence of robustness in conditions that are underrepresented or untested.

## Example 29, table ordering, alignment, and terminology create reviewer friction

Trigger:

> Tables are hard to read, ordered unexpectedly, or use inaccurate terminology.

Likely reviewer concern:

> Presentation issues reduce credibility and can obscure the technical contribution.

What to check:

- Whether related-work entries are ordered by citation, chronology, category, or another clear rationale.
- Whether row and column alignment is correct in the compiled PDF.
- Whether terms such as multi-modal, multi-class, multi-object, multi-task, single-sensor, and multi-sensor are used accurately.

Candidate comment angle:

> The tables should be revised for readability and terminology accuracy. The authors should clarify the ordering rationale, check row and column alignment in the compiled version, and ensure that terms such as multi-modal or multi-task match the actual system design.

## Example 30, acronym and spelling inconsistencies weaken credibility

Trigger:

> Acronyms, title terms, labels, captions, or figure text are undefined or inconsistent.

Likely reviewer concern:

> The manuscript appears less mature even if the technical work is sound.

What to check:

- Whether title acronyms are defined at first mention.
- Whether acronyms are used consistently in abstract, body, figures, and conclusion.
- Whether figure labels contain spelling variants not present in the text.

Candidate comment angle:

> The manuscript should check acronym definition and spelling consistency across the title, abstract, body text, figures, and tables. Figure text should be treated as part of the manuscript because reviewers read it with the same scrutiny as the main text.

## Example 31, title or table claims enumerate capabilities that are not analyzed

Trigger:

> A title, abstract, contribution list, or table enumerates many classes, tasks, modules, or capabilities, but the experiments analyze only aggregate or partial performance.

Likely reviewer concern:

> The manuscript advertises capabilities that are not supported by the evaluation.

What to check:

- Whether each advertised capability is evaluated or explicitly scoped.
- Whether rare or safety-critical classes are analyzed separately.
- Whether aggregate metrics hide class-level or function-level failures.

Candidate comment angle:

> The manuscript should align capability claims with the evidence provided. If the paper advertises multiple classes, tasks, or downstream functions, the results should discuss class-level or function-level performance rather than relying only on aggregate metrics.

## Example 32, configurations called equivalent are not traceably the same

Trigger:

> Controlled and field experiments are said to use the same implementation, but the apparatus is identified completely in only one condition.

What to check:

- Whether the receiver, front end, gain, filtering, antenna path, calibration, and digital chain are explicitly matched.
- Whether a hardware or settings change could explain the cross-condition result.

Candidate comment angle:

> The controlled setup identifies the receiver and signal path, whereas the field description states only that the processing operations are preserved. Were both conditions acquired with the same receiver front end and settings? This should be explicit because an apparatus change could contribute to the reported difference.

## Example 33, null-condition calibration assumes an operational reference that may not exist

Trigger:

> Thresholds or normalization parameters are learned from verified negative, empty, healthy, or noise-only observations and the environment varies over time.

What to check:

- How the reference state is verified without circular use of the method under test.
- How often calibration is updated and what drift invalidates it.
- Whether the reference state is realistically available during deployment.

Candidate comment angle:

> The threshold procedure depends on a verified reference condition, while the results show that the background distribution changes across measurements. How would the system obtain and refresh that reference during operation, and what criterion would trigger recalibration? The practical feasibility of the thresholding claim depends on these assumptions.

## Example 34, a held-out subset is disjoint but not demonstrably independent

Trigger:

> A single recording, subject, run, or sequence is divided into calibration and validation subsets.

What to check:

- Whether the split is random, chronological, blocked, grouped, or stratified.
- Whether alternative splits give stable results.
- Whether dependence or leakage crosses the split boundary.

Candidate comment angle:

> The manuscript reserves a held-out subset from the same acquisition but does not explain how the split was formed. Was it randomized, chronological, or blocked, and are the conclusions stable across alternative valid splits? Disjoint samples alone do not establish independent validation when they share an acquisition.

## Example 35, qualitative regimes drive the conclusion without a reproducible assignment rule

Trigger:

> Results are organized by labels such as Gaussian, impulsive, adverse, clean, noisy, easy, or difficult based mainly on representative plots.

What to check:

- Which statistic or decision rule assigns a recording to each regime.
- Whether the rule is applied to the disturbance or to a signal-contaminated observation.
- Whether the condition was selected before inspecting the method's performance.

Candidate comment angle:

> The comparison depends on separating the recordings into two disturbance regimes, but the current evidence is visual. What quantitative criterion assigned each acquisition to a regime, and was that rule defined independently of detector performance? A reproducible classification is needed to interpret the claimed regime-dependent behavior.

## Example 36, many windows are treated as many experiments

Trigger:

> Thousands of samples or windows are derived from one or a few recordings and then used for confidence intervals or generalization claims.

What to check:

- What the independent acquisition or experimental unit is.
- Whether temporal, spatial, subject-level, or device-level correlation reduces the effective sample size.
- Whether uncertainty is estimated across independent acquisitions or only derived observations.

Candidate comment angle:

> The reported realizations are consecutive windows from one acquisition rather than independent measurement campaigns. How does within-record dependence affect the effective sample size and the reported uncertainty? The distinction is important because more windows improve within-record estimation but do not establish repeatability across conditions.

## Example 37, one channel or case supports a deployment-level conclusion

Trigger:

> A central comparison uses one positive-negative pair, one site, one device, or one operating condition.

What to check:

- Whether the case was selected by a predeclared rule.
- Whether the conclusion is framed as illustrative or representative.
- Whether independent cases show the same ordering.

Candidate comment angle:

> The central comparison is based on one paired condition. How was this pair selected, and does the ordering persist across other independently acquired pairs? Without that information, the result should be framed as evidence for the measured case rather than a general deployment recommendation.

## Example 38, reproducibility details are requested without their scientific purpose

Trigger:

> A draft review asks for a long list of hardware and acquisition metadata without connecting it to a result.

What to check:

- Which omitted setting could change the conclusion, comparison, or ability to reproduce the measurement.
- Whether separate uncertainties should become separate focused comments.

Candidate comment angle:

> The field results vary with receiver gain and antenna placement, but those settings are not linked to the reported acquisitions. Please identify the settings used for each condition and explain whether they were held fixed. This is needed to distinguish detector behavior from changes in the measurement chain.
