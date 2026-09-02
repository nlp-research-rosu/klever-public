#!/usr/bin/env python3
"""Bounded structural inspection of the untrusted generation JSONL trace."""

from __future__ import annotations

import collections
import json
from pathlib import Path

TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T05-52-01-019f8e9a-8c6a-7f51-8b30-5aaf29584db0.jsonl"
)

outer = collections.Counter()
payload_types = collections.Counter()
calls = collections.Counter()
commands: list[str] = []
messages: list[str] = []
bad_lines: list[int] = []

with TRACE.open(encoding="utf-8") as handle:
    for line_number, line in enumerate(handle, 1):
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            bad_lines.append(line_number)
            continue
        outer[item.get("type", "<missing>")] += 1
        payload = item.get("payload")
        if not isinstance(payload, dict):
            continue
        payload_type = payload.get("type", "<missing>")
        payload_types[payload_type] += 1
        if payload_type in {"function_call", "custom_tool_call"}:
            name = str(payload.get("name", "<missing>"))
            calls[name] += 1
            if name == "exec_command":
                raw = payload.get("arguments", "")
                try:
                    arguments = json.loads(raw) if isinstance(raw, str) else raw
                except json.JSONDecodeError:
                    arguments = {}
                if isinstance(arguments, dict) and "cmd" in arguments:
                    commands.append(str(arguments["cmd"]))
        if payload_type == "agent_message":
            messages.append(str(payload.get("message", "")))

print("trace_path:", TRACE)
print("line_count:", sum(outer.values()) + len(bad_lines))
print("invalid_json_lines:", bad_lines)
print("outer_types:", dict(sorted(outer.items())))
print("payload_types:", dict(sorted(payload_types.items())))
print("tool_calls:", dict(sorted(calls.items())))
print("exec_command_count:", len(commands))
print("first_10_exec_commands:")
for command in commands[:10]:
    print("---")
    print(command[:2000])
print("last_10_exec_commands:")
for command in commands[-10:]:
    print("---")
    print(command[:2000])
print("assistant_message_count:", len(messages))
print("last_8_assistant_messages:")
for message in messages[-8:]:
    print("---")
    print(message[:4000])
