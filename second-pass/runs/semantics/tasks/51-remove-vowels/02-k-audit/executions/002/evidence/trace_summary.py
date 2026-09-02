#!/usr/bin/env python3
"""Parse every structured generation-trace line and summarize observable events."""

from __future__ import annotations

import collections
import json
from pathlib import Path


trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
assert trace_files, "no structured trace JSONL"

outer_counts: collections.Counter[str] = collections.Counter()
payload_counts: collections.Counter[str] = collections.Counter()
tool_calls: list[tuple[int, str, str]] = []
tool_outputs = 0
final_messages: list[tuple[int, str]] = []
last_usage: dict[str, object] | None = None

for trace_file in trace_files:
    print(f"TRACE FILE {trace_file} bytes={trace_file.stat().st_size}")
    with trace_file.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            event = json.loads(line)
            outer_type = str(event.get("type"))
            payload = event.get("payload", {})
            payload_type = str(payload.get("type", ""))
            outer_counts[outer_type] += 1
            payload_counts[payload_type] += 1
            if outer_type == "response_item" and payload_type in {
                "function_call",
                "custom_tool_call",
            }:
                name = str(payload.get("name", ""))
                arguments = str(payload.get("arguments", payload.get("input", "")))
                arguments = arguments.replace("\n", "\\n")
                tool_calls.append((line_number, name, arguments[:500]))
            if outer_type == "response_item" and payload_type in {
                "function_call_output",
                "custom_tool_call_output",
            }:
                tool_outputs += 1
            if outer_type == "event_msg" and payload_type == "agent_message":
                final_messages.append((line_number, str(payload.get("message", ""))))
            if outer_type == "event_msg" and payload_type == "token_count":
                last_usage = payload.get("info")

print(f"OUTER COUNTS {dict(sorted(outer_counts.items()))}")
print(f"PAYLOAD COUNTS {dict(sorted(payload_counts.items()))}")
print(f"TOOL CALLS {len(tool_calls)} TOOL OUTPUTS {tool_outputs}")
for line_number, name, arguments in tool_calls:
    print(f"CALL line={line_number} name={name} args={arguments}")
print(f"AGENT MESSAGES {len(final_messages)}")
for line_number, message in final_messages:
    print(f"AGENT MESSAGE line={line_number}: {message}")
print(f"LAST TOKEN USAGE {last_usage}")
print("ALL TRACE LINES PARSED")
