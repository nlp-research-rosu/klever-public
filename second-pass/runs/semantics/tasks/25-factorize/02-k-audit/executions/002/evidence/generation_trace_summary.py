#!/usr/bin/env python3
"""Read every structured generation trace event and emit a bounded audit summary."""

from __future__ import annotations

import collections
import glob
import hashlib
import json
from pathlib import Path


def compact(value: object, limit: int = 900) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit] + f"...[truncated {len(text) - limit} chars]"


def main() -> int:
    paths = sorted(glob.glob("/generation-evidence/codex-trace/**/*.jsonl", recursive=True))
    print(f"trace_file_count={len(paths)}")
    total = 0
    bad: list[tuple[str, int, str]] = []
    top_counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    for raw_path in paths:
        path = Path(raw_path)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"TRACE {path} sha256={digest}")
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                total += 1
                try:
                    event = json.loads(line)
                except Exception as err:
                    bad.append((raw_path, line_number, str(err)))
                    continue
                top_type = str(event.get("type", "<none>"))
                top_counts[top_type] += 1
                payload = event.get("payload")
                payload_type = payload.get("type", "<none>") if isinstance(payload, dict) else "<none>"
                payload_counts[str(payload_type)] += 1
                if payload_type in {
                    "user_message",
                    "agent_message",
                    "function_call",
                    "custom_tool_call",
                    "patch_apply_end",
                    "task_complete",
                }:
                    print(f"EVENT line={line_number} top={top_type} payload={payload_type} {compact(payload)}")
    print(f"total_lines_read={total}")
    print(f"bad_json={bad}")
    print(f"top_type_counts={dict(top_counts)}")
    print(f"payload_type_counts={dict(payload_counts)}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
