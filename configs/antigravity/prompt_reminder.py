#!/usr/bin/env python3
"""Antigravity PreInvocation hook that reminds the agent of the global instructions."""

import json
import sys


REMINDER = (
    "Apply global gates: code/debug=Superpowers (even small edits). "
    "plot=Superpowers+scientific-plot-maker. research=no Superpowers. paper=scribe. "
    "README=readmaker. explain/report=explainer. docs=docs/. "
    "test scripts=tests/agents/<area>/ unless user path. "
    "if asked: ingest=ingest-context, handoff=session-handoff."
)


def main():
    """Print the reminder on the first model call of each user prompt.

    Antigravity restarts `invocationNum` at 0 for every user prompt, so
    injecting only at 0 adds the reminder once per prompt and not once per
    tool-loop model call.

    Returns:
        int: Always zero so a malformed payload never interrupts a turn.
    """
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return 0
    if isinstance(event, dict) and event.get("invocationNum") == 0:
        sys.stdout.write(json.dumps({"injectSteps": [{"ephemeralMessage": REMINDER}]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
