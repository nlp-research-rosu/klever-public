#!/usr/bin/env python3
"""Validate and summarize every generation trace/transcript record."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
print(f"trace_file_count={len(trace_files)}")

for trace in trace_files:
    raw_lines = trace.read_text().splitlines()
    top_types = Counter()
    payload_types = Counter()
    tool_calls = []
    tool_outputs = []
    final_messages = []
    for line_number, raw in enumerate(raw_lines, 1):
        event = json.loads(raw)
        top_type = event.get("type", "<missing>")
        top_types[top_type] += 1
        payload = event.get("payload")
        if isinstance(payload, dict):
            payload_type = payload.get("type")
            if payload_type is not None:
                payload_types[str(payload_type)] += 1
            if top_type == "response_item" and payload_type == "custom_tool_call":
                tool_calls.append(
                    (
                        line_number,
                        payload.get("name"),
                        str(payload.get("input", "")),
                    )
                )
            if top_type == "response_item" and payload_type == "custom_tool_call_output":
                tool_outputs.append(
                    (
                        line_number,
                        payload.get("call_id"),
                        json.dumps(payload.get("output"), sort_keys=True),
                    )
                )
            if top_type == "event_msg" and payload_type in {
                "agent_message",
                "task_complete",
            }:
                final_messages.append((line_number, payload_type, payload))

    print()
    print(f"TRACE {trace}")
    print(f"line_count={len(raw_lines)}")
    print(
        "top_types="
        + ",".join(f"{key}:{value}" for key, value in sorted(top_types.items()))
    )
    print(
        "payload_types="
        + ",".join(
            f"{key}:{value}" for key, value in sorted(payload_types.items())
        )
    )
    print(f"tool_call_count={len(tool_calls)} tool_output_count={len(tool_outputs)}")

    print("TOOL_CALLS")
    for line_number, name, content in tool_calls:
        digest = hashlib.sha256(content.encode()).hexdigest()
        bounded = content if len(content) <= 3000 else content[:1500] + "\n...[bounded]...\n" + content[-1500:]
        print(
            f"line={line_number} name={name} bytes={len(content)} sha256={digest}\n"
            f"{bounded}"
        )

    print("TOOL_OUTPUTS")
    for line_number, call_id, content in tool_outputs:
        digest = hashlib.sha256(content.encode()).hexdigest()
        bounded = content if len(content) <= 2000 else content[:1000] + "\n...[bounded]...\n" + content[-1000:]
        print(
            f"line={line_number} call_id={call_id} bytes={len(content)} "
            f"sha256={digest}\n{bounded}"
        )

    print("FINAL_MESSAGES")
    for line_number, payload_type, payload in final_messages:
        print(
            f"line={line_number} payload_type={payload_type} "
            f"payload={json.dumps(payload, sort_keys=True)}"
        )

transcript = Path("/generation-evidence/codex-output.log")
lines = transcript.read_text(errors="replace").splitlines()
markers = Counter()
interesting = []
needles = (
    "kompile ",
    "kprove ",
    "krun ",
    "#Top",
    "RESULT:",
    "succeeded in ",
    "failed in ",
    "Warning",
    "Error",
)
for number, line in enumerate(lines, 1):
    if line in {"user", "codex", "exec", "apply_patch"}:
        markers[line] += 1
    if any(needle in line for needle in needles):
        interesting.append((number, line))

print()
print(f"TRANSCRIPT {transcript}")
print(f"line_count={len(lines)}")
print(
    "marker_counts="
    + ",".join(f"{key}:{value}" for key, value in sorted(markers.items()))
)
print(f"interesting_line_count={len(interesting)}")
for number, line in interesting:
    print(f"{number}: {line}")
