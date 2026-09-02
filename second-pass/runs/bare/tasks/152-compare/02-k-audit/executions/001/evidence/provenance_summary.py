#!/usr/bin/env python3
"""Summarize untrusted generation records without executing their contents."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


CANDIDATE = Path("/candidate")
TRACE = next((CANDIDATE / "codex-trace").rglob("*.jsonl"))
FILES = [
    CANDIDATE / "run-input.json",
    CANDIDATE / "metrics.json",
    CANDIDATE / "codex-last.txt",
    CANDIDATE / "codex-output.log",
    TRACE,
]

for path in FILES:
    data = path.read_bytes()
    print(
        f"FILE {path}: bytes={len(data)} lines={data.count(bytes([10]))} "
        f"sha256={hashlib.sha256(data).hexdigest()}"
    )

run_input = json.loads((CANDIDATE / "run-input.json").read_text())
metrics = json.loads((CANDIDATE / "metrics.json").read_text())
print("RUN_INPUT:", json.dumps(run_input, sort_keys=True))
print("METRICS:", json.dumps(metrics, sort_keys=True))

log_text = (CANDIDATE / "codex-output.log").read_text(errors="replace")
for marker in ["#Top", "KPROVE_PASSED", "kompile", "kprove", "krun"]:
    print(f"CODEX_OUTPUT_OCCURRENCES {marker!r}: {log_text.count(marker)}")

record_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
tool_results: collections.Counter[str] = collections.Counter()
final_messages: list[str] = []
with TRACE.open() as source:
    for line_number, line in enumerate(source, 1):
        record = json.loads(line)
        record_types[str(record.get("type"))] += 1
        payload = record.get("payload")
        if isinstance(payload, dict):
            payload_types[str(payload.get("type"))] += 1
            if payload.get("type") == "function_call_output":
                output = str(payload.get("output", ""))
                for status in ["exit_code", "Process exited with code 0", "#Top"]:
                    if status in output:
                        tool_results[status] += 1
            if payload.get("type") == "message" and payload.get("role") == "assistant":
                texts = [
                    item.get("text", "")
                    for item in payload.get("content", [])
                    if isinstance(item, dict) and item.get("type") == "output_text"
                ]
                if texts:
                    final_messages.append("\n".join(texts))

print("TRACE_RECORD_TYPES:", dict(sorted(record_types.items())))
print("TRACE_PAYLOAD_TYPES:", dict(sorted(payload_types.items())))
print("TRACE_TOOL_RESULT_MARKERS:", dict(sorted(tool_results.items())))
print("TRACE_ASSISTANT_MESSAGES:", len(final_messages))
if final_messages:
    print("TRACE_LAST_ASSISTANT_MESSAGE:", final_messages[-1])
