#!/usr/bin/env python3
"""Bounded structural inspection of the untrusted generation trace and log."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


ROOT = Path("/generation-evidence")
TRACE = next((ROOT / "codex-trace").rglob("*.jsonl"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
tool_names: collections.Counter[str] = collections.Counter()
commands: list[str] = []
final_messages: list[str] = []
parse_errors: list[str] = []

with TRACE.open(encoding="utf-8") as stream:
    for number, line in enumerate(stream, 1):
        try:
            event = json.loads(line)
        except Exception as err:  # evidence should say exactly where parsing failed
            parse_errors.append(f"line {number}: {type(err).__name__}: {err}")
            continue
        top_types[str(event.get("type", "<missing>"))] += 1
        payload = event.get("payload")
        if isinstance(payload, dict):
            payload_types[str(payload.get("type", "<missing>"))] += 1
            name = payload.get("name")
            if isinstance(name, str):
                tool_names[name] += 1
            if payload.get("type") == "function_call":
                args = payload.get("arguments")
                if isinstance(args, str):
                    try:
                        parsed_args = json.loads(args)
                    except json.JSONDecodeError:
                        parsed_args = {}
                    cmd = parsed_args.get("cmd")
                    if isinstance(cmd, str):
                        commands.append(cmd)
            if payload.get("type") == "agent_message":
                message = payload.get("message")
                if isinstance(message, str):
                    final_messages.append(message)

print(f"trace={TRACE}")
print(f"trace_sha256={digest(TRACE)}")
print(f"trace_lines={sum(top_types.values()) + len(parse_errors)}")
print(f"parse_errors={len(parse_errors)}")
for error in parse_errors:
    print(error)
print("top_level_types=" + json.dumps(dict(top_types), sort_keys=True))
print("payload_types=" + json.dumps(dict(payload_types), sort_keys=True))
print("tool_names=" + json.dumps(dict(tool_names), sort_keys=True))
print(f"function_call_commands={len(commands)}")
for index, command in enumerate(commands, 1):
    one_line = command.replace("\n", "\\n")
    print(f"command[{index}]={one_line[:1000]}")
print(f"agent_messages={len(final_messages)}")
for index, message in enumerate(final_messages, 1):
    one_line = message.replace("\n", "\\n")
    print(f"agent_message[{index}]={one_line[:2000]}")

log = (ROOT / "codex-output.log").read_text(encoding="utf-8", errors="replace")
print(f"codex_output_sha256={digest(ROOT / 'codex-output.log')}")
print(f"codex_output_lines={len(log.splitlines())}")
for needle in ("#Top", "kprove", "kompile", "VERDICT", "LEGITIMACY"):
    matching = [line for line in log.splitlines() if needle in line]
    print(f"codex_output_lines_containing_{needle!r}={len(matching)}")
    for line in matching[:20]:
        print(f"  {line[:1000]}")
