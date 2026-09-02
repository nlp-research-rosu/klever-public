#!/usr/bin/env python3
"""Render the untrusted structured generation trace into an auditable index."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/30/"
    "rollout-2026-07-30T02-41-01-019fb1f8-331d-7603-85c8-afe787e74891.jsonl"
)


def compact(value: object, limit: int = 1600) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    text = text.replace("\n", "\\n")
    return text if len(text) <= limit else text[:limit] + "...<TRUNCATED>"


counts: collections.Counter[str] = collections.Counter()
payload_counts: collections.Counter[str] = collections.Counter()
indexed: list[str] = []
parse_errors: list[str] = []

with TRACE.open(encoding="utf-8") as handle:
    for line_number, raw in enumerate(handle, 1):
        try:
            event = json.loads(raw)
        except Exception as error:  # noqa: BLE001 - audit malformed evidence
            parse_errors.append(f"line={line_number} error={error}")
            continue
        event_type = str(event.get("type"))
        counts[event_type] += 1
        payload = event.get("payload", {})
        payload_type = str(payload.get("type")) if isinstance(payload, dict) else type(payload).__name__
        payload_counts[f"{event_type}/{payload_type}"] += 1

        if event_type == "response_item" and isinstance(payload, dict):
            if payload_type == "function_call":
                indexed.append(
                    f"line={line_number} function_call "
                    f"name={payload.get('name')} arguments={compact(payload.get('arguments'))}"
                )
            elif payload_type == "function_call_output":
                output = payload.get("output")
                indexed.append(
                    f"line={line_number} function_output "
                    f"call_id={payload.get('call_id')} output={compact(output, 900)}"
                )
            elif payload_type == "message":
                role = payload.get("role")
                if role in {"assistant", "user"}:
                    indexed.append(
                        f"line={line_number} message role={role} "
                        f"content={compact(payload.get('content'), 2200)}"
                    )
        elif event_type == "event_msg" and isinstance(payload, dict):
            if payload_type in {"agent_message", "task_complete", "task_completed"}:
                indexed.append(
                    f"line={line_number} event_msg type={payload_type} payload={compact(payload, 2200)}"
                )

print(f"trace={TRACE}")
print(f"line_count={sum(counts.values())}")
print(f"parse_error_count={len(parse_errors)}")
for error in parse_errors:
    print(f"PARSE_ERROR {error}")
print("EVENT_COUNTS")
for name, count in sorted(counts.items()):
    print(f"{name}={count}")
print("PAYLOAD_COUNTS")
for name, count in sorted(payload_counts.items()):
    print(f"{name}={count}")
print("INDEXED_GENERATION_ACTIONS_AND_MESSAGES")
for line in indexed:
    print(line)
