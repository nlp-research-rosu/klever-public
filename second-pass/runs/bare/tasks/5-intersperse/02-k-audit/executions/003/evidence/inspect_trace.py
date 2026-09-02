#!/usr/bin/env python3
"""Read every JSONL trace record and emit a bounded structural inventory."""

from __future__ import annotations

import collections
import json
import pathlib
import sys


def compact(value: object, limit: int = 500) -> str:
    text = json.dumps(value, sort_keys=True, ensure_ascii=False)
    return text if len(text) <= limit else text[:limit] + "...<truncated>"


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE_ROOT", file=sys.stderr)
        return 64
    root = pathlib.Path(sys.argv[1])
    paths = sorted(root.rglob("*"))
    files = [path for path in paths if path.is_file()]
    print(f"TRACE_ROOT {root}")
    print(f"FILES {len(files)}")
    for path in paths:
        kind = "symlink" if path.is_symlink() else "file" if path.is_file() else "dir"
        print(f"ENTRY {kind} {path.relative_to(root)}")

    type_counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    total = 0
    parse_errors = 0
    noteworthy: list[tuple[str, int, object]] = []
    for path in files:
        with path.open("r", encoding="utf-8") as stream:
            for lineno, line in enumerate(stream, 1):
                total += 1
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as error:
                    parse_errors += 1
                    noteworthy.append((str(path), lineno, {"parse_error": str(error)}))
                    continue
                rtype = str(record.get("type", "<none>"))
                type_counts[rtype] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    ptype = str(payload.get("type", "<none>"))
                    payload_counts[ptype] += 1
                    if ptype in {
                        "function_call",
                        "function_call_output",
                        "agent_message",
                        "user_message",
                    }:
                        noteworthy.append((str(path), lineno, record))
                elif rtype not in {"event_msg", "turn_context", "session_meta"}:
                    noteworthy.append((str(path), lineno, record))

    print(f"RECORDS {total}")
    print(f"PARSE_ERRORS {parse_errors}")
    print("TOP_LEVEL_TYPES " + compact(type_counts))
    print("PAYLOAD_TYPES " + compact(payload_counts))
    print(f"NOTEWORTHY {len(noteworthy)}")
    for path, lineno, record in noteworthy:
        print(f"AT {path}:{lineno} {compact(record)}")
    return 1 if parse_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
