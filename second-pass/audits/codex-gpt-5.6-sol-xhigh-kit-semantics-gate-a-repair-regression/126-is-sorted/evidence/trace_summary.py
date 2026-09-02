#!/usr/bin/env python3
"""Bounded structural summary of the untrusted generation JSONL trace."""

from __future__ import annotations

import collections
import json
import pathlib
import sys


def main() -> int:
    trace = pathlib.Path(sys.argv[1])
    type_counts: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    commands: list[str] = []
    final_messages: list[str] = []

    with trace.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            record = json.loads(line)
            record_type = str(record.get("type", "<none>"))
            type_counts[record_type] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type = str(payload.get("type", "<none>"))
                payload_types[payload_type] += 1
                if payload_type == "function_call":
                    name = payload.get("name", "<none>")
                    arguments = payload.get("arguments", "")
                    commands.append(
                        f"line {line_number}: {name}: {arguments[:500]}"
                    )
                if payload_type == "message" and payload.get("role") == "assistant":
                    text_parts = []
                    for item in payload.get("content", []):
                        if isinstance(item, dict) and "text" in item:
                            text_parts.append(str(item["text"]))
                    if text_parts:
                        final_messages.append(
                            f"line {line_number}: {' '.join(text_parts)[:1000]}"
                        )

    print(f"trace={trace}")
    print(f"lines={sum(type_counts.values())}")
    print("top-level types:")
    for key, count in sorted(type_counts.items()):
        print(f"  {key}: {count}")
    print("payload types:")
    for key, count in sorted(payload_types.items()):
        print(f"  {key}: {count}")
    print(f"function calls={len(commands)}")
    for command in commands:
        print(command)
    print(f"assistant messages={len(final_messages)}")
    for message in final_messages:
        print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
