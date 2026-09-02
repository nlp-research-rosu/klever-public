#!/usr/bin/env python3
"""Bounded structural inspection of every JSONL generation-trace record."""

from __future__ import annotations

import collections
import json
from pathlib import Path


trace = Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T03-47-52-019f8902-899a-77b0-80ed-82a38b5648a8.jsonl"
)

top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
tool_calls = []
final_messages = []
last_token_usage = None

with trace.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        record = json.loads(line)
        top_type = record.get("type", "<missing>")
        top_types[top_type] += 1
        payload = record.get("payload")
        if isinstance(payload, dict):
            payload_type = payload.get("type")
            if isinstance(payload_type, str):
                payload_types[payload_type] += 1
            if payload_type in {"custom_tool_call", "function_call"}:
                name = payload.get("name", "<missing>")
                raw_input = payload.get("input", payload.get("arguments", ""))
                if not isinstance(raw_input, str):
                    raw_input = repr(raw_input)
                compact = " ".join(raw_input.split())
                tool_calls.append((line_number, name, compact[:500]))
            if payload_type == "message" and payload.get("role") == "assistant":
                content = payload.get("content")
                if isinstance(content, list):
                    texts = [
                        item.get("text", "")
                        for item in content
                        if isinstance(item, dict)
                        and item.get("type") in {"output_text", "input_text"}
                    ]
                    text = "\n".join(texts)
                    if "RESULT:" in text:
                        final_messages.append((line_number, text))
            if payload_type == "token_count":
                info = payload.get("info")
                if isinstance(info, dict):
                    last_token_usage = info.get("total_token_usage")

print(f"trace={trace}")
print(f"json_lines={sum(top_types.values())}")
print(f"top_level_types={dict(sorted(top_types.items()))}")
print(f"payload_types={dict(sorted(payload_types.items()))}")
print(f"tool_call_count={len(tool_calls)}")
for line_number, name, compact in tool_calls:
    print(f"TOOL line={line_number} name={name} input={compact}")
print(f"final_message_count={len(final_messages)}")
for line_number, text in final_messages:
    print(f"FINAL line={line_number}: {text}")
print(f"last_token_usage={last_token_usage}")
