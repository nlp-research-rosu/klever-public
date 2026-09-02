#!/usr/bin/env python3
"""Bounded structural summary of the untrusted generation JSONL trace."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path(
    "/candidate/codex-trace/2026/07/22/"
    "rollout-2026-07-22T06-47-27-019f89a6-f12e-78d1-90ea-0d9527fcca8d.jsonl"
)


def main() -> int:
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    task_events = []
    final_messages = []
    lines = 0
    with TRACE.open(encoding="utf-8") as stream:
        for lines, raw_line in enumerate(stream, 1):
            record = json.loads(raw_line)
            top_types[record.get("type", "<missing>")] += 1
            payload = record.get("payload", {})
            if isinstance(payload, dict):
                payload_type = payload.get("type")
                if payload_type:
                    payload_types[payload_type] += 1
                if payload_type in {"task_started", "task_complete"}:
                    task_events.append(
                        {
                            "timestamp": record.get("timestamp"),
                            "type": payload_type,
                            "duration_ms": payload.get("duration_ms"),
                        }
                    )
                if (
                    payload_type == "agent_message"
                    and payload.get("phase") == "final_answer"
                ):
                    final_messages.append(payload.get("message", ""))
    print(f"trace={TRACE}")
    print(f"lines={lines}")
    print(f"top_types={json.dumps(top_types, sort_keys=True)}")
    print(f"payload_types={json.dumps(payload_types, sort_keys=True)}")
    print(f"task_events={json.dumps(task_events, sort_keys=True)}")
    print(f"final_message_count={len(final_messages)}")
    for index, message in enumerate(final_messages, 1):
        print(f"FINAL_MESSAGE_{index}:")
        print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
