#!/usr/bin/env python3
"""Bounded structural inspection of every record in the generation JSONL."""

from __future__ import annotations

import collections
import json
from pathlib import Path


trace = next(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
outer_types = collections.Counter()
payload_types = collections.Counter()
calls = []
outputs = []
record_count = 0

with trace.open() as stream:
    for line_number, line in enumerate(stream, 1):
        record_count += 1
        record = json.loads(line)
        outer_types[record.get("type")] += 1
        payload = record.get("payload", {})
        payload_type = payload.get("type")
        payload_types[payload_type] += 1
        if payload_type in ("function_call", "custom_tool_call"):
            value = payload.get("arguments") or payload.get("input") or ""
            calls.append((line_number, payload.get("name"), len(str(value))))
        if payload_type in ("function_call_output", "custom_tool_call_output"):
            value = payload.get("output") or ""
            outputs.append((line_number, len(str(value))))

print(f"trace={trace}")
print(f"records_parsed={record_count}")
print(f"outer_types={dict(sorted(outer_types.items(), key=lambda item: str(item[0])))}")
print(f"payload_types={dict(sorted(payload_types.items(), key=lambda item: str(item[0])))}")
print("tool_calls=line,name,serialized_input_bytes")
for item in calls:
    print(*item, sep=",")
print("tool_outputs=line,serialized_output_bytes")
for item in outputs:
    print(*item, sep=",")
