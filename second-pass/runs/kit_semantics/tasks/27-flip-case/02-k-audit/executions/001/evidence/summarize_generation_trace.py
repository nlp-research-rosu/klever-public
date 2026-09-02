#!/usr/bin/env python3
"""Parse every structured trace event and emit a bounded chronological index."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


def flattened_text(value: object) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


trace = next(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
counts: collections.Counter[tuple[object, object]] = collections.Counter()
parsed = []
with trace.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        event = json.loads(line)
        parsed.append((line_number, event))
        counts[(event.get("type"), event.get("payload", {}).get("type"))] += 1

print(f"trace={trace}")
print(f"line_count={len(parsed)}")
print(f"sha256={hashlib.sha256(trace.read_bytes()).hexdigest()}")
print("event_counts:")
for key, count in sorted(counts.items(), key=lambda item: str(item[0])):
    print(f"  {key}: {count}")

print("chronological_visible_event_index:")
for line_number, event in parsed:
    event_type = event.get("type")
    payload = event.get("payload", {})
    payload_type = payload.get("type")
    if event_type == "response_item" and payload_type in {
        "custom_tool_call",
        "function_call",
    }:
        body = flattened_text(payload.get("input") or payload.get("arguments") or "")
        body = " ".join(body.split())
        print(
            f"  line={line_number} call={payload.get('name')} "
            f"input_sha256={hashlib.sha256(body.encode()).hexdigest()} "
            f"input_preview={body[:500]}"
        )
    elif event_type == "response_item" and payload_type in {
        "custom_tool_call_output",
        "function_call_output",
    }:
        body = flattened_text(payload.get("output") or "")
        body_one_line = " ".join(body.split())
        print(
            f"  line={line_number} output_bytes={len(body.encode())} "
            f"output_sha256={hashlib.sha256(body.encode()).hexdigest()} "
            f"output_preview={body_one_line[:300]}"
        )
    elif payload_type in {"agent_message", "user_message"}:
        body = flattened_text(payload.get("message") or "")
        body_one_line = " ".join(body.split())
        print(
            f"  line={line_number} {payload_type} "
            f"bytes={len(body.encode())} "
            f"sha256={hashlib.sha256(body.encode()).hexdigest()} "
            f"preview={body_one_line[:300]}"
        )
    elif event_type in {"session_meta", "turn_context", "world_state"}:
        body = flattened_text(payload)
        print(
            f"  line={line_number} {event_type} "
            f"payload_sha256={hashlib.sha256(body.encode()).hexdigest()}"
        )

print("TRACE_PARSE=PASS")
