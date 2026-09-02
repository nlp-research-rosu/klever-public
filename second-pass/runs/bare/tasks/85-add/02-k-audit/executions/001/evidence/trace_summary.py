#!/usr/bin/env python3
"""Validate every JSONL record and summarize untrusted generation claims."""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: trace_summary.py TRACE.jsonl", file=sys.stderr)
        return 64

    path = Path(sys.argv[1])
    records = []
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as error:
                print(f"MALFORMED line={line_number}: {error}")
                return 1

    top_types = collections.Counter(record.get("type") for record in records)
    payload_types = collections.Counter(
        record.get("payload", {}).get("type") for record in records
    )
    print(f"RECORDS: {len(records)}")
    print(f"TOP_LEVEL_TYPES: {dict(sorted(top_types.items(), key=lambda item: str(item[0])))}")
    print(f"PAYLOAD_TYPES: {dict(sorted(payload_types.items(), key=lambda item: str(item[0])))}")
    print(f"FIRST_TIMESTAMP: {records[0].get('timestamp') if records else None}")
    print(f"LAST_TIMESTAMP: {records[-1].get('timestamp') if records else None}")

    needles = ("kompile", "krun", "kprove", "differential", "py2mpy")
    matching_calls = []
    for record in records:
        payload = record.get("payload", {})
        if payload.get("type") != "custom_tool_call":
            continue
        raw_input = json.dumps(payload.get("input", ""), sort_keys=True)
        if any(needle in raw_input.lower() for needle in needles):
            matching_calls.append((payload.get("name"), raw_input))

    print(f"RELEVANT_CUSTOM_TOOL_CALLS: {len(matching_calls)}")
    for index, (name, raw_input) in enumerate(matching_calls, 1):
        bounded = raw_input[:1200].replace("\n", "\\n")
        print(f"CALL_{index}: name={name!r} input_prefix={bounded}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
