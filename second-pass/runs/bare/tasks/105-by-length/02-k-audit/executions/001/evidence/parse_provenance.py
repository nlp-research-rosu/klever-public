#!/usr/bin/env python3
"""Parse candidate provenance records as untrusted data and print a bounded summary."""

from __future__ import annotations

import collections
import json
from pathlib import Path


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


for json_path in (
    Path("/candidate/run-input.json"),
    Path("/candidate/metrics.json"),
):
    value = load_json(json_path)
    print(f"=== {json_path} ===")
    print(json.dumps(value, indent=2, sort_keys=True))

trace_path = Path(
    "/candidate/codex-trace/2026/07/22/"
    "rollout-2026-07-22T06-30-04-019f8997-0a34-7ee0-9e2f-79a643c89e58.jsonl"
)
counts: collections.Counter[str] = collections.Counter()
first_timestamp = None
last_timestamp = None
lines = 0
with trace_path.open("r", encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, start=1):
        record = json.loads(line)
        if not isinstance(record, dict):
            raise TypeError(f"line {line_number}: expected object")
        lines += 1
        counts[str(record.get("type"))] += 1
        timestamp = record.get("timestamp")
        if first_timestamp is None:
            first_timestamp = timestamp
        last_timestamp = timestamp

print(f"=== {trace_path} ===")
print(f"line_count={lines}")
print(f"first_timestamp={first_timestamp}")
print(f"last_timestamp={last_timestamp}")
print(f"top_level_types={dict(sorted(counts.items()))}")
