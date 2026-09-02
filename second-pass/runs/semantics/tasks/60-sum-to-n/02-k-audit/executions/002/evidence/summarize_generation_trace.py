#!/usr/bin/env python3
"""Parse every structured generation-trace record and summarize untrusted actions."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T00-51-43-019f8d87-a172-7f52-8300-3fbac7774c34.jsonl"
)


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


outer = collections.Counter()
inner = collections.Counter()
calls = {}
lines = TRACE.read_text().splitlines()
print(f"trace={TRACE}")
print(f"line_count={len(lines)}")

for line_number, raw in enumerate(lines, 1):
    record = json.loads(raw)
    record_type = record.get("type")
    payload = record.get("payload", {})
    payload_type = payload.get("type") if isinstance(payload, dict) else None
    outer[record_type] += 1
    inner[(record_type, payload_type)] += 1

    if record_type == "response_item" and payload_type == "function_call":
        call_id = payload.get("call_id")
        calls[call_id] = (payload.get("name"), payload.get("arguments", ""))
        print(
            f"line={line_number} function_call id={call_id} "
            f"name={payload.get('name')} arguments={payload.get('arguments')}"
        )
    elif record_type == "response_item" and payload_type == "function_call_output":
        call_id = payload.get("call_id")
        output = str(payload.get("output", ""))
        name, arguments = calls.get(call_id, ("UNKNOWN", ""))
        first = output[:240].replace("\n", "\\n")
        last = output[-240:].replace("\n", "\\n")
        print(
            f"line={line_number} function_output id={call_id} name={name} "
            f"bytes={len(output.encode())} sha256={digest(output)} "
            f"first={first!r} last={last!r}"
        )
    elif record_type == "response_item" and payload_type == "message":
        role = payload.get("role")
        parts = []
        for item in payload.get("content", []):
            if isinstance(item, dict):
                parts.append(str(item.get("text", "")))
        text = "\n".join(parts)
        print(
            f"line={line_number} message role={role} chars={len(text)} "
            f"sha256={digest(text)} first={text[:240]!r} last={text[-240:]!r}"
        )
    elif record_type == "event_msg" and payload_type in {
        "agent_message",
        "user_message",
        "task_complete",
    }:
        text = json.dumps(payload, sort_keys=True)
        print(
            f"line={line_number} event={payload_type} chars={len(text)} "
            f"sha256={digest(text)} first={text[:240]!r} last={text[-240:]!r}"
        )

print("outer_counts=" + json.dumps(outer, sort_keys=True))
print(
    "inner_counts="
    + json.dumps({f"{a}/{b}": n for (a, b), n in inner.items()}, sort_keys=True)
)
print(f"parsed_all_lines={len(lines)}")
