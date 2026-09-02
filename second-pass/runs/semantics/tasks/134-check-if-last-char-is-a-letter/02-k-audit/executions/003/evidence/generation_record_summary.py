#!/usr/bin/env python3
"""Read and summarize every required legacy-selected-stage1 generation record."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


root = Path("/generation-evidence")
json_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    root / "invocation.json",
    root / "metrics.json",
    root / "usage.json",
]

for path in json_records:
    value = json.loads(path.read_text())
    print(
        f"json_ok path={path} top_type={type(value).__name__} "
        f"top_keys={','.join(sorted(value))}"
    )

for path in [
    root / "codex-last.txt",
    root / "codex-output.log",
    root / "prompt.txt",
]:
    text = path.read_text()
    print(
        f"text_read path={path} chars={len(text)} lines={len(text.splitlines())} "
        f"kprove_mentions={text.count('kprove')} top_mentions={text.count('#Top')}"
    )

trace_files = sorted((root / "codex-trace").rglob("*.jsonl"))
assert len(trace_files) == 1
trace = trace_files[0]
outer: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
tools: Counter[str] = Counter()
all_lines = trace.read_text().splitlines()
for line_number, line in enumerate(all_lines, 1):
    event = json.loads(line)
    outer[str(event.get("type"))] += 1
    payload = event.get("payload", {})
    payload_types[str(payload.get("type"))] += 1
    if payload.get("type") in {"function_call", "custom_tool_call"}:
        tools[str(payload.get("name"))] += 1

print(f"trace_jsonl_ok path={trace} lines={len(all_lines)}")
print(f"trace_outer_types={dict(sorted(outer.items()))}")
print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
print(f"trace_tool_names={dict(sorted(tools.items()))}")

last = (root / "codex-last.txt").read_text()
assert "RESULT: KPROVE_PASSED" in last
print("generation_claim_only=RESULT: KPROVE_PASSED")
