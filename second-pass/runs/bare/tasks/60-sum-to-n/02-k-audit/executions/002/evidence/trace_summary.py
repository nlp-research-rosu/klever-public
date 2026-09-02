#!/usr/bin/env python3
"""Render the untrusted structured generation trace into a bounded audit summary."""

from __future__ import annotations

import collections
import json
from pathlib import Path


trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
if len(trace_files) != 1:
    raise SystemExit(f"expected exactly one JSONL trace, found {len(trace_files)}")

top_types: collections.Counter[str] = collections.Counter()
response_types: collections.Counter[str] = collections.Counter()
calls = 0
outputs = 0
final_messages: list[str] = []
with trace_files[0].open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        item = json.loads(line)
        item_type = item.get("type", "<missing>")
        top_types[item_type] += 1
        payload = item.get("payload", {})
        if item_type == "response_item":
            payload_type = payload.get("type", "<missing>")
            response_types[payload_type] += 1
            if payload_type == "custom_tool_call":
                calls += 1
                raw = str(payload.get("input", "")).replace("\n", "\\n")
                print(
                    f"CALL line={line_number} name={payload.get('name')} "
                    f"input={raw[:1200]}"
                )
            elif payload_type == "custom_tool_call_output":
                outputs += 1
                raw = json.dumps(payload.get("output", ""), ensure_ascii=True)
                print(f"OUTPUT line={line_number} value={raw[:1600]}")
            elif payload_type == "message" and payload.get("role") == "assistant":
                text = "\n".join(
                    part.get("text", "")
                    for part in payload.get("content", [])
                    if isinstance(part, dict)
                )
                if text:
                    final_messages.append(text)
        elif item_type == "event_msg" and payload.get("type") == "task_complete":
            print(
                f"TASK_COMPLETE line={line_number} "
                f"duration_ms={payload.get('duration_ms')}"
            )

print(f"trace={trace_files[0]}")
print(f"line_count={line_number}")
print(f"top_types={dict(top_types)}")
print(f"response_types={dict(response_types)}")
print(f"custom_calls={calls} custom_outputs={outputs}")
print("last_assistant_message:")
print(final_messages[-1])
print("TRACE_PARSE: PASS")
