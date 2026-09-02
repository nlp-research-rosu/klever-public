#!/usr/bin/env python3
"""Read every structured generation-trace record and emit a bounded inventory."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/24/"
    "rollout-2026-07-24T22-25-59-019f974e-ea3b-79b3-849b-474a773871f0.jsonl"
)


def clipped(value: object, limit: int = 500) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit] + "…"


outer_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
response_roles: collections.Counter[str] = collections.Counter()
tool_calls: list[tuple[int, str, str]] = []
assistant_messages: list[tuple[int, str]] = []
token_events: list[tuple[int, str]] = []

with TRACE.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        record = json.loads(line)
        outer_type = str(record.get("type", "<missing>"))
        outer_types[outer_type] += 1
        payload = record.get("payload", {})
        if not isinstance(payload, dict):
            payload = {}
        payload_type = str(payload.get("type", "<missing>"))
        payload_types[payload_type] += 1

        if outer_type == "response_item":
            role = str(payload.get("role", ""))
            response_roles[role] += 1
            if payload_type in {"function_call", "custom_tool_call"}:
                name = str(payload.get("name", "<unnamed>"))
                arguments = payload.get("arguments", payload.get("input", ""))
                tool_calls.append((line_number, name, clipped(arguments)))
            elif payload_type == "message" and role == "assistant":
                pieces: list[str] = []
                for item in payload.get("content", []):
                    if isinstance(item, dict) and "text" in item:
                        pieces.append(str(item["text"]))
                assistant_messages.append((line_number, clipped(" ".join(pieces))))

        if outer_type == "event_msg" and payload_type == "token_count":
            info = payload.get("info", {})
            token_events.append((line_number, clipped(info)))

print(f"trace={TRACE}")
print(f"records={sum(outer_types.values())}")
print(f"outer_types={dict(sorted(outer_types.items()))}")
print(f"payload_types={dict(sorted(payload_types.items()))}")
print(f"response_roles={dict(sorted(response_roles.items()))}")
print(f"tool_calls={len(tool_calls)}")
for line_number, name, arguments in tool_calls:
    print(f"tool line={line_number} name={name} args={arguments}")
print(f"assistant_messages={len(assistant_messages)}")
for line_number, message in assistant_messages:
    print(f"assistant line={line_number} text={message}")
print(f"token_count_events={len(token_events)}")
for line_number, info in token_events:
    print(f"tokens line={line_number} info={info}")
