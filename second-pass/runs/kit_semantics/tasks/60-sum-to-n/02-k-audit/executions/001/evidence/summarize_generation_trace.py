#!/usr/bin/env python3
"""Bounded structural review of the untrusted generation trace and text log."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


trace = Path(
    "/generation-evidence/codex-trace/2026/07/29/"
    "rollout-2026-07-29T09-23-11-019fae42-09bd-7633-b7cc-c2617702bfca.jsonl"
)
outer = Counter()
payloads = Counter()
calls = []
assistant_messages = []

for line_number, line in enumerate(trace.open(), 1):
    event = json.loads(line)
    outer[event.get("type", "<none>")] += 1
    payload = event.get("payload")
    if not isinstance(payload, dict):
        continue
    payload_type = payload.get("type", "<none>")
    payloads[payload_type] += 1
    if payload_type == "function_call":
        name = payload.get("name", "<none>")
        arguments = payload.get("arguments", "")
        try:
            parsed = json.loads(arguments)
        except (TypeError, ValueError):
            parsed = {}
        if name == "exec_command":
            detail = str(parsed.get("cmd", "")).replace("\n", " ")[:500]
        else:
            detail = str(arguments).replace("\n", " ")[:500]
        calls.append((line_number, name, detail))
    if payload_type == "message" and payload.get("role") == "assistant":
        pieces = []
        for item in payload.get("content", []):
            if isinstance(item, dict) and item.get("type") == "output_text":
                pieces.append(item.get("text", ""))
        if pieces:
            assistant_messages.append((line_number, "\n".join(pieces)))

print(f"trace_lines={sum(outer.values())}")
print(f"outer_types={dict(sorted(outer.items()))}")
print(f"payload_types={dict(sorted(payloads.items()))}")
print(f"function_calls={len(calls)}")
for line_number, name, detail in calls:
    print(f"CALL line={line_number} name={name} detail={detail}")

print(f"assistant_messages={len(assistant_messages)}")
for line_number, message in assistant_messages:
    # Final/status prose is untrusted; keep a bounded, single-line rendering.
    bounded = " ".join(message.split())[:1200]
    print(f"ASSISTANT line={line_number} text={bounded}")

output = Path("/generation-evidence/codex-output.log").read_text()
print(f"codex_output_lines={len(output.splitlines())}")
for marker in (
    "kprove spec.k",
    "#Top",
    "WarnStuckClaimState",
    "VALIDATED",
    "RESULT: KPROVE_PASSED",
):
    print(f"codex_output_marker={marker!r} count={output.count(marker)}")

print("GENERATION_TRACE_SUMMARY_PASS")
