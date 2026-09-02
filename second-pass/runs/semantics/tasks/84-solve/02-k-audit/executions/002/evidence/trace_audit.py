#!/usr/bin/env python3
"""Read and summarize every structured generation-trace record."""

from __future__ import annotations

import collections
import json
from pathlib import Path


trace_root = Path("/generation-evidence/codex-trace")
files = sorted(path for path in trace_root.rglob("*.jsonl") if path.is_file() and not path.is_symlink())
outer_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
roles: collections.Counter[str] = collections.Counter()
tool_names: collections.Counter[str] = collections.Counter()
commands: list[str] = []
agent_messages: list[str] = []
line_count = 0

for path in files:
    with path.open() as stream:
        for line in stream:
            line_count += 1
            record = json.loads(line)
            outer_types[str(record.get("type"))] += 1
            payload = record.get("payload")
            if not isinstance(payload, dict):
                continue
            payload_types[str(payload.get("type"))] += 1
            if "role" in payload:
                roles[str(payload["role"])] += 1
            if payload.get("type") == "agent_message":
                agent_messages.append(str(payload.get("message", "")))
            if payload.get("type") == "function_call":
                name = str(payload.get("name"))
                tool_names[name] += 1
                arguments = payload.get("arguments")
                if name in {"exec_command", "exec"} and isinstance(arguments, str):
                    try:
                        decoded = json.loads(arguments)
                    except json.JSONDecodeError:
                        decoded = {"raw": arguments}
                    command = decoded.get("cmd") or decoded.get("raw")
                    if command:
                        commands.append(str(command))

print("files:", len(files))
print("lines:", line_count)
print("outer_types:", dict(sorted(outer_types.items())))
print("payload_types:", dict(sorted(payload_types.items())))
print("roles:", dict(sorted(roles.items())))
print("tool_names:", dict(sorted(tool_names.items())))
print("recorded_commands:", len(commands))
for index, command in enumerate(commands, 1):
    print(f"COMMAND {index}:")
    print(command)
print("agent_messages:", len(agent_messages))
for index, message in enumerate(agent_messages, 1):
    print(f"AGENT_MESSAGE {index}: {message}")
