#!/usr/bin/env python3
"""Summarize every record in a Codex JSONL trace without trusting its claims."""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path


def clipped(value: object, limit: int = 1200) -> str:
    text = json.dumps(value, sort_keys=True, ensure_ascii=False)
    if len(text) <= limit:
        return text
    return text[:limit] + f"... <{len(text) - limit} chars omitted>"


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 2

    trace = Path(sys.argv[1])
    records: list[dict[str, object]] = []
    parse_errors: list[tuple[int, str]] = []
    with trace.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            try:
                record = json.loads(line)
            except json.JSONDecodeError as err:
                parse_errors.append((line_number, str(err)))
                continue
            records.append(record)

    top_types = collections.Counter(str(r.get("type")) for r in records)
    payload_types: collections.Counter[str] = collections.Counter()
    roles: collections.Counter[str] = collections.Counter()
    selected: list[str] = []

    for line_number, record in enumerate(records, 1):
        payload = record.get("payload")
        if not isinstance(payload, dict):
            continue
        nested_type = str(payload.get("type"))
        payload_types[nested_type] += 1
        if "role" in payload:
            roles[str(payload["role"])] += 1

        if nested_type in {
            "function_call",
            "function_call_output",
            "custom_tool_call",
            "custom_tool_call_output",
            "message",
            "agent_message",
        }:
            selected.append(
                f"line={line_number} timestamp={record.get('timestamp')} "
                f"record_type={record.get('type')} payload={clipped(payload)}"
            )
        elif record.get("type") == "event_msg" and nested_type in {
            "task_started",
            "task_complete",
            "turn_aborted",
            "error",
            "token_count",
        }:
            selected.append(
                f"line={line_number} timestamp={record.get('timestamp')} "
                f"record_type=event_msg payload={clipped(payload)}"
            )

    print(f"trace={trace}")
    print(f"record_count={len(records)}")
    print(f"parse_errors={parse_errors}")
    print(f"top_level_types={dict(sorted(top_types.items()))}")
    print(f"payload_types={dict(sorted(payload_types.items()))}")
    print(f"roles={dict(sorted(roles.items()))}")
    print("selected_records:")
    for item in selected:
        print(item)
    return 0 if not parse_errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
