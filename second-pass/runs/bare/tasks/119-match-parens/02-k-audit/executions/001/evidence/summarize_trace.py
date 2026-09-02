#!/usr/bin/env python3
"""Read every untrusted generation-trace record and summarize its claims."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path(
    "/candidate/codex-trace/2026/07/22/"
    "rollout-2026-07-22T06-48-27-019f89a7-de49-7c02-9181-b3ba72376aad.jsonl"
)

top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
commands: list[str] = []
assistant_messages: list[str] = []
parse_errors: list[tuple[int, str]] = []
first_timestamp = None
last_timestamp = None
records = 0

with TRACE.open("r", encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        try:
            record = json.loads(line)
        except Exception as err:  # Trace is deliberately untrusted.
            parse_errors.append((line_number, repr(err)))
            continue
        records += 1
        timestamp = record.get("timestamp")
        first_timestamp = first_timestamp or timestamp
        last_timestamp = timestamp
        top_types[str(record.get("type"))] += 1
        payload = record.get("payload")
        if not isinstance(payload, dict):
            continue
        payload_type = str(payload.get("type"))
        payload_types[payload_type] += 1
        if payload_type == "function_call" and payload.get("name") == "exec_command":
            arguments = payload.get("arguments")
            try:
                args_object = json.loads(arguments) if isinstance(arguments, str) else arguments
            except Exception:
                args_object = None
            if isinstance(args_object, dict) and isinstance(args_object.get("cmd"), str):
                commands.append(args_object["cmd"])
        if payload_type == "message" and payload.get("role") == "assistant":
            pieces = []
            for item in payload.get("content", []):
                if isinstance(item, dict) and isinstance(item.get("text"), str):
                    pieces.append(item["text"])
            if pieces:
                assistant_messages.append("\n".join(pieces))

print(f"TRACE: {TRACE}")
print(f"RECORDS_READ: {records}")
print(f"PARSE_ERROR_COUNT: {len(parse_errors)}")
print(f"FIRST_TIMESTAMP: {first_timestamp}")
print(f"LAST_TIMESTAMP: {last_timestamp}")
print(f"TOP_LEVEL_TYPES: {dict(sorted(top_types.items()))}")
print(f"PAYLOAD_TYPES: {dict(sorted(payload_types.items()))}")
print(f"EXEC_COMMAND_COUNT: {len(commands)}")
for index, command in enumerate(commands, 1):
    print(f"COMMAND_{index}: {command}")
print(f"ASSISTANT_MESSAGE_COUNT: {len(assistant_messages)}")
for index, message in enumerate(assistant_messages, 1):
    print(f"ASSISTANT_MESSAGE_{index}: {message}")
for line_number, error in parse_errors:
    print(f"PARSE_ERROR line={line_number}: {error}")

raise SystemExit(1 if parse_errors else 0)
