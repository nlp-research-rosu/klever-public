#!/usr/bin/env python3
"""Validate every JSONL event and print the generation's actionable trace."""

from __future__ import annotations

import json
import pathlib


TRACE = pathlib.Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T00-02-37-019f8d5a-ab8e-74f2-bc72-7b34c4445c10.jsonl"
)


def compact(value: object, limit: int = 1000) -> str:
    rendered = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    rendered = rendered.replace("\x1b", "<ESC>")
    if len(rendered) > limit:
        return rendered[:limit] + f"... <{len(rendered) - limit} chars omitted>"
    return rendered


counts: dict[str, int] = {}
calls = 0
outputs = 0
messages = 0

with TRACE.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        event = json.loads(line)
        event_type = event.get("type", "<missing>")
        counts[event_type] = counts.get(event_type, 0) + 1
        payload = event.get("payload", {})
        payload_type = payload.get("type")

        if event_type == "response_item" and payload_type == "function_call":
            calls += 1
            print(
                f"LINE {line_number} CALL {payload.get('name')}: "
                f"{compact(payload.get('arguments', ''))}"
            )
        elif event_type == "response_item" and payload_type == "function_call_output":
            outputs += 1
            print(
                f"LINE {line_number} OUTPUT {payload.get('call_id')}: "
                f"{compact(payload.get('output', ''))}"
            )
        elif event_type == "event_msg" and payload_type == "agent_message":
            messages += 1
            print(f"LINE {line_number} AGENT: {compact(payload.get('message', ''))}")
        elif event_type == "event_msg" and payload_type in {
            "task_started",
            "task_complete",
        }:
            print(f"LINE {line_number} EVENT {payload_type}: {compact(payload)}")

print(f"PARSED_LINES={sum(counts.values())}")
print(f"EVENT_COUNTS={json.dumps(counts, sort_keys=True)}")
print(f"FUNCTION_CALLS={calls}")
print(f"FUNCTION_OUTPUTS={outputs}")
print(f"AGENT_MESSAGES={messages}")
