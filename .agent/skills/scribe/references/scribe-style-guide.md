# Scribe Style Guide

This file preserves detailed operational guidance for academic writing. Load it only when examples or detailed format behavior are needed. Use `writing-guide-pages-27-52.md` when paper-structure guidance is relevant.

### Allowed Output Formats

LaTeX format returns three separate fenced outputs: main `.tex` content, `.bib` entries actually used, and acronym definitions using `\DeclareAcronym`.

Plain text format returns only the final text without LaTeX commands or separate files.

### Citations

The user may specify direct or indirect citation style.

Direct citations attribute a statement explicitly to the cited work. Indirect citations place the citation at the end of the supported sentence.

LaTeX spacing rule: always use a non-breaking space before attached citations and cross-references: `word~\cite{Key}`, `Fig.~\ref{fig:name}`, `Table~\ref{tab:name}`, `Section~\ref{sec:name}`, and `Eq.~\eqref{eq:name}`.

### Acronyms

Every acronym appearing in LaTeX text must be defined in the acronym file using `\DeclareAcronym{...}` and referenced in the text using `\ac{...}`.

### Writing Style

Prefer third person unless the user or venue requires otherwise. Sentences should be concise and logically connected. In double-column layout, split long explanations across shorter sentences. Prefer commas and full stops over semicolons or long dashes.

### LaTeX Conventions

Ensure LaTeX code is syntactically correct and that special characters are properly escaped. Use standard notation for equations, variables, operators, and units.

### Focusing Citations on Relevant Aspects

When summarizing references, emphasize the aspects that align with the user’s research focus. The same reference may be described differently depending on whether the user is focusing on methodology, modeling, implementation, evaluation, or limitations.

### Revisions after response

Always remove artifacts such as `:contentReference[oaicite:0]{index=0}`. Use only `\cite`. Do not overuse citations. Each reference should normally be cited once per local discussion unless a later section is sufficiently far away to require repetition.
