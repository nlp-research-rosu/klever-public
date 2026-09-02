#!/usr/bin/env python3
"""Extract untrusted generation commands, tool results, and agent claims."""

from __future__ import annotations

import json
import pathlib
import sys


def emit(label: str, value: object) -> None:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    print(f"{label}: {text}")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 64

    path = pathlib.Path(sys.argv[1])
    counts: dict[str, int] = {}
    parsed = 0
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        item = json.loads(raw)
        parsed += 1
        event_type = item.get("type", "<missing>")
        counts[event_type] = counts.get(event_type, 0) + 1
        payload = item.get("payload", {})
        payload_type = payload.get("type")

        if event_type == "response_item" and payload_type in {
            "custom_tool_call",
            "custom_tool_call_output",
            "function_call",
            "function_call_output",
        }:
            emit(f"line {line_number} {payload_type}", payload)
        elif event_type == "response_item" and payload_type == "message":
            role = payload.get("role")
            if role == "assistant":
                emit(f"line {line_number} assistant", payload.get("content", []))
        elif event_type == "event_msg" and payload_type in {
            "agent_message",
            "task_complete",
        }:
            emit(f"line {line_number} {payload_type}", payload)

    print(f"parsed_json_lines={parsed}")
    print("event_type_counts=" + json.dumps(counts, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
