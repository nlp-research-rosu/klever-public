#!/usr/bin/env python3
"""Parse every structured generation-trace event into a bounded audit table."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")
OUTPUT = Path("/audit-output/evidence/01-generation-trace-summary.tsv")


def flatten(value) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, sort_keys=True, ensure_ascii=False)


rows = []
outer_counts = Counter()
inner_counts = Counter()
for trace_file in sorted(TRACE_ROOT.rglob("*")):
    if not trace_file.is_file():
        continue
    with trace_file.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            event = json.loads(line)
            outer = event.get("type", "")
            payload = event.get("payload", {})
            inner = payload.get("type", "") if isinstance(payload, dict) else ""
            outer_counts[outer] += 1
            inner_counts[(outer, inner)] += 1
            selected = {}
            if isinstance(payload, dict):
                for key in (
                    "role",
                    "name",
                    "arguments",
                    "output",
                    "message",
                    "content",
                    "summary",
                    "status",
                    "call_id",
                ):
                    if key in payload:
                        selected[key] = payload[key]
            readable = flatten(selected)
            rows.append(
                {
                    "file": trace_file.relative_to(TRACE_ROOT).as_posix(),
                    "line": line_number,
                    "timestamp": event.get("timestamp", ""),
                    "outer_type": outer,
                    "inner_type": inner,
                    "readable_sha256": hashlib.sha256(readable.encode()).hexdigest(),
                    "readable_length": len(readable),
                    "preview": readable[:1200].replace("\n", "\\n"),
                }
            )

with OUTPUT.open("w", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, fieldnames=rows[0].keys(), delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)

print(f"PARSED_EVENTS={len(rows)}")
print("OUTER_COUNTS=" + json.dumps(outer_counts, sort_keys=True))
print(
    "INNER_COUNTS="
    + json.dumps(
        {f"{outer}/{inner}": count for (outer, inner), count in inner_counts.items()},
        sort_keys=True,
    )
)
print(f"OUTPUT={OUTPUT}")
