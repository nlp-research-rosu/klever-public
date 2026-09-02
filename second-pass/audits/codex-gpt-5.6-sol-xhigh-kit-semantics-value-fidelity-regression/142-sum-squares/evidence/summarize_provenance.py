#!/usr/bin/env python3
"""Summarize untrusted generation metadata without treating it as authority."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path


CANDIDATE = Path("/candidate")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


for name in ("run-input.json", "metrics.json"):
    path = CANDIDATE / name
    print(f"{name}: sha256={sha256(path)}")
    print(json.dumps(json.loads(path.read_text(encoding="utf-8")), sort_keys=True))

last = CANDIDATE / "codex-last.txt"
print(f"codex-last.txt: sha256={sha256(last)} bytes={last.stat().st_size}")
print(last.read_text(encoding="utf-8"))

log = CANDIDATE / "codex-output.log"
log_lines = log.read_text(encoding="utf-8", errors="replace").splitlines()
print(
    f"codex-output.log: sha256={sha256(log)} bytes={log.stat().st_size} "
    f"lines={len(log_lines)}"
)
print("codex-output-first-12-lines:")
for line in log_lines[:12]:
    print(line)
print("codex-output-last-16-lines:")
for line in log_lines[-16:]:
    print(line)

trace_paths = sorted((CANDIDATE / "codex-trace").rglob("*.jsonl"))
print(f"structured-trace-count={len(trace_paths)}")
for trace in trace_paths:
    counts: Counter[tuple[object, object]] = Counter()
    malformed = 0
    first_timestamp = None
    last_timestamp = None
    lines = 0
    with trace.open(encoding="utf-8") as handle:
        for line in handle:
            lines += 1
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                malformed += 1
                continue
            timestamp = row.get("timestamp")
            if first_timestamp is None:
                first_timestamp = timestamp
            last_timestamp = timestamp
            payload = row.get("payload") or {}
            counts[(row.get("type"), payload.get("type"))] += 1
    print(
        f"trace={trace.relative_to(CANDIDATE)} sha256={sha256(trace)} "
        f"bytes={trace.stat().st_size} lines={lines} malformed={malformed} "
        f"first={first_timestamp} last={last_timestamp}"
    )
    for key, count in sorted(counts.items(), key=lambda pair: str(pair[0])):
        print(f"  type={key!r} count={count}")

print(
    "classification=UNTRUSTED_CLAIMS_ONLY; none of these prior success markers "
    "is used as proof evidence"
)
