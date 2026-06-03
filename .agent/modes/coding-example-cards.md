# Coding Example Cards

Compact behavior-shaping cards for coding tasks. Search this file before reading full examples.

## Hidden Assumptions

Trigger:

- The user asks to add, export, save, load, generate, support, or integrate something without specifying scope, fields, destination, data ownership, security, or output format.

Failure mode:

- The agent silently chooses defaults and implements behavior the user did not request.

Required behavior:

- State only assumptions that affect correctness.
- Ask targeted questions when implementation would otherwise depend on unknown scope.
- Present plausible interpretations instead of choosing silently.
- Prefer the smallest reversible implementation.

Bad signs:

- Exports all records by default.
- Invents fields, paths, formats, permissions, filters, pagination, background jobs, notifications, or caching.
- Treats missing requirements as permission to design a broad feature.

Good response pattern:

```text
This can mean A, B, or C. The smallest safe version is X. Which target behavior should I implement?
```

## Multiple Interpretations

Trigger:

- The user asks to make something faster, better, cleaner, robust, scalable, secure, or optimized without defining the target metric or failure condition.

Failure mode:

- The agent picks one interpretation silently and implements unrelated changes.

Required behavior:

- Name the plausible interpretations.
- Tie each interpretation to a concrete mechanism and verification check.
- Ask for the dimension that matters when the choice changes implementation.

Bad signs:

- Adds caching, async, indexes, batching, or monitoring without evidence.
- Optimizes throughput when the issue is latency, or optimizes latency when the issue is memory.
- Provides a vague plan such as "review, improve, test".

Good response pattern:

```text
"Faster" can mean lower latency, higher throughput, lower memory, or faster perceived UI. These require different changes. Which target should I optimize?
```

## Over-abstraction

Trigger:

- The task is small, simple, local, or explicitly described as basic.

Failure mode:

- The agent adds frameworks, strategies, registries, protocols, configuration layers, decorators, inheritance, caches, validators, or extension points before they are needed.

Required behavior:

- Implement the smallest direct solution that solves the current requirement.
- Add abstraction only when the current requirement has multiple real variants.
- Defer future flexibility until it becomes necessary.

Bad signs:

- A simple function becomes a class hierarchy.
- A one-case rule becomes a strategy pattern.
- Optional parameters or extension hooks appear without a current user need.

Good response pattern:

```text
The direct function is enough for the current requirement. I would not add a strategy layer unless there are multiple discount types or runtime selection rules.
```

## Drive-by Refactoring

Trigger:

- The user asks to fix a specific bug, crash, validation issue, or edge case.

Failure mode:

- The agent changes unrelated logic, reformats surrounding code, rewrites comments, adds type hints, changes validation semantics, or improves adjacent behavior.

Required behavior:

- Reproduce or isolate the specific failure when possible.
- Change only the lines required to fix the confirmed bug.
- Remove only unused code introduced by the fix.
- Preserve unrelated behavior, formatting, comments, and style.

Bad signs:

- The diff touches unrelated functions.
- Validation becomes stricter than requested.
- Comments, quote style, or formatting are changed for no reason.
- New behavior is described as an improvement but was not requested.

Good response pattern:

```text
I will only fix the empty-input crash path and leave the existing validation semantics unchanged.
```

## Style Drift

Trigger:

- The user asks for a small local addition such as logging, a guard, a message, a field, or a narrow patch.

Failure mode:

- The agent changes quote style, typing style, function layout, naming patterns, error style, comments, or control flow unrelated to the requested change.

Required behavior:

- Match nearby style even if it is not your preferred style.
- Preserve existing public behavior.
- Add only the minimal import, constant, check, or line needed.

Bad signs:

- Unrequested type hints appear.
- Single quotes become double quotes, or vice versa, across unrelated lines.
- Boolean logic is rewritten while adding logging.
- Existing print/error behavior is converted to logging without request.

Good response pattern:

```text
I will follow the local style and add only the requested log lines.
```

## Vague vs. Verifiable

Trigger:

- The user asks to fix a broad subsystem or vague behavior, such as authentication, search, training, deployment, data loading, or evaluation.

Failure mode:

- The agent proceeds with a vague plan and changes code before defining success criteria.

Required behavior:

- Convert the vague request into a specific failure case or measurable target.
- Define verification before implementation.
- Ask for the missing failure detail if the implementation cannot be chosen safely.

Bad signs:

- "I will review the code, identify issues, make improvements, and test." 
- Large edits without a named failure case.
- No pass/fail criterion.

Good response pattern:

```text
To fix this safely, I need the concrete failure. For example, if the issue is stale sessions after password changes, the verification is: change password, old session is rejected.
```

## Multi-Step Verification

Trigger:

- The task adds a feature that naturally spans multiple files, behaviors, or phases.

Failure mode:

- The agent implements everything at once and verifies only at the end, making regressions hard to localize.

Required behavior:

- Split the work into independently verifiable steps.
- Use `1. [Step] -> verify: [check]`.
- Prefer the simplest deployable step first.

Bad signs:

- A single large diff combines parsing, storage, UI, caching, tests, and docs.
- Verification is only "run the full suite".
- Failure localization is unclear.

Good response pattern:

```text
1. Add parser -> verify: parser unit test passes.
2. Wire parser into loader -> verify: loader smoke test passes.
3. Add validation -> verify: invalid-input tests pass.
```

## Test-First Verification

Trigger:

- The user reports a failure, crash, regression, duplicate handling issue, nondeterminism, data corruption, or edge case.

Failure mode:

- The agent changes code without first demonstrating the bug or defining a concrete failing condition.

Required behavior:

- Reproduce the issue with a minimal test, script, or concrete input when possible.
- Make the test fail before the fix when the environment allows it.
- Apply the smallest fix.
- Re-run the targeted check and report the result.

Bad signs:

- The fix is based only on speculation.
- A broad implementation change is made without a failing case.
- The verification does not exercise the reported edge case.

Good response pattern:

```text
I will first create a minimal failing case for duplicate scores, then change only the tie-breaking logic and re-run that case.
```
