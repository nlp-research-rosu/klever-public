#!/usr/bin/env python3
"""Inspect every JSONL generation-trace record and summarize visible actions."""

from __future__ import annotations

import collections
import glob
import json


def main() -> None:
    outer: collections.Counter[str] = collections.Counter()
    inner: collections.Counter[tuple[str, str | None]] = collections.Counter()
    records = 0
    for filename in sorted(glob.glob("/generation-evidence/codex-trace/**/*.jsonl", recursive=True)):
        print(f"TRACE_FILE {filename}")
        with open(filename, encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                records += 1
                record_type = record.get("type")
                payload = record.get("payload", {})
                payload_type = payload.get("type")
                outer[record_type] += 1
                inner[(record_type, payload_type)] += 1
                if record_type == "response_item" and payload_type == "function_call":
                    print(
                        f"LINE {line_number} FUNCTION {payload.get('name')} "
                        f"{payload.get('arguments')}"
                    )
                elif record_type == "response_item" and payload_type == "custom_tool_call":
                    print(
                        f"LINE {line_number} CUSTOM {payload.get('name')} "
                        f"{payload.get('input')}"
                    )
                elif (
                    record_type == "response_item"
                    and payload_type == "message"
                    and payload.get("role") == "assistant"
                ):
                    text = "\n".join(
                        part.get("text", "") for part in payload.get("content", [])
                    )
                    print(f"LINE {line_number} ASSISTANT {text}")
                elif record_type == "event_msg" and payload_type in {
                    "task_started",
                    "task_complete",
                }:
                    print(f"LINE {line_number} EVENT {payload_type} {payload}")
    print(f"PARSED_RECORDS {records}")
    print("OUTER_COUNTS", dict(sorted(outer.items())))
    print(
        "INNER_COUNTS",
        {f"{outer_type}/{inner_type}": count for (outer_type, inner_type), count in sorted(inner.items())},
    )


if __name__ == "__main__":
    main()
