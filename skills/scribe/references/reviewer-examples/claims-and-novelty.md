# Reviewer Examples: Claims and Novelty

Use this file only when the current paragraph or section contains the corresponding claim type. Apply the examples during the single reviewer-informed revision pass. Preserve supplied facts, numbers, citations, labels, equations, and terminology.

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
