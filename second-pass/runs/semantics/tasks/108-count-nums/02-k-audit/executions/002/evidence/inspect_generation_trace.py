#!/usr/bin/env python3
"""Read the complete generation trace/log and emit a bounded audit index."""

from __future__ import annotations

import collections
import glob
import hashlib
import json
from pathlib import Path


trace_paths = [Path(p) for p in glob.glob("/generation-evidence/codex-trace/**/*.jsonl", recursive=True)]
assert len(trace_paths) == 1
trace_path = trace_paths[0]

outer_counts: collections.Counter[str] = collections.Counter()
payload_counts: collections.Counter[tuple[str, str]] = collections.Counter()
call_counts: collections.Counter[str] = collections.Counter()
exec_calls: list[tuple[int, str]] = []
patch_calls: list[tuple[int, str]] = []
messages: list[tuple[int, str, str]] = []
output_statuses: list[tuple[int, str, str]] = []

with trace_path.open(encoding="utf-8") as stream:
    for number, line in enumerate(stream, 1):
        record = json.loads(line)
        outer = str(record.get("type"))
        payload = record.get("payload", {})
        payload_type = str(payload.get("type"))
        outer_counts[outer] += 1
        payload_counts[(outer, payload_type)] += 1
        if outer == "response_item" and payload_type in ("function_call", "custom_tool_call"):
            name = str(payload.get("name"))
            call_counts[name] += 1
            arguments = payload.get("arguments") or payload.get("input") or ""
            if name == "exec_command":
                parsed = json.loads(arguments)
                exec_calls.append((number, parsed["cmd"]))
            elif name == "apply_patch":
                first = next((part for part in str(arguments).splitlines() if part.startswith("*** ")), "")
                targets = [
                    part for part in str(arguments).splitlines()
                    if part.startswith(("*** Add File:", "*** Update File:", "*** Delete File:"))
                ]
                patch_calls.append((number, first + " " + " | ".join(targets)))
        if outer == "response_item" and payload_type == "message":
            role = str(payload.get("role"))
            text = "\n".join(
                str(block.get("text", ""))
                for block in payload.get("content", [])
                if block.get("type") in ("input_text", "output_text")
            )
            if role in ("assistant", "user"):
                messages.append((number, role, text))
        if outer == "response_item" and payload_type == "function_call_output":
            text = str(payload.get("output", ""))
            status = "unknown"
            if "Process exited with code 0" in text or '"exit_code":0' in text:
                status = "exit0"
            elif "Process exited with code" in text or '"exit_code":' in text:
                status = "nonzero_or_reported"
            if "#Top" in text:
                status += "+top"
            output_statuses.append((number, str(payload.get("call_id", "")), status))

print(f"trace={trace_path}")
print(f"trace_lines={sum(outer_counts.values())}")
print(f"outer_counts={dict(outer_counts)}")
print("payload_counts=")
for key in sorted(payload_counts):
    print(f"  {key}={payload_counts[key]}")
print(f"call_counts={dict(call_counts)}")
print("exec_command_index=")
for number, command in exec_calls:
    one_line = " ".join(command.splitlines())
    print(f"  trace_line={number}: {one_line}")
print("patch_index=")
for number, patch in patch_calls:
    print(f"  trace_line={number}: {patch}")
print("user_and_assistant_messages=")
for number, role, text in messages:
    bounded = " ".join(text.split())
    if len(bounded) > 500:
        bounded = bounded[:500] + "...[bounded]"
    print(f"  trace_line={number} role={role}: {bounded}")
print(f"function_call_outputs_read={len(output_statuses)}")
print(f"function_output_status_counts={dict(collections.Counter(status for _, _, status in output_statuses))}")

log_path = Path("/generation-evidence/codex-output.log")
line_count = 0
byte_count = 0
markers: collections.Counter[str] = collections.Counter()
keywords = (
    "#Top",
    "WarnStuckClaimState",
    "Process exited with code",
    "KPROVE_PASSED",
    "apply_patch",
    "kompile",
    "kprove",
    "krun",
)
sha = hashlib.sha256()
with log_path.open("rb") as stream:
    for raw in stream:
        sha.update(raw)
        line_count += 1
        byte_count += len(raw)
        text = raw.decode("utf-8", "replace")
        for keyword in keywords:
            markers[keyword] += text.count(keyword)
print(f"codex_output_lines={line_count}")
print(f"codex_output_bytes={byte_count}")
print(f"codex_output_sha256={sha.hexdigest()}")
print(f"codex_output_marker_counts={dict(markers)}")
print("GENERATION_TRACE_INSPECTION=COMPLETE")
