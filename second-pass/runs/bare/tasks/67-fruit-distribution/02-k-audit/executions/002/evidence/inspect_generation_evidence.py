#!/usr/bin/env python3
"""Read every byte of the untrusted generation logs and summarize their structure."""

from __future__ import annotations

import collections
import hashlib
import json
import pathlib
import re


TRACE = pathlib.Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T05-23-04-019f8959-b185-7d82-8ffc-e748bfcc65c7.jsonl"
)
OUTPUT = pathlib.Path("/generation-evidence/codex-output.log")


def digest(path: pathlib.Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


print(f"TRACE_SHA256={digest(TRACE)}")
trace_lines = TRACE.read_text(encoding="utf-8").splitlines()
print(f"TRACE_LINES={len(trace_lines)}")

top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
roles: collections.Counter[str] = collections.Counter()
tool_calls: list[tuple[int, str, str]] = []
assistant_messages: list[tuple[int, str]] = []

for number, line in enumerate(trace_lines, 1):
    event = json.loads(line)
    top_types[str(event.get("type"))] += 1
    payload = event.get("payload")
    if isinstance(payload, dict):
        payload_type = str(payload.get("type"))
        payload_types[payload_type] += 1
        if "role" in payload:
            roles[str(payload.get("role"))] += 1
        if payload_type in {"function_call", "custom_tool_call"}:
            name = str(payload.get("name", payload.get("tool", "")))
            arguments = str(payload.get("arguments", payload.get("input", "")))
            tool_calls.append((number, name, arguments))
        if payload_type == "message" and payload.get("role") == "assistant":
            content = payload.get("content", [])
            assistant_messages.append((number, json.dumps(content, ensure_ascii=False)))

print(f"TOP_TYPES={dict(top_types)}")
print(f"PAYLOAD_TYPES={dict(payload_types)}")
print(f"ROLES={dict(roles)}")
print("TRACE_TOOL_CALLS_BEGIN")
for number, name, arguments in tool_calls:
    one_line = re.sub(r"\s+", " ", arguments).strip()
    print(f"{number}: {name}: {one_line[:1400]}")
print("TRACE_TOOL_CALLS_END")
print("TRACE_ASSISTANT_MESSAGES_BEGIN")
for number, message in assistant_messages:
    one_line = re.sub(r"\s+", " ", message).strip()
    print(f"{number}: {one_line[:2000]}")
print("TRACE_ASSISTANT_MESSAGES_END")

print(f"OUTPUT_SHA256={digest(OUTPUT)}")
output_text = OUTPUT.read_text(encoding="utf-8", errors="replace")
output_lines = output_text.splitlines()
print(f"OUTPUT_BYTES={len(output_text.encode('utf-8'))}")
print(f"OUTPUT_LINES={len(output_lines)}")
patterns = re.compile(
    r"(kompile|kprove|krun|py2mpy|#Top|WarnStuck|Error|RESULT:|"
    r"semantic\.k|verification\.k|spec\.k|solution\.mpy|prove\.sh)",
    re.IGNORECASE,
)
print("OUTPUT_RELEVANT_LINES_BEGIN")
for number, line in enumerate(output_lines, 1):
    if patterns.search(line):
        print(f"{number}: {line[:2400]}")
print("OUTPUT_RELEVANT_LINES_END")
print("OUTPUT_FIRST_20_BEGIN")
for number, line in enumerate(output_lines[:20], 1):
    print(f"{number}: {line[:2400]}")
print("OUTPUT_FIRST_20_END")
print("OUTPUT_LAST_40_BEGIN")
start = max(0, len(output_lines) - 40)
for offset, line in enumerate(output_lines[start:], start + 1):
    print(f"{offset}: {line[:2400]}")
print("OUTPUT_LAST_40_END")
