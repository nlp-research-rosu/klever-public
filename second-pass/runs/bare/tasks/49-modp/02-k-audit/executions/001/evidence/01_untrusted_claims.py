#!/usr/bin/env python3
"""Bounded inventory of untrusted candidate generation claims."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


CANDIDATE = Path("/candidate")
TRACE = next((CANDIDATE / "codex-trace").rglob("*.jsonl"))
OUTPUT = CANDIDATE / "codex-output.log"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


print("UNTRUSTED_CLAIM_FILES")
for name in [
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
]:
    path = CANDIDATE / name
    data = path.read_bytes()
    print(
        f"{path}|bytes={len(data)}|lines={data.count(bytes([10]))}|sha256={digest(path)}"
    )

print("CODEX_LAST_TEXT")
print((CANDIDATE / "codex-last.txt").read_text(encoding="utf-8"), end="")

output_text = OUTPUT.read_text(encoding="utf-8", errors="replace")
print("CODEX_OUTPUT_PATTERN_COUNTS")
for pattern in [
    "kompile",
    "krun",
    "kprove",
    "#Top",
    "WarnStuckClaimState",
    "KPROVE_PASSED",
]:
    print(f"{pattern}={len(re.findall(re.escape(pattern), output_text))}")

records = []
type_counts: Counter[str] = Counter()
payload_type_counts: Counter[str] = Counter()
with TRACE.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        record = json.loads(line)
        records.append((line_number, record))
        type_counts[str(record.get("type"))] += 1
        payload = record.get("payload")
        if isinstance(payload, dict):
            payload_type_counts[str(payload.get("type"))] += 1

print("STRUCTURED_TRACE")
print(f"path={TRACE}")
print(f"bytes={TRACE.stat().st_size}")
print(f"sha256={digest(TRACE)}")
print(f"records={len(records)}")
print(f"record_types={dict(type_counts)}")
print(f"payload_types={dict(payload_type_counts)}")

print("STRUCTURED_TRACE_RELEVANT_CALLS")
relevant = re.compile(r"\b(?:kompile|krun|kprove)\b")
for line_number, record in records:
    payload = record.get("payload")
    if not isinstance(payload, dict):
        continue
    if payload.get("type") != "custom_tool_call":
        continue
    raw_input = str(payload.get("input", ""))
    if relevant.search(raw_input):
        compact = " ".join(raw_input.split())
        print(
            f"line={line_number}|call_id={payload.get('call_id')}|"
            f"input={compact[:1000]}"
        )

print("STRUCTURED_TRACE_TOP_OUTPUTS")
for line_number, record in records:
    payload = record.get("payload")
    if not isinstance(payload, dict):
        continue
    if payload.get("type") != "custom_tool_call_output":
        continue
    output_repr = json.dumps(payload.get("output"), ensure_ascii=False)
    if "#Top" in output_repr or "WarnStuckClaimState" in output_repr:
        compact = " ".join(output_repr.split())
        print(
            f"line={line_number}|call_id={payload.get('call_id')}|"
            f"output={compact[:1600]}"
        )
