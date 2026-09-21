# Book ingestion

Use for books and textbooks, especially technical books with equations, figures, exercises, tables, or printed code.

## Inspect

Read the table of contents and relevant chapter openings first. Preserve exact chapter/section numbering and titles. For PDFs, establish reliable PDF-page and printed-page mapping when printed numbering exists. Prefer embedded text. OCR only unusable pages. Visually verify equations, code, tables, and figure boundaries when extraction is uncertain.

## Output

For a nontrivial book, use:

```text
<context-id>/
├── 00_overview.md
├── 00_map.md
├── chapters/
│   └── chNN_slug/
│       ├── 00_chapter_summary.md
│       ├── NN_SS_section.md
│       ├── code/                 # only if listings exist
│       └── problems/             # only if exercises are retained
├── source/
│   ├── chapters/chNN_slug.pdf
│   └── sections/chNN/NN_SS_slug.pdf
└── figures/
    ├── 00_index.md
    └── chNN/fig_<source-number-or-id>.<ext>
```

Do not create empty directories.

### Retained source PDFs

For PDF books, chapter PDFs are required for every ingested chapter. Also create a section PDF when that section has its own Markdown context file. Section PDFs use inclusive page ranges and may overlap adjacent sections when boundaries share a page. Preserve full pages rather than cropping away neighboring source text.

Use source-native chapter and section boundaries. Never split derivations, algorithms, examples, or listings merely to reduce size.

`00_map.md` routes book-level topics to chapter summaries and, where useful, directly to sections. Chapter summaries route only within their chapter and should point to the matching retained PDF slices.

## Section content

Keep section files compact and source-grounded. Include only useful elements such as purpose, formulation, key equations/procedure, source-supported interpretation, dependencies, verification notes, and source locations. Do not force empty headings.

### Equations

Transcribe equations that matter for reasoning. Preserve signs, indices, limits, units, staggering/half-steps, and equation numbers. Verify uncertain transcription visually. Never silently repair a suspected source error. Record the uncertainty and source page.

### Printed code

Store useful printed listings separately under the chapter `code/` directory using the original language extension when practical. Preserve whether a listing is complete, incremental, or modifies an earlier program. Do not invent omitted declarations, imports, or unchanged blocks. Add companion Markdown only when it materially improves retrieval.

### Problems

Create problem files only for relevant exercises. Preserve numbering, variables, conditions, and requested tasks. Do not add solutions unless explicitly requested.

## Figures

Extract every meaningful numbered figure in the ingested scope, plus unnumbered diagrams that carry technical information needed for later reasoning.

Prefer a crop rendered from the source page because technical figures often combine raster/vector graphics, labels, arrows, and legends. Use an embedded image directly only after confirming it represents the complete figure. Do not save decorative artwork, publisher logos, repeated icons, or incidental images.

`figures/00_index.md` records, for each retained figure:

```text
Figure <number/title> -> figures/chNN/<file> | chapter/section | PDF p. <n> | printed p. <n if known> | caption/purpose
```

A full-page render is acceptable only when a clean figure crop cannot be isolated reliably. Keep the figure asset in that case and say so in the index.

## Completion

An ingested chapter is complete when all represented sections match the requested source scope, chapter/section PDFs exist, meaningful figures are indexed and extracted, important equations and code uncertainty are verified, relevant programs/problems are routed, and page mappings are recorded when available.

Retrieval order:

```text
00_overview -> 00_map -> chapter summary -> section/code/problem/figure -> matching source PDF
```
