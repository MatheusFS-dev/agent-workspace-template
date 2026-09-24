# Scribe Style Guide

This file preserves detailed operational guidance for academic writing. Load it only when examples or detailed format behavior are needed. Use `writing-guide-pages-27-52.md` when paper-structure guidance is relevant.

### Allowed Output Formats

For manuscript LaTeX prose, return the main `.tex` content, `.bib` entries actually used, and acronym definitions using `\DeclareAcronym` when relevant. For a cover or response letter, return one complete `.tex` file based on the corresponding Scribe asset; add bibliography material only when the letter cites actual sources.

Plain text format returns only the final text without LaTeX commands or separate files.

### Citations

Use indirect citations by default. State the supported point, then cite its source. Use direct attribution when the author's identity matters to the argument or the user or venue requests it.

Direct citations attribute a statement explicitly to the cited work. Indirect citations place the citation at the end of the supported sentence.

LaTeX spacing rule: always use a non-breaking space before attached citations and cross-references: `word~\cite{Key}`, `Fig.~\ref{fig:name}`, `Table~\ref{tab:name}`, `Section~\ref{sec:name}`, and `Eq.~\eqref{eq:name}`.

### Acronyms

Every acronym appearing in LaTeX manuscript text must be defined in the acronym file using `\DeclareAcronym{...}` and referenced in the text using `\ac{...}`. In standalone letters, spell out unfamiliar terms on first use and do not require an external acronym file.

### Writing Style

Prefer third person unless the user or venue requires otherwise. Sentences should be concise and logically connected. In double-column layout, split long explanations across shorter sentences. Do not use semicolons or em dashes in manuscript prose, captions, or table-cell text. Use full stops, commas, or conjunctions instead.

### LaTeX Conventions

Ensure LaTeX code is syntactically correct and that special characters are properly escaped. Use standard notation for equations, variables, operators, and units.
Write decimals below one with a leading zero unless the venue requires another style.

### Visible Manuscript Revisions

When editing an existing LaTeX manuscript, mark the visible changed or added content in blue until the user asks to remove the coloring. Reuse an existing suitable revision command when the document defines one. Otherwise load `xcolor` once and define `\newcommand{\changed}[1]{{\color{blue}#1}}`, then wrap only the changed span, for example `\changed{revised text}`. Preserve citations, equations, labels, and other LaTeX syntax. For a deletion, color any replacement; do not reinsert deleted prose merely to mark it. For a changed figure, color only its caption blue, not the artwork. Do not add LaTeX color codes to plain-text drafts.

When asked to remove revision coloring, keep the revised content and remove the revision markup from the `.tex` source. Unwrap `\changed{...}` or the document's equivalent carefully, preserving nested commands and braces. Remove the command definition and `xcolor` import only if nothing else needs them. Compile and inspect the affected content after either operation when the complete manuscript and tools are available.

### Tables and Page Layout

Use a horizontal divider between body rows when the user requests per-row separation, the document has established that convention, or dense rows are otherwise difficult to track. Apply the choice consistently to comparable tables. Keep adjacent headers and data columns visually distinct by adjusting column widths, alignment, `\tabcolsep`, or explicit padding as the table environment permits. Do not reduce type to an unreadable size to force a fit.

Keep prose, mathematics, and tables within the text block. Break long setup sentences, move long parameter sets or equations to display math, and use wrapping columns where appropriate. Compile after layout edits, inspect the affected pages and structurally similar tables, and resolve overfull boxes, crowded headers, and collisions in the source.

### Paragraphs After Displayed Equations

A source-code line break after `equation`, `align`, or `\[...\]` does not begin a new LaTeX paragraph. First determine whether prose following the display is semantically a new paragraph. If it is, explicitly end the preceding paragraph and begin the new one with an indent:

```latex
\begin{equation}
E = mc^2.
\end{equation}
\par\indent In Equation~\ref{eq:example}, ...
```

Do not add `\par\indent` when the prose continues the same sentence or paragraph that introduced the equation; `\indent` alone is insufficient while LaTeX still considers the text part of that paragraph. After editing, compile the document and visually inspect the affected pages to confirm the intended indentation rendered correctly.

### Focusing Citations on Relevant Aspects

When summarizing references, emphasize the aspects that align with the user’s research focus. The same reference may be described differently depending on whether the user is focusing on methodology, modeling, implementation, evaluation, or limitations.

### Revisions after response

Always remove artifacts such as `:contentReference[oaicite:0]{index=0}`. Use only `\cite`. Do not overuse citations. Each reference should normally be cited once per local discussion unless a later section is sufficiently far away to require repetition.
