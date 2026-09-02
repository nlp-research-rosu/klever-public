#!/usr/bin/env python3
"""Read and summarize every structured generation-trace event."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


trace_root = Path("/generation-evidence/codex-trace")
event_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
function_calls: list[tuple[int, str, str]] = []
function_outputs: list[tuple[int, str, str]] = []
messages: list[tuple[int, str, str]] = []
line_count = 0

for trace_path in sorted(trace_root.rglob("*.jsonl")):
    print(f"TRACE {trace_path}")
    with trace_path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            line_count += 1
            event = json.loads(line)
            event_type = str(event.get("type"))
            event_types[event_type] += 1
            payload = event.get("payload") or {}
            payload_type = str(payload.get("type"))
            payload_types[payload_type] += 1
            if event_type == "response_item" and payload_type == "function_call":
                function_calls.append(
                    (
                        line_number,
                        str(payload.get("name")),
                        str(payload.get("arguments")),
                    )
                )
            elif event_type == "response_item" and payload_type == "function_call_output":
                output = str(payload.get("output"))
                function_outputs.append(
                    (line_number, str(payload.get("call_id")), output[-1200:])
                )
            elif event_type == "response_item" and payload_type == "message":
                role = str(payload.get("role"))
                content = payload.get("content") or []
                text = "\n".join(
                    str(item.get("text", ""))
                    for item in content
                    if isinstance(item, dict)
                )
                messages.append((line_number, role, text))
            elif event_type == "event_msg" and payload_type == "agent_message":
                messages.append(
                    (line_number, "agent_message", str(payload.get("message")))
                )

print("VALID_JSON_LINES", line_count)
print("EVENT_TYPES", dict(sorted(event_types.items())))
print("PAYLOAD_TYPES", dict(sorted(payload_types.items())))
print("FUNCTION_CALLS")
for line_number, name, arguments in function_calls:
    print(f"  line={line_number} name={name} arguments={arguments}")
print("FUNCTION_OUTPUT_TAILS")
for line_number, call_id, output in function_outputs:
    print(f"  line={line_number} call_id={call_id} tail={output!r}")
print("NONEMPTY_MESSAGES")
for line_number, role, message in messages:
    if message:
        print(f"  line={line_number} role={role} text={message!r}")
