#!/usr/bin/env python3
"""Bounded reader for the untrusted structured generation trace."""

from __future__ import annotations

import json
import sys
from pathlib import Path


path = Path(sys.argv[1])
counts: dict[tuple[str | None, str | None], int] = {}


def bounded(value: object, limit: int = 1600) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    if len(text) > limit:
        return text[:limit] + f"\n... [truncated {len(text) - limit} characters]"
    return text


with path.open(encoding="utf-8") as stream:
    for lineno, line in enumerate(stream, 1):
        item = json.loads(line)
        outer = item.get("type")
        payload = item.get("payload") or {}
        inner = payload.get("type") if isinstance(payload, dict) else None
        counts[(outer, inner)] = counts.get((outer, inner), 0) + 1

        if outer == "event_msg" and inner in {
            "user_message",
            "agent_message",
            "task_complete",
            "patch_apply_end",
        }:
            print(f"LINE {lineno} EVENT {inner}")
            print(bounded(payload))
        elif outer == "response_item" and inner in {
            "custom_tool_call",
            "custom_tool_call_output",
            "function_call",
            "function_call_output",
        }:
            print(f"LINE {lineno} RESPONSE {inner}")
            print(bounded(payload))

print("EVENT_COUNTS")
for key in sorted(counts, key=lambda k: (str(k[0]), str(k[1]))):
    print(f"{key}: {counts[key]}")
