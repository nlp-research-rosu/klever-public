#!/usr/bin/env python3
"""Bounded inspection of all required pipeline-v3 generation records."""

from __future__ import annotations

import json
from pathlib import Path


json_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation/invocation.json"),
    Path("/generation/metrics.json"),
    Path("/generation/runtime-metrics.json"),
    Path("/generation/usage.json"),
]
for path in json_records:
    obj = json.loads(path.read_text(encoding="utf-8"))
    print(f"JSON_RECORD {path} keys={sorted(obj)}")
    for key in (
        "schema_version",
        "status",
        "stage",
        "condition",
        "problem_id",
        "exit_code",
        "oom_killed",
        "timeout_marker",
        "inputs",
        "outputs",
    ):
        if key in obj:
            rendered = json.dumps(obj[key], sort_keys=True)
            print(f"  {key}={rendered[:1500]}")

for path in (
    Path("/generation/codex-last.txt"),
    Path("/generation/prompt.txt"),
):
    text = path.read_text(encoding="utf-8")
    print(f"TEXT_RECORD {path} chars={len(text)} lines={len(text.splitlines())}")
    print(text[:4500])

output = Path("/generation/codex-output.log").read_text(encoding="utf-8")
print(
    "CODEX_OUTPUT",
    f"chars={len(output)}",
    f"lines={len(output.splitlines())}",
    f"top_mentions={output.count('#Top')}",
    f"kprove_mentions={output.count('kprove')}",
    f"expected_failure_mentions={output.count('EXPECTED_FAILURE')}",
)
for marker in (
    "inputs=1521 mismatches=0",
    "BODY_MUTATION_EXIT=1",
    "VACUITY_EXIT=1",
    "RESULT: KPROVE_PASSED",
):
    positions = [i + 1 for i, line in enumerate(output.splitlines()) if marker in line]
    print("CODEX_OUTPUT_MARKER", marker, positions[:20])

trace = Path(
    "/generation/codex-trace/2026/07/24/"
    "rollout-2026-07-24T22-25-55-019f974e-dac3-7be2-961b-a3bf7b11aa27.jsonl"
)
for lineno, raw in enumerate(trace.open(encoding="utf-8"), 1):
    obj = json.loads(raw)
    payload = obj.get("payload")
    if not isinstance(payload, dict):
        continue
    ptype = payload.get("type")
    if ptype == "function_call":
        name = payload.get("name")
        args = payload.get("arguments", "")
        if any(token in args for token in ("kompile", "kprove", "./prove.sh")):
            print(f"TRACE_CALL line={lineno} name={name} args={args[:2000]}")
    elif ptype in ("agent_message", "task_complete"):
        message = payload.get("message") or payload.get("last_agent_message") or ""
        if any(token in message for token in ("#Top", "Gate A", "KPROVE_PASSED")):
            print(f"TRACE_CLAIM line={lineno} type={ptype} message={message[:2000]}")

