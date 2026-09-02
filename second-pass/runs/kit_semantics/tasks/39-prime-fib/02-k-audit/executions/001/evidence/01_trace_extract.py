#!/usr/bin/env python3
"""Parse every structured generation-trace record and summarize untrusted claims."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/25/"
    "rollout-2026-07-25T00-04-10-019f97a8-cf37-7dd3-8884-fef0cf5c5bbc.jsonl"
)
rows = [json.loads(line) for line in TRACE.read_text().splitlines()]
print("records:", len(rows))
print("top-level types:", dict(collections.Counter(row["type"] for row in rows)))
print(
    "payload types:",
    dict(collections.Counter(row.get("payload", {}).get("type") for row in rows)),
)

print("\nASSISTANT MESSAGES")
for index, row in enumerate(rows, 1):
    payload = row.get("payload", {})
    if row["type"] == "response_item" and payload.get("type") == "message":
        if payload.get("role") != "assistant":
            continue
        text = "\n".join(
            item.get("text", "")
            for item in payload.get("content", [])
            if item.get("type") in {"input_text", "output_text"}
        )
        print(f"--- record {index}, phase={payload.get('phase')}")
        print(text[:4000])

print("\nTOOL CALL INVENTORY (arguments bounded to 1200 characters)")
calls = collections.Counter()
for index, row in enumerate(rows, 1):
    payload = row.get("payload", {})
    if row["type"] != "response_item":
        continue
    if payload.get("type") not in {"function_call", "custom_tool_call"}:
        continue
    name = payload.get("name", "<unknown>")
    calls[name] += 1
    arguments = payload.get("arguments", payload.get("input", ""))
    if not isinstance(arguments, str):
        arguments = json.dumps(arguments, sort_keys=True)
    arguments = arguments.replace("\x00", "<NUL>")
    print(f"{index}: {name}: {arguments[:1200]}")
print("tool counts:", dict(calls))

log_text = Path("/generation-evidence/codex-output.log").read_text(errors="replace")
print("\nCODEX OUTPUT LOG")
print("characters:", len(log_text), "lines:", len(log_text.splitlines()))
for needle in (
    "kompile",
    "kprove",
    "krun",
    "#Top",
    "WarnStuckClaimState",
    "EXPECTED FAILURE",
    "RESULT:",
):
    print(f"{needle!r} occurrences:", log_text.count(needle))
