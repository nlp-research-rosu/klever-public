#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import random
from pathlib import Path
from typing import Callable


def load_entry(path: Path, module_name: str) -> Callable[[int], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    entry = getattr(module, "largest_divisor")
    assert callable(entry)
    return entry


def independent_oracle(n: int) -> int:
    if n <= 1:
        raise ValueError("oracle domain is n > 1")
    for candidate in range(n - 1, 0, -1):
        if n % candidate == 0:
            return candidate
    raise AssertionError("1 must divide every n")


def capture(function: Callable[[int], object], n: int) -> tuple[str, object]:
    try:
        return ("return", function(n))
    except Exception as error:  # This is intentional evidence for excluded cases.
        return ("raise", type(error).__name__)


def main() -> None:
    canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
    generated = load_entry(
        Path("/tmp/audit-work/case/solution.py"), "generated_solution"
    )

    documented = [15]
    lower_boundary = [2, 3, 4, 5, 6]
    branch_boundaries = [
        7,
        8,
        9,
        10,
        11,
        12,
        14,
        16,
        25,
        27,
        49,
        97,
        100,
        101,
    ]
    exhaustive = list(range(2, 5001))
    rng = random.Random(240024)
    generated_inputs = [rng.randint(2, 200_000) for _ in range(250)]
    inputs = sorted(
        set(documented + lower_boundary + branch_boundaries + exhaustive + generated_inputs)
    )

    mismatches: list[tuple[int, object, object, object]] = []
    for n in inputs:
        expected = independent_oracle(n)
        trusted = canonical(n)
        actual = generated(n)
        if trusted != expected or actual != expected:
            mismatches.append((n, trusted, actual, expected))

    print("formal/intended domain: integer n > 1")
    print(f"documented_examples={documented}")
    print(f"lower_boundary={lower_boundary}")
    print(f"branch_boundaries={branch_boundaries}")
    print("exhaustive_range=2..5000")
    print("generated_seed=240024")
    print("generated_count=250 generated_range=2..200000")
    print(f"unique_test_count={len(inputs)}")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print(f"first_mismatches={mismatches[:20]}")

    print("outside_domain_observations:")
    for n in [1, 0]:
        print(
            f"n={n} canonical={capture(canonical, n)} "
            f"generated={capture(generated, n)}"
        )

    assert not mismatches
    assert generated(15) == canonical(15) == 5
    assert generated(2) == canonical(2) == 1
    print("DIFFERENTIAL_TEST=PASS")


if __name__ == "__main__":
    main()
