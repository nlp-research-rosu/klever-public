#!/usr/bin/env python3
"""Independent differential check against trusted canonical.py and the contract."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_choose_num(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.choose_num


def contract_oracle(x: int, y: int) -> int:
    if x > y:
        return -1
    upper = y if y % 2 == 0 else y - 1
    return upper if upper >= x else -1


def main() -> None:
    canonical = load_choose_num(Path("canonical.py"), "trusted_canonical")
    generated = load_choose_num(Path("solution.py"), "generated_solution")

    named_cases = [
        ("prompt-even-below-top", 12, 15),
        ("prompt-empty-reversed", 13, 12),
        ("smallest-odd-singleton", 1, 1),
        ("smallest-even-top", 1, 2),
        ("even-singleton", 2, 2),
        ("odd-singleton", 3, 3),
        ("reversed-adjacent", 2, 1),
        ("even-lower-odd-upper", 4, 5),
        ("odd-lower-even-upper", 5, 6),
        ("odd-adjacent-no-even", 5, 5),
        ("large-even-singleton", 10**100, 10**100),
        ("large-odd-singleton", 10**100 + 1, 10**100 + 1),
        ("large-reversed", 10**100 + 2, 10**100),
    ]
    checks = 0
    for label, x, y in named_cases:
        expected = contract_oracle(x, y)
        observed_canonical = canonical(x, y)
        observed_generated = generated(x, y)
        assert observed_canonical == expected, (label, x, y, observed_canonical, expected)
        assert observed_generated == expected, (label, x, y, observed_generated, expected)
        print(f"{label}: ({x}, {y}) -> {expected}")
        checks += 1

    branch_counts = {"x>y": 0, "even-y": 0, "odd-has-even": 0, "odd-no-even": 0}
    for x in range(1, 301):
        for y in range(1, 301):
            expected = contract_oracle(x, y)
            assert canonical(x, y) == expected, (x, y, "canonical")
            assert generated(x, y) == expected, (x, y, "generated")
            if x > y:
                branch_counts["x>y"] += 1
            elif y % 2 == 0:
                branch_counts["even-y"] += 1
            elif y - 1 >= x:
                branch_counts["odd-has-even"] += 1
            else:
                branch_counts["odd-no-even"] += 1
            checks += 1

    rng = random.Random(102)
    for _ in range(10_000):
        x = rng.randint(1, 10**80)
        y = rng.randint(1, 10**80)
        expected = contract_oracle(x, y)
        assert canonical(x, y) == expected, (x, y, "canonical-generated")
        assert generated(x, y) == expected, (x, y, "candidate-generated")
        checks += 1

    print(f"branch_counts={branch_counts}")
    print(f"checks={checks} mismatches=0")
    print("DIFFERENTIAL=PASS")


if __name__ == "__main__":
    main()
