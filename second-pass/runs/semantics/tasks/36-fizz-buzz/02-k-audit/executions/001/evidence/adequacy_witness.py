#!/usr/bin/env python3
"""Ground witnesses for every submitted entry claim and the inner-loop claim."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fizz_buzz


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical_witness")
generated = load_entry(
    Path("/tmp/audit-work/fizz-buzz-audit/solution.py"), "generated_witness"
)

claimed = {-5: 0, 0: 0, 50: 0, 78: 2, 79: 3, 100: 3}
for n, post in claimed.items():
    oracle = canonical(n)
    subject = generated(n)
    print(
        f"entry n={n} pre_state=pristine_call "
        f"claimed={post} canonical={oracle} generated={subject} "
        f"matches={post == oracle == subject}"
    )
    if not (post == oracle == subject):
        raise SystemExit(1)

# Satisfies the inner claim with L=1, A=4, X=707, N=1000, I=12,
# scopeLoc=2, empty heap/stack, noRet, NoExc, and exit code 0.
a, x = 4, 707
start_x = x
while x > 0:
    if x % 10 == 7:
        a += 1
    x //= 10
print(
    "inner L=1 A=4 X=707 N=1000 I=12 CONT=.K "
    f"post_count={a} post_x={x} expected_count=6 "
    f"satisfies_pre={start_x >= 0} matches={a == 6 and x == 0}"
)
raise SystemExit(0 if a == 6 and x == 0 else 1)
