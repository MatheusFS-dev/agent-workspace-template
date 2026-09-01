# Reviewer Examples: Deployment and Efficiency

Use this file only when the current paragraph or section contains the corresponding claim type. Apply the examples during the single reviewer-informed revision pass. Preserve supplied facts, numbers, citations, labels, equations, and terminology.

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
