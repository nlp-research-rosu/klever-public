#!/usr/bin/env python3
"""Bounded inspection summary of every structured generation-trace record."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T02-57-20-019f8dfa-a035-7bf1-8404-35efaf6246c7.jsonl"
)


def short(value: object, limit: int = 500) -> str:
    rendered = json.dumps(value, ensure_ascii=True, sort_keys=True)
    if len(rendered) <= limit:
        return rendered
    return rendered[:limit] + f"...<truncated total_chars={len(rendered)}>"


counts: Counter[tuple[str | None, str | None]] = Counter()
function_calls = []
messages = []
tool_outputs = []

with TRACE.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        record = json.loads(line)
        payload = record.get("payload")
        subtype = payload.get("type") if isinstance(payload, dict) else None
        counts[(record.get("type"), subtype)] += 1
        if isinstance(payload, dict) and subtype in {
            "function_call",
            "custom_tool_call",
        }:
            function_calls.append(
                (
                    line_number,
                    payload.get("name"),
                    payload.get("arguments")
                    if "arguments" in payload
                    else payload.get("input"),
                )
            )
        if isinstance(payload, dict) and subtype in {
            "function_call_output",
            "custom_tool_call_output",
        }:
            output = str(payload.get("output", ""))
            tool_outputs.append(
                (
                    line_number,
                    len(output),
                    hashlib.sha256(output.encode()).hexdigest(),
                    output[:200],
                )
            )
        if isinstance(payload, dict) and subtype in {
            "message",
            "agent_message",
            "user_message",
        }:
            messages.append((line_number, subtype, payload))

print(f"trace={TRACE}")
print(f"valid_jsonl_lines={line_number}")
for key, count in sorted(counts.items(), key=lambda item: str(item[0])):
    print(f"event_count type={key[0]} subtype={key[1]} count={count}")
print(f"function_call_count={len(function_calls)}")
for line_number, name, arguments in function_calls:
    print(
        f"function_call line={line_number} name={name} "
        f"arguments={short(arguments)}"
    )
print(f"tool_output_count={len(tool_outputs)}")
for line_number, length, digest, prefix in tool_outputs:
    print(
        f"tool_output line={line_number} chars={length} sha256={digest} "
        f"prefix={short(prefix, 250)}"
    )
print(f"message_count={len(messages)}")
for line_number, subtype, payload in messages:
    redacted = {
        key: value
        for key, value in payload.items()
        if key not in {"encrypted_content", "base_instructions"}
    }
    print(
        f"message line={line_number} subtype={subtype} "
        f"payload={short(redacted, 1200)}"
    )
