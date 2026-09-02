#!/usr/bin/env python3
"""Parse every generation trace/output record and extract audit-relevant claims."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")
OUTPUT = Path("/generation-evidence/codex-output.log")
SUMMARY = Path("/audit-output/evidence/generation-trace-summary.txt")
KEYLINES = Path("/audit-output/evidence/generation-output-keylines.txt")


def clipped(value: object, limit: int = 1800) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    if len(text) <= limit:
        return text
    return text[: limit // 2] + f"\n...<{len(text) - limit} chars omitted>...\n" + text[-limit // 2 :]


def content_text(content: object) -> str:
    if not isinstance(content, list):
        return clipped(content)
    texts: list[str] = []
    for item in content:
        if isinstance(item, dict):
            value = item.get("text")
            if isinstance(value, str):
                texts.append(value)
    return "\n".join(texts)


trace_counts: collections.Counter[str] = collections.Counter()
subtype_counts: collections.Counter[str] = collections.Counter()
selected: list[str] = []
line_total = 0

for trace in sorted(TRACE_ROOT.rglob("*.jsonl")):
    for line_number, raw in enumerate(trace.open(), 1):
        line_total += 1
        event = json.loads(raw)
        event_type = str(event.get("type"))
        payload = event.get("payload", {})
        trace_counts[event_type] += 1
        subtype = payload.get("type") if isinstance(payload, dict) else None
        subtype_counts[f"{event_type}:{subtype}"] += 1

        if event_type == "response_item" and isinstance(payload, dict):
            if subtype == "message":
                role = payload.get("role")
                if role == "assistant":
                    text = content_text(payload.get("content"))
                    selected.append(
                        f"TRACE {trace.name}:{line_number} ASSISTANT MESSAGE\n{clipped(text)}"
                    )
            elif subtype in {"function_call", "custom_tool_call"}:
                selected.append(
                    f"TRACE {trace.name}:{line_number} TOOL CALL {payload.get('name')}\n"
                    + clipped(payload.get("arguments") or payload.get("input"))
                )
            elif subtype in {"function_call_output", "custom_tool_call_output"}:
                selected.append(
                    f"TRACE {trace.name}:{line_number} TOOL OUTPUT\n"
                    + clipped(payload.get("output"))
                )
        elif event_type == "event_msg" and isinstance(payload, dict):
            if subtype in {"agent_message", "turn_aborted", "task_complete"}:
                selected.append(
                    f"TRACE {trace.name}:{line_number} EVENT {subtype}\n{clipped(payload)}"
                )

with SUMMARY.open("w") as stream:
    stream.write(f"PARSED_JSONL_LINES: {line_total}\n")
    stream.write("EVENT_COUNTS:\n")
    for key, value in sorted(trace_counts.items()):
        stream.write(f"  {key}: {value}\n")
    stream.write("SUBTYPE_COUNTS:\n")
    for key, value in sorted(subtype_counts.items()):
        stream.write(f"  {key}: {value}\n")
    stream.write("\nSELECTED_EVENTS:\n")
    for item in selected:
        stream.write(item)
        stream.write("\n\n")

patterns = re.compile(
    r"#Top|WarnStuck|Error|kompile|kprove|krun|python3|apply_patch|"
    r"VALIDATED|SOUND-BUT|FORMALLY|Incomplete|Gate [ABC]|"
    r"RESULT:|mutation|vacu|differential|bridge|oracle|opaque|"
    r"solution\\.mpy|verification\\.k|spec\\.k",
    re.IGNORECASE,
)
output_line_count = 0
matching: list[tuple[int, str]] = []
for number, line in enumerate(OUTPUT.open(errors="replace"), 1):
    output_line_count = number
    if patterns.search(line):
        matching.append((number, line.rstrip("\n")))

with KEYLINES.open("w") as stream:
    stream.write(f"READ_OUTPUT_LINES: {output_line_count}\n")
    stream.write(f"MATCHING_LINES: {len(matching)}\n")
    for number, line in matching:
        stream.write(f"{number}: {line}\n")

print(f"parsed_jsonl_lines={line_total}")
print(f"selected_trace_events={len(selected)}")
print(f"read_codex_output_lines={output_line_count}")
print(f"keylines={len(matching)}")
print(f"summary={SUMMARY}")
print(f"keylines_file={KEYLINES}")
