#!/usr/bin/env python3
"""Stream and summarize the untrusted structured generation trace."""

from __future__ import annotations

import collections
import json
from pathlib import Path


paths = sorted(Path("/candidate/codex-trace").rglob("*.jsonl"))
if not paths:
    raise SystemExit("no structured trace found")

top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
records = 0
invalid = 0
last_agent_message = None

for path in paths:
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            records += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                invalid += 1
                continue
            top_types[str(record.get("type"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
                if record.get("type") == "event_msg":
                    if payload.get("type") == "agent_message":
                        last_agent_message = payload.get("message")

print(
    json.dumps(
        {
            "files": [str(path) for path in paths],
            "records_read": records,
            "invalid_json_records": invalid,
            "top_level_types": dict(sorted(top_types.items())),
            "payload_types": dict(sorted(payload_types.items())),
            "last_agent_message_claim": last_agent_message,
        },
        indent=2,
        sort_keys=True,
    )
)
