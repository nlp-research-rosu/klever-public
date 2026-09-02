#!/usr/bin/env python3
"""Validate and render the inspectable portions of the untrusted generation trace."""

import json
from pathlib import Path

TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/24/"
    "rollout-2026-07-24T23-46-28-019f9798-98c3-7780-b369-3a06c3b7ec88.jsonl"
)


def compact(value: object, limit: int = 1400) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = str(text).replace("\x00", "\\0")
    if len(text) <= limit:
        return text
    half = (limit - 80) // 2
    return text[:half] + f"\n... OMITTED {len(text) - 2 * half} CHARS ...\n" + text[-half:]


print(f"TRACE={TRACE}")
records = 0
for line_number, line in enumerate(TRACE.open(encoding="utf-8"), 1):
    record = json.loads(line)
    records += 1
    kind = record.get("type")
    payload = record.get("payload", {})
    subtype = payload.get("type", "")

    if kind == "response_item" and subtype == "message":
        role = payload.get("role")
        texts = [item.get("text", "") for item in payload.get("content", [])]
        print(f"\nLINE {line_number} MESSAGE role={role}")
        print(compact("\n".join(texts), 4000 if role in {"assistant", "user"} else 1200))
    elif kind == "response_item" and subtype in {"function_call", "custom_tool_call"}:
        print(
            f"\nLINE {line_number} CALL type={subtype} "
            f"name={payload.get('name')} call_id={payload.get('call_id')}"
        )
        print(compact(payload.get("arguments", payload.get("input", "")), 3000))
    elif kind == "response_item" and subtype in {
        "function_call_output",
        "custom_tool_call_output",
    }:
        print(
            f"\nLINE {line_number} OUTPUT type={subtype} "
            f"call_id={payload.get('call_id')}"
        )
        print(compact(payload.get("output", ""), 1200))
    elif kind == "event_msg" and subtype in {
        "task_started",
        "task_complete",
        "user_message",
    }:
        print(f"\nLINE {line_number} EVENT type={subtype}")
        print(compact(payload, 2000))

print(f"\nJSONL_VALID records={records}")
