#!/usr/bin/env python3
"""Bounded structural inspection of the required pipeline-v3 Codex trace."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import json


trace_path = next(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
top_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
function_names: Counter[str] = Counter()
custom_names: Counter[str] = Counter()
exec_commands = []
patch_targets = []
user_messages = []
assistant_messages = []
selected_event = None

for line_number, line in enumerate(trace_path.open(), start=1):
    record = json.loads(line)
    top_types[record.get("type")] += 1
    payload = record.get("payload", {})
    payload_type = payload.get("type")
    payload_types[payload_type] += 1
    if payload_type == "function_call":
        name = payload.get("name")
        function_names[name] += 1
        if name == "exec_command":
            arguments = payload.get("arguments", "")
            exec_commands.append((line_number, arguments[:2000]))
    elif payload_type == "custom_tool_call":
        name = payload.get("name")
        custom_names[name] += 1
        if name == "apply_patch":
            call_input = payload.get("input", "")
            for patch_line in call_input.splitlines():
                if patch_line.startswith(
                    ("*** Add File:", "*** Update File:", "*** Delete File:")
                ):
                    patch_targets.append((line_number, patch_line))
    elif payload_type == "message":
        content = payload.get("content", [])
        text = "\n".join(
            part.get("text", "")
            for part in content
            if part.get("type") in {"input_text", "output_text"}
        )
        if payload.get("role") == "user":
            user_messages.append((line_number, text))
        elif payload.get("role") == "assistant":
            assistant_messages.append((line_number, text))
    elif payload_type == "token_count" and line_number == 2108:
        selected_event = payload

print(f"TRACE path={trace_path}")
print(f"LINES {sum(top_types.values())}")
print("TOP_TYPES", dict(sorted(top_types.items(), key=lambda row: str(row[0]))))
print(
    "PAYLOAD_TYPES",
    dict(sorted(payload_types.items(), key=lambda row: str(row[0]))),
)
print("FUNCTION_CALLS", dict(sorted(function_names.items())))
print("CUSTOM_CALLS", dict(sorted(custom_names.items())))
print(f"SELECTED_USAGE_EVENT_PRESENT {selected_event is not None}")

for line_number, text in user_messages:
    print(f"USER_MESSAGE line={line_number} text={text[:4000]!r}")

for line_number, command in exec_commands:
    print(f"EXEC_COMMAND line={line_number} arguments={command!r}")

for line_number, target in patch_targets:
    print(f"PATCH_TARGET line={line_number} {target}")

for line_number, text in assistant_messages[-12:]:
    print(f"ASSISTANT_MESSAGE line={line_number} text={text[:4000]!r}")
