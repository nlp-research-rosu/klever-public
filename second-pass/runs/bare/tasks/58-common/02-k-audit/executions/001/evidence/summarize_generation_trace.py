#!/usr/bin/env python3
"""Bounded extraction of untrusted claims from the structured generation trace."""

from __future__ import annotations

import json
from pathlib import Path


TRACE = Path(
    "/candidate/codex-trace/2026/07/22/"
    "rollout-2026-07-22T05-16-05-019f8953-4b0c-78f2-bbcc-2c3fb4e7a761.jsonl"
)


def bounded(value: object, limit: int = 2400) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    if len(text) <= limit:
        return text
    half = limit // 2
    return text[:half] + "\n...[BOUNDED]...\n" + text[-half:]


seen = 0
selected = 0
for line_number, line in enumerate(TRACE.read_text(encoding="utf-8").splitlines(), 1):
    seen += 1
    record = json.loads(line)
    outer_type = record.get("type")
    payload = record.get("payload") or {}
    payload_type = payload.get("type")

    if outer_type == "session_meta":
        summary = {
            key: payload.get(key)
            for key in ("session_id", "cwd", "cli_version", "model_provider")
        }
    elif outer_type == "event_msg" and payload_type in {
        "agent_message",
        "task_complete",
        "user_message",
    }:
        summary = payload.get("message", payload)
    elif outer_type == "response_item" and payload_type in {
        "custom_tool_call",
        "custom_tool_call_output",
        "function_call",
        "function_call_output",
        "message",
    }:
        summary = {
            key: payload.get(key)
            for key in ("role", "name", "input", "output", "content")
            if payload.get(key) is not None
        }
    else:
        continue

    selected += 1
    print(
        f"TRACE_LINE={line_number} OUTER={outer_type} PAYLOAD={payload_type}\n"
        + bounded(summary)
    )

print(f"TRACE_TOTAL_LINES={seen}")
print(f"TRACE_SELECTED_RECORDS={selected}")
