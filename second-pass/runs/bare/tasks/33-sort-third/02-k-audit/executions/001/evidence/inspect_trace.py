#!/usr/bin/env python3
"""Summarize the entire untrusted structured generation trace."""

from __future__ import annotations

import glob
import json
from collections import Counter


files = sorted(glob.glob("/candidate/codex-trace/**/*.jsonl", recursive=True))
print(f"TRACE_FILES={len(files)}")
outer_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
commands: list[str] = []
messages: list[str] = []
events = 0

for path in files:
    with open(path, encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            event = json.loads(line)
            events += 1
            outer_types[str(event.get("type", ""))] += 1
            payload = event.get("payload", {})
            payload_type = str(payload.get("type", ""))
            payload_types[payload_type] += 1

            if payload_type in {"function_call", "custom_tool_call"}:
                name = str(payload.get("name", ""))
                arguments = str(payload.get("arguments", payload.get("input", "")))
                commands.append(f"{path}:{line_number} {name} {arguments}")
            if payload_type in {"agent_message", "message"}:
                text = str(payload.get("message", payload.get("text", "")))
                if text:
                    messages.append(f"{path}:{line_number} {text}")

print(f"TRACE_EVENTS={events}")
print(f"OUTER_TYPES={dict(sorted(outer_types.items()))}")
print(f"PAYLOAD_TYPES={dict(sorted(payload_types.items()))}")
print("RELEVANT_UNTRUSTED_COMMANDS:")
for command in commands:
    if any(
        needle in command
        for needle in (
            "kompile",
            "kprove",
            "krun",
            "semantic.k",
            "verification.k",
            "spec.k",
            "solution.py",
            "solution.mpy",
            "prove.sh",
        )
    ):
        print(command[:4000])
print("UNTRUSTED_AGENT_MESSAGES:")
for message in messages:
    print(message[:4000])
