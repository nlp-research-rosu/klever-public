#!/usr/bin/env python3
"""Summarize the untrusted generation JSONL without trusting its conclusions."""

import collections
import json
import pathlib

trace = pathlib.Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T21-52-48-019f8ce3-d1dc-7f80-b54a-00f6e2d254c8.jsonl"
)

top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
calls: list[tuple[int, str, str]] = []
outputs: dict[str, str] = {}
messages: list[tuple[int, str, str]] = []

with trace.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        event = json.loads(line)
        top_types[event.get("type", "<missing>")] += 1
        payload = event.get("payload", {})
        payload_type = payload.get("type", "<missing>")
        payload_types[payload_type] += 1
        if payload_type == "function_call":
            calls.append(
                (
                    line_number,
                    payload.get("name", "<missing>"),
                    payload.get("arguments", ""),
                )
            )
        elif payload_type == "function_call_output":
            outputs[payload.get("call_id", "<missing>")] = payload.get("output", "")
        elif payload_type == "message":
            role = payload.get("role", "<missing>")
            text = "\n".join(
                item.get("text", "")
                for item in payload.get("content", [])
                if item.get("type") in {"input_text", "output_text"}
            )
            messages.append((line_number, role, text))
        elif payload_type == "agent_message":
            messages.append((line_number, "assistant-event", payload.get("message", "")))

print(f"TRACE: {trace}")
print(f"LINES: {sum(top_types.values())}")
print("TOP_LEVEL_TYPES:", dict(sorted(top_types.items())))
print("PAYLOAD_TYPES:", dict(sorted(payload_types.items())))
print(f"FUNCTION_CALL_COUNT: {len(calls)}")
for line_number, name, arguments in calls:
    compact = arguments.replace("\n", "\\n")
    print(f"CALL line={line_number} name={name} args={compact[:1200]}")
print(f"FUNCTION_OUTPUT_COUNT: {len(outputs)}")
print(f"MESSAGE_COUNT: {len(messages)}")
for line_number, role, message in messages:
    if role.startswith("assistant"):
        compact = message.replace("\n", "\\n")
        print(f"MESSAGE line={line_number} role={role} text={compact[:2000]}")
