#!/usr/bin/env python3
"""Read every generation trace/log record and emit a bounded audit summary."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


trace_root = Path("/generation-evidence/codex-trace")
trace_files = sorted(path for path in trace_root.rglob("*") if path.is_file())

calls: dict[str, tuple[str, str]] = {}
call_outputs: dict[str, str] = {}
messages: list[tuple[str, str]] = []
payload_counts: Counter[str] = Counter()

for trace_file in trace_files:
    with trace_file.open(encoding="utf-8") as stream:
        for line in stream:
            record = json.loads(line)
            payload = record.get("payload")
            if not isinstance(payload, dict):
                continue
            payload_type = str(payload.get("type"))
            payload_counts[payload_type] += 1
            if payload_type == "custom_tool_call":
                calls[str(payload.get("call_id"))] = (
                    str(payload.get("name")),
                    str(payload.get("input")),
                )
            elif payload_type == "custom_tool_call_output":
                output = payload.get("output")
                call_outputs[str(payload.get("call_id"))] = json.dumps(
                    output, sort_keys=True
                )
            elif payload_type in {"agent_message", "user_message"}:
                messages.append((payload_type, str(payload.get("message"))))
            elif payload_type == "message":
                text_parts = []
                for item in payload.get("content", []):
                    if isinstance(item, dict) and "text" in item:
                        text_parts.append(str(item["text"]))
                messages.append((f"message:{payload.get('role')}", "\n".join(text_parts)))

print(f"trace_files={len(trace_files)}")
print(f"payload_counts={dict(sorted(payload_counts.items()))}")
print(f"tool_calls={len(calls)} tool_outputs={len(call_outputs)}")
print("TRACE MESSAGES")
for index, (kind, message) in enumerate(messages, 1):
    collapsed = re.sub(r"\s+", " ", message).strip()
    print(f"{index:03d} {kind}: {collapsed[:1000]}")

print("TRACE TOOL-CALL INVENTORY")
for index, (call_id, (name, call_input)) in enumerate(calls.items(), 1):
    output = call_outputs.get(call_id, "<missing>")
    input_collapsed = re.sub(r"\s+", " ", call_input).strip()
    output_collapsed = re.sub(r"\s+", " ", output).strip()
    print(
        f"{index:03d} {name} id={call_id} "
        f"input={input_collapsed[:1600]} output={output_collapsed[:1000]}"
    )

log_path = Path("/generation-evidence/codex-output.log")
patterns = {
    "kprove": re.compile(rb"kprove", re.IGNORECASE),
    "krun": re.compile(rb"\bkrun\b", re.IGNORECASE),
    "kompile": re.compile(rb"kompile", re.IGNORECASE),
    "top": re.compile(rb"#Top"),
    "stuck": re.compile(rb"WarnStuckClaimState"),
    "result_marker": re.compile(rb"KPROVE_PASSED"),
    "error": re.compile(rb"\berror\b", re.IGNORECASE),
}
counts = Counter()
selected: list[tuple[int, str]] = []
with log_path.open("rb") as stream:
    for line_number, line in enumerate(stream, 1):
        matched = []
        for name, pattern in patterns.items():
            if pattern.search(line):
                counts[name] += 1
                matched.append(name)
        if matched and len(selected) < 160:
            text = line.decode("utf-8", errors="replace")
            text = re.sub(r"\s+", " ", text).strip()
            selected.append((line_number, text[:1200]))
print(f"codex_output_pattern_counts={dict(sorted(counts.items()))}")
print("CODEX OUTPUT SELECTED LINES (bounded)")
for line_number, text in selected:
    print(f"{line_number}: {text}")

print("GENERATION_RECORD_REVIEW=COMPLETE")
