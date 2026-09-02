#!/usr/bin/env python3
"""Independent fidelity checks for HumanEval/150 x_or_y."""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path
from typing import Any, Callable


SCRATCH = Path("/tmp/audit-work/150-x-or-y-review")


def load_entry(path: Path, module_name: str) -> Callable[[int, Any, Any], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.x_or_y


candidate = load_entry(SCRATCH / "solution.py", "audited_candidate")
canonical = load_entry(SCRATCH / "canonical.py", "trusted_canonical")


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    return all(n % divisor != 0 for divisor in range(2, math.isqrt(n) + 1))


def contract_oracle(n: int, x: Any, y: Any) -> Any:
    return x if is_prime(n) else y


def same(left: Any, right: Any) -> bool:
    return left == right and type(left) is type(right)


def main() -> int:
    documented = [7, 15]
    boundaries = [
        -100,
        -2,
        -1,
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        8,
        9,
        25,
        49,
        97,
    ]
    generated = list(range(-25, 301))
    rng = random.Random(150)
    generated.extend(rng.randint(-10_000, 10_000) for _ in range(200))
    ns = list(dict.fromkeys(documented + boundaries + generated))
    payloads = [
        (34, 12),
        (0, 1),
        ("prime", "composite"),
        ([], ["not-prime"]),
        (None, False),
    ]

    candidate_oracle_mismatches: list[tuple[Any, ...]] = []
    candidate_canonical_mismatches: list[tuple[Any, ...]] = []
    total = 0
    for n in ns:
        for x, y in payloads:
            total += 1
            got = candidate(n, x, y)
            expected = contract_oracle(n, x, y)
            reference = canonical(n, x, y)
            if not same(got, expected):
                candidate_oracle_mismatches.append((n, x, y, got, expected))
            if not same(got, reference):
                candidate_canonical_mismatches.append((n, x, y, got, reference))

    print(f"documented_examples={documented}")
    print(f"branch_boundaries={boundaries}")
    print(
        "branches represented: n<2; n==2 empty range; first divisor; "
        "later divisor; prime fallthrough"
    )
    print(f"unique_n_values={len(ns)} payload_pairs={len(payloads)} total_cases={total}")
    print(f"candidate_vs_contract_mismatches={len(candidate_oracle_mismatches)}")
    print(f"candidate_vs_canonical_mismatches={len(candidate_canonical_mismatches)}")
    print(
        "candidate_vs_canonical_mismatch_n_values="
        f"{sorted({row[0] for row in candidate_canonical_mismatches})}"
    )
    print(
        "candidate_vs_canonical_first_five="
        f"{candidate_canonical_mismatches[:5]!r}"
    )
    print(
        "judgment: the trusted canonical returns x for n<=0 despite the "
        "unrestricted prose contract; the candidate returns y and agrees "
        "with the mathematical primality oracle"
    )
    return 1 if candidate_oracle_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
