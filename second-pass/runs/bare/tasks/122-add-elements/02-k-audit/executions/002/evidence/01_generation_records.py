#!/usr/bin/env python3
"""Bounded inspection of every generation transcript/trace record."""

from __future__ import annotations

import json
import re
from pathlib import Path


root = Path("/generation-evidence")
output_lines = (root / "codex-output.log").read_text(errors="replace").splitlines()
patterns = re.compile(
    r"/bin/bash -lc|#Top|WarnStuckClaimState|RESULT:|KPROVE_PASSED|"
    r"final prove\.sh|kprove spec\.k"
)
selected = [(number, line) for number, line in enumerate(output_lines, 1)
            if patterns.search(line)]
print(
    f"codex-output.log lines={len(output_lines)} selected_claim_or_command_lines={len(selected)}"
)
for number, line in selected[:300]:
    print(f"codex-output:{number}: {line[:1200]}")
if len(selected) > 300:
    print(f"codex-output: omitted_selected_lines={len(selected) - 300}")

events = 0
tool_calls = 0
agent_messages = 0
for trace in sorted((root / "codex-trace").rglob("*.jsonl")):
    for line_number, line in enumerate(trace.read_text(errors="strict").splitlines(), 1):
        item = json.loads(line)
        events += 1
        payload = item.get("payload", {})
        subtype = payload.get("type")
        if item.get("type") == "response_item" and subtype in {
            "custom_tool_call",
            "function_call",
        }:
            tool_calls += 1
            name = payload.get("name", "")
            raw = payload.get("input", payload.get("arguments", ""))
            if not isinstance(raw, str):
                raw = json.dumps(raw, sort_keys=True)
            print(
                f"trace-tool-call {trace.relative_to(root)}:{line_number} "
                f"name={name} input={raw[:1800]!r}"
            )
        elif (
            item.get("type") == "event_msg"
            and subtype in {"agent_message", "task_complete"}
        ):
            agent_messages += 1
            text = payload.get("message", payload.get("last_agent_message", ""))
            print(
                f"trace-agent-record {trace.relative_to(root)}:{line_number} "
                f"type={subtype} text={str(text)[:1800]!r}"
            )
print(
    f"trace_records_parsed={events} tool_calls_inspected={tool_calls} "
    f"agent_records_inspected={agent_messages}"
)
