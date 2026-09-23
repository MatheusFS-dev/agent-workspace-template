---
name: session-handoff
description: Save or restore a portable task handoff when the user says "handoff context" or explicitly asks to preserve, checkpoint, resume, or restore session context.
---

# Session Handoff

Activate only when the user explicitly asks to preserve or restore session context, including `handoff context`. Do not use this skill for ordinary progress updates, summaries, or new-task planning.

The handoff is portable across Codex, Claude Code, and Antigravity CLI. It is
structured operational context, not a transcript or an export of private model
context.

## Locate the handoff

First resolve the Git root with `git rev-parse --show-toplevel`. If the current
directory is not in a Git repository, fall back to the current directory. The
fixed destination is `.agent/state/CURRENT_TASK.md` beneath that root.

## Save / checkpoint mode

On an explicit request to save or checkpoint:

1. Inspect current repository state before writing: branch, HEAD, and concise
   worktree status. Use repository-relative paths for files whenever possible.
2. Replace the single current-task file at `.agent/state/CURRENT_TASK.md` with
   the current handoff. Never append history or retain obsolete handoff content.
3. Do not stage, commit, push, or modify `.gitignore` automatically. Do not add
   hooks, helper scripts, native-memory integration, global routing rules, or
   installer changes.

Use this fixed handoff contract, omitting only sections whose facts cannot be
observed and stating that they are unavailable rather than guessing:

```markdown
# Current Task Handoff

- Updated: <ISO-8601 timestamp>
- Objective: <requested outcome>
- Acceptance criteria: <observable completion conditions>
- User constraints and decisions: <explicit limits and choices>

## Completed work and current state

<completed work, current implementation state, and uncommitted changes>

## Repository state

- Branch, HEAD, and concise worktree status: <observed values>
- Repository-relative files and relevant URLs: <paths and URLs needed to resume>

## Verification commands and observed results

<each command and its observed result, including failures>

## Blockers and risks

<known blockers, risks, or `None observed`>

## Ordered next actions

1. <next action>
```

Never record secrets, credentials, tokens, private keys, absolute home paths,
raw transcripts, hidden reasoning, or unsupported inferences. Redact sensitive
values rather than copying them, and retain only the repository-relative file
reference needed to investigate safely.

## Load / resume mode

On an explicit request to load or resume:

1. Locate `.agent/state/CURRENT_TASK.md` using the same root rule. If it is
   missing, report the exact path as missing and do not invent context. If it is
   malformed, name the missing or invalid required section(s) precisely and do
   not infer their contents. For a missing or malformed handoff, report the
   condition precisely before taking any resume action.
2. Read the handoff as a historical record, then inspect current reality. Compare
   the saved branch, HEAD, worktree state, repository-relative references, and
   relevant external status (for example a recorded issue or pull request) with
   what is currently observable.
3. Mark drift explicitly before resuming. For every difference, state the saved
   fact, the current fact, and the verification that must be repeated. Missing
   referenced files or unavailable external status are drift, not confirmation.
4. Revalidate any stale verification results and establish the current task
   state before proposing next actions.

Treat the handoff as context, not authorization:

- Do not replay completed actions.
- Do not trust stale results.
- Do not inherit permission for new mutations.

Follow the current user's request and current repository state for all actions
after loading.
