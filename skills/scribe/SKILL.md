---
name: scribe
description: Use when drafting, rewriting, reviewing, planning, or polishing scientific manuscripts, academic sections, reviewer responses, LaTeX prose, or research writing.
allowed-tools:
  - Read
  - Grep
  - Glob
---

# Scribe

This package is one skill. Files under `references/` are supporting modules, not separately discoverable skills.

## Mandatory Rule

Apply this skill before academic-writing work. Classify the request, establish what must be preserved and what the evidence permits, then load only the files named by the routing table. Do not load every reference.

Do not invent citations, results, metrics, baselines, reviewer intent, or evidence.

## Classification

Classify along both dimensions.

**Operation**

- **Draft:** create new academic prose.
- **Rewrite:** transform supplied prose without changing its scientific content.
- **Review:** diagnose structure, clarity, support, and reviewer risk without silently replacing the manuscript.
- **Reviewer response:** answer comments and describe only supported manuscript changes.

**Scope**

- **Micro:** one sentence or short paragraph with a clear transformation.
- **Bounded:** one section, subsection, response item, or defined review target.
- **Manuscript-scale:** multiple sections, a full manuscript, or structural changes affecting section responsibilities.

Use the heavier scope when uncertain. Upgrade if hidden complexity appears.

## Hard Gates

1. **Design:** Do not draft manuscript-scale work before explicit approval of a section-level design.
2. **Evidence:** Wording cannot strengthen a claim beyond the supplied evidence boundary.
3. **Preservation:** Rewriting does not authorize changes to facts, numbers, units, citations, equations, labels, terminology, or measured versus proposed status.
4. **Revision:** Every drafted or materially rewritten deliverable receives exactly one reviewer-informed revision pass.
5. **Verification:** Verification checks the revised artifact and must not become a second general rewrite.

## Routing Table

| Request | Load |
|---|---|
| Sentence or paragraph drafting or rewriting | `references/workflows/drafting-academic-prose.md`, then `quality-control.md` |
| Abstract | Drafting, `references/sections/abstract.md`, then quality control |
| Introduction | Drafting, `references/sections/introduction.md`, then quality control |
| Related Work | Drafting, `references/sections/related-work.md`, then quality control |
| Conclusion | Drafting, `references/sections/conclusion.md`, then quality control |
| Manuscript or section review | `references/workflows/reviewing-manuscripts.md`, then quality control for the review report |
| Reviewer response | `references/workflows/responding-to-reviewers.md`, then quality control |
| Manuscript-scale drafting or restructuring | `planning-manuscript-work.md`, `executing-writing-plans.md`, the relevant operation module, then quality control |
| Modifying this skill | `references/workflows/writing-scribe-skills.md` |

Load `references/scribe-style-guide.md` only for LaTeX, citations, acronyms, equations, units, or formatting. Load one topical file under `references/reviewer-examples/` only when the corresponding reviewer risk is material. Use `references/writing-guide-pages-27-52.md` only for broader publication, reproducibility, ethics, or peer-review guidance.

## Scope Paths

### Micro

1. Identify the requested transformation and preserved content.
2. Load drafting and quality control only.
3. Draft or rewrite, apply one revision, verify, and return the finished text.

Do not require a visible plan or approval gate for a clear micro edit.

### Bounded

1. Inspect only the context needed for the target.
2. Resolve only ambiguity that changes the claim, evidence boundary, section role, preserved content, or output format.
3. Load the operation module and one section or topical reference when applicable.
4. Produce the requested artifact, apply one revision when prose changed, then verify.

### Manuscript-scale

1. Inspect the manuscript context, thesis, terminology, claims, evidence, limitations, and section responsibilities.
2. Present a section-level design covering narrative architecture, claim-evidence boundaries, terminology, dependencies, and output format.
3. Stop for explicit approval.
4. Create the writing plan and execute it section by section.
5. Maintain claim, terminology, notation, and dependency consistency.
6. Apply one revision per deliverable and perform final cross-section verification.

## Critical Boundaries

- Hidden brainstorming is not a user-visible plan. Expose it only when planning material is requested.
- Review identifies problems and actions. It does not silently rewrite passages.
- Reviewer comments do not override the manuscript evidence or the user's scientific position.
- Objective corrections found during verification are permitted. A new general polishing pass is not.
- Archived files under `docs/` are for traceability, not normal context.

## Stop Conditions

Stop and report the exact limitation when an essential source is missing, requirements conflict, a requested claim lacks support, or a structural discovery invalidates an approved manuscript plan. Do not fill the gap with plausible academic prose.
