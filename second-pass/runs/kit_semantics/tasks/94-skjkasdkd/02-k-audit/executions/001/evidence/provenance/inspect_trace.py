#!/usr/bin/env python3
"""Parse every structured generation-trace record and report a bounded inventory."""

import collections
import json
from pathlib import Path


path = next(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
top_types = collections.Counter()
payload_types = collections.Counter()
tool_names = collections.Counter()
messages = []
output_statuses = collections.Counter()
lines = 0
for lines, raw in enumerate(path.open(), 1):
    record = json.loads(raw)
    top_types[record.get("type", "<none>")] += 1
    payload = record.get("payload", {})
    payload_type = payload.get("type", "<none>")
    payload_types[payload_type] += 1
    if record.get("type") == "response_item":
        if payload_type == "function_call":
            tool_names[payload.get("name", "<none>")] += 1
        elif payload_type == "function_call_output":
            output = str(payload.get("output", ""))
            if "exit_code" in output:
                output_statuses["has_exit_code"] += 1
            if "#Top" in output:
                output_statuses["contains_top"] += 1
            if "WarnStuckClaimState" in output:
                output_statuses["contains_stuck"] += 1
        elif payload_type == "message":
            content = payload.get("content", [])
            text = " ".join(
                str(item.get("text", ""))
                for item in content
                if isinstance(item, dict)
            )
            messages.append((payload.get("role"), text))

print("trace_path", path)
print("json_records", lines)
print("top_types", dict(top_types))
print("payload_types", dict(payload_types))
print("tool_names", dict(tool_names))
print("tool_output_markers", dict(output_statuses))
print("message_count", len(messages))
print("last_messages")
for role, message in messages[-8:]:
    compact = " ".join(message.split())
    print(role, len(message), compact[:500])
