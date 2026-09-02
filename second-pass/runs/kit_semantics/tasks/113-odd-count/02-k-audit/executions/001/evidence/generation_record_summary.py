#!/usr/bin/env python3
"""Read every generation trace/log record and emit a bounded audit summary."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path


root = Path("/generation-evidence")
trace_files = sorted((root / "codex-trace").rglob("*.jsonl"))
top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
tool_names: collections.Counter[str] = collections.Counter()
commands: list[tuple[int, str]] = []
assistant_messages: list[tuple[int, str]] = []
invalid_lines: list[int] = []
trace_line_count = 0

for trace_file in trace_files:
    for line_number, line in enumerate(trace_file.read_text().splitlines(), 1):
        trace_line_count += 1
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            invalid_lines.append(line_number)
            continue
        top_types[event.get("type", "<missing>")] += 1
        payload = event.get("payload")
        if not isinstance(payload, dict):
            continue
        payload_type = str(payload.get("type", "<missing>"))
        payload_types[payload_type] += 1
        if payload_type in {"function_call", "custom_tool_call"}:
            name = str(payload.get("name", "<missing>"))
            tool_names[name] += 1
            if name == "exec_command":
                arguments = payload.get("arguments", "{}")
                try:
                    parsed = json.loads(arguments)
                    command = str(parsed.get("cmd", ""))
                except (json.JSONDecodeError, AttributeError):
                    command = str(arguments)
                commands.append((line_number, command))
        if payload_type == "message" and payload.get("role") == "assistant":
            content = payload.get("content", [])
            text = "\n".join(
                str(block.get("text", ""))
                for block in content
                if isinstance(block, dict)
            )
            assistant_messages.append((line_number, text))

output_text = (root / "codex-output.log").read_text(errors="replace")
last_text = (root / "codex-last.txt").read_text(errors="replace")
markers = {
    "#Top": output_text.count("#Top"),
    "WarnStuckClaimState": output_text.count("WarnStuckClaimState"),
    "KPROVE_PASSED": output_text.count("KPROVE_PASSED"),
    "PARTIAL": output_text.count("PARTIAL"),
    "BLOCKED": output_text.count("BLOCKED"),
}

print(f"TRACE_FILES={len(trace_files)}")
print(f"TRACE_LINES={trace_line_count}")
print(f"TRACE_INVALID_JSON_LINES={invalid_lines}")
print("TOP_TYPES " + " ".join(f"{k}={v}" for k, v in sorted(top_types.items())))
print(
    "PAYLOAD_TYPES "
    + " ".join(f"{k}={v}" for k, v in sorted(payload_types.items()))
)
print("TOOL_NAMES " + " ".join(f"{k}={v}" for k, v in sorted(tool_names.items())))
print(f"EXEC_COMMAND_COUNT={len(commands)}")
for line_number, command in commands:
    one_line = re.sub(r"\s+", " ", command).strip()
    if len(one_line) > 500:
        one_line = one_line[:500] + "...[bounded]"
    print(f"COMMAND trace_line={line_number} {one_line}")

print(f"ASSISTANT_MESSAGE_COUNT={len(assistant_messages)}")
for line_number, message in assistant_messages:
    one_line = re.sub(r"\s+", " ", message).strip()
    if len(one_line) > 1000:
        one_line = one_line[:1000] + "...[bounded]"
    print(f"ASSISTANT_MESSAGE trace_line={line_number} {one_line}")

print(f"CODEX_OUTPUT_BYTES={len(output_text.encode())}")
print("CODEX_OUTPUT_MARKERS " + " ".join(f"{k}={v}" for k, v in markers.items()))
print(f"CODEX_LAST_BYTES={len(last_text.encode())}")
print("CODEX_LAST_BEGIN")
print(last_text.rstrip())
print("CODEX_LAST_END")
