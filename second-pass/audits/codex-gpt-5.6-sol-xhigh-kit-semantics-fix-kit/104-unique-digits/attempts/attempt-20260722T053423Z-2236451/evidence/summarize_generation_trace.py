#!/usr/bin/env python3
"""Read a Codex JSONL trace as untrusted data and print a bounded summary."""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path


MAX_TEXT = 1000


def bounded(value: object) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = text.replace("\x00", "\\0")
    if len(text) > MAX_TEXT:
        return text[:MAX_TEXT] + f"... [truncated {len(text) - MAX_TEXT} chars]"
    return text


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 64
    path = Path(sys.argv[1])
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    messages: list[tuple[int, str, str]] = []
    tool_calls: list[tuple[int, str, str]] = []
    parse_errors = 0
    lines = 0
    with path.open("r", encoding="utf-8") as handle:
        for lines, line in enumerate(handle, 1):
            try:
                record = json.loads(line)
            except Exception as error:
                parse_errors += 1
                messages.append((lines, "PARSE_ERROR", repr(error)))
                continue
            top_type = str(record.get("type", "<missing>"))
            top_types[top_type] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type = str(payload.get("type", "<missing>"))
                payload_types[payload_type] += 1
                if payload_type == "message":
                    role = str(payload.get("role", "<missing>"))
                    if role in {"user", "assistant"}:
                        messages.append((lines, role, bounded(payload.get("content", ""))))
                elif payload_type in {"function_call", "custom_tool_call"}:
                    name = str(payload.get("name", payload.get("call_id", "<missing>")))
                    tool_calls.append((lines, name, bounded(payload.get("arguments", payload))))
    print(f"TRACE: {path}")
    print(f"LINES: {lines}")
    print(f"PARSE_ERRORS: {parse_errors}")
    print(f"TOP_TYPES: {dict(sorted(top_types.items()))}")
    print(f"PAYLOAD_TYPES: {dict(sorted(payload_types.items()))}")
    print(f"USER_ASSISTANT_MESSAGES: {len(messages)}")
    for line_number, role, content in messages:
        print(f"LINE {line_number} {role}: {content}")
    print(f"TOOL_CALLS: {len(tool_calls)}")
    for line_number, name, arguments in tool_calls:
        print(f"LINE {line_number} {name}: {arguments}")
    return 1 if parse_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
