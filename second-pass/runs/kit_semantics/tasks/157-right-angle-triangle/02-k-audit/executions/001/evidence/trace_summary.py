#!/usr/bin/env python3
"""Summarize the untrusted structured generation trace without executing it."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def truncate(text: str, limit: int = 500) -> str:
    text = text.replace("\r", "")
    if len(text) <= limit:
        return text
    return text[:limit] + f"... <{len(text) - limit} chars omitted>"


def main() -> None:
    top_types: collections.Counter[str] = collections.Counter()
    response_types: collections.Counter[str] = collections.Counter()
    event_types: collections.Counter[str] = collections.Counter()
    tool_names: collections.Counter[str] = collections.Counter()
    calls: list[tuple[int, str, str]] = []
    messages: list[tuple[int, str, str]] = []
    total = 0

    for trace in sorted(TRACE_ROOT.rglob("*.jsonl")):
        print(f"TRACE_FILE {trace}")
        with trace.open() as stream:
            for line_number, line in enumerate(stream, 1):
                event = json.loads(line)
                total += 1
                event_type = event.get("type", "<missing>")
                top_types[event_type] += 1
                payload = event.get("payload", {})
                if event_type == "response_item":
                    response_type = payload.get("type", "<missing>")
                    response_types[response_type] += 1
                    if response_type in {"function_call", "custom_tool_call"}:
                        name = payload.get("name", "<missing>")
                        tool_names[name] += 1
                        args = payload.get("arguments", payload.get("input", ""))
                        calls.append((line_number, name, truncate(str(args))))
                    elif response_type == "message":
                        role = payload.get("role", "<missing>")
                        chunks = payload.get("content", [])
                        texts = [
                            chunk.get("text", "")
                            for chunk in chunks
                            if isinstance(chunk, dict) and "text" in chunk
                        ]
                        if texts:
                            messages.append((line_number, role, truncate("\n".join(texts), 1000)))
                elif event_type == "event_msg":
                    subtype = payload.get("type", "<missing>")
                    event_types[subtype] += 1

    print(f"TOTAL_JSON_EVENTS {total}")
    print(f"TOP_LEVEL_TYPES {dict(top_types)}")
    print(f"RESPONSE_ITEM_TYPES {dict(response_types)}")
    print(f"EVENT_MSG_TYPES {dict(event_types)}")
    print(f"TOOL_NAMES {dict(tool_names)}")
    print("MESSAGES")
    for line_number, role, text in messages:
        print(f"  line={line_number} role={role} text={text!r}")
    print("TOOL_CALLS")
    for line_number, name, args in calls:
        print(f"  line={line_number} name={name} args={args!r}")


if __name__ == "__main__":
    main()
