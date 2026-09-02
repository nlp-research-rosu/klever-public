#!/usr/bin/env python3
"""Bounded structural inspection of the complete generation trace/log."""

from __future__ import annotations

import collections
import json
from pathlib import Path


trace = next(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
counts: collections.Counter[str] = collections.Counter()
tool_calls = []
json_errors = []
line_count = 0
for line_count, line in enumerate(trace.open(), 1):
    try:
        event = json.loads(line)
    except Exception as err:
        json_errors.append((line_count, type(err).__name__, str(err)))
        continue
    counts["event:" + str(event.get("type", "<none>"))] += 1
    payload = event.get("payload")
    if isinstance(payload, dict):
        payload_type = payload.get("type")
        if payload_type:
            counts["payload:" + str(payload_type)] += 1
        if payload_type == "function_call":
            name = str(payload.get("name", ""))
            arguments = str(payload.get("arguments", ""))
            tool_calls.append((line_count, name, arguments))

print("trace:", trace)
print("trace_lines_scanned:", line_count)
print("json_errors:", json_errors)
print("event_counts:")
for key, value in sorted(counts.items()):
    print(f"  {key}: {value}")
print("tool_calls:")
for line_number, name, arguments in tool_calls:
    compact = " ".join(arguments.split())
    print(f"  line={line_number} name={name} arguments={compact[:600]}")

output_log = Path("/generation-evidence/codex-output.log")
output_lines = output_log.read_text(errors="replace").splitlines()
print("codex_output_lines_scanned:", len(output_lines))
for needle in ("#Top", "kprove", "kompile", "RESULT: KPROVE_PASSED"):
    matches = [index + 1 for index, line in enumerate(output_lines) if needle in line]
    print(f"codex_output_occurrences[{needle!r}]: count={len(matches)} lines={matches[:40]}")

assert not json_errors
assert line_count == 255
print("GENERATION_TRACE_SCAN: PASS")
