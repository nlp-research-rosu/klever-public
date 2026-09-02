#!/usr/bin/env python3
"""Bounded semantic inspection of every structured generation-trace event."""

import collections
import hashlib
import json
import pathlib


trace_files = sorted(
    pathlib.Path("/generation-evidence/codex-trace").rglob("*.jsonl")
)
calls = []
messages = []
counts = collections.Counter()

for path in trace_files:
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            event = json.loads(line)
            payload = event.get("payload")
            payload_type = payload.get("type") if isinstance(payload, dict) else None
            counts[str(payload_type)] += 1
            if payload_type == "agent_message":
                messages.append(
                    (
                        line_number,
                        payload.get("phase"),
                        payload.get("message", ""),
                    )
                )
            if payload_type in {"function_call", "custom_tool_call"}:
                name = payload.get("name")
                argument = payload.get("arguments", payload.get("input", ""))
                if not isinstance(argument, str):
                    argument = json.dumps(argument, sort_keys=True)
                calls.append(
                    (
                        line_number,
                        name,
                        len(argument),
                        hashlib.sha256(argument.encode()).hexdigest(),
                        argument[:300].replace("\n", "\\n"),
                    )
                )

print("trace_files=", [str(path) for path in trace_files])
print("payload_counts=", dict(sorted(counts.items())))
print("agent_message_count=", len(messages))
for line_number, phase, message in messages:
    print(f"AGENT_MESSAGE line={line_number} phase={phase}: {message}")
print("tool_call_count=", len(calls))
for line_number, name, size, digest, preview in calls:
    print(
        f"TOOL_CALL line={line_number} name={name} bytes={size} "
        f"sha256={digest} preview={preview}"
    )
