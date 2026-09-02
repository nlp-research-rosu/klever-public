#!/usr/bin/env python3
"""Compare fresh concrete K results with independent Python prefix counts."""

from __future__ import annotations

from pathlib import Path


cases = [
    ("empty", "", 0),
    ("a", "a", 1),
    ("abc", "abc", 3),
    ("emoji", "🙂", 4),
    ("unicode", "a🙂b", 6),
]

mismatches = []
for label, string, expected_k_count in cases:
    number = {
        "empty": "05",
        "a": "06",
        "abc": "07",
        "unicode": "08",
        "emoji": "19",
    }[label]
    text = Path(f"/audit-output/evidence/{number}-krun-{label}.log").read_text(
        encoding="utf-8"
    )
    actual_k_count = text.count("strVal (")
    assert actual_k_count == expected_k_count, (label, actual_k_count, expected_k_count)
    python_result = [string[:i] for i in range(1, len(string) + 1)]
    print(
        f"case={label!r} python_prefix_count={len(python_result)} "
        f"k_prefix_count={actual_k_count} python_result={python_result!r}"
    )
    if actual_k_count != len(python_result):
        mismatches.append(label)

print(f"mismatch_count={len(mismatches)}")
print(f"mismatches={mismatches!r}")
raise SystemExit(1 if mismatches else 0)
