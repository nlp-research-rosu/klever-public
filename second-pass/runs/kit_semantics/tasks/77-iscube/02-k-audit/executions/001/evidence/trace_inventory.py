#!/usr/bin/env python3
"""Parse every JSONL record and summarize the untrusted generation trace."""

from __future__ import annotations

import collections
import json
from pathlib import Path


def shorten(value: object, limit: int = 280) -> str:
    text = json.dumps(value, sort_keys=True, ensure_ascii=False)
    text = text.replace("\n", "\\n")
    return text if len(text) <= limit else text[:limit] + "..."


def main() -> None:
    paths = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    event_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    commands: list[tuple[int, str]] = []
    final_messages: list[tuple[int, str]] = []
    line_count = 0
    for path in paths:
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                line_count += 1
                value = json.loads(line)
                event_type = str(value.get("type", "<missing>"))
                event_types[event_type] += 1
                payload = value.get("payload")
                if isinstance(payload, dict):
                    payload_type = str(payload.get("type", "<missing>"))
                    payload_types[payload_type] += 1
                    if payload_type in {
                        "function_call",
                        "custom_tool_call",
                        "function_call_output",
                    }:
                        commands.append((line_number, shorten(payload, 640)))
                    if (
                        payload_type == "message"
                        and payload.get("role") == "assistant"
                    ):
                        content = payload.get("content")
                        if isinstance(content, list):
                            for item in content:
                                if (
                                    isinstance(item, dict)
                                    and item.get("type") == "output_text"
                                ):
                                    final_messages.append(
                                        (line_number, shorten(item, 640))
                                    )
                response = value.get("response")
                if isinstance(response, dict):
                    response_type = str(response.get("type", "<missing>"))
                    payload_types[f"response:{response_type}"] += 1
    print(f"trace_files={len(paths)}")
    print(f"jsonl_records={line_count}")
    print(f"event_types={dict(sorted(event_types.items()))}")
    print(f"payload_types={dict(sorted(payload_types.items()))}")
    print(f"tool_related_records={len(commands)}")
    for line_number, record in commands:
        print(f"TRACE_TOOL line={line_number} {record}")
    print(f"assistant_output_messages={len(final_messages)}")
    for line_number, record in final_messages:
        print(f"TRACE_ASSISTANT line={line_number} {record}")


if __name__ == "__main__":
    main()
