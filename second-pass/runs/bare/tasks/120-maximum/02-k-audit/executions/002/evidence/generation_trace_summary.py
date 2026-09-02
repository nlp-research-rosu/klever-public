#!/usr/bin/env python3
"""Read every generation JSONL record and summarize claims without executing them."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def shorten(value: object, limit: int = 800) -> str:
    text = json.dumps(value, sort_keys=True, ensure_ascii=False)
    if len(text) <= limit:
        return text
    return text[:limit] + f"... <{len(text) - limit} chars omitted>"


def main() -> None:
    paths = sorted(path for path in TRACE_ROOT.rglob("*") if path.is_file())
    event_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    line_count = 0
    parse_errors = 0
    tool_calls: list[tuple[int, str, object]] = []
    agent_messages: list[tuple[int, str]] = []
    top_mentions: list[int] = []

    for path in paths:
        print(f"TRACE {path}")
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, start=1):
                line_count += 1
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as error:
                    parse_errors += 1
                    print(f"PARSE_ERROR line={line_number}: {error}")
                    continue
                event_types[str(record.get("type"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type"))] += 1
                    if payload.get("type") == "custom_tool_call":
                        tool_calls.append(
                            (line_number, str(payload.get("name")), payload.get("input"))
                        )
                    if payload.get("type") == "agent_message":
                        agent_messages.append(
                            (line_number, str(payload.get("message", "")))
                        )
                if "#Top" in line:
                    top_mentions.append(line_number)

    print(f"line_count={line_count}")
    print(f"parse_errors={parse_errors}")
    print(f"event_types={dict(sorted(event_types.items()))}")
    print(f"payload_types={dict(sorted(payload_types.items()))}")
    print(f"top_mention_lines={top_mentions}")
    for line_number, name, value in tool_calls:
        print(f"TOOL_CALL line={line_number} name={name} input={shorten(value)}")
    for line_number, message in agent_messages:
        print(f"AGENT_MESSAGE line={line_number} text={shorten(message)}")


if __name__ == "__main__":
    main()
