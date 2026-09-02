#!/usr/bin/env python3
"""Independently check the candidate's finite contract-prime table."""

from __future__ import annotations

import json


CANDIDATE_TABLE = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97,
]


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 1
    return True


expected = [n for n in range(0, 101) if is_prime(n)]
print(
    json.dumps(
        {
            "range": [0, 100],
            "candidate": CANDIDATE_TABLE,
            "independent": expected,
            "equal": CANDIDATE_TABLE == expected,
        },
        sort_keys=True,
    )
)
raise SystemExit(0 if CANDIDATE_TABLE == expected else 1)
