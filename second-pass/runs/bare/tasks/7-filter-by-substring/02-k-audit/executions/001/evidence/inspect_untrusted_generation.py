#!/usr/bin/env python3
"""Read the full untrusted generation records and summarize their claims."""

from __future__ import annotations

import collections
import json
from pathlib import Path
from typing import Any, Iterable


CANDIDATE = Path("/candidate")
TRACE = (
    CANDIDATE
    / "codex-trace/2026/07/22/"
    / "rollout-2026-07-22T03-47-52-019f8902-899a-77b0-80ed-82a38b5648a8.jsonl"
)
KEYWORDS = [
    "kompile",
    "krun",
    "kprove",
    "#Top",
    "KPROVE_PASSED",
    "vacuity",
    "UNIVERSAL-PROGRAM-REDUCTION",
    "UNIVERSAL-STEP-KEEP",
    "UNIVERSAL-STEP-DROP",
]


def strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from strings(child)


def main() -> int:
    print("RUN_INPUT_JSON:")
    print((CANDIDATE / "run-input.json").read_text(encoding="utf-8").rstrip())
    print()
    print("METRICS_JSON:")
    print((CANDIDATE / "metrics.json").read_text(encoding="utf-8").rstrip())
    print()
    print("CODEX_LAST:")
    print((CANDIDATE / "codex-last.txt").read_text(encoding="utf-8").rstrip())
    print()

    output = (CANDIDATE / "codex-output.log").read_text(
        encoding="utf-8", errors="replace"
    )
    print(f"CODEX_OUTPUT_BYTES_READ: {len(output.encode('utf-8'))}")
    print(f"CODEX_OUTPUT_LINES: {len(output.splitlines())}")
    for keyword in KEYWORDS:
        print(f"CODEX_OUTPUT_COUNT[{keyword!r}]: {output.count(keyword)}")
    print("CODEX_OUTPUT_FINAL_LINES:")
    for line in output.splitlines()[-20:]:
        print(line)
    print()

    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    keyword_counts: collections.Counter[str] = collections.Counter()
    malformed = 0
    line_count = 0
    byte_count = 0
    with TRACE.open("r", encoding="utf-8", errors="replace") as handle:
        for raw_line in handle:
            line_count += 1
            byte_count += len(raw_line.encode("utf-8"))
            try:
                record = json.loads(raw_line)
            except json.JSONDecodeError:
                malformed += 1
                continue
            top_types[str(record.get("type", "<missing>"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type", "<missing>"))] += 1
            joined = "\n".join(strings(record))
            for keyword in KEYWORDS:
                keyword_counts[keyword] += joined.count(keyword)

    print(f"TRACE_PATH: {TRACE}")
    print(f"TRACE_BYTES_READ: {byte_count}")
    print(f"TRACE_LINES: {line_count}")
    print(f"TRACE_MALFORMED_JSON_LINES: {malformed}")
    print(f"TRACE_TOP_TYPES: {dict(sorted(top_types.items()))}")
    print(f"TRACE_PAYLOAD_TYPES: {dict(sorted(payload_types.items()))}")
    for keyword in KEYWORDS:
        print(f"TRACE_COUNT[{keyword!r}]: {keyword_counts[keyword]}")
    return 0 if malformed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
