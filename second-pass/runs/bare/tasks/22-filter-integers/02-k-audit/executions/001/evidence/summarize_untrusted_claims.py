#!/usr/bin/env python3
"""Bounded inventory of candidate-supplied generation claims.

This script intentionally treats every parsed value as untrusted text.  It does
not use candidate code as an import or execute any candidate command.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


CANDIDATE = Path("/candidate")
TRACE_FILES = sorted((CANDIDATE / "codex-trace").rglob("*.jsonl"))


def digest(path: Path) -> tuple[bytes, str]:
    data = path.read_bytes()
    return data, hashlib.sha256(data).hexdigest()


for name in (
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
):
    path = CANDIDATE / name
    data, sha256 = digest(path)
    print(f"{name}: bytes={len(data)} sha256={sha256}")

for name in ("run-input.json", "metrics.json"):
    parsed = json.loads((CANDIDATE / name).read_text(encoding="utf-8"))
    print(f"{name} parsed value (UNTRUSTED):")
    print(json.dumps(parsed, indent=2, sort_keys=True))

print("codex-last.txt (UNTRUSTED):")
print((CANDIDATE / "codex-last.txt").read_text(encoding="utf-8").rstrip())

output_lines = (CANDIDATE / "codex-output.log").read_text(
    encoding="utf-8", errors="replace"
).splitlines()
markers = (
    "Claim proven without rewriting",
    "#Top",
    "WarnStuckClaimState",
    "[Error]",
    "RESULT:",
)
selected_lines = [
    f"{line_number}:{line}"
    for line_number, line in enumerate(output_lines, start=1)
    if any(marker in line for marker in markers)
]
print(f"codex-output.log total_lines={len(output_lines)}")
print("codex-output.log selected proof/result claims (UNTRUSTED, last 80):")
for line in selected_lines[-80:]:
    print(line)

for trace_path in TRACE_FILES:
    raw, sha256 = digest(trace_path)
    type_counts: Counter[tuple[str, str]] = Counter()
    complete_messages: list[str] = []
    for line_number, line in enumerate(raw.splitlines(), start=1):
        record = json.loads(line)
        record_type = str(record.get("type", "<missing>"))
        payload = record.get("payload")
        payload_type = (
            str(payload.get("type", "<missing>"))
            if isinstance(payload, dict)
            else "<non-object>"
        )
        type_counts[(record_type, payload_type)] += 1
        if (
            record_type == "event_msg"
            and payload_type == "task_complete"
            and isinstance(payload, dict)
        ):
            complete_messages.append(str(payload.get("last_agent_message", "")))
    print(
        f"trace={trace_path} bytes={len(raw)} sha256={sha256} "
        f"records={sum(type_counts.values())}"
    )
    for key, count in sorted(type_counts.items()):
        print(f"  {key[0]}/{key[1]}: {count}")
    print("  task_complete claims (UNTRUSTED):")
    for message in complete_messages:
        print(message)
