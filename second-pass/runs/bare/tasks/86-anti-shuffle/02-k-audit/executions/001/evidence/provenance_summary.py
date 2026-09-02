#!/usr/bin/env python3
"""Bounded structural summary of the untrusted generation metadata and trace."""

import collections
import hashlib
import json
from pathlib import Path


def digest(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


for name in ("run-input.json", "metrics.json"):
    path = Path("/candidate") / name
    data = json.loads(path.read_text(encoding="utf-8"))
    print(f"{name}: sha256={digest(path)}")
    print(json.dumps(data, indent=2, sort_keys=True))

for name in ("codex-last.txt", "codex-output.log"):
    path = Path("/candidate") / name
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    print(
        f"{name}: sha256={digest(path)} bytes={path.stat().st_size} "
        f"lines={len(lines)}"
    )
    print("first_lines:")
    for line in lines[:8]:
        print(line[:500])
    print("last_lines:")
    for line in lines[-8:]:
        print(line[:500])

traces = sorted(Path("/candidate/codex-trace").rglob("*.jsonl"))
print(f"trace_file_count={len(traces)}")
for path in traces:
    counts = collections.Counter()
    first_timestamp = None
    last_timestamp = None
    line_count = 0
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            line_count += 1
            record = json.loads(line)
            counts[record.get("type", "<missing>")] += 1
            timestamp = record.get("timestamp")
            first_timestamp = first_timestamp or timestamp
            last_timestamp = timestamp
    print(
        f"trace={path} sha256={digest(path)} lines={line_count} "
        f"first={first_timestamp} last={last_timestamp}"
    )
    print(f"event_types={dict(sorted(counts.items()))}")
