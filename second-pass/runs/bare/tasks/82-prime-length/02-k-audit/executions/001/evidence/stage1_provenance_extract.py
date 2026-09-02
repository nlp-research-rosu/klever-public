#!/usr/bin/env python3
"""Bounded extraction from untrusted generation logs and structured trace."""

from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: stage1_provenance_extract.py CODEX_LOG TRACE_JSONL")
    log_path = Path(sys.argv[1])
    trace_path = Path(sys.argv[2])

    raw = log_path.read_text(encoding="utf-8", errors="replace")
    lines = raw.splitlines()
    needles = re.compile(
        r"(#Top|KPROVE|WarnStuck|Error|solution\.mpy|semantic\.k|"
        r"verification\.k|spec\.k|prove\.sh|byte-for-byte|RESULT:)",
        re.IGNORECASE,
    )
    matches = [(number, line) for number, line in enumerate(lines, 1) if needles.search(line)]
    print("CODEX_OUTPUT_SUMMARY")
    print(
        json.dumps(
            {
                "path": str(log_path),
                "bytes_read": len(raw.encode("utf-8", errors="replace")),
                "line_count": len(lines),
                "matching_line_count": len(matches),
                "sha256_checked_elsewhere": True,
            },
            sort_keys=True,
        )
    )
    print("FIRST_MATCHES")
    for number, line in matches[:60]:
        print(f"{number}: {line[:400]}")
    print("LAST_MATCHES")
    for number, line in matches[-60:]:
        print(f"{number}: {line[:400]}")

    event_counts = collections.Counter()
    user_messages = []
    final_messages = []
    with trace_path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            item = json.loads(line)
            payload = item.get("payload") or {}
            event_counts[payload.get("type")] += 1
            if payload.get("type") == "user_message":
                user_messages.append((line_number, payload))
            if payload.get("type") == "task_complete":
                final_messages.append((line_number, payload))
    print("TRACE_SUMMARY")
    print("event_counts", dict(sorted(event_counts.items(), key=lambda row: str(row[0]))))
    print("USER_MESSAGES")
    for line_number, payload in user_messages:
        print(line_number, json.dumps(payload, ensure_ascii=False)[:5000])
    print("TASK_COMPLETE_EVENTS")
    for line_number, payload in final_messages:
        print(line_number, json.dumps(payload, ensure_ascii=False)[:5000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
