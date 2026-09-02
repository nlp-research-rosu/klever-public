#!/usr/bin/env python3
"""Read the entire untrusted JSONL generation trace and summarize its claims."""

from __future__ import annotations

import collections
import json
from pathlib import Path


trace_files = sorted(Path("/candidate/codex-trace").rglob("*.jsonl"))
print(f"trace_files={len(trace_files)}")

top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
record_count = 0
parse_errors = 0
interesting_commands: list[str] = []
final_messages: list[str] = []

for path in trace_files:
    print(f"trace={path} bytes={path.stat().st_size}")
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            record_count += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError as err:
                parse_errors += 1
                print(f"parse_error={path}:{line_number}:{err}")
                continue

            top_types[str(record.get("type"))] += 1
            payload = record.get("payload")
            if not isinstance(payload, dict):
                continue
            payload_type = str(payload.get("type"))
            payload_types[payload_type] += 1

            searchable = json.dumps(payload, sort_keys=True)
            if any(term in searchable for term in ("kompile", "krun", "kprove", "./prove.sh")):
                if payload_type in {"function_call", "custom_tool_call", "agent_message"}:
                    interesting_commands.append(searchable[:1600])

            if payload_type == "agent_message" and payload.get("phase") == "final_answer":
                final_messages.append(str(payload.get("message")))
            if (
                payload_type == "message"
                and payload.get("role") == "assistant"
                and payload.get("phase") == "final_answer"
            ):
                final_messages.append(searchable[:2400])

print(f"record_count={record_count}")
print(f"parse_errors={parse_errors}")
print(f"top_types={dict(top_types)}")
print(f"payload_types={dict(payload_types)}")
print(f"interesting_command_records={len(interesting_commands)}")
for index, command in enumerate(interesting_commands[-12:], 1):
    print(f"interesting[{index}]={command}")
print(f"final_messages={len(final_messages)}")
for index, message in enumerate(final_messages, 1):
    print(f"final[{index}]={message}")
