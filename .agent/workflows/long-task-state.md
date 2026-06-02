# Long-Task State Workflow

Use this workflow only when the user explicitly asks the agent to keep task state, create a session state file, resume from a state file, or maintain progress across a long task.

## Rule

Do not create or read a default `.agent/context/session-state.md` file. Session state is task-local, not global template context.

## Where to create state

Create the state file at the narrowest relevant location for the work:

- Repository-wide task: `.agent/task-state/session-state.md`
- Subproject task: `<subproject>/.agent-state/session-state.md`
- Documentation task: `<docs-folder>/.agent-state/session-state.md`
- Experiment task: `<experiment-folder>/.agent-state/session-state.md`

If the repository has an existing task-state convention, use it instead of creating a new location.

## File content

Keep the state file compact and operational:

```md
# Session State

## User goal

## Current status

## Decisions made

## Files inspected

## Files changed

## Verification run

## Open issues

## Next action
```

## Maintenance

- Update only after meaningful progress, not after every small action.
- Remove obsolete details as the task evolves.
- Keep enough information to resume safely, but avoid storing full logs, tool outputs, source dumps, or repeated rationale.
- Delete the state file when the user says the long task is complete and no future resume is needed.
