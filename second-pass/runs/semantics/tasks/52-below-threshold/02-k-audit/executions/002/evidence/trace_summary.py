#!/usr/bin/env python3
"""Summarize every structured generation-trace event without trusting it."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T00-15-52-019f8d66-ccce-7290-978b-ee0c01f86d86.jsonl"
)


def compact(value: object, limit: int = 1000) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = text.replace("\x00", "\\0")
    if len(text) <= limit:
        return text
    digest = hashlib.sha256(text.encode()).hexdigest()
    return f"{text[:limit]} ... [truncated chars={len(text)} sha256={digest}]"


top_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
tool_calls = 0
tool_outputs = 0
messages = 0
line_count = 0

with TRACE.open(encoding="utf-8") as stream:
    for line_count, line in enumerate(stream, 1):
        event = json.loads(line)
        top = str(event.get("type"))
        payload = event.get("payload", {})
        ptype = str(payload.get("type")) if isinstance(payload, dict) else type(payload).__name__
        top_types[top] += 1
        payload_types[ptype] += 1

        if top == "response_item" and isinstance(payload, dict):
            if ptype == "function_call":
                tool_calls += 1
                print(
                    f"line={line_count} TOOL_CALL name={payload.get('name')} "
                    f"arguments={compact(payload.get('arguments'))}"
                )
            elif ptype == "custom_tool_call":
                tool_calls += 1
                raw_input = str(payload.get("input", ""))
                print(
                    f"line={line_count} CUSTOM_TOOL_CALL name={payload.get('name')} "
                    f"input_chars={len(raw_input)} input_sha256="
                    f"{hashlib.sha256(raw_input.encode()).hexdigest()} "
                    f"input={compact(raw_input)}"
                )
            elif ptype in {"function_call_output", "custom_tool_call_output"}:
                tool_outputs += 1
                output = str(payload.get("output", ""))
                first = output.splitlines()[0] if output.splitlines() else ""
                last = output.splitlines()[-1] if output.splitlines() else ""
                print(
                    f"line={line_count} TOOL_OUTPUT call_id={payload.get('call_id')} "
                    f"chars={len(output)} sha256={hashlib.sha256(output.encode()).hexdigest()} "
                    f"first={compact(first, 300)} last={compact(last, 300)}"
                )
            elif ptype == "message":
                messages += 1
                content = payload.get("content", [])
                text_parts = []
                if isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict):
                            text_parts.append(str(item.get("text", "")))
                text = "\n".join(text_parts)
                print(
                    f"line={line_count} MESSAGE role={payload.get('role')} "
                    f"chars={len(text)} sha256={hashlib.sha256(text.encode()).hexdigest()} "
                    f"text={compact(text)}"
                )

print(f"TRACE_SHA256={hashlib.sha256(TRACE.read_bytes()).hexdigest()}")
print(f"LINE_COUNT={line_count}")
print(f"TOP_TYPES={dict(sorted(top_types.items()))}")
print(f"PAYLOAD_TYPES={dict(sorted(payload_types.items()))}")
print(f"TOOL_CALLS={tool_calls}")
print(f"TOOL_OUTPUTS={tool_outputs}")
print(f"MESSAGES={messages}")
