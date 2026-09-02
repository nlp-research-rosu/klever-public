#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path

CANDIDATE = Path("/candidate")
TRACE = next((CANDIDATE / "codex-trace").glob("**/*.jsonl"))

run_input = json.loads((CANDIDATE / "run-input.json").read_text())
metrics = json.loads((CANDIDATE / "metrics.json").read_text())
last = (CANDIDATE / "codex-last.txt").read_text()
output = (CANDIDATE / "codex-output.log").read_text()
records = [json.loads(line) for line in TRACE.read_text().splitlines()]

record_types = Counter(
    (record.get("type"), record.get("payload", {}).get("type"))
    for record in records
)
tool_statuses = []
for record in records:
    payload = record.get("payload", {})
    if payload.get("type") != "custom_tool_call_output":
        continue
    for item in payload.get("output", []):
        if not isinstance(item, dict):
            continue
        text = item.get("text", "")
        if '"exit_code":' in text:
            tool_statuses.append(text)

print("UNTRUSTED_EVIDENCE_ONLY: true")
print(f"RUN_INPUT_PROBLEM_ID_CLAIM: {run_input.get('problem_id')}")
print(f"RUN_INPUT_CONDITION_CLAIM: {run_input.get('condition')}")
print(
    "METRICS_CLAIM:",
    json.dumps(
        {
            key: metrics.get(key)
            for key in ("agent", "model", "timeout_s", "duration_s", "exit_code", "timed_out")
        },
        sort_keys=True,
    ),
)
print(f"CODEX_LAST_HAS_KPROVE_PASSED: {'RESULT: KPROVE_PASSED' in last}")
print(f"CODEX_OUTPUT_TOP_COUNT: {output.count('#Top')}")
print(f"CODEX_OUTPUT_COMPILER_ERROR_COUNT: {output.count('[Error] Compiler')}")
print(f"TRACE_PATH: {TRACE}")
print(f"TRACE_RECORD_COUNT: {len(records)}")
for key, count in sorted(record_types.items(), key=str):
    print(f"TRACE_TYPE_COUNT: {key}={count}")
print(f"TRACE_TOOL_OUTPUTS_WITH_EXIT_STATUS: {len(tool_statuses)}")
task_complete = [
    record for record in records
    if record.get("payload", {}).get("type") == "task_complete"
]
print(f"TRACE_TASK_COMPLETE_COUNT: {len(task_complete)}")
if task_complete:
    final = task_complete[-1]["payload"].get("last_agent_message", "")
    print(f"TRACE_FINAL_CLAIMS_KPROVE_PASSED: {'RESULT: KPROVE_PASSED' in final}")
print(
    "NOTE: encrypted reasoning fields were treated as unreadable opaque data; "
    "readable messages, tool calls/outputs, patches, and completion records were inspected"
)
