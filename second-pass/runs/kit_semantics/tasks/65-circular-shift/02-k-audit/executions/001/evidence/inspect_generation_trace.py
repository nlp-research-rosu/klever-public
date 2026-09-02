#!/usr/bin/env python3
"""Parse every generation trace record and emit a bounded chronology."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def compact(value: object, limit: int = 500) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    text = " ".join(text.split())
    if len(text) > limit:
        return text[:limit] + "...<bounded>"
    return text


def main() -> None:
    files = sorted(TRACE_ROOT.rglob("*.jsonl"))
    print(f"trace_files={len(files)}")
    event_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    total = 0

    for path in files:
        print(f"TRACE_FILE {path}")
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                total += 1
                event_type = str(record.get("type"))
                event_types[event_type] += 1
                payload = record.get("payload")
                payload_type = (
                    str(payload.get("type"))
                    if isinstance(payload, dict)
                    else type(payload).__name__
                )
                payload_types[payload_type] += 1

                detail: object | None = None
                if event_type == "response_item" and isinstance(payload, dict):
                    item_type = payload.get("type")
                    if item_type == "message":
                        detail = {
                            "role": payload.get("role"),
                            "content": payload.get("content"),
                        }
                    elif item_type == "custom_tool_call":
                        detail = {
                            "name": payload.get("name"),
                            "input": payload.get("input"),
                            "status": payload.get("status"),
                        }
                    elif item_type == "custom_tool_call_output":
                        detail = {
                            "call_id": payload.get("call_id"),
                            "output": payload.get("output"),
                        }
                    elif item_type in {"function_call", "function_call_output"}:
                        detail = payload
                elif event_type == "event_msg" and isinstance(payload, dict):
                    if payload_type in {
                        "agent_message",
                        "user_message",
                        "task_complete",
                        "turn_aborted",
                    }:
                        detail = payload

                if detail is not None:
                    print(
                        f"EVENT {line_number:04d} {record.get('timestamp')} "
                        f"{event_type}/{payload_type} {compact(detail)}"
                    )

    print(f"total_records={total}")
    print(f"event_types={dict(sorted(event_types.items()))}")
    print(f"payload_types={dict(sorted(payload_types.items()))}")
    print("TRACE_PARSE: PASS")


if __name__ == "__main__":
    main()
