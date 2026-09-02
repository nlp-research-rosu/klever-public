#!/usr/bin/env python3
"""Read every structured-trace record and summarize untrusted generation claims."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path("/generation-evidence")
TRACE = ROOT / (
    "codex-trace/2026/07/29/"
    "rollout-2026-07-29T08-50-54-019fae24-7cdb-7a70-856a-b202f3a61f1e.jsonl"
)

outer = Counter()
payloads = Counter()
tool_calls = []
agent_messages = []
with TRACE.open(encoding="utf-8") as stream:
    for number, line in enumerate(stream, 1):
        item = json.loads(line)
        outer[item.get("type", "<none>")] += 1
        payload = item.get("payload")
        if not isinstance(payload, dict):
            continue
        payload_type = payload.get("type", "<none>")
        payloads[payload_type] += 1
        if payload_type in {"custom_tool_call", "function_call"}:
            name = payload.get("name", "<none>")
            raw_input = payload.get("input", payload.get("arguments", ""))
            if not isinstance(raw_input, str):
                raw_input = json.dumps(raw_input, sort_keys=True)
            compact = " ".join(raw_input.split())
            tool_calls.append((number, name, compact[:400]))
        if payload_type == "agent_message":
            agent_messages.append((number, " ".join(payload.get("message", "").split())))

output = (ROOT / "codex-output.log").read_text(encoding="utf-8")
last = (ROOT / "codex-last.txt").read_text(encoding="utf-8")
prompt = (ROOT / "prompt.txt").read_bytes()
print(f"trace_line_count={number}")
print(f"trace_outer_types={dict(sorted(outer.items()))}")
print(f"trace_payload_types={dict(sorted(payloads.items()))}")
print(f"tool_call_count={len(tool_calls)}")
for line_number, name, compact in tool_calls:
    print(f"tool_call line={line_number} name={name} input={compact}")
print(f"agent_message_count={len(agent_messages)}")
for line_number, message in agent_messages:
    print(f"agent_message line={line_number} text={message}")
print(f"codex_output_line_count={len(output.splitlines())}")
print(f"codex_output_top_marker_count={output.count('#Top')}")
print(f"codex_output_stuck_marker_count={output.count('WarnStuckClaimState')}")
print(f"codex_last_contains_kprove_passed={'RESULT: KPROVE_PASSED' in last}")
print(f"generation_prompt_sha256={hashlib.sha256(prompt).hexdigest()}")
print("GENERATION_RECORD_READ_STATUS=COMPLETE")
