#!/usr/bin/env python3
"""Read untrusted generation records and emit a bounded structural summary."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path
import re


CANDIDATE = Path("/candidate")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


for name in ("run-input.json", "metrics.json"):
    path = CANDIDATE / name
    print(f"=== {name} ===")
    print(f"bytes={path.stat().st_size} sha256={digest(path)}")
    print(json.dumps(json.loads(path.read_text()), indent=2, sort_keys=True))

for name in ("codex-last.txt",):
    path = CANDIDATE / name
    print(f"=== {name} ===")
    print(f"bytes={path.stat().st_size} sha256={digest(path)}")
    print(path.read_text())

log_path = CANDIDATE / "codex-output.log"
log_text = log_path.read_text(errors="replace")
log_lines = log_text.splitlines()
pattern = re.compile(r"(kompile|krun|kprove|#Top|RESULT:|semantic\\.k|spec\\.k|verification\\.k)")
matches = [(number, line) for number, line in enumerate(log_lines, 1) if pattern.search(line)]
print("=== codex-output.log ===")
print(
    f"bytes={log_path.stat().st_size} lines={len(log_lines)} "
    f"sha256={digest(log_path)} relevant_matches={len(matches)}"
)
for number, line in matches[:100]:
    print(f"{number}: {line[:1000]}")
if len(matches) > 200:
    print(f"[... {len(matches) - 200} matching lines omitted ...]")
for number, line in matches[-100:]:
    if (number, line) not in matches[:100]:
        print(f"{number}: {line[:1000]}")

trace_paths = sorted((CANDIDATE / "codex-trace").rglob("*.jsonl"))
print("=== structured generation trace ===")
print(f"files={len(trace_paths)}")
for path in trace_paths:
    type_counts: collections.Counter[str] = collections.Counter()
    role_counts: collections.Counter[str] = collections.Counter()
    payload_type_counts: collections.Counter[str] = collections.Counter()
    last_assistant_text = ""
    line_count = 0
    with path.open(errors="replace") as stream:
        for line_count, line in enumerate(stream, 1):
            record = json.loads(line)
            type_counts[str(record.get("type"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type_counts[str(payload.get("type"))] += 1
                role_counts[str(payload.get("role"))] += 1
                if payload.get("role") == "assistant":
                    content = payload.get("content")
                    if isinstance(content, list):
                        pieces = [
                            item.get("text", "")
                            for item in content
                            if isinstance(item, dict) and isinstance(item.get("text"), str)
                        ]
                        if pieces:
                            last_assistant_text = "\n".join(pieces)
    print(
        f"path={path} bytes={path.stat().st_size} lines={line_count} "
        f"sha256={digest(path)}"
    )
    print(f"record_types={dict(sorted(type_counts.items()))}")
    print(f"payload_types={dict(sorted(payload_type_counts.items()))}")
    print(f"roles={dict(sorted(role_counts.items()))}")
    if last_assistant_text:
        print("last_assistant_text:")
        print(last_assistant_text[:4000])
