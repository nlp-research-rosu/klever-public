#!/usr/bin/env python3
"""Bounded structural summary of the untrusted generation trace."""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: untrusted_trace_summary.py TRACE.jsonl")
    path = Path(sys.argv[1])
    records = []
    with path.open(encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            try:
                records.append((number, json.loads(line)))
            except json.JSONDecodeError as exc:
                print(f"INVALID JSON line={number}: {exc}")
                return 1

    outer = collections.Counter(record.get("type") for _, record in records)
    inner = collections.Counter(
        record.get("payload", {}).get("type")
        for _, record in records
        if record.get("payload", {}).get("type")
    )
    print(f"records={len(records)}")
    print(f"outer_types={dict(sorted(outer.items(), key=lambda item: str(item[0])))}")
    print(f"payload_types={dict(sorted(inner.items(), key=lambda item: str(item[0])))}")

    print("UNTRUSTED TEXTUAL CLAIMS:")
    emitted = 0
    for number, record in records:
        payload = record.get("payload", {})
        candidate_fields = (
            payload.get("message"),
            payload.get("text"),
            payload.get("last_agent_message"),
        )
        for value in candidate_fields:
            if not isinstance(value, str):
                continue
            lowered = value.lower()
            if any(
                marker in lowered
                for marker in ("#top", "kprove", "completed successfully", "result:")
            ):
                compact = " ".join(value.split())
                print(f"line={number} type={record.get('type')}: {compact[:600]}")
                emitted += 1
                break
    print(f"claim_records_printed={emitted}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
