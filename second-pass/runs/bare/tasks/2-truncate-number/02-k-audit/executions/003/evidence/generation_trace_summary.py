#!/usr/bin/env python3
"""Summarize every recorded generation tool call without trusting its claims."""

from __future__ import annotations

import json
from pathlib import Path


trace = next(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
events = [json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()]
outputs: dict[str, object] = {}
for event in events:
    payload = event.get("payload", {})
    if isinstance(payload, dict) and payload.get("type") in {
        "function_call_output",
        "custom_tool_call_output",
    }:
        outputs[str(payload.get("call_id"))] = payload.get("output")


def compact(value: object, limit: int) -> str:
    if isinstance(value, str):
        text = value
    else:
        text = json.dumps(value, sort_keys=True)
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit] + "...[bounded]"


for line_number, event in enumerate(events, 1):
    payload = event.get("payload", {})
    if not isinstance(payload, dict):
        continue
    if payload.get("type") in {"function_call", "custom_tool_call"}:
        call_id = str(payload.get("call_id"))
        print(
            f"TRACE line={line_number} tool={payload.get('name')} "
            f"input={compact(payload.get('input'), 700)}"
        )
        print(f"TRACE output={compact(outputs.get(call_id), 500)}")
    elif payload.get("type") == "message" and payload.get("role") in {"user", "assistant"}:
        print(
            f"TRACE line={line_number} role={payload.get('role')} "
            f"message={compact(payload.get('content'), 700)}"
        )

print(f"TRACE_SUMMARY_OK events={len(events)}")
