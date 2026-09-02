#!/usr/bin/env python3
"""Read all untrusted generation evidence and emit a bounded structural summary."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


CANDIDATE = Path("/candidate")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


for name in ("run-input.json", "metrics.json"):
    path = CANDIDATE / name
    value = json.loads(path.read_text())
    print(f"{name} sha256={digest(path)} parsed={json.dumps(value, sort_keys=True)}")

for name in ("codex-last.txt", "codex-output.log"):
    path = CANDIDATE / name
    text = path.read_text(errors="replace")
    claims = [
        line
        for line in text.splitlines()
        if "#Top" in line
        or "random" in line.lower()
        or "RESULT:" in line
        or "exit=" in line.lower()
    ]
    print(
        f"{name} sha256={digest(path)} bytes={len(text.encode())} "
        f"lines={len(text.splitlines())} selected_claim_lines={len(claims)}"
    )
    for line in claims[-30:]:
        print(f"  CLAIM {line[:500]}")

trace_paths = sorted((CANDIDATE / "codex-trace").rglob("*.jsonl"))
print(f"structured_trace_files={len(trace_paths)}")
for path in trace_paths:
    type_counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    invalid: list[tuple[int, str]] = []
    records = []
    for lineno, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        try:
            record = json.loads(line)
        except Exception as err:
            invalid.append((lineno, repr(err)))
            continue
        records.append(record)
        type_counts[str(record.get("type"))] += 1
        payload = record.get("payload")
        if isinstance(payload, dict):
            payload_counts[str(payload.get("type"))] += 1
    print(
        f"TRACE {path} sha256={digest(path)} records={len(records)} "
        f"invalid={invalid} types={dict(type_counts)} "
        f"payload_types={dict(payload_counts)}"
    )
    for record in records:
        payload = record.get("payload")
        if not isinstance(payload, dict):
            continue
        if payload.get("type") in {"agent_message", "task_complete"}:
            message = payload.get("message") or payload.get("last_agent_message")
            if message:
                print(f"  TRACE_CLAIM {str(message)[:1000]}")
