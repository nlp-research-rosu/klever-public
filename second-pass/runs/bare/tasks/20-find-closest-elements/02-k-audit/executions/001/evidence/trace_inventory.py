#!/usr/bin/env python3
"""Summarize the untrusted structured generation trace without executing it."""

from __future__ import annotations

import collections
import json
import pathlib
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 64

    path = pathlib.Path(sys.argv[1])
    outer_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    calls: list[tuple[str, str]] = []
    final_messages: list[str] = []

    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            outer = str(record.get("type"))
            outer_types[outer] += 1
            payload = record.get("payload") or {}
            inner = str(payload.get("type"))
            payload_types[f"{outer}/{inner}"] += 1
            if outer == "response_item" and inner == "function_call":
                calls.append((str(payload.get("name")), str(payload.get("arguments"))))
            if outer == "response_item" and inner == "message":
                role = payload.get("role")
                content = payload.get("content") or []
                if role == "assistant":
                    for item in content:
                        if item.get("type") in {"output_text", "text"}:
                            final_messages.append(str(item.get("text", "")))

    print(f"TRACE: {path}")
    print("OUTER_TYPES:")
    for name, count in sorted(outer_types.items()):
        print(f"  {count} {name}")
    print("PAYLOAD_TYPES:")
    for name, count in sorted(payload_types.items()):
        print(f"  {count} {name}")
    print(f"FUNCTION_CALL_COUNT: {len(calls)}")
    for index, (name, arguments) in enumerate(calls, 1):
        compact = " ".join(arguments.split())
        print(f"CALL {index}: {name} {compact[:1000]}")
    print(f"ASSISTANT_MESSAGE_COUNT: {len(final_messages)}")
    for index, message in enumerate(final_messages, 1):
        compact = " ".join(message.split())
        print(f"ASSISTANT_MESSAGE {index}: {compact[:2000]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
