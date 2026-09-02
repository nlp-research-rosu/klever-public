#!/usr/bin/env python3
"""Ground satisfying witnesses for every target-claim precondition."""

import importlib.util


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.choose_num


canonical = load("/reference/canonical.py", "canonical_witness")
generated = load("/tmp/audit-work/solution.py", "generated_witness")


def largest_even_in_range(x: int, y: int) -> int:
    candidate = y - (y % 2)
    return candidate if x <= candidate else -1


witnesses = [
    (
        "all-positive-inputs",
        12,
        15,
        lambda x, y: x > 0 and y > 0,
        largest_even_in_range,
    ),
    (
        "even-upper-in-range",
        1,
        2,
        lambda x, y: x > 0 and y > 0 and y % 2 == 0 and x <= y,
        lambda _x, y: y,
    ),
    (
        "even-upper-before-range",
        3,
        2,
        lambda x, y: x > 0 and y > 0 and y % 2 == 0 and x > y,
        lambda _x, _y: -1,
    ),
    (
        "odd-upper-predecessor-in-range",
        1,
        3,
        lambda x, y: x > 0 and y > 0 and y % 2 == 1 and x < y,
        lambda _x, y: y - 1,
    ),
    (
        "odd-upper-no-even-in-range",
        3,
        3,
        lambda x, y: x > 0 and y > 0 and y % 2 == 1 and x >= y,
        lambda _x, _y: -1,
    ),
]

for label, x, y, precondition, rhs in witnesses:
    pre = precondition(x, y)
    expected = rhs(x, y)
    canon = canonical(x, y)
    actual = generated(x, y)
    assert pre
    assert expected == canon == actual
    print(
        f"{label}: X={x} Y={y} precondition={pre} "
        f"claimed={expected} canonical={canon} generated={actual}"
    )
