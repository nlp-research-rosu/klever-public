#!/usr/bin/env python3
"""Validate every trace record and produce a bounded semantic inventory."""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path


def walk_strings(value, key_path=()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk_strings(child, key_path + (str(key),))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_strings(child, key_path + (str(index),))
    elif isinstance(value, str):
        yield key_path, value


for argument in sys.argv[1:]:
    path = Path(argument)
    counts = collections.Counter()
    commands: list[tuple[int, str, str]] = []
    notable: list[tuple[int, str, str]] = []
    parsed = 0
    byte_count = 0

    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            byte_count += len(line.encode())
            record = json.loads(line)
            parsed += 1
            record_type = str(record.get("type", "<missing>"))
            counts[record_type] += 1

            for key_path, text in walk_strings(record):
                last = key_path[-1] if key_path else ""
                lowered = text.lower()
                if last in {"cmd", "command"}:
                    commands.append((line_number, ".".join(key_path), text))
                elif (
                    "kprove" in lowered
                    or "kompile" in lowered
                    or "verification.k" in lowered
                    or "spec.k" in lowered
                    or "opaque" in lowered
                ):
                    one_line = " ".join(text.split())
                    if len(one_line) > 500:
                        one_line = one_line[:500] + "...[bounded]"
                    notable.append((line_number, ".".join(key_path), one_line))

    print(f"FILE: {path}")
    print(f"VALID_JSONL_RECORDS: {parsed}")
    print(f"BYTES_READ: {byte_count}")
    print("TOP_LEVEL_TYPE_COUNTS:")
    for key, value in sorted(counts.items()):
        print(f"  {key}: {value}")
    print("COMMAND_STRINGS:")
    for line_number, key_path, text in commands:
        print(f"  line {line_number} {key_path}: {text}")
    print("NOTABLE_STRINGS (bounded; duplicates retained as trace evidence):")
    for line_number, key_path, text in notable:
        print(f"  line {line_number} {key_path}: {text}")
