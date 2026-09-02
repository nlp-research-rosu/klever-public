#!/usr/bin/env python3
"""Validate and summarize the untrusted structured generation trace."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path(
    "/candidate/codex-trace/2026/07/22/"
    "rollout-2026-07-22T06-31-35-019f8998-6dbc-7a80-84ac-a9d9f8fe86d5.jsonl"
)

outer_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
messages: list[tuple[str, str, str]] = []

with TRACE.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        record = json.loads(line)
        outer_types[str(record.get("type", "<missing>"))] += 1
        payload = record.get("payload")
        if isinstance(payload, dict):
            payload_type = str(payload.get("type", "<missing>"))
            payload_types[payload_type] += 1
            if payload_type == "agent_message":
                messages.append(
                    (
                        str(record.get("timestamp", "")),
                        str(payload.get("phase", "")),
                        str(payload.get("message", "")).replace("\n", "\\n"),
                    )
                )

print(f"valid_json_lines={sum(outer_types.values())}")
print(f"outer_types={dict(sorted(outer_types.items()))}")
print(f"payload_types={dict(sorted(payload_types.items()))}")
print(f"agent_message_count={len(messages)}")
for timestamp, phase, message in messages:
    print(f"agent_message timestamp={timestamp} phase={phase} text={message}")
