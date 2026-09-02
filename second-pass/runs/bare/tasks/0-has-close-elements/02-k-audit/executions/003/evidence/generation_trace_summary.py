#!/usr/bin/env python3
"""Validate and summarize every structured generation-trace record."""

from __future__ import annotations

import collections
import hashlib
import json
import pathlib
import re


def main() -> None:
    root = pathlib.Path("/generation-evidence/codex-trace")
    traces = sorted(root.rglob("*.jsonl"))
    if not traces:
        raise RuntimeError("no structured trace")
    event_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    tool_calls: list[tuple[int, str, str]] = []
    final_messages: list[str] = []
    total_lines = 0
    for trace in traces:
        digest = hashlib.sha256(trace.read_bytes()).hexdigest()
        print(f"TRACE_FILE {trace} sha256={digest}")
        for line_number, line in enumerate(trace.open(), 1):
            total_lines += 1
            record = json.loads(line)
            event_types[record.get("type", "<missing>")] += 1
            payload = record.get("payload") or {}
            payload_types[payload.get("type", "<missing>")] += 1
            if (
                record.get("type") == "response_item"
                and payload.get("type") == "custom_tool_call"
            ):
                raw = payload.get("input", "")
                commands = re.findall(
                    r'cmd:\s*"((?:\\.|[^"\\])*)"|cmd:\s*`([^`]*)`', raw
                )
                summary = " | ".join(
                    bytes(first or second, "utf-8")
                    .decode("unicode_escape", "replace")
                    .replace("\n", " ")
                    for first, second in commands
                )
                if not summary:
                    summary = raw.replace("\n", " ")[:180]
                tool_calls.append(
                    (line_number, payload.get("name", "<missing>"), summary[:500])
                )
            if (
                record.get("type") == "response_item"
                and payload.get("type") == "message"
                and payload.get("role") == "assistant"
                and payload.get("phase") == "final_answer"
            ):
                text = " ".join(
                    part.get("text", "")
                    for part in payload.get("content", [])
                    if isinstance(part, dict)
                )
                final_messages.append(text)

    print(f"JSONL_FILES={len(traces)}")
    print(f"JSON_RECORDS={total_lines}")
    print("EVENT_TYPES=" + json.dumps(event_types, sort_keys=True))
    print("PAYLOAD_TYPES=" + json.dumps(payload_types, sort_keys=True))
    print(f"CUSTOM_TOOL_CALLS={len(tool_calls)}")
    for index, (line, name, summary) in enumerate(tool_calls, 1):
        print(f"CALL {index:02d} trace_line={line} tool={name} summary={summary}")
    print(f"FINAL_MESSAGES={len(final_messages)}")
    for message in final_messages:
        print("UNTRUSTED_FINAL=" + " ".join(message.split()))


if __name__ == "__main__":
    main()
