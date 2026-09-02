#!/usr/bin/env python3
"""Read every untrusted generation-trace record and print a bounded audit index."""

from __future__ import annotations

import collections
import json
import pathlib
import sys


def compact(value: object, limit: int = 1200) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[: limit // 2] + " ...<bounded>... " + text[-limit // 2 :]


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 64

    path = pathlib.Path(sys.argv[1])
    outer_counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    significant: list[str] = []
    total = 0

    with path.open(encoding="utf-8") as trace:
        for line_number, line in enumerate(trace, 1):
            total += 1
            record = json.loads(line)
            outer_type = str(record.get("type", "<missing>"))
            outer_counts[outer_type] += 1
            payload = record.get("payload")
            payload_type = (
                str(payload.get("type", "<missing>"))
                if isinstance(payload, dict)
                else type(payload).__name__
            )
            payload_counts[f"{outer_type}/{payload_type}"] += 1

            if outer_type == "session_meta" and isinstance(payload, dict):
                keys = (
                    "session_id",
                    "timestamp",
                    "cwd",
                    "cli_version",
                    "model_provider",
                )
                significant.append(
                    f"{line_number}: session_meta "
                    + compact({key: payload.get(key) for key in keys})
                )
            elif outer_type == "event_msg" and isinstance(payload, dict):
                if payload_type in {
                    "task_started",
                    "task_complete",
                    "agent_message",
                    "turn_aborted",
                }:
                    significant.append(
                        f"{line_number}: event_msg/{payload_type} {compact(payload)}"
                    )
            elif outer_type == "response_item" and isinstance(payload, dict):
                if payload_type in {
                    "function_call",
                    "function_call_output",
                    "message",
                }:
                    significant.append(
                        f"{line_number}: response_item/{payload_type} "
                        f"{compact(payload)}"
                    )

    print(f"TRACE: {path}")
    print(f"RECORDS_PARSED: {total}")
    print("OUTER_TYPE_COUNTS:")
    for key, count in sorted(outer_counts.items()):
        print(f"  {key}: {count}")
    print("PAYLOAD_TYPE_COUNTS:")
    for key, count in sorted(payload_counts.items()):
        print(f"  {key}: {count}")
    print("SIGNIFICANT_RECORD_INDEX:")
    for item in significant:
        print(item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
