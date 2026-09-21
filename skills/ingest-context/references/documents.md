# Document ingestion

Use for papers, reports, specifications, manuals, and other documents, including general PDFs, Markdown, and HTML.

## Inspect and classify

Preserve the source's actual hierarchy. For PDFs, prefer embedded text and use OCR only where extraction is unusable. Render pages for visual verification of equations, tables, figures, layout, or OCR uncertainty.

For papers, preserve the paper's real section structure rather than forcing IMRaD. Capture the research question, contribution, method, reported findings, source-stated limitations, datasets, metrics, baselines, parameters, and experimental conditions when material.

For specifications/manuals, preserve numbered clauses, requirements, interfaces, procedures, limits, configuration keys, and normative terms such as MUST, SHALL, and SHOULD.

## Output

For a nontrivial PDF:

```text
<context-id>/
├── 00_overview.md
├── 00_map.md
├── sections/
│   ├── 01_<section>.md
│   └── ...
├── source/
│   └── sections/
│       ├── 01_<section>.pdf
│       └── ...
└── figures/
    ├── 00_index.md
    └── fig_<source-number-or-id>.<ext>
```

Short non-PDF documents may need only the root files. Do not create empty directories.

### Retained source PDFs

For nontrivial PDFs, retain one smaller PDF per top-level semantic section represented in context. Create subsection PDFs only when subsections have separate context files or are independently useful retrieval units.

Page ranges are inclusive and may overlap when two sections share a boundary page. Preserve full source pages. Do not crop text just to make section PDFs mutually exclusive.

Each `00_map.md` entry should route to both the Markdown unit and matching source PDF when present, for example:

```text
- Channel model -> sections/03_channel_model.md | source/sections/03_channel_model.pdf | PDF pp. 4-7
```

## Figures

Extract meaningful figures that communicate results, architecture, procedures, experimental setups, diagrams, or other information likely to be queried later.

Prefer a source-page crop containing the entire composed figure, including labels and legend. Embedded-image extraction may be used to discover candidate images but must be checked because PDF figures may be vector, multi-part, or have text stored separately. Exclude decorative and irrelevant images.

`figures/00_index.md` records:

```text
Figure <number/title> -> figures/<file> | section | PDF p. <n> | caption/purpose
```

Keep source caption wording when useful for lookup. If a clean crop is impossible, retain a full-page render and mark it as such.

## Source fidelity

Do not strengthen paper claims beyond the evidence. Preserve exact equations, requirements, limits, and conditions when they change interpretation. Tables should normally be represented compactly in the relevant section Markdown. Retain a table image only when layout itself is needed.

For Markdown/HTML and other non-PDF sources, preserve meaningful links, code blocks, warnings, equations, and tables while removing navigation chrome and repeated boilerplate. No PDF slicing is required when the source is not PDF.
