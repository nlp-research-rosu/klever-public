#!/usr/bin/env python3
"""Concrete witnesses for every one of the eight entry-claim sort domains."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.right_angle_triangle


def claimed_result(a, b, c):
    return (
        a * a == b * b + c * c
        or b * b == a * a + c * c
        or c * c == a * a + b * b
    )


def main() -> None:
    root = Path("/tmp/audit-work/reconstruction")
    canonical = load(root / "canonical.py", "claim_witness_canonical")
    candidate = load(root / "solution.py", "claim_witness_candidate")
    sort_combinations = [
        ("iii", int, int, int),
        ("iif", int, int, float),
        ("ifi", int, float, int),
        ("iff", int, float, float),
        ("fii", float, int, int),
        ("fif", float, int, float),
        ("ffi", float, float, int),
        ("fff", float, float, float),
    ]

    count = 0
    for label, a_type, b_type, c_type in sort_combinations:
        for values, expected in (((3, 4, 5), True), ((1, 2, 3), False)):
            args = (
                a_type(values[0]),
                b_type(values[1]),
                c_type(values[2]),
            )
            formal = claimed_result(*args)
            trusted = canonical(*args)
            generated = candidate(*args)
            print(
                f"WITNESS claim=right-angle-{label} input={args!r} "
                f"formal={formal!r} canonical={trusted!r} candidate={generated!r}"
            )
            assert formal is expected
            assert trusted is formal
            assert generated is formal
            count += 1
    print(f"RESULT witnesses={count} all_agree=true")


if __name__ == "__main__":
    main()
