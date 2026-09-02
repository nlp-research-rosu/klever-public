#!/usr/bin/env python3
"""Bounded inventory of the untrusted structured generation trace."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


trace = next(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
rows = [
    json.loads(line)
    for line in trace.read_text(encoding="utf-8").splitlines()
    if line.strip()
]
print(f"TRACE: {trace}")
print(f"JSONL_RECORDS: {len(rows)}")
print(
    "TOP_LEVEL_TYPES:",
    dict(Counter(row.get("type") for row in rows)),
)
print(
    "PAYLOAD_TYPES:",
    dict(Counter(row.get("payload", {}).get("type") for row in rows)),
)

print("TOOL_CALL_INVENTORY:")
for line_number, row in enumerate(rows, 1):
    payload = row.get("payload", {})
    payload_type = payload.get("type")
    if payload_type == "custom_tool_call":
        value = payload.get("input", "").replace("\n", "\\n")
        print(
            f"{line_number}: custom {payload.get('name')} "
            f"{value[:900]}"
        )
    elif payload_type == "function_call":
        print(
            f"{line_number}: function {payload.get('name')} "
            f"{payload.get('arguments', '')[:900]}"
        )

print("TOOL_RESULT_INVENTORY:")
for line_number, row in enumerate(rows, 1):
    payload = row.get("payload", {})
    payload_type = payload.get("type")
    if payload_type not in {"custom_tool_call_output", "function_call_output"}:
        continue
    encoded = json.dumps(payload.get("output"), ensure_ascii=False)
    signals = []
    for needle in (
        '"exit_code":0',
        '"exit_code":113',
        "#Top",
        "WarnStuckClaimState",
        "krun multiply(",
    ):
        if needle in encoded:
            signals.append(needle)
    print(
        f"{line_number}: {payload_type} "
        f"signals={signals} bytes={len(encoded.encode())}"
    )

final_messages = [
    row.get("payload", {}).get("message", "")
    for row in rows
    if row.get("payload", {}).get("type") == "agent_message"
    and row.get("payload", {}).get("phase") == "final_answer"
]
assert len(final_messages) == 1
print("UNTRUSTED_FINAL_MESSAGE:")
print(final_messages[0])
