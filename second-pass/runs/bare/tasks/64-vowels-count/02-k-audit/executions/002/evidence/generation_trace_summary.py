#!/usr/bin/env python3
"""Read every structured trace record and emit a bounded evidentiary summary."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def shorten(value: str, limit: int = 1200) -> str:
    value = value.replace("\x00", "\\0")
    if len(value) <= limit:
        return value
    return value[:limit] + f"... <truncated {len(value) - limit} chars>"


top_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
record_count = 0
parse_failures = 0
selected: list[str] = []

for trace_path in sorted(TRACE_ROOT.rglob("*.jsonl")):
    print(f"TRACE_FILE {trace_path}")
    with trace_path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record_count += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                parse_failures += 1
                selected.append(f"line={line_number} JSON_ERROR {error}")
                continue
            top_type = str(record.get("type"))
            top_types[top_type] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type = str(payload.get("type"))
                payload_types[payload_type] += 1
                if payload_type == "custom_tool_call":
                    name = payload.get("name")
                    tool_input = str(payload.get("input", ""))
                    if any(
                        keyword in tool_input
                        for keyword in ("kompile", "kprove", "krun", "semantic.k", "spec.k")
                    ):
                        selected.append(
                            f"line={line_number} TOOL name={name} input={shorten(tool_input)}"
                        )
                elif payload_type == "custom_tool_call_output":
                    output = json.dumps(payload.get("output"), sort_keys=True)
                    if any(
                        keyword in output
                        for keyword in ("#Top", "WarnStuckClaimState", "kompile", "krun")
                    ):
                        selected.append(
                            f"line={line_number} TOOL_OUTPUT {shorten(output)}"
                        )
                elif payload_type == "message" and payload.get("role") == "assistant":
                    text_parts: list[str] = []
                    for item in payload.get("content", []):
                        if isinstance(item, dict) and "text" in item:
                            text_parts.append(str(item["text"]))
                    message = "\n".join(text_parts)
                    if message:
                        selected.append(
                            f"line={line_number} ASSISTANT phase={payload.get('phase')} "
                            f"text={shorten(message)}"
                        )
                elif payload_type in {"agent_message", "task_complete"}:
                    selected.append(
                        f"line={line_number} EVENT {payload_type} {shorten(json.dumps(payload, sort_keys=True))}"
                    )

print(f"record_count={record_count}")
print(f"parse_failures={parse_failures}")
print(f"top_types={dict(sorted(top_types.items()))}")
print(f"payload_types={dict(sorted(payload_types.items()))}")
print(f"selected_record_count={len(selected)}")
for item in selected:
    print(item)

assert record_count > 0
assert parse_failures == 0
print("STRUCTURED_TRACE_FULL_PARSE_OK")
