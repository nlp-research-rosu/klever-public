#!/usr/bin/env python3
"""Summarize all readable records in the untrusted structured generation trace."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


TRACE_DIR = Path("/candidate/codex-trace")
OUTPUT_LOG = Path("/candidate/codex-output.log")


def flatten_text(value: object) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(flatten_text(item) for item in value)
    if isinstance(value, dict):
        if isinstance(value.get("text"), str):
            return value["text"]
        return "\n".join(flatten_text(item) for item in value.values())
    return ""


def bounded(text: str, limit: int = 1200) -> str:
    text = text.replace("\x00", "<NUL>")
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n...[{len(text) - limit} characters omitted]"


trace_files = sorted(TRACE_DIR.rglob("*.jsonl"))
print(f"trace_files={len(trace_files)}")
counts: collections.Counter[tuple[object, ...]] = collections.Counter()
records = 0
encrypted_reasoning = 0

for trace_path in trace_files:
    digest = hashlib.sha256(trace_path.read_bytes()).hexdigest()
    print(f"TRACE {trace_path} sha256={digest}")
    with trace_path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            records += 1
            payload = record.get("payload") or {}
            key = (
                record.get("type"),
                payload.get("type"),
                payload.get("role"),
                payload.get("name"),
            )
            counts[key] += 1
            payload_type = payload.get("type")
            if payload_type == "reasoning":
                if payload.get("encrypted_content"):
                    encrypted_reasoning += 1
                continue
            if payload_type in {
                "message",
                "user_message",
                "agent_message",
                "custom_tool_call",
                "custom_tool_call_output",
                "function_call",
                "function_call_output",
                "task_complete",
            }:
                fields = {
                    name: payload.get(name)
                    for name in (
                        "role",
                        "phase",
                        "name",
                        "status",
                        "message",
                        "input",
                        "arguments",
                        "output",
                        "last_agent_message",
                    )
                    if payload.get(name) is not None
                }
                print(f"\nRECORD line={line_number} type={record.get('type')} payload={payload_type}")
                print(bounded(flatten_text(fields)))

print(f"\nrecords={records}")
print(f"encrypted_reasoning_records={encrypted_reasoning}")
print("event_inventory:")
for key, count in sorted(counts.items(), key=lambda item: tuple("" if v is None else str(v) for v in item[0])):
    print(count, key)

output_bytes = OUTPUT_LOG.read_bytes()
output_text = output_bytes.decode("utf-8", errors="replace")
print(
    f"\ncodex_output path={OUTPUT_LOG} bytes={len(output_bytes)} "
    f"lines={len(output_text.splitlines())} sha256={hashlib.sha256(output_bytes).hexdigest()}"
)
needles = (
    "#Top",
    "WarnTrivialClaim",
    "kprove spec.k",
    "kompile verification.k",
    "RESULT: KPROVE_PASSED",
)
for needle in needles:
    matching = [line for line in output_text.splitlines() if needle in line]
    print(f"codex_output occurrences {needle!r}: {len(matching)}")
    for line in matching[:10]:
        print("  " + bounded(line, 500))
