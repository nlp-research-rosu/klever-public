#!/usr/bin/env python3
"""Read every structured trace record and emit a bounded structural audit."""

from __future__ import annotations

import collections
import json
from pathlib import Path

TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T23-03-06-019f8d24-2cbe-7ac0-a0ea-9ae7e6694037.jsonl"
)


def compact(value: object, limit: int = 1200) -> str:
    text = json.dumps(value, sort_keys=True, ensure_ascii=False)
    if len(text) > limit:
        return text[:limit] + f"...[truncated {len(text) - limit} chars]"
    return text


counts: collections.Counter[str] = collections.Counter()
payload_counts: collections.Counter[str] = collections.Counter()
records = []
with TRACE.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        record = json.loads(line)
        records.append(record)
        top_type = str(record.get("type", "<missing>"))
        counts[top_type] += 1
        payload = record.get("payload")
        if isinstance(payload, dict):
            payload_counts[str(payload.get("type", "<missing>"))] += 1
        if not isinstance(record, dict):
            raise AssertionError(f"line {line_number}: non-object record")

print(f"parsed_records={len(records)}")
print("top_level_type_counts=" + compact(counts))
print("payload_type_counts=" + compact(payload_counts))

print("\nSelected semantically relevant records:")
for line_number, record in enumerate(records, 1):
    payload = record.get("payload")
    if not isinstance(payload, dict):
        continue
    payload_type = payload.get("type")
    if payload_type in {
        "function_call",
        "function_call_output",
        "custom_tool_call",
        "custom_tool_call_output",
        "message",
        "agent_message",
    }:
        selected = {
            key: payload.get(key)
            for key in (
                "type",
                "role",
                "name",
                "call_id",
                "arguments",
                "input",
                "output",
                "content",
                "message",
            )
            if key in payload
        }
        print(f"line={line_number} {compact(selected)}")
