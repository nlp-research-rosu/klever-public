#!/usr/bin/env python3
"""Parse every structured generation-trace record and inventory tool activity."""

from __future__ import annotations

import collections
import json
from pathlib import Path


def flatten_text(value: object) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        pieces = []
        for item in value:
            if isinstance(item, dict) and isinstance(item.get("text"), str):
                pieces.append(item["text"])
        return "".join(pieces)
    return ""


def one_line(text: str, limit: int = 500) -> str:
    normalized = " ".join(text.split())
    return normalized if len(normalized) <= limit else normalized[:limit] + "…"


def main() -> int:
    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    calls: list[tuple[int, str, str, str]] = []
    outputs: dict[str, tuple[int, str]] = {}
    final_messages: list[tuple[int, str, str]] = []
    record_count = 0

    for trace_file in trace_files:
        for line_number, line in enumerate(trace_file.open(), 1):
            record_count += 1
            record = json.loads(line)
            top_type = str(record.get("type"))
            payload = record.get("payload", {})
            payload_type = str(payload.get("type"))
            top_types[top_type] += 1
            payload_types[payload_type] += 1

            if payload_type in {"custom_tool_call", "function_call"}:
                call_id = str(payload.get("call_id", payload.get("id", "")))
                name = str(payload.get("name", ""))
                raw_input = str(payload.get("input", payload.get("arguments", "")))
                calls.append((line_number, call_id, name, raw_input))
            elif payload_type in {"custom_tool_call_output", "function_call_output"}:
                call_id = str(payload.get("call_id", ""))
                text = flatten_text(payload.get("output"))
                outputs[call_id] = (line_number, text)
            elif payload_type == "message":
                role = str(payload.get("role", ""))
                text = flatten_text(payload.get("content"))
                if role == "assistant":
                    final_messages.append((line_number, role, text))

    print(f"trace_files={len(trace_files)}")
    print(f"json_records_parsed={record_count}")
    print(f"top_types={dict(sorted(top_types.items()))}")
    print(f"payload_types={dict(sorted(payload_types.items()))}")
    print(f"tool_calls={len(calls)} tool_outputs={len(outputs)}")
    for index, (line_number, call_id, name, raw_input) in enumerate(calls, 1):
        output_line, output = outputs.get(call_id, (-1, ""))
        success_words = [
            token
            for token in ("#Top", "exit code: 0", "Process exited with code 0", "succeeded")
            if token in output
        ]
        print(
            f"CALL {index:02d} trace_line={line_number} output_line={output_line} "
            f"name={name} input={one_line(raw_input)}"
        )
        print(
            f"  output_chars={len(output)} markers={success_words} "
            f"output_head={one_line(output, 240)}"
        )
    print(f"assistant_messages={len(final_messages)}")
    for line_number, role, text in final_messages:
        print(
            f"ASSISTANT trace_line={line_number} role={role} "
            f"text={one_line(text, 800)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
