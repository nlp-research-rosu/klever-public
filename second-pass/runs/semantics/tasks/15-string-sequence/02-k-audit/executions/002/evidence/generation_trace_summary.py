#!/usr/bin/env python3
"""Validate and summarize every JSONL record in the untrusted generation trace."""

from __future__ import annotations

import collections
import json
from pathlib import Path


trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
assert len(trace_files) == 1

top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
roles: collections.Counter[str] = collections.Counter()
call_inputs: list[str] = []
output_texts: list[str] = []

with trace_files[0].open() as stream:
    for line_count, line in enumerate(stream, 1):
        record = json.loads(line)
        top_types[str(record.get("type"))] += 1
        payload = record.get("payload", {})
        payload_types[str(payload.get("type"))] += 1
        if payload.get("role") is not None:
            roles[str(payload["role"])] += 1
        if payload.get("type") == "custom_tool_call":
            call_inputs.append(str(payload.get("input") or payload.get("arguments") or ""))
        if payload.get("type") == "custom_tool_call_output":
            output_texts.append(str(payload.get("output") or ""))

print(f"trace_file={trace_files[0]}")
print(f"json_lines={line_count} malformed=0")
print(f"top_types={dict(top_types)}")
print(f"payload_types={dict(payload_types)}")
print(f"roles={dict(roles)}")
print(f"tool_calls={len(call_inputs)} tool_outputs={len(output_texts)}")
print(f"call_records_mentioning_kompile={sum('kompile ' in item for item in call_inputs)}")
print(f"call_records_mentioning_kprove={sum('kprove ' in item for item in call_inputs)}")
print(f"output_records_containing_top={sum('#Top' in item for item in output_texts)}")
print(
    "output_records_containing_stuck="
    f"{sum('WarnStuckClaimState' in item for item in output_texts)}"
)
