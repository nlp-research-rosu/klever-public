#!/usr/bin/env python3
"""Validate every generation trace record and print an auditable event summary."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def compact(value: object, limit: int = 700) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit] + "...[truncated]"


top_counts: Counter[str] = Counter()
payload_counts: Counter[str] = Counter()
records = 0

for trace_path in sorted(TRACE_ROOT.rglob("*.jsonl")):
    print(f"TRACE_FILE {trace_path.relative_to(TRACE_ROOT)}")
    with trace_path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            records += 1
            top_type = str(record.get("type"))
            top_counts[top_type] += 1
            payload = record.get("payload", {})
            payload_type = payload.get("type") if isinstance(payload, dict) else None
            if payload_type is not None:
                payload_counts[str(payload_type)] += 1

            if top_type == "response_item" and isinstance(payload, dict):
                if payload_type == "function_call":
                    print(
                        f"line={line_number} function_call name={payload.get('name')} "
                        f"arguments={compact(payload.get('arguments', ''))}"
                    )
                elif payload_type == "function_call_output":
                    print(
                        f"line={line_number} function_output "
                        f"call_id={payload.get('call_id')} output={compact(payload.get('output', ''))}"
                    )
                elif payload_type == "message":
                    role = payload.get("role")
                    if role in {"assistant", "user"}:
                        print(
                            f"line={line_number} message role={role} "
                            f"content={compact(payload.get('content', ''))}"
                        )
            elif top_type == "event_msg" and isinstance(payload, dict):
                if payload_type in {"agent_message", "task_complete", "task_started"}:
                    print(
                        f"line={line_number} event={payload_type} payload={compact(payload)}"
                    )

print(f"records={records}")
print(f"top_level_types={dict(sorted(top_counts.items()))}")
print(f"payload_types={dict(sorted(payload_counts.items()))}")
print("TRACE_JSON_VALID=True")
