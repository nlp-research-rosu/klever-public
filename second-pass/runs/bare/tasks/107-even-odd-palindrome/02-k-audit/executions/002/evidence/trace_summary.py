#!/usr/bin/env python3
"""Read every structured generation-trace record and summarize auditable actions."""

from __future__ import annotations

import collections
import json
from pathlib import Path


root = Path("/generation-evidence/codex-trace")
top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
commands: list[tuple[int, str, str]] = []
final_messages: list[tuple[int, str]] = []
record_count = 0

print("COMMAND: python3 /audit-output/evidence/trace_summary.py")
for path in sorted(root.rglob("*.jsonl")):
    print(f"TRACE_FILE {path.relative_to(root)}")
    with path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            record_count += 1
            record = json.loads(line)
            top_types[record.get("type", "<missing>")] += 1
            payload = record.get("payload", {})
            if isinstance(payload, dict):
                payload_type = str(payload.get("type", "<missing>"))
                payload_types[payload_type] += 1
                if payload_type in {"function_call", "custom_tool_call"}:
                    name = str(payload.get("name", payload.get("tool_name", "")))
                    arguments = payload.get("arguments", payload.get("input", ""))
                    if not isinstance(arguments, str):
                        arguments = json.dumps(arguments, sort_keys=True)
                    commands.append((line_number, name, arguments))
                if payload_type == "message" and payload.get("role") == "assistant":
                    text_parts = []
                    for item in payload.get("content", []):
                        if isinstance(item, dict) and isinstance(item.get("text"), str):
                            text_parts.append(item["text"])
                    if text_parts:
                        final_messages.append((line_number, "\n".join(text_parts)))

print(f"RECORD_COUNT {record_count}")
print("TOP_TYPES " + json.dumps(dict(sorted(top_types.items())), sort_keys=True))
print(
    "PAYLOAD_TYPES "
    + json.dumps(dict(sorted(payload_types.items())), sort_keys=True)
)
print(f"TOOL_CALL_COUNT {len(commands)}")
for line_number, name, arguments in commands:
    compact = " ".join(arguments.split())
    if len(compact) > 700:
        compact = compact[:700] + "...<bounded>"
    print(f"TOOL line={line_number} name={name} args={compact}")
print(f"ASSISTANT_MESSAGE_COUNT {len(final_messages)}")
for line_number, message in final_messages:
    compact = " ".join(message.split())
    if len(compact) > 1200:
        compact = compact[:1200] + "...<bounded>"
    print(f"ASSISTANT line={line_number} text={compact}")
