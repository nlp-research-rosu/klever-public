#!/usr/bin/env python3
"""Parse every required legacy-selected-stage1 generation record."""

from __future__ import annotations

import hashlib
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
    root / "legacy-metrics.json",
    root / "legacy-run-input.json",
]
for path in json_records:
    obj = json.loads(path.read_text(encoding="utf-8"))
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    print(
        f"JSON_OK path={path} bytes={path.stat().st_size} "
        f"sha256={digest} top_keys={sorted(obj)}"
    )

for path in [
    root / "codex-last.txt",
    root / "codex-output.log",
    root / "prompt.txt",
]:
    text = path.read_text(encoding="utf-8")
    print(
        f"TEXT_OK path={path} chars={len(text)} lines={len(text.splitlines())} "
        f"sha256={hashlib.sha256(path.read_bytes()).hexdigest()} "
        f"top_markers={{'#Top': {text.count('#Top')}, "
        f"'$proofPath': {text.count('$proofPath')}, "
        f"'RESULT: KPROVE_PASSED': {text.count('RESULT: KPROVE_PASSED')}}}"
    )

trace = next((root / "codex-trace").rglob("*.jsonl"))
outer_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
calls: list[tuple[int, str, str]] = []
with trace.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        event = json.loads(line)
        outer_types[event.get("type", "<none>")] += 1
        payload = event.get("payload")
        if isinstance(payload, dict):
            payload_type = payload.get("type", "<none>")
            payload_types[payload_type] += 1
            if payload_type in {"function_call", "custom_tool_call"}:
                raw = payload.get("arguments") or payload.get("input") or ""
                calls.append((line_number, str(payload.get("name")), str(raw)))
        else:
            payload_types["<none>"] += 1

print(
    f"TRACE_OK path={trace} lines={line_number} "
    f"sha256={hashlib.sha256(trace.read_bytes()).hexdigest()}"
)
print("TRACE_OUTER_TYPES", dict(sorted(outer_types.items())))
print("TRACE_PAYLOAD_TYPES", dict(sorted(payload_types.items())))
print("TRACE_TOOL_CALLS", len(calls))
for line_number, name, raw in calls:
    normalized = " ".join(raw.split())
    print(
        f"TRACE_CALL line={line_number} name={name} "
        f"args_sha256={hashlib.sha256(raw.encode()).hexdigest()} "
        f"args_prefix={normalized[:240]!r}"
    )
