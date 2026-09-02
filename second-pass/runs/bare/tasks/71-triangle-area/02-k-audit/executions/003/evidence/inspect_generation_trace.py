#!/usr/bin/env python3
"""Validate and summarize every JSONL record in the untrusted generation trace."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


ROOT = Path("/generation-evidence/codex-trace")


def compact(value: object, limit: int = 500) -> str:
    rendered = json.dumps(value, sort_keys=True, ensure_ascii=False)
    if len(rendered) > limit:
        return rendered[:limit] + f"... <{len(rendered) - limit} chars omitted>"
    return rendered


files = sorted(path for path in ROOT.rglob("*") if path.is_file())
print(f"trace_files={len(files)}")
top_types: Counter[str] = Counter()
item_types: Counter[str] = Counter()
tool_names: Counter[str] = Counter()
total_lines = 0
commands: list[tuple[str, int, str]] = []
messages: list[tuple[str, int, str, str]] = []

for path in files:
    relative = path.relative_to(ROOT).as_posix()
    file_lines = 0
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            file_lines += 1
            total_lines += 1
            record = json.loads(line)
            record_type = str(record.get("type"))
            top_types[record_type] += 1
            payload = record.get("payload")
            if not isinstance(payload, dict):
                continue
            payload_type = str(payload.get("type"))
            if record_type == "response_item":
                item_types[payload_type] += 1
            if payload_type == "function_call":
                name = str(payload.get("name"))
                tool_names[name] += 1
                arguments = payload.get("arguments", "")
                if name in {"exec_command", "write_stdin"}:
                    try:
                        parsed = json.loads(arguments)
                    except (TypeError, json.JSONDecodeError):
                        parsed = arguments
                    commands.append((relative, line_number, compact(parsed, 2000)))
            if payload_type == "custom_tool_call":
                name = str(payload.get("name"))
                tool_names[name] += 1
                commands.append(
                    (
                        relative,
                        line_number,
                        compact(payload.get("input", ""), 4000),
                    )
                )
            if payload_type in {"message", "reasoning"}:
                role = str(payload.get("role", ""))
                messages.append(
                    (relative, line_number, role, compact(payload.get("content"), 1200))
                )
    print(f"file={relative} lines={file_lines}")

print(f"total_lines={total_lines}")
print(f"top_types={dict(sorted(top_types.items()))}")
print(f"response_item_types={dict(sorted(item_types.items()))}")
print(f"tool_names={dict(sorted(tool_names.items()))}")
print("EXECUTION_CALLS")
for relative, line_number, command in commands:
    print(f"{relative}:{line_number}: {command}")
print("MESSAGES")
for relative, line_number, role, content in messages:
    print(f"{relative}:{line_number}: role={role} content={content}")
