---
name: ingest-context
description: Use when the user explicitly asks to ingest, index, import, or prepare books, papers, PDFs, documents, code, or other material as reusable project context for agents.
---

# Ingest Context

Create source-grounded, progressively retrievable context under `<project_root>/.agents/context/<context-id>/`. Ingestion is explicit. Ordinary reading, summarizing, or analysis does not trigger it.

## Core contract

Resolve the project root, preferably with `git rev-parse --show-toplevel`. Use a stable human-readable context ID. Every package starts with:

```text
<context-id>/
├── 00_overview.md
└── 00_map.md
```

`00_overview.md` is the cheap entry point. Record source identity, type, exact provenance, SHA-256 or Git commit, scope, key terminology, limitations, and what the package can answer.

`00_map.md` is routing only. Point topics to the smallest useful context file and its retained source slice when one exists. Do not duplicate summaries there.

## Route

Load only the matching reference:

- book/textbook -> `references/books.md`
- paper/report/specification/manual/PDF/Markdown/HTML -> `references/documents.md`
- repository/notebook/script/source tree -> `references/code.md`
- other material -> preserve its natural hierarchy using this contract

Semantic type beats file extension.

## Common rules

1. Inspect structure before writing.
2. Split by semantic boundaries, never arbitrary token counts.
3. Preserve exact equations, parameters, constraints, normative wording, code semantics, and source terminology when material.
4. Keep generated explanation distinguishable from source-derived content.
5. For PDFs, retain smaller source PDFs as defined by the active handler. OCR and page renders are temporary unless a retained visual is itself useful context.
6. Extract meaningful figures from PDFs into final figure assets with page/section provenance. Prefer a page crop that captures the complete composed figure. Embedded-image extraction is only a candidate source because vector labels or multi-part figures may be lost.
7. Do not duplicate current-project code. Route to canonical files and symbols.
8. Do not create central catalogs, manifests, JSONL indexes, full OCR dumps, or duplicate version directories unless explicitly needed.
9. Remove temporary extraction files after verification.

For PDF slicing/cropping, use `scripts/pdf_tools.py` when convenient. It is a utility, not a required storage format.

## Retrieval

Downstream agents use:

```text
00_overview.md -> 00_map.md -> smallest relevant unit -> retained source slice/original source only when needed
```

Never recursively load the package.

## Completion

Verify both root files exist, every map target resolves, retained PDF slices open, figure assets are complete and correctly attributed, source-sensitive content was checked against the source, and temporary artifacts are gone.
