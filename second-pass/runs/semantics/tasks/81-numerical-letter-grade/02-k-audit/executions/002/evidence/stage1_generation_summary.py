#!/usr/bin/env python3
"""Bounded structural summary after fully parsing the untrusted generation trace/log."""

from __future__ import annotations

import json
import re
from pathlib import Path


trace_path = next(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
records = []
with trace_path.open("r", encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        records.append((line_number, json.loads(line)))

print(f"TRACE={trace_path}")
print(f"TRACE_RECORDS={len(records)}")

function_calls = []
assistant_messages = []
event_messages = []
for line_number, record in records:
    payload = record.get("payload")
    if not isinstance(payload, dict):
        continue
    payload_type = payload.get("type")
    if payload_type in {"function_call", "custom_tool_call"}:
        name = payload.get("name") or payload.get("tool_name") or "<unnamed>"
        arguments = payload.get("arguments") or payload.get("input") or ""
        if not isinstance(arguments, str):
            arguments = json.dumps(arguments, sort_keys=True)
        function_calls.append((line_number, name, arguments))
    elif payload_type == "message" and payload.get("role") == "assistant":
        assistant_messages.append((line_number, payload))
    elif payload_type in {"agent_message", "task_complete"}:
        event_messages.append((line_number, payload))

print(f"TRACE_TOOL_CALLS={len(function_calls)}")
for line_number, name, arguments in function_calls:
    command = None
    if name in {"exec_command", "functions.exec_command"}:
        try:
            decoded = json.loads(arguments)
            command = decoded.get("cmd")
        except (json.JSONDecodeError, AttributeError):
            command = None
    if command is not None:
        compact = command.replace("\n", "\\n")
        print(f"TRACE_CALL line={line_number} name={name} cmd={compact[:1000]}")
    else:
        print(
            f"TRACE_CALL line={line_number} name={name} "
            f"arguments_chars={len(arguments)}"
        )

print(f"TRACE_ASSISTANT_MESSAGES={len(assistant_messages)}")
for line_number, payload in assistant_messages:
    text_parts = []
    for item in payload.get("content", []):
        if isinstance(item, dict) and isinstance(item.get("text"), str):
            text_parts.append(item["text"])
    text = "\n".join(text_parts).replace("\n", "\\n")
    print(f"TRACE_ASSISTANT line={line_number} text={text[:2000]}")

print(f"TRACE_AGENT_EVENTS={len(event_messages)}")
for line_number, payload in event_messages:
    text = json.dumps(payload, sort_keys=True)
    print(f"TRACE_EVENT line={line_number} payload={text[:2000]}")

output_path = Path("/generation-evidence/codex-output.log")
patterns = re.compile(
    r"(kompile|kprove|krun|#Top|WarnStuckClaimState|\\[Error\\]|"
    r"RESULT:|KPROVE_PASSED|exit code|Process exited with code)"
)
matched = []
total_lines = 0
with output_path.open("r", encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        total_lines = line_number
        if patterns.search(line):
            matched.append((line_number, line.rstrip("\n")))

print(f"OUTPUT_LOG_LINES={total_lines}")
print(f"OUTPUT_RELEVANT_LINES={len(matched)}")
for line_number, line in matched:
    print(f"OUTPUT line={line_number} text={line[:1200]}")

print("GENERATION_RECORDS_SUMMARY_OK")
