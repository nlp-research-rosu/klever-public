#!/usr/bin/env python3
"""Bounded structural summary of the untrusted generation JSONL trace."""

import json
from collections import Counter, deque
from pathlib import Path


trace_paths = sorted(Path("/candidate/codex-trace").rglob("*"))
trace_paths = [path for path in trace_paths if path.is_file()]
print(f"trace_file_count={len(trace_paths)}")

for path in trace_paths:
    counts: Counter[str] = Counter()
    event_counts: Counter[str] = Counter()
    invalid = []
    first = []
    last = deque(maxlen=8)
    line_count = 0
    for line_count, line in enumerate(path.open(encoding="utf-8"), start=1):
        try:
            item = json.loads(line)
        except json.JSONDecodeError as error:
            invalid.append((line_count, str(error)))
            continue
        kind = item.get("type", "<missing>")
        counts[kind] += 1
        record = {
            "line": line_count,
            "timestamp": item.get("timestamp"),
            "type": kind,
        }
        if kind == "event_msg":
            payload_kind = item.get("payload", {}).get("type", "<missing>")
            event_counts[payload_kind] += 1
            record["payload_type"] = payload_kind
        if len(first) < 8:
            first.append(record)
        last.append(record)
    print(f"path={path}")
    print(f"line_count={line_count}")
    print(f"top_level_counts={dict(sorted(counts.items()))}")
    print(f"event_counts={dict(sorted(event_counts.items()))}")
    print(f"invalid_json={invalid}")
    print(f"first={first}")
    print(f"last={list(last)}")
