#!/usr/bin/env python3
"""Parse every structured trace record and report a bounded audit summary."""

from __future__ import annotations

import collections
import hashlib
import json
import sys
from pathlib import Path


def walk_strings(value: object):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from walk_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from walk_strings(item)


def main() -> int:
    trace_root = Path("/generation-evidence/codex-trace")
    trace_files = sorted(trace_root.rglob("*.jsonl"))
    print(f"trace_file_count={len(trace_files)}")
    malformed = 0
    total = 0
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    timestamps: list[str] = []
    matched_records: list[tuple[int, str]] = []
    needles = (
        "kompile",
        "kprove",
        "krun",
        "verification.k",
        "spec.k",
        "connection",
        "#Top",
        "WarnStuckClaimState",
        "test_solution.py",
    )
    for trace_path in trace_files:
        digest = hashlib.sha256(trace_path.read_bytes()).hexdigest()
        rel = trace_path.relative_to(trace_root)
        print(f"trace_file={rel} bytes={trace_path.stat().st_size} sha256={digest}")
        with trace_path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                total += 1
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as err:
                    malformed += 1
                    print(f"MALFORMED line={line_number} error={err}")
                    continue
                top_types[str(record.get("type", "<missing>"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type", "<missing>"))] += 1
                timestamp = record.get("timestamp")
                if isinstance(timestamp, str):
                    timestamps.append(timestamp)
                strings = list(walk_strings(record))
                if any(needle in string for needle in needles for string in strings):
                    summary = next(
                        (
                            string.replace("\n", " ")[:240]
                            for string in strings
                            if any(needle in string for needle in needles)
                        ),
                        "",
                    )
                    matched_records.append((line_number, summary))
    print(f"record_count={total}")
    print(f"malformed_count={malformed}")
    print(f"top_level_types={dict(sorted(top_types.items()))}")
    print(f"payload_types={dict(sorted(payload_types.items()))}")
    print(f"first_timestamp={min(timestamps) if timestamps else None}")
    print(f"last_timestamp={max(timestamps) if timestamps else None}")
    print(f"relevant_record_count={len(matched_records)}")
    for line_number, summary in matched_records[:40]:
        print(f"relevant line={line_number}: {summary}")
    if len(matched_records) > 40:
        print("...")
        for line_number, summary in matched_records[-40:]:
            print(f"relevant line={line_number}: {summary}")
    return 1 if malformed else 0


if __name__ == "__main__":
    sys.exit(main())
