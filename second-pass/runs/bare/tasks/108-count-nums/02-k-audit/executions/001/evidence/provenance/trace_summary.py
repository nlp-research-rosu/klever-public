#!/usr/bin/env python3
"""Summarize every record in the untrusted candidate JSONL trace."""

from __future__ import annotations

import collections
import json
import pathlib
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 64

    trace_path = pathlib.Path(sys.argv[1])
    outer_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    roles: collections.Counter[str] = collections.Counter()
    commands: list[tuple[str, str]] = []
    custom_calls: list[tuple[str, str]] = []
    custom_outputs: list[str] = []
    messages: list[tuple[str, str]] = []
    malformed: list[tuple[int, str]] = []
    record_count = 0

    with trace_path.open(encoding="utf-8") as trace_file:
        for line_no, line in enumerate(trace_file, 1):
            try:
                record = json.loads(line)
            except json.JSONDecodeError as err:
                malformed.append((line_no, str(err)))
                continue
            record_count += 1
            outer_types[str(record.get("type", "<missing>"))] += 1
            payload = record.get("payload")
            if not isinstance(payload, dict):
                continue
            payload_type = str(payload.get("type", "<missing>"))
            payload_types[payload_type] += 1
            role = payload.get("role")
            if role is not None:
                roles[str(role)] += 1
            if payload_type == "function_call":
                commands.append(
                    (
                        str(payload.get("name", "<missing>")),
                        str(payload.get("arguments", "")),
                    )
                )
            if payload_type == "custom_tool_call":
                custom_calls.append(
                    (
                        str(payload.get("name", "<missing>")),
                        str(payload.get("input", "")),
                    )
                )
            if payload_type == "custom_tool_call_output":
                output_text = []
                for item in payload.get("output", []):
                    if isinstance(item, dict) and isinstance(item.get("text"), str):
                        output_text.append(item["text"])
                custom_outputs.append("\n".join(output_text))
            if payload_type == "message":
                text_parts = []
                for item in payload.get("content", []):
                    if isinstance(item, dict) and isinstance(item.get("text"), str):
                        text_parts.append(item["text"])
                messages.append((str(role), "\n".join(text_parts)))

    print(f"TRACE: {trace_path}")
    print(f"VALID_RECORDS: {record_count}")
    print(f"MALFORMED_RECORDS: {len(malformed)}")
    for line_no, error in malformed:
        print(f"  line {line_no}: {error}")
    print("OUTER_TYPES:")
    for key, value in sorted(outer_types.items()):
        print(f"  {key}: {value}")
    print("PAYLOAD_TYPES:")
    for key, value in sorted(payload_types.items()):
        print(f"  {key}: {value}")
    print("ROLES:")
    for key, value in sorted(roles.items()):
        print(f"  {key}: {value}")
    print(f"FUNCTION_CALLS: {len(commands)}")
    for index, (name, arguments) in enumerate(commands, 1):
        print(f"  [{index}] {name}: {arguments}")
    print(f"CUSTOM_TOOL_CALLS: {len(custom_calls)}")
    for index, (name, call_input) in enumerate(custom_calls, 1):
        compact = " ".join(call_input.split())
        print(f"  [{index}] {name} chars={len(call_input)} input={compact[:1200]}")
    print(f"CUSTOM_TOOL_OUTPUTS: {len(custom_outputs)}")
    for index, output in enumerate(custom_outputs, 1):
        compact = " ".join(output.split())
        print(f"  [{index}] chars={len(output)} output={compact[:800]}")
    print(f"MESSAGES: {len(messages)}")
    for index, (role, text) in enumerate(messages, 1):
        compact = " ".join(text.split())
        print(f"  [{index}] role={role} chars={len(text)} text={compact[:500]}")
    return 1 if malformed else 0


if __name__ == "__main__":
    raise SystemExit(main())
