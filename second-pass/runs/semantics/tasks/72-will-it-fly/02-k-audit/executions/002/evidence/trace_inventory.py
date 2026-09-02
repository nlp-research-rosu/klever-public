#!/usr/bin/env python3
"""Parse every structured generation-trace event and summarize its actions."""

from __future__ import annotations

import collections
import json
from pathlib import Path


trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
if not trace_files:
    raise SystemExit("no trace JSONL found")

outer: collections.Counter[str] = collections.Counter()
inner: collections.Counter[str] = collections.Counter()
calls: list[tuple[str, int, str, object]] = []
line_count = 0

for path in trace_files:
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            line_count += 1
            record = json.loads(line)
            outer[str(record.get("type"))] += 1
            payload = record.get("payload", {})
            inner[str(payload.get("type"))] += 1
            if payload.get("type") in {"function_call", "custom_tool_call"}:
                calls.append(
                    (
                        path.relative_to("/generation-evidence/codex-trace").as_posix(),
                        line_number,
                        str(payload.get("name")),
                        payload.get("arguments", payload.get("input")),
                    )
                )

print(f"trace_files={len(trace_files)}")
print(f"trace_lines={line_count}")
print(f"outer_types={dict(sorted(outer.items()))}")
print(f"payload_types={dict(sorted(inner.items()))}")
print(f"tool_calls={len(calls)}")
for relative, line_number, name, arguments in calls:
    compact = json.dumps(arguments, sort_keys=True, ensure_ascii=False)
    print(f"{relative}:{line_number}\t{name}\t{compact}")
