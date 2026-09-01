# Reviewer Examples: Metrics and Results

Use this file only when the current paragraph or section contains the corresponding claim type. Apply the examples during the single reviewer-informed revision pass. Preserve supplied facts, numbers, citations, labels, equations, and terminology.

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
