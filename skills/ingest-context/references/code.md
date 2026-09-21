# Code ingestion

Code context should explain and route to canonical source, not duplicate it.

## Source identity

For code already in the active project, reference project-relative files and symbols. Do not copy source into `.agents/context/`.

For external repositories, record the canonical repository URL and exact commit SHA. Copy external source only when the user explicitly needs a self-contained snapshot or reliable future access cannot be assumed.

## Inspect

Capture only retrieval-relevant structure:

- languages and build/package system,
- entry points and public APIs,
- major modules and responsibilities,
- important configuration,
- significant data/control flow,
- tests and validation commands when relevant.

Exclude dependencies, environments, caches, generated outputs, binaries, datasets, checkpoints, credentials, and vendor trees unless explicitly relevant.

## Structure

For small codebases, keep everything in the two root files. For larger ones, add a few responsibility-oriented files:

```text
<context-id>/
├── 00_overview.md
├── 00_map.md
└── modules/
    ├── training.md
    ├── models.md
    └── ...
```

Organize by responsibility or execution path rather than mirroring every directory.

Map directly to canonical source where possible:

```text
- Training loop -> modules/training.md | src/train.py: train_model | optimizer, checkpointing
```

Prefer symbols over line numbers because line numbers drift. Create symbol or dependency indexes only when the map becomes insufficient. Never store full function bodies in an index.

For notebooks, describe meaningful sections or cells and important outputs. Do not persist large binary outputs or rendered notebooks unless necessary for understanding.
