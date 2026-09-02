#!/usr/bin/env python3
"""Bounded summary of candidate generation records, treated only as claims."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


ROOT = Path("/candidate")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


for name in ("run-input.json", "metrics.json"):
    path = ROOT / name
    print(f"=== {name} (UNTRUSTED CLAIM) ===")
    print(json.dumps(json.loads(path.read_text(encoding="utf-8")), indent=2, sort_keys=True))

for name in ("codex-last.txt", "codex-output.log"):
    path = ROOT / name
    text = path.read_text(encoding="utf-8", errors="replace")
    print(
        f"FILE {name} bytes={len(text.encode('utf-8'))} "
        f"lines={len(text.splitlines())} sha256={digest(path)}"
    )
    if name == "codex-last.txt":
        print("=== codex-last.txt (UNTRUSTED CLAIM) ===")
        print(text.rstrip())
    else:
        needles = (
            "#Top",
            "WarnStuckClaimState",
            "RESULT:",
            "program-term-match:",
            "tested=",
            "VALIDATED",
        )
        print("=== codex-output.log claim-marker counts ===")
        for needle in needles:
            print(f"{needle!r}: {text.count(needle)}")
        print("=== codex-output.log bounded tail ===")
        print("\n".join(text.splitlines()[-40:]))

trace_paths = sorted((ROOT / "codex-trace").rglob("*.jsonl"))
print(f"TRACE_FILES {len(trace_paths)}")
for path in trace_paths:
    top = collections.Counter()
    payload = collections.Counter()
    parse_errors = []
    agent_messages = []
    line_count = 0
    for line_count, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            record = json.loads(line)
        except Exception as error:  # pragma: no cover - audit diagnostic
            parse_errors.append((line_count, str(error)))
            continue
        top[record.get("type", "<none>")] += 1
        body = record.get("payload")
        if isinstance(body, dict):
            payload_type = body.get("type", "<none>")
            payload[payload_type] += 1
            if payload_type == "agent_message":
                message = body.get("message")
                if isinstance(message, str):
                    agent_messages.append((line_count, message))
    print(
        f"TRACE {path.relative_to(ROOT)} bytes={path.stat().st_size} "
        f"lines={line_count} sha256={digest(path)} parse_errors={parse_errors}"
    )
    print(f"top_types={dict(top)}")
    print(f"payload_types={dict(payload)}")
    print("agent_messages_bounded")
    for line_number, message in agent_messages:
        compact = " ".join(message.split())
        print(f"{line_number}: {compact[:1000]}")
