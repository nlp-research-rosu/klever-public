#!/usr/bin/env python3
"""Summarize every structured generation trace record without trusting it."""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path


trace = Path(sys.argv[1])
outer_counts: collections.Counter[str] = collections.Counter()
inner_counts: collections.Counter[str] = collections.Counter()
records = []

for line_number, line in enumerate(trace.read_text(encoding="utf-8").splitlines(), 1):
    record = json.loads(line)
    outer = str(record.get("type"))
    payload = record.get("payload", {})
    inner = str(payload.get("type", ""))
    outer_counts[outer] += 1
    inner_counts[f"{outer}/{inner}"] += 1
    records.append((line_number, record, payload, inner))

print(f"TRACE {trace}")
print(f"RECORD_COUNT {len(records)}")
print("OUTER_COUNTS")
for key, count in sorted(outer_counts.items()):
    print(f"  {key}: {count}")
print("OUTER_INNER_COUNTS")
for key, count in sorted(inner_counts.items()):
    print(f"  {key}: {count}")

print("CHRONOLOGY")
for line_number, record, payload, inner in records:
    timestamp = record.get("timestamp", "")
    if record.get("type") == "response_item" and inner in {
        "function_call",
        "custom_tool_call",
        "function_call_output",
        "custom_tool_call_output",
    }:
        name = payload.get("name", "")
        arguments = payload.get("arguments", payload.get("input", ""))
        output = payload.get("output", "")
        if isinstance(arguments, str):
            arguments = arguments.replace("\n", "\\n")
        if isinstance(output, str):
            output_lines = output.splitlines()
            output = " | ".join(output_lines[:4])
            if len(output_lines) > 4:
                output += f" | ... ({len(output_lines)} lines)"
        print(
            f"{line_number:03d} {timestamp} {inner} name={name!r} "
            f"args={str(arguments)[:500]!r} output={str(output)[:500]!r}"
        )
    elif record.get("type") == "event_msg" and inner in {
        "agent_message",
        "user_message",
        "task_complete",
        "task_started",
        "turn_aborted",
    }:
        message = str(payload.get("message", "")).replace("\n", " ")
        print(f"{line_number:03d} {timestamp} {inner} {message[:700]}")

print("USAGE_EVENTS")
for line_number, record, payload, inner in records:
    if inner == "token_count":
        print(f"{line_number:03d} {json.dumps(payload, sort_keys=True)}")
