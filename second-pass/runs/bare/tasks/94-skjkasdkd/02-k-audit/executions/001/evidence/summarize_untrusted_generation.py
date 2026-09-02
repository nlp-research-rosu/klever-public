#!/usr/bin/env python3
"""Bounded structural summary of the untrusted generation records."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


CANDIDATE = Path("/candidate")
TRACE = next((CANDIDATE / "codex-trace").rglob("*.jsonl"))
KEYWORDS = (
    "kprove",
    "kompile",
    "krun",
    "prove.sh",
    "#Top",
    "WarnStuck",
    "spec-vacuity",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


for name in ("run-input.json", "metrics.json", "codex-last.txt", "codex-output.log"):
    path = CANDIDATE / name
    data = path.read_bytes()
    print(f"FILE {path} bytes={len(data)} sha256={digest(path)}")

print("RUN_INPUT")
print((CANDIDATE / "run-input.json").read_text(encoding="utf-8"))
print("METRICS")
print((CANDIDATE / "metrics.json").read_text(encoding="utf-8"))
print("CODEX_LAST")
print((CANDIDATE / "codex-last.txt").read_text(encoding="utf-8"))

top_counts: collections.Counter[str] = collections.Counter()
payload_counts: collections.Counter[str] = collections.Counter()
role_counts: collections.Counter[str] = collections.Counter()
interesting: list[tuple[int, str, str]] = []
parse_errors: list[tuple[int, str]] = []

with TRACE.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        try:
            item = json.loads(line)
        except Exception as err:  # pragma: no cover - audit diagnostic
            parse_errors.append((line_number, repr(err)))
            continue
        top_type = str(item.get("type", "<missing>"))
        top_counts[top_type] += 1
        payload = item.get("payload")
        if isinstance(payload, dict):
            payload_type = str(payload.get("type", "<missing>"))
            payload_counts[payload_type] += 1
            role = payload.get("role")
            if role is not None:
                role_counts[str(role)] += 1
            serialized = json.dumps(payload, sort_keys=True)
            if any(keyword in serialized for keyword in KEYWORDS):
                bounded = " ".join(serialized.split())
                interesting.append((line_number, payload_type, bounded[:1200]))

print(f"TRACE {TRACE} bytes={TRACE.stat().st_size} sha256={digest(TRACE)}")
print(f"TRACE_PARSE_ERRORS {parse_errors}")
print(f"TRACE_TOP_TYPES {dict(top_counts)}")
print(f"TRACE_PAYLOAD_TYPES {dict(payload_counts)}")
print(f"TRACE_ROLES {dict(role_counts)}")
print(f"TRACE_INTERESTING_COUNT {len(interesting)}")
for line_number, payload_type, text in interesting:
    print(f"TRACE_EVENT line={line_number} payload_type={payload_type} {text}")

log_path = CANDIDATE / "codex-output.log"
log_lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
print(f"CODEX_OUTPUT_LINES {len(log_lines)}")
for keyword in KEYWORDS:
    matches = [number for number, line in enumerate(log_lines, 1) if keyword in line]
    print(f"CODEX_OUTPUT_MATCH keyword={keyword!r} count={len(matches)} lines={matches[:80]}")

contexts: set[int] = set()
for number, line in enumerate(log_lines, 1):
    if (
        "#Top" in line
        or "bash prove.sh" in line
        or "RESULT: KPROVE_PASSED" in line
        or "failed in" in line
    ):
        contexts.add(number)
for center in sorted(contexts):
    start = max(1, center - 2)
    end = min(len(log_lines), center + 2)
    print(f"CODEX_OUTPUT_CONTEXT lines={start}-{end}")
    for number in range(start, end + 1):
        print(f"{number}: {log_lines[number - 1][:1200]}")
