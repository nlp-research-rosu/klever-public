#!/usr/bin/env python3
"""Bounded, reviewer-authored summary of the untrusted generation records."""

from __future__ import annotations

import collections
import json
import pathlib
import re
import sys


def flatten_text(value: object) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts: list[str] = []
        for item in value:
            if isinstance(item, dict):
                parts.append(str(item.get("text", item.get("output", ""))))
            else:
                parts.append(str(item))
        return " ".join(parts)
    return str(value)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: summarize_generation.py TRACE.jsonl CODEX-OUTPUT.log", file=sys.stderr)
        return 64

    trace_path = pathlib.Path(sys.argv[1])
    output_path = pathlib.Path(sys.argv[2])
    counts: collections.Counter[tuple[str, str, str]] = collections.Counter()
    interesting: list[str] = []

    with trace_path.open(encoding="utf-8") as trace_file:
        for line_number, line in enumerate(trace_file, 1):
            record = json.loads(line)
            payload = record.get("payload", {})
            outer_type = str(record.get("type", ""))
            inner_type = str(payload.get("type", ""))
            role = str(payload.get("role", ""))
            counts[(outer_type, inner_type, role)] += 1

            if inner_type in {"function_call", "function_call_output"}:
                name = payload.get("name", "")
                call_id = payload.get("call_id", "")
                body = flatten_text(
                    payload.get("arguments", payload.get("output", ""))
                )
                body = re.sub(r"\s+", " ", body)[:500]
                interesting.append(
                    f"trace:{line_number} {inner_type} {name} {call_id} {body}"
                )
            elif inner_type == "message" and role == "assistant":
                body = re.sub(r"\s+", " ", flatten_text(payload.get("content", "")))
                interesting.append(
                    f"trace:{line_number} assistant-message {body[:500]}"
                )

    print("TRACE COUNTS")
    for key, value in sorted(counts.items()):
        print(value, *key, sep="\t")
    print("TRACE COMMANDS AND ASSISTANT CLAIMS (BOUNDED)")
    for item in interesting:
        print(item)

    patterns = re.compile(
        r"kprove|kompile|krun|#Top|WarnStuckClaimState|"
        r"\\[Error\\]|randomized|RESULT:"
    )
    matched: list[tuple[int, str]] = []
    line_count = 0
    byte_count = 0
    with output_path.open(encoding="utf-8", errors="replace") as output_file:
        for line_count, line in enumerate(output_file, 1):
            byte_count += len(line.encode("utf-8", errors="replace"))
            if patterns.search(line):
                matched.append((line_count, line.rstrip()))

    print(f"CODEX OUTPUT: lines={line_count} bytes={byte_count} matches={len(matched)}")
    print("CODEX OUTPUT RELEVANT TAIL (AT MOST 300 MATCHES)")
    for line_number, line in matched[-300:]:
        print(f"output:{line_number}: {line[:1000]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
