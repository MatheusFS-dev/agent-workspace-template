# Code ingestion

Code context explains and routes to canonical source rather than duplicating it.

## Source identity

For code in the active project, reference project-relative files and symbols. For external repositories, record the canonical repository URL and exact commit SHA. Copy external source only when a self-contained snapshot is explicitly required or future access cannot be assumed.

## Capture

Record only retrieval-relevant structure: languages/build system, entry points, public APIs, major responsibilities, important configuration, significant data/control flow, and relevant validation commands. Exclude dependencies, environments, caches, generated outputs, binaries, datasets, checkpoints, credentials, and vendor trees unless specifically relevant.

For small codebases, keep everything in the root files. For larger ones, add a few responsibility-oriented files:

```text
<context-id>/
├── 00_overview.md
├── 00_map.md
└── modules/
    ├── training.md
    └── models.md
```

Organize by responsibility or execution path, not by mirroring every directory. Map to canonical symbols where possible, for example:

```text
- Training loop -> modules/training.md | src/train.py: train_model | optimizer, checkpoints
```

Prefer symbols over line numbers because lines drift. Create a separate index only if `00_map.md` becomes insufficient. Never store full function bodies merely for indexing.

For notebooks, describe meaningful sections/cells and important outputs. Do not retain large binary outputs unless they are necessary context.
