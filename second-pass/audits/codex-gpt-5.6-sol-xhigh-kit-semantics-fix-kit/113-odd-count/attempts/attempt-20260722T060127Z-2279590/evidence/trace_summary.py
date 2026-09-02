#!/usr/bin/env python3
"""Parse every JSONL record in the untrusted structured generation trace."""

from __future__ import annotations

import collections
import json
from pathlib import Path


trace = Path("/candidate/codex-trace/2026/07/21/rollout-2026-07-21T22-07-08-019f87ca-9402-73b3-bd41-12e1a19d095f.jsonl")
counts: collections.Counter[tuple[str, str]] = collections.Counter()
proof_mentions = 0
first_timestamp = None
last_timestamp = None
records = 0

with trace.open(encoding="utf-8") as handle:
    for line_number, line in enumerate(handle, 1):
        record = json.loads(line)
        records += 1
        timestamp = record.get("timestamp")
        first_timestamp = first_timestamp or timestamp
        last_timestamp = timestamp
        payload = record.get("payload")
        payload_type = payload.get("type", "-") if isinstance(payload, dict) else "-"
        counts[(record.get("type", "-"), payload_type)] += 1
        if any(token in line for token in ("kprove", "#Top", "EXPECTED FAILURE")):
            proof_mentions += 1

print(f"trace={trace}")
print(f"records={records}")
print(f"first_timestamp={first_timestamp}")
print(f"last_timestamp={last_timestamp}")
print(f"records_mentioning_proof_terms={proof_mentions}")
print("event_counts:")
for (outer, inner), count in sorted(counts.items()):
    print(f"  {outer}\t{inner}\t{count}")
