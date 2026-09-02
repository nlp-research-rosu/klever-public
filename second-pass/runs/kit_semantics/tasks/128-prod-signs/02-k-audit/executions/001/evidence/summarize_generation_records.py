#!/usr/bin/env python3
"""Stream and summarize every required pipeline-v3 generation record."""

from __future__ import annotations

import collections
import json
from pathlib import Path


ROOT = Path("/generation-evidence")
TRACE = ROOT / (
    "codex-trace/2026/07/25/"
    "rollout-2026-07-25T02-42-31-019f9839-c891-7582-ba7d-29d91c2aeab9.jsonl"
)

for path in [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    ROOT / "invocation.json",
    ROOT / "metrics.json",
    ROOT / "runtime-metrics.json",
    ROOT / "usage.json",
]:
    document = json.loads(path.read_text())
    print(f"JSON_RECORD={path} KEYS={','.join(sorted(document))}")
    if "status" in document:
        print(f"  STATUS={document['status']}")
    if "exit_code" in document:
        print(f"  EXIT_CODE={document['exit_code']}")

for path in [ROOT / "prompt.txt", ROOT / "codex-last.txt"]:
    content = path.read_text()
    print(f"TEXT_RECORD={path} LINES={len(content.splitlines())} BYTES={len(content.encode())}")
    print(content.rstrip())

output = ROOT / "codex-output.log"
output_lines = 0
output_markers = collections.Counter()
markers = [
    "#Top",
    "WarnStuckClaimState",
    "kompile",
    "kprove",
    "VALIDATED",
    "KPROVE_PASSED",
]
with output.open(errors="replace") as stream:
    for output_lines, line in enumerate(stream, 1):
        for marker in markers:
            output_markers[marker] += line.count(marker)
print(
    f"TEXT_RECORD={output} LINES={output_lines} BYTES={output.stat().st_size} "
    f"MARKERS={dict(output_markers)}"
)

top_types = collections.Counter()
payload_types = collections.Counter()
call_names = collections.Counter()
assistant_messages = 0
trace_lines = 0
for trace_lines, line in enumerate(TRACE.open(), 1):
    record = json.loads(line)
    top_types[record.get("type")] += 1
    payload = record.get("payload") or {}
    payload_types[payload.get("type")] += 1
    if payload.get("type") in {"function_call", "custom_tool_call"}:
        call_names[payload.get("name", "<unnamed>")] += 1
    if payload.get("type") in {"agent_message", "message"}:
        assistant_messages += int(payload.get("role", "assistant") == "assistant")

print(f"TRACE_RECORD={TRACE} LINES={trace_lines} ALL_JSON=true")
print(f"TRACE_TOP_TYPES={dict(top_types)}")
print(f"TRACE_PAYLOAD_TYPES={dict(payload_types)}")
print(f"TRACE_CALL_NAMES={dict(call_names)}")
print(f"TRACE_ASSISTANT_MESSAGE_EVENTS={assistant_messages}")
print("GENERATION_RECORDS_READ=PASS")
