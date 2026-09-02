#!/usr/bin/env python3
"""Produce a bounded, complete event inventory of the untrusted JSONL trace."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")
MAX_FIELD = 6000


def bounded(value: object) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    if len(text) <= MAX_FIELD:
        return text
    return text[:MAX_FIELD] + f"\n...[truncated {len(text) - MAX_FIELD} characters]"


def main() -> int:
    top_counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    bad_lines: list[tuple[str, int, str]] = []
    records: list[tuple[Path, int, dict[str, object]]] = []

    for path in sorted(TRACE_ROOT.rglob("*.jsonl")):
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                try:
                    record = json.loads(line)
                except Exception as error:  # evidence parser, report rather than hide
                    bad_lines.append((str(path), line_number, repr(error)))
                    continue
                records.append((path, line_number, record))
                top_counts[str(record.get("type"))] += 1
                payload = record.get("payload", {})
                if isinstance(payload, dict):
                    payload_counts[
                        f"{record.get('type')}:{payload.get('type')}"
                    ] += 1

    print(f"trace_files={len(list(TRACE_ROOT.rglob('*.jsonl')))}")
    print(f"records={len(records)}")
    print(f"json_parse_failures={bad_lines}")
    print(f"top_type_counts={dict(sorted(top_counts.items()))}")
    print(f"payload_type_counts={dict(sorted(payload_counts.items()))}")

    print("ACTION_AND_RESULT_INVENTORY_BEGIN")
    for path, line_number, record in records:
        payload = record.get("payload", {})
        if not isinstance(payload, dict):
            continue
        top_type = record.get("type")
        payload_type = payload.get("type")
        relative = path.relative_to(TRACE_ROOT)
        prefix = (
            f"TRACE {relative}:{line_number} timestamp={record.get('timestamp')} "
            f"type={top_type}/{payload_type}"
        )
        if top_type == "response_item" and payload_type == "custom_tool_call":
            print(prefix)
            print(f"name={payload.get('name')} call_id={payload.get('call_id')}")
            print(bounded(payload.get("input", "")))
        elif top_type == "response_item" and payload_type == "custom_tool_call_output":
            print(prefix)
            print(f"call_id={payload.get('call_id')}")
            print(bounded(payload.get("output", "")))
        elif top_type == "event_msg" and payload_type in {
            "agent_message",
            "task_started",
            "task_complete",
            "turn_aborted",
        }:
            print(prefix)
            print(bounded(payload))
        elif top_type == "response_item" and payload_type == "message":
            role = payload.get("role")
            if role in {"user", "assistant"}:
                print(prefix)
                print(f"role={role}")
                print(bounded(payload.get("content", "")))
    print("ACTION_AND_RESULT_INVENTORY_END")

    return 1 if bad_lines else 0


if __name__ == "__main__":
    raise SystemExit(main())
