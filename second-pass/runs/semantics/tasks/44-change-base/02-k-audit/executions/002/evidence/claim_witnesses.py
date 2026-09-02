#!/usr/bin/env python3
"""Ground witnesses for both entry claims and their result terms."""

from __future__ import annotations

import importlib.util
from pathlib import Path


WORK = Path("/tmp/audit-work/44-change-base")


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, WORK / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.change_base


canonical = load("canonical_witness", "canonical.py")
generated = load("generated_witness", "solution.py")


def mathematical_digits(number: int, base: int) -> str:
    result = ""
    while number > 0:
        quotient, remainder = divmod(number, base)
        result = chr(48 + remainder) + result
        number = quotient
    return result


print(
    "APPLY_PRECONDITION_WITNESS="
    "X=8,B=3,K=.K,L=0,FRAMES=.Map,N=1,H=.Map,HL=0,"
    "ST=.List,EC=0; freshScopes(1,.Map)=true"
)
print(
    "MODULE_PRECONDITION_WITNESS="
    "X=8,B=3 with the exact ground cells shown in spec.k"
)
for x, base in [(0, 2), (1, 2), (8, 3), (9, 9), (31, 5), (999, 9)]:
    expected = mathematical_digits(x, base)
    left = canonical(x, base)
    right = generated(x, base)
    print(
        f"X={x} B={base} baseDigits_as_text={expected!r} "
        f"canonical={left!r} generated={right!r}"
    )
    assert left == expected == right
print("GROUND_WITNESSES=PASS")
