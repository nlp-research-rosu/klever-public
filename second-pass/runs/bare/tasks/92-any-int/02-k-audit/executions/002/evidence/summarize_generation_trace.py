#!/usr/bin/env python3
"""Parse every structured trace record and summarize observable generation actions."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def compact(value: object, limit: int = 1400) -> str:
    text = json.dumps(value, sort_keys=True, ensure_ascii=False)
    if len(text) <= limit:
        return text
    return text[:limit] + f"... <{len(text) - limit} chars omitted>"


def main() -> None:
    files = sorted(TRACE_ROOT.rglob("*"))
    trace_files = [path for path in files if path.is_file()]
    print(f"trace_files={len(trace_files)}")
    type_counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    total_lines = 0
    first_timestamp = None
    last_timestamp = None
    for path in trace_files:
        print(f"FILE {path.relative_to(TRACE_ROOT)} size={path.stat().st_size}")
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                total_lines += 1
                record = json.loads(line)
                timestamp = record.get("timestamp")
                first_timestamp = first_timestamp or timestamp
                last_timestamp = timestamp
                event_type = record.get("type", "<missing>")
                type_counts[event_type] += 1
                payload = record.get("payload", {})
                payload_type = payload.get("type") if isinstance(payload, dict) else None
                if payload_type:
                    payload_counts[payload_type] += 1

                if event_type == "response_item" and payload_type in {
                    "custom_tool_call",
                    "function_call",
                }:
                    print(
                        f"TOOL_CALL line={line_number} name={payload.get('name')} "
                        f"input={compact(payload.get('input'))}"
                    )
                elif event_type == "response_item" and payload_type in {
                    "custom_tool_call_output",
                    "function_call_output",
                }:
                    print(
                        f"TOOL_OUTPUT line={line_number} call_id={payload.get('call_id')} "
                        f"output={compact(payload.get('output'))}"
                    )
                elif event_type == "event_msg" and payload_type in {
                    "agent_message",
                    "task_complete",
                    "turn_aborted",
                }:
                    print(f"EVENT line={line_number} {compact(payload)}")
                elif event_type == "response_item" and payload_type == "message":
                    role = payload.get("role")
                    if role in {"assistant", "user"}:
                        print(
                            f"MESSAGE line={line_number} role={role} "
                            f"content={compact(payload.get('content'))}"
                        )
    print(f"total_lines={total_lines}")
    print(f"first_timestamp={first_timestamp}")
    print(f"last_timestamp={last_timestamp}")
    print(f"record_type_counts={dict(sorted(type_counts.items()))}")
    print(f"payload_type_counts={dict(sorted(payload_counts.items()))}")


if __name__ == "__main__":
    main()
