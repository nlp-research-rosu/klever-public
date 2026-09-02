#!/usr/bin/env python3
"""Compare K helper-function ground results with an independent oracle."""

from __future__ import annotations

import math
import re
from pathlib import Path


def is_prime_math(n: int) -> bool:
    if n < 2:
        return False
    return all(n % d for d in range(2, math.isqrt(n) + 1))


def prime_from_math(n: int, d: int) -> bool:
    return all(n % candidate for candidate in range(d, math.isqrt(n) + 1))


text = Path("/audit-output/evidence/stage5/summary-ground-tests.log").read_text()
result = r"<result>\s*intVal\s*\(\s*([01])\s*\)\s*~>\s*\.K\s*</result>"
summary_pattern = re.compile(
    r"SUMMARY n=(-?\d+)\n(.*?)(?=\nSUMMARY(?:_FROM)? |\nEXIT_STATUS:)",
    re.DOTALL,
)
from_pattern = re.compile(
    r"SUMMARY_FROM n=(-?\d+) d=(-?\d+)\n"
    r"(.*?)(?=\nSUMMARY_FROM |\nEXIT_STATUS:)",
    re.DOTALL,
)

summary_count = 0
for match in summary_pattern.finditer(text):
    n = int(match.group(1))
    actual_match = re.search(result, match.group(2), re.DOTALL)
    if actual_match is None:
        raise AssertionError(f"missing Summary result for n={n}")
    actual = bool(int(actual_match.group(1)))
    expected = is_prime_math(n)
    print(f"Summary({n}):k={actual}:oracle={expected}:match={actual == expected}")
    assert actual == expected
    summary_count += 1

from_count = 0
for match in from_pattern.finditer(text):
    n, d = map(int, match.group(1, 2))
    actual_match = re.search(result, match.group(3), re.DOTALL)
    if actual_match is None:
        raise AssertionError(f"missing SummaryFrom result for n={n}, d={d}")
    actual = bool(int(actual_match.group(1)))
    expected = prime_from_math(n, d)
    print(
        f"SummaryFrom({n},{d}):k={actual}:"
        f"oracle={expected}:match={actual == expected}"
    )
    assert actual == expected
    from_count += 1

print(f"summary_case_count={summary_count}")
print(f"summary_from_case_count={from_count}")
assert summary_count == 15
assert from_count == 8
