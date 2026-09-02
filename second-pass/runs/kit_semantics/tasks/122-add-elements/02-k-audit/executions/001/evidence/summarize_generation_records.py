#!/usr/bin/env python3
"""Bounded inspection summary of all untrusted generation records."""

from __future__ import annotations

import collections
import json
from pathlib import Path


root = Path("/generation-evidence")
trace_files = sorted((root / "codex-trace").rglob("*.jsonl"))
counts: collections.Counter[str] = collections.Counter()
exec_commands: list[str] = []
agent_messages: list[str] = []
malformed = 0

for trace_file in trace_files:
    with trace_file.open() as stream:
        for line in stream:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                malformed += 1
                continue
            payload = event.get("payload")
            if not isinstance(payload, dict):
                continue
            payload_type = str(payload.get("type"))
            counts[payload_type] += 1
            if payload_type == "function_call" and payload.get("name") == "exec_command":
                try:
                    arguments = json.loads(payload.get("arguments", "{}"))
                except json.JSONDecodeError:
                    arguments = {}
                command = str(arguments.get("cmd", "")).replace("\n", " ")
                exec_commands.append(command)
            if payload_type == "agent_message":
                agent_messages.append(str(payload.get("message", "")))

output_log = (root / "codex-output.log").read_text(errors="replace")
print(f"trace_files={len(trace_files)}")
print(f"trace_malformed_lines={malformed}")
print(f"trace_payload_counts={dict(sorted(counts.items()))}")
print(f"exec_command_count={len(exec_commands)}")
for index, command in enumerate(exec_commands, 1):
    print(f"exec[{index}]={command[:360]}")
print(f"agent_message_count={len(agent_messages)}")
for index, message in enumerate(agent_messages, 1):
    print(f"agent_message[{index}]={message.replace(chr(10), ' ')[:360]}")
print(f"codex_output_chars={len(output_log)}")
print(f"codex_output_lines={output_log.count(chr(10)) + 1}")
for marker in (
    "kprove",
    "#Top",
    "VALIDATED",
    "projectIntTotal",
    "loop-spec.k",
    "spec-vacuity.k",
    "RESULT: KPROVE_PASSED",
):
    print(f"codex_output_marker_count {marker!r}={output_log.count(marker)}")
