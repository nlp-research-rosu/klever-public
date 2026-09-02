#!/usr/bin/env python3
"""Ground witnesses for every claim precondition and claimed result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.x_or_y


def prime_from(n: int, divisor: int) -> bool:
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 1
    return True


generated = load_entry(
    "witness_generated", Path("/tmp/audit-work/rebuild/solution.py")
)
canonical = load_entry(
    "witness_canonical", Path("/tmp/audit-work/trusted/canonical.py")
)

# LOOP-SPEC: D=2 satisfies 2 <= D; this exact control state is reached at
# depth 17 in loop-head-depth-final.log for n=7, x=34, y=12.
d, n, x, y = 2, 7, 34, 12
loop_claim_result = x if prime_from(n, d) else y
print(
    f"LOOP-SPEC witness D={d},N={n},X={x},Y={y}:"
    f"precondition={2 <= d}:claimed={loop_claim_result}:"
    f"generated={generated(n, x, y)}:canonical={canonical(n, x, y)}"
)
assert 2 <= d
assert loop_claim_result == generated(n, x, y) == canonical(n, x, y) == 34

# Universal SPEC entry claim has no requires clause; the initial empty env,
# empty result, and these integer input cells therefore satisfy it.
n, x, y = 15, 8, 5
universal_claim_result = x if prime_from(n, 2) and n >= 2 else y
print(
    f"SPEC universal witness N={n},X={x},Y={y}:"
    f"precondition=True:claimed={universal_claim_result}:"
    f"generated={generated(n, x, y)}:canonical={canonical(n, x, y)}"
)
assert universal_claim_result == generated(n, x, y) == canonical(n, x, y) == 5

for label, n, x, y, claimed in [
    ("SPEC example-prime", 7, 34, 12, 34),
    ("SPEC example-composite", 15, 8, 5, 5),
]:
    print(
        f"{label} witness N={n},X={x},Y={y}:precondition=True:"
        f"claimed={claimed}:generated={generated(n, x, y)}:"
        f"canonical={canonical(n, x, y)}"
    )
    assert claimed == generated(n, x, y) == canonical(n, x, y)

# Also instantiate the universal theorem at the canonical-disagreement
# boundary.  This does not invalidate the theorem about the generated program;
# it makes the implementation-to-canonical difference explicit.
n, x, y = 0, 101, -303
universal_claim_result = y
print(
    f"SPEC universal n<=0 witness N={n},X={x},Y={y}:"
    f"claimed={universal_claim_result}:generated={generated(n, x, y)}:"
    f"canonical={canonical(n, x, y)}"
)
assert universal_claim_result == generated(n, x, y)
assert canonical(n, x, y) != universal_claim_result
