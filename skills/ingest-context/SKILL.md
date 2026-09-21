---
name: ingest-context
description: Use only when the user explicitly asks to ingest, index, import, or prepare material as reusable project context for agents.
---

# Ingest Context

Convert requested material into compact, source-grounded context for later agent retrieval. This is an explicit gate. Reading, summarizing, or analyzing a source does not trigger ingestion.

## Destination

Resolve the project root with `git rev-parse --show-toplevel` when possible. Store each ingested source at:

```text
<project_root>/.agents/context/<context-id>/
```

Use a short stable slug for `<context-id>`. Do not create a central catalog, version-like duplicate directories, or ingest `.agents/context/` into itself.

## Package contract

Start every package with only:

```text
<context-id>/
├── 00_overview.md
└── 00_map.md
```

Add detailed files only when they materially improve retrieval.

`00_overview.md` is the cheap entry point. Keep it concise and record source identity, exact provenance, fingerprint, type, scope, what the package can answer, key terminology or limitations, and a pointer to `00_map.md`.

Use compact frontmatter only here:

```yaml
---
id: example-id
type: paper
source: path-or-url
fingerprint: sha256-or-git-commit
---
```

`00_map.md` is navigation only. Each entry should route a topic to the smallest useful file and, when useful, its source location:

```text
- Z-transform formulation -> sections/02_04_z_transform.md | pp. 41-44 | recurrence, dispersive media
```

Do not repeat summaries in the map.

## Route by semantic type

Load only one source-type reference unless the source genuinely mixes types:

- **Book or textbook:** `references/books.md`
- **Paper, report, specification, manual, PDF, Markdown, HTML, or similar document:** `references/documents.md`
- **Repository, source tree, notebook, script, or source file:** `references/code.md`
- **Other content:** preserve its natural hierarchy and apply this file's common rules.

A paper in PDF form is a paper. A book in PDF form is a book. Prefer semantic type over extension.

## Common workflow

1. Resolve the source and project root.
2. Classify the source and choose one primary handler.
3. Choose a stable context ID and fingerprint the source. Use SHA-256 for local files and exact commit SHA for Git repositories.
4. If an existing `00_overview.md` records the same fingerprint, stop unless regeneration was requested.
5. Inspect source structure before writing.
6. Create `00_overview.md`, `00_map.md`, then only the semantic units needed for effective retrieval.
7. Verify map targets and source support for generated claims.
8. Remove temporary extraction, OCR, rendering, and analysis artifacts unless later verification truly depends on them.

## Common rules

- Split by meaning, not fixed token or page counts.
- Keep tightly coupled derivations, procedures, algorithms, and code paths together.
- Preserve source-native headings and terminology when useful for lookup.
- Keep summaries source-grounded. Clearly label interpretation that goes beyond direct source statements.
- Preserve exact equations, parameters, constraints, normative language, API contracts, and experimental conditions when correctness depends on them.
- Give compact source locations in detailed files, for example `Source: pp. 7-9` or `Source: src/train.py, train_model`.
- Do not copy current-project source code into context. Route to canonical files and symbols.
- Do not retain complete raw extraction merely because ingestion produced it.
- Do not create indexes whose routing information already fits in `00_map.md`.

## Retrieval rule

Downstream agents should use:

```text
00_overview.md -> 00_map.md -> smallest relevant unit -> original source only if needed
```

Never recursively load an entire context package when one unit is sufficient.

## Completion

Before reporting success, confirm that the package is under `.agents/context/<context-id>/`, both root files exist, provenance and fingerprint are recorded, map targets resolve, generated material is source-supported, important uncertainty is disclosed, and temporary artifacts were removed.
