#!/usr/bin/env python3
"""Validate every JSONL record and summarize all observable generation actions."""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path


def text_content(payload: dict) -> str:
    return "\n".join(
        item.get("text", "")
        for item in payload.get("content", [])
        if isinstance(item, dict)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("trace", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    outer = collections.Counter()
    inner = collections.Counter()
    calls = []
    messages = []
    record_count = 0
    with args.trace.open() as stream:
        for line_number, line in enumerate(stream, 1):
            record_count = line_number
            record = json.loads(line)
            record_type = record["type"]
            payload = record.get("payload", {})
            outer[record_type] += 1
            inner[(record_type, payload.get("type"))] += 1
            if record_type == "response_item" and payload.get("type") == "function_call":
                calls.append(
                    (
                        line_number,
                        payload.get("name"),
                        payload.get("arguments", ""),
                    )
                )
            if record_type == "response_item" and payload.get("type") == "message":
                content = text_content(payload)
                messages.append(
                    (line_number, payload.get("role"), len(content), content)
                )

    lines = [
        "# Generation trace structural review",
        "",
        f"- JSONL records parsed: {record_count}",
        f"- Outer record types: `{dict(sorted(outer.items()))}`",
        f"- Nested record types: `{dict(sorted(inner.items(), key=str))}`",
        f"- Function calls: {len(calls)}",
        f"- Messages: {len(messages)}",
        "",
        "## Function calls",
        "",
    ]
    for line_number, name, arguments in calls:
        lines.extend(
            [
                f"### Line {line_number}: `{name}`",
                "",
                "```json",
                arguments,
                "```",
                "",
            ]
        )
    lines.extend(["## Messages", ""])
    for line_number, role, length, content in messages:
        lines.extend(
            [
                f"### Line {line_number}: `{role}` ({length} characters)",
                "",
                "```text",
                content,
                "```",
                "",
            ]
        )
    args.output.write_text("\n".join(lines).rstrip() + "\n")
    print(f"valid_jsonl_records={record_count}")
    print(f"function_calls={len(calls)}")
    print(f"messages={len(messages)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
