#!/usr/bin/env python3
"""Read and summarize every structured generation trace event and console log."""

from __future__ import annotations

import collections
import glob
import hashlib
import json
from pathlib import Path


def digest(text: str | bytes) -> str:
    if isinstance(text, str):
        text = text.encode()
    return hashlib.sha256(text).hexdigest()


trace_paths = sorted(glob.glob("/generation-evidence/codex-trace/**/*.jsonl", recursive=True))
print(f"trace_file_count={len(trace_paths)}")
event_counts: collections.Counter[str] = collections.Counter()
payload_counts: collections.Counter[str] = collections.Counter()
events = []
for trace_path in trace_paths:
    line_count = 0
    for line_number, line in enumerate(Path(trace_path).read_text().splitlines(), 1):
        event = json.loads(line)
        events.append((trace_path, line_number, event))
        line_count += 1
        event_counts[str(event.get("type"))] += 1
        payload = event.get("payload")
        if isinstance(payload, dict):
            payload_counts[str(payload.get("type"))] += 1
    print(
        f"trace={trace_path} lines={line_count} "
        f"sha256={digest(Path(trace_path).read_bytes())}"
    )
print(f"event_counts={dict(sorted(event_counts.items()))}")
print(f"payload_counts={dict(sorted(payload_counts.items()))}")

print("AGENT_AND_TASK_MESSAGES:")
for trace_path, line_number, event in events:
    payload = event.get("payload")
    if not isinstance(payload, dict):
        continue
    payload_type = payload.get("type")
    if payload_type in {"agent_message", "task_complete"}:
        text = payload.get("message", "")
        print(f"{line_number} {payload_type}: {text}")
    elif payload_type == "message" and payload.get("role") == "assistant":
        content = payload.get("content", [])
        text = "\n".join(
            str(item.get("text", ""))
            for item in content
            if isinstance(item, dict) and item.get("type") in {"output_text", "input_text"}
        )
        print(f"{line_number} assistant-message: {text}")

print("TOOL_CALLS:")
for trace_path, line_number, event in events:
    payload = event.get("payload")
    if not isinstance(payload, dict):
        continue
    if payload.get("type") not in {"custom_tool_call", "function_call"}:
        continue
    name = str(payload.get("name"))
    raw_input = payload.get("input", payload.get("arguments", ""))
    raw_text = raw_input if isinstance(raw_input, str) else json.dumps(raw_input, sort_keys=True)
    if name in {"exec_command", "write_stdin"}:
        try:
            parsed = json.loads(raw_text)
        except (TypeError, ValueError):
            parsed = raw_text
        rendered = json.dumps(parsed, sort_keys=True) if not isinstance(parsed, str) else parsed
        print(f"{line_number} {name}: {rendered}")
    else:
        print(
            f"{line_number} {name}: input_bytes={len(raw_text.encode())} "
            f"input_sha256={digest(raw_text)}"
        )

print("TOOL_OUTPUTS:")
for trace_path, line_number, event in events:
    payload = event.get("payload")
    if not isinstance(payload, dict):
        continue
    if payload.get("type") not in {"custom_tool_call_output", "function_call_output"}:
        continue
    combined = "\n".join(
        str(payload.get(key, "")) for key in ("output", "stdout", "stderr")
    )
    tail = combined[-1200:].replace("\x00", "<NUL>")
    print(
        f"{line_number} type={payload.get('type')} success={payload.get('success')} "
        f"bytes={len(combined.encode())} sha256={digest(combined)} tail={tail!r}"
    )

console_path = Path("/generation-evidence/codex-output.log")
console = console_path.read_text(errors="replace")
console_lines = console.splitlines()
print("CONSOLE_LOG:")
print(
    f"bytes={len(console.encode())} lines={len(console_lines)} "
    f"nonblank={sum(bool(line.strip()) for line in console_lines)} "
    f"sha256={digest(console_path.read_bytes())}"
)
for marker in ("#Top", "KPROVE_PASSED", "kompile", "kprove", "krun", "priority(40)"):
    print(f"marker {marker!r}: occurrences={console.count(marker)}")
print(f"console_tail={console[-5000:]!r}")
