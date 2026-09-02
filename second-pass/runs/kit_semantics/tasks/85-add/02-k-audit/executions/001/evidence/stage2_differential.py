#!/usr/bin/env python3
"""Independent differential test against the trusted canonical entry point."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_add(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.add


canonical_add = load_add(Path("/reference/canonical.py"), "trusted_canonical")
generated_add = load_add(
    Path("/tmp/audit-work/fresh/solution.py"), "generated_solution"
)


def check(label: str, values: list[int]) -> None:
    expected = canonical_add(list(values))
    actual = generated_add(list(values))
    if actual != expected:
        raise AssertionError(
            f"{label}: input={values!r} canonical={expected!r} generated={actual!r}"
        )


def main() -> None:
    named_cases = [
        ("documented-example", [4, 2, 6, 7]),
        ("empty-outside-contract-boundary", []),
        ("singleton", [10]),
        ("singleton-zero", [0]),
        ("odd-index-even-positive", [1, 2]),
        ("odd-index-odd-positive", [1, 3]),
        ("odd-index-zero", [1, 0]),
        ("odd-index-even-negative", [1, -2]),
        ("odd-index-odd-negative", [1, -3]),
        ("even-index-even-must-skip", [2, 1]),
        ("both-branches-repeated", [2, 4, 6, 7, 8, -10]),
        ("large-magnitudes", [10**50, -(10**70), -3, 10**80]),
    ]
    checked = 0
    for label, values in named_cases:
        check(label, values)
        checked += 1

    # Exhaust every short list over values that cross sign, parity, and zero.
    alphabet = (-3, -2, -1, 0, 1, 2, 3)
    for length in range(0, 6):
        for values in itertools.product(alphabet, repeat=length):
            check(f"exhaustive-length-{length}", list(values))
            checked += 1

    generator = random.Random(850029)
    for case_index in range(2500):
        length = generator.randint(0, 80)
        values = [
            generator.choice(
                (
                    generator.randint(-10**6, 10**6),
                    generator.randint(-10**100, 10**100),
                )
            )
            for _ in range(length)
        ]
        check(f"generated-{case_index}", values)
        checked += 1

    print(
        f"DIFFERENTIAL checked={checked} mismatches=0 "
        "oracle=/reference/canonical.py generated=/tmp/audit-work/fresh/solution.py"
    )


if __name__ == "__main__":
    main()
