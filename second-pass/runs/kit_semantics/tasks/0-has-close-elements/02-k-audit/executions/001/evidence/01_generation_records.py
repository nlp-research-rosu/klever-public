#!/usr/bin/env python3
"""Parse every pipeline-v3 generation record without trusting its claims."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path


TRACE = Path(
    "/generation/codex-trace/2026/07/26/"
    "rollout-2026-07-26T00-57-01-019f9cff-8c9c-76e3-8d3b-1ccd3a1400fc.jsonl"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clipped(value: object, limit: int = 360) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit] + "...[clipped]"


print("COMMAND: python3 /audit-output/evidence/01_generation_records.py")
for raw_path in (
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/generation/invocation.json",
    "/generation/metrics.json",
    "/generation/runtime-metrics.json",
    "/generation/usage.json",
):
    path = Path(raw_path)
    value = json.loads(path.read_text())
    print(
        "VALID_JSON",
        raw_path,
        "sha256=" + digest(path),
        "top_keys=" + ",".join(sorted(value)),
    )

type_counts: Counter[str] = Counter()
payload_counts: Counter[str] = Counter()
function_counts: Counter[str] = Counter()
commands: list[str] = []
messages: list[tuple[str, str]] = []
line_count = 0
with TRACE.open() as stream:
    for line_count, line in enumerate(stream, 1):
        event = json.loads(line)
        event_type = event.get("type", "<missing>")
        type_counts[event_type] += 1
        payload = event.get("payload", {})
        payload_type = payload.get("type", "<missing>")
        payload_counts[f"{event_type}/{payload_type}"] += 1
        if event_type == "response_item" and payload_type == "function_call":
            name = payload.get("name", "<missing>")
            function_counts[name] += 1
            args = payload.get("arguments", "")
            commands.append(f"{name}: {clipped(args)}")
        if event_type == "response_item" and payload_type == "message":
            role = payload.get("role", "<missing>")
            for content in payload.get("content", []):
                if content.get("type") in {"input_text", "output_text"}:
                    messages.append((role, clipped(content.get("text", ""), 500)))
        if event_type == "event_msg" and payload_type == "agent_message":
            messages.append(("agent_message", clipped(payload.get("message", ""), 500)))

print("TRACE_VALID_JSONL", f"lines={line_count}", "sha256=" + digest(TRACE))
print("TRACE_EVENT_COUNTS", dict(sorted(type_counts.items())))
print("TRACE_PAYLOAD_COUNTS", dict(sorted(payload_counts.items())))
print("TRACE_FUNCTION_COUNTS", dict(sorted(function_counts.items())))
print("TRACE_TOOL_CALLS_BEGIN")
for index, command in enumerate(commands, 1):
    print(f"{index:03d}", command)
print("TRACE_TOOL_CALLS_END")
print("TRACE_MESSAGES_BEGIN")
for role, message in messages:
    print(role + ":", message)
print("TRACE_MESSAGES_END")

output_path = Path("/generation/codex-output.log")
output_text = output_path.read_text(errors="strict")
print(
    "CODEX_OUTPUT_FULL_READ",
    f"chars={len(output_text)}",
    f"lines={output_text.count(chr(10))}",
    "sha256=" + digest(output_path),
    f"kprove_mentions={output_text.count('kprove')}",
    f"Top_mentions={output_text.count('#Top')}",
    f"RESULT_mentions={output_text.count('RESULT:')}",
)
print("CODEX_OUTPUT_PREFIX", clipped(output_text[:1000], 1000))
print("CODEX_OUTPUT_SUFFIX", clipped(output_text[-1600:], 1600))

last_path = Path("/generation/codex-last.txt")
last_text = last_path.read_text(errors="strict")
print("CODEX_LAST_FULL_READ", "sha256=" + digest(last_path), clipped(last_text, 1000))
print("SCRIPT_EXIT=0")
