#!/usr/bin/env python3
"""Ground satisfying witnesses for every entry-claim precondition."""

from importlib.util import module_from_spec, spec_from_file_location


def load(path: str, name: str):
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rounded_avg


canonical = load("/reference/canonical.py", "canonical_witness")
generated = load("/candidate/solution.py", "generated_witness")


def py_mod(a: int, b: int) -> int:
    return ((a % b) + b) % b


witnesses = [
    ("inverted", 2, 1, lambda n, m: n > 0 and m > 0 and n > m, -1),
    (
        "integral",
        1,
        5,
        lambda n, m: n > 0 and m > 0 and n <= m and py_mod(n + m, 2) == 0,
        bin((1 + 5) // 2),
    ),
    (
        "half_down",
        2,
        3,
        lambda n, m: n > 0
        and m > 0
        and n <= m
        and py_mod(n + m, 2) == 1
        and py_mod((n + m - 1) // 2, 2) == 0,
        bin((2 + 3 - 1) // 2),
    ),
    (
        "half_up",
        1,
        2,
        lambda n, m: n > 0
        and m > 0
        and n <= m
        and py_mod(n + m, 2) == 1
        and py_mod((n + m - 1) // 2, 2) == 1,
        bin(((1 + 2 - 1) // 2) + 1),
    ),
]

for name, n, m, guard, claimed in witnesses:
    actual = generated(n, m)
    reference = canonical(n, m)
    print(
        f"{name}: input=({n},{m}) guard={guard(n,m)} "
        f"claim={claimed!r} generated={actual!r} canonical={reference!r}"
    )
    if not guard(n, m) or claimed != actual or actual != reference:
        raise SystemExit(1)
