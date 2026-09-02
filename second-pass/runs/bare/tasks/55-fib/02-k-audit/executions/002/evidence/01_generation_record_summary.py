#!/usr/bin/env python3
"""Bounded inspection of every structured trace record."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


trace = Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T05-11-27-019f894f-0f4b-7912-adc3-c85b88e6a8cd.jsonl"
)
top_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
tool_calls = []
final_messages = []

for line_number, line in enumerate(trace.read_text().splitlines(), 1):
    event = json.loads(line)
    top_types[event["type"]] += 1
    payload = event.get("payload", {})
    subtype = payload.get("type")
    if subtype:
        payload_types[subtype] += 1
    if event["type"] == "response_item" and subtype in {"function_call", "custom_tool_call"}:
        raw = payload.get("arguments", payload.get("input", ""))
        tool_calls.append((line_number, payload.get("name", ""), str(raw)[:500]))
    if subtype in {"agent_message", "task_complete"}:
        text = payload.get("message", payload.get("last_agent_message", ""))
        final_messages.append((line_number, subtype, text[:500]))

print(f"trace_lines={sum(top_types.values())}")
print(f"top_level_types={dict(top_types)}")
print(f"payload_types={dict(payload_types)}")
print(f"tool_call_count={len(tool_calls)}")
for line_number, name, raw in tool_calls:
    print(f"tool_call line={line_number} name={name} input={raw!r}")
for line_number, subtype, text in final_messages:
    print(f"terminal_event line={line_number} type={subtype} text={text!r}")
