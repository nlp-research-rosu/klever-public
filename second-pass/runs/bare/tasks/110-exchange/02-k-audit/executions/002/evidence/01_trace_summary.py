#!/usr/bin/env python3
"""Read every structured generation-trace record and emit an audit summary."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T06-36-30-019f899c-ec7c-7ca0-a088-956a8111c8c6.jsonl"
)


def one_line(value: object, limit: int = 800) -> str:
    text = str(value).replace("\n", "\\n")
    if len(text) > limit:
        return text[:limit] + f"...[truncated {len(text) - limit} chars]"
    return text


rows = [json.loads(line) for line in TRACE.read_text(encoding="utf-8").splitlines()]
print(f"TRACE {TRACE}")
print(f"ROWS {len(rows)}")
print("TOP_TYPES", dict(Counter(row.get("type") for row in rows)))
print(
    "PAYLOAD_TYPES",
    dict(Counter((row.get("payload") or {}).get("type") for row in rows)),
)

for line_number, row in enumerate(rows, 1):
    payload = row.get("payload") or {}
    payload_type = payload.get("type")
    if payload_type in {"agent_message", "message"}:
        if payload_type == "agent_message":
            text = payload.get("message", "")
            role = payload.get("phase", "")
        else:
            role = payload.get("role", "")
            if role not in {"assistant"}:
                continue
            content = payload.get("content") or []
            text = " ".join(
                item.get("text", "")
                for item in content
                if isinstance(item, dict) and "text" in item
            )
        print(f"LINE {line_number} MESSAGE role={role} {one_line(text, 1600)}")
    elif payload_type in {"custom_tool_call", "function_call"}:
        body = payload.get("input")
        if body is None:
            body = payload.get("arguments")
        print(
            f"LINE {line_number} CALL {payload.get('name')} "
            f"{one_line(body, 2400)}"
        )
    elif payload_type in {"custom_tool_call_output", "function_call_output"}:
        output = payload.get("output", "")
        print(f"LINE {line_number} OUTPUT {one_line(output, 2400)}")
    elif payload_type == "task_complete":
        print(f"LINE {line_number} TASK_COMPLETE {one_line(payload)}")

print("TRACE_SUMMARY_COMPLETE")
