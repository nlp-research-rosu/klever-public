#!/usr/bin/env python3
"""Render the auditable, non-encrypted actions from the untrusted Codex trace."""

from __future__ import annotations

import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T05-24-27-019f8e81-5130-73c3-84ea-e9a1baf016ad.jsonl"
)


def compact(value: object, limit: int = 1600) -> str:
    rendered = json.dumps(value, ensure_ascii=False, sort_keys=True)
    if len(rendered) <= limit:
        return rendered
    return rendered[:limit] + f"... <truncated {len(rendered) - limit} chars>"


for line_number, line in enumerate(TRACE.read_text().splitlines(), 1):
    record = json.loads(line)
    if record.get("type") != "response_item":
        continue
    payload = record.get("payload", {})
    payload_type = payload.get("type")
    if payload_type == "reasoning":
        continue
    if payload_type == "message":
        role = payload.get("role")
        if role in {"assistant", "user"}:
            print(f"line {line_number} message/{role}: {compact(payload.get('content'))}")
    elif payload_type in {"function_call", "custom_tool_call"}:
        name = payload.get("name")
        arguments = payload.get("arguments", payload.get("input"))
        print(f"line {line_number} {payload_type}/{name}: {compact(arguments)}")
    elif payload_type in {"function_call_output", "custom_tool_call_output"}:
        output = payload.get("output")
        print(f"line {line_number} {payload_type}: {compact(output, 1000)}")
