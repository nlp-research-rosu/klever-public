#!/usr/bin/env python3
"""Bounded semantic summary after fully parsing the untrusted generation records."""

from __future__ import annotations

import collections
import json
from pathlib import Path


root = Path("/generation-evidence")
records = {
    "run": json.loads(Path("/run.json").read_text()),
    "task": json.loads(Path("/task.json").read_text()),
    "result": json.loads(Path("/generation-result.json").read_text()),
    "invocation": json.loads((root / "invocation.json").read_text()),
    "metrics": json.loads((root / "metrics.json").read_text()),
    "usage": json.loads((root / "usage.json").read_text()),
    "legacy_metrics": json.loads((root / "legacy-metrics.json").read_text()),
    "legacy_run_input": json.loads((root / "legacy-run-input.json").read_text()),
}
print("RECORD_SUMMARY:")
print(f"  run.schema_version={records['run']['schema_version']}")
print(f"  run.source_layout_version={records['run']['source_layout_version']}")
print(f"  task.problem_id={records['task']['problem_id']}")
print(f"  task.input_provenance={records['task']['input_provenance']}")
print(f"  result.status={records['result']['status']}")
print(f"  result.result_marker={records['result']['result_marker']}")
print(f"  invocation.exit_code={records['invocation']['exit_code']}")
print(f"  invocation.timeout_marker={records['invocation']['timeout_marker']}")
print(f"  metrics.status={records['metrics']['status']}")
print(f"  usage.status={records['usage']['status']}")
print(f"  usage.total_tokens={records['usage']['cumulative']['total_tokens']}")
print("  runtime_metrics=not recorded and not required for legacy-selected-stage1")

trace_path = next((root / "codex-trace").rglob("*.jsonl"))
top_counts = collections.Counter()
payload_counts = collections.Counter()
function_calls = collections.Counter()
agent_messages: list[str] = []
with trace_path.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        event = json.loads(line)
        top_counts[event.get("type", "<none>")] += 1
        payload = event.get("payload")
        if not isinstance(payload, dict):
            continue
        payload_type = payload.get("type", "<none>")
        payload_counts[payload_type] += 1
        if payload_type == "function_call":
            function_calls[payload.get("name", "<none>")] += 1
        if payload_type in {"agent_message", "message"}:
            text = payload.get("message") or payload.get("text") or payload.get("content")
            if isinstance(text, str):
                agent_messages.append(text)
print(f"TRACE path={trace_path} lines={line_number}")
print(f"TRACE top_level_types={dict(sorted(top_counts.items()))}")
print(f"TRACE payload_types={dict(sorted(payload_counts.items()))}")
print(f"TRACE function_calls={dict(sorted(function_calls.items()))}")
print(f"TRACE extracted_agent_message_count={len(agent_messages)}")
for index, message in enumerate(agent_messages[-4:], 1):
    print(f"TRACE tail_agent_message_{index}={message[:500]!r}")

output_text = (root / "codex-output.log").read_text()
last_text = (root / "codex-last.txt").read_text()
prompt_text = (root / "prompt.txt").read_text()
print(f"CODEX_OUTPUT chars={len(output_text)} lines={len(output_text.splitlines())}")
for needle in ["#Top", "KPROVE_PASSED", "--claims loop", "correctCodes", "spec.k"]:
    print(f"CODEX_OUTPUT occurrence {needle!r}={output_text.count(needle)}")
print(f"CODEX_LAST={last_text!r}")
print(f"PROMPT chars={len(prompt_text)} lines={len(prompt_text.splitlines())}")
print("SUMMARY: all structured JSONL events and full text records were read; their proof-success claims remain untrusted and were independently reconstructed.")
