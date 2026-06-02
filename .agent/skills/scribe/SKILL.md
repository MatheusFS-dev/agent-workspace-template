---
name: scribe
description: |
  Drafts, rewrites, edits, and polishes scientific papers, reviewer responses,
  abstracts, paper sections, LaTeX prose, and plain-text academic prose.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Scribe

Use this skill for manuscripts, abstracts, introductions, related work, methods, results explanations, limitations, conclusions, reviewer responses, and LaTeX academic prose.

## Core behavior

- Write concise, formal, readable academic prose.
- Prefer third person unless the user or venue requires otherwise.
- Do not fabricate citations, venues, results, baselines, reviewer intent, datasets, metrics, or quantitative claims.
- Keep novelty and causality claims conservative and supported.
- Translate code into manuscript language focused on mechanisms, assumptions, inputs, outputs, and limitations.
- Avoid bullets in final manuscript prose unless requested or structurally required.
- Prefer commas and full stops over semicolons or long dashes.
- Split long explanations for double-column readability.

## Output formats

Use plain text unless the user requests LaTeX.

For LaTeX output, return separate fenced blocks for main `.tex` content, `.bib` entries actually used, and acronym definitions using `\DeclareAcronym`.

Use `\cite{...}` only. Remove artifacts such as `:contentReference[oaicite:0]{index=0}`.

Use non-breaking spaces before attached citations and cross-references: `word~\cite{Key}`, `Fig.~ef{fig:name}`, `Table~ef{tab:name}`, `Section~ef{sec:name}`, and `Eq.~\eqref{eq:name}`.

For LaTeX acronym use, define each acronym with `\DeclareAcronym{...}` and reference it with `c{...}`.

## Reference access

Search references before reading them fully:

```bash
python .agent/scripts/search_reference.py .agent/skills/scribe/references/scribe-style-guide.md citation acronym latex
python .agent/scripts/search_reference.py .agent/skills/scribe/references/writing-guide-pages-27-52.md abstract introduction discussion
```

Use `scribe-style-guide.md` for examples of output format, citation style, acronym handling, or legacy scribe behavior.

Use `writing-guide-pages-27-52.md` for paper structure, abstract, introduction, discussion, conclusion, reviewer-response strategy, or explicit writing-guide requests.

Do not load the full writing guide for small sentence-level edits unless search output is insufficient.

## Completion checklist

- Claims are supported or explicitly framed as limitations.
- Citations and BibTeX entries are not fabricated.
- LaTeX citations and cross-references use non-breaking spaces.
- Acronyms use `c{...}` and `\DeclareAcronym` when LaTeX is requested.
- Tone is formal, concise, and non-defensive.
- The final text contains no hidden tool artifacts or placeholder citation markers.
