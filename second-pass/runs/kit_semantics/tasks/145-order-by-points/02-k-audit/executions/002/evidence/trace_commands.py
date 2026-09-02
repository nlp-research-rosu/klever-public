#!/usr/bin/env python3
import json
from pathlib import Path


trace_root = Path("/generation-evidence/codex-trace")


def bounded(value, limit=4000):
    text = str(value)
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n...[truncated {len(text) - limit} characters]"


for path in sorted(trace_root.rglob("*.jsonl")):
    print(f"TRACE FILE {path}")
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            payload = record.get("payload", {})
            payload_type = payload.get("type")
            if payload_type in {
                "function_call",
                "function_call_output",
                "custom_tool_call",
                "custom_tool_call_output",
                "agent_message",
            }:
                print(f"LINE {line_number} TYPE {payload_type}")
                if payload_type == "function_call":
                    print(f"NAME {payload.get('name')}")
                    print(bounded(payload.get("arguments", "")))
                elif payload_type == "function_call_output":
                    print(bounded(payload.get("output", "")))
                elif payload_type == "custom_tool_call":
                    print(f"NAME {payload.get('name')}")
                    print(bounded(payload.get("input", "")))
                elif payload_type == "custom_tool_call_output":
                    print(bounded(payload.get("output", "")))
                else:
                    print(bounded(payload.get("message", "")))
