#!/usr/bin/env python3
"""Independently enumerate products of three primes below 100."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def is_prime(value: int) -> bool:
    return value >= 2 and all(value % divisor for divisor in range(2, value))


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: contract_set_check.py SPEC_K")
    spec = Path(sys.argv[1]).read_text()
    result_text = spec.split("<k>", 1)[1].split("</k>", 1)[0].split("=>", 1)[1]
    claimed = {int(x) for x in re.findall(r"A\s*==Int\s*(-?\d+)", result_text)}

    primes = [value for value in range(2, 100) if is_prime(value)]
    enumerated = {
        p * q * r
        for p in primes
        for q in primes
        for r in primes
        if p * q * r < 100
    }
    result = {
        "primes_below_100": primes,
        "claimed_values": sorted(claimed),
        "enumerated_three_prime_products_below_100": sorted(enumerated),
        "missing_from_claim": sorted(enumerated - claimed),
        "extra_in_claim": sorted(claimed - enumerated),
        "negative_inputs_cannot_be_products_of_positive_primes": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if claimed == enumerated else 1


if __name__ == "__main__":
    raise SystemExit(main())
