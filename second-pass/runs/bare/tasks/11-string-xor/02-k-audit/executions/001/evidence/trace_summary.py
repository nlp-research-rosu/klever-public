#!/usr/bin/env python3
"""Read every structured trace record and report bounded provenance facts."""

from __future__ import annotations

import collections
import json
from pathlib import Path


counts: collections.Counter[str] = collections.Counter()
records = 0
malformed = 0
final_messages: list[str] = []
for path in sorted(Path("/candidate/codex-trace").rglob("*.jsonl")):
    with path.open(encoding="utf-8") as trace:
        for line in trace:
            records += 1
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                malformed += 1
                continue
            counts[str(item.get("type", "<none>"))] += 1
            payload = item.get("payload")
            if (
                isinstance(payload, dict)
                and payload.get("type") == "agent_message"
                and payload.get("phase") == "final_answer"
            ):
                final_messages.append(str(payload.get("message", "")))

print(f"records: {records}")
print(f"malformed records: {malformed}")
for kind, count in sorted(counts.items()):
    print(f"type {kind}: {count}")
print(f"final agent messages: {len(final_messages)}")
for message in final_messages:
    print("final message sha256 omitted; bounded suffix follows:")
    print(message[-1000:])
