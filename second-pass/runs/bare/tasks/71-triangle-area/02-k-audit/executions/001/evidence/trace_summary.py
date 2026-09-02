#!/usr/bin/env python3
"""Read every structured generation-trace record and emit a bounded summary."""

import json
from collections import Counter
from pathlib import Path

path = Path(
    "/candidate/codex-trace/2026/07/22/"
    "rollout-2026-07-22T05-34-08-019f8963-d311-7600-88de-0356008e00ef.jsonl"
)
top_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
roles: Counter[str] = Counter()
records = 0
last_task_complete = None

with path.open() as stream:
    for line_number, line in enumerate(stream, 1):
        record = json.loads(line)
        records += 1
        top_types[str(record.get("type"))] += 1
        payload = record.get("payload")
        if isinstance(payload, dict):
            payload_types[str(payload.get("type"))] += 1
            if "role" in payload:
                roles[str(payload["role"])] += 1
            if payload.get("type") == "task_complete":
                last_task_complete = {
                    "line": line_number,
                    "duration_ms": payload.get("duration_ms"),
                    "last_agent_message": payload.get("last_agent_message"),
                }

print(f"records={records}")
print(f"top_types={dict(sorted(top_types.items()))}")
print(f"payload_types={dict(sorted(payload_types.items()))}")
print(f"roles={dict(sorted(roles.items()))}")
print(f"task_complete={last_task_complete!r}")
