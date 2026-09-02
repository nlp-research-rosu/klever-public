#!/usr/bin/env python3
"""Parse every structured-trace record and inspect the complete console log."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path


trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
top_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
tool_calls: list[dict[str, object]] = []
tool_outputs: list[dict[str, object]] = []
messages: list[dict[str, object]] = []
record_count = 0

for trace in trace_files:
    with trace.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            record_count += 1
            top = str(record.get("type"))
            top_types[top] += 1
            payload = record.get("payload")
            subtype = payload.get("type") if isinstance(payload, dict) else None
            if subtype is not None:
                payload_types[str(subtype)] += 1
            if top == "response_item" and isinstance(payload, dict):
                if subtype in {"function_call", "custom_tool_call"}:
                    tool_calls.append(
                        {
                            "line": line_number,
                            "name": payload.get("name"),
                            "arguments": payload.get("arguments")
                            or payload.get("input"),
                        }
                    )
                elif subtype in {
                    "function_call_output",
                    "custom_tool_call_output",
                }:
                    raw = str(payload.get("output", ""))
                    tool_outputs.append(
                        {
                            "line": line_number,
                            "length": len(raw),
                            "sha256": hashlib.sha256(raw.encode()).hexdigest(),
                            "head": raw[:160].replace("\n", "\\n"),
                            "tail": raw[-160:].replace("\n", "\\n"),
                        }
                    )
                elif subtype == "message":
                    content = payload.get("content", [])
                    text = "\n".join(
                        str(item.get("text", ""))
                        for item in content
                        if isinstance(item, dict)
                    )
                    messages.append(
                        {
                            "line": line_number,
                            "role": payload.get("role"),
                            "phase": payload.get("phase"),
                            "length": len(text),
                            "sha256": hashlib.sha256(text.encode()).hexdigest(),
                            "head": text[:240].replace("\n", "\\n"),
                            "tail": text[-240:].replace("\n", "\\n"),
                        }
                    )

print(f"trace_files={len(trace_files)}")
print(f"valid_json_records={record_count}")
print("top_level_types=" + json.dumps(top_types, sort_keys=True))
print("payload_types=" + json.dumps(payload_types, sort_keys=True))
print(f"tool_call_count={len(tool_calls)}")
for item in tool_calls:
    print("TOOL_CALL " + json.dumps(item, sort_keys=True))
print(f"tool_output_count={len(tool_outputs)}")
for item in tool_outputs:
    print("TOOL_OUTPUT " + json.dumps(item, sort_keys=True))
print(f"message_count={len(messages)}")
for item in messages:
    print("MESSAGE " + json.dumps(item, sort_keys=True))

console = Path("/generation-evidence/codex-output.log").read_text(
    encoding="utf-8", errors="replace"
)
console_lines = console.splitlines()
keywords = [
    "kprove",
    "#Top",
    "WarnStuckClaimState",
    "Error",
    "RESULT:",
    "timed out",
]
print(f"console_bytes={len(console.encode())}")
print(f"console_lines={len(console_lines)}")
for keyword in keywords:
    hits = [
        {"line": index, "text": line[:500]}
        for index, line in enumerate(console_lines, 1)
        if keyword in line
    ]
    print(f"CONSOLE_MATCHES[{keyword}]=" + json.dumps(hits, sort_keys=True))
print("console_head=" + json.dumps(console_lines[:20]))
print("console_tail=" + json.dumps(console_lines[-20:]))
print("RESULT=COMPLETE_PARSE")
