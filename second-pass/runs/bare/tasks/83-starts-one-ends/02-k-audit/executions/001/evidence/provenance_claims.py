#!/usr/bin/env python3
"""Read all untrusted generation records and emit a bounded claim summary."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


candidate = Path("/candidate")
trace_path = (
    candidate
    / "codex-trace/2026/07/22/"
    / "rollout-2026-07-22T05-55-05-019f8977-00e7-74e3-8113-548ceabd44ea.jsonl"
)

run_input_text = (candidate / "run-input.json").read_text(encoding="utf-8")
metrics_text = (candidate / "metrics.json").read_text(encoding="utf-8")
last_text = (candidate / "codex-last.txt").read_text(encoding="utf-8")
output_text = (candidate / "codex-output.log").read_text(encoding="utf-8")
trace_text = trace_path.read_text(encoding="utf-8")

run_input = json.loads(run_input_text)
metrics = json.loads(metrics_text)

trace_top_types: Counter[str] = Counter()
trace_payload_types: Counter[str] = Counter()
bad_trace_lines = []
function_calls = []
final_messages = []
for line_number, line in enumerate(trace_text.splitlines(), 1):
    try:
        item = json.loads(line)
    except Exception as err:  # evidence parsing must expose malformed records
        bad_trace_lines.append({"line": line_number, "error": str(err)})
        continue
    trace_top_types[str(item.get("type"))] += 1
    payload = item.get("payload")
    if isinstance(payload, dict):
        payload_type = str(payload.get("type"))
        trace_payload_types[payload_type] += 1
        if payload_type in {"function_call", "custom_tool_call"}:
            function_calls.append(
                {"line": line_number, "name": payload.get("name")}
            )
        if payload_type in {"message", "agent_message"}:
            content = payload.get("content") or payload.get("message")
            if content:
                final_messages.append(
                    {
                        "line": line_number,
                        "role": payload.get("role"),
                        "content": content,
                    }
                )

claim_lines = [
    line
    for line in output_text.splitlines()
    if (
        "#Top" in line
        or "RESULT:" in line
        or "K execution produced" in line
        or "kprove" in line and "exited" in line
    )
]

summary = {
    "warning": "All fields below are untrusted candidate-generation claims.",
    "run_input": run_input,
    "metrics": metrics,
    "codex_last_bytes": len(last_text.encode()),
    "codex_last": last_text,
    "codex_output": {
        "bytes_read": len(output_text.encode()),
        "lines_read": len(output_text.splitlines()),
        "reported_success_tokens": len(re.findall(r"\\bsucceeded\\b", output_text)),
        "reported_failure_tokens": len(re.findall(r"\\bfailed\\b", output_text)),
        "bounded_claim_lines": claim_lines[-20:],
    },
    "structured_trace": {
        "path": str(trace_path),
        "bytes_read": len(trace_text.encode()),
        "lines_read": len(trace_text.splitlines()),
        "top_types": dict(trace_top_types),
        "payload_types": dict(trace_payload_types),
        "bad_json_lines": bad_trace_lines,
        "function_call_count": len(function_calls),
        "function_calls": function_calls,
        "last_message_records": final_messages[-3:],
    },
}
print(json.dumps(summary, indent=2, sort_keys=True))
raise SystemExit(1 if bad_trace_lines else 0)
