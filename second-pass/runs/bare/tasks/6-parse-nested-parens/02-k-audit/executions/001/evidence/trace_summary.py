#!/usr/bin/env python3
"""Parse every record in the untrusted structured generation trace."""

from __future__ import annotations

import collections
import glob
import json
from pathlib import Path


paths = sorted(
    Path(path)
    for path in glob.glob("/candidate/codex-trace/2026/07/22/*.jsonl")
)
record_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
tool_names: collections.Counter[str] = collections.Counter()
bad_json: list[tuple[str, int, str]] = []
claims: list[dict[str, object]] = []

for path in paths:
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            try:
                record = json.loads(line)
            except Exception as err:
                bad_json.append((str(path), line_number, str(err)))
                continue
            record_type = str(record.get("type", "<none>"))
            record_types[record_type] += 1
            payload = record.get("payload")
            if not isinstance(payload, dict):
                continue
            payload_type = str(payload.get("type", "<none>"))
            payload_types[payload_type] += 1
            if payload_type == "custom_tool_call":
                tool_names[str(payload.get("name", "<none>"))] += 1
            if payload_type == "agent_message":
                message = str(payload.get("message", ""))
                if any(
                    marker in message
                    for marker in ("#Top", "proof", "mutation", "RESULT:")
                ):
                    claims.append(
                        {
                            "path": str(path),
                            "line": line_number,
                            "phase": payload.get("phase"),
                            "message": message,
                        }
                    )

print(
    json.dumps(
        {
            "files": [str(path) for path in paths],
            "record_types": dict(record_types),
            "payload_types": dict(payload_types),
            "tool_names": dict(tool_names),
            "bad_json": bad_json,
        },
        sort_keys=True,
    )
)
for claim in claims:
    print(json.dumps(claim, sort_keys=True))
