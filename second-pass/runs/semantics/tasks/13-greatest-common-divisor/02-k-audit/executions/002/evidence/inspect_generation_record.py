#!/usr/bin/env python3
"""Parse every structured trace record and summarize observable actions."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


trace_path = Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T21-18-11-019f8cc4-2204-79c0-90c8-74fabe114144.jsonl"
)
output_path = Path("/generation-evidence/codex-output.log")

top_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
visible_actions = []
bad_lines = []

for line_number, raw_line in enumerate(trace_path.read_text().splitlines(), 1):
    try:
        record = json.loads(raw_line)
    except Exception as err:  # pragma: no cover - audit diagnostic
        bad_lines.append((line_number, repr(err)))
        continue
    top_types[record.get("type", "<none>")] += 1
    payload = record.get("payload")
    if not isinstance(payload, dict):
        continue
    payload_type = payload.get("type", "<none>")
    payload_types[payload_type] += 1
    if payload_type in {"agent_message", "custom_tool_call", "function_call"}:
        visible_actions.append(
            {
                "line": line_number,
                "type": payload_type,
                "name": payload.get("name"),
                "phase": payload.get("phase"),
                "message": payload.get("message"),
                "input": payload.get("input"),
                "arguments": payload.get("arguments"),
            }
        )

print(f"trace_sha256={hashlib.sha256(trace_path.read_bytes()).hexdigest()}")
print(f"trace_lines={sum(top_types.values())}")
print(f"trace_top_types={dict(top_types)}")
print(f"trace_payload_types={dict(payload_types)}")
print(f"trace_bad_json_lines={bad_lines}")
print(f"output_log_sha256={hashlib.sha256(output_path.read_bytes()).hexdigest()}")
print(f"output_log_lines={len(output_path.read_text(errors='replace').splitlines())}")
print("visible_action_sequence=")
for action in visible_actions:
    encoded = json.dumps(action, sort_keys=True)
    print(encoded)
