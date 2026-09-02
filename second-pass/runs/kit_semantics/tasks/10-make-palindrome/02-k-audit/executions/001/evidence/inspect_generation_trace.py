#!/usr/bin/env python3
"""Parse every structured generation record and summarize the untrusted trace."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path


JSON_RECORDS = (
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
)
TRACE = next(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))


for record in JSON_RECORDS:
    document = json.loads(record.read_text())
    assert isinstance(document, dict)
    print(f"parsed_json={record}")

top_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
tool_names: Counter[str] = Counter()
tool_calls: list[tuple[int, str, str]] = []
final_messages: list[str] = []
last_token_total = None

with TRACE.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        event = json.loads(line)
        top_type = str(event.get("type"))
        top_types[top_type] += 1
        payload = event.get("payload")
        if isinstance(payload, dict):
            payload_type = str(payload.get("type"))
            payload_types[payload_type] += 1
            if top_type == "response_item" and payload_type == "custom_tool_call":
                name = str(payload.get("name"))
                tool_names[name] += 1
                raw_input = str(payload.get("input", ""))
                summary = raw_input.replace("\n", "\\n")[:240]
                tool_calls.append((line_number, name, summary))
            if payload_type == "agent_message" and payload.get("phase") == "final_answer":
                final_messages.append(str(payload.get("message", "")))
            if payload_type == "token_count":
                info = payload.get("info", {})
                usage = info.get("total_token_usage", {})
                last_token_total = usage.get("total_tokens", last_token_total)

line_count = sum(top_types.values())
print(f"trace={TRACE}")
print(f"trace_sha256={hashlib.sha256(TRACE.read_bytes()).hexdigest()}")
print(f"trace_lines_parsed={line_count}")
print(f"top_level_types={dict(sorted(top_types.items()))}")
print(f"payload_types={dict(sorted(payload_types.items()))}")
print(f"tool_names={dict(sorted(tool_names.items()))}")
print(f"custom_tool_call_count={len(tool_calls)}")
for line_number, name, summary in tool_calls:
    print(f"tool_call line={line_number} name={name} input_prefix={summary}")
print(f"final_agent_message_count={len(final_messages)}")
print(f"last_token_total={last_token_total}")
assert line_count > 0
assert payload_types["task_complete"] == 1
assert final_messages
