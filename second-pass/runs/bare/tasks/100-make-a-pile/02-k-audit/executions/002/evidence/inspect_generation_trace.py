#!/usr/bin/env python3
"""Parse every JSONL event and emit a bounded, audit-oriented trace summary."""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path


def one_line(value: object, limit: int = 500) -> str:
    text = json.dumps(value, sort_keys=True, ensure_ascii=False)
    text = " ".join(text.splitlines())
    return text if len(text) <= limit else text[:limit] + "...[truncated]"


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    roles: collections.Counter[str] = collections.Counter()
    selected: list[tuple[int, str, object]] = []
    last_usage: tuple[int, object] | None = None
    line_count = 0

    with path.open("r", encoding="utf-8") as stream:
        for line_count, raw in enumerate(stream, 1):
            event = json.loads(raw)
            top_type = str(event.get("type", "<missing>"))
            payload = event.get("payload", {})
            payload_type = (
                str(payload.get("type", "<missing>"))
                if isinstance(payload, dict)
                else "<non-object>"
            )
            top_types[top_type] += 1
            payload_types[f"{top_type}/{payload_type}"] += 1

            if isinstance(payload, dict):
                role = payload.get("role")
                if role is not None:
                    roles[str(role)] += 1

                if top_type == "response_item":
                    if payload_type in {
                        "function_call",
                        "function_call_output",
                        "custom_tool_call",
                        "custom_tool_call_output",
                        "message",
                    }:
                        if payload_type == "message":
                            role = str(payload.get("role", ""))
                            if role in {"assistant", "user"}:
                                selected.append((line_count, f"message/{role}", payload))
                        else:
                            selected.append((line_count, payload_type, payload))

                if top_type == "event_msg" and payload_type in {
                    "agent_message",
                    "task_complete",
                    "token_count",
                }:
                    if payload_type == "token_count":
                        last_usage = (line_count, payload)
                    else:
                        selected.append((line_count, payload_type, payload))

    print(f"TRACE={path}")
    print(f"PARSED_LINES={line_count}")
    print("TOP_LEVEL_TYPES")
    for key, count in sorted(top_types.items()):
        print(f"  {count:4d} {key}")
    print("PAYLOAD_TYPES")
    for key, count in sorted(payload_types.items()):
        print(f"  {count:4d} {key}")
    print("ROLES")
    for key, count in sorted(roles.items()):
        print(f"  {count:4d} {key}")
    print("SELECTED_EVENTS")
    for line_number, kind, payload in selected:
        print(f"LINE {line_number} {kind}: {one_line(payload)}")
    if last_usage is not None:
        print("LAST_TOKEN_COUNT")
        print(f"LINE {last_usage[0]}: {one_line(last_usage[1], 2000)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
