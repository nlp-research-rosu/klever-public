#!/usr/bin/env python3
"""Read-only, bounded summary of the untrusted structured generation trace."""

from __future__ import annotations

import collections
import json
import pathlib
import sys


def bounded(value: object, limit: int = 4000) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n...[truncated {len(text) - limit} characters]"


trace_path = pathlib.Path(sys.argv[1])
type_counts: collections.Counter[str] = collections.Counter()
payload_counts: collections.Counter[str] = collections.Counter()
selected: list[str] = []

with trace_path.open(encoding="utf-8") as trace_file:
    for line_number, line in enumerate(trace_file, 1):
        event = json.loads(line)
        event_type = str(event.get("type", "<missing>"))
        type_counts[event_type] += 1
        payload = event.get("payload", {})
        payload_type = str(payload.get("type", "<missing>"))
        payload_counts[f"{event_type}/{payload_type}"] += 1

        if event_type == "response_item":
            if payload_type in {"function_call", "custom_tool_call"}:
                selected.append(
                    f"line {line_number}: CALL {payload.get('name')}\n"
                    f"{bounded(payload.get('arguments', payload.get('input', '')))}"
                )
            elif payload_type in {"function_call_output", "custom_tool_call_output"}:
                selected.append(
                    f"line {line_number}: OUTPUT {payload.get('call_id', '')}\n"
                    f"{bounded(payload.get('output', ''))}"
                )
            elif payload_type == "message" and payload.get("role") == "assistant":
                selected.append(
                    f"line {line_number}: ASSISTANT\n"
                    f"{bounded(payload.get('content', ''))}"
                )
        elif event_type == "event_msg" and payload_type in {
            "agent_message",
            "task_complete",
            "turn_aborted",
        }:
            selected.append(
                f"line {line_number}: EVENT {payload_type}\n{bounded(payload)}"
            )

print(f"trace={trace_path}")
print(f"event_type_counts={dict(sorted(type_counts.items()))}")
print(f"payload_type_counts={dict(sorted(payload_counts.items()))}")
for item in selected:
    print(item)
