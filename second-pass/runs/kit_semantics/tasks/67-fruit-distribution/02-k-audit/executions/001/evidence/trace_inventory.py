#!/usr/bin/env python3
"""Inventory every structured generation trace event and tool call."""

from __future__ import annotations

import collections
import json
from pathlib import Path


trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
if not trace_files:
    raise SystemExit("no structured trace files")

for trace in trace_files:
    outer = collections.Counter()
    inner = collections.Counter()
    roles = collections.Counter()
    calls: list[tuple[int, str, str, str]] = []
    line_count = 0
    for line_count, line in enumerate(trace.read_text().splitlines(), 1):
        record = json.loads(line)
        outer[record.get("type")] += 1
        payload = record.get("payload", {})
        payload_type = payload.get("type")
        inner[payload_type] += 1
        if payload_type == "message":
            roles[payload.get("role")] += 1
        if payload_type in {"function_call", "custom_tool_call"}:
            rendered = payload.get("arguments") or payload.get("input") or ""
            calls.append(
                (
                    line_count,
                    payload_type,
                    str(payload.get("name")),
                    str(rendered).replace("\n", "\\n"),
                )
            )
    print(f"TRACE {trace} lines={line_count}")
    print(f"OUTER_TYPES {dict(sorted(outer.items(), key=lambda item: str(item[0])))}")
    print(f"PAYLOAD_TYPES {dict(sorted(inner.items(), key=lambda item: str(item[0])))}")
    print(f"MESSAGE_ROLES {dict(sorted(roles.items(), key=lambda item: str(item[0])))}")
    print(f"TOOL_CALLS count={len(calls)}")
    for line_number, payload_type, name, rendered in calls:
        print(f"line={line_number} type={payload_type} name={name} input={rendered}")
print("TRACE_INVENTORY=PASS")
