# Executing Writing Plans

> **Supporting module:** Part of the single `scribe-superpowers` skill. Load it for an approved manuscript writing plan.

## Start

Read the approved design and plan. Confirm the thesis, evidence boundary, global constraints, section responsibilities, and output format. Report a critical gap before drafting when sources are missing, claims are unsupported, requirements conflict, or verification is impossible.

## Internal Ledgers

Maintain compact internal ledgers for:

- claims, allowed wording, evidence, qualifiers, and destinations,
- preferred terminology, prohibited variants, acronyms, symbols, capitalization, and spelling,
- cross-section dependencies, forward references, unresolved evidence gaps, and changes requiring updates elsewhere.

Do not expose the ledgers unless requested.

## Task Execution

For each task:

1. read only its relevant inputs,
2. load the drafting, review, reviewer-response, and section files required by that task,
3. produce the defined deliverable without changing the approved thesis or scope,
4. check its claims against the ledger,
5. use `quality-control.md` once,
6. update the ledgers and mark the task complete.

## Cross-Section Checkpoints

Verify that topic sentences form a coherent argument, contributions and limitations are described consistently, numbers match their source, terminology and notation remain stable, references and labels are valid, and later sections do not exceed earlier evidence.

Correct objective inconsistencies directly. Do not run a new general polishing pass on already revised sections. A material architectural change requires returning to the design gate.

## Completion

After all tasks, check every plan task and global constraint, run final cross-section verification through `quality-control.md` Phase B, and report unresolved evidence limitations. Do not claim completion from section-level success alone.
