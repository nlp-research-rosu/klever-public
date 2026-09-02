#!/usr/bin/env python3
"""Parse the complete legacy-selected-stage1 structured generation record."""

from __future__ import annotations

import collections
import json
from pathlib import Path


root = Path("/generation-evidence")
trace_files = sorted((root / "codex-trace").rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
assert len(trace_files) == 1

rows = [json.loads(line) for line in trace_files[0].read_text().splitlines()]
counts = collections.Counter(
    (row.get("type"), row.get("payload", {}).get("type")) for row in rows
)
invocation = json.loads((root / "invocation.json").read_text())
metrics = json.loads((root / "metrics.json").read_text())
usage = json.loads((root / "usage.json").read_text())
result = json.loads(Path("/generation-result.json").read_text())
task = json.loads(Path("/task.json").read_text())
run = json.loads(Path("/run.json").read_text())

session_meta = next(row for row in rows if row["type"] == "session_meta")
task_complete = next(
    row
    for row in rows
    if row["type"] == "event_msg"
    and row.get("payload", {}).get("type") == "task_complete"
)
selected = usage["selected_event"]
selected_row = rows[selected["line_number"] - 1]

assert session_meta["payload"]["session_id"] == invocation["session_id"]
assert invocation["session_id"] == result["session_id"]
assert task_complete["payload"]["last_agent_message"] == (
    root / "codex-last.txt"
).read_text()
assert selected_row["type"] == "event_msg"
assert selected_row["payload"]["type"] == "token_count"
assert invocation["status"] == metrics["status"] == result["status"] == "SUCCEEDED"
assert invocation["result_marker"] == result["result_marker"] == "KPROVE_PASSED"
assert task["problem_id"] == "33-sort-third"
assert task["condition"] == run["condition"]

output = (root / "codex-output.log").read_text(errors="strict")
assert "kprove spec.k --definition verification-kompiled --spec-module SPEC" in output
assert "RESULT: KPROVE_PASSED" in output

print(f"trace_file={trace_files[0]}")
print(f"trace_lines={len(rows)}")
for key, value in sorted(counts.items(), key=lambda item: str(item[0])):
    print(f"trace_count[{key}]={value}")
print(f"session_id={invocation['session_id']}")
print(f"invocation_exit_code={invocation['exit_code']}")
print(f"duration_s={metrics['duration_s']}")
print(f"usage_status={usage['status']}")
print(f"selected_usage_event={selected}")
print(f"generation_result={result['status']} marker={result['result_marker']}")
print("generation records parsed completely; claims remain untrusted")
