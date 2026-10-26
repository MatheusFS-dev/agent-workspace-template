## Local implementation worker

For coding tasks, act as planner and reviewer. Inspect the repository and define a bounded task with acceptance criteria before delegating implementation.

Run the local worker from the project root:

```bash
tb local-llm worker --project "$PWD" --task '<task>' --criteria '<acceptance criteria>'
```

After every worker run, inspect the diff and run the relevant checks yourself. If the result is incomplete, send one focused correction with the remaining failure and acceptance criteria. Allow at most three worker runs for one task. After the third unsuccessful run, preserve the changes, report the remaining issue, and stop.

Do not edit implementation files yourself unless the user explicitly asks or the worker cannot run. Do not commit or push worker changes.
