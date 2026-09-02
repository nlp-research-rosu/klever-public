#!/usr/bin/env python3
"""Summarize every structured generation-trace record as untrusted provenance."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def compact(value, limit: int = 800) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    if len(text) <= limit:
        return text
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return f"{text[:limit]}...<TRUNCATED sha256={digest} chars={len(text)}>"


def main() -> int:
    trace_files = sorted(TRACE_ROOT.rglob("*.jsonl"))
    print(f"TRACE_FILE_COUNT={len(trace_files)}")
    for trace_file in trace_files:
        print(f"TRACE_FILE={trace_file}")
        type_counts: collections.Counter[str] = collections.Counter()
        subtype_counts: collections.Counter[tuple[str, str]] = collections.Counter()
        tool_calls = []
        tool_outputs = []
        assistant_messages = []
        malformed = 0
        first_timestamp = None
        last_timestamp = None
        line_count = 0
        with trace_file.open("r", encoding="utf-8") as stream:
            for line_count, line in enumerate(stream, 1):
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as err:
                    malformed += 1
                    print(f"MALFORMED line={line_count} error={err}")
                    continue
                timestamp = record.get("timestamp")
                first_timestamp = first_timestamp or timestamp
                last_timestamp = timestamp
                record_type = record.get("type", "<missing>")
                payload = record.get("payload") or {}
                subtype = payload.get("type", "<none>")
                type_counts[record_type] += 1
                subtype_counts[(record_type, subtype)] += 1
                if record_type == "response_item" and subtype in {
                    "function_call",
                    "custom_tool_call",
                }:
                    tool_calls.append((line_count, payload))
                if record_type == "response_item" and subtype in {
                    "function_call_output",
                    "custom_tool_call_output",
                }:
                    tool_outputs.append((line_count, payload))
                if record_type == "event_msg" and subtype == "agent_message":
                    assistant_messages.append((line_count, payload))
                if (
                    record_type == "response_item"
                    and subtype == "message"
                    and payload.get("role") == "assistant"
                ):
                    assistant_messages.append((line_count, payload))

        print(
            f"TRACE_PARSE lines={line_count} malformed={malformed} "
            f"first={first_timestamp} last={last_timestamp}"
        )
        for name, count in sorted(type_counts.items()):
            print(f"TYPE_COUNT {name}={count}")
        for (name, subtype), count in sorted(subtype_counts.items()):
            print(f"SUBTYPE_COUNT {name}/{subtype}={count}")

        print(f"TOOL_CALL_COUNT={len(tool_calls)}")
        for line_number, payload in tool_calls:
            name = payload.get("name") or payload.get("tool")
            call_id = payload.get("call_id") or payload.get("id")
            arguments = payload.get("arguments")
            if arguments is None:
                arguments = payload.get("input")
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError:
                    pass
            print(
                f"TOOL_CALL line={line_number} name={name} id={call_id} "
                f"arguments={compact(arguments)}"
            )

        print(f"TOOL_OUTPUT_COUNT={len(tool_outputs)}")
        for line_number, payload in tool_outputs:
            call_id = payload.get("call_id") or payload.get("id")
            output = payload.get("output")
            if output is None:
                output = payload.get("content")
            print(
                f"TOOL_OUTPUT line={line_number} id={call_id} "
                f"output={compact(output, 500)}"
            )

        print(f"ASSISTANT_MESSAGE_COUNT={len(assistant_messages)}")
        for line_number, payload in assistant_messages:
            text = payload.get("message")
            if text is None:
                text = payload.get("content")
            print(f"ASSISTANT_MESSAGE line={line_number} content={compact(text, 1200)}")

    return 1 if malformed else 0


if __name__ == "__main__":
    raise SystemExit(main())
