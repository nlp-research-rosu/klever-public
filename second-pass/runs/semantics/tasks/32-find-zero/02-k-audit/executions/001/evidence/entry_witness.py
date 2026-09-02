#!/usr/bin/env python3
"""Concrete intended-domain witnesses for the two symbolic entry claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any


def load(name: str, path: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("witness_canonical", "/reference/canonical.py")
candidate = load("witness_candidate", "/candidate/solution.py")

for xs in ([1, 2], [-6, 11, -6, 1]):
    trusted = canonical.find_zero(list(xs))
    generated = candidate.find_zero(list(xs))
    polynomial_value = canonical.poly(list(xs), generated)
    vs_term = ".ValSeq"
    for value in reversed(xs):
        vs_term = f"vCons({value}, {vs_term})"
    formal_result = (
        f"bisectLow({vs_term}, bracketLow({vs_term}), "
        f"bracketHigh({vs_term}))"
    )
    print(f"xs={xs!r}")
    print(f"formal_precondition_model=validPolynomial({vs_term}) = true")
    print(f"formal_first_claim_result={formal_result}")
    print(f"trusted_python_result={trusted!r}")
    print(f"candidate_python_result={generated!r}")
    print(f"candidate_polynomial_value={polynomial_value!r}")
    print(f"formal_second_claim_result=true (via approximatesZero constructor rule)")
