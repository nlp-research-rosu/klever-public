#!/usr/bin/env python3
"""Read the complete untrusted generation trace and print a bounded summary."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


TRACE = Path(
    "/candidate/codex-trace/2026/07/22/"
    "rollout-2026-07-22T04-01-45-019f890f-3e04-7d23-b491-4c26b5662f21.jsonl"
)


def all_text(value: object) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "\n".join(all_text(v) for v in value.values())
    if isinstance(value, list):
        return "\n".join(all_text(v) for v in value)
    return ""


raw = TRACE.read_bytes()
top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
tool_names: collections.Counter[str] = collections.Counter()
assistant_messages: list[str] = []
notable_outputs: list[str] = []
invalid_lines: list[int] = []
total_text_chars = 0

for line_no, raw_line in enumerate(raw.splitlines(), 1):
    try:
        item = json.loads(raw_line)
    except json.JSONDecodeError:
        invalid_lines.append(line_no)
        continue
    top_types[str(item.get("type"))] += 1
    payload = item.get("payload") or {}
    payload_type = str(payload.get("type"))
    payload_types[payload_type] += 1
    payload_text = all_text(payload)
    total_text_chars += len(payload_text)
    if item.get("type") == "response_item":
        if payload_type in {"custom_tool_call", "function_call"}:
            tool_names[str(payload.get("name"))] += 1
        if payload_type == "message" and payload.get("role") == "assistant":
            assistant_messages.append(all_text(payload.get("content")))
        if payload_type in {"custom_tool_call_output", "function_call_output"}:
            if "#Top" in payload_text or "WarnStuckClaimState" in payload_text:
                notable_outputs.append(payload_text)

print(f"trace={TRACE}")
print(f"bytes={len(raw)}")
print(f"sha256={hashlib.sha256(raw).hexdigest()}")
print(f"lines={len(raw.splitlines())}")
print(f"invalid_json_lines={invalid_lines}")
print(f"deserialized_payload_text_chars={total_text_chars}")
print(f"top_types={dict(top_types)}")
print(f"payload_types={dict(payload_types)}")
print(f"tool_names={dict(tool_names)}")
print(f"assistant_message_count={len(assistant_messages)}")
for index, message in enumerate(assistant_messages, 1):
    compact = " ".join(message.split())
    print(f"assistant_message_{index}={compact[:600]}")
print(f"notable_proof_output_count={len(notable_outputs)}")
for index, output in enumerate(notable_outputs, 1):
    compact = " ".join(output.split())
    print(f"notable_output_{index}={compact[:800]}")
