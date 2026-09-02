#!/usr/bin/env python3
"""Summarize the untrusted structured generation trace without executing it."""

from __future__ import annotations

import collections
import json
import pathlib
import sys


def clipped(value: object, limit: int = 2500) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n...[clipped {len(text) - limit} characters]"


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 64

    path = pathlib.Path(sys.argv[1])
    outer_counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    records: list[dict[str, object]] = []

    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            records.append(record)
            outer_type = str(record.get("type"))
            outer_counts[outer_type] += 1
            payload = record.get("payload")
            if isinstance(payload, dict) and "type" in payload:
                payload_counts[f"{outer_type}/{payload['type']}"] += 1

    print(f"TRACE: {path}")
    print(f"VALID_JSONL_RECORDS: {len(records)}")
    print("OUTER_TYPE_COUNTS:")
    for key, value in sorted(outer_counts.items()):
        print(f"  {key}: {value}")
    print("PAYLOAD_TYPE_COUNTS:")
    for key, value in sorted(payload_counts.items()):
        print(f"  {key}: {value}")

    print("EXECUTED_COMMANDS_AND_REPORTED_OUTPUTS:")
    pending: dict[str, str] = {}
    for record in records:
        payload = record.get("payload")
        if not isinstance(payload, dict):
            continue
        if payload.get("type") == "custom_tool_call" and payload.get("name") == "exec":
            call_id = str(payload.get("call_id"))
            command = clipped(payload.get("input", ""), 4000)
            pending[call_id] = command
            print(f"  CALL {call_id}: {command}")
        elif payload.get("type") == "custom_tool_call_output":
            call_id = str(payload.get("call_id"))
            if call_id in pending:
                print(f"  OUTPUT {call_id}: {clipped(payload.get('output', ''), 5000)}")

    print("FINAL_AGENT_MESSAGES:")
    for record in records:
        payload = record.get("payload")
        if (
            isinstance(payload, dict)
            and payload.get("type") == "agent_message"
            and payload.get("phase") == "final_answer"
        ):
            print(clipped(payload.get("message", ""), 5000))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
