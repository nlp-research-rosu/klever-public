#!/usr/bin/env python3
"""Bounded, complete-iteration summary of the untrusted generation trace."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T03-15-21-019f8e0b-1e90-7332-9ade-efecd511ca1c.jsonl"
)


def main() -> None:
    counts: Counter[tuple[object, ...]] = Counter()
    calls: list[tuple[int, str, str]] = []
    final_messages: list[tuple[int, str]] = []
    line_count = 0
    with TRACE.open(encoding="utf-8") as stream:
        for line_count, line in enumerate(stream, 1):
            event = json.loads(line)
            payload = event.get("payload", {})
            key = (
                event.get("type"),
                payload.get("type"),
                payload.get("name"),
                payload.get("role"),
            )
            counts[key] += 1
            if payload.get("type") in {"function_call", "custom_tool_call"}:
                body = payload.get("arguments", payload.get("input", ""))
                calls.append((line_count, str(payload.get("name")), str(body)))
            if (
                payload.get("type") == "message"
                and payload.get("role") == "assistant"
            ):
                text = "\n".join(
                    str(item.get("text", ""))
                    for item in payload.get("content", [])
                    if isinstance(item, dict)
                )
                final_messages.append((line_count, text))

    print(f"trace={TRACE}")
    print(f"sha256={hashlib.sha256(TRACE.read_bytes()).hexdigest()}")
    print(f"parsed_lines={line_count}")
    print("event_counts:")
    for key, count in sorted(counts.items(), key=lambda pair: repr(pair[0])):
        print(count, key)
    print("tool_calls (each trace call visited; bodies bounded to 1200 chars):")
    for line_number, name, body in calls:
        compact = body.replace("\x00", "<NUL>")
        print(f"LINE {line_number} {name}")
        print(compact[:1200])
        if len(compact) > 1200:
            print(f"... truncated {len(compact) - 1200} chars")
    print("assistant_messages:")
    for line_number, text in final_messages:
        print(f"LINE {line_number}")
        print(text[:2000])
        if len(text) > 2000:
            print(f"... truncated {len(text) - 2000} chars")


if __name__ == "__main__":
    main()
