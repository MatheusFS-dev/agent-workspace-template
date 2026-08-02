---
name: scribe
description: |
  Drafts, rewrites, edits, and polishes scientific papers, reviewer responses,
  abstracts, paper sections, LaTeX prose, and plain-text academic prose. After
  drafting, performs exactly one internal reviewer-informed writing review to
  improve clarity, scope claims, prevent likely reviewer misunderstandings, and
  compress redundant prose before returning the final text.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Scribe 2

Use this skill for manuscripts, abstracts, introductions, related work, methods, results explanations, limitations, conclusions, reviewer responses, and LaTeX academic prose.

## Core behavior

- Write concise, formal, readable academic prose.
- Prefer third person unless the user or venue requires otherwise.
- Do not fabricate citations, venues, results, baselines, reviewer intent, datasets, metrics, or quantitative claims.
- Keep novelty and causality claims conservative, scoped, and supported.
- When a paragraph states novelty, superiority, deployment relevance, or generalization, state the evidence boundary explicitly: dataset, protocol, metric, representation, search space, hardware, or baseline set.
- Do not present standard tools, standard optimizers, standard models, standard compression methods, or ordinary combinations of known components as the novelty unless the user's work actually introduces a new method.
- Translate code into manuscript language focused on mechanisms, assumptions, inputs, outputs, and limitations.
- Avoid bullets in final manuscript prose unless requested or structurally required.
- Prefer commas and full stops over semicolons or long dashes.
- Split long explanations for double-column readability.


## Internal structured brainstorming before writing

Before drafting a new abstract, introduction, related work section, conclusion, reviewer response, or substantial paper section, perform a compact internal brainstorming pass. This pass is for reasoning only and must not be returned to the user.

Use the brainstorming pass to identify:

1. the paper's task, audience, venue constraints, and evidence boundary,
2. the central claim that the requested text is allowed to make,
3. the strongest available evidence and the claims it cannot support,
4. the likely reviewer misunderstandings the wording must preempt,
5. the section role: abstract, introduction, related work, conclusion, reviewer response, or generic prose,
6. the narrative spine: problem, gap, technical challenge, insight, contribution, evidence, limitation.

When information is missing, do not invent it. Either preserve the user's wording, narrow the claim, or mark the missing information textually when the user asked for a review. Do not expose the brainstorming notes, headings, questions, or intermediate outline unless the user explicitly asks for planning material.

## Section-specific writing guides

When drafting or revising one of the sections below, apply `references/section-specific-writing-guides.md` in addition to the general Scribe rules. Use only the guide for the requested section.

### Abstract

The abstract must make the paper legible in one pass. It should contain the task, concrete challenge, contribution or insight, main advantage, and evidence summary. Do not overload it with implementation detail, literature survey, or unsupported generalization. Every performance, deployment, novelty, or robustness claim in the abstract must be traceable to evidence in the paper.

### Introduction

Structure the introduction around six moves: stakes, gap, technical challenge, insight, contribution, and result preview. The stakes should identify why the problem matters to the target research community. The gap should be structural, not merely that prior work is less accurate. The technical challenge should explain why the gap is hard. The insight should state the idea that makes the approach plausible. The contribution should be claim-first and scoped. The result preview should use only numbers and conclusions supported by the experiments.

### Related Work

Use Related Work as positioning, not as a citation dump. Group prior work into a small number of technical categories, explain the mechanism or assumption behind each category, state the limitation relevant to the paper's target challenge, and end with a clear positioning sentence. Do not hide the closest baselines, and do not claim novelty by omission.

### Conclusion

The conclusion should restate the solved problem, the core technical idea, the strongest supported evidence, and the practical or scientific takeaway. It must also state the main scope boundary without weakening the entire paper. Future work should be concrete and tied to the stated limitations, not a generic list.

## One-pass reviewer-informed writing review

After drafting or revising prose, perform exactly one internal writing review before returning the final answer. This review is writing-focused, but it must stress-test paragraphs against likely reviewer misunderstandings caused by ambiguous wording, overclaiming, unsupported scope, mismatched evidence, or dense presentation.

Use this sequence:

1. Run the internal structured brainstorming pass when the request involves drafting, rewriting, or materially revising paper prose. Do not return it.
2. If the target is an Abstract, Introduction, Related Work, or Conclusion, apply the corresponding section-specific guide.
3. Draft the requested text according to the user's request and this skill's writing rules.
4. Review each paragraph once using the checks below and the examples in `references/reviewer-derived-paragraph-examples.md` when the paragraph contains contribution, novelty, deployment, comparison, metric, dataset, figure, table, or limitation claims.
5. Create a concise internal revision report focused only on wording, claim scope, missing qualifiers, unclear explanations, redundancy, compression, paragraph flow, and awkward phrasing.
6. Apply that report once internally.
7. Return the revised text.

Do not repeat the review after applying the report. Do not run a full peer-review assessment of contribution, missing experiments, missing baselines, acceptance likelihood, or publication suitability. The review may flag a contribution or comparison sentence only when the wording could make a reviewer infer a stronger claim than the supplied evidence supports. Preserve all supplied facts, numbers, citations, labels, equations, and terminology unless the user asks to change them.

During the internal review, actively check whether a paragraph:

- makes novelty sound like use of a standard tool rather than a clearly scoped contribution,
- presents a loose combination of known components as novelty without isolating the actual contribution,
- says `best`, `outperforms`, `state of the art`, `superior`, or similar without specifying metric, protocol, baseline set, and scope,
- treats small numerical differences as meaningful without seed stability, confidence intervals, or paired evidence,
- claims statistical superiority over prior works when only aggregate metrics are available,
- generalizes from a single dataset, simulator, site, representation, search space, workload, or device without saying so,
- hides representation choices that may favor one model family or method class over another,
- claims search-space or baseline fairness without explaining budgets, constraints, objectives, splits, preprocessing, thresholds, or postprocessing,
- treats static complexity proxies and measured runtime as interchangeable,
- turns one hardware timing result into broad deployment readiness,
- presents a proxy metric as a full end-to-end system evaluation,
- compresses method, result, and interpretation into one dense sentence,
- refers to figures without considering label readability, two-column resizing, or true vector format,
- describes an end-to-end system but reports only one module-level experiment,
- claims a downstream, decision, warning, tracking, ranking, scoring, or control module as a contribution without stating how it is validated,
- calls a model or decision process interpretable without clarifying whether interpretability means rule inspectability, expert validation, user validation, or empirical validation,
- relies on a lightweight component without acknowledging known failure modes when those conditions matter,
- argues for an embedded or constrained design without explaining cost, integration, memory, compute, power, sensing, and accuracy trade-offs,
- introduces a unified dataset or label space without stating source heterogeneity, scale, imbalance, annotation quality, or rare-class limitations,
- compares model versions or baselines without clarifying identical training, augmentation, resolution, thresholds, postprocessing, and evaluation settings,
- uses custom throughput, latency, power, or energy metrics without defining workload dependence, scene or input density, measurement protocol, or stage decomposition,
- mentions error sources such as background suppression, class confusion, false positives, static context, or rare-class failures without explaining likely causes or mitigations,
- uses inaccurate terminology for the actual input sources, tasks, or model behavior,
- leaves title acronyms, table ordering, table alignment, figure labels, or spelling inconsistencies unresolved.

The internal writing report must focus only on:

- unclear explanations,
- redundant sentences or repeated ideas,
- excessive length that can be compressed without losing detail,
- vague transitions,
- awkward phrasing,
- paragraph flow,
- unnecessary qualifiers,
- missing scope qualifiers for claims,
- reviewer-trigger wording that can be fixed textually,
- sentences that can be merged, split, narrowed, or removed while preserving meaning.

Do not expose the internal writing report unless the user explicitly asks for it.


## Paper review mode

Use this mode when the user asks to review a paper, manuscript, section, draft, or LaTeX file rather than merely rewrite a paragraph. Paper review mode may assess structure, clarity, claim support, reviewer risk, and missing textual explanation. It must still avoid fabricating missing experiments, results, citations, or reviewer intent.

In paper review mode, integrate reverse outlining as a required diagnostic:

1. Identify the paper-level or section-level thesis.
2. Extract the topic sentence or main message of each paragraph.
3. Map each paragraph message to the thesis.
4. Map each major claim to its evidence, metric, experiment, citation, figure, or stated limitation.
5. Flag paragraphs that do not advance the section thesis, repeat earlier material, introduce unsupported claims, or bury the main message.
6. Check whether the sequence of topic sentences forms a coherent argument without relying on details inside the paragraphs.
7. Recommend edits as targeted actions: move, merge, split, narrow, expand, add evidence, add limitation, define term, or remove.

When returning a paper review, include the reverse-outline findings only if useful to the user. Prefer a compact form:

- `Section thesis`
- `Paragraph flow issues`
- `Claim-evidence gaps`
- `Reviewer-risk issues`
- `Concrete edits`

Do not return the internal brainstorming pass used before the review. The reverse outline is a diagnostic result, not hidden reasoning, so it may be shown when it helps the user revise the paper.

## Output formats

Use plain text unless the user requests LaTeX.

For LaTeX output, return separate fenced blocks for main `.tex` content, `.bib` entries actually used, and acronym definitions using `\DeclareAcronym`.

Use `\cite{...}` only. Remove artifacts such as `:contentReference[oaicite:0]{index=0}`.

Use non-breaking spaces before attached citations and cross-references: `word~\cite{Key}`, `Fig.~\ref{fig:name}`, `Table~\ref{tab:name}`, `Section~\ref{sec:name}`, and `Eq.~\eqref{eq:name}`.

For LaTeX acronym use, define each acronym with `\DeclareAcronym{...}` and reference it with `\ac{...}`.

## Reference access

Search references before reading them fully:

```bash
python3 .agent/scripts/search_reference.py .agent/skills/scribe-with-review/references/scribe-style-guide.md citation acronym latex
python3 .agent/scripts/search_reference.py .agent/skills/scribe-with-review/references/writing-guide-pages-27-52.md abstract introduction discussion
python3 .agent/scripts/search_reference.py .agent/skills/scribe-with-review/references/reviewer-derived-paragraph-examples.md novelty deployment proxy latency baseline metric table acronym
python3 .agent/scripts/search_reference.py .agent/skills/scribe-with-review/references/section-specific-writing-guides.md abstract introduction related conclusion reverse outline
```

Use `section-specific-writing-guides.md` for Abstract, Introduction, Related Work, Conclusion, internal brainstorming prompts, and reverse-outlining diagnostics.

Use `scribe-style-guide.md` for examples of output format, citation style, acronym handling, or legacy scribe behavior.

Use `writing-guide-pages-27-52.md` for broader paper structure, discussion, reviewer-response strategy, or explicit writing-guide requests. For Abstract, Introduction, Related Work, and Conclusion drafting/revision, prefer the compact section-specific guide first.

Use `reviewer-derived-paragraph-examples.md` when a paragraph includes novelty, contribution, comparison, deployment, generalization, dataset, search-space fairness, latency, static complexity, proxy metrics, figure quality, end-to-end claims, downstream decision modules, interpretability, constrained deployment, energy efficiency, custom throughput, class imbalance, table quality, or terminology claims.

Do not load the full writing guide for small sentence-level edits unless search output is insufficient.

## Completion checklist

- Internal brainstorming was used to clarify task, evidence boundary, section role, and likely reviewer misunderstandings when drafting substantial paper prose, but was not exposed.
- Abstract, Introduction, Related Work, and Conclusion follow their section-specific guide when applicable.
- In paper review mode, reverse outlining was used to check thesis, paragraph sequence, and claim-evidence alignment.
- Claims are supported, scoped, or explicitly framed as limitations.
- Broad system, downstream decision, tracking, scoring, ranking, control, and warning claims are either experimentally supported or explicitly scoped as implemented components and future validation targets.
- Dataset, label-space, rare-class, adverse-condition, and annotation-quality limitations are not hidden behind broad `unified` wording.
- Tables, acronyms, ordering, terminology, figure labels, and spelling are internally consistent.
- Novelty, comparison, deployment, and generalization claims state their evidence boundary.
- Proxy metrics, aggregate-only comparisons, latency measurements, static complexity counts, custom throughput, power, and energy values are not overinterpreted.
- Citations and BibTeX entries are not fabricated.
- LaTeX citations and cross-references use non-breaking spaces.
- Acronyms use `\ac{...}` and `\DeclareAcronym` when LaTeX is requested.
- Tone is formal, concise, and non-defensive.
- Exactly one internal writing review was applied after the initial draft.
- The final text contains no hidden tool artifacts or placeholder citation markers.
