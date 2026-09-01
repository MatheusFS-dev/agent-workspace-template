# Reviewer Examples: Terminology and Clarity

Use this file only when the current paragraph or section contains the corresponding claim type. Apply the examples during the single reviewer-informed revision pass. Preserve supplied facts, numbers, citations, labels, equations, and terminology.

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
