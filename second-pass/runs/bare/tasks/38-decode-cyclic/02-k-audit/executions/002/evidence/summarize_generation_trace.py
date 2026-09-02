#!/usr/bin/env python3
"""Parse every generation trace line and emit a bounded audit summary."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def text_blocks(value: object) -> str:
    if isinstance(value, str):
        return value
    if not isinstance(value, list):
        return ""
    parts: list[str] = []
    for item in value:
        if isinstance(item, dict):
            text = item.get("text")
            if isinstance(text, str):
                parts.append(text)
    return "".join(parts)


def bounded(value: str, limit: int = 2400) -> str:
    if len(value) <= limit:
        return value
    half = limit // 2
    return (
        value[:half]
        + f"\n... [{len(value) - limit} characters omitted] ...\n"
        + value[-half:]
    )


files = sorted(TRACE_ROOT.rglob("*.jsonl"))
print(f"TRACE_FILES: {len(files)}")
top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
records = 0
calls: list[dict[str, object]] = []
outputs: dict[str, str] = {}
messages: list[tuple[str, str]] = []
selected_usage_events: list[dict[str, object]] = []

for path in files:
    print(f"TRACE_FILE: {path.relative_to(TRACE_ROOT)}")
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            record = json.loads(line)
            records += 1
            top_type = str(record.get("type"))
            top_types[top_type] += 1
            payload = record.get("payload")
            if not isinstance(payload, dict):
                continue
            payload_type = str(payload.get("type"))
            payload_types[payload_type] += 1
            if payload_type == "message":
                role = str(payload.get("role"))
                if role in {"user", "assistant"}:
                    messages.append((role, text_blocks(payload.get("content"))))
            elif payload_type in {"agent_message", "user_message"}:
                role = "assistant" if payload_type == "agent_message" else "user"
                messages.append((role, str(payload.get("message", ""))))
            elif payload_type in {"custom_tool_call", "function_call"}:
                calls.append(payload)
            elif payload_type in {"custom_tool_call_output", "function_call_output"}:
                outputs[str(payload.get("call_id"))] = text_blocks(payload.get("output"))
            elif payload_type == "token_count":
                selected_usage_events.append(payload)

print(f"VALID_JSONL_RECORDS: {records}")
print(f"TOP_LEVEL_TYPES: {dict(sorted(top_types.items()))}")
print(f"PAYLOAD_TYPES: {dict(sorted(payload_types.items()))}")

print("\nUSER/ASSISTANT MESSAGES")
for index, (role, message) in enumerate(messages, start=1):
    print(f"MESSAGE {index} ROLE={role} LENGTH={len(message)}")
    print(bounded(message))

print("\nTOOL CALLS AND BOUNDED OUTPUTS")
for index, call in enumerate(calls, start=1):
    call_id = str(call.get("call_id"))
    name = str(call.get("name"))
    call_input = call.get("input", call.get("arguments", ""))
    rendered_input = (
        call_input if isinstance(call_input, str) else json.dumps(call_input, sort_keys=True)
    )
    output = outputs.get(call_id, "<NO MATCHING OUTPUT>")
    print(
        f"CALL {index} NAME={name} CALL_ID={call_id} "
        f"INPUT_LENGTH={len(rendered_input)} OUTPUT_LENGTH={len(output)}"
    )
    print("INPUT:")
    print(bounded(rendered_input))
    print("OUTPUT:")
    print(bounded(output))

if selected_usage_events:
    final_usage = selected_usage_events[-1]
    print("\nFINAL TOKEN EVENT")
    print(json.dumps(final_usage, sort_keys=True))
