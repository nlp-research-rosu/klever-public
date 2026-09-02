#!/usr/bin/env python3
"""Render all inspectable generation-trace actions without encrypted reasoning."""

from __future__ import annotations

import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T00-07-13-019f8d5e-e0d7-7d03-ac6b-e662948ad3e7.jsonl"
)


def main() -> None:
    counts: dict[str, int] = {}
    with TRACE.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            record_type = record.get("type", "<missing>")
            payload = record.get("payload", {})
            payload_type = payload.get("type", "<missing>")
            key = f"{record_type}/{payload_type}"
            counts[key] = counts.get(key, 0) + 1

            if record_type == "response_item" and payload_type == "function_call":
                print(f"LINE {line_number} FUNCTION {payload.get('name')}")
                print(payload.get("arguments", ""))
            elif (record_type == "response_item"
                  and payload_type == "function_call_output"):
                print(f"LINE {line_number} FUNCTION_OUTPUT")
                print(payload.get("output", ""))
            elif (record_type == "response_item"
                  and payload_type == "custom_tool_call"):
                print(f"LINE {line_number} CUSTOM_TOOL {payload.get('name')}")
                print(payload.get("input", ""))
            elif (record_type == "response_item"
                  and payload_type == "custom_tool_call_output"):
                print(f"LINE {line_number} CUSTOM_TOOL_OUTPUT")
                print(payload.get("output", ""))
            elif record_type == "event_msg" and payload_type == "agent_message":
                print(f"LINE {line_number} AGENT_MESSAGE")
                print(payload.get("message", ""))
            elif record_type == "event_msg" and payload_type == "task_complete":
                print(f"LINE {line_number} TASK_COMPLETE")
                print(payload.get("last_agent_message", ""))

    print("EVENT_COUNTS")
    for key, count in sorted(counts.items()):
        print(f"{key} {count}")


if __name__ == "__main__":
    main()
