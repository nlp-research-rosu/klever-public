#!/usr/bin/env python3
"""Parse every structured generation-trace record and summarize tool activity."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/29/"
    "rollout-2026-07-29T07-22-04-019fadd3-27b0-7ad3-ba1b-0db75f23c44f.jsonl"
)


def main() -> int:
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    call_names: collections.Counter[str] = collections.Counter()
    session_ids: set[str] = set()
    call_records: list[dict[str, object]] = []

    with TRACE.open() as trace:
        for line_number, line in enumerate(trace, 1):
            record = json.loads(line)
            top_types[record.get("type", "<none>")] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type = payload.get("type", "<none>")
                payload_types[payload_type] += 1
                session_id = payload.get("session_id")
                if isinstance(session_id, str):
                    session_ids.add(session_id)
                if payload_type in {"function_call", "custom_tool_call"}:
                    name = str(payload.get("name", "<none>"))
                    call_names[name] += 1
                    arguments = payload.get("arguments", payload.get("input", ""))
                    call_records.append(
                        {
                            "line": line_number,
                            "name": name,
                            "arguments": arguments,
                        }
                    )

    summary = {
        "records": sum(top_types.values()),
        "top_level_types": dict(sorted(top_types.items())),
        "payload_types": dict(sorted(payload_types.items())),
        "call_names": dict(sorted(call_names.items())),
        "session_ids": sorted(session_ids),
        "function_calls": len(call_records),
    }
    print("SUMMARY " + json.dumps(summary, sort_keys=True))
    for call_record in call_records:
        print("CALL " + json.dumps(call_record, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
