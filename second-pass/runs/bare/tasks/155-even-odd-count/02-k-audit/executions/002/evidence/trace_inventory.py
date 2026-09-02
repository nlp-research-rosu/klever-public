#!/usr/bin/env python3
"""Parse every structured generation-trace record and inventory its contents."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


def digest_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


root = Path("/generation-evidence/codex-trace")
files = sorted(path for path in root.rglob("*") if path.is_file())
top_counts: collections.Counter[str] = collections.Counter()
payload_counts: collections.Counter[str] = collections.Counter()
roles: collections.Counter[str] = collections.Counter()
commands: list[tuple[int, str, str]] = []
tool_outputs: list[tuple[int, str, int, str]] = []
messages: list[tuple[int, str, str, int, str]] = []
line_count = 0

for path in files:
    print(f"trace_begin path={path}")
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            line_count += 1
            record = json.loads(line)
            top_type = str(record.get("type", "<missing>"))
            top_counts[top_type] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type = str(payload.get("type", "<missing>"))
                payload_counts[payload_type] += 1
                role = payload.get("role")
                if isinstance(role, str):
                    roles[role] += 1

                if payload_type in {"function_call", "custom_tool_call"}:
                    name = str(payload.get("name", "<missing>"))
                    arguments = payload.get("arguments", payload.get("input", ""))
                    if not isinstance(arguments, str):
                        arguments = json.dumps(arguments, sort_keys=True)
                    commands.append((line_number, name, arguments))

                if payload_type in {"function_call_output", "custom_tool_call_output"}:
                    output = payload.get("output", "")
                    if not isinstance(output, str):
                        output = json.dumps(output, sort_keys=True)
                    tool_outputs.append((line_number, payload_type, len(output), digest_text(output)))

                if payload_type == "message":
                    chunks: list[str] = []
                    content = payload.get("content", [])
                    if isinstance(content, list):
                        for item in content:
                            if isinstance(item, dict):
                                text = item.get("text")
                                if isinstance(text, str):
                                    chunks.append(text)
                    text = "\n".join(chunks)
                    messages.append((line_number, str(role), payload_type, len(text), digest_text(text)))
                elif payload_type == "agent_message":
                    text = payload.get("message", "")
                    if isinstance(text, str):
                        messages.append((line_number, "assistant", payload_type, len(text), digest_text(text)))
            else:
                payload_counts["<non-dict>"] += 1
    print(f"trace_end path={path}")

print(f"trace_json_lines={line_count}")
print("top_level_types=" + json.dumps(dict(sorted(top_counts.items())), sort_keys=True))
print("payload_types=" + json.dumps(dict(sorted(payload_counts.items())), sort_keys=True))
print("message_roles=" + json.dumps(dict(sorted(roles.items())), sort_keys=True))
for line_number, role, kind, length, digest in messages:
    print(
        f"message line={line_number} role={role} kind={kind} "
        f"length={length} sha256={digest}"
    )
for line_number, name, arguments in commands:
    one_line = arguments.replace("\n", "\\n")
    print(
        f"tool_call line={line_number} name={name} args_length={len(arguments)} "
        f"args_sha256={digest_text(arguments)} args={one_line}"
    )
for line_number, kind, length, digest in tool_outputs:
    print(f"tool_output line={line_number} kind={kind} length={length} sha256={digest}")
print("trace_parse_result=PASS")
