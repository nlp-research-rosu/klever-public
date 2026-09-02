#!/usr/bin/env python3
"""Validate and summarize every record in a Codex structured JSONL trace."""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("trace", type=Path)
    args = parser.parse_args()

    outer_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    roles: collections.Counter[str] = collections.Counter()
    tool_calls: collections.Counter[str] = collections.Counter()
    statuses: collections.Counter[str] = collections.Counter()
    first_timestamp = None
    last_timestamp = None
    records = 0

    with args.trace.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError(f"line {line_number}: record is not an object")
            records += 1
            timestamp = record.get("timestamp")
            first_timestamp = first_timestamp or timestamp
            last_timestamp = timestamp
            outer_types[str(record.get("type"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
                if "role" in payload:
                    roles[str(payload["role"])] += 1
                name = payload.get("name")
                if payload.get("type") in {"function_call", "custom_tool_call"}:
                    tool_calls[str(name)] += 1
                status = payload.get("status")
                if status is not None:
                    statuses[str(status)] += 1

    print(f"records={records}")
    print(f"first_timestamp={first_timestamp}")
    print(f"last_timestamp={last_timestamp}")
    print(f"outer_types={dict(sorted(outer_types.items()))}")
    print(f"payload_types={dict(sorted(payload_types.items()))}")
    print(f"roles={dict(sorted(roles.items()))}")
    print(f"tool_calls={dict(sorted(tool_calls.items()))}")
    print(f"statuses={dict(sorted(statuses.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
