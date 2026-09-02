#!/usr/bin/env python3
"""Read every structured-trace record and summarize its untrusted claims."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


paths = list(Path("/candidate/codex-trace").rglob("*.jsonl"))
print(f"trace_files={len(paths)}")
for path in paths:
    top_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    calls: list[tuple[int, str, str]] = []
    final_messages: list[tuple[int, str]] = []
    records = 0

    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            record = json.loads(line)
            records += 1
            top_types[str(record.get("type"))] += 1
            payload = record.get("payload") or {}
            payload_type = str(payload.get("type"))
            payload_types[payload_type] += 1
            if payload_type in {"function_call", "custom_tool_call"}:
                raw = payload.get("arguments") or payload.get("input") or ""
                calls.append((line_number, str(payload.get("name")), str(raw)))
            if payload_type in {"agent_message", "task_complete"}:
                text = payload.get("message") or payload.get("last_agent_message") or ""
                final_messages.append((line_number, str(text)))

    print(f"path={path}")
    print(f"records_read={records}")
    print(f"top_types={dict(top_types)}")
    print(f"payload_types={dict(payload_types)}")
    print(f"tool_calls={len(calls)}")
    for line_number, name, raw in calls:
        one_line = " ".join(raw.split())
        print(f"call_line={line_number} name={name} text={one_line[:1000]}")
    print(f"agent_status_messages={len(final_messages)}")
    for line_number, message in final_messages:
        one_line = " ".join(message.split())
        print(f"message_line={line_number} text={one_line[:1200]}")
