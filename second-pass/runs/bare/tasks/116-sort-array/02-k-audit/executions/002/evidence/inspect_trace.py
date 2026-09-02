#!/usr/bin/env python3
"""Parse every JSONL trace record and emit a bounded structural index."""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path


def compact(value: object, limit: int = 500) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    text = " ".join(text.split())
    if len(text) > limit:
        return text[:limit] + "...<truncated>"
    return text


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 64

    path = Path(sys.argv[1])
    counts: collections.Counter[str] = collections.Counter()
    parse_errors = 0
    line_count = 0
    for line_count, raw in enumerate(path.open(encoding="utf-8"), start=1):
        try:
            event = json.loads(raw)
        except json.JSONDecodeError as error:
            parse_errors += 1
            print(f"{line_count}: JSON_ERROR {error}")
            continue
        outer = event.get("type", "<missing>")
        payload = event.get("payload")
        inner = payload.get("type", "<none>") if isinstance(payload, dict) else "<none>"
        counts[f"{outer}/{inner}"] += 1
        selected: dict[str, object] = {}
        if isinstance(payload, dict):
            for key in (
                "type",
                "role",
                "name",
                "call_id",
                "status",
                "model_context_window",
                "output_tokens",
                "input_tokens",
            ):
                if key in payload:
                    selected[key] = payload[key]
            for key in ("message", "arguments", "output", "content"):
                if key in payload:
                    selected[key] = payload[key]
        print(f"{line_count}: {outer}/{inner} {compact(selected)}")

    print(f"TOTAL_LINES: {line_count}")
    print(f"PARSE_ERRORS: {parse_errors}")
    for key, value in sorted(counts.items()):
        print(f"COUNT {key}: {value}")
    return 1 if parse_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
