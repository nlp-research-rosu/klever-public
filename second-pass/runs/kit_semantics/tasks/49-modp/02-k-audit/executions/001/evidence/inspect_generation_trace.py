#!/usr/bin/env python3

"""Bounded structural inspection of the untrusted generation JSONL trace."""

from __future__ import annotations

import collections
import hashlib
import json
import re
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/29/"
    "rollout-2026-07-29T13-28-33-019faf22-ad6c-7c00-9e90-9abff2d99374.jsonl"
)
INTERESTING = re.compile(
    r"(?:kompile|kprove|krun|#Top|WarnStuckClaimState|"
    r"MUTATION_EXIT|TARGET_EXIT|PROBE|DecidePredicateUnknown|"
    r"ERROR|FAILED|mismatch|VALIDATED|SOUND-BUT-LIMITED)",
    re.IGNORECASE,
)


def flatten(value: object) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, sort_keys=True, ensure_ascii=False)


raw = TRACE.read_bytes()
print(f"TRACE={TRACE}")
print(f"BYTES={len(raw)}")
print(f"SHA256={hashlib.sha256(raw).hexdigest()}")

counts: collections.Counter[tuple[str, str]] = collections.Counter()
records: list[tuple[int, dict[str, object]]] = []
for line_number, raw_line in enumerate(raw.splitlines(), 1):
    record = json.loads(raw_line)
    payload = record.get("payload", {})
    if not isinstance(payload, dict):
        payload = {}
    counts[(str(record.get("type")), str(payload.get("type")))] += 1
    records.append((line_number, record))

print(f"PARSED_LINES={len(records)}")
print("EVENT_COUNTS")
for key, count in sorted(counts.items()):
    print(f"{key[0]}|{key[1]}|{count}")

print("ASSISTANT_MESSAGES")
for line_number, record in records:
    payload = record.get("payload", {})
    if not isinstance(payload, dict):
        continue
    if payload.get("type") != "message" or payload.get("role") != "assistant":
        continue
    content = payload.get("content", [])
    print(f"LINE={line_number}|PHASE={payload.get('phase')}")
    print(flatten(content))

print("TOOL_CALLS_AND_BOUNDED_OUTPUTS")
for line_number, record in records:
    payload = record.get("payload", {})
    if not isinstance(payload, dict):
        continue
    subtype = payload.get("type")
    if subtype in {"function_call", "custom_tool_call"}:
        body = payload.get("arguments", payload.get("input", ""))
        print(
            f"LINE={line_number}|CALL|NAME={payload.get('name')}|"
            f"CALL_ID={payload.get('call_id')}"
        )
        print(flatten(body))
    elif subtype in {"function_call_output", "custom_tool_call_output"}:
        body = flatten(payload.get("output", ""))
        digest = hashlib.sha256(body.encode()).hexdigest()
        print(
            f"LINE={line_number}|OUTPUT|CALL_ID={payload.get('call_id')}|"
            f"CHARS={len(body)}|SHA256={digest}"
        )
        matched = [line for line in body.splitlines() if INTERESTING.search(line)]
        for line in matched[:80]:
            print(f"MATCH|{line[:1000]}")
        if len(matched) > 80:
            print(f"MATCHES_TRUNCATED={len(matched) - 80}")
        print(f"HEAD|{body[:500]}")
        if len(body) > 500:
            print(f"TAIL|{body[-500:]}")
