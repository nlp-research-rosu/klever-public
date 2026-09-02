#!/usr/bin/env python3
"""Scan the complete untrusted generation trace and print a bounded summary."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path(
    "/candidate/codex-trace/2026/07/22/"
    "rollout-2026-07-22T05-23-03-019f8959-aee9-7291-b260-1ab7e6efadce.jsonl"
)

counts: collections.Counter[str] = collections.Counter()
events: list[dict] = []
parse_errors: list[dict[str, object]] = []

with TRACE.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        try:
            item = json.loads(line)
        except json.JSONDecodeError as error:
            parse_errors.append({"line": line_number, "error": str(error)})
            continue
        counts[str(item.get("type"))] += 1
        payload = item.get("payload", {})
        if (
            item.get("type") == "event_msg"
            and payload.get("type") in {"task_started", "task_complete"}
        ):
            events.append(
                {
                    "timestamp": item.get("timestamp"),
                    "type": item.get("type"),
                    "payload": payload,
                }
            )

print("record_type_counts=" + json.dumps(counts, sort_keys=True))
print("parse_error_count=" + str(len(parse_errors)))
for error in parse_errors[:10]:
    print("PARSE_ERROR " + json.dumps(error, sort_keys=True))
for event in events:
    print("BOUNDARY_EVENT " + json.dumps(event, sort_keys=True))
