#!/usr/bin/env python3
"""Parse every structured generation event and emit a bounded audit summary."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T03-07-44-019f8e04-2636-7460-8e66-afeeb19f5cff.jsonl"
)


def bounded(value: object, limit: int = 500) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[:350] + " ... " + text[-120:]


counts: Counter[tuple[object, object]] = Counter()
session_ids: set[str] = set()
lines = 0
for lines, raw_line in enumerate(TRACE.open(encoding="utf-8"), start=1):
    event = json.loads(raw_line)
    event_type = event.get("type")
    payload = event.get("payload")
    payload_type = payload.get("type") if isinstance(payload, dict) else None
    counts[(event_type, payload_type)] += 1
    if isinstance(payload, dict):
        session = payload.get("session_id")
        if session:
            session_ids.add(str(session))
    if payload_type in {
        "function_call",
        "function_call_output",
        "custom_tool_call",
        "custom_tool_call_output",
        "message",
    }:
        if payload_type in {"function_call", "custom_tool_call"}:
            detail = {
                key: payload.get(key)
                for key in ("name", "call_id", "arguments", "input")
                if key in payload
            }
        elif payload_type in {"function_call_output", "custom_tool_call_output"}:
            detail = {
                key: payload.get(key)
                for key in ("call_id", "output")
                if key in payload
            }
        else:
            detail = {
                key: payload.get(key)
                for key in ("role", "content")
                if key in payload
            }
        print(f"LINE {lines} {event_type}/{payload_type} {bounded(detail)}")

print(f"PARSED_JSONL_LINES={lines}")
print(f"SESSION_IDS={sorted(session_ids)!r}")
for key, count in sorted(counts.items(), key=lambda item: str(item[0])):
    print(f"COUNT {key!r}={count}")
