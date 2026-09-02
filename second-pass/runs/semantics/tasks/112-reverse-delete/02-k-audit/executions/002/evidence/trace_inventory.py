#!/usr/bin/env python3
"""Parse every JSONL record and inventory the untrusted generation trace."""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 64

    path = Path(sys.argv[1])
    top: collections.Counter[str] = collections.Counter()
    payloads: collections.Counter[tuple[str, str]] = collections.Counter()
    records = []

    with path.open(encoding="utf-8") as stream:
        for line_no, line in enumerate(stream, 1):
            record = json.loads(line)
            records.append((line_no, record))
            outer = str(record.get("type"))
            payload = record.get("payload") or {}
            inner = str(payload.get("type"))
            top[outer] += 1
            payloads[(outer, inner)] += 1

    print(f"TRACE: {path}")
    print(f"PARSED_JSONL_RECORDS: {len(records)}")
    print(f"TOP_LEVEL_COUNTS: {dict(sorted(top.items()))}")
    print(
        "PAYLOAD_COUNTS: "
        + repr({str(key): value for key, value in sorted(payloads.items())})
    )

    for line_no, record in records:
        payload = record.get("payload") or {}
        kind = record.get("type")
        inner = payload.get("type")
        if kind == "response_item" and inner in {
            "message",
            "function_call",
            "function_call_output",
            "custom_tool_call",
            "custom_tool_call_output",
        }:
            print(f"\nLINE {line_no}: {kind}/{inner}")
            print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        elif kind == "event_msg" and inner in {
            "task_started",
            "user_message",
            "agent_message",
            "patch_apply_end",
            "task_complete",
        }:
            print(f"\nLINE {line_no}: {kind}/{inner}")
            print(json.dumps(payload, ensure_ascii=False, sort_keys=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
