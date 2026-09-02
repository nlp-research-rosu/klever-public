#!/usr/bin/env python3
"""Extract human-visible claims and tool activity from an untrusted Codex JSONL trace."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


def text_content(content: object) -> str:
    if not isinstance(content, list):
        return ""
    pieces: list[str] = []
    for item in content:
        if isinstance(item, dict) and isinstance(item.get("text"), str):
            pieces.append(item["text"])
    return "\n".join(pieces)


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 64

    trace_path = Path(sys.argv[1])
    top_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    selected: list[str] = []

    with trace_path.open(encoding="utf-8") as trace_file:
        for line_number, line in enumerate(trace_file, 1):
            record = json.loads(line)
            top_type = str(record.get("type"))
            payload = record.get("payload")
            payload = payload if isinstance(payload, dict) else {}
            payload_type = str(payload.get("type"))
            top_types[top_type] += 1
            payload_types[payload_type] += 1

            if top_type == "response_item" and payload_type == "message":
                role = payload.get("role")
                if role in {"user", "assistant"}:
                    selected.append(
                        f"\nLINE {line_number} MESSAGE role={role}\n"
                        f"{text_content(payload.get('content'))}"
                    )
            elif payload_type in {
                "agent_message",
                "user_message",
                "function_call",
                "function_call_output",
                "custom_tool_call",
                "custom_tool_call_output",
                "task_complete",
            }:
                selected.append(
                    f"\nLINE {line_number} {payload_type}\n"
                    f"{json.dumps(payload, ensure_ascii=False, sort_keys=True)}"
                )

    print(f"TRACE: {trace_path}")
    print(f"TOP_TYPES: {dict(top_types)}")
    print(f"PAYLOAD_TYPES: {dict(payload_types)}")
    print("SELECTED RECORDS:")
    print("\n".join(selected))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
