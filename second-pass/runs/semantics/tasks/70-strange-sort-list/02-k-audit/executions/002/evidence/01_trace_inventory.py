#!/usr/bin/env python3
"""Read every structured trace record and emit a bounded provenance inventory."""

from __future__ import annotations

import collections
import glob
import json
import os


TRACE_GLOB = "/generation-evidence/codex-trace/**/*.jsonl"


def clip(value: object, limit: int = 700) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = text.replace("\r", "\\r")
    if len(text) <= limit:
        return text
    half = (limit - 80) // 2
    return text[:half] + f"\n... [clipped {len(text) - 2 * half} chars] ...\n" + text[-half:]


paths = sorted(glob.glob(TRACE_GLOB, recursive=True))
if not paths:
    raise SystemExit("No structured trace found")

counts: collections.Counter[tuple[object, ...]] = collections.Counter()
calls: dict[str, tuple[str, str]] = {}
outputs: dict[str, str] = {}
messages: list[tuple[int, str, str]] = []
patches: list[tuple[int, str]] = []
malformed: list[tuple[str, int, str]] = []
line_number = 0

for path in paths:
    with open(path, encoding="utf-8") as stream:
        for local_line, raw in enumerate(stream, 1):
            line_number += 1
            try:
                row = json.loads(raw)
            except Exception as err:
                malformed.append((path, local_line, repr(err)))
                continue
            payload = row.get("payload", {})
            counts[
                (
                    row.get("type"),
                    payload.get("type"),
                    payload.get("name"),
                    payload.get("role"),
                )
            ] += 1
            if row.get("type") == "response_item" and payload.get("type") == "function_call":
                calls[payload.get("call_id", f"line-{line_number}")] = (
                    payload.get("name", ""),
                    payload.get("arguments", ""),
                )
            elif row.get("type") == "response_item" and payload.get("type") == "function_call_output":
                outputs[payload.get("call_id", f"line-{line_number}")] = payload.get("output", "")
            elif row.get("type") == "response_item" and payload.get("type") == "message":
                content = payload.get("content", [])
                text = "\n".join(
                    part.get("text", "")
                    for part in content
                    if isinstance(part, dict) and "text" in part
                )
                messages.append((line_number, payload.get("role", ""), text))
            elif row.get("type") == "response_item" and payload.get("type") == "custom_tool_call":
                if payload.get("name") == "apply_patch":
                    patches.append((line_number, payload.get("input", "")))

print(f"Trace files: {len(paths)}")
for path in paths:
    print(f"  {os.path.getsize(path)} bytes {path}")
print(f"Parsed JSONL records: {line_number}")
print(f"Malformed records: {len(malformed)}")
for item in malformed:
    print(f"  {item}")

print("Event inventory:")
for key, count in sorted(counts.items(), key=lambda item: tuple("" if x is None else str(x) for x in item[0])):
    print(f"  {count:4d} {key}")

print("Messages:")
for line, role, text in messages:
    if role in {"user", "assistant"}:
        print(f"TRACE LINE {line} ROLE {role}\n{clip(text, 1200)}")

print("Tool calls with paired bounded outputs:")
for call_id, (name, arguments) in calls.items():
    print(f"CALL {call_id} NAME {name}")
    print(clip(arguments, 1200))
    if call_id in outputs:
        print("OUTPUT")
        print(clip(outputs[call_id], 1000))
    else:
        print("OUTPUT MISSING")

print("Patch inventory:")
for line, patch in patches:
    targets = [
        part
        for part in patch.splitlines()
        if part.startswith("*** Add File:")
        or part.startswith("*** Update File:")
        or part.startswith("*** Delete File:")
        or part.startswith("*** Move to:")
    ]
    print(f"TRACE LINE {line}: {targets or ['unrecognized patch target']} ({len(patch)} chars)")
