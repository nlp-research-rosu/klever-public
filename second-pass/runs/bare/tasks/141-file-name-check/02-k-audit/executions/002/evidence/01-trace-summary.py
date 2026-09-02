#!/usr/bin/env python3
"""Parse every structured generation-trace record and summarize untrusted claims."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T07-26-43-019f89ca-e5fc-7482-b894-6e10d45410ce.jsonl"
)

top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
calls: list[tuple[int, str, str]] = []
final_messages: list[tuple[int, str]] = []

line_count = 0
for line_count, line in enumerate(TRACE.open(), 1):
    record = json.loads(line)
    top_types[record["type"]] += 1
    payload = record.get("payload") or {}
    payload_type = payload.get("type")
    payload_types[str(payload_type)] += 1
    if payload_type in {"custom_tool_call", "function_call"}:
        name = str(payload.get("name"))
        body = payload.get("input") or payload.get("arguments") or ""
        calls.append((line_count, name, str(body)))
    if payload_type in {"agent_message", "task_complete"}:
        body = payload.get("message") or payload.get("last_agent_message") or ""
        final_messages.append((line_count, str(body)))

print("line_count:", line_count)
print("top_types:", dict(sorted(top_types.items())))
print("payload_types:", dict(sorted(payload_types.items())))
print("tool_call_count:", len(calls))
for line_number, name, body in calls:
    one_line = " ".join(body.split())
    print("call:", line_number, name, one_line[:500])
print("final_claims:")
for line_number, body in final_messages[-3:]:
    print("line", line_number, " ".join(body.split())[:1000])
