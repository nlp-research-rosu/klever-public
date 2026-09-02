#!/usr/bin/env python3
"""Validate and inventory every JSONL event in the untrusted generation trace."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")
counts: collections.Counter[str] = collections.Counter()
payload_counts: collections.Counter[str] = collections.Counter()
commands: list[tuple[int, str]] = []
messages: list[tuple[int, str, str]] = []
records = 0

for trace in sorted(TRACE_ROOT.rglob("*.jsonl")):
    print(f"TRACE_FILE {trace}")
    with trace.open() as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            records += 1
            counts[str(record.get("type"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type = str(payload.get("type"))
                payload_counts[payload_type] += 1
                if payload_type in {"function_call", "custom_tool_call"}:
                    name = payload.get("name", "")
                    arguments = payload.get("arguments") or payload.get("input") or ""
                    commands.append((line_number, f"{name} {arguments}"))
                if payload_type == "message":
                    role = str(payload.get("role"))
                    content = payload.get("content", [])
                    text = " ".join(
                        str(item.get("text", ""))
                        for item in content
                        if isinstance(item, dict)
                    )
                    messages.append((line_number, role, text[:240].replace("\n", "\\n")))
                if payload_type == "agent_message":
                    messages.append(
                        (
                            line_number,
                            "assistant/event",
                            str(payload.get("message", ""))[:240].replace("\n", "\\n"),
                        )
                    )

print(f"JSONL_RECORDS={records}")
for key, value in sorted(counts.items()):
    print(f"RECORD_TYPE {key}={value}")
for key, value in sorted(payload_counts.items()):
    print(f"PAYLOAD_TYPE {key}={value}")
print(f"TOOL_CALLS={len(commands)}")
for line_number, command in commands:
    print(f"TOOL line={line_number} {command}")
print(f"MESSAGES={len(messages)}")
for line_number, role, text in messages:
    print(f"MESSAGE line={line_number} role={role} text={text}")
