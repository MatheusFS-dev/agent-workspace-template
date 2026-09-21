# Document ingestion

Use for papers, reports, specifications, manuals, general PDFs, Markdown, HTML, and similar documents that are not books.

## Extract

Preserve the source hierarchy. For PDFs, use embedded text first. OCR only pages whose text is absent or unusable, and render pages only when layout, equations, figures, tables, or OCR verification requires it. Extraction artifacts are temporary by default. Do not persist a full text dump unless later retrieval genuinely needs it.

## Structure

Create `sections/` only when the document is large enough that the two root files are insufficient:

```text
<context-id>/
├── 00_overview.md
├── 00_map.md
└── sections/
    ├── methods.md
    ├── results.md
    └── ...
```

Use real headings or coherent topic boundaries. Short documents may need only the two root files.

## Papers

In the overview, capture the research question, contribution, method, main reported findings, source-stated limitations, and important terminology. Preserve parameters, datasets, metrics, baselines, equations, and experimental conditions when they affect interpretation.

Use the paper's actual structure. Do not force IMRaD. Do not strengthen claims beyond the evidence. Create claim, equation, figure, or table indexes only when downstream work clearly requires them.

## Reports, specifications, and manuals

Prefer headings, requirements, procedures, interfaces, tables, and numbered clauses as retrieval boundaries. Preserve normative words such as MUST, SHALL, SHOULD, limits, configuration keys, and ordering constraints. Keep figure and table numbers when they carry retrievable information.

## Generic text and web-style documents

Remove navigation chrome and repeated boilerplate. Preserve meaningful links, code blocks, warnings, equations, tables, and source paths. Prefer source-native headings.
