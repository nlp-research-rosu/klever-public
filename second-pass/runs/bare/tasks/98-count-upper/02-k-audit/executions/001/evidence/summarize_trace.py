#!/usr/bin/env python3
"""Parse every JSONL trace record and emit a bounded audit-oriented summary."""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path


def compact(value: object, limit: int = 1200) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    if len(text) <= limit:
        return text
    return text[:limit] + f"... <{len(text) - limit} chars omitted>"


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 64

    path = Path(sys.argv[1])
    top_counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    selected: list[tuple[int, str, object]] = []

    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            top_type = str(record.get("type", "<missing>"))
            payload = record.get("payload")
            payload_type = (
                str(payload.get("type", "<none>"))
                if isinstance(payload, dict)
                else "<non-object>"
            )
            top_counts[top_type] += 1
            payload_counts[f"{top_type}|{payload_type}"] += 1

            if payload_type in {
                "message",
                "agent_message",
                "function_call",
                "function_call_output",
                "task_started",
                "turn_aborted",
            }:
                selected.append((line_number, payload_type, payload))

    print(f"parsed_json_lines={sum(top_counts.values())}")
    print("top_level_counts:")
    for key, value in sorted(top_counts.items()):
        print(f"  {key}={value}")
    print("top_and_payload_counts:")
    for key, value in sorted(payload_counts.items()):
        print(f"  {key}={value}")
    print("selected_events:")
    for line_number, payload_type, payload in selected:
        print(f"  line={line_number} payload_type={payload_type} {compact(payload)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
