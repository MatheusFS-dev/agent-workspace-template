# Section-Specific Writing Guides for Scribe

Use this file only when drafting, rewriting, or reviewing an Abstract, Introduction, Related Work, or Conclusion, or when running paper review mode with reverse outlining. These guides are compact. They are meant to steer the final writing, not to be returned as a planning artifact unless the user asks for an outline or review.

## Internal Brainstorming Before Writing

Before writing substantial paper prose, answer these questions internally:

1. What is the exact task or research problem?
2. What is the paper allowed to claim based on the supplied evidence?
3. What evidence is available: experiments, theory, analysis, baselines, ablations, figures, citations, or reviewer comments?
4. Which claims would be overclaims if stated broadly?
5. What would a skeptical reviewer likely misunderstand or challenge?
6. What is the required section role: abstract, introduction, related work, conclusion, response, or generic prose?
7. What is the narrative spine: stakes, gap, challenge, insight, contribution, evidence, limitation?

Do not expose these notes. Use them to decide claim strength, ordering, missing qualifiers, and what not to say.

## Abstract Guide

### Purpose

The abstract is a compressed argument. It must let a reader understand the problem, why it is hard, what was done, why it helps, and what evidence supports it.

### Recommended structure

1. Task or setting, one sentence.
2. Concrete challenge or limitation in prior approaches, one sentence.
3. Core contribution or insight, one to two sentences.
4. Main advantage, scoped to the paper's evidence.
5. Result summary with the strongest supported metrics, datasets, protocols, or settings.

### Checks

- The first two sentences should not be generic field motivation.
- The contribution should not sound like standard tool use unless the paper's contribution is explicitly empirical or deployment-oriented.
- The abstract should not promise robustness, generalization, real-time performance, interpretability, or end-to-end validation unless those are evaluated or clearly scoped.
- Numbers must match the paper and should not be interpreted beyond their measurement protocol.
- The abstract should not include implementation details that do not change the paper's contribution.

## Introduction Guide

### Six-move structure

1. Stakes: define why the problem matters and who or what is affected.
2. Gap: state the structural limitation in existing work or existing practice.
3. Technical challenge: explain why the gap is hard to close.
4. Insight: state the core idea that makes the approach plausible.
5. Contribution: state what the paper contributes, using claim-first wording and scoped evidence.
6. Result preview: give the strongest supported result or empirical takeaway.

### Move details

#### Stakes

Use domain-specific stakes, not broad technology hype. The opening should make the target venue care before introducing implementation details.

#### Gap

Prefer structural gaps over purely quantitative gaps. A structural gap explains why prior approaches are limited by design, assumptions, inputs, metrics, constraints, or deployment conditions.

#### Technical challenge

State the mechanism behind the difficulty. Do not write only that the problem is challenging. Explain whether the difficulty comes from scale, latency, data noise, synchronization, ambiguity, distribution shift, sparse labels, missing observability, hardware constraints, or conflicting objectives.

#### Insight

The insight should be one clear idea, not a list of components. It should explain why the method can address the challenge.

#### Contribution

Each contribution should be a claim that the paper supports, not merely an activity. Prefer `We show that...` only when the evaluation directly supports the claim. Otherwise use narrower wording such as `We evaluate...`, `We implement...`, or `We analyze...`.

#### Result preview

Use only results supported by the experiments. Avoid broad superiority claims when the comparison is aggregate-only, unpaired, limited to one dataset, or bounded by one preprocessing choice.

### Checks

- The introduction must not promise more than the evaluation delivers.
- Each contribution should map to a method section, experiment, figure, table, or limitation.
- The final paragraph should not contain a generic contribution list disconnected from the preceding gap.
- If a claim depends on a dataset, benchmark, representation, hardware platform, or protocol, state that scope.

## Related Work Guide

### Purpose

Related Work is a positioning section. It should explain how the paper fits into the literature and why the paper's contribution remains necessary.

### Recommended structure

1. Group prior work into two to four technical categories.
2. For each category, summarize the mechanism or assumption shared by that category.
3. State the limitation that matters for the paper's target challenge.
4. Explain the paper's distinction from the category.
5. End with a positioning sentence that names the closest relation and the exact difference.

### Checks

- Do not organize only by chronology.
- Do not give equal space to weakly related and closely related work.
- Do not hide the strongest baselines or closest papers.
- Do not write a citation dump where each sentence names one paper but no technical relation.
- Do not imply novelty because no cited paper uses the same wording. Explain mechanism, assumption, scope, or evidence differences.
- Related Work claims need citations. Do not invent missing citations.

## Conclusion Guide

### Purpose

The conclusion should close the argument without overstating it. It should leave the reader with the supported takeaway, scope boundary, and next concrete step.

### Recommended structure

1. Restate the problem and paper scope.
2. Restate the core idea or contribution.
3. Summarize the strongest evidence, with scope.
4. State the main practical or scientific implication.
5. State the main limitation or boundary.
6. Give concrete future work tied to that boundary.

### Checks

- Do not introduce new contributions, baselines, or claims in the conclusion.
- Do not claim generality beyond the tested setting.
- Do not convert limitations into vague future work.
- Do not end with generic phrases such as `future work will improve performance` without saying what will be tested, changed, or validated.
- The conclusion should be confident about supported results and precise about boundaries.

## Reverse Outlining for Paper Review Mode

Use reverse outlining to diagnose structure after reading a draft or section.

### Procedure

1. Identify the section thesis in one sentence.
2. Extract each paragraph's topic sentence or infer its main message.
3. List the evidence or explanation used by each paragraph.
4. Check whether each paragraph message supports the thesis.
5. Check whether the paragraph order forms a logical chain.
6. Check whether major claims have evidence, scope, and limitations.
7. Classify issues as move, merge, split, narrow, expand, define, support, qualify, or remove.

### Failure patterns

- A paragraph starts with background but ends with the real claim.
- Two adjacent paragraphs make the same point with different wording.
- A paragraph introduces a claim that no later experiment supports.
- A contribution appears in the introduction but not in the evaluation.
- Related Work categories do not map to the paper's actual contribution.
- The conclusion expands the paper's scope beyond the experiments.
- The abstract makes a stronger claim than the body can defend.
