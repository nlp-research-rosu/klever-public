#!/usr/bin/env python3
"""Validate and summarize every JSONL record in the untrusted generation trace."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 64

    path = Path(sys.argv[1])
    outer_types: Counter[str] = Counter()
    event_types: Counter[str] = Counter()
    role_types: Counter[str] = Counter()
    command_count = 0
    final_messages: list[str] = []

    with path.open("r", encoding="utf-8") as trace:
        for line_number, line in enumerate(trace, 1):
            record = json.loads(line)
            outer_type = str(record.get("type", "<missing>"))
            outer_types[outer_type] += 1
            payload = record.get("payload", {})
            if isinstance(payload, dict):
                event_types[str(payload.get("type", "<missing>"))] += 1
                role = payload.get("role")
                if role is not None:
                    role_types[str(role)] += 1
                if payload.get("type") in {"function_call", "custom_tool_call"}:
                    command_count += 1
                if payload.get("phase") == "final_answer":
                    content = payload.get("content", [])
                    if isinstance(content, list):
                        for item in content:
                            if isinstance(item, dict) and "text" in item:
                                final_messages.append(str(item["text"]))

    print(f"path={path}")
    print(f"records={sum(outer_types.values())}")
    print(f"outer_types={dict(sorted(outer_types.items()))}")
    print(f"payload_types={dict(sorted(event_types.items()))}")
    print(f"roles={dict(sorted(role_types.items()))}")
    print(f"tool_call_records={command_count}")
    print(f"final_message_count={len(final_messages)}")
    for index, message in enumerate(final_messages, 1):
        print(f"final_message_{index}={message!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
