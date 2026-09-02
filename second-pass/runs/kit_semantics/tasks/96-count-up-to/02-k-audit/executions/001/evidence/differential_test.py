#!/usr/bin/env python3
"""Independent three-way differential test for HumanEval/96."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path
from types import ModuleType


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/candidate/solution.py")


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sieve_oracle(n: int) -> list[int]:
    """Independent prime sieve, not either implementation's trial-division loop."""
    if n <= 2:
        return []
    prime = bytearray(b"\x01") * n
    prime[0:2] = b"\x00\x00"
    limit = int((n - 1) ** 0.5)
    for p in range(2, limit + 1):
        if prime[p]:
            start = p * p
            count = ((n - 1 - start) // p) + 1
            prime[start:n:p] = b"\x00" * count
    return [value for value in range(2, n) if prime[value]]


def main() -> None:
    canonical = load_module("trusted_canonical_96", CANONICAL_PATH)
    candidate = load_module("generated_candidate_96", CANDIDATE_PATH)

    documented = {
        5: [2, 3],
        11: [2, 3, 5, 7],
        0: [],
        20: [2, 3, 5, 7, 11, 13, 17, 19],
        1: [],
        18: [2, 3, 5, 7, 11, 13, 17],
    }
    boundaries = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 17, 18, 19, 20, 21]
    exhaustive_small = list(range(0, 251))
    rng = random.Random(960029)
    generated = sorted(set(rng.randrange(251, 1001) for _ in range(100)))
    inputs = sorted(set(documented) | set(boundaries) | set(exhaustive_small) | set(generated))

    mismatches: list[dict[str, object]] = []
    for n in inputs:
        canonical_result = canonical.count_up_to(n)
        candidate_result = candidate.count_up_to(n)
        oracle_result = sieve_oracle(n)
        if n in documented and oracle_result != documented[n]:
            raise AssertionError(
                f"independent oracle contradicts documented example n={n}"
            )
        if not (canonical_result == candidate_result == oracle_result):
            mismatches.append(
                {
                    "n": n,
                    "canonical": canonical_result,
                    "candidate": candidate_result,
                    "sieve": oracle_result,
                }
            )

    print("oracle: independent Eratosthenes sieve")
    print("documented_examples:", json.dumps(documented, sort_keys=True))
    print("branch_boundaries:", json.dumps(boundaries))
    print("complete_input_scope:", json.dumps(inputs))
    print("input_count:", len(inputs))
    print("mismatch_count:", len(mismatches))
    if mismatches:
        print("mismatches:", json.dumps(mismatches, sort_keys=True))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
