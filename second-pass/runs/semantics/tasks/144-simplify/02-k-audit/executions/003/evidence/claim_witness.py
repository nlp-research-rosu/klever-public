#!/usr/bin/env python3
"""Ground witnesses for the entry precondition and claimed result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.simplify


def py_mod(dividend: int, divisor: int) -> int:
    # All witnesses have positive divisors, so K pyMod and Python % agree.
    return dividend % divisor


def main() -> None:
    canonical = load("/reference/canonical.py", "claim_witness_canonical")
    generated = load("/candidate/solution.py", "claim_witness_generated")
    witnesses = [
        (1, 5, 5, 1),
        (1, 6, 2, 1),
        (7, 10, 10, 2),
        (1, 1, 1, 1),
    ]
    for a, b, c, d in witnesses:
        precondition = a > 0 and b > 0 and c > 0 and d > 0
        claimed = py_mod(a * c, b * d) == 0
        x = f"{a}/{b}"
        n = f"{c}/{d}"
        abstract_k_inputs = (
            f"str(fractionCodes({a},{b}))",
            f"str(fractionCodes({c},{d}))",
        )
        concrete_k_inputs = (
            "str(" + ",".join(str(ord(ch)) for ch in x) + ")",
            "str(" + ",".join(str(ord(ch)) for ch in n) + ")",
        )
        print(
            f"A={a} B={b} C={c} D={d} precondition={precondition} "
            f"claimed={claimed} generated={generated(x, n)} canonical={canonical(x, n)}"
        )
        print(f"  claim_inputs={abstract_k_inputs}")
        print(f"  actual_texts={(x, n)} codepoints={concrete_k_inputs}")


if __name__ == "__main__":
    main()
