#!/usr/bin/env python3
"""Allow native Maestro sessions to use only their local worker MCP tools."""

import json
import sys


ALLOWED_TOOLS = {
    "mcp__maestro_worker__read_file",
    "mcp__maestro_worker__list_files",
    "mcp__maestro_worker__search",
    "mcp__maestro_worker__start_implementation",
    "mcp__maestro_worker__job_status",
    "mcp__maestro_worker__wait_for_job",
    "mcp__maestro_worker__job_logs",
    "mcp__maestro_worker__review_job",
}


def main() -> int:
    """Deny direct local tools while permitting the supervised MCP contract.

    Returns:
        int: Zero after emitting the hook decision.
    """
    event = json.load(sys.stdin)
    tool_name = event.get("tool_name", "")
    if tool_name in ALLOWED_TOOLS:
        return 0
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        "Maestro may use only the maestro_worker MCP tools."
                    ),
                }
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
