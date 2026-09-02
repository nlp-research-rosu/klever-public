#!/usr/bin/env python3
"""Read candidate generation records as untrusted claims and summarize them."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path("/candidate")


def metadata(path: Path) -> str:
    raw = path.read_bytes()
    return (
        f"{path}: bytes={len(raw)} lines={raw.count(bytes([10]))} "
        f"sha256={hashlib.sha256(raw).hexdigest()}"
    )


for name in [
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
]:
    path = ROOT / name
    print(metadata(path))

print("RUN_INPUT_UNTRUSTED=" + json.dumps(json.loads((ROOT / "run-input.json").read_text()), sort_keys=True))
print("METRICS_UNTRUSTED=" + json.dumps(json.loads((ROOT / "metrics.json").read_text()), sort_keys=True))
print("CODEX_LAST_UNTRUSTED_BEGIN")
print((ROOT / "codex-last.txt").read_text().rstrip())
print("CODEX_LAST_UNTRUSTED_END")

output = (ROOT / "codex-output.log").read_text(errors="replace")
needles = [
    "#Top",
    "WarnStuckClaimState",
    "KPROVE_PASSED",
    "VALIDATED",
    "kompile ",
    "kprove ",
]
print(
    "CODEX_OUTPUT_UNTRUSTED_COUNTS="
    + json.dumps({needle: output.count(needle) for needle in needles}, sort_keys=True)
)

traces = sorted((ROOT / "codex-trace").rglob("*.jsonl"))
print(f"TRACE_FILE_COUNT={len(traces)}")
for path in traces:
    print(metadata(path))
    top_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    parse_failures = 0
    final_messages: list[str] = []
    for line in path.read_text(errors="replace").splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            parse_failures += 1
            continue
        top_types[str(record.get("type"))] += 1
        payload = record.get("payload")
        if isinstance(payload, dict):
            payload_types[str(payload.get("type"))] += 1
            if payload.get("type") == "message" and payload.get("role") == "assistant":
                if payload.get("phase") == "final_answer":
                    final_messages.append(
                        json.dumps(payload.get("content"), sort_keys=True)
                    )
    print(f"TRACE_PARSE_FAILURES={parse_failures}")
    print("TRACE_TOP_TYPES=" + json.dumps(top_types, sort_keys=True))
    print("TRACE_PAYLOAD_TYPES=" + json.dumps(payload_types, sort_keys=True))
    print("TRACE_FINAL_MESSAGES_UNTRUSTED=" + json.dumps(final_messages))
