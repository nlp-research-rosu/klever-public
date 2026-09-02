#!/usr/bin/env python3
"""Summarize candidate provenance artifacts strictly as untrusted claims."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


CANDIDATE = Path("/candidate")
TRACE = next((CANDIDATE / "codex-trace").rglob("*.jsonl"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


for name in ("run-input.json", "metrics.json", "codex-last.txt", "codex-output.log"):
    path = CANDIDATE / name
    print(f"ARTIFACT {name} bytes={path.stat().st_size} sha256={digest(path)}")

print("RUN_INPUT_UNTRUSTED", json.dumps(json.loads((CANDIDATE / "run-input.json").read_text()), sort_keys=True))
print("METRICS_UNTRUSTED", json.dumps(json.loads((CANDIDATE / "metrics.json").read_text()), sort_keys=True))
print("CODEX_LAST_UNTRUSTED", json.dumps((CANDIDATE / "codex-last.txt").read_text()))

trace_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
records = 0
malformed = 0
final_messages: list[str] = []
with TRACE.open(encoding="utf-8") as stream:
    for line in stream:
        records += 1
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            malformed += 1
            continue
        trace_types[str(record.get("type"))] += 1
        payload = record.get("payload")
        if isinstance(payload, dict):
            payload_types[str(payload.get("type"))] += 1
            if (
                record.get("type") == "response_item"
                and payload.get("type") == "message"
                and payload.get("role") == "assistant"
                and payload.get("phase") == "final_answer"
            ):
                text = "".join(
                    item.get("text", "")
                    for item in payload.get("content", [])
                    if isinstance(item, dict)
                )
                final_messages.append(text)

print(f"TRACE {TRACE} bytes={TRACE.stat().st_size} sha256={digest(TRACE)}")
print(f"TRACE_RECORDS {records}")
print(f"TRACE_MALFORMED {malformed}")
print("TRACE_TOP_TYPES", json.dumps(trace_types, sort_keys=True))
print("TRACE_PAYLOAD_TYPES", json.dumps(payload_types, sort_keys=True))
for message in final_messages:
    print("TRACE_FINAL_UNTRUSTED", json.dumps(message))

output_path = CANDIDATE / "codex-output.log"
markers = (
    "#Top",
    "WarnStuckClaimState",
    "DIFFERENTIAL:",
    "K_DIFFERENTIAL_GENERATED:",
    "RESULT: KPROVE_PASSED",
    "VALIDATED",
)
counts = collections.Counter()
line_count = 0
with output_path.open(encoding="utf-8", errors="replace") as stream:
    for line in stream:
        line_count += 1
        for marker in markers:
            if marker in line:
                counts[marker] += 1
print(f"CODEX_OUTPUT_LINES {line_count}")
print("CODEX_OUTPUT_MARKER_COUNTS_UNTRUSTED", json.dumps(counts, sort_keys=True))
