#!/usr/bin/env python3
"""Bounded semantic summary of every required pipeline-v3 generation record."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


json_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
]
for path in json_records:
    value = json.loads(path.read_text())
    print(f"{path}:")
    if path.name == "run.json":
        print(
            json.dumps(
                {
                    "schema_version": value["schema_version"],
                    "run_id": value["run_id"],
                    "config": value["config"],
                    "condition": value["condition"],
                    "model": value["model"],
                    "task_present": "82-prime-length" in value["tasks"],
                    "runtime": value["runtime"],
                },
                sort_keys=True,
            )
        )
    elif path.name == "task.json":
        print(json.dumps(value, sort_keys=True))
    elif path.name == "generation-result.json":
        print(
            json.dumps(
                {
                    "schema_version": value["schema_version"],
                    "stage": value["stage"],
                    "status": value["status"],
                    "invocation": value["invocation"],
                    "session_id": value["session_id"],
                    "outputs": value["outputs"],
                },
                sort_keys=True,
            )
        )
    elif path.name == "invocation.json":
        print(
            json.dumps(
                {
                    "schema_version": value["schema_version"],
                    "name": value["name"],
                    "kind": value["kind"],
                    "status": value["status"],
                    "exit_code": value["exit_code"],
                    "session_id": value["session_id"],
                    "inputs": value["inputs"],
                    "outputs": value["outputs"],
                },
                sort_keys=True,
            )
        )
    else:
        print(json.dumps(value, sort_keys=True))

prompt = Path("/generation-evidence/prompt.txt").read_text()
last = Path("/generation-evidence/codex-last.txt").read_text()
output = Path("/generation-evidence/codex-output.log").read_text(
    encoding="utf-8", errors="replace"
)
print(
    "/generation-evidence/prompt.txt: "
    f"{len(prompt.splitlines())} lines, deliverables="
    f"{all(name in prompt for name in ['solution.py', 'solution.mpy', 'verification.k', 'spec.k', 'PROOF.md'])}"
)
print("/generation-evidence/codex-last.txt:")
print(last.rstrip())
print(
    "/generation-evidence/codex-output.log: "
    f"{len(output.splitlines())} lines, {len(output.encode())} bytes"
)
for marker in (
    "kompile",
    "kprove",
    "#Top",
    "WarnStuckClaimState",
    "VALIDATED",
    "KPROVE_PASSED",
):
    print(f"codex-output occurrences {marker!r}: {output.count(marker)}")

trace_paths = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
function_names: Counter[str] = Counter()
custom_names: Counter[str] = Counter()
agent_messages: list[str] = []
event_types: Counter[str] = Counter()
for path in trace_paths:
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            record = json.loads(line)
            payload = record.get("payload", {})
            payload_type = payload.get("type") if isinstance(payload, dict) else None
            event_types[str(payload_type)] += 1
            if payload_type == "function_call":
                function_names[str(payload.get("name"))] += 1
            elif payload_type == "custom_tool_call":
                custom_names[str(payload.get("name"))] += 1
            elif payload_type == "agent_message":
                message = payload.get("message")
                if isinstance(message, str):
                    agent_messages.append(message)
            elif payload_type == "message" and payload.get("role") == "assistant":
                text_parts = [
                    part.get("text", "")
                    for part in payload.get("content", [])
                    if isinstance(part, dict) and part.get("type") in {"output_text", "text"}
                ]
                if text_parts:
                    agent_messages.append("\n".join(text_parts))
print(f"structured trace files: {len(trace_paths)}")
print(f"structured trace payload counts: {dict(sorted(event_types.items()))}")
print(f"structured trace function calls: {dict(sorted(function_names.items()))}")
print(f"structured trace custom calls: {dict(sorted(custom_names.items()))}")
print(f"structured trace assistant/agent messages: {len(agent_messages)}")
if agent_messages:
    bounded = agent_messages[-1]
    print("structured trace final assistant/agent message:")
    print(bounded[:2000])
