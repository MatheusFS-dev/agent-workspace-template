# Easy Task Mode

Use this mode only for clearly trivial tasks.

## Allowed tasks

- Answer a simple question without repository-wide context.
- Fix a typo.
- Change one literal line.
- Patch a small Markdown rendering issue.
- Replace a short phrase.
- Edit only text or code directly provided by the user.
- Touch one explicitly named file when the requested change is local and obvious.

## Hard limits

Do not use this mode when the task involves:
- debugging,
- tests,
- refactoring,
- architecture,
- dependencies,
- environment setup,
- ML experiments,
- data pipelines,
- performance,
- writing papers or paragraphs,
- reviewers,
- plots,
- multi-file behavior,
- unclear target files,
- uncertain intent.

## Context rule

Read only the user-provided text or the explicitly named file.

Do not inspect broad repository trees.
Do not read project maps, memories, skills, references, prompts, assets, PDFs, or unrelated files.

## Escalation rule

If the task is not certainly easy, ask before loading more context:

```text
This may require normal routing. Should I continue in easy mode, or load the normal context?
```

If the task becomes non-trivial after starting, stop and ask before escalating.

## Verification

Use the smallest useful check.

For Markdown or prose edits, visual inspection is enough unless the user asks for validation.

For code edits, run only a narrow syntax or targeted check when it is cheap and directly relevant. Do not run broad project checks unless the task escalates to normal coding mode.
