#!/usr/bin/env python3
"""Read an untrusted Codex JSONL trace without executing trace content."""

from __future__ import annotations

import collections
import json
import pathlib
import sys


def clipped(text: str, limit: int = 1200) -> str:
    text = text.replace("\x00", "\\0")
    return text if len(text) <= limit else text[:limit] + "...<clipped>"


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 64

    path = pathlib.Path(sys.argv[1])
    outer_counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    parse_errors: list[str] = []
    records: list[dict] = []

    with path.open("r", encoding="utf-8") as stream:
        for line_number, raw_line in enumerate(stream, 1):
            try:
                record = json.loads(raw_line)
            except Exception as error:  # audit evidence: report malformed input
                parse_errors.append(f"line {line_number}: {error}")
                continue
            records.append(record)
            outer_counts[str(record.get("type"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_counts[str(payload.get("type"))] += 1

    print(f"path={path}")
    print(f"records={len(records)}")
    print(f"parse_errors={len(parse_errors)}")
    print("outer_types=" + json.dumps(dict(sorted(outer_counts.items()))))
    print("payload_types=" + json.dumps(dict(sorted(payload_counts.items()))))
    for error in parse_errors:
        print(error)

    print("assistant_messages:")
    for index, record in enumerate(records, 1):
        payload = record.get("payload")
        if not isinstance(payload, dict):
            continue
        if payload.get("type") != "message" or payload.get("role") != "assistant":
            continue
        content = payload.get("content", [])
        texts = [
            item.get("text", "")
            for item in content
            if isinstance(item, dict)
            and item.get("type") in {"output_text", "input_text"}
        ]
        if texts:
            print(f"record {index}: {clipped(''.join(texts))}")

    print("commands_and_top_claims:")
    for index, record in enumerate(records, 1):
        payload = record.get("payload")
        if not isinstance(payload, dict):
            continue
        payload_text = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        if any(
            needle in payload_text
            for needle in ("kprove", "#Top", "KPROVE_PASSED", "rightTriangle")
        ):
            print(f"record {index}: {clipped(payload_text)}")

    return 0 if not parse_errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
