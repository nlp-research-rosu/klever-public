#!/usr/bin/env python3
"""Validate every JSONL trace record and summarize its structured contents."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


TRACE = next(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))


def main() -> int:
    outer: Counter[str] = Counter()
    payload: Counter[str] = Counter()
    calls: Counter[str] = Counter()
    roles: Counter[str] = Counter()
    task_events: list[tuple[int, str]] = []
    lines = 0
    first_timestamp = None
    last_timestamp = None

    with TRACE.open(encoding="utf-8") as stream:
        for lines, raw in enumerate(stream, 1):
            record = json.loads(raw)
            timestamp = record["timestamp"]
            first_timestamp = first_timestamp or timestamp
            last_timestamp = timestamp
            outer[record["type"]] += 1
            item = record.get("payload", {})
            item_type = item.get("type", "<none>")
            payload[item_type] += 1
            if item_type == "function_call":
                calls[item.get("name", "<none>")] += 1
            if item_type == "message":
                roles[item.get("role", "<none>")] += 1
            if item_type in {
                "task_started",
                "task_complete",
                "task_interrupted",
                "agent_message",
            }:
                task_events.append((lines, item_type))

    print(f"path={TRACE}")
    print(f"lines={lines}")
    print(f"first_timestamp={first_timestamp}")
    print(f"last_timestamp={last_timestamp}")
    print(f"outer_types={dict(sorted(outer.items()))}")
    print(f"payload_types={dict(sorted(payload.items()))}")
    print(f"function_calls={dict(sorted(calls.items()))}")
    print(f"message_roles={dict(sorted(roles.items()))}")
    print(f"task_events={task_events}")
    print("JSON_PARSE_STATUS=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
