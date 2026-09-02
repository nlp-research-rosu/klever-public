#!/usr/bin/env python3
"""Bounded structural summary of the untrusted candidate JSONL trace."""

from __future__ import annotations

import collections
import json
import pathlib
import sys


def compact(value: object, limit: int = 600) -> str:
    rendered = json.dumps(value, sort_keys=True, ensure_ascii=False)
    if len(rendered) <= limit:
        return rendered
    return rendered[:limit] + f"... <{len(rendered) - limit} chars omitted>"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: trace_summary.py TRACE.jsonl", file=sys.stderr)
        return 64

    path = pathlib.Path(sys.argv[1])
    counts: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    bad_json: list[tuple[int, str]] = []
    first: list[tuple[int, object]] = []
    last: collections.deque[tuple[int, object]] = collections.deque(maxlen=5)

    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            try:
                item = json.loads(line)
            except Exception as error:  # The trace is untrusted input.
                bad_json.append((line_number, str(error)))
                continue
            item_type = str(item.get("type", "<missing>"))
            counts[item_type] += 1
            payload = item.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type", "<missing>"))] += 1
            summary = {
                "type": item_type,
                "payload_type": (
                    payload.get("type", "<missing>")
                    if isinstance(payload, dict)
                    else type(payload).__name__
                ),
            }
            if isinstance(payload, dict):
                if "role" in payload:
                    summary["role"] = payload["role"]
                if "name" in payload:
                    summary["name"] = payload["name"]
                if "content" in payload:
                    summary["content_preview"] = compact(payload["content"], 300)
            if len(first) < 5:
                first.append((line_number, summary))
            last.append((line_number, summary))

    print(f"TRACE={path}")
    print(f"VALID_JSON_LINES={sum(counts.values())}")
    print(f"TOP_LEVEL_TYPES={dict(sorted(counts.items()))}")
    print(f"PAYLOAD_TYPES={dict(sorted(payload_types.items()))}")
    print(f"BAD_JSON={bad_json}")
    print("FIRST_EVENTS")
    for line_number, summary in first:
        print(line_number, compact(summary))
    print("LAST_EVENTS")
    for line_number, summary in last:
        print(line_number, compact(summary))
    return 1 if bad_json else 0


if __name__ == "__main__":
    raise SystemExit(main())
