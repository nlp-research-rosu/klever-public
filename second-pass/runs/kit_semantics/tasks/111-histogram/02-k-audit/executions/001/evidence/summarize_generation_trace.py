#!/usr/bin/env python3
"""Read the complete structured generation trace and emit a bounded audit summary."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/25/"
    "rollout-2026-07-25T01-55-45-019f980e-f5c4-70d2-847e-4fd3f905af78.jsonl"
)


def compact(value: object, limit: int = 500) -> str:
    text = json.dumps(value, sort_keys=True, ensure_ascii=True)
    text = " ".join(text.split())
    if len(text) > limit:
        return text[:limit] + "...<truncated>"
    return text


top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
tool_calls: list[tuple[int, str, str]] = []
assistant_messages: list[tuple[int, str]] = []
line_count = 0

with TRACE.open("r", encoding="utf-8") as handle:
    for line_count, line in enumerate(handle, 1):
        record = json.loads(line)
        top_types[str(record.get("type"))] += 1
        payload = record.get("payload")
        if not isinstance(payload, dict):
            continue
        payload_type = str(payload.get("type"))
        payload_types[payload_type] += 1
        if payload_type in {"function_call", "custom_tool_call"}:
            name = str(payload.get("name"))
            raw = payload.get("arguments", payload.get("input", ""))
            if isinstance(raw, str):
                try:
                    parsed = json.loads(raw)
                except (ValueError, TypeError):
                    parsed = raw
            else:
                parsed = raw
            tool_calls.append((line_count, name, compact(parsed)))
        if payload_type == "message" and payload.get("role") == "assistant":
            pieces: list[str] = []
            for item in payload.get("content", []):
                if isinstance(item, dict) and "text" in item:
                    pieces.append(str(item["text"]))
            assistant_messages.append((line_count, " ".join(" ".join(pieces).split())))

print(f"trace lines parsed: {line_count}")
print(f"top-level types: {dict(sorted(top_types.items()))}")
print(f"payload types: {dict(sorted(payload_types.items()))}")
print(f"tool/custom calls: {len(tool_calls)}")
print("tool/custom call summaries:")
for line_number, name, summary in tool_calls:
    print(f"  line {line_number}: {name}: {summary}")
print("assistant messages:")
for line_number, message in assistant_messages:
    print(f"  line {line_number}: {message[:1000]}")
