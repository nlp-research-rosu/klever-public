#!/usr/bin/env python3
"""Parse every structured trace record and summarize its untrusted claims."""

from __future__ import annotations

import collections
import json
from pathlib import Path


def main() -> int:
    root = Path("/generation-evidence/codex-trace")
    files = sorted(root.rglob("*.jsonl"))
    print(f"trace_file_count={len(files)}")
    invalid = 0
    record_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    tool_names: collections.Counter[str] = collections.Counter()
    commands: list[str] = []
    assistant_messages: list[str] = []
    for path in files:
        line_count = 0
        print(f"TRACE_FILE {path}")
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                line_count += 1
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as err:
                    invalid += 1
                    print(f"INVALID_JSON line={line_number} error={err}")
                    continue
                record_types[str(record.get("type"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type"))] += 1
                    name = payload.get("name")
                    if isinstance(name, str):
                        tool_names[name] += 1
                    if payload.get("type") == "function_call":
                        args = payload.get("arguments")
                        if isinstance(args, str):
                            try:
                                parsed = json.loads(args)
                            except json.JSONDecodeError:
                                parsed = {}
                            command = parsed.get("cmd") or parsed.get("command")
                            if isinstance(command, str):
                                commands.append(command)
                    if payload.get("type") == "message" and payload.get("role") == "assistant":
                        content = payload.get("content")
                        if isinstance(content, list):
                            texts = [
                                part.get("text", "")
                                for part in content
                                if isinstance(part, dict) and isinstance(part.get("text"), str)
                            ]
                            if texts:
                                assistant_messages.append("\n".join(texts))
        print(f"trace_line_count={line_count}")
    print(f"invalid_json_count={invalid}")
    print(f"record_types={dict(record_types)}")
    print(f"payload_types={dict(payload_types)}")
    print(f"tool_names={dict(tool_names)}")
    print(f"captured_command_count={len(commands)}")
    for index, command in enumerate(commands, 1):
        compact = " ".join(command.split())
        print(f"COMMAND[{index}] {compact[:1200]}")
    print(f"assistant_message_count={len(assistant_messages)}")
    for index, message in enumerate(assistant_messages, 1):
        compact = " ".join(message.split())
        print(f"ASSISTANT[{index}] {compact[:1600]}")
    return 1 if invalid else 0


if __name__ == "__main__":
    raise SystemExit(main())
