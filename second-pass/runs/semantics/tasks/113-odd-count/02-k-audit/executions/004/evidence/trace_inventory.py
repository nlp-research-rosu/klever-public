#!/usr/bin/env python3
"""Read the complete generation JSONL trace and inventory its actions."""

from __future__ import annotations

import collections
import json
from pathlib import Path


trace = next(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
tool_calls: dict[str, tuple[str, object]] = {}
tool_outputs: dict[str, object] = {}
assistant_messages: list[str] = []

with trace.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        item = json.loads(line)
        top_types[item.get("type", "<none>")] += 1
        payload = item.get("payload", {})
        payload_type = payload.get("type", "<none>")
        payload_types[payload_type] += 1
        if payload_type in ("function_call", "custom_tool_call"):
            raw = payload.get("arguments", payload.get("input"))
            if isinstance(raw, str):
                try:
                    raw = json.loads(raw)
                except json.JSONDecodeError:
                    pass
            tool_calls[payload["call_id"]] = (payload.get("name", "<unknown>"), raw)
        elif payload_type in ("function_call_output", "custom_tool_call_output"):
            tool_outputs[payload["call_id"]] = payload.get("output")
        elif payload_type == "message" and payload.get("role") == "assistant":
            for content in payload.get("content", []):
                if content.get("type") == "output_text":
                    assistant_messages.append(content.get("text", ""))

print(f"trace={trace}")
print(f"lines={line_number}")
print(f"top_types={dict(sorted(top_types.items()))}")
print(f"payload_types={dict(sorted(payload_types.items()))}")
print(f"tool_calls={len(tool_calls)} outputs={len(tool_outputs)}")
print("tool_call_inventory:")
for number, (call_id, (name, args)) in enumerate(tool_calls.items(), 1):
    output = tool_outputs.get(call_id)
    # Keep this audit log bounded while retaining status-bearing tails.
    output_text = json.dumps(output, ensure_ascii=False) if not isinstance(output, str) else output
    tail = output_text[-1200:].replace("\x1b", "<ESC>")
    print(f"[{number}] name={name} call_id={call_id}")
    print(f"args={json.dumps(args, ensure_ascii=False, sort_keys=True)}")
    print(f"output_tail={tail}")
print("assistant_message_inventory:")
for number, message in enumerate(assistant_messages, 1):
    print(f"[{number}] {message}")
