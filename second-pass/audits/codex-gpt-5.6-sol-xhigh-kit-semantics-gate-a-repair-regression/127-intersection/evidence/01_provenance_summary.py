#!/usr/bin/env python3
"""Bounded summary of untrusted candidate-generation claims."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


CANDIDATE = Path("/candidate")
TRACE = next((CANDIDATE / "codex-trace").rglob("*.jsonl"))
FILES = [
    CANDIDATE / "run-input.json",
    CANDIDATE / "metrics.json",
    CANDIDATE / "codex-last.txt",
    CANDIDATE / "codex-output.log",
    TRACE,
]


def bounded(value: object, limit: int = 400) -> str:
    text = str(value).replace("\n", "\\n")
    return text if len(text) <= limit else text[:limit] + "...[truncated]"


print("All content summarized below is UNTRUSTED candidate-generation evidence.")
for path in FILES:
    data = path.read_bytes()
    print(
        f"FILE path={path} bytes={len(data)} lines={data.count(bytes([10]))} "
        f"sha256={hashlib.sha256(data).hexdigest()}"
    )

print("\nrun-input.json:")
print(json.dumps(json.loads((CANDIDATE / "run-input.json").read_text()), indent=2))
print("\nmetrics.json:")
print(json.dumps(json.loads((CANDIDATE / "metrics.json").read_text()), indent=2))
print("\ncodex-last.txt:")
print((CANDIDATE / "codex-last.txt").read_text())

top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
roles: collections.Counter[str] = collections.Counter()
function_outputs: list[tuple[int, str]] = []
final_messages: list[str] = []
malformed = 0

with TRACE.open() as stream:
    for line_number, line in enumerate(stream, 1):
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            malformed += 1
            continue
        top_types[str(event.get("type", "<missing>"))] += 1
        payload = event.get("payload")
        if isinstance(payload, dict):
            payload_types[str(payload.get("type", "<missing>"))] += 1
            if "role" in payload:
                roles[str(payload["role"])] += 1
            if payload.get("type") == "function_call_output":
                output = str(payload.get("output", ""))
                function_outputs.append((line_number, bounded(output)))
            if payload.get("type") in {"agent_message", "task_complete"}:
                message = payload.get("message") or payload.get("last_agent_message")
                if message:
                    final_messages.append(bounded(message, 1_000))

print("\nStructured trace parse:")
print(f"path={TRACE}")
print(f"malformed_json_lines={malformed}")
print(f"top_level_types={dict(sorted(top_types.items()))}")
print(f"payload_types={dict(sorted(payload_types.items()))}")
print(f"roles={dict(sorted(roles.items()))}")
print(f"function_call_output_count={len(function_outputs)}")
print("last_five_function_outputs:")
for line_number, output in function_outputs[-5:]:
    print(f"  line={line_number} output={output}")
print("final_agent_claims:")
for message in final_messages[-3:]:
    print(f"  {message}")

log_lines = (CANDIDATE / "codex-output.log").read_text(errors="replace").splitlines()
needles = (
    "#Top",
    "EXPECTED FAILURE",
    "mismatches: 0",
    "proof body identity",
    "KPROVE_PASSED",
    "VALIDATED",
)
matches = [
    (line_number, line)
    for line_number, line in enumerate(log_lines, 1)
    if any(needle in line for needle in needles)
]
print("\ncodex-output.log claim matches (last 40, each bounded):")
for line_number, line in matches[-40:]:
    print(f"  {line_number}: {bounded(line, 500)}")
