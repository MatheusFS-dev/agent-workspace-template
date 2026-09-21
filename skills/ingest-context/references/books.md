# Book ingestion

Use for books and textbooks, especially technical books containing equations, figures, exercises, or code listings. Build hierarchical context that lets an agent enter at book level, route to a chapter, then load only the necessary section or artifact.

## Inspect first

Determine the requested scope before transformation. For a full book, inspect the table of contents and chapter openings. For selected chapters, inspect only enough surrounding structure to preserve numbering and dependencies.

Record exact chapter and section names and, for PDFs, any reliable PDF-page to printed-page mapping. Do not infer missing headings or numbering.

For PDFs, prefer embedded text. OCR only pages where text is absent or unusable. Render pages only when layout, equations, figures, tables, code, or OCR uncertainty requires visual verification. Extraction artifacts are temporary by default.

## Structure

For multi-chapter material, use:

```text
<context-id>/
├── 00_overview.md
├── 00_map.md
└── chapters/
    └── chNN_slug/
        ├── 00_chapter_summary.md
        ├── NN_SS_section.md
        ├── problems/        # only when problem sets exist
        ├── code/            # only when printed programs/listings exist
        └── figures/         # only when figure-specific context is useful
```

Do not create empty directories. For a short book or a single small chapter, collapse structure when separate files would not improve retrieval.

`00_map.md` should route chapters and major topics. Each `00_chapter_summary.md` should route that chapter's sections, important equations or algorithms, programs, problem sets, and prerequisites without reproducing section content.

## Sections

Split by semantic boundaries, not page count or fixed token size. Keep complete derivations, algorithms, procedures, and tightly coupled examples together. A section file should contain only the parts that are useful for later reasoning, normally:

1. scope or purpose,
2. source-derived formulation,
3. key equations or procedure,
4. computational or conceptual interpretation when supported,
5. dependencies or connections,
6. verification notes when needed,
7. source locations.

Omit headings that would be empty. Do not mechanically force this shape onto every section.

## Equations

Transcribe equations that materially affect understanding or later calculations. Preserve symbols, signs, indices, limits, units, staggering or half-step locations, and equation numbers when present. Verify uncertain equations against the rendered page rather than trusting OCR.

Do not silently repair suspected source errors. Record a concise verification note with the exact source location.

## Printed code

When the book contains code listings, preserve each useful listing separately under `code/` using the original language extension when practical. Add a short companion Markdown file only when the listing needs explanation or retrieval metadata.

Preserve whether a listing is complete, incremental, or modifies an earlier program. Never invent declarations, imports, unchanged blocks, or omitted code.

## Problems and exercises

Create problem files only when exercises are useful to the ingested scope. Preserve task wording closely enough to retain requirements, variables, and numbering. Do not add solutions unless the user explicitly requested solutions as part of ingestion.

## Figures and tables

Create figure-specific context only when a figure or table carries information not adequately represented in the section text. Preserve number, caption or purpose, source page, and the facts needed to interpret it. Do not keep rendered images by default. Retain a crop or page image only when future exact visual verification is necessary.

## Source fidelity

Keep source-derived explanation distinct from your implementation interpretation or later clarification. Preserve book terminology even when modern terminology differs. Mention important OCR, typographical, equation, or code-listing uncertainty rather than normalizing it silently.

## Completion

A requested chapter is complete when its represented sections match the source scope, important equations are verified, relevant printed programs and problem sets are routed, page mappings are recorded when available, map targets resolve, and uncertainty that could change meaning is disclosed.

Downstream retrieval should be:

```text
00_overview.md -> 00_map.md -> chapter summary -> relevant section/code/problem/figure -> original page only if needed
```
